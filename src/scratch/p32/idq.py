"""ID-q: a depth-free incidence identity for P18 window models (lead, 2026-10-20).
Model (m, rho, B), B subset of [1, m): T = <m, m+b : b in B> u [q m - rho, inf). Shifted position of element v:
u = (v + rho) mod m, level floor((v + rho)/m). Canonical rep of position u: the representation (as a multiset of
offsets) minimizing (level, degree, code), code = sum alpha_i * BASE^i (i = index of offset in increasing order).
Canonical reps are divisor-closed, so Dijkstra over positions computes them.
For a position x (level lam_x <= q, degree t_x, wraps j_x = lam_x - t_x):
  out-weight K + t_x = sum_i (alpha_x(i) + 1); incidence (x, i) is USED iff the child y = x + b_i (mod m) has
  lam_y <= q and alpha_y = alpha_x + e_i. u(x) = total weight of unused incidences.
  c_y = crossing in-weight = sum over i in supp(alpha_y) with b_i > y of alpha_y(i).
CLAIM: W0 := (K+1) ell - q d + rho = rho + sum_x (q - lam_x) u(x) + sum_y (c_y - j_y).
Also prints the deficit DEF = sum_y max(0, j_y - c_y) by (j, c) class and the pool.
Usage: python idq.py NRAND SEED [strip]   (strip: allow offsets b >= m - rho)"""
import heapq, random, sys
from collections import Counter

def canon(m, rho, B, q, BASE):
    K = len(B)
    best = {}  # u -> (lam, t, code, alpha tuple)
    start = (0, 0, 0, tuple([0] * K))
    best[rho % m] = start
    heap = [(0, 0, 0, rho % m)]
    done = set()
    while heap:
        lam, t, code, u = heapq.heappop(heap)
        if u in done: continue
        cur = best[u]
        if (lam, t, code) != cur[:3]: continue
        done.add(u)
        if lam > q + 1: continue
        alpha = cur[3]
        for i, b in enumerate(B):
            v = u + b
            cross = 1 if v >= m else 0
            u2 = v % m
            key = (lam + 1 + cross, t + 1, code + BASE ** i)
            if u2 in done: continue
            if u2 not in best or key < best[u2][:3]:
                a2 = list(alpha); a2[i] += 1
                best[u2] = key + (tuple(a2),)
                heapq.heappush(heap, (key[0], key[1], key[2], u2))
    return best

def check(m, rho, B, q):
    K = len(B)
    BASE = q + 3
    best = canon(m, rho, B, q, BASE)
    lam = {u: best[u][0] for u in best}
    ell = sum(q - l for l in lam.values() if l < q)
    d = sum(1 for l in lam.values() if l <= q)
    W0 = (K + 1) * ell - q * d + rho
    pool = 0; cj = 0; defi = Counter(); posj = Counter()
    for x, (lx, tx, cx, ax) in best.items():
        if lx > q: continue
        jx = lx - tx
        # out incidences
        for i, b in enumerate(B):
            w = ax[i] + 1
            y = (x + b) % m
            used = False
            if y in best and best[y][0] <= q:
                ay = list(ax); ay[i] += 1
                if tuple(ay) == best[y][3] and best[y][0] == lx + 1 + (1 if x + b >= m else 0):
                    used = True
            if not used: pool += (q - lx) * w
        cy = sum(ax[i] for i, b in enumerate(B) if ax[i] > 0 and b > x)
        cj += cy - jx
        if cy < jx: defi[(jx, cy)] += jx - cy
        elif jx > 0: posj[(jx, cy)] += cy - jx
    rhs = rho + pool + cj
    return W0, rhs, pool, defi, posj

if __name__ == "__main__":
    NR, SEED = int(sys.argv[1]), int(sys.argv[2]); strip = len(sys.argv) > 3
    rnd = random.Random(SEED)
    bad = 0; agg = Counter(); n = 0
    for it in range(NR):
        q = rnd.randint(3, 7)
        m = rnd.randint(8, 60)
        rho = rnd.randint(0, m - 2)
        hi = m if strip else m - rho
        if hi - 1 < 1: continue
        K = rnd.randint(1, min(8, hi - 1))
        B = sorted(rnd.sample(range(1, hi), K))
        W0, rhs, pool, defi, posj = check(m, rho, B, q)
        n += 1
        if W0 != rhs:
            bad += 1
            if bad <= 5: print("MISMATCH", m, rho, B, q, W0, rhs)
        for k, v in defi.items(): agg[(q,) + k] += 1
    print("checked", n, "mismatches", bad)
    print("deficit classes (q, j, c): #models containing", dict(sorted(agg.items())))
