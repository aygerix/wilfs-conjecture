r"""Split certificates on near-B_3 postage-stamp residues with MIXED lifts (lead, 2026-10-20).  For each residue set A
(mod m), try every lift vector in {1..KMAX}^d (or NS random ones), S = <m, k_i m + a_i>; report NOCERT counts split by
'one window' (max g - min g < m) versus 'spread'.  Usage: /usr/bin/python3 splitmix.py KMAX NS m:a1,a2,.. ..."""
import sys, random, io, contextlib, itertools
sys.path.insert(0, '.')
from splitlp import cert
from tile import build
KMAX, NS = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(3)
for spec in sys.argv[3:]:
    m, A = spec.split(':'); m = int(m); A = [int(t) for t in A.split(',')]; d = len(A)
    allk = list(itertools.product(range(1, KMAX + 1), repeat=d))
    ks = allk if len(allk) <= NS else rnd.sample(allk, NS)
    tab = {}; ex = {}
    for k in ks:
        G = [m] + [ki * m + a for ki, a in zip(k, A)]
        res = build(m, G)
        if res is None or res[0] <= 0: continue
        gens = res[1]; onew = max(gens) - min(gens) < m
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): T = cert(G, False, "", "-unit" in sys.argv)
        key = ('onewin' if onew else 'spread', 'NOCERT' if T < -1e-9 else 'CERT', len(gens))
        tab[key] = tab.get(key, 0) + 1
        if T < -1e-9 and not onew and key not in ex: ex[key] = buf.getvalue().strip() + ' gens=%s' % gens
    print(spec, sorted(tab.items()), flush=True)
    for k, v in ex.items(): print('  spread NOCERT example:', v, flush=True)
