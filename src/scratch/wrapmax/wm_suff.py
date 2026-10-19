"""H1' in up-set form and two sufficient forms (lead, 2026-10-19).  WRAP-MAX tile, V = wrapped maximal cells (v >= m),
lambda(y) = v(y) - m.  For theta in [1, m]: D'_theta = {x not in V : v(x) < theta} (a down-set), V_theta = {y in V : lambda < theta}.
  Out = #{(x,b) : x in D'_theta, b-top of x not in D'_theta}   (= shadow of the up-set D \\ D'_theta)
  Ex  = #{(x,b) : x in D'_theta, x+e_b in D \\ D'_theta}        (exit edges; Out >= Ex)
  H1' : Out >= |V_theta| - sum_{V \\ V_theta} (|y|-1);   SUFF1: Out >= |V_theta|;   SUFF2: Ex >= |V_theta|.
usage: python wm_suff.py seed trials mmin mmax dmin dmax"""
import sys, random
sys.path.insert(0, '../nowrap')
from pmin_tile import apery, minimal_gens, tile

def check(m, P, D):
    d = len(P); Ds = set(D)
    up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
    A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
    v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    if any(v[x] >= m for x in D if x not in A): return None
    V = [y for y in A if v[y] >= m]
    if not V: return None
    def top(x, b):
        y = x
        while up(y, b) in Ds: y = up(y, b)
        return y
    tops = {(x, b): top(x, b) for x in D for b in range(d)}
    out = []
    for th in range(1, m+1):
        Dp = set(x for x in D if v[x] < th and v[x] < m)
        Vt = [y for y in V if v[y]-m < th]
        Out = sum(1 for x in Dp for b in range(d) if tops[(x, b)] not in Dp)
        Ex = sum(1 for x in Dp for b in range(d) if up(x, b) in Ds and up(x, b) not in Dp)
        rest = sum(sum(y)-1 for y in V if v[y]-m >= th)
        out.append((Out-len(Vt)+rest, Out-len(Vt), Ex-len(Vt), th, len(Vt)))
    return out

if __name__ == '__main__':
    seed, T, mmin, mmax, dmin, dmax = map(int, sys.argv[1:7]); rng = random.Random(seed)
    cnt = [0, 0, 0]; ntile = 0; ex = [None, None, None]
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
            res = check(m, P, D)
            if res is None: continue
            ntile += 1
            for i in range(3):
                bad = [t for t in res if t[i] < 0]
                if bad:
                    cnt[i] += 1
                    if ex[i] is None: ex[i] = (m, n, bad[0])
    print("WRAP-MAX tiles with V nonempty:", ntile, "| tiles failing H1':", cnt[0], "SUFF1 (Out>=|V_th|):", cnt[1], "SUFF2 (Ex>=|V_th|):", cnt[2])
    print("first failures:", ex)
