"""Independent check of codex P6d WINDOW-H (all heights), written by the lead from the report's definitions only.
Unit lift l(x) = (1-|x|) rho + sum x_i rho_i, K = floor(l/m).  Core units = non-maximal units (k), spikes = maximal
units (s), d = k + s.  delta_i = k+1 - sum_{z in Q} z_i over degree-2 cells Q.  psi_j(z) = sum_{i: z+e_i in D}(z_i+1).
L_H = sum_{core i}(s+delta_i) rho_i + sum_{j=2}^{H-1} sum_{z in N_j}(d+j-psi_j(z)) r(z).
O_H = rho - #{pairs K=-1} - sum_{j>=3} #{y in C_j : r(y) in W},  W = [m-rho, m).
b_y = (j-1)K(y) - sum_i y_i K(y-e_i) + [r(y) in W].
Claim: S - m*PAplus = L_H + m(O_H + Pplus + sum_{j>=3} b_y), with b_y >= -(j-2), O_H >= 0.
usage: python windowH_check.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/nowrap')
from pmin_tile import apery, minimal_gens, tile

def check(m, n, D):
    d = len(n); P = [g % m for g in n]; Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    dn = lambda x, a: tuple(x[i]-(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    E = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    core = [a for a in range(d) if E[a] not in A]; k = len(core); s = d-k
    H = max(sum(x) for x in D); Q = [z for z in D if sum(z) == 2]
    delta = {i: k+1-sum(z[i] for z in Q) for i in core}
    psi = {z: sum(z[i]+1 for i in range(d) if up(z, i) in Ds) for z in D}
    worst_b = 0; minO = None
    for sg in range(m):
        r = {x: (sum(x[i]*P[i] for i in range(d))-sg) % m for x in D}
        rho = r[(0,)*d]; rh = [r[E[a]] for a in range(d)]
        l = {x: (1-sum(x))*rho+sum(x[i]*rh[i] for i in range(d)) for x in D}
        K = {x: l[x]//m for x in D}
        assert all(l[x]-m*K[x] == r[x] for x in D)
        S = (d+1)*sum(r[x] for x in D if x not in A)-sum((sum(y)-1)*r[y] for y in A)
        inW = lambda x: r[x] >= m-rho
        LH = sum((s+delta[i])*rh[i] for i in core)+sum((d+sum(z)-psi[z])*r[z] for z in D if z not in A and 2 <= sum(z) <= H-1)
        PAplus = sum(1 for z in Q if z in A and K[z] == 1); Pplus = sum(1 for z in Q if z not in A and K[z] == 1)
        OH = rho-sum(1 for z in Q if K[z] == -1)-sum(1 for y in D if sum(y) >= 3 and inW(y))
        bsum = 0
        for y in D:
            j = sum(y)
            if j < 3: continue
            b = (j-1)*K[y]-sum(y[i]*K[dn(y, i)] for i in range(d) if y[i] > 0)+int(inW(y))
            assert b >= -(j-2), ("b bound", m, n, sg, y, b)
            worst_b = min(worst_b, b+(j-2)); bsum += b
        assert S-m*PAplus == LH+m*(OH+Pplus+bsum), ("identity", m, n, sg, S-m*PAplus, LH+m*(OH+Pplus+bsum))
        assert all(psi[z] <= d+sum(z) for z in D if z not in A)
        minO = OH if minO is None else min(minO, OH)
    return H, minO

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed); cnt = {}; negO = 0
    for tr in range(T):
        m = rng.randint(mmin, mmax); kk = rng.randint(2, 7)
        gens = [rng.randint(m+1, rng.choice([2, 3, 4])*m) for _ in range(kk)] if rng.random() < 0.6 else [m+rng.randint(1, max(2, m//2)) for _ in range(kk)]
        if None in apery(m, gens): continue
        n, ap = minimal_gens(m, gens)
        if len(n) < 2: continue
        D = list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values())
        H, minO = check(m, n, D); cnt[H] = cnt.get(H, 0)+1; negO += minO < 0
    print("WINDOW-H identity, b_y >= -(j-2), psi <= d+j verified at every phase; tiles by height:", sorted(cnt.items()), "tiles with O_H < 0 at some phase:", negO)
