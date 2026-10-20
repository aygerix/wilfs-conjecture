"""Degree-form split of E (PROOFS 'Exact reformulations of CORE1'):
  E = rho + PU + PW,  PU = sum_{x unwrapped} (q - t_x) u(x) >= 0,  PW = sum_{x wrapped} [(q - t_x) u(x) - (K+1) j_x].
Question WR0: PW >= 0?   WR1: PW + rho + r >= 0?   (WR1 => CORE1, WR0 => CORE1 with room rho + r)
Also split PW into top-level (self-financing) part and lower part, and report the resource mix in tight cases.
Usage: python wrself.py ex QMIN QMAX MMAX KMAX [strip] | rnd NR SEED"""
import sys, random, itertools
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
from collections import Counter
def split(m, rho, B, q):
    K = len(B); best = canon(m, rho, B, q, q + 3)
    lamlast = best[m - 1][0] if (m - 1) in best else 99
    if lamlast < q: return None
    reach = {x: v for x, v in best.items() if v[0] <= q}
    d = len(reach); r = m - d
    ell = sum(q - v[0] for v in reach.values()); E = (K + 1) * ell - q * d + rho
    PU = 0; PWtop = 0; PWlow = 0; Jlow = 0; JC = 0; PWq1 = 0; Pq1 = 0; PWid = 0
    for x, (lx, tx, cx, ax) in reach.items():
        jx = lx - tx; u = 0
        JC += jx - sum(ax[i] for i, b in enumerate(B) if ax[i] > 0 and b > x)
        for i, b in enumerate(B):
            y = (x + b) % m; ay = tuple(ax[k] + (k == i) for k in range(K))
            if not (y in reach and reach[y][3] == ay): u += ax[i] + 1
        if lx == q - 1:
            Pq1 += u
            if jx > 0: PWq1 += u
        if jx > 0: PWid += (q - lx) * u
        if jx == 0: PU += (q - tx) * u
        elif lx == q: PWtop += (q - tx) * u - (K + 1) * jx
        else: PWlow += (q - tx) * u - (K + 1) * jx; Jlow += jx
    assert E == rho + PU + PWtop + PWlow, (m, rho, B, q)
    assert PWtop + PWlow == JC * 0 + PWid - JC, (m, rho, B, q)
    return dict(E=E, r=r, rho=rho, PU=PU, PWt=PWtop, PWl=PWlow, PW=PWtop + PWlow, Jl=Jlow, JC=JC, PWq1=PWq1, Pq1=Pq1, PWid=PWid)
mode = sys.argv[1]; stat = Counter(); mins = {}
def feed(m, rho, B, q):
    s = split(m, rho, B, q)
    if s is None: return
    stat['n'] += 1
    if s['JC'] == 0 and s['PW'] == 0: stat['nowrapdef'] += 1
    for key, val in (('WR0', s['PW']), ('WR1', s['PW'] + s['rho'] + s['r']), ('CORE1', s['E'] + s['r']),
                     ('WRlow', s['PWl']), ('T1', s['rho'] + s['r'] - s['JC']),
                     ('T2', s['rho'] + s['r'] + s['PWq1'] - s['JC']), ('ANCHOR', s['rho'] + s['r'] + s['Pq1'] - s['JC']),
                     ('WR1wr', (s['PW'] + s['rho'] + s['r']) if s['JC'] > 0 else 10**9)):
        if val < 0: stat[key + '_neg'] += 1
        if key not in mins or val < mins[key][0]: mins[key] = (val, m, rho, tuple(B), q, s)
if mode == 'ex':
    QMIN, QMAX, MMAX, KMAX = map(int, sys.argv[2:6]); strip = len(sys.argv) > 6
    for q in range(QMIN, QMAX + 1):
        for m in range(6, MMAX + 1):
            for rho in range(0, m - 1):
                hi = m if strip else m - rho
                for K in range(2, KMAX + 1):
                    for B in itertools.combinations(range(1, hi), K): feed(m, rho, list(B), q)
else:
    NR, SEED = int(sys.argv[2]), int(sys.argv[3]); rnd = random.Random(SEED)
    for it in range(NR):
        q = rnd.randint(5, 8); m = rnd.randint(20, 110); rho = rnd.randint(0, m - 2)
        hi = m if rnd.random() < 0.3 else m - rho
        if hi < 6: continue
        K = rnd.randint(2, min(12, hi - 2)); lo = rnd.randint(1, hi - 1); top = rnd.randint(lo, hi - 1)
        if top - lo + 1 < K: continue
        feed(m, rho, sorted(rnd.sample(range(lo, top + 1), K)), q)
print(dict(stat))
for k in sorted(mins): print(k, mins[k])
