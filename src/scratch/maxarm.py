# Split of TOP'' at each non-top cell z: arms to tops u_a = t_a(z) in X; mu(z) = max pi, R(z) = sum of the other pi's.
#  (MA)  sum_z (mu(z) - psi(z))^+ <= m(m-1)/2            ("max-arm PE")
#  (NM)  sum_z R(z) + (d-1) sum_u pi(u) <= (d-1) m(m+1)/2  ("non-max arms")
#  MA + NM  =>  TOP''.
import sys, itertools, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def split(s):
    m, c = s.m, s.c; d = s.e - 1
    _, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}
    S = set(cells); pos = {x: ((w - c) % m) + 1 for x, w in cells.items()}
    top = {x for x, w in cells.items() if w >= c}
    MA = NM = 0
    for z in cells:
        if z in top: continue
        ps = []
        for a in range(d):
            t = z
            while True:
                y = t[:a] + (t[a] + 1,) + t[a+1:]
                if y in S: t = y
                else: break
            if t in top: ps.append(pos[t])
        if ps:
            mu = max(ps); MA += max(0, mu - pos[z]); NM += sum(ps) - mu
    sp = sum(pos[u] for u in top)
    return m, d, MA, NM + (d - 1)*sp, m*(m - 1)//2, (d - 1)*m*(m + 1)//2
if __name__ == '__main__':
    mode = sys.argv[1]; res = []
    if mode == 'genus':
        for g, s in all_by_genus(int(sys.argv[2])):
            if g and s.e >= 3: res.append((s.P, s.e) + split(s))
    else:
        rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3])
        while len(res) < N:
            m = rng.randint(20, int(sys.argv[4])); k = rng.choice([2, 3, 4])
            gens = sorted(set([m] + [rng.randint(m + 1, k*m) for _ in range(3)]))
            if len(gens) != 4 or reduce(gcd, gens) != 1: continue
            s = NS.from_generators(gens)
            if s.e == 4: res.append((s.P, s.e) + split(s))
        for a in range(5, 13):   # box family
            s = NS.from_generators([a*a, a*a + 1, a*a + a, a*a + a + 1]); res.append((s.P, s.e) + split(s))
    for e in sorted(set(r[1] for r in res)):
        R = [r for r in res if r[1] == e]
        fa = [r for r in R if r[4] > r[6]]; fn = [r for r in R if r[5] > r[7]]
        print(f'e={e}: n={len(R)} MA fails {len(fa)} NM fails {len(fn)}; max MA/budget {max(r[4]/max(1,r[6]) for r in R):.3f}; max NM/budget {max(r[5]/r[7] for r in R):.3f}')
        for r in fa[:3]: print('   MA fail', r[0], r[2:])
        for r in sorted(fn, key=lambda r: -r[5]/r[7])[:3]: print('   NM fail', r[0], r[2:])
