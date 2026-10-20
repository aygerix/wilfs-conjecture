r"""Core regime of P18 depth four (lead, 2026-10-20): all b in [ceil(h/2), h).
Exact identity  W = e^2 + E1 + E3f - e*delta + 3*tau + 3*kappa - h, where
  E3f = (e-1)|2A| - 3|3A \ 2A| (untruncated Macaulay slack), tau = |3B n [m+h, oo)|, kappa = |(A+m) n (2B u 3B)|.
Chain: window [h, 3h') c 2B u (A+m) gives h <= e^2 - e - E1 - 2 rho2 + 2e' - 2 delta1 - 3[h odd];
tau >= |B' + B| >= k(2e-k-1)/2 - E1/2 (B' = {s - m : s in 2B, s - m in B}, k = |B'|); kappa >= delta, kappa = e if m in 2B.
Final bound: W >= e - 2e' + 3[h odd] >= e - 2. Checks each step.  usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
from math import gcd
sys.path.insert(0, '.')
from p18free import run
def c2(h): return (h + 1) // 2
stats = dict(core=0, idfail=0, winfail=0, taufail=0, kapfail=0, boundfail=0, negW=0)
worst = None
def handle(m, B):
    global worst
    r = run(m, B)
    if not r: return
    h, e, W = r["h"], r["e"], r["W"]
    if min(B) < c2(h) or max(B) >= h: return
    stats["core"] += 1
    A = [0] + list(B); Bs = set(B)
    twoB = set(x + y for x in B for y in B); threeB = set(s + z for s in twoB for z in B)
    twoA = set(A) | twoB; threeA = twoA | threeB
    E1 = e * (e + 1) - 2 * len(twoA); E3f = (e - 1) * len(twoA) - 3 * len(threeA - twoA)
    Am = set(a + m for a in A)
    delta = len(twoB & Am); kappa = len(Am & (twoB | threeB)); tau = sum(1 for s in threeB if s >= m + h)
    if W != e * e + E1 + E3f - e * delta + 3 * tau + 3 * kappa - h: stats["idfail"] += 1
    W1 = set(range(h, 3 * c2(h))); ep = len(Am & W1); rho2 = len(twoB - W1); d1 = len(twoB & Am & W1)
    if h > e * e - e - E1 - 2 * rho2 + 2 * ep - 2 * d1 - 3 * (h % 2): stats["winfail"] += 1
    Bp = [s - m for s in twoB if (s - m) in Bs]; k = len(Bp)
    if k and tau < k * (2 * e - k - 1) // 2 - E1 / 2: stats["taufail"] += 1
    if kappa < delta or (m in twoB and kappa != e): stats["kapfail"] += 1
    bound = e - 2 * ep + 3 * (h % 2)
    if W < bound: stats["boundfail"] += 1
    if W < 0: stats["negW"] += 1
    if worst is None or W - (e - 2) < worst[0]: worst = (W - (e - 2), m, B, h, e, W, delta, k)
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
print(sys.argv[1:], stats, "min W-(e-2):", worst)
