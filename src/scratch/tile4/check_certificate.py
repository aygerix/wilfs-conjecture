#!/usr/bin/python3
"""Check a saved fan without performing any facet traversal or flips.

Reconstruct every closed cone from its saved tile; verify a strict weight
witness, distinct tiles, all down-set/residue conditions, each exact volume,
and the exact total 1 per lattice. Check that every canonical lattice occurs.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import gzip
import json
import time
from fractions import Fraction as F
from pathlib import Path
import enumerate as e


def check_record(m, record):
    """A single-lattice volume certificate, suitable for a VM worker."""
    r = tuple(record['r'])
    distinct, total, non_two, minimum, failures = set(), F(0), 0, None, []
    assert len(record['tile_cells']) == len(record['cone_volumes']) == record['tiles']
    for cells, volume in zip(record['tile_cells'], record['cone_volumes']):
        D = frozenset(tuple(x) for x in cells)
        assert len(cells) == len(D) and D not in distinct
        distinct.add(D)
        e.check_tile(m, r, D)
        cons = e.cone_constraints(m, r, D)
        faces = e.polytope(cons, 4)
        pts = sorted({x for _, f in faces for x in f})
        p = e.barycenter(pts)
        assert min(p) > 0 and all(e.dot(p, v) > 0 for v in cons)
        assert e.tile_for_weight(m, r, p) == D
        v = e.normalized_volume(faces, 4)
        assert volume == 'None' or v == F(volume)
        total += v
        non_two += e.non_two_face(D)
        h = e.hcr_exact(D)
        minimum = h if minimum is None else min(minimum, h)
        if h < 1:
            failures.append(dict(m=m, r=list(r), hcr=str(h), tile=e.tile_record(D)))
    assert total == 1, (m, r, total)
    return dict(r=r, tiles=len(distinct), non_two_face=non_two, min_hcr=str(minimum),
                hcr_failures=failures, tuple_orbit=record['tuple_orbit'],
                lattice_orbit=record['lattice_orbit'], sorted_orbit=record['sorted_orbit'])


def check(m, domain):
    path = e.HERE/f'certificate_{domain}_{m}.jsonl.gz'
    expected = {r:(a,b,c) for r,a,b,c in e.canonical_residues(m, 4, domain)}
    seen_lattices, tiles, non_two, minimum, failures = set(), 0, 0, None, []
    with gzip.open(path, 'rt') as stream:
        for line in stream:
            record = json.loads(line)
            r = tuple(record['r'])
            assert r in expected and r not in seen_lattices
            assert expected[r] == (record['tuple_orbit'], record['lattice_orbit'], record['sorted_orbit'])
            seen_lattices.add(r)
            distinct, total = set(), F(0)
            assert len(record['tile_cells']) == len(record['cone_volumes']) == record['tiles']
            for cells, volume in zip(record['tile_cells'], record['cone_volumes']):
                D = frozenset(tuple(x) for x in cells)
                assert len(cells) == len(D) and D not in distinct
                distinct.add(D)
                e.check_tile(m, r, D)
                cons = e.cone_constraints(m, r, D)
                faces = e.polytope(cons, 4)
                pts = sorted({x for _, f in faces for x in f})
                p = e.barycenter(pts)
                assert min(p) > 0 and all(e.dot(p, v) > 0 for v in cons)
                # Verifies this is the tile of a strictly interior weight.
                assert e.tile_for_weight(m, r, p) == D
                v = e.normalized_volume(faces, 4)
                assert volume == 'None' or v == F(volume)
                total += v
                tiles += 1
                non_two += e.non_two_face(D)
                h = e.hcr_exact(D)
                minimum = h if minimum is None else min(minimum, h)
                if h < 1:
                    failures.append(dict(m=m, r=list(r), hcr=str(h), tile=e.tile_record(D)))
            assert total == 1, (m, r, total)
    assert seen_lattices == set(expected)
    result = json.loads((e.HERE/f'results_{domain}_{m}.json').read_text())
    assert (len(expected),tiles,non_two,str(minimum),failures) == (
        result['lattices'],result['tiles'],result['non_two_face'],result['min_hcr'],result['hcr_failures'])
    return dict(m=m, lattices=len(expected), tiles=tiles, min_hcr=str(minimum),
                hcr_failures=len(failures), status='PASS', certificate='exact-volume')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('m0', type=int)
    p.add_argument('m1', type=int, nargs='?')
    p.add_argument('--domain', choices=['all','minimal'], default='all')
    p.add_argument('--seconds', type=float, default=270)
    args = p.parse_args()
    e.install_budget(args.seconds)
    active = None
    try:
        for m in range(args.m0, (args.m1 or args.m0)+1):
            active = m
            t0 = time.monotonic()
            result = check(m, args.domain)
            result['seconds'] = round(time.monotonic()-t0, 3)
            (e.HERE/f'checked_{args.domain}_{m}.json').write_text(json.dumps(result, indent=2)+'\n')
            print(json.dumps(result), flush=True)
    except e.BudgetExpired:
        print(json.dumps(dict(incomplete_m=active, status='checker budget reached')), flush=True)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
