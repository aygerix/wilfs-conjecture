"""Test the window-exact hybrid bound HC' on height-<=3 tiles (lead, 2026-10-19).
For a height-<=3 tile and phase sigma (r = (phi - sigma) mod m, rho_0 = r(0), rho_a = r(e_a)):
   S >= HC' := sum_{a non-max unit} (d+1-adeg a) rho_a + (d+1) sum_{N2} r - 2 sum_T r - (p+t) rho_0 + m * O_W,
where adeg(a) = sum over maximal pairs z of z_a, p = #non-maximal pairs, t = #cubics, and O_W = number of cells with
residue in the top window [m - rho_0, m) OTHER than maximal pairs z = a+b with rho_a + rho_b < rho_0 (carry -1).
(Proof: flat identity on maximal pairs; their carry -1 cells fill part of the window, which has exactly rho_0 cells.)
Here O_W counts every cell, spikes included.  Reports min HC' and any negative case, on random, core+spike and
near-B_3 families (same generators as crude_imaxcl.py) and on E47/E51.
usage: python hc_test.py seed trials mmin mmax"""
import sys, random
sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import apery_tile, in_semigroup


def hc_min(m, gens):
    best = apery_tile(m, gens)
    if len(best) != m: return None
    d = len(gens); D = {x: w for (w, x) in best.values()}
    if max(sum(x) for x in D) > 3: return None
    def add(x, a): return tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(add(y, a) not in D for a in range(d)))
    E = [tuple(int(i == a) for i in range(d)) for a in range(d)]
    pairs = [x for x in D if sum(x) == 2]; A2 = [z for z in pairs if z in A]; N2 = [z for z in pairs if z not in A]
    T = [y for y in D if sum(y) == 3]; p, t = len(N2), len(T)
    adeg = [sum(z[a] for z in A2) for a in range(d)]
    core = [a for a in range(d) if E[a] not in A]
    def units(z): return [a for a in range(d) for _ in range(z[a])]
    mn = None; mnS = None
    for sg in range(m):
        r = {x: (w-sg) % m for x, w in D.items()}; r0 = r[(0,)*d]
        S = (d+1)*sum(r[x] for x in D if x not in A)-sum((sum(y)-1)*r[y] for y in A)
        hc = sum((d+1-adeg[a])*r[E[a]] for a in core)+(d+1)*sum(r[z] for z in N2)-2*sum(r[y] for y in T)-(p+t)*r0
        ow = 0
        for x, v in r.items():
            if v < m-r0: continue
            if x in A and sum(x) == 2:
                u = units(x)
                if r[E[u[0]]]+r[E[u[1]]] < r0: continue
            ow += 1
        hc += m*ow
        assert S >= hc, (m, gens, sg, S, hc)
        if mn is None or hc < mn[0]: mn = (hc, sg, S)
    return mn


if __name__ == '__main__':
    seed, T, mmin, mmax = map(int, sys.argv[1:5]); rng = random.Random(seed)
    n = 0; neg = 0; worst = None
    named = [(14, [22, 23, 57, 61, 62, 63]), (16, [17, 20, 21]), (14, [16, 17, 19]), (42, [64, 65, 70, 72, 169, 173, 175, 180, 181, 183, 185, 187, 188, 189, 197, 203])]
    for m, g in named: print("named", m, g, "min HC' (value, sigma, S):", hc_min(m, g), flush=True)
    for tr in range(T):
        m = rng.randint(mmin, mmax); fam = rng.random()
        if fam < 0.3: gens = sorted(set(rng.randint(m+1, 3*m) for _ in range(rng.randint(3, 9))))
        elif fam < 0.7:
            k = rng.randint(2, 6); core = [m+x for x in sorted(set(rng.randint(1, m-1) for _ in range(k)))]
            sums = {0}
            for _ in range(3): sums |= {a+x for a in sums for x in core}
            hit = {a % m for a in sums}
            gens = core+[rng.randint(3, 5)*m+res for res in range(1, m) if res not in hit]
        else:
            L = rng.randint(3, max(4, m//2)); gens = [m+x for x in sorted(set(rng.randint(1, L) for _ in range(rng.randint(3, 8))))]
        gens = sorted(set(g for g in gens if g % m))
        gens = [g for g in gens if not in_semigroup(g, m, [h for h in gens if h != g])]
        if len(gens) < 2 or len(set(g % m for g in gens)) < len(gens): continue
        R = hc_min(m, gens)
        if R is None: continue
        n += 1
        if R[0] < 0:
            neg += 1
            if neg <= 8: print("HC' NEGATIVE", m, gens, R, flush=True)
        if worst is None or R[0] < worst[0]: worst = (R[0], m, gens, R)
    print("height<=3 tiles", n, "with HC' < 0 at some phase:", neg, "worst:", worst)
