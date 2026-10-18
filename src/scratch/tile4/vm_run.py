#!/usr/bin/python3
"""Eight-core, time-bounded GCP driver; never invoke on the laptop.

Each lattice is independent. A parent writes certificates in canonical
lattice order; workers do all fan/HCR computations. A second worker pass
checks saved cones without performing traversal or flips.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import gzip
import json
import math
import multiprocessing as mp
import os
import socket
import subprocess
import time
from datetime import datetime, timezone
from fractions import Fraction as F
import enumerate as e
from check_certificate import check_record

HOST = socket.gethostname()


def atomic_json(path, value):
    tmp = path.with_suffix(path.suffix+'.part')
    tmp.write_text(json.dumps(value, indent=2)+'\n')
    tmp.replace(path)


def worker_enumerate(job):
    m, r, orbit, kernels, sorted_orbit = job
    T = e.enumerate_lattice(m, r)
    record = dict(r=r, tuple_orbit=orbit, lattice_orbit=kernels,
                  sorted_orbit=sorted_orbit, tiles=len(T), normalized_volume='1',
                  facet_closure=True, tile_cells=[e.tile_record(D) for D in T],
                  cone_volumes=[str(data[2]) for data in T.values()])
    minimum, witness, non_two, failures = None, None, 0, []
    for D in T:
        non_two += e.non_two_face(D)
        h = e.hcr_exact(D)
        if minimum is None or h < minimum:
            minimum, witness = h, dict(r=r, tile=e.tile_record(D))
        if h < 1:
            failures.append(dict(m=m, r=list(r), hcr=str(h), tile=e.tile_record(D)))
    detail = {k:v for k,v in record.items() if k not in ('tile_cells','cone_volumes')}
    stats = dict(detail=detail, min_hcr=str(minimum), min_hcr_witness=witness,
                 non_two_face=non_two, hcr_failures=failures)
    return json.dumps(record, separators=(',', ':')), stats


def worker_check(job):
    m, line = job
    return check_record(m, json.loads(line))


class Deadline(Exception):
    pass


class Driver:
    def __init__(self, seconds, workers, domain):
        self.start = time.monotonic()
        self.deadline = self.start+seconds
        self.workers, self.domain = workers, domain
        self.state = dict(host=HOST, pid=os.getpid(), workers=workers, domain=domain,
                          start_utc=datetime.now(timezone.utc).isoformat(),
                          budget_seconds=seconds, checked_m=[])
        self.last_update = 0

    def status(self, **kw):
        self.state.update(kw, elapsed_seconds=round(time.monotonic()-self.start,3),
                          remaining_seconds=round(self.deadline-time.monotonic(),3))
        atomic_json(e.HERE/'vm_status.json', self.state)
        self.last_update = time.monotonic()

    def iterate(self, fn, jobs, total, phase, m):
        # A fresh pool ensures an interrupted lattice cannot leak into a
        # subsequent m. Only the parent touches certificate/result files.
        self.status(phase=phase, active_m=m, lattices_done=0, lattices_total=total)
        ctx = mp.get_context('fork')
        pool = ctx.Pool(self.workers)
        completed = 0
        try:
            iterator = pool.imap(fn, jobs, chunksize=1)
            while completed < total:
                remaining = self.deadline-time.monotonic()
                if remaining <= 30:
                    raise Deadline('VM wall-clock budget reached')
                try:
                    item = iterator.next(timeout=min(10, remaining-20))
                except mp.TimeoutError:
                    self.status(lattices_done=completed)
                    continue
                completed += 1
                if time.monotonic()-self.last_update > 10:
                    self.status(lattices_done=completed)
                yield item
            pool.close()
            pool.join()
        except BaseException:
            pool.terminate()
            pool.join()
            raise
        self.status(lattices_done=completed)

    def enumerate_m(self, m):
        t0 = time.monotonic()
        lattices = list(e.canonical_residues(m, 4, self.domain))
        jobs = ((m,*lat) for lat in lattices)
        cert = e.HERE/f'certificate_{self.domain}_{m}.jsonl.gz'
        part = cert.with_suffix('.gz.part')
        details, failures = [], []
        nt = nn = orbit_sum = kernel_sum = minimal_l = minimal_t = 0
        minimum, witness = None, None
        with gzip.open(part, 'wt', compresslevel=1) as stream:
            for line, stats in self.iterate(worker_enumerate, jobs, len(lattices), 'enumerating', m):
                stream.write(line+'\n')
                detail = stats['detail']
                details.append(detail)
                nt += detail['tiles']
                nn += stats['non_two_face']
                orbit_sum += detail['tuple_orbit']
                kernel_sum += detail['lattice_orbit']
                r = detail['r']
                if 0 not in r and len(set(r)) == 4:
                    minimal_l += 1
                    minimal_t += detail['tiles']
                h = F(stats['min_hcr'])
                if minimum is None or h < minimum:
                    minimum, witness = h, stats['min_hcr_witness']
                failures.extend(stats['hcr_failures'])
        if self.domain == 'all':
            expected = F(m**4)
            for p in range(2,m+1):
                if m % p == 0 and all(p%k for k in range(2,math.isqrt(p)+1)):
                    expected *= 1-F(1,p**4)
            assert orbit_sum == expected and kernel_sum*len(e.units(m)) == orbit_sum
        result = dict(m=m, domain=self.domain, lattices=len(lattices), tiles=nt,
                      non_two_face=nn, certificate='exact-volume+facets',
                      min_hcr=str(minimum), min_hcr_witness=witness, hcr_failures=failures,
                      tuple_orbits_sum=orbit_sum, lattice_orbits_sum=kernel_sum,
                      minimal_generator_lattices=minimal_l, minimal_generator_tiles=minimal_t,
                      seconds=round(time.monotonic()-t0,3), lattices_detail=details,
                      certificate_file=cert.name, execution_host=HOST, workers=self.workers)
        part.replace(cert)
        atomic_json(e.HERE/f'results_{self.domain}_{m}.json', result)
        print('ENUMERATED '+json.dumps({k:v for k,v in result.items() if k not in
              ('lattices_detail','min_hcr_witness','hcr_failures')}), flush=True)
        return result

    def check_m(self, m):
        t0 = time.monotonic()
        expected = {r:(a,b,c) for r,a,b,c in e.canonical_residues(m, 4, self.domain)}
        cert = e.HERE/f'certificate_{self.domain}_{m}.jsonl.gz'
        seen, tiles, non_two, minimum, failures = set(), 0, 0, None, []
        with gzip.open(cert, 'rt') as stream:
            lines_read = [0]
            def jobs():
                for line in stream:
                    lines_read[0] += 1
                    yield m,line
            for record in self.iterate(worker_check, jobs(), len(expected), 'checking', m):
                r = tuple(record['r'])
                assert r in expected and r not in seen
                assert expected[r] == (record['tuple_orbit'],record['lattice_orbit'],record['sorted_orbit'])
                seen.add(r)
                tiles += record['tiles']
                non_two += record['non_two_face']
                h = F(record['min_hcr'])
                minimum = h if minimum is None else min(minimum,h)
                failures.extend(record['hcr_failures'])
            # Also reject extra records, beyond the expected count.
            assert lines_read[0] == len(expected) and stream.read() == ''
        assert seen == set(expected)
        result = json.loads((e.HERE/f'results_{self.domain}_{m}.json').read_text())
        assert (len(expected),tiles,non_two,str(minimum),failures) == (
            result['lattices'],result['tiles'],result['non_two_face'],result['min_hcr'],result['hcr_failures'])
        checked = dict(m=m, lattices=len(expected), tiles=tiles, min_hcr=str(minimum),
                       hcr_failures=len(failures), status='PASS', certificate='exact-volume',
                       seconds=round(time.monotonic()-t0,3), execution_host=HOST, workers=self.workers)
        atomic_json(e.HERE/f'checked_{self.domain}_{m}.json',checked)
        self.state['checked_m'].append(m)
        print('CHECKED '+json.dumps(checked), flush=True)
        return checked

    def reports(self):
        self.status(phase='reporting')
        subprocess.run(['/usr/bin/python3','-B',str(e.HERE/'report.py'),
                        '--domain',self.domain,'--seconds','240'], check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds', type=int, default=6900)
    p.add_argument('--workers', type=int, default=8)
    p.add_argument('--domain', choices=['all','minimal'], default='all')
    p.add_argument('--mmax', type=int, default=999)
    p.add_argument('--recheck-existing', action='store_true')
    p.add_argument('--mmin', type=int, default=5)
    args = p.parse_args()
    assert HOST.split('.')[0] == 'fejer', 'All computation must run on GCP fejer'
    assert 1 <= args.workers <= 8
    driver = Driver(args.seconds,args.workers,args.domain)
    last_pair = 0
    try:
        for m in range(args.mmin,args.mmax+1):
            t0 = time.monotonic()
            path = e.HERE/f'results_{args.domain}_{m}.json'
            cert = e.HERE/f'certificate_{args.domain}_{m}.jsonl.gz'
            existing = path.exists() and cert.exists()
            if not existing:
                # Reserve room for the independent checker. Ratios are
                # conservative; no partial m contributes an aggregate row.
                remaining = driver.deadline-time.monotonic()
                if last_pair and remaining < max(60,2*last_pair):
                    driver.status(phase='stopping_before_next_m',active_m=m,
                                  estimated_pair_seconds=round(last_pair,3))
                    break
                driver.enumerate_m(m)
            checked_path = e.HERE/f'checked_{args.domain}_{m}.json'
            checked_on_vm = (checked_path.exists() and
                             json.loads(checked_path.read_text()).get('execution_host','').split('.')[0] == 'fejer')
            if args.recheck_existing or not checked_on_vm:
                driver.check_m(m)
            if not existing:
                last_pair = time.monotonic()-t0
            driver.reports()
    except Deadline as exc:
        driver.status(phase='budget_reached',message=str(exc))
    except BaseException as exc:
        driver.status(phase='ERROR',error=repr(exc))
        raise
    driver.reports()
    driver.status(phase='finished',active_m=None)


if __name__ == '__main__':
    main()
