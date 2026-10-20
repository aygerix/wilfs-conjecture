r"""DEP-CARRY for every S (lead, 2026-10-21). Lex tile D over all generators except m, delta = gens mod m,
rho0 = (-c) mod m, K(x) = floor((rho0 + x.delta)/m), r(x) = (rho0 + x.delta) mod m = (w(x) - c) mod m,
kappa(x) = sum_{b: delta_b > r(x)} x_b - K(x).  Exact identity (CH' rewritten):
    W = rho0 + sum_x kappa(x) + sum_{column tops t} |C_t| j(t),   j(t) = (r(t) - w(t) + c)/m >= 0,
and j >= 1 on non-maximal tops, so DEP-CARRY: rho0 + sum kappa + Dep >= 0 implies Wilf.
Modes: 'sg NS SEED MMAX' (random S, identity + DEP-CARRY at the conductor phase and at every phase);
'tiles N MMIN MMAX' (all down-sets N = 2, 3 and all delta, every phase).  """
import sys, random, itertools
sys.path.insert(0, '.')
def carry(m, D, delta, rho0):
    N = len(delta); Ds = set(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    kap = 0
    for x in D:
        l = rho0 + sum(a * b for a, b in zip(x, delta)); r = l % m
        kap += sum(x[t] for t in range(N) if delta[t] > r) - l // m
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    tops = []
    for b in range(N):
        for x in D:
            if x[b] == 0:
                y = x
                while up(y, b) in Ds: y = up(y, b)
                tops.append((y, y[b] + 1))
    dep = sum(L for t, L in tops if t not in mx)
    lnm = sum(L * ((rho0 + sum(a * b for a, b in zip(t, delta))) % m) for t, L in tops if t not in mx)
    return kap, tops, dep, mx, lnm
if __name__ == '__main__':
  if sys.argv[1] == 'sg':
    from tile import build
    NS, SEED, MMAX = map(int, sys.argv[2:5]); rnd = random.Random(SEED)
    cnt = mism = f0 = fall = fmax = 0; worst = None; worstall = None
    while cnt < NS:
        m = rnd.randint(5, MMAX); c0 = rnd.randint(m + 1, 9 * m)
        G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(8, c0 - 2))))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; N = len(gens)
        if N < 2 or c <= m: continue
        cnt += 1; delta = [g % m for g in gens]; D = list(M); rho0 = (-c) % m
        kap, tops, dep, mx, lnm = carry(m, D, delta, rho0)
        g = sum(w // m for w in M.values()); W = (N + 1) * (c - g) - c
        J = sum(L * (((M[t] - c) % m) - M[t] + c) // m for t, L in tops)
        if W != rho0 + kap + J: mism += 1
        val = rho0 + kap + dep
        if val < 0: f0 += 1
        if rho0 * m + kap * m + lnm < 0: fmax += 1
        if worst is None or val < worst[0]: worst = (val, rho0, kap, dep, m, gens, c, W)
        for s in range(m):   # every phase
            k2, _, d2, _, _ = carry(m, D, delta, s)
            if s + k2 + d2 < 0:
                fall += 1
                if worstall is None or s + k2 + d2 < worstall[0]: worstall = (s + k2 + d2, s, m, gens)
    print("S: %d  identity mismatches %d  DEP-CARRY(conductor phase) fails %d  MaxCL(conductor) fails %d" % (cnt, mism, f0, fmax))
    print("  worst at conductor phase:", worst)
    print("  DEP-CARRY at some phase fails: %d instances; worst %s" % (fall, worstall))
  else:
    from subadd_lp import downsets
    N, MMIN, MMAX = map(int, sys.argv[2:5])
    for m in range(MMIN, MMAX + 1):
        tot = fail = 0; worst = None
        for D in downsets(N, m):
            for b in itertools.product(range(1, m), repeat=N):
                e = {a: sum(x * y for x, y in zip(a, b)) % m for a in D}
                if len(set(e.values())) != m: continue
                for s in range(m):
                    tot += 1
                    k2, _, d2, _, _ = carry(m, D, list(b), s)
                    v = s + k2 + d2
                    if v < 0:
                        fail += 1
                        if fail <= 3: print("  FAIL", m, D, b, s, v, flush=True)
                    if worst is None or v < worst[0]: worst = (v, D if len(D) < 12 else len(D), b, s)
        print("N=%d m=%d (tile, phase) pairs %d  DEP-CARRY fails %d  min %s" % (N, m, tot, fail, worst), flush=True)
