# peq: where does the EQ boundary come from?  For S in Q5 print NE classes (type, below/above, T-rep, U-rep), and every unused
# up-slot (x, i) of an EQ point x of D at level 1 or 2 (weight (x_i+1)(3-|x|)), classified: target class EQ/NE, collision/wrap.
import sys
from itertools import combinations_with_replacement as cwr
def vec(comb, d): return tuple(sum(1 for i in comb if i == q) for q in range(d))
def run(gens):
    m = gens[0]; A = [g - m for g in gens[1:]]; d = len(A); e = d + 1
    val = lambda x: sum(x[i] * A[i] for i in range(d))
    best = {}
    for k in range(0, 4):
        for comb in cwr(range(d), k):
            x = vec(comb, d); v = val(x); s = v % m; key = (v, k, tuple(-t for t in x))
            if s not in best or key < best[s][0]: best[s] = (key, x)
    D = {s: best[s][1] for s in range(m)}; Dset = set(D.values()); sig = {s: val(D[s]) for s in range(m)}
    bt = {}
    for k in range(0, 16):
        for comb in cwr(range(d), k):
            x = vec(comb, d); v = val(x); s = v % m; key = (v, k, tuple(-t for t in x))
            if s not in bt or key < bt[s][0]: bt[s] = (key, x)
        if len(bt) == m and k >= 4 and all(bt[s][0][1] < k for s in bt): break
    tau = {s: bt[s][0][0] for s in range(m)}; Tr = {s: bt[s][1] for s in range(m)}
    mt = max(tau.values())
    NE = {s for s in range(m) if tau[s] < sig[s]}
    D3 = 3 * d * m - e * sum(sum(x) for x in D.values())
    print(f"S={gens} A={A} e={e} D3={D3} maxtau={mt} maxsig={max(sig.values())} cT={mt-m+1}")
    for s in sorted(NE, key=lambda s: tau[s]):
        y = D[s]; typ = 'NE2' if sum(y) == 2 else 'NE3'
        print(f"  {typ} {'below' if sig[s] <= mt else 'ABOVE'} class {s}: tau={tau[s]} z={Tr[s]} |z|={sum(Tr[s])} sigma={sig[s]} y={y}")
    tot = {}
    for s in range(m):
        if s in NE: continue
        x = D[s]; h = sum(x)
        if h == 0 or h == 3: continue
        for i in range(d):
            u = tuple(x[q] + (q == i) for q in range(d))
            if u in Dset: continue
            w = (x[i] + 1) * (3 - h); vu = val(u); t = vu % m
            kind = ('coll' if vu == sig[t] else f"wrap{(vu - sig[t]) // m}") + ('->NE' if t in NE else '')
            tot[kind] = tot.get(kind, 0) + w
    print('  Peq by kind:', tot, 'total', sum(tot.values()))
for arg in sys.argv[1:]: run([int(t) for t in arg.split(',')])
