#!/usr/bin/python3
"""Consolidate complete results and independently audit every HCR failure."""
import sys
sys.dont_write_bytecode = True
import argparse
import csv
import json
from fractions import Fraction as F
from pathlib import Path
import enumerate as e

sys.path.insert(0, str(e.HERE.parents[1]))
sys.path.insert(0, str(e.HERE.parents[0]))
from ns import NS
from cl import factorizations_down_set
from hcr_shape import hcr_shape


def independent_hcr(D):
    """Direct O(m^2 d) definition, independently of the dynamic program."""
    d, m = len(next(iter(D))), len(D)
    height = {x:max(sum(y)-sum(x) for y in D if all(a<=b for a,b in zip(x,y))) for x in D}
    H = 0
    for x in D:
        for a in range(d):
            t = x
            while t[:a]+(t[a]+1,)+t[a+1:] in D:
                t = t[:a]+(t[a]+1,)+t[a+1:]
            H += height[t]
    maxima = sorted((d+sum(x) for x in D if height[x] == 0), reverse=True)
    return F(2*((m+1)*H+sum(i*x for i,x in enumerate(maxima))), (d-1)*m*(m-1))


def audit_failure(f):
    m, r = f['m'], tuple(f['r'])
    D = frozenset(tuple(x) for x in f['tile'])
    h = independent_hcr(D)
    assert h == F(f['hcr']) == e.hcr_exact(D) and h < 1
    assert float(h) == hcr_shape(D)
    e.check_tile(m, r, D)
    cons = e.cone_constraints(m, r, D)
    faces = e.polytope(cons, 4)
    center = e.barycenter(sorted({x for _, face in faces for x in face}))
    # Try modest integer weights in the prescribed residue classes. Strict
    # feasibility is checked, so this search is never a sampling certificate.
    for scale in range(1, 10001):
        pp = tuple(m*(1+scale*x//sum(center))+a for x,a in zip(center,r))
        if all(e.dot(v, pp) > 0 for v in cons):
            break
    else:
        raise RuntimeError('No small semigroup witness found for '+str(f))
    assert e.tile_for_weight(m, r, pp) == D
    if all(tuple(int(i == a) for i in range(4)) in D for a in range(4)):
        s = NS.from_generators([m,*pp])
        assert s.e == 5 and s.m == m
        sorted_pp = [p for p in s.P if p != m]
        perm = [sorted_pp.index(p) for p in pp]
        actual_pp, best = factorizations_down_set(s, 'grlex', perm)
        assert actual_pp == list(pp) and frozenset(best.values()) == D
        f = dict(f, witness_generators=[m,*pp], witness_wilf_defect=s.W)
    return dict(f, independent_hcr_check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds', type=float, default=120)
    p.add_argument('--domain', choices=['all','minimal'], default='all')
    args = p.parse_args()
    e.install_budget(args.seconds)
    results = sorted((json.loads(path.read_text()) for path in e.HERE.glob(f'results_{args.domain}_*.json')),
                     key=lambda r:r['m'])
    failures = [audit_failure(f) for r in results for f in r['hcr_failures']]
    (e.HERE/f'hcr_failures_{args.domain}.json').write_text(json.dumps(failures, indent=2)+'\n')
    columns = ['m','lattices','tiles','non_two_face','certificate','min_hcr',
               'minimal_generator_lattices','minimal_generator_tiles','seconds']
    with (e.HERE/f'table_{args.domain}.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    lines = ['# Complete results', '',
             'Lattices are unit/permutation classes; tiles are counted per canonical lattice.',
             'Default all-domain counts include zero/repeated residues. NT means non-two-face.',
             'V+F means exact rational volume sum 1 for every lattice, plus matched internal facets.', '',
             '| m | Lattices | Tiles | NT | Certificate | Min HCR | Minimal-residue lattices | Minimal-residue tiles | Seconds |',
             '|---:|---:|---:|---:|:---:|---:|---:|---:|---:|']
    for r in results:
        lines.append('| {m} | {lattices} | {tiles} | {non_two_face} | V+F | {min_hcr} | {minimal_generator_lattices} | {minimal_generator_tiles} | {seconds} |'.format(**r))
    lines += ['', '# Every HCR failure', '', f'Total: {len(failures)} lattice/tile pairs. Every exact tile is listed below.',
              'These are failures of the shape criterion, not of Wilf\'s conjecture.', '']
    for i,f in enumerate(failures,1):
        lines += [f'{i}. m={f["m"]}, r={tuple(f["r"])}, HCR={f["hcr"]}.',
                  '   Tile: `'+str([tuple(x) for x in f['tile']])+'`.']
        if 'witness_generators' in f:
            lines.append('   A semigroup witness, in tile coordinate order: `'+str(f['witness_generators'])+'`; Wilf defect '+str(f['witness_wilf_defect'])+'.')
    (e.HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(complete_m=[r['m'] for r in results], hcr_failures=len(failures),
                          tiles=sum(r['tiles'] for r in results))), flush=True)


if __name__ == '__main__':
    raise SystemExit(main())
