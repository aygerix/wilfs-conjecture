# Hill-climb on e = E semigroups with m | c, c > 3m, 3e < m to maximize L*/(d+1) of the top-layer load LP.
import sys, random, time
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from atop import atop
E, seed, budget, mmax = map(int, sys.argv[1:5])
rnd = random.Random(seed); t0 = time.time()
def make(m, g, q):
    try: s = NS.from_generators([m] + g + list(range(q * m, q * m + m + 1)))
    except ValueError: return None
    if s.e != E or s.c % s.m or s.c <= 3 * s.m or 3 * s.e >= s.m: return None
    return s
def score(s):
    lhs, rhs, true, d, nx, _ = atop(s); return lhs / rhs
best = None; cur = None; restarts = 0
while time.time() - t0 < budget:
    if cur is None or rnd.random() < 0.02:
        m = rnd.randint(3 * E + 1, mmax); q = rnd.randint(4, 6); g = sorted(rnd.sample(range(m + 1, 2 * m), E - 1))
        s = make(m, g, q)
        if s is None: continue
        cur = (score(s), m, g, q); restarts += 1
    sc, m, g, q = cur
    m2, g2, q2 = m, list(g), q
    r = rnd.random()
    if r < 0.6: i = rnd.randrange(len(g2)); g2[i] = min(2 * m2 - 1, max(m2 + 1, g2[i] + rnd.choice((-2, -1, 1, 2))))
    elif r < 0.8: m2 = max(3 * E + 1, min(mmax, m2 + rnd.choice((-1, 1)))); g2 = [min(2 * m2 - 1, max(m2 + 1, x)) for x in g2]
    else: q2 = max(4, min(7, q2 + rnd.choice((-1, 1))))
    if len(set(g2)) < len(g2): continue
    s = make(m2, sorted(g2), q2)
    if s is None: continue
    sc2 = score(s)
    if sc2 >= sc or rnd.random() < 0.05: cur = (sc2, m2, sorted(g2), q2)
    if best is None or sc2 > best[0]: best = (round(sc2, 4), s.P, s.m, s.c)
print(f'E={E} seed {seed}: best ATOP lhs/bound {best}; restarts {restarts}; {time.time()-t0:.0f}s')
