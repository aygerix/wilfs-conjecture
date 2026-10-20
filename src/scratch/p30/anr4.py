r"""Annealer against the overflow-token reductions of r4.py (regime 2h <= m, P18 depth four; lead, 2026-10-20).
OBJ in {Z1, Z7, Z8, Z3, W}; ratio objectives Z1r = (OVF + phi)/q, Z8r = (y0 + extra)/core.  Optional 'seedD d' plants a
B3-like block of d elements in (h/2, 2h/3) at start.  usage: anr4.py OBJ seed mlo mhi kmin kmax iters restarts"""
import sys, random, math, r4
obj = sys.argv[1]; seed, mlo, mhi, kmin, kmax, iters, restarts = map(int, sys.argv[2:9]); random.seed(seed)
def f(d):
    if obj == "Z1r": return (d["OVF"] + d["phi"]) / d["q"] if d["q"] else 1e6
    if obj == "Z8r": return (d["y0"] + d["extra"]) / d["core"] if d["core"] else 1e6
    return d[obj]
def ev(m, B):
    if len(set(B)) != len(B) or min(B) < 1 or max(B) >= m: return None, 1e9
    try: d = r4.ev(m, sorted(B))
    except AssertionError as ex: print("ASSERT", m, B, ex, flush=True); return None, 1e9
    if not d: return None, 1e9
    return d, f(d)
best = 1e9
for rs in range(restarts):
    m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); cur = None
    for _ in range(4000):
        B = random.sample(range(1, m), k); d, v = ev(m, B)
        if d: cur = (v, m, sorted(B), d); break
    if not cur: continue
    T0 = 0.3 if obj.endswith("r") else 2.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.01
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
            if v1 < best:
                best = v1; print("best", round(v1, 4), {x: d1[x] for x in ("W", "m", "B", "h", "q", "p", "phi", "OVF", "y0", "core", "extra", "big", "Z1", "Z7", "Z8")}, flush=True)
print("final best", best)
