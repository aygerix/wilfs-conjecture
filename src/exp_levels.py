"""Experiment E1: shifted Apery levels.
Identity to verify: ell = q*m - Lambda, Lambda = sum_{w in Ap} lambda(w), lambda(w) = floor((w+rho)/m).
Hence Wilf <=> (d+1)*Lambda <= d*q*m + rho, d = e-1.
Also list near-equality semigroups (W <= 1)."""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from collections import Counter, defaultdict

G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
nearW = defaultdict(list)
ratio_max = 0
for g, s in all_by_genus(G):
    if s.m == 1:
        continue
    ap = s.apery()
    lam = [s.level(w) for w in ap]
    Lam = sum(lam)
    q, m, rho, d = s.q, s.m, s.rho, s.e - 1
    assert s.ell == q * m - Lam
    assert max(lam) == q
    assert ((d + 1) * Lam <= d * q * m + rho) == (s.W >= 0)
    if s.W <= 1:
        nearW[s.W].append((s.m, s.e, s.c, s.q, s.rho, tuple(s.P)))
for W in sorted(nearW):
    L = nearW[W]
    print(f'W={W}: {len(L)} semigroups (genus<= {G})')
    # classify
    cls = Counter()
    for (m, e, c, q, rho, P) in L:
        if e == 2:
            cls['e=2'] += 1
        elif c <= m:
            cls['c<=m'] += 1
        else:
            cls[(f'q={q}', f'e={e}', f'm={m}')] += 1
    for k, v in sorted(cls.items(), key=lambda kv: str(kv[0])):
        print('   ', k, v)
    if W == 0:
        for x in L:
            if x[1] > 2 and x[2] > x[0]:
                print('      W=0 nontrivial:', x)
