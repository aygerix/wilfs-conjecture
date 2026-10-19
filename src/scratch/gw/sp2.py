# Shape-only sufficient condition for P_2 in the multiplicity form (all n_a > m).
#   P_2:  2(m-1) - d1  <=  d (|L1| + |L2|),  d1 = #{a : k_a = 1}  (exact left side in multiplicity form)
#   shape bounds: L1 >= NonMax = D \ T1,  L2 >= {w : some upward path of value >= 2m} = D \ (T1 u T2(A1)),
#   T2(A1) = non-maximal w all of whose upper covers are maximal and use directions in A1 = {a : k_a = 1}.
#   SP2(D, A1):  2(m-1) - |A1|  <=  d (2m - 2|T1| - |T2(A1)|).
# Test SP2 on all down-sets containing every unit vector and every subset A1 of [d].
import sys
from itertools import combinations
d, m0, m1 = map(int, sys.argv[1:4])
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
def downsets(M):
    lev = {frozenset([tuple([0] * d)])}
    for m in range(1, M + 1):
        if m >= m0: yield m, lev
        nxt = set()
        for D in lev:
            for x in D:
                for u in U:
                    y = add(x, u)
                    if y not in D and all(y[a] == 0 or sub(y, U[a]) in D for a in range(d)): nxt.add(D | {y})
        lev = nxt
for m, lev in downsets(m1):
    tot = bad = 0; worst = None
    for D in lev:
        if any(u not in D for u in U): continue
        up = {x: [a for a in range(d) if add(x, U[a]) in D] for x in D}
        T1 = [x for x in D if not up[x]]
        T1s = set(T1)
        for r in range(d + 1):
            for A1 in combinations(range(d), r):
                A1s = set(A1)
                T2 = [x for x in D if up[x] and all(a in A1s and add(x, U[a]) in T1s for a in up[x])]
                tot += 1
                slack = d * (2 * m - 2 * len(T1) - len(T2)) - (2 * (m - 1) - len(A1))
                if slack < 0:
                    bad += 1
                    if worst is None or slack < worst[0]: worst = (slack, sorted(D), A1)
    print(f"d={d} m={m} pairs={tot} SP2-fail={bad} worst={worst}", flush=True)
