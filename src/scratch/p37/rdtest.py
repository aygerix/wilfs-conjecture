r"""Residue descent test (lead, 2026-10-21).  For S with multiplicity m and other minimal generators g_i, let
T = <m, g_i mod m> (a numerical semigroup of multiplicity min(g_i mod m) < m).  Test RD: W(S) >= W(T) (W(N) := 0).
Families: level-1 (all generators in (m, 2m)), and general random S.  usage: python rdtest.py seed n"""
import sys, random
from math import gcd
from functools import reduce
def data(G):
    G = sorted(set(G)); m = G[0]
    if reduce(gcd, G) != 1: return None
    if m == 1: return dict(m=1, c=0, g=0, e=1, W=0, gens=[1])
    w = [None] * m; w[0] = 0; import heapq; h = [(0, 0)]; done = [False] * m
    while h:
        v, s = heapq.heappop(h)
        if done[s]: continue
        done[s] = True
        for x in G[1:]:
            t = (v + x) % m
            if w[t] is None or v + x < w[t]: w[t] = v + x; heapq.heappush(h, (v + x, t))
    Ap = sorted(w); Aps = set(Ap)
    gens = [m] + [x for x in Ap[1:] if not any((x - y) in Aps for y in Ap[1:] if y < x)]
    c = max(Ap) - m + 1; g = sum(x // m for x in Ap); e = len(gens)
    if c <= 0: c = 0
    return dict(m=m, c=c, g=g, e=e, W=e * (c - g) - c, gens=gens)
random.seed(int(sys.argv[1])); n = int(sys.argv[2])
fails = {}; cnt = {}
for it in range(n):
    fam = random.choice(['lev1', 'lev1', 'gen'])
    m = random.randint(4, 40)
    if fam == 'lev1':
        k = random.randint(1, min(m - 1, 10)); G = [m] + [m + a for a in random.sample(range(1, m), k)]
    else:
        k = random.randint(1, min(m - 1, 8)); G = [m] + [random.randint(m + 1, 6 * m) for _ in range(k)]
    D = data(G)
    if D is None or D['m'] != m: continue
    A = sorted(set(x % m for x in D['gens'][1:]))
    if not A: continue
    T = data([m] + A)
    if T is None: continue
    cnt[fam] = cnt.get(fam, 0) + 1
    if D['W'] < T['W']:
        f = fails.setdefault(fam, [])
        if len(f) < 5: f.append((D['gens'], D['W'], T['gens'], T['W']))
        else: f.append(None)
for fam in cnt:
    F = fails.get(fam, [])
    print(fam, "tested", cnt[fam], "RD failures", len(F))
    for x in [y for y in F if y][:5]: print("   S=%s W=%d  T=%s W(T)=%d" % x)
