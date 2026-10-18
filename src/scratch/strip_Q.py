# Strip bound Q for q*-free cylindrical sets.  Direction 3 (columns over F3, length l3 = min(f(u1), g(u2))):
#   f-strips: for each u1, mu(u1) = #{u2 < h(u1) : g(u2) >= f(u1)}, weight f(u1);
#   g-strips: for each u2, nu(u2) = #{u1 < rho(u2) : f(u1) > g(u2)}, weight g(u2).
#   Every cell of F3 lies in exactly one strip; the run from the cell to the strip end is a straight plateau, so
#   Q3 = sum w*C(mu,2) <= Hs_3 <= H_3, and m = sum w*mu.  Q = Q1 + Q2 + Q3 (cyclic relabelling).
# Q - m = sum_strips w*(C(mu,2) - mu/3)*3/3 ... reported as Q - (m-1).   usage: strip_Q.py tiles m... | cyl M
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from math import comb
def profiles(D, a, b, c):
    """for direction a: face F_a in coords (b, c).  returns lists: h = extent of F_a in c at each b-coordinate,
    f = extent in a over (b, 0) i.e. length l_a(b,0), g = l_a(0,c)."""
    def inD(i, j, k):
        x = [0, 0, 0]; x[a] = i; x[b] = j; x[c] = k
        return tuple(x) in D
    Lb = 0
    while inD(0, Lb, 0): Lb += 1
    Lc = 0
    while inD(0, 0, Lc): Lc += 1
    h = []
    for j in range(Lb):
        n = 0
        while inD(0, j, n): n += 1
        h.append(n)
    def la(j, k):
        n = 0
        while inD(n, j, k): n += 1
        return n
    f = [la(j, 0) for j in range(Lb)]
    g = [la(0, k) for k in range(Lc)]
    return h, f, g, la
def Qdir(D, a):
    b, c = (a + 1) % 3, (a + 2) % 3
    h, f, g, la = profiles(D, a, b, c)
    Q = mass = 0; strips = []
    for j in range(len(h)):             # f-strips (fixed b-coordinate j): cells k < h[j] with g[k] >= f[j]
        mu = sum(1 for k in range(h[j]) if g[k] >= f[j]); w = f[j]
        if mu: Q += w*comb(mu, 2); mass += w*mu; strips.append((w, mu))
    rho = [sum(1 for j in range(len(h)) if h[j] > k) for k in range(len(g))]
    for k in range(len(g)):             # g-strips (fixed c-coordinate k): cells j < rho[k] with f[j] > g[k]
        nu = sum(1 for j in range(rho[k]) if f[j] > g[k]); w = g[k]
        if nu: Q += w*comb(nu, 2); mass += w*nu; strips.append((w, nu))
    return Q, mass, strips
def Q_of(D):
    out = [Qdir(D, a) for a in range(3)]
    m = len(D)
    assert all(o[1] == m for o in out), [o[1] for o in out]   # valid only for q*-free cylindrical D
    return sum(o[0] for o in out), out
if __name__ == '__main__':
    from tile_enum import enumerate_tiles, min_nonelements
    if sys.argv[1] == 'tiles':
        for m in map(int, sys.argv[2:]):
            worst = None; fails = 0; n = 0
            for r, D, poly in enumerate_tiles(m):
                if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
                D = set(D)
                if any(min(q) > 0 for q in min_nonelements(D)): continue
                n += 1
                Q, out = Q_of(D); v = Q - (m - 1); fails += v < 0
                if worst is None or v < worst[0]: worst = (v, r)
            print(f'm={m}: q*-free tiles {n}; Q<m-1: {fails}; min Q-(m-1) {worst}', flush=True)
