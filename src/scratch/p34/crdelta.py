r"""CR-delta (lead, 2026-10-20): delta-dependent rearrangement relaxation of DEP-CARRY via the inversion form.
Exact (PROVED): V(sigma) = N(sigma) - kappa0, N = #{(x,a): x below its a-top at distance k, r(x) >= m - <k delta_a>},
kappa0 = (sum_{(x,a)} <k_a(x) delta_a> - M')/m.  DEP-CARRY <=> N(sigma) + Dep >= kappa0.
CR-delta: min over ALL bijections pi: D -> Z/m of sum_{(x,a)} [pi(x) >= m - s_a(x)]  + Dep >= kappa0.
(min-cost assignment, scipy).  Modes: 'sg NS SEED MMIN MMAX' | 'one m g1 .. gk'."""
import sys, random
import numpy as np
from scipy.optimize import linear_sum_assignment
sys.path.insert(0, '.')
from tile import build
def crdelta(m, D, delta):
    N = len(delta); Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    s = {x: [] for x in D}; dep = 0
    for a in range(N):
        for x in D:
            k = 0; y = x
            while up(y, a) in Ds: y = up(y, a); k += 1
            if k: s[x].append((k * delta[a]) % m)
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    for a in range(N):
        for x in D:
            if up(x, a) not in Ds and x not in mx: dep += x[a] + 1
    tot = sum(v for x in D for v in s[x]); Mp = m * (m - 1) // 2
    assert (tot - Mp) % m == 0
    k0 = (tot - Mp) // m
    C = np.zeros((m, m))
    for i, x in enumerate(D):
        for v in s[x]:
            if v: C[i, m - v:] += 1
    ri, ci = linear_sum_assignment(C)
    nmin = int(C[ri, ci].sum())
    # actual N at every phase
    lab0 = [sum(p * q for p, q in zip(x, delta)) % m for x in D]
    nact = min(int(sum(C[i, (lab0[i] + rho) % m] for i in range(m))) for rho in range(m))
    return nmin + dep - k0, nact + dep - k0, dep, k0
if __name__ == '__main__':
    if sys.argv[1] == 'one':
        v = list(map(int, sys.argv[2:])); c, gens, M = build(v[0], v[1:])
        print(crdelta(v[0], list(M), [g % v[0] for g in gens]))
    else:
        NS, SEED, MMIN, MMAX = map(int, sys.argv[2:6]); rnd = random.Random(SEED)
        cnt = fo = fa = 0; wo = wa = None; byop = [0, 0]
        while cnt < NS:
            m = rnd.randint(MMIN, MMAX); c0 = rnd.randint(m + 1, 9 * m)
            G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(12, c0 - 2))))
            R = build(m, G)
            if R is None: continue
            c, gens, M = R; N = len(gens)
            if N < 2 or c <= m: continue
            cnt += 1; op = int(3 * (N + 1) < m and c > 4 * m); byop[op] += 1
            sl, slact, dep, k0 = crdelta(m, list(M), [g % m for g in gens])
            assert slact >= 0
            if sl < 0:
                fa += 1; fo += op
                if wa is None or sl / m < wa[0]: wa = (sl / m, sl, dep, k0, m, gens, c, op)
        print("S %d (open %d): CR-delta fails %d (open %d); worst %s" % (cnt, byop[1], fa, fo, wa))
