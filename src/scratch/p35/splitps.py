r"""Adversarial search for split certificates on simplex-like tiles (lead, 2026-10-20): S = <m, k_i m + a_i> with small
lifts k_i in {1,..,KMAX} and random residues a_i (these give postage-stamp-like, near-B_h Apery tiles).  Reports the
minimum of maxT/m and every NOCERT with e >= 3.  Usage: /usr/bin/python3 splitps.py NS SEED DMIN DMAX MMIN MMAX KMAX"""
import sys, random, io, contextlib
sys.path.insert(0, '.')
from splitlp import cert
from tile import build
NS, SEED, DMIN, DMAX, MMIN, MMAX, KMAX = map(int, sys.argv[1:8]); rnd = random.Random(SEED)
n = 0; worst = []; fails = []
while n < NS:
    d = rnd.randint(DMIN, DMAX); m = rnd.randint(max(MMIN, d + 2), MMAX)
    A = rnd.sample(range(1, m), d); G = [m] + [rnd.randint(1, KMAX) * m + a for a in A]
    res = build(m, G)
    if res is None or res[0] <= 0 or len(res[1]) < 2: continue
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): T = cert(G)
    n += 1; line = buf.getvalue().strip()
    worst.append((T / m, sorted(G), line)); worst.sort(); worst = worst[:8]
    if T < -1e-9: fails.append(line)
print("tested %d S (e >= 3), NOCERT %d" % (n, len(fails)))
for f in fails[:10]: print("FAIL", f)
for t, G, line in worst: print("%.4f %s | %s" % (t, G, line))
