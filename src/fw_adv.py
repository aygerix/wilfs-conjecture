"""Adversarial search for FW / FWx failures among semigroups outside every theoretical known-Wilf condition.
Phase 1: hill-climb generator sets (fixed m, e) to minimize the density n/c until S is 'uncovered' (fw_uncovered.uncovered).
Phase 2: anneal within the uncovered region minimizing FW/m (target fw) or FWx/m (target fwx).
usage: fw_adv.py m e iters seed target"""
import sys, random, math
sys.path.insert(0, 'src')
from ns import NS
from fw_refine import bounds
from fw_uncovered import uncovered
def mk(gens):
    try:
        s = NS.from_generators(gens)
    except ValueError: return None
    if len(s.P) != len(gens): return None
    return s
def mutate(gens, rnd, m):
    g = list(gens); i = rnd.randrange(1, len(g))
    g[i] = max(m + 1, g[i] + rnd.choice((-3, -2, -1, 1, 2, 3, rnd.randint(-m, m))))
    return sorted(set(g)) if len(set(g)) == len(g) else gens
if __name__ == '__main__':
    m, e, iters, seed, target = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rnd = random.Random(seed)
    while True:
        gens = [m] + sorted(rnd.sample(range(m + 1, 5 * m), e - 1)); s = mk(gens)
        if s: break
    dens = lambda s: (s.c - s.g) / max(1, s.c)
    # phase 1
    cur = dens(s); it = 0
    while not uncovered(s) and it < iters:
        it += 1
        ng = mutate(gens, rnd, m); ns_ = mk(ng)
        if ns_ is None: continue
        v = dens(ns_)
        if v <= cur or rnd.random() < 0.05:
            gens, s, cur = ng, ns_, v
    if not uncovered(s):
        print(f'm={m} e={e} seed={seed}: no uncovered S reached (density {cur:.3f})'); sys.exit()
    key = 'FW' if target == 'fw' else 'FWx'
    b = bounds(s); cur = b[key] / m; best = (cur, gens, b, s.c, s.g)
    for it in range(iters):
        T = max(0.02, 1.0 * (1 - it / iters))
        ng = mutate(gens, rnd, m); ns_ = mk(ng)
        if ns_ is None or not uncovered(ns_): continue
        b = bounds(ns_); v = b[key] / m
        if v <= cur or rnd.random() < math.exp((cur - v) / T):
            gens, s, cur = ng, ns_, v
            if v < best[0]: best = (v, gens, b, s.c, s.g)
    print(f'm={m} e={e} seed={seed} target={key}: min {key}/m = {best[0]:.3f} at {best[1]} (c={best[3]}, g={best[4]}, {best[2]})', flush=True)
