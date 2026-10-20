"""Threshold shift test (lead, 2026-10-21). Full lex tile M^ (N = e-1). With threshold T = qm (c = qm - rho):
W = W' - N rho, W' = (N+1)(m-1)/2 + P' - sum_{phi(y) >= qm} (|y|+N)(phi(y)-qm)/m,
P' = (1/m) sum_{z: phi(z) < qm} sum_{i: z+e_i not in M^} (z_i+1)(qm - phi(z)).
Tests PSHIFT: P' >= N rho, and also checks the identity. Usage: python pshift.py NS SEED MMAX"""
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from tile import build
NS, SEED, MMAX = map(int, sys.argv[1:4]); rnd = random.Random(SEED); tot = f = bad = 0; worst = None
for _ in range(NS):
    m = rnd.randint(4, MMAX); G = [rnd.randint(m + 1, rnd.choice([2, 3, 5, 8]) * m) for _ in range(rnd.randint(1, 6))]
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens)
    if N < 2: continue
    q = -(-c // m); rho = q * m - c; T = q * m
    g = sum(x // m for x in M.values()); W = (N + 1) * (c - g) - c
    up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
    P = Fr(0); top = Fr(0)
    for a, x in M.items():
        if x < T:
            for i in range(N):
                if up(a, i) not in M: P += Fr((a[i] + 1) * (T - x), m)
        else: top += Fr((sum(a) + N) * (x - T), m)
    Wp = Fr((N + 1) * (m - 1), 2) + P - top
    if Wp - N * rho != W: bad += 1
    tot += 1; sl = P - N * rho
    if worst is None or sl < worst[0]: worst = (float(sl), m, gens, c, rho, W)
    if sl < 0:
        f += 1
        if f <= 5: print("PSHIFT FAIL m=%d c=%d rho=%d gens=%s P'=%.2f N*rho=%d W=%d" % (m, c, rho, gens, float(P), N * rho, W), flush=True)
print("tested", tot, "identity mismatches", bad, "PSHIFT failures", f, "worst", worst)
