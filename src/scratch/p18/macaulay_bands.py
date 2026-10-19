"""Test Macaulay-type ratio monotonicity of band counts for S = <m, m+B*> (all generators < 2m).
 (Z) zero-aligned bands  u_H = |S cap [Hm,(H+1)m)|,          H = 0..D
 (C) conductor-aligned   v_j = |S cap [c-(D-j)m, c-(D-j-1)m)|, j = 0..D   (v_D = m, sum_{j<D} v_j = ell)
 claim X: x_j / C(j+k,k) non-increasing in j (as exact rationals).  (C) => (k+1) ell >= mD >= c.
usage: python macaulay_bands.py seed trials mmin mmax kmin kmax"""
import sys, random
from math import comb, gcd
def bands(m, Bs):
    gens = [m] + [m + b for b in Bs]
    N = 4 * m
    while True:
        mem = bytearray(N); mem[0] = 1
        for n in range(1, N):
            for g in gens:
                if g <= n and mem[n - g]: mem[n] = 1; break
        run = 0; c = None
        for n in range(N):
            run = run + 1 if mem[n] else 0
            if run == m: c = n - m + 1; break
        if c is not None: return mem, c
        N *= 2
def check(m, Bs):
    k = len(Bs); mem, c = bands(m, Bs); D = -(-c // m)
    u = [sum(mem[H * m:(H + 1) * m]) for H in range(D + 1)]
    v = []
    for j in range(D + 1):
        lo = c - (D - j) * m; hi = lo + m
        v.append(sum(mem[max(0, lo):hi]))
    def mono(x):
        for j in range(len(x) - 1):
            if x[j + 1] * comb(j + k, k) > x[j] * comb(j + 1 + k, k): return j
        return None
    ell = sum(mem[:c])
    return D, c, ell, u, v, mono(u), mono(v)
seed, T, mmin, mmax, kmin, kmax = map(int, sys.argv[1:7]); rng = random.Random(seed)
stats = {'Z': 0, 'C': 0, 'n': 0}; ex = {}
for t in range(T):
    m = rng.randint(mmin, mmax); k = rng.randint(kmin, min(kmax, m - 2))
    mode = rng.random()
    if mode < 0.4: Bs = sorted(rng.sample(range(1, m), k))
    elif mode < 0.7:
        span = rng.randint(k, max(k, m // rng.randint(1, 6))); Bs = sorted(rng.sample(range(1, span + 1), k))
    else:
        a = rng.randint(1, m - 1); b = rng.randint(1, m - 1)
        cand = sorted(set((i * a + j * b) % m for i in range(4) for j in range(4)) - {0})
        if len(cand) < k: continue
        Bs = sorted(rng.sample(cand, k))
    if gcd(m, *Bs) != 1: continue
    D, c, ell, u, v, fz, fc = check(m, Bs)
    if D < 3: continue
    stats['n'] += 1
    if fz is not None:
        stats['Z'] += 1; ex.setdefault('Z', (m, Bs, D, fz, u))
    if fc is not None:
        stats['C'] += 1; ex.setdefault('C', (m, Bs, D, fc, v))
print(stats)
for key in ex: print(key, ex[key])
