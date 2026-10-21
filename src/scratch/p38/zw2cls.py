# zw2cls: per-class form of ZW2 (Delta3 + e z >= 2m):  sum_s phi(s) >= 0 with
#   phi = 4e-5 (level 0), 3e-5 (level 1), 2e-5 (level 2, sigma<m), e-5 (level 2 large or level 3 small), -5 (level 3 large).
# Counts S2, L2, S3, L3; charging test CH: every large level-3 class y takes 5/3 per unit of parent weight from its
# standard square parents x = y - e_i; a parent's budget is phi(x) + (credit of its unused slots: P(x)... reported).
import sys
from itertools import combinations_with_replacement as cwr
def analyse(m, A):
    d = len(A); e = d + 1; best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k, c)
            if cl not in best or key < best[cl]: best[cl] = key
    vec = lambda c: tuple(sum(1 for t in c if t == i) for i in range(d))
    rep = {cl: vec(best[cl][2]) for cl in best}; h = {cl: sum(rep[cl]) for cl in best}; sg = {cl: best[cl][0] - h[cl] * m for cl in best}
    D = {rep[cl]: cl for cl in best}
    cnt = {}
    for cl in range(m):
        key = (h[cl], sg[cl] >= m); cnt[key] = cnt.get(key, 0) + 1
    S2, L2, S3, L3 = cnt.get((2, False), 0), cnt.get((2, True), 0), cnt.get((3, False), 0), cnt.get((3, True), 0)
    phi = (4 * e - 5) + (e - 1) * (3 * e - 5) + (2 * e - 5) * S2 + (e - 5) * (L2 + S3) - 5 * L3
    z = sum(1 for s in range(m) if sg[s] < m); D3 = 3 * (e - 1) * m - e * sum(h.values())
    assert phi == D3 + e * z - 2 * m, (m, A)
    # parents of large cubes: how much out-weight goes from small squares vs large squares into large cubes
    wS = wL = 0
    for x, cl in D.items():
        if sum(x) != 3 or sg[cl] < m: continue
        for i in range(d):
            if x[i]:
                p = tuple(x[j] - (j == i) for j in range(d)); pc = D[p]
                if sg[pc] < m: wS += x[i]
                else: wL += x[i]
    return dict(e=e, S2=S2, L2=L2, S3=S3, L3=L3, phi=phi, wS=wS, wL=wL, D3=D3)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['m'] = int(t[1]); r['A'] = list(map(int, t[15:])); rows.append(r)
e = rows[0]['e']; v = min(rows, key=lambda r: r['phi'])
print(f"{sys.argv[1]}: {len(rows)} S, e = {e}; min ZW2 = {v['phi']} at m={v['m']} A={v['A']} S2={v['S2']} L2={v['L2']} S3={v['S3']} L3={v['L3']}")
avg = lambda k: round(sum(r[k] for r in rows) / len(rows), 1)
print('  means:', {k: avg(k) for k in ('S2', 'L2', 'S3', 'L3', 'wS', 'wL')})
w = max(rows, key=lambda r: r['L3'] / max(1, r['S2'] + r['L2']))
print(f"  max L3/(S2+L2) = {w['L3'] / max(1, w['S2'] + w['L2']):.2f} at m={w['m']} A={w['A']} (S2={w['S2']} L2={w['L2']} S3={w['S3']} L3={w['L3']} phi={w['phi']})")
w = max(rows, key=lambda r: r['wL'] / max(1, r['wS'] + r['wL']))
print(f"  max share of large-cube parent weight from LARGE squares = {w['wL'] / max(1, w['wS'] + w['wL']):.2f} at m={w['m']} A={w['A']}")
