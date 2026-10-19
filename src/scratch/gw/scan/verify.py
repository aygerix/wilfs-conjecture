"""Run on fejer only. Independent tuple/set and pointwise-floor validation."""
import argparse
import csv
from fractions import Fraction
import heapq
import itertools as it
import json
from pathlib import Path
import subprocess
import time


def canonical(r):
    order = sorted(range(r['d']), key=lambda a: r['n'][a])
    n = tuple(r['n'][a] for a in order)
    D = tuple(sorted(tuple(x[a] for a in order) for x in r['D']))
    return r['m'], n, D


def check(r, checker):
    d, m, n = r['d'], r['m'], r['n']
    D = set(map(tuple, r['D']))
    assert len(D) == len(r['D']) == m
    assert len(n) == d and all(a > 0 for a in n)
    assert all(len(x) == d and min(x) >= 0 for x in D)
    for x in D:
        assert all(y in D for y in it.product(*(range(a+1) for a in x)))
    assert all(tuple(int(a == b) for a in range(d)) in D for b in range(d))
    values = [sum(a*b for a, b in zip(x, n)) for x in r['D']]
    assert sorted(v % m for v in values) == list(range(m))
    kappa = [v // m for v in values]
    g, M = sum(kappa), max(values)
    c = M-m+1
    E = (d+1)*(c-g)-c
    corners = sum(not any(all(a <= b for a, b in zip(x, y)) and x != y
                          for y in D) for x in D)
    assert E*m == d*m*M-(d+1)*sum(values)-(d-1)*m*(m-1)//2
    dist = [10**30]*m
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        v, residue = heapq.heappop(heap)
        if v != dist[residue]:
            continue
        for w in n:
            z, new = (residue+w) % m, v+w
            if new < dist[z]:
                dist[z] = new
                heapq.heappush(heap, (new, z))
    minimal = all(dist[v % m] == v for v in values)
    for key, value in dict(E=E, c=c, g=g, M=M, corners=corners, minimal=minimal).items():
        assert r[key] == value, (key, r[key], value)
    plain = f'{d} {m}\n' + ' '.join(map(str, n)) + '\n'
    plain += '\n'.join(' '.join(map(str, x)) for x in r['D']) + '\n'
    other = subprocess.check_output([str(checker.resolve())], input=plain, text=True)
    assert list(map(int, other.split())) == [E, c, g, M, corners]
    return dict(r, values=values, kappa=kappa, ratio=str(Fraction(E, c)))


def ideals(d, end):
    zero = (0,)*d
    units = [tuple(int(a == b) for a in range(d)) for b in range(d)]
    layer = {frozenset([zero, *units])}
    for size in range(d+1, end+1):
        yield size, layer
        if size == end:
            break
        next_layer = set()
        for D in layer:
            for x in D:
                for a in range(d):
                    z = tuple(x[b]+int(a == b) for b in range(d))
                    if z in D:
                        continue
                    if all(tuple(z[b]-int(a == b) for b in range(d)) in D
                           for a in range(d) if z[a]):
                        next_layer.add(D | {z})
        layer = next_layer


def small_exhaustive(Ds, d, m):
    pairs = instances = hard = 0
    minE, minHard = None, None
    for D in Ds:
        t = sum(not any(all(a <= b for a, b in zip(x, y)) and x != y
                        for y in D) for x in D)
        for s in it.product(range(1, m), repeat=d):
            vs = [sum(a*b for a, b in zip(x, s)) for x in D]
            if len({v % m for v in vs}) != m:
                continue
            pairs += 1
            for k in it.product(range(3), repeat=d):
                n = [s[a]+m*k[a] for a in range(d)]
                v = [sum(a*b for a, b in zip(x, n)) for x in D]
                c, g = max(v)-m+1, sum(a//m for a in v)
                E = (d+1)*(c-g)-c
                assert E >= 0
                instances += 1
                minE = E if minE is None else min(minE, E)
                if t > d:
                    hard += 1
                    minHard = E if minHard is None else min(minHard, E)
    return pairs, instances, hard, minE, minHard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records', nargs='+', required=True)
    ap.add_argument('--csv', nargs='+', required=True)
    ap.add_argument('--checker', default='./gw_verify')
    ap.add_argument('--out', default='verified')
    args = ap.parse_args()
    wall, cpu = time.monotonic(), time.process_time()
    rows = {}
    for name in args.csv:
        for row in csv.DictReader(Path(name).open()):
            rows[int(row['d']), int(row['m'])] = row
    for d, end in [(3, 11), (4, 10), (5, 11)]:
        for m, Ds in ideals(d, end):
            row = rows[d, m]
            assert len(Ds) == int(row['labeled_downsets'])
            if m == 7:
                p, count, hard, lo, hi = small_exhaustive(Ds, d, m)
                assert p == int(row['residue_pairs'])
                assert count == int(row['instances'])
                assert hard == int(row['hard_instances'])
                assert lo == int(row['min_E'])
                assert hi == (None if row['min_E_more_than_d_corners'] == 'NA' else int(row['min_E_more_than_d_corners']))
                print(f'independent full check d={d} m={m}: {p=} {count=} {hard=} {lo=} {hi=}')
        print(f'independent set-union downset count d={d} through m={end}: PASS')
    records = []
    for name in args.records:
        for line in Path(name).read_text().splitlines():
            records.append(check(json.loads(line), Path(args.checker)))
    unique = {}
    for r in records:
        assert r['c'] >= r['m'] and r['corners'] > r['d']
        unique[canonical(r)] = r
    records = sorted(unique.values(), key=lambda r: Fraction(r['E'], r['c']))
    out = Path(args.out)
    out.mkdir(exist_ok=True)
    for name, group in [('top10', records[:10]), ('top10_nonminimal', [r for r in records if not r['minimal']][:10])]:
        (out/(name+'.jsonl')).write_text(''.join(json.dumps(r, separators=(',', ':'))+'\n' for r in group))
        print(name, [(r['m'], r['n'], r['ratio']) for r in group])
    print(f'checked_records={len(records)} wall={time.monotonic()-wall:.6f} cpu={time.process_time()-cpu:.6f}')


if __name__ == '__main__':
    main()
