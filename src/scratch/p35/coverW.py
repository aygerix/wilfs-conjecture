r"""Wilf numbers of semigroups built on near-perfect sum covers (lead, 2026-10-20).
For a cover {0} u delta of Z/m and lifts k_a, S = <m, k_a m + delta_a>.  Exact W by membership DP (independent of tile
code).  Modes: 'eq' (all lifts k in KLIST), 'rnd' (NR random lift vectors in {KLO..KHI}).  Reports min W found,
the S attaining it, c/m, e, and how many S had W < 0 (each such S is re-verified and printed in full).
Usage: python coverW.py m a0,a1,...(cover incl. 0) MODE ARGS   eq: KLIST (e.g. 2,3,4)   rnd: KLO KHI NR SEED AFF(0/1)"""
import sys, math, random
m = int(sys.argv[1]); A = [int(t) for t in sys.argv[2].split(',')]; mode = sys.argv[3]
def W_of(G):
    G = sorted(set(G)); B = 2 * max(G) * 4 + 10 * m
    while True:
        inS = bytearray(B + 1); inS[0] = 1
        for n in range(1, B + 1):
            for g in G:
                if n >= g and inS[n - g]: inS[n] = 1; break
        F = max((n for n in range(B + 1) if not inS[n]), default=-1)
        if F < B - G[-1] - 1: break
        B *= 2
    c = F + 1; g = sum(1 for n in range(c) if not inS[n])
    mins = [s for s in range(1, c + G[-1] + 1) if inS[s] and not any(inS[a] and inS[s - a] for a in range(1, s // 2 + 1))]
    e = len(mins); return e * (c - g) - c, c, e, mins
def affines(A):
    out = set()
    for u in range(1, m):
        if math.gcd(u, m) != 1: continue
        for a in A: out.add(tuple(sorted({(u * (x - a)) % m for x in A} - {0})))
    return sorted(out)
best = None; neg = []
if mode == 'eq':
    KL = [int(t) for t in sys.argv[4].split(',')]
    for dl in affines(A):
        for k in KL:
            W, c, e, mins = W_of([m] + [k * m + x for x in dl])
            if best is None or W < best[0]: best = (W, c, e, mins)
            if W < 0: neg.append(mins)
else:
    KLO, KHI, NR, SEED, AFF = map(int, sys.argv[4:9]); rnd = random.Random(SEED)
    pool = affines(A) if AFF else [tuple(sorted(set(A) - {0}))]
    for _ in range(NR):
        dl = rnd.choice(pool); G = [m] + [rnd.randint(KLO, KHI) * m + x for x in dl]
        W, c, e, mins = W_of(G)
        if best is None or W < best[0]: best = (W, c, e, mins)
        if W < 0: neg.append(mins)
W, c, e, mins = best
print("m=%d mode=%s minW=%d (c=%d, c/m=%.2f, e=%d, 3e<m=%s) S=%s  #W<0: %d %s" % (m, mode, W, c, c / m, e, 3 * e < m, mins, len(neg), neg[:3]), flush=True)
