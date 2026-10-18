# Structure of 3-D tiles: minimal non-elements (generators of the complement ideal).
# Claims (proved on paper): (1) <= 1 full-support minimal non-element q*, and q* in Lambda (p.q* = 0 mod m);
# (2) a minimal non-element q with support {a,b} (q_c = 0) has p.q = t p_c (mod m) with t e_c in D, distinct t's;
# hence D = cylinders over the three coordinate slices minus (q* + N^3).
import sys, itertools
import numpy as np
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
d = 3
def minimal_nonelements(S):
    cand = set()
    for x in S:
        for a in range(d):
            y = x[:a] + (x[a] + 1,) + x[a+1:]
            if y not in S: cand.add(y)
    for a in range(d): cand.add(tuple(int(i == a) for i in range(d)) if False else None)
    cand.discard(None)
    # axis non-elements
    for a in range(d):
        L = 0
        while tuple(L if i == a else 0 for i in range(d)) in S: L += 1
        cand.add(tuple(L if i == a else 0 for i in range(d)))
    out = []
    for q in cand:
        if q in S: continue
        if all((q[a] == 0) or (q[:a] + (q[a] - 1,) + q[a+1:] in S) for a in range(d)): out.append(q)
    return out
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    P = np.array(np.meshgrid(*[np.arange(m)]*d, indexing='ij')).reshape(d, -1).T
    K = np.arange(m); nT = 0; bad = 0; maxfull = 0; stats = []
    for D in downsets(m, d):
        Dl = sorted(D)
        if any(all(n[a] == 0 for n in Dl) for a in range(d)): continue
        C = np.array(Dl); pos = (P @ C.T) % m
        ok = np.all(np.sort(pos, axis=1) == K, axis=1)
        if not ok.any(): continue
        S = set(Dl); mins = minimal_nonelements(S)
        full = [q for q in mins if all(q)]; maxfull = max(maxfull, len(full))
        for p in P[ok]:
            nT += 1
            if len(full) > 1 or any((np.dot(p, q) % m) != 0 for q in full): bad += 1; continue
            for c in range(d):
                ts = []
                for q in mins:
                    if q[c] == 0 and sum(1 for v in q if v) == 2:
                        r = int(np.dot(p, q) % m)
                        tt = [t for t in range(m) if tuple(t if i == c else 0 for i in range(d)) in S and (t*p[c]) % m == r]
                        if len(tt) != 1: bad += 1
                        else: ts.append(tt[0])
                if len(ts) != len(set(ts)): bad += 1
        # cylinder reconstruction
        sl = [set(tuple(v for i, v in enumerate(x) if i != c) for x in S if x[c] == 0) for c in range(d)]
        box = [max(x[a] for x in S) + 2 for a in range(d)]
        R = set()
        for x in itertools.product(*[range(b) for b in box]):
            if all(tuple(v for i, v in enumerate(x) if i != c) in sl[c] for c in range(d)) and not any(all(x[a] >= q[a] for a in range(d)) for q in full):
                R.add(x)
        if R != S: bad += 1; print('cylinder reconstruction FAILS', Dl)
    print(f'm={m}: tiles (D,p) {nT}, violations {bad}, max #full-support min non-elements per tile shape {maxfull}', flush=True)
