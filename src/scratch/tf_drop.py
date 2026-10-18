# Two-face e=5 semigroups (e_a + e_b not in the grlex tile): compare W(S) with W(S_a), W(S_b), where S_a drops n_b and
# S_b drops n_a (when the gcd stays 1). Test candidate inductive inequalities.
import sys, random, math; sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
rnd = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); M0, M1, K = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
stats = {'n': 0, 'W>=min': 0, 'W>=max': 0, 'W>=sum': 0}; worst = None
while stats['n'] < N:
    m = rnd.randint(M0, M1)
    g = [m] + sorted(rnd.sample(range(m + 1, K * m), 4))
    try: s = NS.from_generators(g)
    except Exception: continue
    if s.e != 5 or s.c <= 3 * m: continue
    P, best = factorizations_down_set(s, 'grlex'); D = set(best.values()); d = len(P)
    U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    pairs = [(a, b) for a in range(d) for b in range(a + 1, d) if tuple(x + y for x, y in zip(U[a], U[b])) not in D]
    if not pairs: continue
    a, b = pairs[0]; gens = [p for p in P]
    ga = [m] + [p for i, p in enumerate(gens) if i != b]; gb = [m] + [p for i, p in enumerate(gens) if i != a]
    if math.gcd(*ga) != 1 or math.gcd(*gb) != 1: continue
    Sa, Sb = NS.from_generators(ga), NS.from_generators(gb)
    W, Wa, Wb = s.W, Sa.W, Sb.W
    stats['n'] += 1; stats['W>=min'] += W >= min(Wa, Wb); stats['W>=max'] += W >= max(Wa, Wb); stats['W>=sum'] += W >= Wa + Wb
    r = W / max(1, min(Wa, Wb))
    if worst is None or r < worst[0]: worst = (round(r, 3), g, W, Wa, Wb, Sa.e, Sb.e, s.c, Sa.c, Sb.c)
print(stats, 'worst W/min(Wa,Wb)', worst)
