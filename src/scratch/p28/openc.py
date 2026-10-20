r"""Open classes of Conjecture M vs degree-4 tokens from the small part (lead, 2026-10-20).
Open: low carried pairs {b<=b'} whose token (g_b, b', 3) is USED (alive); carried triples of class O (all sub-pairs >= h) and
class C (some sub-pair carried) -- i.e. triples with no sub-pair < h.  G4 = degree-4 tokens (u, x, 4), u in {0} u {g_b : b < h}.
Tests: N_open <= #unused G4 ; and Hall for open elements with edges to unused G4 tokens inside their representation.
usage: openc.py exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
from collections import defaultdict
from match4 import build
def test(m, B):
    D = build(m, B)
    if D is None: return None
    w, car, unused, e, g, rep, h = D["w"], D["car"], D["unused"], D["e"], D["g"], D["rep"], D["h"]
    k = len(B)
    small = [i for i in range(k) if B[i] < h]
    G4 = set((0, i, 4) for i in range(k)) | set((g[j], i, 4) for j in small for i in range(k))
    G4u = G4 & unused
    opn = []
    for v in w:
        if car[v] == 0: continue
        M = rep[v]
        if len(M) == 2:
            i, j = M
            if v % m >= h: continue
            if (g[i], j, 3) in unused: continue
            opn.append(v)
        else:
            b = sorted(B[i] for i in M)
            if b[0] + b[1] < h: continue
            opn.append(v)
    adj = {}
    for v in opn:
        M = rep[v]; ss = set([0]) | set(g[i] for i in M)
        adj[v] = [t for t in G4u if t[0] in ss]
    matchR = {}
    def aug(v, seen):
        for t in adj[v]:
            if t in seen: continue
            seen.add(t)
            if t not in matchR or aug(matchR[t], seen): matchR[t] = v; return True
        return False
    ms = sum(1 for v in opn if aug(v, set()))
    return dict(m=m, B=tuple(B), e=e, h=h, a=len(small), W=D["W"], Nopen=len(opn), G4u=len(G4u), hall_def=len(opn) - ms)
if __name__ == "__main__":
    recs = []
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = test(m, list(B))
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
            r = test(m, B)
            if r: recs.append(r)
    c1 = [r for r in recs if r["Nopen"] > r["G4u"]]; c2 = [r for r in recs if r["hall_def"] > 0]
    print(sys.argv[1:], "S", len(recs), "count fails", len(c1), "Hall fails", len(c2), "(h>e:", sum(1 for r in c2 if r["h"] > r["e"]), ")")
    for r in sorted(c2, key=lambda r: -r["hall_def"])[:4]: print("  ", r)
    if not c2 and recs:
        mr = min(recs, key=lambda r: r["G4u"] - r["Nopen"]); print("  min slack", mr["G4u"] - mr["Nopen"], mr)
