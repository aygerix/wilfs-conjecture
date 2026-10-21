r"""Does the difference-body family explain H3-CASEA? (lead, 2026-10-20)
For every height-<=3 down-set D in N^d containing all units (d = 3, 4) with a cubic cell and case-B margin
mu = Sigma_supp - Dep >= 1, test the shape inequalities DB_U: |D_U - U| <= |D|, where D_U = {b : b + U subset of D},
for every U in a family (all subsets of Delta_2 containing 0, up to size USZ).  A lattice tile satisfies every DB_U
(if b - u = b' - u' mod L then b + u' = b' + u in D).  Reports how many case-B shapes survive all DB_U.
Usage: python shape_db.py d USZ"""
import sys, itertools
d, USZ = map(int, sys.argv[1:3])
E = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
pairs = sorted(set(add(E[a], E[b]) for a in range(d) for b in range(d)))
trips = sorted(set(add(add(E[a], E[b]), E[c]) for a in range(d) for b in range(d) for c in range(d)))
def mu(D):
    Ds = set(D); dep = 0; ss = 0
    for x in D:
        T = [b for b in range(d) if add(x, E[b]) not in Ds]
        if len(T) < d: dep += sum(x[b] + 1 for b in T)
        ss += max(0, sum(1 for t in x if t) - 1)
    return ss - dep
zero = (0,) * d
D2 = [zero] + E + pairs
Ufam = [U for k in range(2, USZ + 1) for U in itertools.combinations(D2, k) if zero in U]
def db_fail(D):
    Ds = set(D)
    for U in Ufam:
        DU = [b for b in D if all(add(b, u) in Ds for u in U)]
        if not DU: continue
        S = set(sub(b, u) for b in DU for u in U)
        if len(S) > len(D): return U, len(S)
    return None
tot = cb = surv = 0; ex = []
for P in itertools.chain.from_iterable(itertools.combinations(pairs, k) for k in range(len(pairs) + 1)):
    Pset = set(P); base = [zero] + E + list(P)
    elig = [t for t in trips if all(sub(t, E[b]) in Pset or sub(t, E[b]) in E or min(sub(t, E[b])) < 0 for b in range(d))
            and all((min(sub(t, E[b])) < 0) or (sub(t, E[b]) in Pset) for b in range(d))]
    for k in range(1, len(elig) + 1):
        for R in itertools.combinations(elig, k):
            tot += 1; D = base + list(R); v = mu(D)
            if v >= 1:
                cb += 1; f = db_fail(D)
                if f is None:
                    surv += 1
                    if len(ex) < 5: ex.append((v, len(D), sorted(P), sorted(R)))
print("d=%d USZ=%d height-3 shapes %d, case-B %d, surviving every DB_U %d; examples %s" % (d, USZ, tot, cb, surv, ex), flush=True)
