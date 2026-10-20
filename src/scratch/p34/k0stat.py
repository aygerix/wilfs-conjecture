r"""kappa0 vs Dep and min-phase inversions (lead, 2026-10-21). DEP-CARRY <=> N(sigma) + Dep >= kappa0 (inversion form).
Checks kappa0 = sum_x [floor(x.delta/m) - sum_a floor(k_a(x) delta_a/m)] and reports: TRIV (kappa0 <= Dep) rate,
distribution of (kappa0 - Dep)/m and of (N_cond - (kappa0 - Dep))/m at the conductor phase, open regime separately.
Usage: python k0stat.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
rows = []
cnt = 0
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); c0 = rnd.randint(m + 1, 9 * m)
    G = sorted(rnd.sample(range(m + 1, c0 + m), rnd.randint(2, min(12, c0 - 2))))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; N = len(gens)
    if N < 2 or c <= m: continue
    cnt += 1; D = list(M); Ds = set(D); delta = [g % m for g in gens]
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(N))
    K = {}
    for a in range(N):
        for x in D:
            k = 0; y = x
            while up(y, a) in Ds: y = up(y, a); k += 1
            K[(x, a)] = k
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(N))}
    dep = sum(x[a] + 1 for x in D for a in range(N) if K[(x, a)] == 0 and x not in mx)
    Mp = m * (m - 1) // 2
    tot = sum((K[(x, a)] * delta[a]) % m for x in D for a in range(N))
    k0 = (tot - Mp) // m
    k0b = sum(sum(p * q for p, q in zip(x, delta)) // m - sum(K[(x, a)] * delta[a] // m for a in range(N)) for x in D)
    assert k0 == k0b and (tot - Mp) % m == 0
    lab = {x: (M[x] - c) % m for x in D}
    Ncond = sum(1 for x in D for a in range(N) if K[(x, a)] and lab[x] >= m - (K[(x, a)] * delta[a]) % m)
    op = int(3 * (N + 1) < m and c > 4 * m)
    rows.append((op, (k0 - dep) / m, (Ncond - k0 + dep) / m, k0 <= dep, N, m))
for op in (0, 1):
    R = [r for r in rows if r[0] == op]
    if not R: continue
    tr = sum(r[3] for r in R)
    a = sorted(r[1] for r in R); b = sorted(r[2] for r in R)
    q = lambda v, p: v[int(p * (len(v) - 1))]
    print("open=%d n=%d TRIV %.3f  (k0-Dep)/m quantiles 0/.5/.9/1: %.3f %.3f %.3f %.3f   slack/m at cond min/.1/.5: %.3f %.3f %.3f" % (op, len(R), tr / len(R), q(a, 0), q(a, .5), q(a, .9), q(a, 1), q(b, 0), q(b, .1), q(b, .5)))
