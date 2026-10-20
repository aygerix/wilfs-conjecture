"""Gate test for ANCHOR-q (lead, 2026-10-20). In ID-q terms (idq.py):
  W0 = rho + POOL + EXC - DEF, POOL = sum_x (q - lam_x) u(x), EXC = sum max(0, c_y - j_y), DEF = sum max(0, j_y - c_y).
ANCHOR-q:  DEF <= rho + EXC + U_top + p,   U_top = sum_{lam_x = q-1} u(x)   (pool part of weight 1), p = #{lam > q}.
At q = 4 this follows from the kernel-checked anchor theorem when d4 >= h4. Reports failures, min slack, and for
failures how much of the lower pool (weights >= 2) is needed. Also reports the plain CORE1 slack W0 + p.
Usage: python anchq.py NRAND SEED QMIN QMAX [strip]"""
import random, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon

def parts(m, rho, B, q):
    K = len(B); BASE = q + 3
    best = canon(m, rho, B, q, BASE)
    POOL = 0; Utop = 0; EXC = 0; DEF = 0
    for x, (lx, tx, cx, ax) in best.items():
        if lx > q: continue
        jx = lx - tx
        for i, b in enumerate(B):
            w = ax[i] + 1
            y = (x + b) % m
            used = False
            if y in best and best[y][0] <= q:
                ay = list(ax); ay[i] += 1
                if tuple(ay) == best[y][3] and best[y][0] == lx + 1 + (1 if x + b >= m else 0):
                    used = True
            if not used:
                POOL += (q - lx) * w
                if lx == q - 1: Utop += w
        cy = sum(ax[i] for i, b in enumerate(B) if ax[i] > 0 and b > x)
        if cy > jx: EXC += cy - jx
        else: DEF += jx - cy
    d = sum(1 for v in best.values() if v[0] <= q)
    p = m - d
    lam_top = best[m - 1][0] if (m - 1) in best else 10**9
    W0 = rho + POOL + EXC - DEF
    return dict(W0=W0, POOL=POOL, Utop=Utop, EXC=EXC, DEF=DEF, p=p, slack=rho + EXC + Utop + p - DEF,
                true_depth=lam_top >= q)

if __name__ == "__main__":
    NR, SEED, QMIN, QMAX = map(int, sys.argv[1:5]); strip = len(sys.argv) > 5
    rnd = random.Random(SEED)
    stats = {}
    for it in range(NR):
        q = rnd.randint(QMIN, QMAX)
        m = rnd.randint(10, 70)
        rho = rnd.randint(0, m - 2)
        hi = m if strip else m - rho
        if hi - 1 < 2: continue
        K = rnd.randint(2, min(10, hi - 1))
        # bias towards high offsets (the deficit needs them)
        lo = rnd.choice([1, hi // 3, hi // 2])
        pool = list(range(max(1, lo), hi))
        if len(pool) < K: continue
        B = sorted(rnd.sample(pool, K))
        r = parts(m, rho, B, q)
        s = stats.setdefault(q, dict(n=0, fail=0, minslack=None, ex=None, core1min=None, defpos=0))
        s['n'] += 1
        if r['DEF'] > 0: s['defpos'] += 1
        c1 = r['W0'] + r['p']
        if s['core1min'] is None or c1 < s['core1min']: s['core1min'] = c1
        if s['minslack'] is None or r['slack'] < s['minslack']:
            s['minslack'] = r['slack']; s['ex'] = (m, rho, B, r)
        if r['slack'] < 0:
            s['fail'] += 1
            if s['fail'] <= 3: print("FAIL q=%d" % q, m, rho, B, r, flush=True)
    for q in sorted(stats): print(q, stats[q])
