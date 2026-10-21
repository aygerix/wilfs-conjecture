# u0anat: anatomy of residual Q5 semigroups with U' = 0 (every element of U below c_T is a multiple of mu).
# There P1 = e|U cap [0,c_T)| - c_T; prints the extremal ones with T-minimal generators, redundant set R, the NE
# classes with their U-representations, and the gap classes below c_T with their sigma (level, value - class).
import sys, heapq
from itertools import combinations_with_replacement as cwr
def analyse(m, A):
    d = len(A); e = d + 1; mu = A[0]; best = {}; rep = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl]: best[cl] = key; rep[cl] = [A[i] for i in c]
    hS = {c: -best[c][1] for c in best}; sg = {c: best[c][0] - hS[c] * m for c in best}
    tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m
    while pq:
        t, c = heapq.heappop(pq)
        if done[c]: continue
        done[c] = True
        for a in A:
            u = t + a; cc = u % m
            if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
    cT = max(tau) - m + 1
    inU = lambda x: x >= sg[x % m]; inT = lambda x: x >= tau[x % m]
    Ulo = [x for x in range(cT) if inU(x)]
    gens = sorted(set(A) | {m}); Tmin = [g for g in gens if not any(inT(g - h) and g - h > 0 for h in gens if h < g)]
    return dict(e=e, mu=mu, m=m, cT=cT, Ulo=Ulo, P1=e * len(Ulo) - cT, Tmin=Tmin, R=[g for g in gens if g not in Tmin],
                NE=[(x, sg[x % m], rep[x % m]) for x in range(cT) if inT(x) and not inU(x)],
                gaps=[(x, sg[x % m] - x, rep[x % m]) for x in range(cT) if not inT(x)])
rows = []
for fn in sys.argv[2:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            m = int(t[1]); A = list(map(int, t[15:])); r = analyse(m, A)
            if all(x % r['mu'] == 0 for x in r['Ulo']): rows.append(r)
rows.sort(key=lambda r: r['P1'])
print(len(rows), 'residual S with U\' = 0; P1 histogram (lowest):', [r['P1'] for r in rows[:30]])
for r in rows[:int(sys.argv[1])]:
    print(f"P1={r['P1']} e={r['e']} mu={r['mu']} m={r['m']} cT={r['cT']} 4e-cT={4*r['e']-r['cT']} |Ulo|={len(r['Ulo'])} Tmin={r['Tmin']} R={r['R']}")
    print('   NE:', r['NE']); print('   gaps:', [(x, k, rp) for x, k, rp in r['gaps']])
