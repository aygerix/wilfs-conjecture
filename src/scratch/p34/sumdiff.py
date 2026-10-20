r"""Sum-difference conditions versus CR_DEP (lead, 2026-10-21). For a lattice tile D and any finite Delta subset N^d,
E = {x in D : x + Delta subset D} gives an injective labeling on E - Delta, so |E - Delta| <= m (SD(Delta)).
For every CR_DEP-failing down-set D (N = 2, 3), search Delta over all sub-down-sets of D (and their translates are
irrelevant) for a violated SD(Delta).  Usage: python sumdiff.py N MMIN MMAX"""
import sys
sys.path.insert(0, '.')
from subadd_lp import downsets
from crdep import crdep
def subdownsets(D, N):
    Ds = sorted(D, key=sum); out = [frozenset([(0,) * N])]; seen = set(out)
    stack = list(out)
    while stack:
        S = stack.pop()
        for x in Ds:
            if x in S: continue
            if all(x[t] == 0 or tuple(x[s] - (s == t) for s in range(N)) in S for t in range(N)):
                T = S | {x}
                if T not in seen: seen.add(T); stack.append(T)
    return seen
def sd_violation(D, N, m):
    Ds = set(D)
    for Dl in subdownsets(D, N):
        E = [x for x in D if all(tuple(a + b for a, b in zip(x, s)) in Ds for s in Dl)]
        diff = {tuple(a - b for a, b in zip(x, s)) for x in E for s in Dl}
        if len(diff) > m: return sorted(Dl), len(diff)
    return None
N, MMIN, MMAX = map(int, sys.argv[1:4])
for m in range(MMIN, MMAX + 1):
    fails = caught = 0; esc = []
    for D in downsets(N, m):
        sl, dep = crdep(D, N)
        if sl >= 0: continue
        fails += 1; v = sd_violation(D, N, m)
        if v: caught += 1
        else: esc.append(D)
    print("N=%d m=%d CR_DEP-failing down-sets %d, excluded by some SD(Delta) %d, escaping %d %s" % (N, m, fails, caught, len(esc), esc[:1]), flush=True)
