# Two-face e = 4 tiles: test candidate 2-D-type inequalities over ALL sigma.
#  C3a: sum_{y in A} (|y|+1) r(y) <= 3M'          (=> MaxCL when 2 sum_A r <= M', e.g. |A| <= m/4)
#  C2 : sum_x [r(h x) + r(t_c x)] <= 3M'           (h = arm/leg end; axis cells use the b-row)
#  TCL: full Tile-CL  sum_a sum_x r(t_a x) <= 4M'
import sys, itertools, collections, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def check(s):
    p, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}; D = set(cells); d = 3; m = s.m
    faces = [(a, b) for a in range(d) for b in range(a + 1, d) if tuple(int(i in (a, b)) for i in range(d)) not in D]
    if len(faces) != 1: return None
    a, b = faces[0]; cx = 3 - a - b
    w = (p[a] + p[b]) % m
    z = [x for x in D if sum(xi*pi for xi, pi in zip(x, p)) % m == w][0]; t = z[cx]
    def top(x, i):
        while True:
            y = x[:i] + (x[i] + 1,) + x[i+1:]
            if y not in D: return x
            x = y
    A = [x for x in D if all(x[:i] + (x[i] + 1,) + x[i+1:] not in D for i in range(d))]
    M2 = m*(m - 1)//2
    phi = {x: cells[x] % m for x in D}
    res = []
    hx = {x: top(x, a) if x[b] == 0 and x[a] > 0 else top(x, b) for x in D}
    tc = {x: top(x, cx) for x in D}
    ta = {x: top(x, a) for x in D}; tb = {x: top(x, b) for x in D}
    worst = [10**9]*3
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}
        c3a = 3*M2 - sum((sum(y) + 1)*r[y] for y in A)
        c2 = 3*M2 - sum(r[hx[x]] + r[tc[x]] for x in D)
        tcl = 4*M2 - sum(r[ta[x]] + r[tb[x]] + r[tc[x]] for x in D)
        for i, v in enumerate((c3a, c2, tcl)):
            if v < worst[i]: worst[i] = v
    return t, m, worst, len(A)
stats = collections.defaultdict(lambda: [0, [10**9]*3, [0]*3, None])
def rec(r, P):
    if r is None: return
    t, m, worst, nA = r; st = stats[min(t, 2)]; st[0] += 1
    for i in range(3):
        if worst[i]/m < st[1][i]: st[1][i] = worst[i]/m
        if worst[i] < 0: st[2][i] += 1; 
    if worst[0] < 0 and st[3] is None: st[3] = (P, worst)
if sys.argv[1] == 'exh':
    for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        for g3 in itertools.combinations(range(m + 1, int(sys.argv[4])*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e == 4: rec(check(s), s.P)
else:
    rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); lo, hi = int(sys.argv[4]), int(sys.argv[5]); n0 = 0
    while n0 < N:
        m = rng.randint(lo, hi); pa = rng.randint(m + 1, 3*m); pb = rng.randint(m + 1, 3*m); n = rng.randint(1, 3); pc = pa + pb - n*m
        if pc <= m or len({pa, pb, pc}) < 3 or reduce(gcd, (m, pa, pb, pc)) != 1: continue
        s = NS.from_generators([m, pa, pb, pc])
        if s.e != 4: continue
        r = check(s)
        if r: rec(r, s.P); n0 += 1
for k in sorted(stats):
    st = stats[k]; print(f't={k}: n {st[0]}; min slack/m  C3a {st[1][0]:.2f}  C2 {st[1][1]:.2f}  TCL {st[1][2]:.2f}; fails C3a {st[2][0]} C2 {st[2][1]} TCL {st[2][2]}; first C3a fail {st[3]}')
