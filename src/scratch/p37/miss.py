# miss: for S = <m, m+A> in Q5, list the U-tile D (lex-largest min-length reps of sigma = min(3A' n class)), the T-tile D^T
# (lex-largest min-length reps of tau), the missing level-2/3 vectors of D with the reason (collision = same value as the rep,
# wrap = value exceeds sigma by k*m), and the NE pairs (y = U-rep, z = T-rep).
import sys
from itertools import combinations_with_replacement as cwr
def vec(comb, d): return tuple(sum(1 for i in comb if i == q) for q in range(d))
def run(gens):
    m = gens[0]; A = [g - m for g in gens[1:]]; d = len(A); e = d + 1
    val = lambda x: sum(x[i] * A[i] for i in range(d))
    best = {}   # class -> (value, -len, lexkey) minimal value, then min length, then lex-largest
    allv = {}
    for k in range(0, 4):
        for comb in cwr(range(d), k):
            x = vec(comb, d); v = val(x); s = v % m; allv[x] = v
            key = (v, k, tuple(-t for t in x))
            if s not in best or key < best[s][0]: best[s] = (key, x)
    assert len(best) == m
    D = {s: best[s][1] for s in range(m)}; Dset = set(D.values()); sig = {s: val(D[s]) for s in range(m)}
    # T-tile by BFS over lengths up to 12
    bt = {}
    frontier = [tuple([0] * d)]
    for k in range(0, 14):
        for comb in cwr(range(d), k):
            x = vec(comb, d); v = val(x); s = v % m; key = (v, k, tuple(-t for t in x))
            if s not in bt or key < bt[s][0]: bt[s] = (key, x)
        if len(bt) == m and k >= 4 and all(bt[s][0][1] < k for s in bt): break
    tau = {s: bt[s][0][0] for s in range(m)}; DT = {s: bt[s][1] for s in range(m)}
    D3 = 3 * d * m - e * sum(sum(x) for x in D.values())
    lv = lambda S, k: sum(1 for x in S if sum(x) == k)
    print(f"S={gens} m={m} A={A} e={e} Delta3={D3} |D_k|={[lv(Dset,k) for k in range(4)]} |DT_k|={[lv(DT.values(),k) for k in range(8)]}")
    NE = [s for s in range(m) if tau[s] < sig[s]]
    for s in sorted(NE, key=lambda s: tau[s]):
        print(f"  NE class {s}: tau={tau[s]} z={DT[s]} |z|={sum(DT[s])}  sigma={sig[s]} y={D[s]} |y|={sum(D[s])} j={(sig[s]-tau[s])//m}")
    for k in (2, 3):
        miss = [x for x in allv if sum(x) == k and x not in Dset]
        col = [x for x in miss if allv[x] == sig[allv[x] % m]]
        wr = [x for x in miss if allv[x] != sig[allv[x] % m]]
        print(f"  level {k}: missing {len(miss)} = collisions {len(col)} + wraps {len(wr)}")
        for x in wr:
            s = allv[x] % m; print(f"     wrap {x} val={allv[x]} class {s} rep {D[s]} sigma={sig[s]} diff={(allv[x]-sig[s])//m}m {'NEclass' if s in NE else ''}")
        for x in col:
            s = allv[x] % m; print(f"     coll {x} val={allv[x]} rep {D[s]}")
for arg in sys.argv[1:]: run([int(t) for t in arg.split(',')])
