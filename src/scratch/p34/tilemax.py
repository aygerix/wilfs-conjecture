"""Variants of TOP0' on leaves (lead, 2026-10-21). eps = phi mod m (bijection M -> Z/m), threshold qm.
  TOP0'   : sum_{y in M, phi(y) >= qm} (|y|-1) eps(y) <= (n+1) sum_{rest} eps
  TILEMAX : the same with ALL componentwise-maximal elements of M on the left (gamma-free, stronger)
  TOP0    : threshold c (census-verified)
Usage: python tilemax.py NS SEED MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
def variants(m, G):
    R = build(m, G)
    if R is None: return None
    c, gens, M = R; n = len(gens)
    if n < 2 or any(g >= c for g in gens): return None
    q = -(-c // m); T = q * m
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(n))
    eps = {a: x % m for a, x in M.items()}
    top = [a for a, x in M.items() if x >= T]
    mx = [a for a in M if all(up(a, i) not in M for i in range(n))]
    def sl(Z):
        Zs = set(Z)
        return (n + 1) * sum(eps[a] for a in M if a not in Zs) - sum((sum(a) - 1) * eps[a] for a in Z)
    return sl(top), sl(mx), len(mx), len(top), c, gens
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED)
cnt = f1 = f2 = 0; w2 = None
for _ in range(NS):
    m = rnd.randint(4, MMAX); G = [rnd.randint(m + 1, rnd.choice([2, 3, 4]) * m) for _ in range(rnd.randint(2, 6))]
    v = variants(m, G)
    if v is None: continue
    cnt += 1
    if v[0] < 0: f1 += 1; print("TOP0' FAIL", m, v)
    if v[1] < 0:
        f2 += 1
        if f2 <= 5: print("TILEMAX FAIL m=%d slack=%d #max=%d #top=%d c=%d gens=%s" % (m, v[1], v[2], v[3], v[4], v[5]), flush=True)
print("leaves", cnt, "TOP0' fails", f1, "TILEMAX fails", f2)
