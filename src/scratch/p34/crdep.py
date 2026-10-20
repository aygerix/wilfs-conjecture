r"""CR_DEP: shape-only (residue-free) sufficient condition for DEP-CARRY (lead, 2026-10-21).
Every boundary cell t (a column top in some direction) gets weight w(t) = sum over directions b in which t is a b-top
of |C_b(t)| (= d + |t| when t is maximal); total weight d m.  DEP-CARRY reads sum_t w(t) r(t) <= (d+1)M' + m Dep, and
rearrangement over injective labels gives the sufficient condition
    CR_DEP:  sum_i w_(i) (m - 1 - i) <= (d+1) m(m-1)/2 + m Dep      (w sorted decreasingly).
Modes: 'sg NS SEED MMIN MMAX' (random S, open regime 3e < m, c > 4m, and all S) | 'tiles N MMIN MMAX'."""
import sys, random, itertools
sys.path.insert(0, '.')
def crdep(D, N):
    Ds = set(D); m = len(D)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    w = {}; dep = 0
    for b in range(N):
        for x in D:
            if up(x, b) not in Ds:
                L = x[b] + 1; w[x] = w.get(x, 0) + L
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    dep = sum(v for x, v in w.items() if x not in mx)
    ws = sorted(w.values(), reverse=True)
    lhs = sum(v * (m - 1 - i) for i, v in enumerate(ws))
    return (N + 1) * m * (m - 1) // 2 + m * dep - lhs, dep
if __name__ == '__main__':
  if sys.argv[1] == 'sg':
    from tile import build
    NS, SEED, MMIN, MMAX = map(int, sys.argv[2:6]); rnd = random.Random(SEED)
    cnt = fo = fa = no = 0; wo = wa = None
    while cnt < NS:
        m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 2)); c0 = rnd.randint(m + 1, 10 * m)
        G = sorted(rnd.sample(range(m + 1, min(rnd.choice([2 * m, 3 * m, c0 + m]), c0 + m)), min(k, c0 - 1)))
        R = build(m, G)
        if R is None: continue
        c, gens, M = R; d = len(gens)
        if d < 2: continue
        cnt += 1; sl, dep = crdep(list(M), d)
        openr = c > 4 * m and 3 * (d + 1) < m
        if sl < 0:
            fa += 1
            if wa is None or sl / m / m < wa[0]: wa = (sl / m / m, m, gens, c)
            if openr:
                fo += 1
                if wo is None or sl / m / m < wo[0]: wo = (sl / m / m, m, gens, c)
        if openr: no += 1
    print("S %d (open regime %d)  CR_DEP fails: all %d, open %d" % (cnt, no, fa, fo)); print("  worst all", wa); print("  worst open", wo)
  else:
    from subadd_lp import downsets
    N, MMIN, MMAX = map(int, sys.argv[2:5])
    for m in range(MMIN, MMAX + 1):
        tot = f = fo = 0; worst = None
        for D in downsets(N, m):
            # only shapes that admit some injective labeling (lattice tiles)
            ok = False
            for b in itertools.product(range(1, m), repeat=N):
                if len({sum(x * y for x, y in zip(a, b)) % m for a in D}) == m: ok = True; break
            if not ok: continue
            tot += 1; sl, dep = crdep(D, N)
            if sl < 0:
                f += 1
                if 3 * (N + 1) < m: fo += 1
                if worst is None or sl < worst[0]: worst = (sl, D if m < 12 else '', dep)
        print("N=%d m=%d tile shapes %d  CR_DEP fails %d (with m > 3(N+1): %d)  worst %s" % (N, m, tot, f, fo, worst), flush=True)
