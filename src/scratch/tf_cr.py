# Two-face e = 4 tiles: crude residue-free bound CR (sum_i i*T_(i) >= (m-1)(T(A) - 2m)) and T(A) - 2m, split by t.
# Also asserts: t = 0 => each face has <= 1 inner corner and |A| <= 4.
import sys, itertools, collections, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def inner_corners(F):
    U = max(u for u, v in F) + 2; V = max(v for u, v in F) + 2
    return [(u, v) for u in range(1, U) for v in range(1, V) if (u, v) not in F and (u-1, v) in F and (u, v-1) in F]
def tf(s):
    p, best = factorizations_down_set(s, 'grlex'); D = set(best.values()); d = 3; m = s.m
    faces = [(a, b) for a in range(d) for b in range(a + 1, d) if tuple(int(i in (a, b)) for i in range(d)) not in D]
    if len(faces) != 1: return None
    a, b = faces[0]; c = 3 - a - b
    w = (p[a] + p[b]) % m
    z = [x for x in D if sum(xi*pi for xi, pi in zip(x, p)) % m == w][0]; t = z[c]
    A = [x for x in D if all(x[:i] + (x[i] + 1,) + x[i+1:] not in D for i in range(d))]
    T = sorted((3 + sum(y) for y in A), reverse=True)
    cr = sum(i*Ti for i, Ti in enumerate(T)) - (m - 1)*(sum(T) - 2*m)
    if t == 0:
        F1 = {(x[a], x[c]) for x in D if x[b] == 0}; F2 = {(x[b], x[c]) for x in D if x[a] == 0}
        assert len(inner_corners(F1)) <= 1 and len(inner_corners(F2)) <= 1 and len(A) <= 4, (s.P,)
    return t, m, sum(T) - 2*m, cr, len(A)
stats = collections.defaultdict(lambda: [0, -10**9, 10**9, 0])
def rec(r, P):
    if r is None: return
    t, m, ex, cr, nA = r; k = min(t, 3); st = stats[k]
    st[0] += 1
    if ex > st[1]: st[1] = ex
    if cr < st[2]: st[2] = cr
    if cr < 0: st[3] += 1; print('  CR fails', P, 't', t, 'excess', ex, 'cr', cr)
mode = sys.argv[1]
if mode == 'exh':
    for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        for g3 in itertools.combinations(range(m + 1, int(sys.argv[4])*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e == 4: rec(tf(s), s.P)
else:
    rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); lo, hi = int(sys.argv[4]), int(sys.argv[5]); n = 0
    while n < N:
        m = rng.randint(lo, hi); gens = sorted(set([m] + [rng.randint(m + 1, rng.choice([2, 3, 5])*m) for _ in range(3)]))
        if len(gens) != 4 or reduce(gcd, gens) != 1: continue
        s = NS.from_generators(gens)
        if s.e != 4: continue
        r = tf(s)
        if r: n += 1; rec(r, s.P)
for k in sorted(stats): print(f't={k}{"+" if k == 3 else ""}: n {stats[k][0]}, max T(A)-2m {stats[k][1]}, min CR slack {stats[k][2]}, CR fails {stats[k][3]}')
