"""Layer budget of WINDOW-H (lead, 2026-10-19): per degree j >= 3, neg_j = sum (b_y)^-, pos_j = sum (b_y)^+, and the
global budget G = L_H/m + O_H + Pplus + PAplus.  MaxCL <=> G + sum_j (pos_j - neg_j) >= 0.
Reports at each tile's worst phase (min S): how the deficit sum_j neg_j compares with G and with pos, per height.
usage: python layer_budget.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/nowrap')
from pmin_tile import apery, minimal_gens, tile

def layers(m, n, D):
    d = len(n); P = [g % m for g in n]; Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d)); dn = lambda x, a: tuple(x[i]-(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    E = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    core = [a for a in range(d) if E[a] not in A]; k = len(core); s = d-k; H = max(sum(x) for x in D)
    Q = [z for z in D if sum(z) == 2]; delta = {i: k+1-sum(z[i] for z in Q) for i in core}
    psi = {z: sum(z[i]+1 for i in range(d) if up(z, i) in Ds) for z in D}
    best = None
    for sg in range(m):
        r = {x: (sum(x[i]*P[i] for i in range(d))-sg) % m for x in D}; rho = r[(0,)*d]; rh = [r[e] for e in E]
        K = {x: ((1-sum(x))*rho+sum(x[i]*rh[i] for i in range(d)))//m for x in D}
        S = (d+1)*sum(r[x] for x in D if x not in A)-sum((sum(y)-1)*r[y] for y in A)
        inW = lambda x: r[x] >= m-rho
        LH = sum((s+delta[i])*rh[i] for i in core)+sum((d+sum(z)-psi[z])*r[z] for z in D if z not in A and 2 <= sum(z) <= H-1)
        PAp = sum(1 for z in Q if z in A and K[z] == 1); Pp = sum(1 for z in Q if z not in A and K[z] == 1)
        OH = rho-sum(1 for z in Q if K[z] == -1)-sum(1 for y in D if sum(y) >= 3 and inW(y))
        neg = {}; pos = {}
        for y in D:
            j = sum(y)
            if j < 3: continue
            b = (j-1)*K[y]-sum(y[i]*K[dn(y, i)] for i in range(d) if y[i] > 0)+int(inW(y))
            if b < 0: neg[j] = neg.get(j, 0)-b
            else: pos[j] = pos.get(j, 0)+b
        G = LH/m+OH+Pp+PAp
        if best is None or S < best[0]: best = (S, sg, G, neg, pos, H)
    return best

if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed); stats = {}
    for tr in range(T):
        m = rng.randint(mmin, mmax); kk = rng.randint(2, 7)
        gens = [rng.randint(m+1, rng.choice([2, 3, 4])*m) for _ in range(kk)] if rng.random() < 0.5 else [m+rng.randint(1, max(2, m//rng.choice([2, 3, 5]))) for _ in range(kk)]
        if None in apery(m, gens): continue
        n, ap = minimal_gens(m, gens)
        if len(n) < 2: continue
        S, sg, G, neg, pos, H = layers(m, n, list(tile(m, n, ap, lambda x: (sum(x), tuple(-t for t in x))).values()))
        N = sum(neg.values()); Pz = sum(pos.values())
        key = min(H, 6); st = stats.setdefault(key, [0, 0, 0, 0.0, None])
        st[0] += 1; st[1] += N > 0; st[2] += N > G   # deficit exceeds global budget (so needs positive b's)
        if N > 0:
            frac = N/(G+Pz) if G+Pz > 0 else 9
            st[3] = max(st[3], frac)
            # does each layer's deficit fit under the next-lower layer's positive mass plus G?  (LAYER-LOCAL test)
            ok = all(neg.get(j, 0) <= pos.get(j-1, 0)+G for j in neg)
            if not ok and st[4] is None: st[4] = (m, n, sg, round(G, 2), neg, pos)
    for h in sorted(stats):
        st = stats[h]; print("height", h if h < 6 else ">=6", "tiles", st[0], "with deficit", st[1], "deficit > G", st[2], "max deficit/(G+pos)", round(st[3], 3), "LAYER-LOCAL counterexample:", st[4])
