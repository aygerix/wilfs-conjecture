r"""Full-window realizability test (lead, 2026-10-21).  RT2-WINDOW (FAKE3(c)) needs every non-generator Apery cell in the
wrap window W_rho = positions [m - rho, m - 1].  Positions are r_s = (s + rho) mod m, so the cells OUTSIDE W_rho are the
residues r+1, ..., 2r+1 (positions 0..r), r = m - rho - 1 the conductor residue.  Full window <=> those r+1 residues
are minimal generators (r <= d - 1).  For each dense cover residue set s (Delta_3 covers Z/m) and each unit u, each
r in [1, d-1] with {r+1..2r+1} <= u*s and r not in u*s, generator levels K in {1..L}^d are enumerated; a lift counts
when e = d+1, the conductor residue is r and q >= 5 (c > 4m).  For each lift: graded height-3 flag, full-window flag,
RT2, RT3, UA2, UA3, W, and the FAKE3(c) value (q-2)Gcap + rho - 2m + e^2 + e (only meaningful under graded height 3).
usage: /usr/bin/python3 fullwin.py L NCOV FILE [FILE ..]"""
import sys, re, itertools, math
sys.path.insert(0, '.')
from rt2lib import data, relax
L, NC = int(sys.argv[1]), int(sys.argv[2])
best = {}; nconf = nlift = 0; cnt = {}
for fn in sys.argv[3:]:
    nc = 0
    for line in open(fn):
        mm = re.match(r'm=(\d+) d=(\d+) s=([0-9,]+)', line)
        if not mm: continue
        nc += 1
        if nc > NC: break
        m, d = int(mm.group(1)), int(mm.group(2)); s0 = [int(t) for t in mm.group(3).split(',')]
        seen = set()
        for u in range(1, m):
            if math.gcd(u, m) != 1: continue
            s = tuple(sorted(u * x % m for x in s0))
            if s in seen: continue
            seen.add(s)
            for r in range(1, d):
                if r in s or not all(x % m in s for x in range(r + 1, 2 * r + 2)): continue
                nconf += 1
                for K in itertools.product(range(1, L + 1), repeat=d):
                    G = [m] + [m * k + x for k, x in zip(K, s)]
                    D = data(G)
                    w = D['w']
                    if D['e'] != d + 1 or w.index(max(w)) != r or D['q'] < 5: continue
                    nlift += 1
                    m_, e, q, rho, rp = D['m'], D['e'], D['q'], D['rho'], D['rp']
                    nong = [x for x in range(1, m) if x not in D['gens']]
                    fw = all(rp[x] >= m - rho for x in nong)
                    R = relax(D, ('RT2', 'RT3', 'UA2', 'UA3'))
                    # graded height <= 3
                    hg = [0] * m; hn = [0] * m
                    for x in sorted(range(1, m), key=lambda t: w[t]):
                        if x in D['gens']: hg[x] = hn[x] = 1
                        else:
                            hg[x] = max(hg[i] + hg[j] for (i, j, t) in D['tight'] if t == x)
                            hn[x] = min(hn[i] + hn[j] for (i, j, t) in D['tight'] if t == x)
                    H = max(hg) <= 3 and hg == hn
                    P = sum(1 for x in range(1, m) if hg[x] == 2)
                    Gcap = e * (P + 2 * d + 3) / 3 - m; fake = (q - 2) * Gcap + rho - 2 * m + e * e + e
                    cnt[(H, fw)] = cnt.get((H, fw), 0) + 1
                    if H and fw: print("GRADED FULL-WINDOW", s, K, flush=True)
                    rec = dict(m=m, d=d, s=s, r=r, K=K, q=q, rho=rho, H=H, fw=fw, h=max(hg), W=D['W'], fake=round(fake, 2),
                               **{k: round(v, 3) for k, v in R.items()})
                    for key in ('RT2', 'RT3', 'UA3'):
                        kk = (m, d, key)
                        if kk not in best or rec[key] < best[kk][key]: best[kk] = rec
                    if R['RT2'] < -1e-9 or R['RT3'] < -1e-9: print("NEGATIVE", rec, flush=True)
    print("file %s (cumulative): configurations %d, lifts %d" % (fn, nconf, nlift), flush=True)
for kk in sorted(best): print("min", kk[2], best[kk], flush=True)
print("lifts by (graded height<=3, full window):", cnt, flush=True)
