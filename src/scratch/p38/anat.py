# anat: anatomy of the missing level-2/3 monomials of the Q5 U-tile D, for D6 (Delta3 >= 6|NE|).
# Delta3 = 4*M2 + B2, B2 = sum over missing level-3 v of w(v) = sum_{i: v-e_i in D} v_i.
# For each missing monomial: its class, the tile rep it loses to, and the relation type.
import sys
from itertools import combinations_with_replacement as cwr
def anat(gens, verbose=True):
    m = gens[0]; A = [g - m for g in gens[1:]]; d = len(A); e = d + 1
    N = 8 * m; inS = [False] * N; inS[0] = True
    for x in range(1, N): inS[x] = any(x >= g and inS[x - g] for g in gens)
    w = [min(x for x in range(s, N, m) if inS[x]) for s in range(m)]
    mons = {k: [tuple(sum(1 for i in c if i == q) for q in range(d)) for c in cwr(range(d), k)] for k in range(4)}
    sig = lambda v: sum(v[i] * A[i] for i in range(d))
    X = {}
    for s in range(m):
        best = None
        for k in range(4):
            for v in mons[k]:
                if k * m + sig(v) == w[s] and (best is None or (k, v) > best): best = (k, v)
        assert best is not None
        X[s] = best[1]
    inT = [False] * N; inT[0] = True
    for x in range(1, N): inT[x] = any(x >= g and inT[x - g] for g in A + [m])
    tau = [min(x for x in range(s, N, m) if inT[x]) for s in range(m)]
    D = set(X.values()); cls = {X[s]: s for s in range(m)}
    typ = {}
    for s in range(m):
        h = sum(X[s]); sg = w[s] - h * m
        typ[s] = 'EQ' if sg == tau[s] else ('NE2' if h == 2 else 'NE3')
    h = sum(1 for s in range(m) if typ[s] != 'EQ')
    D3 = 3 * (e - 1) * m - e * sum(sum(X[s]) for s in range(m))
    miss2 = [v for v in mons[2] if v not in D]; miss3 = [v for v in mons[3] if v not in D]
    wt = lambda v: sum(v[i] for i in range(d) if v[i] and tuple(v[q] - (q == i) for q in range(d)) in D)
    B2 = sum(wt(v) for v in miss3)
    assert D3 == 4 * len(miss2) + B2, (D3, len(miss2), B2)
    def lbl(v):
        return '+'.join(str(A[i]) for i in range(d) for _ in range(v[i]))
    out = []
    if verbose:
        print(f"S={gens} m={m} A={A} e={e} D3={D3} h={h} D3-6h={D3-6*h} M2={len(miss2)} B2={B2}")
        for s in sorted(range(m), key=lambda s: (sum(X[s]), w[s])):
            if typ[s] != 'EQ': print(f"  {typ[s]} class {s} x={lbl(X[s])} sigma={w[s]-sum(X[s])*m} tau={tau[s]}")
        for v in miss2 + miss3:
            k = sum(v); sv = sig(v); s = sv % m; x = X[s]; sx = w[s] - sum(x) * m
            rel = f"{lbl(v)}={sv} -> class {s} rep {lbl(x)}={sx} ({typ[s]}, |rep|={sum(x)}) diff={(sv-sx)//m}m"
            print(f"  miss{k} w={wt(v) if k==3 else 4} {rel}")
    return D3, h
for arg in sys.argv[1:]:
    anat([int(t) for t in arg.split(',')])
