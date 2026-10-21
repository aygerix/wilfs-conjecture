r"""RT and W on genuine S built from the near-perfect height-3 covers of nearcov.c (lead, 2026-10-20):
S = <m, m K_b + s_b> with levels K_b drawn from KLIST (all equal levels first, then NR random level vectors per cover).
Prints the S with the smallest RT among those with e = d+1 and c >= 4m+1, and the count with RT < 0.
usage: /usr/bin/python3 covfam.py FILE KLIST NR SEED"""
import sys, random, re
sys.path.insert(0, '.')
from h3rnd import analyse
f, KL, NR, seed = sys.argv[1], [int(t) for t in sys.argv[2].split(',')], int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed); res = []; neg = 0
for line in open(f):
    mm = re.match(r'm=(\d+) d=(\d+) s=([0-9,]+)', line)
    if not mm: continue
    m, d = int(mm.group(1)), int(mm.group(2)); s = [int(t) for t in mm.group(3).split(',')]
    levs = [[k] * d for k in KL] + [[rng.choice(KL) for _ in range(d)] for _ in range(NR)]
    for K in levs:
        R = analyse([m] + [m * k + x for k, x in zip(K, s)])
        if R['e'] != d + 1 or R['c'] < 4 * m + 1: continue
        R['s'] = s; R['K'] = K; res.append(R)
        if R['RT'] < -1e-9: neg += 1; print("NEGATIVE RT", R, flush=True)
print("%s: %d S (e=d+1, c>4m), RT<0: %d" % (f, len(res), neg))
for R in sorted(res, key=lambda R: R['RT'])[:5]: print("  ", {k: R[k] for k in ('m', 'e', 'c', 'q', 'rho', 'h', 'W', 'RT', 'lead', 's', 'K')})
