"""Run decomposition of H1' (lead, 2026-10-19).  WRAP-MAX tile (D, P): v = x.P < m on non-maximal cells,
V = {y in A : v(y) >= m}, label h = v on D° = D \\ V and h = lam = v - m on V.  For a threshold theta:
L = {x in D° : v < theta}, E_b(L) = #{x in L : top_b(x) not in L}, V_th = {y in V : lam < theta}.
H1' (shadow form):  f(theta) = sum_b E_b(L) + sum_{y in V, lam >= theta} |y| - |V| >= 0.
Middle regime p <= theta <= m - p (p = P_a = min P): the labels [0, theta) split into p runs (classes mod p).
Each run ends with a low->high step of one of three kinds, each paid by a distinct resource:
  T1  internal a-step z -> z+e_a (z in L, z+e_a in U, inside D°)          weight z_a + 1   (an a-column of E_a)
  T2a a-top z jumps (sigma_a) to an a-floor cell f in V with lam(f) >= theta  weight |f| - 1   (budget)
  T2b a-top z jumps to an a-floor cell f in D° with v(f) in [theta, theta+p) weight |f|       (b-columns of E_b into f)
Cells y in V_th with a lower cover in L are paid by that column (first U-cell = y).  Remaining: F' = cells of V_th
whose lower covers are all in U.  CLAIM-M:  |F'| <= sum of run-end weights (then H1' holds at theta).
usage: python wm_runs.py cert mlo mhi certdir   |   python wm_runs.py rand seed trials mmin mmax dmin dmax"""
import sys, random, gzip, json
from math import gcd

def analyze(m, P, D, stats):
    d = len(P); Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    dn = lambda x, a: tuple(x[i]-(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    if any(v[x] >= m for x in D if x not in A): return False
    V = set(y for y in A if v[y] >= m)
    h = {x: (v[x]-m if x in V else v[x]) for x in D}
    cell = {}
    for x in D: cell[h[x]] = x
    assert len(cell) == m and set(cell) == set(range(m)), "not a tile"
    if not V: return True
    top = {}
    for b in range(d):
        for x in D:
            y = x
            while up(y, b) in Ds: y = up(y, b)
            top[(x, b)] = y
    p = min(P); amin = [a for a in range(d) if P[a] == p]
    for th in range(1, m+1):
        L = set(x for x in D if x not in V and v[x] < th)
        E = [sum(1 for x in L if top[(x, b)] not in L) for b in range(d)]
        f = sum(E)+sum(sum(y) for y in V if v[y]-m >= th)-len(V)
        stats['inst'] += 1
        if f < 0:
            stats['H1fail'] += 1
            print("H1' FAIL", m, P, th, sorted(D), flush=True)
        Vth = [y for y in V if v[y]-m < th]
        Fp = [y for y in Vth if not any(y[b] > 0 and dn(y, b) in L for b in range(d))]
        if not Fp: continue
        if p <= th <= m-p:
            stats['M'] += 1
            best = None
            for a in amin:
                W = 0; types = []
                for c in range(p):
                    if c >= th: continue
                    e = c+((th-1-c)//p)*p
                    z = cell[e]
                    if up(z, a) in Ds:
                        g = up(z, a)
                        assert z in L and g not in V and v[g] == e+p >= th
                        W += z[a]+1; types.append('T1')
                    else:
                        fc = cell[e+p]; assert fc[a] == 0
                        if fc in V:
                            assert v[fc]-m >= th; W += sum(fc)-1; types.append('T2a')
                        else:
                            assert th <= v[fc] < th+p and all(dn(fc, b) in L for b in range(d) if fc[b] > 0)
                            W += sum(fc); types.append('T2b')
                runs = {}
                for y in Fp: runs[(v[y]-m) % p] = runs.get((v[y]-m) % p, 0)+1
                marg = W-len(Fp)
                if best is None or marg < best[0]: best = (marg, a, max(runs.values()), W, len(Fp))
            marg, a, mx, W, nF = best
            stats['Mmaxrun'] = max(stats['Mmaxrun'], mx)
            stats['Fp_gt_p'] += nF > p
            if marg < 0:
                stats['Mfail'] += 1
                if stats['Mfail'] <= 5: print("CLAIM-M FAIL", m, P, "theta", th, "a", a, "W", W, "|F'|", nF, "f", f, sorted(D), flush=True)
            if stats['Mmin'] is None or marg < stats['Mmin'][0]: stats['Mmin'] = (marg, m, P, th)
        elif th > m-p:
            stats['Hi'] += 1
            if stats['Himin'] is None or f < stats['Himin'][0]: stats['Himin'] = (f, m, P, th, len(Fp))
        else:
            stats['Lo'] += 1
    return True

def newstats():
    return dict(inst=0, H1fail=0, M=0, Mfail=0, Mmin=None, Mmaxrun=0, Fp_gt_p=0, Hi=0, Himin=None, Lo=0, tiles=0)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'cert':
        mlo, mhi, cdir = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        for m in range(mlo, mhi+1):
            st = newstats(); units = [u for u in range(1, m) if gcd(u, m) == 1]
            with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as fh:
                for line in fh:
                    rec = json.loads(line); r0 = [x % m for x in rec['r']]
                    if 0 in r0: continue
                    for Dl in rec['tile_cells']:
                        D = list(map(tuple, Dl))
                        for u in units:
                            if analyze(m, [(u*x) % m for x in r0], D, st): st['tiles'] += 1
            print("m=%d" % m, st, flush=True)
    else:
        sys.path.insert(0, sys.argv[9] if len(sys.argv) > 9 else '../nowrap')
        from pmin_tile import apery, minimal_gens, tile
        seed, T, mmin, mmax, dmin, dmax = map(int, sys.argv[2:8]); rng = random.Random(seed); st = newstats()
        for tr in range(T):
            m = rng.randint(mmin, mmax); kk = rng.randint(dmin, dmax); mode = rng.random()
            if mode < 0.4: gens = [m+rng.randint(1, m-1) for _ in range(kk)]
            elif mode < 0.7: gens = [m+rng.randint(1, max(2, m//2)) for _ in range(kk)]
            else: gens = [rng.randint(m+1, 3*m) for _ in range(kk)]
            if None in apery(m, gens): continue
            n, ap = minimal_gens(m, gens)
            if len(n) < 2: continue
            d = len(n); P = [g % m for g in n]
            for key in (lambda x: (sum(x), tuple(-t for t in x)), lambda x: (sum(x[i]*P[i] for i in range(d)), sum(x), tuple(-t for t in x))):
                D = list(tile(m, n, ap, key).values())
                if analyze(m, P, D, st): st['tiles'] += 1
        print(st)
