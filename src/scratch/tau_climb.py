# Adversarial search for the e = 4 residual of the sharp tau-criterion: maximize 4 tau + 2 P2 - 2(m+1).
import sys, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from tau_residual import analyse
def score(gens):
    if reduce(gcd, gens) != 1 or len(set(gens)) != 4: return None
    s = NS.from_generators(sorted(gens))
    if s.e != 4 or s.m != min(gens) or s.c > 60*s.m: return None
    r = analyse(s); return 4*r['tau'] + 2*r['P2'] - 2*(r['m'] + 1), r
for g in ([36,37,42,43], [39,71,72,77], [25,44,45,49], [29,50,69,90], [49,84,107,121], [64,65,72,73], [100,101,110,111]):
    sc = score(g); print('fixed', g, 'deficit', sc[0], {k: sc[1][k] for k in ('m', 'tau', 'P2', 't', 'two', 'slack')})
rng = random.Random(int(sys.argv[1])); runs = int(sys.argv[2]); steps = int(sys.argv[3])
worst = None
for run in range(runs):
    m = rng.randint(20, 120)
    while True:
        g = [m] + [rng.randint(m + 1, 3*m) for _ in range(3)]
        sc = score(g)
        if sc: break
    for _ in range(steps):
        h = list(g); i = rng.randint(1, 3); h[i] = max(m + 1, h[i] + rng.choice([-3, -2, -1, 1, 2, 3, m, -m]))
        sc2 = score(h)
        if sc2 and sc2[0] >= sc[0]: g, sc = h, sc2
    if worst is None or sc[0] > worst[0]: worst = (sc[0], g, sc[1])
    print(f'run {run}: m={m} best deficit {sc[0]} gens {sorted(g)} tau {sc[1]["tau"]} P2 {sc[1]["P2"]} two {sc[1]["two"]} TOP2 slack {sc[1]["slack"]:.3f}', flush=True)
print('WORST', worst[0], sorted(worst[1]), {k: worst[2][k] for k in ('m', 'tau', 'P2', 't', 'q', 'two', 'slack')})
