r"""Check the inversion identity V(sigma) = N(sigma) - kappa0 against depcarry.carry (V = rho + sum kappa) at every
phase, on random S tiles and on all small tiles; also report TRIV (kappa0 <= Dep).  Usage: python invcheck.py NS SEED"""
import sys, random, itertools
sys.path.insert(0, '.')
from tile import build
from depcarry import carry
from subadd_lp import downsets
def inv(m, D, delta):
    N = len(delta); Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    K = {}
    for a in range(N):
        for x in D:
            k = 0; y = x
            while up(y, a) in Ds: y = up(y, a); k += 1
            K[(x, a)] = k
    Mp = m * (m - 1) // 2
    tot = sum((K[(x, a)] * delta[a]) % m for x in D for a in range(N))
    return K, (tot - Mp) // m, (tot - Mp) % m
NS, SEED = map(int, sys.argv[1:3]); rnd = random.Random(SEED); cnt = bad = 0
while cnt < NS:
    m = rnd.randint(5, 40); c0 = rnd.randint(m + 1, 9 * m)
    G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(8, c0 - 2))))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens)
    if N < 2: continue
    cnt += 1; D = list(M); delta = [g % m for g in gens]
    K, k0, rem = inv(m, D, delta); assert rem == 0
    for s in range(m):
        kap, tops, dep, mx, lnm = carry(m, D, delta, s)
        V = s + kap
        Nn = sum(1 for x in D for a in range(N) if K[(x, a)] and (s + sum(p * q for p, q in zip(x, delta))) % m >= m - (K[(x, a)] * delta[a]) % m)
        if V != Nn - k0: bad += 1
print("random S tiles %d, phase mismatches %d" % (cnt, bad))
tri = tt = 0
for N, MM in ((2, 14), (3, 10)):
    for m in range(3, MM + 1):
        for D in downsets(N, m):
            for b in itertools.product(range(1, m), repeat=N):
                if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) != m: continue
                tt += 1
                K, k0, rem = inv(m, D, list(b)); assert rem == 0
                kap, tops, dep, mx, lnm = carry(m, D, list(b), 0)
                if k0 > dep: tri += 1
print("small tiles %d: TRIV failures %d" % (tt, tri))
