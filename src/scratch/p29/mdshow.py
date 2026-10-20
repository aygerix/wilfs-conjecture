r"""Show a TMD matching (lead, 2026-10-20): for each Delta unit (v, k), the slot (u, b, k') it gets, preferring
(in order) larger u (closest sub-sum), then larger k'.  usage: mdshow.py gens..."""
import sys
sys.path.insert(0, ".")
from twin import build, subsums
sys.setrecursionlimit(100000)
gens = list(map(int, sys.argv[1:])); D = build(gens)
m, w, aps, gen, e, order, car, rep, q, h, W = (D[k] for k in "m w aps gen e order car rep q h W".split())
top = lambda u: q if u % m < h else q - 1
lam = {(u, b): next(j for j in range(m + 1) if (u + (j + 1) * g) not in aps) for u in w for b, g in enumerate(gen)}
L = {u: top(u) - u // m for u in w}
slots_of = {u: [(u, b, order[u] + j) for b in range(e - 1) for j in range(lam[u, b] + 1, L[u] + 1)] for u in w}
units = [(v, k) for v in sorted(w) if car[v] > 0 for k in range(top(v) - car[v] + 1, top(v) + 1)]
fixed = {}; rest = []
for (v, k) in units:
    tw = None
    for b in sorted(rep[v]):
        tk = (v - gen[b], b, k)
        if tk in set(slots_of[v - gen[b]]) and tk not in fixed.values(): tw = tk; break
    if tw: fixed[(v, k)] = tw
    else: rest.append((v, k))
used = set(fixed.values())
adj = []
for (v, k) in rest:
    cand = [s for u in subsums(rep[v], gen) for s in slots_of[u] if s[2] <= k and s not in used]
    cand.sort(key=lambda s: (-s[0], -s[2]))
    adj.append(cand)
mt = {}
def aug(x, seen):
    for y in adj[x]:
        if y in seen: continue
        seen.add(y)
        if y not in mt or aug(mt[y], seen): mt[y] = x; return True
    return False
ok = sum(1 for x in range(len(rest)) if aug(x, set()))
inv = {x: y for y, x in mt.items()}
fac = lambda u: "+".join(str(gen[b]) + ("^%d" % a if a > 1 else "") for b, a in sorted(rep[u].items())) or "0"
print("m", m, "gens", gen, "q", q, "h", h, "W", W, "units", len(units), "twins", len(fixed), "Delta", len(rest), "matched", ok)
for x, (v, k) in enumerate(rest):
    s = inv.get(x)
    print("  unit (%s, k=%d) t=%d  ->  slot u=%s dir=%d k'=%d  (v-u = %s)" % (fac(v), k, car[v], fac(s[0]) if s else None, gen[s[1]] if s else -1, s[2] if s else -1, (v - s[0]) if s else None))
