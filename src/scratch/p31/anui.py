r"""Diagnostic annealer (lead, 2026-10-20): is the wrapped part WI of sigT ever needed at P18 depth four?
Minimises Q4 + UI (sigsplit.py), with UI = sigT - WI.  usage: anui.py seed mlo mhi kmin kmax iters restarts"""
import sys, random, math, sigsplit
seed, mlo, mhi, kmin, kmax, iters, restarts = map(int, sys.argv[1:8]); random.seed(seed)
def ev(m, B):
    if len(set(B)) != len(B) or min(B) < 1 or max(B) >= m: return None, 1e9
    d = sigsplit.ev(m, sorted(B))
    if not d: return None, 1e9
    return d, d["Q4"] + d["UI"]
best = 1e9
for rs in range(restarts):
    m = random.randint(mlo, mhi); k = random.randint(kmin, kmax); cur = None
    for _ in range(4000):
        B = random.sample(range(1, m), k); d, v = ev(m, B)
        if d: cur = (v, m, sorted(B), d); break
    if not cur: continue
    for it in range(iters):
        T = 3.0 * (1 - it / iters) + 0.01
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
                best = v1; print("best", v1, {y: d1[y] for y in ("m", "B", "h", "W", "Q4", "sigT", "WI", "UI", "L3", "d4")}, flush=True)
print("final best", best)
