"""List nontrivial equality cases of T1 (J - C = rho + r with J - C > 0) among small true-depth P18 models and print
their canonical structure: position, level, degree, wraps, c_y, rep. Usage: python t1tight.py Q MMAX KMAX NSHOW"""
import sys, itertools
sys.path.insert(0, __import__('os').path.dirname(__file__))
from idq import canon
Q, MMAX, KMAX, NSHOW = map(int, sys.argv[1:5]); shown = 0; tot = 0; tight = 0
from collections import Counter
pat = Counter()
for m in range(5, MMAX + 1):
    for rho in range(0, m - 1):
        for K in range(2, KMAX + 1):
            for B in itertools.combinations(range(1, m), K):
                best = canon(m, rho, list(B), Q, Q + 3)
                if (m - 1) not in best or best[m - 1][0] < Q: continue
                reach = {x: v for x, v in best.items() if v[0] <= Q}
                r = m - len(reach); JC = 0; rows = []
                for x, (lx, tx, cx, ax) in sorted(reach.items()):
                    cy = sum(ax[i] for i, b in enumerate(B) if ax[i] > 0 and b > x)
                    JC += (lx - tx) - cy
                    if lx > tx or cy: rows.append((x, lx, tx, lx - tx, cy, [b for i, b in enumerate(B) for _ in range(ax[i])]))
                tot += 1
                if JC > 0 and JC == rho + r:
                    tight += 1
                    pat[(rho > 0, r > 0, any(b >= m - rho for b in B))] += 1
                    if shown < NSHOW:
                        shown += 1
                        print("TIGHT m=%d rho=%d B=%s q=%d r=%d J-C=%d holes=%s" % (m, rho, B, Q, r, JC, [x for x in range(m) if x not in reach]))
                        for row in rows: print("   pos %2d lev %d deg %d j %d c %d rep %s" % row)
print("models", tot, "nontrivial tight", tight, "patterns (rho>0, r>0, strip)", dict(pat))
