"""Adversarial search for FW failures at fixed embedding dimension e (no coverage filter): anneal generator sets
<m, a_1..a_{e-1}> (m in [mlo, mhi], a_i in (m, K m)) minimizing FW/m.  usage: fw_adv2.py e mlo mhi K iters seed [fw|fwx|fwy] [qmin]   (qmin: only S with c > (qmin-1) m)"""
import sys, random, math
sys.path.insert(0, 'src')
from ns import NS
from fw_refine import bounds
def mk(gens):
    try: s = NS.from_generators(gens)
    except ValueError: return None
    return s if len(s.P) == len(gens) else None
if __name__ == '__main__':
    e, mlo, mhi, K, iters, seed = map(int, sys.argv[1:7]); key = {'fwx': 'FWx', 'fwy': 'FWy'}.get(sys.argv[7] if len(sys.argv) > 7 else '', 'FW')
    qmin = int(sys.argv[8]) if len(sys.argv) > 8 else 0
    ok = lambda s: s is not None and s.c > (qmin - 1) * s.m
    rnd = random.Random(seed)
    while True:
        m = rnd.randint(mlo, mhi); gens = [m] + sorted(rnd.sample(range(m + 1, K * m), e - 1)); s = mk(gens)
        if ok(s) or (s and qmin == 0): break
    cur = bounds(s)[key] / m; best = (cur, gens, s.c)
    for it in range(iters):
        T = max(0.02, 2.0 * (1 - it / iters))
        g = list(gens)
        if rnd.random() < 0.1 and mlo < mhi:
            nm = min(mhi, max(mlo, g[0] + rnd.choice((-1, 1)))); g[0] = nm
        else:
            i = rnd.randrange(1, e); g[i] = g[i] + rnd.choice((-2, -1, 1, 2, rnd.randint(-g[0], g[0])))
        if any(x <= g[0] for x in g[1:]) or len(set(g)) < e or max(g) >= K * g[0]: continue
        g = [g[0]] + sorted(g[1:]); s = mk(g)
        if not ok(s): continue
        v = bounds(s)[key] / g[0]
        if v <= cur or rnd.random() < math.exp((cur - v) / T):
            gens, cur = g, v
            if v < best[0]: best = (v, g, s.c)
    print(f'e={e} m in [{mlo},{mhi}] K={K} seed={seed} qmin={qmin}: min {key}/m = {best[0]:.3f} at {best[1]} (c={best[2]})', flush=True)
