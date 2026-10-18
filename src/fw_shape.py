"""Shape-only consequences of FWx in the deep regime (c > 3m): which crude inequalities hold?
  FW3 : m/2 + D >= sum_Z |z|_1          (final-line residues bounded by z_j distinct residues <= m-1 each)
  FW3b: C(m,2) + sum_deep (m + C(L,2)) >= sum_Z sum_j (z_j (m-1) - C(z_j, 2))   (same, exact form)
  also reports tau/m, sum_Z|z|/m, D/m."""
import sys, random
from math import comb
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def shape(s):
    m, c = s.m, s.c
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp)
    T = set(best.values()); lam = {x: w for w, x in best.items()}
    Z = [x for x in T if lam[x] >= c]
    D = 0; deepsum = 0
    for j in range(d):
        for x in T:
            if tuple(x[i] + (i == j) for i in range(d)) in T or lam[x] >= c: continue
            L = x[j] + 1; D += 1; deepsum += m + comb(L, 2)
    sz = sum(sum(z) for z in Z)
    fw3 = m / 2 + D - sz
    fw3b = comb(m, 2) + deepsum - sum(z[j] * (m - 1) - comb(z[j], 2) for z in Z for j in range(d))
    return dict(m=m, e=d + 1, q=-(-c // m), tau=len(Z), sz=sz, D=D, fw3=fw3, fw3b=fw3b)
if __name__ == '__main__':
    mode = sys.argv[1]; rnd = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    if mode == 'g':
        src = (s for g, s in all_by_genus(int(sys.argv[2])) if g > 0 and len(s.P) >= 2 and s.c > 3 * s.m)
    else:
        def gen():
            for it in range(int(sys.argv[2])):
                m = rnd.randint(12, 70); d = rnd.randint(3, 8); K = rnd.choice((3, 4, 6, 8))
                try: s = NS.from_generators([m] + rnd.sample(range(m + 1, K * m), d))
                except ValueError: continue
                if s.c > 3 * s.m: yield s
        src = gen()
    n = 0; bad3 = []; bad3b = []
    for s in src:
        r = shape(s); n += 1
        if r['fw3'] < 0: bad3.append((s.P, r))
        if r['fw3b'] < 0: bad3b.append((s.P, r))
    print(f'{mode}: {n} deep S (c > 3m); FW3 fails {len(bad3)}, FW3b fails {len(bad3b)}')
    for x in bad3b[:8]: print('  FW3b-bad', x)
    for x in bad3[:8]: print('  FW3-bad', x)
