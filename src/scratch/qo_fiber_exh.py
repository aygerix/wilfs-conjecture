# Exhaustive check of Fiber Lemma claims (A), (B) [lattice-free] on the cone class: D = Cyl(h,F,G) \ (q + N^3), q in Cyl,
# q >= (1,1,1); h nonincreasing, len(h) <= L, h(0) <= L; F (len = len h), G (len = h(0)) nonincreasing in [1, V], F(0) = G(0).
import sys, itertools
sys.path.insert(0, 'src/scratch')
from cls_anneal import build
from qo_fiber_check import check
L, V, MAXM = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
def seqs(n, top, lo=1):
    if n == 0: yield (); return
    for v in range(lo, top + 1):
        for rest in seqs(n - 1, v, lo): yield (v,) + rest
n = 0; bad = 0; mx = [0, 0]
for nl in range(1, L + 1):
    for h in seqs(nl, L):
        for F0 in range(2, V + 1):
            for Fr in seqs(nl - 1, F0):
                F = (F0,) + Fr
                for Gr in seqs(h[0] - 1, F0):
                    G = (F0,) + Gr
                    Cyl = build(h, F, G, None)
                    if len(Cyl) > MAXM: continue
                    for q in Cyl:
                        if min(q) < 1: continue
                        D = build(h, F, G, q)
                        viol, nds, co, rk, qt, ny = check(D, q); n += 1
                        viol = [v for v in viol if v[0] in ('A', 'B', 'Drank', 'Dq')]
                        if viol:
                            bad += 1
                            if bad <= 5: print('VIOL', viol[:2], h, F, G, q)
                        mx = [max(mx[0], nds), max(mx[1], qt)]
print(f'L={L} V={V} |Cyl|<={MAXM}: {n} cone sets, violations of (A)/(B)/(D) {bad}; max #DS {mx[0]}, max qO-t {mx[1]}', flush=True)
