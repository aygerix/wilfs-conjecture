#!/usr/bin/python3
"""Exact positive-weight Apery fans in dimensions 3 and 4. See README.md.

All geometry, shortest paths, comparisons and HCR calculations use Python
integers or fractions.Fraction. Wall-clock time is used only for run budgets.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import gzip
import heapq
import itertools as it
import json
import math
import signal
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def primitive(v):
    g = math.gcd(*v)
    assert g
    return tuple(x//g for x in v)


def vertex(v):
    v = primitive(v)
    return v if sum(v) > 0 else tuple(-x for x in v)


def determinant(rows):
    """Bareiss elimination; unbounded integers, with checked exact divisions."""
    a = [list(row) for row in rows]
    n = len(a)
    sign, prev = 1, 1
    for k in range(n-1):
        j = next((j for j in range(k, n) if a[j][k]), None)
        if j is None:
            return 0
        if j != k:
            a[k], a[j] = a[j], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                q = a[i][j]*p - a[i][k]*a[k][j]
                assert q % prev == 0
                a[i][j] = q//prev
            a[i][k] = 0
        prev = p
    return sign*a[-1][-1]


def units(m):
    return tuple(u for u in range(1, m) if math.gcd(u, m) == 1)


def canonicalize(m, r):
    """Return canonical residues and permutation: new x[i] = old x[perm[i]]."""
    best = None
    for u in units(m):
        ur = tuple(u*x % m for x in r)
        perm = tuple(sorted(range(len(r)), key=lambda i: (ur[i], i)))
        c = tuple(ur[i] for i in perm)
        if best is None or c < best[0]:
            best = c, perm
    return best


def canonical_residues(m, d=4, domain='all'):
    """Yield (r, tuple orbit size, lattice orbit size, sorted orbit size).

    Primitive ordered residue vectors have free unit action. Thus each
    lattice kernel is represented by phi(m) vectors. Coordinate permutations
    can stabilize a lattice, so its orbit size need not be d!.
    """
    uu = units(m)
    candidates = (it.combinations(range(1, m), d) if domain == 'minimal'
                  else it.combinations_with_replacement(range(m), d))
    for r in candidates:
        if math.gcd(m, *r) != 1:
            continue
        orbit = {tuple(sorted(u*x % m for x in r)) for u in uu}
        if r != min(orbit):
            continue
        mult = math.factorial(d)
        for x in set(r):
            mult //= math.factorial(r.count(x))
        size = len(orbit)*mult
        assert size % len(uu) == 0
        yield r, size, size//len(uu), len(orbit)


def tile_for_weight(m, r, p, secondary=None):
    """Dijkstra for the order (p.x, secondary.x, |x|, x), p_i > 0."""
    d = len(r)
    assert len(p) == d and all(x > 0 for x in p)
    secondary = secondary or (0,)*d
    z = (0,)*d
    key = (0, 0, 0, z)
    best = {0: key}
    heap = [(key, 0)]
    done = {}
    while heap:
        k, g = heapq.heappop(heap)
        if g in done:
            continue
        w, w2, degree, x = k
        done[g] = x
        for a in range(d):
            h = (g+r[a]) % m
            if h in done:
                continue
            y = x[:a] + (x[a]+1,) + x[a+1:]
            k2 = w+p[a], w2+secondary[a], degree+1, y
            if h not in best or k2 < best[h]:
                best[h] = k2
                heapq.heappush(heap, (k2, h))
    assert len(done) == m
    return frozenset(done.values())


def check_tile(m, r, D):
    d = len(r)
    assert len(D) == m and len({dot(r, x) % m for x in D}) == m
    for x in D:
        assert len(x) == d and min(x) >= 0 and sum(x) <= m-1
        for a in range(d):
            if x[a]:
                assert x[:a]+(x[a]-1,)+x[a+1:] in D


def cone_constraints(m, r, D):
    d = len(r)
    reps = {dot(r, x) % m: x for x in D}
    cand = {x[:a]+(x[a]+1,)+x[a+1:] for x in D for a in range(d)} - D
    out = set()
    for q in cand:
        if all(not q[a] or q[:a]+(q[a]-1,)+q[a+1:] in D for a in range(d)):
            y = reps[dot(r, q) % m]
            out.add(primitive(tuple(x-z for x, z in zip(q, y))))
    return tuple(sorted(out))


def dedup_cycle(points):
    out = []
    for p in points:
        if not out or p != out[-1]:
            out.append(p)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return tuple(out)


def clip_polygon(poly, v):
    values = tuple(dot(P, v) for P in poly)
    if min(values) >= 0:
        return poly
    if max(values) <= 0:
        return tuple(P for P, value in zip(poly, values) if value == 0)
    out = []
    for i, P in enumerate(poly):
        Q = poly[(i+1) % len(poly)]
        a, b = values[i], values[(i+1) % len(poly)]
        if a >= 0:
            out.append(P)
        if a*b < 0:
            # Sign is immaterial after projective normalization.
            out.append(vertex(tuple(a*y-b*x for x, y in zip(P, Q))))
    return dedup_cycle(out)


def noncollinear(poly):
    """Exact affine rank test using homogeneous, denominator-cleared edges."""
    if len(poly) < 3:
        return False
    a, b = poly[:2]
    sa, sb = sum(a), sum(b)
    u = tuple(y*sa-x*sb for x,y in zip(a,b))
    pivot = next((i for i,x in enumerate(u) if x), None)
    assert pivot is not None
    for c in poly[2:]:
        sc = sum(c)
        v = tuple(z*sa-x*sc for x,z in zip(a,c))
        if any(u[pivot]*v[j] != v[pivot]*u[j] for j in range(len(a))):
            return True
    return False


def polytope(cons, d):
    """Facets (inward normal, cyclic projective vertices), exact clipping."""
    ee = tuple(tuple(int(i == j) for i in range(d)) for j in range(d))
    if d == 3:
        poly = ee
        for v in cons:
            poly = clip_polygon(poly, v)
        assert noncollinear(poly)
        faces = []
        for P, Q in zip(poly, poly[1:]+poly[:1]):
            normal = next(v for v in ee+cons if dot(v, P) == dot(v, Q) == 0)
            faces.append((normal, (P, Q)))
        return tuple(faces)
    assert d == 4
    faces = [(e, tuple(p for p in ee if p != e)) for e in ee]
    for v in cons:
        verts = {p for _, f in faces for p in f}
        signs = [dot(p, v) for p in verts]
        if min(signs) >= 0:
            continue
        assert max(signs) > 0, ('empty cone', cons)
        new = []
        edges = set()
        for n, f in faces:
            f = clip_polygon(f, v)
            if not noncollinear(f):
                continue
            new.append((n, f))
            for P, Q in zip(f, f[1:]+f[:1]):
                if dot(P, v) == dot(Q, v) == 0:
                    edges.add(tuple(sorted((P, Q))))
        graph = {}
        for P, Q in edges:
            graph.setdefault(P, set()).add(Q)
            graph.setdefault(Q, set()).add(P)
        assert len(graph) >= 3 and all(len(ns) == 2 for ns in graph.values())
        start = min(graph)
        cap, prev, cur = [start], None, start
        while True:
            nxt = min(graph[cur] - ({prev} if prev is not None else set()))
            if nxt == start:
                break
            assert nxt not in cap
            cap.append(nxt)
            prev, cur = cur, nxt
        assert len(cap) == len(graph)
        new.append((v, tuple(cap)))
        faces = new
    return tuple(faces)


def barycenter(points):
    """An integer positive multiple of the normalized vertex average."""
    den = math.lcm(*(sum(p) for p in points))
    return vertex(tuple(sum(p[i]*(den//sum(p)) for p in points)
                        for i in range(len(points[0]))))


def normalized_volume(faces, d):
    """Exact (d-1)-volume divided by volume of the standard simplex."""
    points = sorted({p for _, f in faces for p in f})
    ref = points[0]
    total = F(0)
    for _, f in faces:
        simplices = ([f] if d == 3 else
                     [(f[0], f[i], f[i+1]) for i in range(1, len(f)-1)])
        for facet_simplex in simplices:
            rows = (ref,)+tuple(facet_simplex)
            n = abs(determinant(rows))
            if n:
                total += F(n, math.prod(sum(p) for p in rows))
    assert total > 0
    return total


def hcr_exact(D):
    """Integer reformulation of src/scratch/hcr_shape.py; returns Fraction."""
    d, m = len(next(iter(D))), len(D)
    ht, tops = {}, {}
    Hn = 0
    maxima = []
    for x in sorted(D, key=lambda x: (-sum(x), x)):
        succ = [x[:a]+(x[a]+1,)+x[a+1:] for a in range(d)]
        ht[x] = max((ht[y]+1 for y in succ if y in D), default=0)
        tops[x] = tuple(tops[y][a] if y in D else x for a, y in enumerate(succ))
        Hn += sum(ht[t] for t in tops[x])
        if ht[x] == 0:
            maxima.append(d+sum(x))
    T = sorted(maxima, reverse=True)
    return F(2*((m+1)*Hn + sum(i*t for i, t in enumerate(T))),
             (d-1)*m*(m-1))


def non_two_face(D):
    """Same missing-pair criterion as the existing dimension-3 scan."""
    d = len(next(iter(D)))
    return all(tuple(int(i in (a, b)) for i in range(d)) in D
               for a, b in it.combinations(range(d), 2))


def enumerate_lattice(m, r, with_volume=True):
    """Return tile -> (constraints, facets, exact normalized volume).

    Each internal facet is crossed symbolically and checked against ALL its
    vertices. The returned set is then checked for closure under every flip.
    """
    d = len(r)
    start = tile_for_weight(m, r, (1,)*d)
    pending, queued = [start], {start}
    seen, links = {}, []
    cache = {}
    while pending:
        D = pending.pop()
        check_tile(m, r, D)
        cons = cache.pop(D, None)
        if cons is None:
            cons = cone_constraints(m, r, D)
        faces = polytope(cons, d)
        points = sorted({p for _, f in faces for p in f})
        center = barycenter(points)
        assert min(center) > 0 and all(dot(center, v) > 0 for v in cons)
        volume = normalized_volume(faces, d) if with_volume else None
        seen[D] = cons, faces, volume
        for n, f in faces:
            p = barycenter(f)
            if min(p) == 0:
                # A relative-interior point has a zero coordinate iff the
                # entire facet lies in that coordinate boundary.
                assert any(all(v[a] == 0 for v in f) for a in range(d))
                continue
            neg = tuple(-x for x in n)
            D2 = tile_for_weight(m, r, p, neg)
            assert D2 != D
            cons2 = (seen[D2][0] if D2 in seen else cache.get(D2))
            if cons2 is None:
                cons2 = cone_constraints(m, r, D2)
                cache[D2] = cons2
            assert all(dot(v, p) >= 0 for v in cons2)
            assert all(dot(v, neg) > 0 for v in cons2 if dot(v, p) == 0)
            assert all(dot(v, P) >= 0 for v in cons2 for P in f)
            assert tuple(-x for x in primitive(n)) in cons2
            links.append((D, D2, primitive(n), frozenset(f)))
            if D2 not in queued:
                queued.add(D2)
                pending.append(D2)
    assert queued == set(seen)
    # Reverse facet matching: both cells must exhibit the same facet, with
    # opposite inward normals. No floating or modular certificate is used.
    linkset = set(links)
    assert all((B, A, tuple(-x for x in n), f) in linkset for A, B, n, f in links)
    if with_volume:
        assert sum((x[2] for x in seen.values()), F(0)) == 1
    return seen


class BudgetExpired(Exception):
    pass


def install_budget(seconds):
    assert 0 < seconds <= 280, 'Every run must remain under five minutes'
    def stop(signum, frame):
        raise BudgetExpired('wall-clock budget reached')
    signal.signal(signal.SIGALRM, stop)
    signal.setitimer(signal.ITIMER_REAL, seconds)


def tile_record(D):
    return [list(x) for x in sorted(D)]


def scan(m, domain='all', facet_only=False, dump=False, certificate_stream=None):
    t0 = time.monotonic()
    nl = nt = nn = orbit_sum = kernel_sum = 0
    minimum, worst = None, None
    failures, lattice_records = [], []
    admissible_lattices = admissible_tiles = 0
    for r, orbit, kernels, sorted_orbit in canonical_residues(m, 4, domain):
        T = enumerate_lattice(m, r, not facet_only)
        nl += 1
        nt += len(T)
        orbit_sum += orbit
        kernel_sum += kernels
        admissible = 0 not in r and len(set(r)) == 4
        if admissible:
            admissible_lattices += 1
            admissible_tiles += len(T)
        record = dict(r=r, tuple_orbit=orbit, lattice_orbit=kernels,
                      sorted_orbit=sorted_orbit, tiles=len(T),
                      normalized_volume=None if facet_only else '1',
                      facet_closure=True)
        if dump:
            record['tile_cells'] = [tile_record(D) for D in T]
        if certificate_stream is not None:
            certificate_record = dict(record)
            certificate_record['tile_cells'] = [tile_record(D) for D in T]
            certificate_record['cone_volumes'] = [str(data[2]) for data in T.values()]
            certificate_stream.write(json.dumps(certificate_record, separators=(',', ':'))+'\n')
        lattice_records.append(record)
        for D in T:
            nn += non_two_face(D)
            h = hcr_exact(D)
            if minimum is None or h < minimum:
                minimum, worst = h, dict(r=r, tile=tile_record(D))
            if h < 1:
                failures.append(dict(m=m, r=r, hcr=str(h), tile=tile_record(D)))
    # Jordan totient counts all primitive tuples. Unit action is free.
    if domain == 'all':
        primes = [p for p in range(2, m+1) if m % p == 0 and
                  all(p % k for k in range(2, math.isqrt(p)+1))]
        expected = F(m**4)
        for p in primes:
            expected *= 1-F(1, p**4)
        assert orbit_sum == expected
        assert kernel_sum*len(units(m)) == orbit_sum
    return dict(m=m, domain=domain, lattices=nl, tiles=nt, non_two_face=nn,
                certificate='facets' if facet_only else 'exact-volume+facets',
                min_hcr=str(minimum), min_hcr_witness=worst,
                hcr_failures=failures, tuple_orbits_sum=orbit_sum,
                lattice_orbits_sum=kernel_sum,
                minimal_generator_lattices=admissible_lattices,
                minimal_generator_tiles=admissible_tiles,
                seconds=round(time.monotonic()-t0, 3), lattices_detail=lattice_records)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('m0', type=int)
    p.add_argument('m1', type=int, nargs='?')
    p.add_argument('--domain', choices=['all', 'minimal'], default='all')
    p.add_argument('--seconds', type=float, default=270)
    p.add_argument('--facet-only', action='store_true')
    p.add_argument('--dump', action='store_true')
    p.add_argument('--resume', action='store_true')
    args = p.parse_args()
    install_budget(args.seconds)
    active = None
    try:
        for m in range(args.m0, (args.m1 or args.m0)+1):
            active = m
            path = HERE / f'results_{args.domain}_{m}.json'
            cert = HERE / f'certificate_{args.domain}_{m}.jsonl.gz'
            if args.resume and path.exists() and cert.exists():
                result = json.loads(path.read_text())
            else:
                part = cert.with_suffix(cert.suffix+'.part')
                with gzip.open(part, 'wt', compresslevel=1) as stream:
                    result = scan(m, args.domain, args.facet_only, args.dump, stream)
                part.replace(cert)
                result['certificate_file'] = cert.name
                result_part = path.with_suffix('.json.part')
                result_part.write_text(json.dumps(result, indent=2)+'\n')
                result_part.replace(path)
            print(json.dumps({k:v for k,v in result.items()
                              if k not in ('lattices_detail', 'min_hcr_witness', 'hcr_failures')}), flush=True)
            for failure in result['hcr_failures']:
                print('HCR-FAIL '+json.dumps(failure), flush=True)
    except BudgetExpired:
        print(json.dumps(dict(incomplete_m=active, budget_seconds=args.seconds,
                              status='no aggregate claim for incomplete m')), flush=True)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
