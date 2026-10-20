"""Degree statistics of the local carry/slack graph (ljm.build): min carry degree vs max item degree."""
import sys, itertools, random, ljm
mode = sys.argv[1]
if mode == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    gen = ((random.randint(mlo, mhi), None) for _ in range(N))
n = bad = 0; worst = None; fr = None
for m, B in gen:
    if B is None: B = sorted(random.sample(range(1, m), k))
    out = ljm.build(m, B)
    if not out: continue
    info, adj = out
    if not adj: continue
    n += 1
    cdeg = min(len(v) for v in adj.values())
    ideg = {}
    for u, vs in adj.items():
        for v in vs: ideg[v] = ideg.get(v, 0) + 1
    mi = max(ideg.values()) if ideg else 0
    # fractional uniform discharging: each carry sends 1/deg to each neighbour; max load
    load = {}
    for u, vs in adj.items():
        for v in vs: load[v] = load.get(v, 0) + 1.0 / len(vs)
    ml = max(load.values()) if load else 0
    if cdeg < mi: bad += 1
    if worst is None or cdeg / max(mi, 1) < worst[0]: worst = (cdeg / max(mi, 1), cdeg, mi, info)
    if fr is None or ml > fr[0]: fr = (ml, info)
print(sys.argv[1:], "S with carries:", n, "#(min carry deg < max item deg):", bad)
print("  worst deg ratio:", worst)
print("  max uniform-discharge load:", fr)
