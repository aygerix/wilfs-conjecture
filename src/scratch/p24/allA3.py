r"""All-A P18 depth four (B c [1,h)), lead 2026-10-20. Exact identity (checked):
  W = E1 + E3f + e*y0 - e*delta + 3*tau + 3*omega - 3*N4 - h,
  tau = |3A n [m+h, oo)|, omega = |4A_{<h} n (3A_{[m,m+h)} - m)|.
Window part: W1 = [h, 3h'), h' = ceil(h/2).  Z = e(y0-e) + 2(|2A_<h| - e) + e - 2|(3A\2A) n W1| - 3N4 - 2e'' + 3[h odd],
e'' = |W1 n (m + 4A_<h) \ 3A|; then W >= 2E1 + E3f + 2 rho + Z + (3 tau + 3 omega - e delta), rho = |2A n [3h', oo)|.
Reports min Z, min (Z + 2E1 + E3f), and min (3tau + 3omega - e delta) over non-core all-A S (some b < h').
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
from math import gcd
sys.path.insert(0, '.')
from p18free import run
def c2(h): return (h + 1) // 2
st = dict(allA=0, noncore=0, idfail=0, boundfail=0)
mins = {}
def upd(key, val, info):
    if key not in mins or val < mins[key][0]: mins[key] = (val, info)
def handle(m, B):
    r = run(m, B)
    if not r: return
    h, e, W = r["h"], r["e"], r["W"]
    if max(B) >= h: return
    st["allA"] += 1
    A = [0] + list(B)
    X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    E1 = e * (e + 1) - 2 * len(X2); E3f = (e + 2) * len(X2) - 3 * len(X3)
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    delta = sum(1 for s in X2 if m <= s < m + h and (s - m) in X3)
    tau = sum(1 for s in X3 if s >= m + h)
    A4h = set(s for s in X4 if s < h); omega = sum(1 for s in X3 if m <= s < m + h and (s - m) in A4h)
    if W != E1 + E3f + e * y0 - e * delta + 3 * tau + 3 * omega - 3 * N4 - h: st["idfail"] += 1
    if min(B) >= c2(h): return
    st["noncore"] += 1
    W1 = set(range(h, 3 * c2(h)))
    x2h = sum(1 for s in X2 if s < h)
    t3w = len((X3 - X2) & W1)
    epp = len(set(m + s for s in A4h) & W1 - X3)
    rho = sum(1 for s in X2 if s >= 3 * c2(h))
    Z = e * (y0 - e) + 2 * (x2h - e) + e - 2 * t3w - 3 * N4 - 2 * epp + 3 * (h % 2)
    D = 3 * tau + 3 * omega - e * delta
    if W < 2 * E1 + E3f + 2 * rho + Z + D: st["boundfail"] += 1
    info = dict(m=m, B=B, h=h, e=e, W=W, y0=y0, N4=N4, t3w=t3w, x2h=x2h, E1=E1, E3f=E3f, delta=delta, tau=tau, omega=omega)
    upd("Z", Z, info); upd("Z+2E1+E3f", Z + 2 * E1 + E3f, info); upd("D", D, info); upd("W-(e-2)", W - (e - 2), info)
    upd("Z+2E1+E3f+2rho+D", Z + 2 * E1 + E3f + 2 * rho + D, info)
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
        if h0 - 1 < k: continue
        B = tuple(sorted(random.sample(range(1, h0), k)))
        if gcd(m, *B) == 1: handle(m, B)
print(sys.argv[1:], st)
for kk, (v, info) in mins.items(): print("  min", kk, v, info)
