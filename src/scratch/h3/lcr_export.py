"""Export the CR-failing (core, s) pairs with k+s >= 6 for core dimension k, one per S_k orbit (lead, 2026-10-19).
Line format: m s ncells then the cells (each as k digits, the exponent vector) and a coefficient per cell in the
spike form of MaxCL: N cells (origin, units, non-maximal pairs) get d+1 = k+s+1, maximal pairs -1, cubics -2.
usage: python lcr_export.py k > cases_k.txt"""
import sys, itertools
from lcr3_exh import shapes, cr_fail_range
k = int(sys.argv[1]); seen = set(); out = []
perms = list(itertools.permutations(range(k)))
def canon(P, T):
    best = None
    for pi in perms:
        Pp = tuple(sorted(tuple(sorted(pi[a] for a in z)) for z in P)); Tp = tuple(sorted(tuple(sorted(pi[a] for a in y)) for y in T))
        if best is None or (Pp, Tp) < best: best = (Pp, Tp)
    return best
norb = 0; ncases = 0
for P, T in shapes(k):
    if not T: continue
    ss = cr_fail_range(k, P, T)
    if ss is None: continue
    assert ss != float('inf'), "a shape fails CR for every s: needs separate treatment"
    c = canon(P, T)
    if c in seen: continue
    seen.add(c); P, T = c; norb += 1
    Tset = set(T); PN = set(z for z in P if any(tuple(sorted(z+(x,))) in Tset for x in range(k)))
    size = 1+k+len(P)+len(T)
    def vec(t):
        v = [0]*k
        for a in t: v[a] += 1
        return ''.join(map(str, v))
    for s in range(max(0, 6-k), int(ss)+1):
        if s >= ss: break
        dd = k+s; m = size+s; ncases += 1
        cells = [('0'*k, dd+1)]+[(vec((a,)), dd+1) for a in range(k)]+[(vec(z), dd+1 if z in PN else -1) for z in P]+[(vec(y), -2) for y in T]
        print(m, s, len(cells), ' '.join(f"{c}:{w}" for c, w in cells))
print(f"# k={k} orbits={norb} cases={ncases}", file=sys.stderr)
