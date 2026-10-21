r"""Per-direction form PD of CR_DEP (lead, 2026-10-20): sum_b n(lambda^b) + m Dep >= (d-1) C(m,2), where lambda^b is
the partition of m into b-column lengths and n(lambda) = sum_i (i-1) lambda_i (= sum over pairs of b-columns of the
shorter length).  PD implies CR_DEP (min(sum, sum) >= sum of mins).  Also the per-direction split PD_b:
n(lambda^b) + m Dep_b >= (d-1) C(m,2) / d.  Usage: python pdtest.py NS SEED MMIN MMAX"""
import sys, random
sys.path.insert(0, '.')
from tile import build
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED)
C2 = lambda n: n * (n - 1) // 2
def nl(parts):
    p = sorted(parts, reverse=True); return sum(i * v for i, v in enumerate(p))
cnt = no = f = fo = fb = fbo = 0; w = None
while cnt < NS:
    m = rnd.randint(MMIN, MMAX); k = rnd.randint(2, max(2, m // 2)); c0 = rnd.randint(m + 1, 10 * m)
    G = sorted(rnd.sample(range(m + 1, min(rnd.choice([2 * m, 3 * m, c0 + m]), c0 + m)), min(k, c0 - 1)))
    R = build(m, G)
    if R is None: continue
    c, gens, M = R; d = len(gens)
    if d < 2: continue
    cnt += 1; D = list(M); Ds = set(D); op = 3 * (d + 1) < m; no += op
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
    mx = {x for x in D if all(up(x, b) not in Ds for b in range(d))}
    tot = 0; dep = 0; bad_b = False
    for b in range(d):
        lens = []; depb = 0
        for x in D:
            if up(x, b) not in Ds:
                lens.append(x[b] + 1)
                if x not in mx: depb += x[b] + 1
        tot += nl(lens); dep += depb
        if d * (nl(lens) + m * depb) < (d - 1) * C2(m): bad_b = True
    s = tot + m * dep - (d - 1) * C2(m)
    if s < 0:
        f += 1; fo += op
        if op and (w is None or s / m / m < w[0]): w = (s / m / m, m, gens)
    if bad_b: fb += 1; fbo += op
print("S %d (open %d): PD fails %d (open %d)  per-direction split fails %d (open %d)  worst open PD %s" % (cnt, no, f, fo, fb, fbo, w))
