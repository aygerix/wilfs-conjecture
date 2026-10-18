#!/usr/bin/python3
"""Reproducible cross-checks; all writes are confined to this directory."""
import sys
sys.dont_write_bytecode = True
import argparse
import itertools as it
import json
import math
import random
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import enumerate as e
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'scratch'))
from ns import NS
from cl import factorizations_down_set
from hcr_shape import hcr_shape
import tile_enum as ref


def intersection_vertices(cons, d):
    """Independent H-to-V conversion by all intersections of d-1 planes."""
    ee = tuple(tuple(int(i == j) for i in range(d)) for j in range(d))
    normals = tuple(set(ee+cons))
    vertices = set()
    for rows in it.combinations(normals, d-1):
        x = tuple((-1)**i*e.determinant([row[:i]+row[i+1:] for row in rows])
                  for i in range(d))
        if not any(x) or not sum(x):
            continue
        x = e.vertex(x)
        if all(e.dot(v, x) >= 0 for v in normals):
            vertices.add(x)
    return vertices


def geometry_tests():
    tests = 0
    for d in (3, 4):
        assert e.normalized_volume(e.polytope((), d), d) == 1
        chain = tuple(tuple(int(j == i)-int(j == i+1) for j in range(d))
                      for i in range(d-1))
        for k in range(1, d):
            assert e.normalized_volume(e.polytope(chain[:k], d), d) == F(1, math.factorial(k+1))
            tests += 1
        # Redundancy, clipping through old edges/vertices, nonsimple vertices.
        for cons in (chain+chain, chain+((1,)*d,), tuple(reversed(chain))):
            faces = e.polytope(cons, d)
            assert e.normalized_volume(faces, d) == F(1, math.factorial(d))
            assert {x for _, f in faces for x in f} == intersection_vertices(cons, d)
            tests += 1
    return tests


def orbit_tests():
    tested = 0
    for m in range(2, 8):
        brute = {}
        for r in it.product(range(m), repeat=4):
            if math.gcd(m, *r) == 1:
                c, _ = e.canonicalize(m, r)
                brute[c] = brute.get(c, 0)+1
        actual = {r:n for r,n,_,_ in e.canonical_residues(m)}
        assert brute == actual
        tested += sum(brute.values())
    return tested


def dimension_tests():
    results = []
    for m in range(4, 11):
        total = embedded = 0
        assert [r for r,*_ in e.canonical_residues(m, 3, 'minimal')] == ref.canonical_residues(m)
        for r in ref.canonical_residues(m):
            old = ref.enumerate_lattice(m, r)
            new = e.enumerate_lattice(m, r)
            assert set(old) == set(new)
            total += len(new)
            # The zero residue makes the fourth coordinate unused for ALL
            # positive weights. This checks a full 4-D fan, not one slice.
            lifted = e.enumerate_lattice(m, r+(0,))
            assert set(lifted) == {frozenset(x+(0,) for x in D) for D in old}
            embedded += len(lifted)
        result = dict(m=m, reference_tiles=total, unused_coordinate_tiles=embedded,
                      lattices=len(ref.canonical_residues(m)))
        print('DIMENSION '+json.dumps(result), flush=True)
        results.append(result)
    return results


def all_small_tests():
    tiles = hcrs = geometry = 0
    for m in range(5, 9):
        for r,*_ in e.canonical_residues(m):
            T = e.enumerate_lattice(m, r)
            for D, (cons, faces, volume) in T.items():
                tiles += 1
                assert float(e.hcr_exact(D)) == hcr_shape(D)
                hcrs += 1
                if m <= 7:
                    assert {x for _, f in faces for x in f} == intersection_vertices(cons, 4)
                    geometry += 1
        print('SMALL '+json.dumps(dict(m=m, cumulative_tiles=tiles)), flush=True)
    return dict(tiles=tiles, hcr_crosschecks=hcrs, independent_vertex_crosschecks=geometry)


def random_tests(n, seed, mmax):
    rng = random.Random(seed)
    cache, samples, distinct = {}, [], set()
    attempts, ties = 0, 0
    while len(samples) < n:
        m = rng.randrange(5, mmax+1)
        residues = rng.sample(range(1, m), 4)
        gens = tuple(sorted([m]+[m*rng.randrange(1, 13)+r for r in residues]))
        attempts += 1
        if gens in distinct or math.gcd(*gens) != 1:
            continue
        s = NS.from_generators(gens)
        if s.e != 5 or s.m != m:
            continue
        distinct.add(gens)
        pp, best = factorizations_down_set(s, 'grlex')
        r = tuple(p % m for p in pp)
        c, perm = e.canonicalize(m, r)
        key = m, c
        if key not in cache:
            cache[key] = e.enumerate_lattice(m, c)
        D = frozenset(best.values())
        Dc = frozenset(tuple(x[i] for i in perm) for x in D)
        assert Dc in cache[key], dict(gens=gens, r=r, c=c, tile=sorted(Dc))
        # Direct shortest path uses the original coordinate order, including
        # grlex ties; this is checked separately from canonical membership.
        assert D == e.tile_for_weight(m, r, tuple(pp))
        cons = e.cone_constraints(m, r, D)
        ties += any(e.dot(v, pp) == 0 for v in cons)
        samples.append(dict(generators=gens, canonical_r=c))
        if len(samples) % 500 == 0:
            print('RANDOM '+json.dumps(dict(accepted=len(samples), attempts=attempts,
                                           lattices=len(cache), ties=ties)), flush=True)
    return dict(seed=seed, requested=n, accepted=len(samples), distinct_semigroups=len(distinct),
                attempts=attempts, m_range=[5,mmax], lattices=len(cache),
                boundary_weight_cases=ties, missing=0, samples=samples)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--samples', type=int, default=2000)
    p.add_argument('--seed', type=int, default=20261018)
    p.add_argument('--mmax', type=int, default=14)
    p.add_argument('--seconds', type=float, default=270)
    args = p.parse_args()
    e.install_budget(args.seconds)
    t0 = time.monotonic()
    try:
        result = dict(geometry_tests=geometry_tests(), primitive_vectors=orbit_tests())
        result['dimension_reduction'] = dimension_tests()
        result['small_exhaustive'] = all_small_tests()
        result['random'] = random_tests(args.samples, args.seed, args.mmax)
        result['seconds'] = round(time.monotonic()-t0, 3)
        result['status'] = 'PASS'
        (HERE/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
        print('PASS '+json.dumps({k:v for k,v in result.items() if k != 'random'}), flush=True)
        return 0
    except e.BudgetExpired:
        print('INCOMPLETE: validation exceeded budget; no PASS result written.', flush=True)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
