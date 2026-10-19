"""Decompose the CHAIN deficit of one semigroup given by its Apery set (lead): con(0), rest = sum_{w!=0} con(w),
per-layer sums, per-direction sums D_a (w != 0), counts of escape / stuck pairs.  usage: python chain_decomp.py m w0,w1,..."""
import sys
m = int(sys.argv[1]); w = [int(x) for x in sys.argv[2].strip(',').split(',')]
assert len(w) == m and w[0] == 0
ap = set(w); M = max(w); c = M - m + 1; C2 = m*(m - 1)//2
gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
d = len(gens); q = -(-c//m)
con = {}; lay = {}; Da = []; esc = stuck = mid = 0
for g in gens:
    da = 0
    for x in w:
        t = x
        while t + g in ap: t += g
        s = (M - x) % m; y = M - t; v = s - y
        con[x] = con.get(x, 0) + v
        if x: da += v
        lam = (M - x)//m
        if x and lam >= 1:
            if t == x: stuck += 1
            elif M - t < m: esc += 1
            else: mid += 1
    Da.append(da)
for x in w: lam = (M - x)//m; lay[lam] = lay.get(lam, 0) + (con[x] if x else 0)
rest = sum(con[x] for x in w if x)
print('m=%d e=%d c=%d q=%d 3e<m=%s  Delta/C2=%.4f  con(0)/C2=%.4f  rest/C2=%.4f  ratio=%.4f' % (m, d + 1, c, q, 3*(d + 1) < m, (con[0] + rest)/C2, con[0]/C2, rest/C2, (d*C2 - con[0] - rest)/((d - 1)*C2)))
print('layer sums (w!=0)/C2:', {k: round(v/C2, 4) for k, v in sorted(lay.items())})
print('per-direction D_a/C2 (w!=0):', [round(x/C2, 3) for x in Da])
print('left nonzero pairs: escape-to-L0 %d, stuck %d, intermediate %d' % (esc, stuck, mid))
print('gens:', gens)
