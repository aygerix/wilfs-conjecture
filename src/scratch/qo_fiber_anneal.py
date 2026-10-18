# Anneal over RCON (Wall+Floor cone sets) maximizing the fiber size of doubly-same qO cells (target fib) or their number (ndbl).
import sys, random, math
sys.path.insert(0, 'src/scratch')
from cls_anneal import build
from corner_anneal import valid, mutate, msize
from qo_fiber import dbl
name, M0, M1, iters, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
INIT = eval(sys.argv[6]) if len(sys.argv) > 6 else None
rnd = random.Random(seed)
h, F, G, q = ([list(v) for v in INIT] if INIT else ([3, 2, 2], [3, 2, 2], [3, 2, 2], [1, 1, 1]))
cur = None; best = (-1, None)
for it in range(iters):
    T = max(0.05, 2.0 * (1 - it / iters))
    nh, nF, nG, nq = mutate(h, F, G, q, rnd)
    if not valid(nh, nF, nG, nq, 'cone'): continue
    m = msize(nh, nF, nG, nq)
    if m > 2 * M1: continue
    n, t, a, g = dbl(build(nh, nF, nG, nq))
    v = {'fib': g, 'fibany': a, 'ndbl': n, 'ndbl-t': n - t}[name]
    pen = 0 if M0 <= m <= M1 else -abs(m - (M0 if m < M0 else M1)) * 0.3
    sc = v + pen
    if cur is None or sc >= cur or rnd.random() < math.exp((sc - cur) / T):
        h, F, G, q, cur = nh, nF, nG, nq, sc
        if pen == 0 and v > best[0]: best = (v, (tuple(h), tuple(F), tuple(G), tuple(q), (n, t, a, g)))
print(name, M0, M1, 'seed', seed, 'best', best, flush=True)
