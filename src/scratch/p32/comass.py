"""Check the centre-of-mass identity (lead, 2026-10-20):
  m*(DEF - EXC) = sum_{unused (x,i)} w(x,i)*x - (K+1)*sum_{lam_y <= q} y + rho*d,  and  sum_{unused} w = K*d.
Here w(x,i) = alpha_x(i) + 1, positions are shifted positions in [0, m), and DEF - EXC = sum_y (j_y - c_y).
Works for P18 models (offsets < m). Usage: python comass.py NRAND SEED"""
import random, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
NR, SEED = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(SEED); bad = 0; n = 0
for it in range(NR):
    q = rnd.randint(2, 7); m = rnd.randint(6, 50); rho = rnd.randint(0, m - 2)
    K = rnd.randint(1, min(8, m - 1)); B = sorted(rnd.sample(range(1, m), K))
    best = canon(m, rho, B, q, q + 3)
    reach = [x for x in best if best[x][0] <= q]
    d = len(reach); sy = sum(reach)
    Uw = 0; Uwx = 0; dme = 0
    for x in reach:
        lx, tx, cx, ax = best[x]
        for i, b in enumerate(B):
            w = ax[i] + 1; y = (x + b) % m; used = False
            if y in best and best[y][0] <= q:
                ay = list(ax); ay[i] += 1
                if tuple(ay) == best[y][3] and best[y][0] == lx + 1 + (1 if x + b >= m else 0): used = True
            if not used: Uw += w; Uwx += w * x
        jx = lx - tx
        cy = sum(ax[i] for i, b in enumerate(B) if ax[i] > 0 and b > x)
        dme += jx - cy
    n += 1
    if Uw != K * d or m * dme != Uwx - (K + 1) * sy + rho * d:
        bad += 1
        if bad < 5: print("MISMATCH", m, rho, B, q, Uw, K * d, m * dme, Uwx - (K + 1) * sy + rho * d)
print("checked", n, "mismatches", bad)
