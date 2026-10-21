r"""Random S through kunz_face.face (lead, 2026-10-20): counts of R < 0, RT < 0, UA < 0, AM < 0, FX < 0 (each a valid
lower bound for W); prints every RT < 0 instance.  Usage: /usr/bin/python3 facernd.py NS SEED MMIN MMAX KMAX [-open]"""
import sys, random, io, contextlib
sys.path.insert(0, '.')
from kunz_face import face, apery
NS, SEED, MMIN, MMAX, KMAX = map(int, sys.argv[1:6]); OPEN = '-open' in sys.argv
rnd = random.Random(SEED); n = 0; neg = {k: 0 for k in ('R', 'RT', 'UA', 'AM', 'FX')}; worst = []
while n < NS:
    m = rnd.randint(MMIN, MMAX); K = rnd.randint(2, KMAX); k = rnd.randint(1, max(1, m // 2))
    G = [m] + rnd.sample(range(m + 1, K * m), min(k, K * m - m - 1))
    w = apery(m, G)
    if max(w) >= 10**17: continue
    c = max(w) - m + 1
    if c <= 0: continue
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): W, out = face(G)
    e = int(buf.getvalue().split('e=')[1].split()[0])
    if OPEN and (c <= 4 * m or 3 * e >= m): continue
    n += 1
    if e < 3: continue
    for kk in neg:
        if out[kk] is not None and out[kk] < -1e-7: neg[kk] += 1
    if out['RT'] < -1e-7: print('RT<0 (e>=3):', buf.getvalue().strip(), flush=True)
    worst.append((out['RT'] / max(1, c), buf.getvalue().strip())); worst.sort(); worst = worst[:5]
print("tested %d (all e), negatives among e >= 3: %s" % (n, neg))
for t, l in worst: print('%.4f %s' % (t, l))
