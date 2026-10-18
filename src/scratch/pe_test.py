# PE (positive-excess) candidate, stronger than TOP'':
#   sum over arm incidences (y,a) [y non-top cell, t_a(y) in X] of (pi(t_a y) - psi(y))^+  <=  m(m-1)/2
# Cut profile N(s) = #{(y,a): psi(y) <= s < pi(t_a y)}, s = 1..m-1;  compare with s, m-s.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def pe(s):
    m, c = s.m, s.c; d = s.e - 1
    _, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}  # cell -> apery value
    S = set(cells)
    pos = {}
    for x, w in cells.items():
        pos[x] = (w - c + 1) if w >= c else ((w - c) % m) + 1     # pi for top, psi for non-top
    top = {x for x, w in cells.items() if w >= c}
    inc = []
    for y in cells:
        if y in top: continue
        for a in range(d):
            t = y
            while True:
                z = t[:a] + (t[a] + 1,) + t[a+1:]
                if z in S: t = z
                else: break
            if t in top: inc.append((pos[y], pos[t]))
    PEsum = sum(max(0, b - a) for a, b in inc)
    N = [sum(1 for a, b in inc if a <= s < b) for s in range(1, m)]
    exact = sum(b - a for a, b in inc)    # TOP'' <=> exact <= m(m-1)/2 + sum_y (d - deg y) psi(y)
    deg = {}
    for y in cells:
        if y not in top: deg[y] = 0
    return m, PEsum, N, inc
if __name__ == '__main__':
    G = int(sys.argv[1]); worst = None; nfail = n = 0; cutfail = 0
    for g, s in all_by_genus(G):
        if g == 0 or s.e < 3: continue
        m, PEsum, N, inc = pe(s); n += 1
        r = PEsum/(m*(m-1)/2)
        if PEsum > m*(m-1)//2: nfail += 1
        if any(N[s_-1] > max(s_, m - s_) for s_ in range(1, m)): cutfail += 1
        if worst is None or r > worst[0]: worst = (r, s.P, m, PEsum)
    print('semigroups', n, 'PE fails', nfail, 'cut N(s)<=max(s,m-s) fails', cutfail, 'worst', worst)
