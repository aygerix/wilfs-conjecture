# Tile-CL for d = 3 tiles from 4-generated semigroups with varied factorization choices (grlex/lex/revlex, all generator
# permutations) and conductor-truncated variants with e = 4.  Skips non-down-sets.  Reports failures and min slack.
import sys, random, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
from exp_cl_adv import with_conductor
from twoface_census import rand_gens
def tcl_cells(cells, d, m):
    S = set(cells)
    if any(x[a] > 0 and tuple(x[:a] + (x[a]-1,) + x[a+1:]) not in S for x in cells for a in range(d)): return None
    w = [0]*m
    for y in cells:
        w[cells[y] % m] += sum(y[a] + 1 for a in range(d) if tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S)
    M = m*(m-1)//2
    return min(((d+1)*M - sum(w[g]*((g - sg) % m) for g in range(m)))/((d+1)*M) for sg in range(m))
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MMIN, MMAX = int(sys.argv[3]), int(sys.argv[4])
n = f = skipped = 0; worst = None
for _ in range(N):
    g = rand_gens(rng, MMIN, MMAX); s0 = NS.from_generators(g)
    sems = [s0] + [with_conductor(g, int(s0.c*fr)) for fr in (0.4, 0.7) if int(s0.c*fr) > s0.m]
    for s in sems:
        if s.e != 4: continue
        for order in ('grlex', 'lex', 'revlex'):
            for perm in itertools.permutations(range(3)):
                Pp, best = factorizations_down_set(s, order, perm)
                cells = {v: w for w, v in best.items()}
                sl = tcl_cells(cells, 3, s.m)
                if sl is None: skipped += 1; continue
                n += 1
                if sl < -1e-12:
                    f += 1
                    if f <= 5: print('Tile-CL d=3 FAIL', s.P, 'c', s.c, order, perm, round(sl, 5), flush=True)
                if worst is None or sl < worst[0]: worst = (round(sl, 5), s.P, s.c, order, perm)
print('d=3 tiles tested', n, '(skipped non-down-sets', skipped, ') Tile-CL fails', f, 'min', worst)
