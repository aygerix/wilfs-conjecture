r"""Independent check of a CR_DEP failure (lead, 2026-10-20): S = <m, gens>. Brute-force S, c, g, ell, e, W; then for
every monomial order (lex over every permutation of the generators, and graded variants) the factorization tile of
Ap(S,m), CR_DEP slack, DEP-CARRY at the conductor phase, and MaxCL. Usage: python crfail.py m g1 ... gk"""
import sys, itertools
sys.path.insert(0, '.')
from depcarry import carry
m, *G = map(int, sys.argv[1:])
B = 20 * max(G) + 20 * m
S = [False] * B; S[0] = True
for x in range(1, B): S[x] = any(x >= g and S[x - g] for g in [m] + G)
gaps = [x for x in range(B) if not S[x]]; c = max(gaps) + 1; g = len(gaps); ell = c - g
mingens = [x for x in [m] + G if not any(S[x - y] and S[y] for y in range(1, x))]
e = len(mingens); W = e * ell - c
print("c=%d g=%d ell=%d e=%d W=%d  min gens %s" % (c, g, ell, e, W, mingens))
gens = [x for x in mingens if x != m]; N = len(gens)
ap = [min(x for x in range(B) if S[x] and x % m == i) for i in range(m)]
apset = sorted(ap)
def tile(key):
    # factorization of each Apery element minimal under 'key' over all factorizations (exhaustive)
    M = {}
    for x in apset:
        best = None
        def rec(i, rem, cur):
            nonlocal best
            if i == N:
                if rem == 0:
                    a = tuple(cur)
                    if best is None or key(a) < key(best): best = a
                return
            for k in range(rem // gens[i] + 1): rec(i + 1, rem - k * gens[i], cur + [k])
        rec(0, x, []); M[best] = x
    Ms = set(M)
    down = all(tuple(a[t] - (t == i) for t in range(N)) in Ms for a in M for i in range(N) if a[i])
    return M, down
def crdep(D):
    Ds = set(D); up = lambda x, b: tuple(x[t] + (t == b) for t in range(N)); w = {}
    for b in range(N):
        for x in D:
            if up(x, b) not in Ds: w[x] = w.get(x, 0) + x[b] + 1
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    dep = sum(v for x, v in w.items() if x not in mx)
    ws = sorted(w.values(), reverse=True)
    return (N + 1) * m * (m - 1) // 2 + m * dep - sum(v * (m - 1 - i) for i, v in enumerate(ws)), dep, w, mx
delta = [x % m for x in gens]; rho0 = (-c) % m
res = {}
for perm in itertools.permutations(range(N)):
    for graded in (0, 1):
        key = (lambda a, p=perm, gr=graded: ((sum(a),) if gr else ()) + tuple(a[i] for i in p))
        M, down = tile(key)
        if not down: res[(perm, graded)] = 'notdown'; continue
        sl, dep, w, mx = crdep(list(M))
        kap, tops, dep2, mx2, lnm = carry(m, list(M), delta, rho0)
        assert dep2 == dep
        res[(perm, graded)] = (sl, dep, rho0 + kap + dep, tuple(sorted(M)))
vals = sorted(set((v[0], v[1], v[2]) for v in res.values() if v != 'notdown'))
print("distinct (CR_DEP slack, Dep, DEP-CARRY value) over %d orders:" % len(res), vals)
print("non-down-set orders:", sum(1 for v in res.values() if v == 'notdown'))
# show the default (reverse-lex as in tile.py: compare last coordinate first) tile
M, _ = tile(lambda a: a[::-1])
sl, dep, w, mx = crdep(list(M))
print("rev-lex tile: CR_DEP slack %d Dep %d" % (sl, dep))
for a, x in sorted(M.items(), key=lambda t: t[1]):
    print("  %s w=%3d r=%2d omega=%d %s" % (a, x, (x - c) % m, w.get(a, 0), 'MAX' if a in mx else ''))
