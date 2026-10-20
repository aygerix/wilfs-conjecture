"""SIG* and the Q3 component ablation on Eliahou-Fromentin semigroups S = <{m} u A>_{4m} (Semigroup Forum 98 (2019)),
A subset [(3m+1)/2, (5m-1)/3] a B_3-set mod m (lead, 2026-10-20).  General-S components as in qabl.c.
usage: efam.py mlo mhi nmax seed"""
import sys, random, itertools
def mingens(Sset, c):
    inS = lambda x: x >= c or x in Sset
    gens = []
    for x in range(1, c + max(Sset) + 2):
        if not inS(x): continue
        if not any(inS(x - g) and x - g > 0 for g in gens): gens.append(x)
        if len(gens) and x > c + gens[0]: break
    return gens
def comps(gens):
    m = gens[0]; e = len(gens); c_lim = 8 * m
    S = set([0]); 
    for x in range(1, c_lim):
        if any(x - g >= 0 and (x - g) in S for g in gens): S.add(x)
    c = max(x for x in range(c_lim) if x not in S) + 1
    if not (3 * m < c <= 4 * m): return None
    lev = [min(j for j in range(10) if j * m + r in S) for r in range(m)]
    G1 = [g - m for g in gens if m < g < 2 * m]; G2 = [g - 2 * m for g in gens if 2 * m < g < 3 * m]
    k1, k2 = len(G1), len(G2); k3 = sum(1 for g in gens if 3 * m < g < 4 * m); k4p = sum(1 for g in gens if g > 4 * m)
    isgen = set(gens)
    U2 = [r for r in range(m) if lev[r] == 2 and 2 * m + r not in isgen]; u2 = len(U2)
    Pu = Pw = 0; R = set()
    for i in range(k1):
        for j in range(i, k1):
            s = G1[i] + G1[j]
            if s < m: Pu += 1
            else: Pw += 1; R.add(s - m)
    TG = set(x + y for x in G1 for y in G2 if x + y < m)
    S2 = set(r for r in range(m) if lev[r] <= 2)
    TU = set(x + u for x in G1 for u in U2 if x + u < m and x + u not in S2 and x + u not in TG)
    aG = sum(1 for r in range(m) if lev[r] == 3 and 3 * m + r not in isgen and r in TG)
    aR = sum(1 for r in range(m) if lev[r] == 3 and 3 * m + r not in isgen and r not in TG and r not in TU)
    s012 = 3 + 2 * k1 + k2 + u2
    C = dict(sigT=k1 * u2 + 2 * Pu - 3 * len(TU), Pwp3=3 * (Pw - aR), Puu2=2 * (Pu - u2), Pw=Pw,
             Gam23=(1 + k1) * k2 + (k2 + k3) * s012 - 3 * k2 - 3 * k3 - 3 * aG, Gam4=k4p * s012)
    s3 = sum(1 for r in range(m) if lev[r] <= 3); Q3 = e * sum(3 - l for l in lev if l <= 2) - 3 * s3
    assert Q3 == sum(C.values()), (gens, Q3, C)
    h = c - 3 * m; L3 = sum(1 for r in range(h) if lev[r] <= 3); d4 = h - L3; Q4 = (e - 1) * L3 - 4 * d4
    g = sum(lev); W = e * (c - g) - c; assert W == Q3 + Q4
    return dict(m=m, e=e, c=c, h=h, W=W, Q3=Q3, Q4=Q4, SIGs=Q4 + C["sigT"] + C["Gam23"] + C["Gam4"], **C)
def b3mod(m, lo, hi, n, rng):
    cand = list(range(lo, hi + 1)); rng.shuffle(cand); A = []
    sums = set()
    for a in cand:
        new = [ (a + x + y) % m for i, x in enumerate(A + [a]) for y in (A + [a])[i:] ]
        ns = set((a + s) % m for s in [x + y for i, x in enumerate(A + [a]) for y in (A + [a])[i:]])
        trip = set()
        A2 = A + [a]
        for i in range(len(A2)):
            for j in range(i, len(A2)):
                for l in range(j, len(A2)): trip.add((A2[i] + A2[j] + A2[l]) % m)
        if len(trip) == len(A2) * (len(A2) + 1) * (len(A2) + 2) // 6: A = A2
        if len(A) == n: break
    return sorted(A)
if __name__ == "__main__":
    mlo, mhi, nmax, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
    worst = {}
    for m in range(mlo, mhi + 1):
        lo, hi = (3 * m + 2) // 2, (5 * m - 1) // 3
        for trial in range(3):
            A = b3mod(m, lo, hi, nmax, rng)
            if len(A) < 3: continue
            S0 = set([0]); lim = 4 * m
            for x in range(1, lim):
                if any(x - g >= 0 and (x - g) in S0 for g in [m] + A): S0.add(x)
            gens = mingens(S0, 4 * m)
            d = comps(gens)
            if not d: continue
            d["A"] = tuple(A)
            for key in ("W", "SIGs"):
                if key not in worst or d[key] < worst[key][key]: worst[key] = d
            drops = {"sigT": d["W"] - d["sigT"], "Gam4": d["W"] - d["Gam4"], "pairs": d["W"] - d["Pwp3"] - d["Puu2"] - d["Pw"]}
            for k2, v in drops.items():
                kk = "drop_" + k2
                if kk not in worst or v < worst[kk][0]: worst[kk] = (v, d)
    for key, v in worst.items(): print(key, v if key in ("W", "SIGs") else (v[0], {x: v[1][x] for x in ("m", "A", "e", "W", "Q3", "Q4", "sigT", "Gam4", "Gam23", "Pw", "Pwp3", "Puu2")}))
