# Adversarial search for the split W = Lev + Car: minimize W/Lev over S with Car < 0 (ratio Lev/|Car| -> 1 means
# the geometric surplus barely covers the residue deficit). Random restarts + local moves on generators.
import sys, random, time; sys.path.insert(0, 'src')
from fractions import Fraction as Fr
from ns import NS
from cl import factorizations_down_set
def split(g):
    s = NS.from_generators(g); P, best = factorizations_down_set(s, 'grlex'); D = list(best.values()); d = len(P); m = s.m
    k = [p // m for p in P]; r = [p % m for p in P]; lam = {x: w for w, x in best.items()}; xs = max(D, key=lambda x: lam[x])
    dot = lambda x, v: sum(a * b for a, b in zip(x, v))
    Lev = d * m * dot(xs, k) - (d + 1) * sum(dot(x, k) for x in D)
    Car = d * dot(xs, r) - Fr(d + 1, m) * sum(dot(x, r) for x in D) - Fr((d - 1) * (m - 1), 2)
    return s, Lev, Car
rnd = random.Random(int(sys.argv[1])); e = int(sys.argv[2]); M0, M1, K, budget = map(int, sys.argv[3:7]); t0 = time.time(); best = None
def score(g):
    try: s, Lev, Car = split(g)
    except Exception: return None
    if s.e != len(g) or Car >= 0 or Lev <= 0: return None
    return float((Lev + Car) / Lev), s, Lev, Car
while time.time() - t0 < budget:
    m = rnd.randint(M0, M1); g = [m] + sorted(rnd.sample(range(m + 1, K * m), e - 1)); cur = score(g)
    if cur is None: continue
    for it in range(300):
        h = list(g); i = rnd.randrange(1, e); h[i] = max(m + 1, h[i] + rnd.choice([-3, -2, -1, 1, 2, 3, m, -m]))
        if len(set(h)) < e: continue
        c = score(sorted(h))
        if c is not None and c[0] <= cur[0]: g, cur = sorted(h), c
    if best is None or cur[0] < best[0]:
        best = cur; print(f"{time.time()-t0:.0f}s e={e} W/Lev={best[0]:.4f} gens={best[1].P} Lev={int(best[2])} Car={float(best[3]):.1f} W={best[1].W} c={best[1].c}", flush=True)
