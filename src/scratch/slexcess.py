# Sharper SL candidate (**): with s_x = <r(x) + r(0)> for every cell (a bijection D -> [0,m) for tiles), and
# B_y = w_y * #{u in [0,y]\{0,y} : r(u) <= s_y} (= uniform low-split mass; PROVED characterization), for every t:
#   sum_{y in A, s_y <= t} (B_y - 1)^+  <=  #{z in N : s_z <= t}.
# (**) implies SL(t) for tiles.  Also verify the characterization of low splits against the direct definition.
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, 'src')
from exp_cl_tiling import downsets
def box(y): return list(itertools.product(*[range(k+1) for k in y]))
def check(D, p, m, d):
    S = set(D); zero = tuple([0]*d)
    A = [y for y in D if sum(y) >= 2 and all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d))]
    Aall = set(y for y in D if all(tuple(y[:a] + (y[a]+1,) + y[a+1:]) not in S for a in range(d)))
    boxes = {y: [u for u in box(y) if u != zero and u != y] for y in A}
    phi = {x: sum(i*j for i, j in zip(x, p)) % m for x in D}
    bad = 0
    for sg in range(m):
        r = {x: (phi[x] - sg) % m for x in D}; r0 = r[zero]
        s = {x: (r[x] + r0) % m for x in D}
        ex = [Fr(0)]*m; free = [0]*m
        for y in A:
            w = Fr(sum(y) - 1, len(boxes[y]))
            N1 = sum(1 for u in boxes[y] if r[u] <= s[y])
            N2 = sum(1 for u in boxes[y] if r[u] + r[tuple(a - b for a, b in zip(y, u))] == s[y])
            assert N1 == N2
            ex[s[y]] += max(Fr(0), w*N1 - 1)
        for z in D:
            if not (z in Aall and sum(z) >= 2): free[s[z]] += 1
        a1 = a2 = 0
        for t in range(m):
            a1 += ex[t]; a2 += free[t]
            if a1 > a2: bad += 1; break
    return bad
if __name__ == '__main__':
    for d, mmax in [(2, 12), (3, 10), (4, 8), (5, 7)]:
        n = F = 0; ex = None
        for m in range(3, mmax + 1):
            for D in downsets(m, d):
                if any(all(x[a] == 0 for x in D) for a in range(d)): continue
                for p in itertools.product(range(1, m), repeat=d):
                    if len({sum(i*j for i, j in zip(y, p)) % m for y in D}) != m: continue
                    n += 1; b = check(D, p, m, d)
                    if b:
                        F += 1
                        if ex is None: ex = (m, sorted(D), p)
        print('d', d, 'tiles', n, '(**) fails', F, 'first', ex, flush=True)
