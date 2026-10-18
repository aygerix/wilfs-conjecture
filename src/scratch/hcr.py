# HCR: column-wise combination of the height bound and the residue rearrangement bound inside CH'.
#   CH':  m W + (d-1) m (m-1)/2 = B := sum_a sum_{a-columns C} |C| (Lam - lam(top C)),  Lam = max lam on D.
#   Non-maximal top t: Lam - lam(t) >= (m+1) ht(t) (ht = longest upward path in D from t).
#   Maximal tops: Lam - lam(t) are distinct values in [0, m-1] residue classes, so sum_A T(t)(Lam - lam(t)) >= sum_i T_(i) i.
#   HCR(D): (m+1) sum_{(x,a): top_a(x) non-maximal} ht(top_a(x)) + sum_i T_(i) i >= (d-1) m (m-1)/2   ==> W >= 0.
import sys, random, time; sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def parts(s):
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp); D = set(best.values()); m = s.m
    lam = {x: w for w, x in best.items()}; Lam = max(lam.values())
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, u)] + 1 for u in U if add(x, u) in D], default=0)
    A = {y for y in D if ht[y] == 0}
    def top(x, a):
        while add(x, U[a]) in D: x = add(x, U[a])
        return x
    B = 0; Hn = 0
    for x in D:
        for a in range(d):
            t = top(x, a); B += Lam - lam[t]
            if t not in A: Hn += ht[t]
    W = s.e * (s.c - s.g) - s.c
    assert m * W + (d - 1) * m * (m - 1) // 2 == B, (s.P, m * W + (d - 1) * m * (m - 1) // 2, B)
    T = sorted((d + sum(y) for y in A), reverse=True)
    need = (d - 1) * m * (m - 1) / 2
    two = any(add(U[a], U[b]) not in D for a in range(d) for b in range(a + 1, d))
    hcr = ((m + 1) * Hn + sum(i * t for i, t in enumerate(T))) / need
    ht_only = (m + 1) * sum(ht[top(x, a)] for x in D for a in range(d)) / need
    return hcr, ht_only, two, W
if __name__ == '__main__':
    if sys.argv[1] == 'list':
        for g in sys.argv[2:]:
            s = NS.from_generators(list(map(int, g.split(','))))
            hcr, hto, two, W = parts(s)
            print(f'<{g}> W={W} two-face={two}: HCR {hcr:.3f}  HT {hto:.3f}  (>= 1 certifies Wilf)')
    else:
        E0, E1, seed, budget, mmax, K = map(int, sys.argv[2:8]); rnd = random.Random(seed); t0 = time.time(); res = {}
        while time.time() - t0 < budget:
            e = rnd.randint(E0, E1); m = rnd.randint(3 * e + 1, mmax)
            try: s = NS.from_generators([m] + rnd.sample(range(m + 1, K * m), e - 1))
            except ValueError: continue
            if s.e != e or s.c <= 3 * s.m: continue
            hcr, hto, two, W = parts(s)
            R = res.setdefault((e, two), [0, 0, 0, None]); R[0] += 1; R[1] += hcr < 1 - 1e-12; R[2] += hto < 1 - 1e-12
            if R[3] is None or hcr < R[3][0]: R[3] = (round(hcr, 4), s.P)
        for k in sorted(res): print(f'  e={k[0]} two-face={k[1]}: {res[k][0]} S, HCR fails {res[k][1]}, HT fails {res[k][2]}, worst HCR {res[k][3]}')
