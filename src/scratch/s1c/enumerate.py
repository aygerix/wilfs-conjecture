#!/usr/bin/python3
"""Exact class-C enumeration, independent cell checks, and complete extrema.

Usage: /usr/bin/python3 src/scratch/s1c/enumerate.py FIRST LAST [SECONDS]
The entire invocation is bounded (default 270 seconds).
Only completed volumes are advertised as exhaustive. All outputs stay here.
Axis lengths are sorted L1 <= L2 <= L3. This loses no S3-orbit.
The corpus retains every such oriented triple; extrema are S3 representatives.
"""
import gzip
import itertools
import json
import pathlib
import signal
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
PERMS = tuple(itertools.permutations(range(3)))


def cells(h, f, g):
    return {(i, j, k) for i, hi in enumerate(h) for j in range(hi)
            for k in range(min(f[i], g[j]))}


def direct_s1(d):
    """Definition only: check the three successors of every cell."""
    a = [(i, j, k) for i, j, k in d
         if (i + 1, j, k) not in d and (i, j + 1, k) not in d
         and (i, j, k + 1) not in d]
    return sum(3 + i + j + k for i, j, k in a), tuple(sorted(a))


def corner_s1(h, f, g):
    ans = 0
    for i, hi in enumerate(h):
        for j in range(hi):
            z = min(f[i], g[j])
            if i + 1 < len(h) and j < h[i + 1] and min(f[i + 1], g[j]) >= z:
                continue
            if j + 1 < hi and min(f[i], g[j + 1]) >= z:
                continue
            ans += i + j + z + 2
    return ans


def face_parameters(d):
    l1 = max(x[0] for x in d) + 1
    l2 = max(x[1] for x in d) + 1
    h = tuple(sum((i, j, 0) in d for j in range(l2)) for i in range(l1))
    f = tuple(1 + max(k for x, j, k in d if x == i and j == 0) for i in range(l1))
    g = tuple(1 + max(k for i, y, k in d if i == 0 and y == j) for j in range(l2))
    return h, f, g


def canonical(d):
    return min(face_parameters({tuple(x[a] for a in p) for x in d}) for p in PERMS)


def g_partitions(length, top, budget):
    """G[0]=top, G[1]>=2, positive decreasing, sum(G)<=budget."""
    def rec(prefix, rem):
        left = length - len(prefix)
        if left == 0:
            yield tuple(prefix)
            return
        lo = 2 if len(prefix) == 1 else 1
        hi = min(prefix[-1], rem - (left - 1))
        for v in range(lo, hi + 1):
            yield from rec(prefix + [v], rem - v)
    yield from rec([top], budget - top)


def triples(m):
    """All face triples of volume m having sorted axis lengths."""
    # min m = L1+L2+L3+2, since the 2-cube and remaining axis cells are disjoint.
    for l2 in range(2, (m - 4) // 2 + 1):
        for l3 in range(l2, m - l2 - 3):
            for g in g_partitions(l2, l3, m - 4):
                rem = m - sum(g)
                # Precompute row volumes for this G.
                area = [[0] * (l3 + 1) for _ in range(l2 + 1)]
                for hi in range(1, l2 + 1):
                    for fi in range(1, l3 + 1):
                        area[hi][fi] = area[hi - 1][fi] + min(fi, g[hi - 1])

                def rows(h, f, budget):
                    if budget == 0:
                        yield tuple(h), tuple(f), g
                        return
                    if len(h) == l2:
                        return
                    lo = 2 if len(h) == 1 else 1
                    for hi in range(lo, min(h[-1], budget) + 1):
                        for fi in range(lo, min(f[-1], budget) + 1):
                            cost = area[hi][fi]
                            if cost > budget:
                                break
                            rest = budget - cost
                            slots = l2 - len(h) - 1
                            if rest > slots * cost:
                                continue
                            yield from rows(h + [hi], f + [fi], rest)

                yield from rows([l2], [l3], rem)


class BudgetExpired(Exception):
    pass


def alarm_handler(signum, frame):
    raise BudgetExpired()


def run(m, seconds):
    start = time.monotonic()
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    count = labelled = 0
    maximum = -10**9
    winners = set()
    path = HERE / ('corpus_%02d.jsonl.gz' % m)
    complete = False
    try:
        with gzip.open(path, 'wt', compresslevel=1) as out:
            for h, f, g in triples(m):
                d = cells(h, f, g)
                assert len(d) == m
                assert (1, 1, 0) in d and (1, 0, 1) in d and (0, 1, 1) in d
                assert (1, 1, 1) in d
                s, maxima = direct_s1(d)
                assert s == corner_s1(h, f, g), (h, f, g, s)
                count += 1
                dims = (len(h), len(g), f[0])
                assert dims[0] <= dims[1] <= dims[2]
                labelled += len(set(itertools.permutations(dims)))
                excess = s - 2 * m
                if excess >= maximum:
                    c = canonical(d)
                    if excess > maximum:
                        maximum = excess
                        winners.clear()
                    winners.add(c)
                out.write(json.dumps([h, f, g, s], separators=(',', ':')) + '\n')
        complete = True
    except BudgetExpired:
        pass
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    result = dict(m=m, complete=complete, sorted_axis_count=count,
                  labelled_count=labelled, max_excess=maximum if count else None,
                  extrema=sorted(winners), seconds=round(time.monotonic() - start, 3),
                  python=sys.version.split()[0])
    (HERE / ('result_%02d.json' % m)).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)
    return complete


if __name__ == '__main__':
    first, last = map(int, sys.argv[1:3])
    seconds = min(float(sys.argv[3]) if len(sys.argv) > 3 else 270.0, 285.0)
    deadline = time.monotonic() + seconds
    for m in range(first, last + 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not run(m, remaining):
            break
