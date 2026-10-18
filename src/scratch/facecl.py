# Face-split test for two-face d=3 tiles (x_a x_b = 0 on D): per face D_i (containing the shared axis),
#   F_i(sigma) = sum_{y in A cap D_i} T(y) r(y)  vs  2 * sum_{x in D_i} r(x)   (T = 3 + |y|, axis cells in both faces,
#   axis maximal cell counted in both with weight T/2).  If F_i <= 2 R_i for both faces then
#   sum_A T r <= 2(M' + sum_axis r): report also whether that bound alone is <= 4M'.
import sys, random
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from srcl import tile_of
from twoface_census import twoface_info, rand_gens
def run(s):
    cells, d = tile_of(s); m = s.m
    info = twoface_info(cells, m)
    if not info: return None
    a, b = info[0]['pair']; c = 3 - a - b
    S = set(cells)
    A = {y for y in cells if all(tuple(y[:t] + (y[t]+1,) + y[t+1:]) not in S for t in range(3))}
    faces = [[x for x in cells if x[a] == 0], [x for x in cells if x[b] == 0]]
    axis = [x for x in cells if x[a] == 0 and x[b] == 0]
    M = m*(m-1)//2; worst = None
    for sg in range(m):
        r = {x: (cells[x] - sg) % m for x in cells}
        res = []
        for F in faces:
            lhs = sum((3 + sum(y))*r[y]*(0.5 if (y[a] == 0 and y[b] == 0) else 1) for y in F if y in A)
            res.append(2*sum(r[x] for x in F) - lhs)
        tot = 4*M - sum((3 + sum(y))*r[y] for y in A)
        key = min(res)/(4*M)
        if worst is None or key < worst[0]: worst = (round(key, 4), sg, [round(t/(4*M), 4) for t in res], round(tot/(4*M), 4))
    return worst
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2]); MMIN, MMAX = int(sys.argv[3]), int(sys.argv[4])
    tests = [[36, 37, 42, 43], [29, 50, 69, 90], [23, 54, 60, 75], [87, 144, 160, 190], [78, 113, 188, 231], [23, 37, 59, 68], [50, 91, 104, 113], [37, 65, 91, 119]]
    n = f = 0; W = None
    for g in tests + [rand_gens(rng, MMIN, MMAX) for _ in range(N)]:
        s = NS.from_generators(g)
        if s.e != 4: continue
        w = run(s)
        if w is None: continue
        n += 1
        if w[0] < 0:
            f += 1
            if f <= 8: print('face-split fails', s.P, 'm', s.m, w, flush=True)
        if W is None or w[0] < W[0]: W = (w, s.P)
    print('two-face tiles', n, 'face-split fails', f, 'worst', W)
