r"""Random S through splitlp.cert (lead, 2026-10-20).  Usage: /usr/bin/python3 splitrnd.py NS SEED MMIN MMAX [-k3] [-open]"""
import sys, random, io, contextlib
sys.path.insert(0, '.')
from splitlp import cert
from tile import build
NS, SEED, MMIN, MMAX = map(int, sys.argv[1:5]); K3 = "-k3" in sys.argv; OPEN = "-open" in sys.argv; UNIT = "-unit" in sys.argv
rnd = random.Random(SEED); n = 0; fails = []; tmin = None
while n < NS:
    m = rnd.randint(MMIN, MMAX); K = rnd.randint(2, 7); k = rnd.randint(1, max(1, m // 2))
    G = [m] + rnd.sample(range(m + 1, K * m), min(k, K * m - m - 1))
    res = build(m, G)
    if res is None: continue
    c, gens, M = res
    if c <= 0: continue
    if OPEN and (c <= 4 * m or 3 * (len(gens) + 1) >= m): continue
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): T = cert(G, K3, "", UNIT)
    n += 1; tmin = T if tmin is None else min(tmin, T)
    if T < -1e-9: fails.append(buf.getvalue().strip())
print("tested %d S, NOCERT %d, min maxT %.3f" % (n, len(fails), tmin))
for f in fails:
    if " d=1 " not in f: print(f)
print("NOCERT with d >= 2:", sum(1 for f in fails if " d=1 " not in f))
