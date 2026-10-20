# Core regime, delta >= 2 (lead, 2026-10-20): lower bounds lb = e - 2e' - (e-5)delta + 3Omega and
# lb2 = 2E1 + e - 2e' + 2delta1 + 2rho2 - (e-3)delta + 3Omega (rho2 = |2B \ W1|, delta1 = delta-pairs inside W1). Both <= W - E3.
import sys, itertools, random
from math import gcd
sys.path.insert(0, '.')
from p18free import run
def c2(h): return (h + 1) // 2
res = []
def handle(m, B):
    r = run(m, B)
    if not r: return
    h, e = r["h"], r["e"]
    if min(B) < c2(h) or max(B) >= h: return
    A = [0] + list(B); W1 = set(range(h, 3 * c2(h)))
    ep = sum(1 for a in A if (a + m) in W1)
    twoB = set(x + y for x in B for y in B)
    rho2 = len(twoB - W1)
    d1 = sum(1 for s in twoB if s in W1 and m <= s < m + h and (s - m) in set(A))
    lb = e - 2 * ep - (e - 5) * r["delta"] + 3 * r["Omega"]
    lb2 = 2 * r["E1"] + e - 2 * ep + 2 * d1 + 2 * rho2 - (e - 3) * r["delta"] + 3 * r["Omega"]
    res.append((r, lb, lb2, ep, rho2, d1))
mode = sys.argv[1]
if mode == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k):
            if gcd(m, *B) == 1: handle(m, B)
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); h0 = random.randint(max(4, m // 2), m)
        if h0 - c2(h0) < k: continue
        B = tuple(sorted(random.sample(range(c2(h0), h0), k)))
        if gcd(m, *B) == 1: handle(m, B)
big = [x for x in res if x[0]["delta"] >= 2]
print("core:", len(res), "delta>=2:", len(big))
print("  lb < 0:", sum(1 for x in big if x[1] < 0), " lb2 < 0:", sum(1 for x in big if x[2] < 0))
if big:
    w = min(big, key=lambda x: x[2]); print("  min lb2", w[2], "lb", w[1], {k2: w[0][k2] for k2 in ("m", "B", "h", "e", "W", "E1", "E3", "delta", "Omega")}, "e'", w[3], "rho2", w[4])
    w = min(big, key=lambda x: x[1]); print("  min lb", w[1], {k2: w[0][k2] for k2 in ("m", "B", "h", "e", "W", "E1", "E3", "delta", "Omega")})
