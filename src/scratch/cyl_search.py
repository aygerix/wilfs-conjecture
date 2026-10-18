# Is HT a property of CYLINDRICAL sets alone (no lattice)?  D = {(i,j,k): j < h(i), k < f(i), k < g(j)} [minus q*+N^3],
# h, f, g nonincreasing (faces F3, F2, F1), non-two-face: h(1), f(1), g(1) >= 2.  Hill-climb minimising H - (m-1)
# for m in [mlo, mhi].  usage: cyl_search.py mlo mhi iters seed [qstar]
import sys, random
sys.path.insert(0, 'src/scratch')
from heightH import H_of
import os
from bounds_lib import all_bounds
OBJ = os.environ.get('OBJ', 'H')
ALLC = bool(os.environ.get('ALLC'))
def build(h, f, g, q=None):
    D = set()
    for i in range(len(h)):
        for j in range(h[i]):
            if j >= len(g): break
            for k in range(min(f[i], g[j])):
                if q and i >= q[0] and j >= q[1] and k >= q[2]: continue
                D.add((i, j, k))
    return D
def valid(h, f, g):
    ok = lambda s: all(s[i] >= s[i+1] for i in range(len(s)-1)) and s[-1] >= 1
    return (ok(h) and ok(f) and ok(g) and h[0] == len(g) and f[0] == g[0] and len(h) == len(f)
            and (ALLC or (len(h) >= 2 and len(g) >= 2 and h[1] >= 2 and f[1] >= 2 and g[1] >= 2)))
def rand_stair(n, top):
    s = sorted((random.randint(1, top) for _ in range(n)), reverse=True); s[0] = top
    return s
def mutate(h, f, g):
    h, f, g = h[:], f[:], g[:]
    c = random.randrange(6)
    if c == 0:   # change an entry of h
        i = random.randrange(1, len(h)); h[i] += random.choice((-1, 1))
    elif c == 1:
        i = random.randrange(1, len(f)); f[i] += random.choice((-1, 1))
    elif c == 2:
        j = random.randrange(1, len(g)); g[j] += random.choice((-1, 1))
    elif c == 3:  # change L1 (append/remove last of h, f)
        if random.random() < .5 and len(h) > (1 if ALLC else 2): h.pop(); f.pop()
        else: h.append(1); f.append(1)
    elif c == 4:  # L2
        if random.random() < .5 and len(g) > (1 if ALLC else 2): g.pop(); h = [min(x, len(g)) for x in h]; h[0] = len(g)
        else: g.append(1); h[0] = len(g)
    else:         # L3
        d = random.choice((-1, 1)); f[0] += d; g[0] += d
    return h, f, g
def score(h, f, g, mlo, mhi, q=None):
    D = build(h, f, g, q); m = len(D)
    if q and (q not in build(h, f, g) or any(q[i] == 0 for i in range(3))): return (10**9, m)
    pen = max(0, mlo - m, m - mhi) * 10
    if OBJ == 'H': v = H_of(D) - (m - 1)
    elif OBJ == 'Pi': v = all_bounds(D)['Pi'] - 2*(m - 1)
    elif OBJ == 'psi':
        from peel_test import psis
        v = max(psis(D))
    else: v = all_bounds(D)[OBJ] - (m - 1)
    return v + pen, m
if __name__ == '__main__':
    mlo, mhi, iters, seed = map(int, sys.argv[1:5]); random.seed(seed)
    USEQ = len(sys.argv) > 5
    best_overall = None
    for restart in range(int(__import__('os').environ.get('RESTARTS', 20))):
        L1, L2, L3 = (random.randint(2, 9) for _ in range(3))
        while True:
            h = rand_stair(L1, L2); f = rand_stair(L1, L3); g = rand_stair(L2, L3)
            for s in (h, f, g): s[1] = max(s[1], 2)
            if valid(h, f, g): break
        q = None
        cur = score(h, f, g, mlo, mhi); state = (h, f, g, q)
        T = 3.0
        for it in range(iters):
            nh, nf, ng = mutate(*state[:3]); nq = state[3]
            if USEQ and random.random() < 0.15:
                nq = None if (nq and random.random() < .3) else tuple(random.randint(1, 4) for _ in range(3))
            if not valid(nh, nf, ng): continue
            sc = score(nh, nf, ng, mlo, mhi, nq)
            if sc[0] <= cur[0] or random.random() < pow(2.718, (cur[0] - sc[0]) / T):
                state, cur = (nh, nf, ng, nq), sc
            T = max(0.05, T * 0.999)
            if mlo <= cur[1] <= mhi and (best_overall is None or cur[0] < best_overall[0]):
                best_overall = (cur[0], cur[1], state)
        print(restart, 'cur', cur, 'best', best_overall[:2] if best_overall else None, flush=True)
    print('BEST', best_overall)
