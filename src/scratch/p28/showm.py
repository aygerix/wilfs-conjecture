r"""Show carried elements of a P18 depth-four S with their classes and a saturating inside matching (lead, 2026-10-20).
usage: showm.py m b1 b2 ..."""
import sys, itertools
from collections import defaultdict
from match4 import build
m = int(sys.argv[1]); B = list(map(int, sys.argv[2:]))
D = build(m, B); w, car, unused, e, g, rep, order, h = D["w"], D["car"], D["unused"], D["e"], D["g"], D["rep"], D["order"], D["h"]
print("m", m, "B", B, "e", e, "h", h, "W", D["W"])
by_u = defaultdict(list)
for t in unused: by_u[t[0]].append(t)
name = lambda u: "0" if u == 0 else "{" + ",".join(str(B[i]) for i in rep[u]) + "}"
for v in sorted(w, key=lambda v: (order[v], v)):
    if car[v] == 0: continue
    M = rep[v]; Ms = [B[i] for i in M]
    ss = set([0])
    for r in range(1, len(M)):
        for S in itertools.combinations(M, r): ss.add(sum(g[i] for i in S))
    toks = []
    for u in sorted(ss):
        for t in sorted(by_u[u], key=lambda t: (t[2], t[1])):
            toks.append("%s%s(%s,%d,k%d)" % ("" if car[u] == 0 else "*", "", name(u), B[t[1]], t[2]))
    cls = "pair" if len(M) == 2 else ("Y" if min(Ms[0] + Ms[1], Ms[0] + Ms[2], Ms[1] + Ms[2]) < h else ("C" if Ms[1] + Ms[2] >= m else "O"))
    print(" ", "residue", v % m, "level", v // m, "ord", order[v], "rep", Ms, "class", cls, "| inside unused:", " ".join(toks[:14]), "..." if len(toks) > 14 else "")
