r"""Random open-regime S (c > 4m, 3e < m): joint statistics of U >= 0 (unit truncation), W2 >= 0, case A (Sigma_supp <= Dep),
kappa-case A (kappa0 <= Dep), height <= 2 (lead, 2026-10-20).  Usage: python truncrnd.py NS SEED MMIN MMAX"""
import sys, random, io, contextlib
sys.path.insert(0, ".")
from collections import Counter
from trunc import one
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); rnd = random.Random(SEED); tab = Counter(); kept = 0; bad = []
while kept < NS:
    m = rnd.randint(MMIN, MMAX); K = rnd.randint(2, 7); n = rnd.randint(2, max(2, m // 3 - 1))
    G = [m] + rnd.sample(range(m + 1, K * m), n)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): r = one(G)
    if r is None or r['c'] <= 4 * m or 3 * (r['d'] + 1) >= m: continue
    kept += 1
    key = (r['U'] >= 0, r['W2'] >= 0, r['mu'] <= 0, r['mk'] <= 0, r['h'] <= 2); tab[key] += 1
    if not (r['U'] >= 0 or r['mk'] <= 0 or r['h'] <= 2): bad.append((G, r))
print("U>=0 W2>=0 caseA kcaseA flat : count")
for k, v in sorted(tab.items()): print(k, v)
print("residual (not U>=0, not kcaseA, not flat):", len(bad))
for G, r in bad[:10]: print(sorted(G), r)
