"""Show the residual (types B, D) carries of an instance, their reps, local items and a matching."""
import sys, ljm, itertools
def show(m, B):
    info, adj = ljm.build(m, B); fixed = info["fixed"]; taken = set(fixed.values())
    res = {u: [v for v in vs if v not in taken] for u, vs in adj.items() if u not in fixed}
    match = {}
    def aug(u, seen):
        for v in res[u]:
            if v in seen: continue
            seen.add(v)
            if v not in match or aug(match[v], seen): match[v] = u; return True
        return False
    for u in res: aug(u, set())
    inv = {u: v for v, u in match.items()}
    print({x: info[x] for x in ("m", "B", "h", "W", "p", "q")}, "fixed:", fixed)
    for u in sorted(res):
        print("   residual", u, "matched ->", inv.get(u), " | #local free items", len(res[u]), sorted(res[u])[:14])
for a in sys.argv[1:]:
    v = list(map(int, a.split(","))); show(v[0], v[1:])
