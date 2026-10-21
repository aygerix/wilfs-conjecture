r"""BASE family test (lead, 2026-10-21).  If S has graded height <= 3, all pairs, all generators HIGH with mu_g = (2q+1)/3,
every pair relation tau = +1 and every cubic mu_z = 0, then W(S) = FAKE3(a) = (q-1)T - qm + rho + e^2 exactly (T = C(d+3,3)),
so Wilf for S is the packing inequality qm <= (q-1)T + e^2 + rho.  Scan: dense covers, all unit rescalings, all levels K in
{1..L}^d; report S meeting the hypotheses (any q, including q = 4 where depth-4 Wilf applies) and the closest ones.
usage: /usr/bin/python3 basefam.py L NCOV FILE [FILE ..]"""
import sys, re, itertools, math
sys.path.insert(0, '.')
from rt2lib import data
from math import comb
L, NC = int(sys.argv[1]), int(sys.argv[2]); hits = 0; tested = 0; near = []
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
            for K in itertools.product(range(1, L + 1), repeat=d):
                G = [m] + [m * k + x for k, x in zip(K, s)]
                D = data(G); w = D['w']; e, q, rho, mu, rp, T = D['e'], D['q'], D['rho'], D['mu'], D['rp'], D['tight']
                if e != d + 1 or D['c'] <= 3 * m: continue
                gens = set(D['gens']); hg = [0] * m; hn = [0] * m
                for x in sorted(range(1, m), key=lambda t: w[t]):
                    if x in gens: hg[x] = hn[x] = 1
                    else:
                        hg[x] = max(hg[i] + hg[j] for (i, j, t) in T if t == x); hn[x] = min(hn[i] + hn[j] for (i, j, t) in T if t == x)
                if not (max(hg) <= 3 and hg == hn) or sum(1 for x in range(1, m) if hg[x] == 2) != comb(d + 1, 2): continue
                tested += 1
                tau = lambda i, j, z: mu[i] + mu[j] - mu[z] - q
                viol = sum(1 for g in gens if rp[g] <= rho) + sum(1 for g in gens if 3 * mu[g] != 2 * q + 1)
                viol += sum(1 for (i, j, z) in T if hg[z] == 2 and tau(i, j, z) != 1) + sum(1 for z in range(1, m) if hg[z] == 3 and mu[z] != 0)
                base = (q - 1) * comb(d + 3, 3) - q * m + rho + e * e
                if viol == 0:
                    hits += 1; assert D['W'] == base, (G, D['W'], base)
                    print("BASE-FAMILY S", sorted(G), "q=%d rho=%d W=%d = BASE" % (q, rho, D['W']), flush=True)
                near.append((viol, D['W'] - base, sorted(G), q, rho, D['W']))
print("graded full-pair height-3 S tested %d, BASE-family hits %d" % (tested, hits))
for t in sorted(near)[:8]: print("closest (violations, W - BASE, G, q, rho, W):", t)
