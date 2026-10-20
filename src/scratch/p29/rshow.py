r"""P18 depth four (lead, 2026-10-20): after pi (pairs) and rho (triples with a sub-pair < h), match the residual R
into slots (dead, non-forced tokens) inside each element's box, degree <= 4; print the token types used.
usage: rshow.py m b1 b2 ...   (S = <m, m+B>)"""
import sys
sys.path.insert(0, ".")
from twin import build, subsums
sys.setrecursionlimit(100000)
m = int(sys.argv[1]); B = list(map(int, sys.argv[2:])); D = build([m] + [m + b for b in B])
w, aps, gen, e, order, car, rep, q, h, W = (D[k] for k in "w aps gen e order car rep q h W".split())
assert q == 4, q
top = lambda u: q if u % m < h else q - 1
lam = {(u, b): next(j for j in range(m + 1) if (u + (j + 1) * g) not in aps) for u in w for b, g in enumerate(gen)}
L = {u: top(u) - u // m for u in w}
slots_of = {u: [(u, b, order[u] + j) for b in range(e - 1) for j in range(lam[u, b] + 1, L[u] + 1)] for u in w}
allslots = set(s for u in w for s in slots_of[u])
bb = lambda i: gen[i] - m
fixed = set(); R = []
for v in w:
    if car[v] == 0: continue
    idx = sorted((i for i, a in rep[v].items() for _ in range(a)), key=bb)
    if len(idx) == 2:
        b, b2 = idx; tk = (gen[b], b2, 3) if bb(b2) >= h else (gen[b], b2, 4)
        assert tk in allslots and tk not in fixed; fixed.add(tk)
    else:
        if bb(idx[0]) + bb(idx[1]) < h:
            tk = (v - gen[idx[2]], idx[2], 4); assert tk in allslots and tk not in fixed; fixed.add(tk)
        else: R.append(v)
adj = [[s for u in subsums(rep[v], gen) for s in slots_of[u] if s not in fixed] for v in R]
mt = {}
def aug(x, seen):
    for y in adj[x]:
        if y in seen: continue
        seen.add(y)
        if y not in mt or aug(mt[y], seen): mt[y] = x; return True
    return False
for x in range(len(R)): aug(x, set())
inv = {x: y for y, x in mt.items()}
print("m", m, "B", B, "h", h, "e", e, "W", W, "|R|", len(R), "matched", len(inv), "free slots", len(allslots) - len(fixed))
for x, v in enumerate(R):
    s = inv.get(x); bs = sorted(bb(i) for i, a in rep[v].items() for _ in range(a))
    if s: print("  R elt b=%s r=%d -> slot first=%s (level %d, r %d) dir %d deg %d" % (bs, v % m, s[0], s[0] // m, s[0] % m, bb(s[1]), s[2]))
    else: print("  R elt b=%s UNMATCHED" % bs)
