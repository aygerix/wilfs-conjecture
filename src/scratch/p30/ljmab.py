"""Ablation of the local matching (ljm.build): drop item types and count instances where matching fails."""
import sys, itertools, random, ljm
mode = sys.argv[1]
if mode == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    gen = ((random.randint(mlo, mhi), None) for _ in range(N))
abl = {"all": set(), "-I": {"I"}, "-D": {"D"}, "-T": {"T"}, "-R": {"R"}, "-I-R": {"I", "R"}, "-D-R": {"D", "R"}, "T only": {"I", "D", "R"}}
fails = {a: 0 for a in abl}; ex = {a: None for a in abl}; n = 0
for m, B in gen:
    if B is None: B = sorted(random.sample(range(1, m), k))
    out = ljm.build(m, B)
    if not out: continue
    info, adj = out; n += 1
    for a, drop in abl.items():
        adj2 = {u: [v for v in vs if v[0] not in drop] for u, vs in adj.items()}
        if ljm.maxmatch(adj2) < len(adj2):
            fails[a] += 1
            if ex[a] is None: ex[a] = info
print(sys.argv[1:], "S:", n)
for a in abl: print("  ", a, "failures", fails[a], ex[a] if ex[a] else "")
