"""Scan FWx >= 0 (src/fw_refine.py) on all S of genus <= G (mode g) or random hard S (modes R, E as in fw_hard.py)."""
import sys, random
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
from fw_refine import bounds
from fw_hard import closure_with_conductor
def gen(mode, N, seed):
    rnd = random.Random(seed)
    if mode == 'g':
        for g, s in all_by_genus(N):
            if g > 0 and len(s.P) >= 2: yield s
        return
    for it in range(N):
        try:
            if mode == 'R':
                m = rnd.randint(16, 70); d = rnd.randint(3, 9); K = rnd.choice((2, 3, 4, 6, 8))
                s = NS.from_generators([m] + rnd.sample(range(m + 1, K * m), min(d, K * m - m - 1)))
                if s.c < 4 * s.m: continue
            else:
                m = rnd.randint(10, 45); q = rnd.randint(4, 7); k = rnd.randint(1, 4)
                s = closure_with_conductor([m] + rnd.sample(range(m + 1, 2 * m), k), q * m)
        except ValueError: continue
        yield s
if __name__ == '__main__':
    mode, N, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 0
    n = 0; neg = []; negy = []; minr = {}
    for s in gen(mode, N, seed):
        b = bounds(s); n += 1; e = len(s.P)
        r = b['FWx'] / s.m
        if e not in minr or r < minr[e][0]: minr[e] = (r, s.P)
        if b['FWx'] < 0: neg.append((s.P, s.m, s.c, b['mW'], b['FWx'], b['FWy']))
        if b['FWy'] < 0: negy.append((s.P, s.m, s.c, b['mW'], b['FWy']))
    print(f'mode {mode} N {N} seed {seed}: {n} semigroups, FWx < 0 for {len(neg)}')
    for e in sorted(minr): print(f'  e={e}: min FWx/m {minr[e][0]:.3f} at {minr[e][1]}')
    for x in neg[:30]: print('  NEG', x)
    print('  FWy < 0:', len(negy))
    for x in negy[:30]: print('  NEGY', x)
