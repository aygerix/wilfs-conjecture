# classmate: for each Q3 class s (Q1': demand 1; M2': demand 2), count missing cube monomials in the same class (value
# congruent to s, not the rep) that have >= 1 standard parent square (so they contribute w_D >= 1 to D3), and their
# total weight W_s = sum w_D.  Q3T would follow from  sum_s min(W_s, ...)  if W_s >= dem(s) for all s (classes disjoint).
import sys
from itertools import combinations_with_replacement as cwr
for fn in sys.argv[1:]:
    n = 0; bad1 = bad2 = 0; badS = 0; ex = None; tot_short = 0
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); d = len(A); e = d + 1; n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl][0]: best[cl] = (key, c)
        sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
        D = set(rep.values())
        cubes = {}
        for c in cwr(range(d), 3): cubes.setdefault(sum(A[i] for i in c) % m, []).append(c)
        short = 0
        for s in sg:
            if sg[s] >= 2 * m: dem = 2
            elif sg[s] >= m and len(rep[s]) == 3 and not any(A[l] > s for l in rep[s]): dem = 1
            else: continue
            Ws = 0
            for y in cubes.get(s, []):
                if y == rep[s]: continue
                Ws += sum(y.count(i) for i in set(y) if tuple(sorted(y[:y.index(i)] + y[y.index(i) + 1:])) in D)
            if Ws < dem:
                short += dem - Ws
                if dem == 1: bad1 += 1
                else: bad2 += 1
        if short: badS += 1; tot_short = max(tot_short, short); ex = ex or (m, A, short)
    print(fn, n, 'S; S with a short Q3 class:', badS, '; short Q1p classes', bad1, '; short M2p classes', bad2, '; max shortfall', tot_short, 'ex', ex)
