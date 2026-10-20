"""Check, for general S (from generators), the centre-of-mass form
  m*E = rho*r + sum_{unused (x,i)} w*(c - s_x) + (K+1)*sum_{reached y} y
and the sumset form of CORE1: (q+1)*d <= n*ell + m + rho.
Positions u = (s+rho) mod m, levels floor((s+rho)/m); canonical reps via Dijkstra-like DP on (level, degree, code).
Usage: python comass2.py NRAND SEED"""
import random, sys
def semigroup(gens, bound):
    S = [False]*(bound+1); S[0] = True
    for s in range(1, bound+1):
        S[s] = any(s >= g and S[s-g] for g in gens)
    return S
def analyse(gens):
    m = min(gens); B0 = 50*m*max(1, max(gens)//m+1)
    S = semigroup(gens, 4*max(gens)*m + 10)
    n = len(S); f = max(i for i in range(n) if not S[i]); c = f+1
    if c <= m: return None
    q = -(-c//m); rho = q*m - c
    L = [s for s in range(c) if S[s]]
    prim = [s for s in range(1, c) if S[s] and not any(S[a] and S[s-a] for a in range(1, s))]
    A = [g for g in prim if g != m]; K = len(A)
    # canonical reps: best[x] = (level, degree, code, alpha) over sums of A at position x with level <= q+? ; BFS over degree
    Bh = q+3; best = {}
    from itertools import combinations_with_replacement
    frontier = {(0,)*K}
    allreps = {}
    deg = 0
    while frontier and deg <= q+1:
        nf = set()
        for al in frontier:
            s = sum(a*g for a, g in zip(al, A)); lv = (s+rho)//m; x = (s+rho) % m
            if lv > q+1: continue
            code = sum(a*Bh**i for i, a in enumerate(al))
            key = (lv, deg, code)
            if x not in best or key < best[x][0]: best[x] = (key, al)
            for i in range(K):
                b = list(al); b[i] += 1; nf.add(tuple(b))
        frontier = nf; deg += 1
    reach = {x: v for x, v in best.items() if v[0][0] <= q}
    d = len(reach); r = m - d
    ell = len(L); assert ell == sum(q - v[0][0] for v in reach.values() if v[0][0] < q)
    E = (K+1)*ell - q*d + rho
    tot = 0
    for x, ((lx, tx, _), al) in reach.items():
        sx = lx*m + x - rho
        for i, g in enumerate(A):
            w = al[i]+1; s2 = sx + g; y = (s2+rho) % m; ly = (s2+rho)//m
            ay = list(al); ay[i] += 1
            used = y in reach and reach[y][1] == tuple(ay)
            if not used: tot += w*(c - sx)
    lhs = m*E; rhs = rho*r + tot + (K+1)*sum(reach)
    return lhs == rhs, (q+1)*d <= (K+1)*ell + m + rho, E + r >= 0, (m, c, K, E, r)
NR, SEED = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(SEED)
bad = 0; core_eq_bad = 0; nn = 0
for it in range(NR):
    m = rnd.randint(3, 25); k = rnd.randint(2, 5)
    gens = sorted(set([m] + [rnd.randint(m+1, rnd.choice([2, 3, 5, 9])*m) for _ in range(k-1)]))
    import math
    if math.gcd(*gens) != 1: continue
    res = analyse(gens)
    if res is None: continue
    nn += 1
    ok, sumset, core1, info = res
    if not ok: bad += 1; print("ID MISMATCH", gens, info)
    if sumset != core1: core_eq_bad += 1; print("EQUIV MISMATCH", gens, info)
print("checked", nn, "identity mismatches", bad, "equivalence mismatches", core_eq_bad)
