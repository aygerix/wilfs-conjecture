# t = 1 two-face e = 4 semigroups S = <m, pa, pb, pa + pb - n m>: hook picture Omega' = psi(D), psi(i,j,k) = (i+k, j+k).
# Classify Omega' (rectangle / L-shape / not a down-set) and record CR, MaxCL(sigma = c) slack, W/m per class.
import sys, itertools, collections, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def analyse(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells); d = 3; m = s.m; c = s.c
    faces = [(a, b) for a in range(d) for b in range(a + 1, d) if tuple(int(i in (a, b)) for i in range(d)) not in D]
    if len(faces) != 1: return None
    a, b = faces[0]; cx = 3 - a - b
    w = (p[a] + p[b]) % m
    z = [x for x in D if sum(xi*pi for xi, pi in zip(x, p)) % m == w][0]
    if z[cx] != 1: return None
    n = (p[a] + p[b] - p[cx]) // m; assert p[a] + p[b] - p[cx] == n*m and n >= 1
    Om = {(x[a] + x[cx], x[b] + x[cx]) for x in D}; assert len(Om) == m
    down = all((u-1, v) in Om for u, v in Om if u) and all((u, v-1) in Om for u, v in Om if v)
    if down:
        U = max(u for u, v in Om) + 1; V = max(v for u, v in Om) + 1
        kind = 'rect' if len(Om) == U*V else 'L'
    else: kind = 'non-down'
    A = [x for x in D if all(x[:i] + (x[i] + 1,) + x[i+1:] not in D for i in range(d))]
    T = sorted((3 + sum(y) for y in A), reverse=True)
    cr = sum(i*Ti for i, Ti in enumerate(T)) - (m - 1)*(sum(T) - 2*m)
    r = {x: (cells[x] - c) % m for x in D}
    mc = 1 - sum((3 + sum(y))*r[y] for y in A)/(2*m*(m - 1))
    W = s.W if isinstance(s.W, int) else s.W()
    return kind, n, cr, mc, W/m, sum(T) - 2*m
if __name__ == '__main__':
    st = collections.defaultdict(list)
    if sys.argv[1] == 'exh':
        for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            for g3 in itertools.combinations(range(m + 1, int(sys.argv[4])*m), 3):
                if reduce(gcd, (m,) + g3) != 1: continue
                s = NS.from_generators([m, *g3])
                if s.e != 4: continue
                r = analyse(s)
                if r: st[r[0]].append((r, s.P))
    else:  # random t=1 two-face: pick m, pa, pb, n
        rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); lo, hi = int(sys.argv[4]), int(sys.argv[5]); cnt = 0
        while cnt < N:
            m = rng.randint(lo, hi); pa = rng.randint(m + 1, 3*m); pb = rng.randint(m + 1, 3*m); n = rng.randint(1, 3)
            pc = pa + pb - n*m
            if pc <= m or len({pa, pb, pc}) < 3 or reduce(gcd, (m, pa, pb, pc)) != 1: continue
            s = NS.from_generators([m, pa, pb, pc])
            if s.e != 4: continue
            r = analyse(s)
            if r: st[r[0]].append((r, s.P)); cnt += 1
    for k, L in st.items():
        print(f'{k}: n={len(L)} CR fails {sum(r[2] < 0 for r, P in L)}, min MaxCL slack {min(r[3] for r, P in L):.3f}, min W/m {min(r[4] for r, P in L):.3f}, max T(A)-2m {max(r[5] for r, P in L)}')
        for r, P in sorted(L, key=lambda z: z[0][3])[:3]: print('    ', P, 'n', r[1], 'CR', r[2], 'maxcl', round(r[3], 3), 'W/m', round(r[4], 3))
