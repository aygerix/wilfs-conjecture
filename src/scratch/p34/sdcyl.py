r"""Do the proved tile properties SD (|E_Delta - Delta| <= m for every sub-down-set Delta) and CYL (cylinder lemma (b):
for every nonempty tau, #{minimal non-elements q : supp q >= tau} <= |D cap {x_tau = 0}|) exclude every CR_DEP-failing
down-set?  (lead, 2026-10-20).  Usage: python sdcyl.py N MMIN MMAX"""
import sys, itertools
sys.path.insert(0, '.')
from subadd_lp import downsets
from crdep import crdep
from sumdiff import sd_violation
def cyl_ok(D, N):
    Ds = set(D); H = max(max(x) for x in D) + 2
    G = []
    for q in itertools.product(range(H), repeat=N):
        if q in Ds: continue
        if all(q[t] == 0 or tuple(q[s] - (s == t) for s in range(N)) in Ds for t in range(N)): G.append(q)
    for k in range(1, N + 1):
        for tau in itertools.combinations(range(N), k):
            cnt = sum(1 for q in G if all(q[t] > 0 for t in tau))
            if cnt > sum(1 for x in D if all(x[t] == 0 for t in tau)): return False
    return True
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    f = sd = both = 0; esc = []
    for D in downsets(N, m):
        sl, dep = crdep(D, N)
        if sl >= 0: continue
        f += 1
        if sd_violation(D, N, m): continue
        sd += 1
        if not cyl_ok(D, N): continue
        both += 1; esc.append(D)
    print("N=%d m=%d CR_DEP-failing %d, passing SD %d, passing SD+CYL %d %s" % (N, m, f, sd, both, esc[:1]), flush=True)
