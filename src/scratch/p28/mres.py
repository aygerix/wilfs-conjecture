r"""Residual matching at P18 depth four after the canonical maps (lead, 2026-10-20).
pi(pair {b<=b'}) = (g_b, b', 3) if b' >= h else (g_b, b', 4)    [dead, injective: PROVED]
rho(triple with b1+b2 < h) = (u_12, b3, 4)                        [dead, injective: PROVED]
Residual: triples with b1 + b2 >= h (classes O, C) must be matched inside to the remaining unused tokens / spares.
Checks: pi, rho images are unused and distinct; Hall for the residual.  usage: mres.py exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
from collections import defaultdict
from match4 import build
def test(m, B):
    D = build(m, B)
    if D is None: return None
    w, car, unused, e, g, rep, h, order = D["w"], D["car"], D["unused"], D["e"], D["g"], D["rep"], D["h"], D["order"]
    taken = set(); resid = []; bad = 0
    for v in w:
        if car[v] == 0: continue
        M = rep[v]
        if len(M) == 2:
            i, j = sorted(M, key=lambda i: B[i])
            t = (g[i], j, 3) if B[j] >= h else (g[i], j, 4)
        else:
            Ms = sorted(M, key=lambda i: B[i])
            if B[Ms[0]] + B[Ms[1]] < h:
                t = (g[Ms[0]] + g[Ms[1]], Ms[2], 4)
            else:
                resid.append(v); continue
        if t not in unused or t in taken: bad += 1
        taken.add(t)
    by_u = defaultdict(list)
    for t in unused:
        if t not in taken: by_u[t[0]].append(t)
    spare = {v: len([t for t in unused if t[0] == v]) - (e - 1) * car[v] for v in w if car[v] > 0}
    adj = {}
    for v in resid:
        M = rep[v]; ss = set([0])
        for r in range(1, len(M)):
            for S in itertools.combinations(M, r): ss.add(sum(g[i] for i in S))
        lst = []
        for u in ss:
            if car.get(u, 0) == 0: lst.extend(by_u[u])
            elif spare.get(u, 0) > 0: lst.append(("spare", u))
        if spare[v] > 0: lst.append(("spare", v))
        adj[v] = lst
    cap = defaultdict(int)
    for v in resid:
        for t in adj[v]: cap[t] = spare[t[1]] if t[0] == "spare" else 1
    matchR = defaultdict(list)
    def aug(v, seen):
        for t in adj[v]:
            if t in seen: continue
            seen.add(t)
            if len(matchR[t]) < cap[t]: matchR[t].append(v); return True
            for v2 in list(matchR[t]):
                if aug(v2, seen): matchR[t].remove(v2); matchR[t].append(v); return True
        return False
    ms = sum(1 for v in resid if aug(v, set()))
    tally = defaultdict(int)
    for t, vs in matchR.items():
        for v in vs:
            if t[0] == "spare": tally["spare_own" if t[1] == v else "spare_sub"] += 1
            else:
                u = t[0]; o = order[u]
                tally[("0" if u == 0 else ("gen" if o == 1 else "pair")) + "_k%d" % t[2]] += 1
    return dict(m=m, B=tuple(B), e=e, h=h, W=D["W"], canon_bad=bad, resid=len(resid), deficit=len(resid) - ms, tally=dict(tally))
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
    print(sys.argv[1:], "S", len(recs), "canonical-map failures", sum(r["canon_bad"] > 0 for r in recs),
          "residual Hall failures", sum(r["deficit"] > 0 for r in recs), "max residual", max((r["resid"] for r in recs), default=0))
    for r in [r for r in recs if r["deficit"] > 0 or r["canon_bad"] > 0][:5]: print("  ", r)
    tot = defaultdict(int)
    for r in recs:
        for k_, v_ in r["tally"].items(): tot[k_] += v_
    print("  token types used by residual matching:", dict(sorted(tot.items())))
    for r in sorted(recs, key=lambda r: -r["resid"])[:3]: print("  big residual:", r)
