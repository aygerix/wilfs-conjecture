r"""Planted annealer against Z1 (r4.py; regime 2h <= m): B = D u BL with a fixed planted block D (e.g. a B3-Sidon set in
(h/2, 2h/3)); only BL and m move (lead, 2026-10-20).  usage: anr4p.py OBJ seed mlo mhi kL_min kL_max iters restarts d1,d2,..."""
import sys, random, math, heapq, r4
def pen(m, B):
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return 1e8
    c = max(w) - m + 1; h = c - 3 * m
    return 1000 + 30 * abs(c / m - 3.5) + max(0, 2 * h - m)
obj = sys.argv[1]; seed, mlo, mhi, kmin, kmax, iters, restarts = map(int, sys.argv[2:9]); random.seed(seed)
D = list(map(int, sys.argv[9].split(",")))
def ev(m, BL):
    B = sorted(set(D) | set(BL))
    if len(B) != len(D) + len(BL) or min(B) < 1 or max(B) >= m: return None, 1e9
    try: d = r4.ev(m, B)
    except AssertionError as ex: print("ASSERT", m, B, ex, flush=True); return None, 1e9
    if not d: return {"pen": True, "m": m}, pen(m, B)
    return d, d[obj] + (0 if d["core"] else 5)
best = 1e9; lo = max(D) + 1
for rs in range(restarts):
    m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); cur = None
    for _ in range(20000):
        BL = random.sample(range(1, m), k); d, v = ev(m, BL)
        if d: cur = (v, m, sorted(BL), d); break
    if not cur: print("no start", m, k, flush=True); continue
    for it in range(iters):
        T = 2.0 * (1 - it / iters) + 0.01
        v0, m0, B0, d0 = cur; m1, B1 = m0, list(B0); mv = random.random()
        if mv < 0.6: i = random.randrange(len(B1)); B1[i] = max(1, min(m1 - 1, B1[i] + random.choice([-3, -2, -1, 1, 2, 3])))
        elif mv < 0.75: i = random.randrange(len(B1)); B1[i] = random.randint(1, m1 - 1)
        elif mv < 0.85 and len(B1) < kmax: B1.append(random.randint(1, m1 - 1))
        elif mv < 0.92 and len(B1) > kmin: B1.pop(random.randrange(len(B1)))
        else: m1 = max(mlo, min(mhi, m0 + random.choice([-2, -1, 1, 2]))); B1 = [min(b, m1 - 1) for b in B1]
        d1, v1 = ev(m1, B1)
        if d1 is None: continue
        if v1 <= v0 or random.random() < math.exp(-(v1 - v0) / T):
            cur = (v1, m1, sorted(B1), d1)
            if v1 < best and "pen" not in d1:
                best = v1; print("best", v1, {x: d1[x] for x in ("W", "m", "B", "h", "q", "p", "phi", "OVF", "y0", "core", "extra", "big", "Z1", "Z7", "Z8", "Z3")}, flush=True)
print("final best", best)
