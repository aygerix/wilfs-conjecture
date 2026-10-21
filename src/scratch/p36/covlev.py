r"""All level vectors K in KSET^d on given covers (lead, 2026-10-20): S = <m, m K_b + s_b>; keeps e = d+1, c >= 4m+1;
reports RT (kunz_face relaxation, via h3rnd.analyse), W, rho, h, lead; prints any RT < 0 and the NK smallest RT.
usage: /usr/bin/python3 covlev.py FILE KSET NCOV [NK]"""
import sys, re, itertools
sys.path.insert(0, '.')
from h3rnd import analyse
f, KS, NC = sys.argv[1], [int(t) for t in sys.argv[2].split(',')], int(sys.argv[3])
NK = int(sys.argv[4]) if len(sys.argv) > 4 else 6
res = []; neg = 0; nc = 0
for line in open(f):
    mm = re.match(r'm=(\d+) d=(\d+) s=([0-9,]+)', line)
    if not mm: continue
    nc += 1
    if nc > NC: break
    m, d = int(mm.group(1)), int(mm.group(2)); s = [int(t) for t in mm.group(3).split(',')]
    for K in itertools.product(KS, repeat=d):
        R = analyse([m] + [m * k + x for k, x in zip(K, s)])
        if R['e'] != d + 1 or R['c'] < 4 * m + 1: continue
        R['s'] = s; R['K'] = K; res.append(R)
        if R['RT'] < -1e-9: neg += 1; print("NEGATIVE RT", R, flush=True)
print("%s: covers %d, S %d (e=d+1, c>4m), RT<0: %d" % (f, min(nc, NC), len(res), neg))
for R in sorted(res, key=lambda R: R['RT'])[:NK]:
    print("  ", {k: R[k] for k in ('m', 'e', 'c', 'q', 'rho', 'h', 'W', 'RT', 'lead', 's', 'K')})
