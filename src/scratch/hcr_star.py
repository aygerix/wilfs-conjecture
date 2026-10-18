# Near-star tiles: d ~ gamma*sqrt(m) generators in (m, 2m), so Ap lives at levels <= 2 (or 3).
# Prediction (exact count for pure level-2 tiles D = {0, e_a} + Q, |Q| = q, every e_a covered):
#   HCR = [(m+1)(d(d+1) - 2q) + (d+2) q(q-1)/2] / [(d-1) m (m-1)/2]  ~  1 - 1/d  for q ~ beta d^2.
import sys, random; sys.path.insert(0, 'src'); sys.path.insert(0, 'fwx')
from ns import NS
from cl import factorizations_down_set
from hcr import parts
rnd = random.Random(int(sys.argv[1]))
for m in map(int, sys.argv[2].split(',')):
    for gam in map(float, sys.argv[3].split(',')):
        d = max(3, round(gam * m ** 0.5)); best = None
        for trial in range(int(sys.argv[4])):
            g = [m] + sorted(rnd.sample(range(m + 1, 2 * m), d))
            try: s = NS.from_generators(g)
            except Exception: continue
            if s.e != d + 1: continue
            Pp, bst = factorizations_down_set(s, 'grlex'); D = set(bst.values())
            lev = max(sum(x) for x in D); q2 = sum(1 for x in D if sum(x) == 2)
            hcr, hto, two, W = parts(s)
            if best is None or hcr < best[0]: best = (round(hcr, 4), lev, q2, s.c, W, two)
        print(f"m={m} d={d} e={d+1} (3e={3*d+3}) worst HCR {best}  [HCR, max level, #level-2 cells, c, W, two-face]", flush=True)
