# ATOP hunt on semigroup tiles, m | c, c > 3m, 3e < m.  mode 'rand' (random generators in (m, 3m)) or 'climb'
# (hill-climb on the ATOP ratio, generators in (m, 2m)).  Reports ATOP with X = top layer and X = all maximal cells,
# and whether the tile is two-face (e_a + e_b not in T for some a != b).
import sys, random, time
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0]); sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
from atop_shape import atop_shape
mode, E, seed, budget, mmax = sys.argv[1], *map(int, sys.argv[2:6])
rnd = random.Random(seed); t0 = time.time()
def make(m, g, q):
    try: s = NS.from_generators([m] + g + list(range(q * m, q * m + m + 1)))
    except ValueError: return None
    if s.e != E or s.c % s.m or s.c <= 3 * s.m or 3 * s.e >= s.m: return None
    return s
def evaluate(s):
    Pp, best = factorizations_down_set(s, 'grlex'); d = len(Pp)
    T = sorted(best.values()); Ts = set(T); lam = {x: w for w, x in best.items()}
    X = [x for x in T if lam[x] >= s.c]
    two = any(tuple(int(i in (a, b)) for i in range(d)) not in Ts for a in range(d) for b in range(a + 1, d))
    lx, rhs, *_ = atop_shape(T, X); la, *_ = atop_shape(T)
    return lx / rhs, la / rhs, two
n = 0; fails = []; worst = {False: None, True: None}; cur = None
while time.time() - t0 < budget:
    if mode == 'rand':
        m = rnd.randint(3 * E + 1, mmax); q = rnd.randint(4, 7)
        s = make(m, sorted(rnd.sample(range(m + 1, 3 * m), E - 1)), q)
        if s is None: continue
        rx, ra, two = evaluate(s)
    else:
        if cur is None or rnd.random() < 0.02:
            m = rnd.randint(3 * E + 1, mmax); q = rnd.randint(4, 6); g = sorted(rnd.sample(range(m + 1, 2 * m), E - 1))
            s = make(m, g, q)
            if s is None: continue
            rx, ra, two = evaluate(s); cur = (rx, m, g, q)
        else:
            sc, m, g, q = cur; m2, g2, q2 = m, list(g), q; r = rnd.random()
            if r < 0.6: i = rnd.randrange(len(g2)); g2[i] = min(2 * m2 - 1, max(m2 + 1, g2[i] + rnd.choice((-2, -1, 1, 2))))
            elif r < 0.8: m2 = max(3 * E + 1, min(mmax, m2 + rnd.choice((-1, 1)))); g2 = [min(2 * m2 - 1, max(m2 + 1, x)) for x in g2]
            else: q2 = max(4, min(7, q2 + rnd.choice((-1, 1))))
            if len(set(g2)) < len(g2): continue
            s = make(m2, sorted(g2), q2)
            if s is None: continue
            rx, ra, two = evaluate(s)
            if rx >= sc or rnd.random() < 0.05: cur = (rx, m2, sorted(g2), q2)
    n += 1
    if rx > 1 + 1e-9:
        fails.append((s.P, round(rx, 4), two)); print('FAIL X', s.P, 'c', s.c, f'ratio {rx:.4f}', 'two-face' if two else 'NON-TWO-FACE', flush=True)
    key = worst[two]
    if key is None or rx > key[0]: worst[two] = (round(rx, 4), round(ra, 4), s.P, s.c)
print(f'{mode} E={E} seed {seed} mmax {mmax}: {n} S, ATOP(X) fails {len(fails)} '
      f'(non-two-face {sum(1 for f in fails if not f[2])}); worst non-two-face (rX, rA, P, c) {worst[False]}; worst two-face {worst[True]}; {time.time()-t0:.0f}s', flush=True)
