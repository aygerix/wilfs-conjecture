"""WRAP-MAX probe (lead, 2026-10-19).  Canonical lift P_a = <p_a>, v = x.P, k = floor(v/m) (phase-free wrap),
c = [label in top window [m-rho0, m)], K = k + c.  Exact cell form (any tile, any sigma):
  S = sum_{nonmax-top cols} |C| l(t) + m [ sum_A ((|y|-1) k_y + |y| c_y) - sum_N (d c_x + (d+1) k_x) ],  l = rho0 + v.
WRAP-MAX tiles: k = 0 on non-maximal cells.  Then the only uncovered deficit after the direct column charging is
F = {y in A : k_y = 1, c_y = 0, all |y| cells strictly below y in its columns lie in the window} (deficit m each).
Reports: identity check, #WRAP-MAX (tile,sigma), #with F nonempty, worst ratio |F| m / (S + m|F|), and examples.
usage: python wrapmax_test.py seed trials mmin mmax"""
import sys, random
from pmin_tile import apery, minimal_gens, tile

def analyse(m, n, D):
    d = len(n); P = [g % m for g in n]; Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = [y for y in D if all(up(y, a) not in Ds for a in range(d))]; As = set(A)
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}; k = {x: v[x]//m for x in D}
    wrapmax = all(k[x] == 0 for x in D if x not in As)
    cols = []
    for b in range(d):
        for t in D:
            if up(t, b) in Ds: continue
            col = [t]; y = list(t)
            while y[b] > 0: y[b] -= 1; col.append(tuple(y))
            cols.append((b, t, col))
    out = []
    for sg in range(m):
        r0 = (-sg) % m
        c = {x: int((v[x] % m) >= m-r0) for x in D}; r = {x: (v[x]-sg) % m for x in D}
        S = (d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A)
        rhs = sum(len(col)*(r0+v[t]) for (b, t, col) in cols if t not in As) + \
            m*(sum((sum(y)-1)*k[y]+sum(y)*c[y] for y in A)-sum(d*c[x]+(d+1)*k[x] for x in D if x not in As))
        assert S == rhs, (m, n, sg, S, rhs)
        F = []; beta = 0
        if wrapmax:
            for (b, t, col) in cols:
                if c[t] == 1: beta += sum(1 for x in col if x != t and c[x] == 0)
            for y in A:
                if k[y] == 1 and c[y] == 0:
                    below = [tuple(y[j]-(j == b)*i for j in range(d)) for b in range(d) for i in range(1, y[b]+1)]
                    if all(c[x] == 1 for x in below): F.append(y)
        out.append((S, F, r0, beta))
    return wrapmax, out

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    H1fail = [0]; nwm = 0; nF = 0; ntot = 0; worst = None; shown = 0
    for tr in range(T):
        m = rng.randint(mmin, mmax); kk = rng.randint(2, 7)
        gens = [rng.randint(m+1, rng.choice([2, 3, 5])*m) for _ in range(kk)]
        if None in apery(m, gens): continue
        n, ap = minimal_gens(m, gens)
        if len(n) < 2: continue
        d = len(n); P = [g % m for g in n]
        for key in (lambda x: (sum(x), tuple(-t for t in x)), lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))):
            D = list(tile(m, n, ap, key).values())
            wm, out = analyse(m, n, D); ntot += 1
            if not wm: continue
            nwm += 1
            for (S, F, r0, beta) in out:
                assert S >= 0
                if beta < len(F):
                    H1fail[0] += 1
                    if H1fail[0] <= 5: print("H1 FAIL m", m, "n", n, "rho0", r0, "S", S, "F", F, "beta", beta)
                if F:
                    nF += 1; ratio = len(F)*m/(S+len(F)*m)
                    if worst is None or ratio > worst[0]: worst = (ratio, m, n, r0, S, F)
                    if shown < 4: print("F example m", m, "n", n, "rho0", r0, "S", S, "F", F); shown += 1
    print("H1 (beta >= |F|) failures:", H1fail[0]); print("tiles", ntot, "WRAP-MAX tiles", nwm, "(tile,sigma) with F nonempty", nF, "worst m|F|/(S+m|F|)", worst)
