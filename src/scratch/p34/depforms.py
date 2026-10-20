r"""Strength ladder for DEP-CARRY (lead, 2026-10-21). At every phase s (rho0 = s), tile (D, delta):
  V = rho0 + sum_x kappa_s(x).  Bonuses:  Dep (non-maximal-top incidences, DEP-CARRY),
  BD = |boundary \ Max| (non-maximal cells blocked in some direction),  RA = sum_{y in Max} (deg^-_{N1}(y) - 1),
  N1 = interior {x : x + e_b in D for all b}.  Proved: Dep >= BD >= RA (tile difference body).
Tests V + BD >= 0 (S1) and V + RA >= 0 (S2) on all tiles N = 2, 3 and on random lex Apery tiles.
Usage: python depforms.py tiles N MMIN MMAX | sg NS SEED MMAX"""
import sys, random, itertools
sys.path.insert(0, '.')
def forms(m, D, delta, s):
    N = len(delta); Ds = set(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    dn = lambda x, b: tuple(x[t] - (t == b) for t in range(N))
    V = s
    for x in D:
        l = s + sum(a * b for a, b in zip(x, delta)); r = l % m
        V += sum(x[t] for t in range(N) if delta[t] > r) - l // m
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    N1 = {x for x in D if all(up(x, b) in Ds for b in range(N))}
    dep = sum(x[b] + 1 for x in D if x not in mx for b in range(N) if up(x, b) not in Ds)
    BD = sum(1 for x in D if x not in mx and x not in N1)
    RA = sum(sum(1 for b in range(N) if y[b] >= 1 and dn(y, b) in N1) - 1 for y in mx)
    assert dep >= BD >= RA, (D, delta)
    return V, dep, BD, RA
if __name__ == '__main__':
  if sys.argv[1] == 'tiles':
    from subadd_lp import downsets
    N, MMIN, MMAX = map(int, sys.argv[2:5])
    for m in range(MMIN, MMAX + 1):
        tot = f0 = f1 = f2 = 0; w1 = w2 = None
        for D in downsets(N, m):
            for b in itertools.product(range(1, m), repeat=N):
                if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) != m: continue
                for s in range(m):
                    tot += 1; V, dep, BD, RA = forms(m, D, list(b), s)
                    if V + dep < 0: f0 += 1
                    if V + BD < 0:
                        f1 += 1
                        if w1 is None or V + BD < w1[0]: w1 = (V + BD, D if m < 10 else m, b, s, V, BD)
                    if V + RA < 0:
                        f2 += 1
                        if w2 is None or V + RA < w2[0]: w2 = (V + RA, D if m < 10 else m, b, s, V, RA)
        print("N=%d m=%d pairs %d  DEP fails %d  S1(BD) fails %d  S2(RA) fails %d" % (N, m, tot, f0, f1, f2), flush=True)
        if w1: print("   S1 worst", w1)
        if w2: print("   S2 worst", w2)
  else:
    from tile import build
    NS, SEED, MMAX = map(int, sys.argv[2:5]); rnd = random.Random(SEED); cnt = f0 = f1 = f2 = 0; w1 = w2 = None
    while cnt < NS:
        m = rnd.randint(5, MMAX); c0 = rnd.randint(m + 1, 9 * m)
        G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(9, c0 - 2))))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R
        if len(gens) < 2: continue
        cnt += 1; delta = [g % m for g in gens]; D = list(M)
        for s in range(m):
            V, dep, BD, RA = forms(m, D, delta, s)
            if V + dep < 0: f0 += 1
            if V + BD < 0:
                f1 += 1
                if w1 is None or V + BD < w1[0]: w1 = (V + BD, m, gens, s, V, BD)
            if V + RA < 0:
                f2 += 1
                if w2 is None or V + RA < w2[0]: w2 = (V + RA, m, gens, s, V, RA)
    print("S %d (all phases)  DEP fails %d  S1 fails %d  S2 fails %d" % (cnt, f0, f1, f2)); print("  S1 worst", w1); print("  S2 worst", w2)
