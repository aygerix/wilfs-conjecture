# Two-face d=3 tiles with e_a + e_b == e_c: pass to the 2-D picture Omega' = psi(D), psi(x) = (x_a + x_c, x_b + x_c).
# X(sigma) = sum_{rows R} |R| r(end R) + sum_{cols C} |C| r(top C)   (rows/cols = maximal runs of Omega').
# Checks:  (W)   T(y) = 3 + |y| <= lambda(y) + 2 for every 3-D maximal y (lambda = length of the row/col it ends);
#          (TC2) X(sigma) <= 3M'  (2-D Tile-CL on Omega');
#          (SUF) X(sigma) + 2 sum_{A} r <= 4M'  (then MaxCL follows from (W)).
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from twoface_census import twoface_info, rand_gens
def analyse(s):
    cells, d = tile_of(s); m = s.m
    info = [i for i in twoface_info(cells, m) if 'psi_inj' in i]
    if not info: return None
    a, b = info[0]['pair']; c = 3 - a - b
    S = set(cells)
    A = {y for y in cells if all(tuple(y[:t] + (y[t]+1,) + y[t+1:]) not in S for t in range(3))}
    pic = {(x[a] + x[c], x[b] + x[c]): x for x in cells}
    rows = {}; cols = {}
    for (u, v) in pic:
        if (u - 1, v) not in pic:
            L = 0
            while (u + L, v) in pic: L += 1
            rows[(u + L - 1, v)] = L
        if (u, v - 1) not in pic:
            L = 0
            while (u, v + L) in pic: L += 1
            cols[(u, v + L - 1)] = L
    inv = {x: uv for uv, x in pic.items()}
    lam = {}
    W_ok = True
    for y in A:
        u, v = inv[y]; cand = []
        if (u, v) in rows: cand.append(rows[(u, v)])
        if (u, v) in cols: cand.append(cols[(u, v)])
        lam[y] = max(cand) if cand else 0
        if 3 + sum(y) > lam[y] + 2: W_ok = False
    M = m*(m - 1)//2; worst_tc = None; worst_suf = None; worst_mx = None
    for sg in range(m):
        r = {x: (cells[x] - sg) % m for x in cells}
        X = sum(L*r[pic[e]] for e, L in rows.items()) + sum(L*r[pic[t]] for t, L in cols.items())
        tc = (3*M - X)/(4*M); suf = (4*M - X - 2*sum(r[y] for y in A))/(4*M)
        mx = (4*M - sum((3 + sum(y))*r[y] for y in A))/(4*M)
        worst_tc = tc if worst_tc is None else min(worst_tc, tc)
        worst_suf = suf if worst_suf is None else min(worst_suf, suf)
        worst_mx = mx if worst_mx is None else min(worst_mx, mx)
    down = info[0]['psi_down']
    return dict(W=W_ok, tc=round(worst_tc, 4), suf=round(worst_suf, 4), maxcl=round(worst_mx, 4), down=down, m=m)
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MMIN, MMAX = int(sys.argv[3]), int(sys.argv[4])
    tests = [[36, 37, 42, 43], [29, 50, 69, 90], [23, 54, 60, 75], [87, 144, 160, 190], [78, 113, 188, 231], [23, 37, 59, 68], [50, 91, 104, 113], [37, 65, 91, 119]]
    for g in tests:
        s = NS.from_generators(g); print(g, analyse(s), flush=True)
    n = wf = tf = sf = 0; mins = [1, 1, 1]
    for _ in range(N):
        s = NS.from_generators(rand_gens(rng, MMIN, MMAX))
        if s.e != 4: continue
        R = analyse(s)
        if R is None: continue
        n += 1; wf += not R['W']; tf += R['tc'] < 0; sf += R['suf'] < 0
        if R['tc'] < 0 and tf <= 5: print('  TC2 fail', s.P, R)
        mins = [min(mins[0], R['tc']), min(mins[1], R['suf']), min(mins[2], R['maxcl'])]
    print('two-face (z*=e_c) tiles', n, '| W fails', wf, '| TC2 fails', tf, '| SUF fails', sf, '| min tc, suf, maxcl', mins)
