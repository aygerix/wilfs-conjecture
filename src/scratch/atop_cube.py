# Adversarial anneal over abstract down-sets D in N^d satisfying the general cylinder conditions
#   (CYL) for every nonempty tau: #{q in G : supp q ⊇ tau} <= |D ∩ {x_tau = 0}|     (G = minimal non-elements)
# (necessary for D to be a lattice tile) and non-two-face (all e_a, e_a+e_b in D).  Maximize the ATOP ratio (X = A).
import sys, random, time, itertools
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from atop_shape import atop_shape
d, seed, budget, mlo, mhi = map(int, sys.argv[1:6]); rnd = random.Random(seed); t0 = time.time()
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
def gens(D):
    cand = {add(x, u) for x in D for u in U} - D
    return [q for q in cand if all(sub(q, U[a]) in D for a in range(d) if q[a] > 0)]
CYLONLY = len(sys.argv) > 6 and 'C' in sys.argv[6]
CUBE = len(sys.argv) > 6 and 'Q' in sys.argv[6]
def iscyl(D):
    L = [max(x[a] for x in D) + 1 for a in range(d)]
    return all(x in D for x in itertools.product(*[range(l) for l in L]) if all(tuple(0 if b == c else x[b] for b in range(d)) in D for c in range(d)))
def ok(D):
    if CYLONLY and not iscyl(D): return False
    if CUBE and not all(v in D for v in itertools.product((0, 1), repeat=d)): return False
    if not all(u in D for u in U) or not all(add(U[a], U[b]) in D for a in range(d) for b in range(a + 1, d)): return False
    G = gens(D)
    for k in range(1, d + 1):
        for tau in itertools.combinations(range(d), k):
            if sum(1 for q in G if all(q[t] > 0 for t in tau)) > sum(1 for x in D if all(x[t] == 0 for t in tau)): return False
    return True
def maximal(D): return [x for x in D if all(add(x, u) not in D for u in U)]
def moves(D):
    out = []
    for q in gens(D): out.append(('add', q))
    for x in maximal(D):
        if sum(x) > 2: out.append(('rem', x))
    return out
def start():
    while True:
        L = [rnd.randint(2, 5) for _ in range(d)]
        D = {x for x in itertools.product(*[range(l) for l in L]) if sum(x) <= rnd.randint(2, sum(L))}
        D |= set(itertools.product((0, 1), repeat=d)) if CUBE else (set(U) | {add(U[a], U[b]) for a in range(d) for b in range(a + 1, d)} | {tuple([0] * d)})
        # close downward
        changed = True
        while changed:
            changed = False
            for x in list(D):
                for a in range(d):
                    if x[a] > 0 and sub(x, U[a]) not in D: D.add(sub(x, U[a])); changed = True
        if mlo <= len(D) <= mhi and ok(D): return D
score = lambda D: (lambda r: r[0] / r[1])(atop_shape(sorted(D)))
best = None; cur = None; n = 0
while time.time() - t0 < budget:
    if cur is None or rnd.random() < 0.01:
        D = start(); cur = (score(D), D)
    sc, D = cur
    mv = rnd.choice(moves(D)); D2 = set(D)
    if mv[0] == 'add': D2.add(mv[1])
    else: D2.discard(mv[1])
    if not (mlo <= len(D2) <= mhi) or not ok(D2): continue
    s2 = score(D2); n += 1
    if s2 >= sc or rnd.random() < 0.03: cur = (s2, D2)
    if best is None or s2 > best[0]:
        best = (s2, sorted(D2))
        if s2 > 1: print(f'FAIL ratio {s2:.4f} m={len(D2)}', sorted(D2), flush=True)
print(f'd={d} seed {seed} m in [{mlo},{mhi}]: {n} evaluations; best ATOP ratio {best[0]:.4f} at m={len(best[1])}; {time.time()-t0:.0f}s')
print('best D:', best[1])
