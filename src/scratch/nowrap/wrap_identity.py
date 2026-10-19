"""Check the column/wrap identity for MaxCL (lead, 2026-10-19) on Apery tiles and no-wrap tiles.
For a tile (D, p mod m), canonical lift P_a = p_a mod m in [0,m), v(x) = x.P (integer), E = sum_D floor(v/m).
At phase sigma: rho0 = (-sigma) mod m, l(x) = rho0 + v(x), K(x) = floor(l/m), r(x) = l - mK = (phi(x)-sigma) mod m.
Columns: for each direction b, the b-columns (maximal chains t, t-e_b, ..., with top t: t+e_b not in D).
Claim (exact):  S(sigma) = sum_{nonmax-top cols} sum_{x in C} (l(t) - m K(x))
                         + m * sum_{max-top cols} sum_{x in C} (K(t) - K(x))  -  m*E,
where S = (d+1) sum_N r - sum_A (|y|-1) r.  Both column sums are >= 0, so E = 0 (no-wrap lift) implies MaxCL.
usage: python wrap_identity.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup

def identity_check(m, P, D):
    d = len(P)
    def up(x, a): y = list(x); y[a] += 1; return tuple(y)
    Dset = set(D)
    A = {x for x in D if all(up(x, a) not in Dset for a in range(d))}
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    E = sum(v[x]//m for x in D)
    tops = []  # (b, top, column cells)
    for b in range(d):
        for x in D:
            if up(x, b) not in Dset:
                col = [x]; y = list(x)
                while y[b] > 0:
                    y[b] -= 1; col.append(tuple(y))
                tops.append((b, x, col))
    worst = None
    for sg in range(m):
        r0 = (-sg) % m
        l = {x: r0 + v[x] for x in D}; K = {x: l[x]//m for x in D}; r = {x: l[x] - m*K[x] for x in D}
        S = (d+1)*sum(r[x] for x in D if x not in A) - sum((sum(y)-1)*r[y] for y in A)
        nonmax = sum(l[t] - m*K[x] for (b, t, col) in tops if t not in A for x in col)
        maxw = m*sum(K[t] - K[x] for (b, t, col) in tops if t in A for x in col)
        rhs = nonmax + maxw - m*E
        assert S == rhs, (m, P, sg, S, rhs)
        if worst is None or S < worst[0]: worst = (S, sg, nonmax, maxw, m*E)
    return worst, E

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed); n = 0; nE0 = 0
    for tr in range(T):
        m = rng.randint(mmin, mmax)
        gens = sorted(set(rng.randint(m+1, 3*m) for _ in range(rng.randint(2, 6))))
        gens = [g for g in gens if g % m]
        gens = [g for g in gens if not in_semigroup(g, m, [h for h in gens if h != g])]
        if len(gens) < 2 or len(set(g % m for g in gens)) < len(gens): continue
        best = apery_tile(m, gens)
        if len(best) != m: continue
        D = [x for (w, x) in best.values()]
        P = [g % m for g in gens]
        worst, E = identity_check(m, P, D); n += 1; nE0 += (E == 0)
    print("Apery tiles checked", n, "identity holds at every phase; tiles with E = 0:", nE0)
