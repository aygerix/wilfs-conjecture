"""TILE-CENTROID test (lead, 2026-10-21). Drop Apery-minimality: M any down-set in N^N that is a complete residue
system for phi mod m (phi = sum gamma_i a_i, gamma_i > m). Test
    (N+1) sum_M phi <= m [ N max_M phi - (N-1)(m-1)/2 ]      (for the lex Apery tile this is exactly Wilf).
Enumerates all down-sets of size m in N^2 (partitions) or N^3 (plane partitions), gamma_i in (m, GMAX*m].
Usage: python tilecent.py N MMIN MMAX GMAX [NSAMPLE SEED]"""
import sys, itertools, random
def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p): yield (p,) + rest
def downsets2(m):
    for lam in partitions(m):
        yield [(i, j) for i, row in enumerate(lam) for j in range(row)]
def downsets3(m):
    # plane partitions: sequence of partitions (layers) each contained in the previous
    def layers(n, prev):
        if n == 0: yield []; return
        for size in range(n, 0, -1):
            for lam in partitions(size):
                if len(lam) <= len(prev) and all(lam[i] <= prev[i] for i in range(len(lam))):
                    for rest in layers(n - size, lam): yield [lam] + rest
    for L in layers(m, (m,) * m):
        yield [(k, i, j) for k, lam in enumerate(L) for i, row in enumerate(lam) for j in range(row)]
N, MMIN, MMAX, GMAX = map(int, sys.argv[1:5])
NS = int(sys.argv[5]) if len(sys.argv) > 5 else 0; rnd = random.Random(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
tot = fail = 0; worst = None
for m in range(MMIN, MMAX + 1):
    Ds = list(downsets2(m) if N == 2 else downsets3(m))
    gams = list(itertools.combinations(range(m + 1, GMAX * m + 1), N))
    if NS: gams = [tuple(sorted(rnd.sample(range(m + 1, GMAX * m + 1), N))) for _ in range(NS)]
    for gs in gams:
        for D in Ds:
            vals = [sum(g * a for g, a in zip(gs, p)) for p in D]
            if len(set(v % m for v in vals)) != m: continue
            tot += 1
            lhs = (N + 1) * sum(vals) * 2; rhs = m * (2 * N * max(vals) - (N - 1) * (m - 1))
            sl = (rhs - lhs) / (2 * m)
            if worst is None or sl < worst[0]: worst = (sl, m, gs, D)
            if lhs > rhs:
                fail += 1
                if fail <= 5: print("FAIL m=%d gammas=%s D=%s slack=%s" % (m, gs, D, sl), flush=True)
    print("m=%d done: tiles tested %d, failures %d, worst %s" % (m, tot, fail, worst[:3] if worst else None), flush=True)
