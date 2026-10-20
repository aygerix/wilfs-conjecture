"""Per-column test at P18 depth four: for every z in B, #carries with canonical max z <= #unused items in column z.
Column z items: unused tokens (u, z) (u uncarried in X), unused entries (z, a) and (a, z) [variants], unused incidences
(s, z).  Canonical max: a carried triple uses the rep with the largest maximum; a carried pair the rep with largest max."""
import sys, itertools, random, ljm
mode = sys.argv[1]
if mode == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    gen = ((random.randint(mlo, mhi), None) for _ in range(N))
variants = ["T+Dz.+I.z", "T+D.z+I.z", "T+Dboth+I.z", "T+Dz.", "T+I.z", "T only"]
fails = {v: 0 for v in variants}; ex = {v: None for v in variants}; n = 0
for m, B in gen:
    if B is None: B = sorted(random.sample(range(1, m), k))
    out = ljm.build(m, B)
    if not out: continue
    info, adj = out; n += 1
    items = set(v for vs in adj.values() for v in vs)
    # full unused item list is not stored; rebuild from adj union plus all-free items is hard -> use ljm internals:
    # recompute via a light call: ljm.build stores nothing else, so approximate column items by items adjacent to some carry
    Bs = sorted(B); h = info["h"]
    # carries with canonical max
    cmax = {}
    for (kind, val) in adj:
        best = None
        if kind == "c":
            for (x, y, z) in ljm_ts[(m, tuple(Bs))][val + m] if False else []: pass
    # recompute reps directly
    ps = {}; ts = {}
    for i in range(len(Bs)):
        for j in range(i, len(Bs)): ps.setdefault(Bs[i] + Bs[j], []).append((Bs[i], Bs[j]))
    for i in range(len(Bs)):
        for j in range(i, len(Bs)):
            for l in range(j, len(Bs)): ts.setdefault(Bs[i] + Bs[j] + Bs[l], []).append((Bs[i], Bs[j], Bs[l]))
    for (kind, val) in adj:
        if kind == "c": z = max(r[2] for r in ts[val + m])
        else: z = max(r[1] for r in ps[val + m])
        cmax[z] = cmax.get(z, 0) + 1
    for var in variants:
        col = {}
        for it in items:
            t = it[0]; zs = []
            if t == "T": zs = [it[2]]
            elif t == "I" and "I.z" in var: zs = [it[2]]
            elif t == "D" and ("Dz." in var or "Dboth" in var) and it[1] != it[2]: zs.append(it[1])
            if t == "D" and ("D.z" in var or "Dboth" in var) and it[1] != it[2]: zs.append(it[2])
            if t == "D" and ("Dz." in var or "D.z" in var or "Dboth" in var) and it[1] == it[2]: zs = [it[1]]
            for z in set(zs): col[z] = col.get(z, 0) + 1
        if any(cmax[z] > col.get(z, 0) for z in cmax):
            fails[var] += 1
            if ex[var] is None: ex[var] = ({z: (cmax[z], col.get(z, 0)) for z in cmax}, {x: info[x] for x in ("m", "B", "h", "W", "p", "q")})
print(sys.argv[1:], "S:", n)
for v in variants: print("  ", v, "failures", fails[v], ex[v] if ex[v] else "")
