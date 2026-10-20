r"""Annealer for the carry-identity conjectures at P18 depth four (lead, 2026-10-20).
Objectives (minimised over depth-four S = <m, m+B>):
  K7  = defU + slB - p - q            (carries <= unused repeat entries + unused degree-4 tokens)
  L1  = incU + incC - qres            (unused incidences pay carried triples with all pair sums >= h)
  L2  = incU + incC + 2 d2el - qres - pres
  W   (sanity)
Mode suffix "/k" divides by k.  Restricting to h > e when 'hgt' is given.
usage: anjid.py OBJ seed mlo mhi kmin kmax iters restarts [hgt]"""
import sys, random, math, jid
obj, seed, mlo, mhi, kmin, kmax, iters, restarts = sys.argv[1], *map(int, sys.argv[2:9])
hgt = len(sys.argv) > 9 and sys.argv[9] == "hgt"
random.seed(seed)
def f(r):
    base = obj.split("/")[0]
    if base == "K7": v = r["defU"] + r["slB"] - r["p"] - r["q"]
    elif base == "L1": v = r["incU"] + r["incC"] - r["qres"]
    elif base == "L2": v = r["incU"] + r["incC"] + 2 * r["d2el"] - r["qres"] - r["pres"]
    elif base == "K7r": v = (r["defU"] + r["slB"]) / (r["p"] + r["q"]) if r["p"] + r["q"] else 1e6
    elif base == "L1r": v = (r["incU"] + r["incC"]) / r["qres"] if r["qres"] else 1e6
    elif base == "L2r": v = (r["incU"] + r["incC"] + 2 * r["d2el"]) / (r["qres"] + r["pres"]) if r["qres"] + r["pres"] else 1e6
    elif base == "Wr": v = (r["W"] + r["p"] + r["q"]) / (r["p"] + r["q"]) if r["p"] + r["q"] else 1e6
    else: v = r["W"]
    if obj.endswith("/k"): v = v / len(r["B"])
    return v
def ev(m, B):
    if len(set(B)) != len(B) or min(B) < 1 or max(B) >= m: return None, 1e9
    r = jid.info(m, sorted(B))
    if r is None or (hgt and r["h"] <= r["e"]): return None, 1e9
    return r, f(r)
best = (1e9, None)
base_ratio = obj.split("/")[0].endswith("r")
for rs in range(restarts):
    m = random.randint(mlo, mhi); k = random.randint(kmin, kmax)
    cur = None
    for _ in range(2000):
        B = random.sample(range(1, m), k); r, v = ev(m, B)
        if r: cur = (v, m, B, r); break
    if not cur: continue
    T0 = 0.3 if base_ratio else 2.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.01
        v0, m0, B0, r0 = cur; m1, B1 = m0, list(B0)
        mv = random.random()
        if mv < 0.6: i = random.randrange(len(B1)); B1[i] = max(1, min(m1 - 1, B1[i] + random.choice([-3, -2, -1, 1, 2, 3])))
        elif mv < 0.75: i = random.randrange(len(B1)); B1[i] = random.randint(1, m1 - 1)
        elif mv < 0.85 and len(B1) < kmax: B1.append(random.randint(1, m1 - 1))
        elif mv < 0.92 and len(B1) > kmin: B1.pop(random.randrange(len(B1)))
        else:
            m1 = max(mlo, min(mhi, m0 + random.choice([-2, -1, 1, 2]))); B1 = [min(b, m1 - 1) for b in B1]
        r1, v1 = ev(m1, B1)
        if r1 is None: continue
        if v1 <= v0 or random.random() < math.exp(-(v1 - v0) / T):
            cur = (v1, m1, sorted(B1), r1)
            if v1 < best[0]:
                best = (v1, r1)
                print("best", round(v1, 3), r1, flush=True)
print("final", best)
