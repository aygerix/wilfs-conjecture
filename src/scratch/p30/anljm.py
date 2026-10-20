r"""Annealer against the local matching conjecture LM at P18 depth four (lead, 2026-10-20).
Objective (minimised): (|N(all carries)| - #carries) / #carries in the local graph of ljm.build (a necessary Hall
condition), or 'W' ratio (W + p + q)/(p + q).  At each new best the exact matching is checked; failures are printed.
usage: anljm.py OBJ seed mlo mhi kmin kmax iters restarts     (OBJ in {hall, wr})"""
import sys, random, math, ljm
obj = sys.argv[1]; seed, mlo, mhi, kmin, kmax, iters, restarts = map(int, sys.argv[2:9]); random.seed(seed)
def ev(m, B):
    if len(set(B)) != len(B) or min(B) < 1 or max(B) >= m: return None, 1e9
    out = ljm.build(m, sorted(B))
    if not out: return None, 1e9
    info, adj = out
    nc = len(adj)
    if nc == 0: return None, 1e9
    if obj == "hall":
        Nb = set(v for vs in adj.values() for v in vs); v = (len(Nb) - nc) / nc
    else:
        v = (info["W"] + nc) / nc
    return (info, adj), v
best = 1e9
for rs in range(restarts):
    m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); cur = None
    for _ in range(3000):
        B = random.sample(range(1, m), k); r, v = ev(m, B)
        if r: cur = (v, m, sorted(B), r); break
    if not cur: continue
    for it in range(iters):
        T = 0.3 * (1 - it / iters) + 0.005
        v0, m0, B0, r0 = cur; m1, B1 = m0, list(B0); mv = random.random()
        if mv < 0.6: i = random.randrange(len(B1)); B1[i] = max(1, min(m1 - 1, B1[i] + random.choice([-3, -2, -1, 1, 2, 3])))
        elif mv < 0.75: i = random.randrange(len(B1)); B1[i] = random.randint(1, m1 - 1)
        elif mv < 0.85 and len(B1) < kmax: B1.append(random.randint(1, m1 - 1))
        elif mv < 0.92 and len(B1) > kmin: B1.pop(random.randrange(len(B1)))
        else: m1 = max(mlo, min(mhi, m0 + random.choice([-2, -1, 1, 2]))); B1 = [min(b, m1 - 1) for b in B1]
        r1, v1 = ev(m1, B1)
        if r1 is None: continue
        if v1 <= v0 or random.random() < math.exp(-(v1 - v0) / T):
            cur = (v1, m1, sorted(B1), r1)
            if v1 < best:
                best = v1; info, adj = r1; mm = ljm.maxmatch(adj)
                print("best", round(v1, 4), "match-deficit", len(adj) - mm, {x: info[x] for x in ("m", "B", "h", "W", "p", "q")}, flush=True)
print("final best", best)
