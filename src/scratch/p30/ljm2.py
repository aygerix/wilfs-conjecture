"""Two-phase local matching: fix the proved self-payments (types A, C), then match the residual carries (B, D) to the
remaining local items.  Reports failures and item-type usage of the residual matching."""
import sys, itertools, random, ljm
mode = sys.argv[1]
if mode == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    gen = ((random.randint(mlo, mhi), None) for _ in range(N))
n = bad = 0; ex = []; use = {}
for m, B in gen:
    if B is None: B = sorted(random.sample(range(1, m), k))
    out = ljm.build(m, B)
    if not out: continue
    info, adj = out; n += 1
    fixed = info["fixed"]; taken = set(fixed.values())
    res = {u: [v for v in vs if v not in taken] for u, vs in adj.items() if u not in fixed}
    mm = ljm.maxmatch(res)
    if mm < len(res):
        bad += 1
        if len(ex) < 6: ex.append((len(res) - mm, {x: info[x] for x in ("m", "B", "h", "W", "p", "q")}))
    else:
        match = {}
        def aug(u, seen):
            for v in res[u]:
                if v in seen: continue
                seen.add(v)
                if v not in match or aug(match[v], seen): match[v] = u; return True
            return False
        for u in res: aug(u, set())
        for v, u in match.items():
            key = (u[0], v[0]); use[key] = use.get(key, 0) + 1
print(sys.argv[1:], "S:", n, "two-phase failures:", bad, ex)
print("  residual usage (carry kind, item type):", sorted(use.items()))
