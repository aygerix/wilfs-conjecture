# neanat: per-class anatomy of Delta3 = 4 M2 + sum_{level-2 x in D} P(x) (column-top form) for one S in Q5.
# D = U-tile (standard monomial x_s of sigma_s: least value, then max length, then lex); P(x) = sum_{i: x+e_i not in D}
# (x_i + 1)(3 - |x|).  Classes: EQ / NE2 / NE3 (tau_s < sigma_s, level 2 / 3).  Prints the budget split and, for
# every level-2 class, P(x), its out-edges and whether the class is NE; for NE3 classes the T-parents.
import sys, heapq
from itertools import combinations_with_replacement as cwr
m = int(sys.argv[1]); A = list(map(int, sys.argv[2].split(','))); d = len(A); e = d + 1; mu = A[0]
best = {}
for k in range(4):
    for c in cwr(range(d), k):
        s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k, c)
        if cl not in best or key < best[cl]: best[cl] = key
rep = {cl: best[cl][2] for cl in best}; h = {cl: len(rep[cl]) for cl in best}; sg = {cl: best[cl][0] - h[cl] * m for cl in best}
assert len(best) == m
vec = lambda c: tuple(sum(1 for t in c if t == i) for i in range(d))
D = {vec(rep[cl]): cl for cl in best}
tau = [None] * m; tau[0] = 0; pq = [(0, 0)]; done = [False] * m; klen = {0: 0}
while pq:
    t, c = heapq.heappop(pq)
    if done[c]: continue
    done[c] = True
    for a in A:
        u = t + a; cc = u % m
        if tau[cc] is None or u < tau[cc]: tau[cc] = u; heapq.heappush(pq, (u, cc))
# least T-length of tau_s by DP over values
INF = 99; L = [INF] * (max(tau) + 1); L[0] = 0
for v in range(1, len(L)):
    L[v] = min([L[v - a] + 1 for a in A if a <= v and L[v - a] < INF] + [INF])
st = {cl: ('EQ' if tau[cl] == sg[cl] else ('NE%d' % h[cl])) for cl in range(m)}
cT = max(tau) - m + 1
def P(x):
    n = sum(x); return sum((x[i] + 1) * (3 - n) for i in range(d) if tuple(x[j] + (j == i) for j in range(d)) not in D)
M2 = sum(1 for c in cwr(range(d), 2) if vec(c) not in D)
D3 = 3 * (e - 1) * m - e * sum(h.values())
lev2 = [(x, cl) for x, cl in D.items() if sum(x) == 2]
B2 = sum(P(x) for x, _ in lev2); assert D3 == 4 * M2 + B2, (D3, M2, B2)
NE = [cl for cl in range(m) if st[cl] != 'EQ']
hlo_mu = sum(1 for cl in NE if tau[cl] < cT and tau[cl] % mu == 0); hhi = sum(1 for cl in NE if tau[cl] >= cT)
print(f"m={m} A={A} e={e} mu={mu} cT={cT} Delta3={D3} = 4*M2({M2}) + B2({B2}); h={len(NE)} NE2={sum(1 for c in NE if st[c]=='NE2')} NE3={sum(1 for c in NE if st[c]=='NE3')}")
print(f"  MU-LO rhs = mu*hlo_mu + hhi = {mu}*{hlo_mu} + {hhi} = {mu*hlo_mu+hhi}; ratio {(mu*hlo_mu+hhi)/D3:.3f}")
nm = lambda x: '+'.join(str(A[i]) + ('^%d' % x[i] if x[i] > 1 else '') for i in range(d) if x[i])
print('  NE classes (tau, k_T, status, sigma rep):')
for cl in sorted(NE, key=lambda c: tau[c]):
    print(f"    tau={tau[cl]:4d} k={L[tau[cl]]} {st[cl]} sigma={sg[cl]}={nm(vec(rep[cl]))}")
print('  level-2 classes with P > 0 sorted by P (EQ/NE, P, rep, out-edges):')
rows = sorted(((P(x), st[cl], x, cl) for x, cl in lev2), reverse=True)
for p, s_, x, cl in rows[:40]:
    outs = [A[i] for i in range(d) if tuple(x[j] + (j == i) for j in range(d)) in D]
    print(f"    P={p:3d} {s_:3s} sigma={sg[cl]:4d}={nm(x)} out={outs}")
print('  sum P over NE2 =', sum(p for p, s_, _, _ in rows if s_ == 'NE2'), ' over EQ level 2 =', sum(p for p, s_, _, _ in rows if s_ == 'EQ'))
