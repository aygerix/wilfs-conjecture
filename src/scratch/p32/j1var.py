"""Strip-free P18 models at q = 5 (only j <= 1): which weakenings of ANCHOR's j<=1 form
   N - |U| <= 2p + U_top + C   (N = m - rho, U = unwrapped canonical reached positions, C = used crossing weight)
survive?  Variants:
  V2: N - |U| <= p + U_top + C      V3: N - |U| <= C + p      V4: N - |U| <= C
  V5: #deficit positions <= #wrapped-minimal excess (sum over wrapped y of (c_y - 1)_+) + p + U_top
  V6 (window-only): #{wrapped or hole in [rho,m)} <= sum_{wrapped y in [rho,m)} c_y + p + U_top
Exhaustive over small m or random. Usage: python j1var.py MODE ...  MODE=ex MMAX KMAX | rnd NR SEED"""
import sys, random, itertools
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
from collections import Counter
def stats(m, rho, B, q):
    K = len(B); best = canon(m, rho, B, q, q + 3)
    reach = {x: v for x, v in best.items() if v[0] <= q}
    if not (m - 1 + 0) in best or best.get((m - 1), (99,))[0] < q:  # true depth: position m-1 at level >= q
        pass
    lam_last = best[(m - 1)][0] if (m - 1) in best else 99
    if lam_last < q: return None
    d = len(reach); p = m - d; N = m - rho
    U = [x for x, v in reach.items() if v[0] == v[1]]
    C = 0; Utop = 0; exc_min = 0; ndef = 0; wr_win = 0; Cwin = 0; jmax = 0
    for x, (lx, tx, cx, ax) in reach.items():
        jx = lx - tx; jmax = max(jmax, jx)
        cy = sum(ax[i] for i, b in enumerate(B) if ax[i] > 0 and b > x)
        C += cy
        if jx > 0:
            if cy < jx: ndef += jx - cy
            else: exc_min += cy - jx
            if x >= rho: wr_win += 1; Cwin += cy
        if lx == q - 1:
            for i, b in enumerate(B):
                w = ax[i] + 1; y = (x + b) % m
                used = y in reach and reach[y][3] == tuple(ax[k] + (k == i) for k in range(K))
                if not used: Utop += w
    lhs = N - len(U)
    holes_win = sum(1 for x in range(rho, m) if x not in reach)
    return dict(lhs=lhs, p=p, Utop=Utop, C=C, ndef=ndef, exc=exc_min, jmax=jmax, rho=rho,
                V1=2*p + Utop + C - lhs, V2=p + Utop + C - lhs, V3=C + p - lhs, V4=C - lhs,
                V5=exc_min + p + Utop - ndef, V6=Cwin + p + Utop - (wr_win + holes_win))
mode = sys.argv[1]; q = 5
mins = {}; arg = {}; cnt = Counter(); n = 0
def feed(m, rho, B):
    global n
    s = stats(m, rho, B, q)
    if s is None: return
    n += 1
    if s['jmax'] > 1: cnt['j>1'] += 1
    for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6'):
        if s[k] < 0: cnt[k] += 1
        if k not in mins or s[k] < mins[k]: mins[k] = s[k]; arg[k] = (m, rho, B, s['lhs'], s['p'], s['Utop'], s['C'])
if mode == 'ex':
    MMAX, KMAX = int(sys.argv[2]), int(sys.argv[3])
    for m in range(6, MMAX + 1):
        for rho in range(0, m - 1):
            N = m - rho
            for K in range(2, KMAX + 1):
                for B in itertools.combinations(range(1, N), K): feed(m, rho, list(B))
else:
    NR, SEED = int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(SEED)
    for it in range(NR):
        m = rnd.randint(20, 120); rho = rnd.randint(0, m // 2); N = m - rho
        K = rnd.randint(2, min(12, N - 1)); lo = rnd.randint(1, N - 1); hi = rnd.randint(lo, N - 1)
        if hi - lo + 1 < K: continue
        feed(m, rho, sorted(rnd.sample(range(lo, hi + 1), K)))
print("models", n, "failures", dict(cnt))
for k in sorted(mins): print(k, "min slack", mins[k], "at", arg[k])
