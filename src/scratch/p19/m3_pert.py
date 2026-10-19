"""CHAIN-M3 test (lead, 2026-10-19): is CHAIN (B_chain >= need) true whenever M >= 3*n1 (n1 = least generator > m)?
M < 3*n1 forces Apery height <= 2 (an element whose factorizations all have length >= 3 is >= 3*n1 > M), where Wilf is
LEAN-proved (Flat-MaxCL).  Families: interval cores <m, km+a..km+b> (k = 1, 2) plus one extra generator x in (m, 4m).
Reports CHAIN failures split by the class M >= 3 n1, and by Apery height.
usage: python m3_pert.py mlo mhi"""
import sys
sys.path.insert(0, '../p18')
from chain_interval import apery
def stats(m, gens_in):
    w = apery(m, [m] + gens_in)
    if any(x is None for x in w): return None
    ap = set(w); M = max(w); c = M - m + 1; q = -(-c//m)
    gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
    d = len(gens)
    if d < 2: return None
    Bc = 0
    for g in gens:
        for x in w:
            t = x
            while t + g in ap: t += g
            Bc += M - t
    need = (d - 1)*m*(m - 1)//2
    # least factorization length over Apery elements (increasing order DP)
    ml = {0: 0}
    for x in sorted(w)[1:]:
        ml[x] = min(1 + ml[x - g] for g in gens if x - g in ml)
    H = max(ml.values())
    return dict(ratio=Bc/need, M=M, n1=gens[0], e=d+1, q=q, H=H, c=c, gens=gens)
if __name__ == '__main__':
    mlo, mhi = int(sys.argv[1]), int(sys.argv[2])
    cnt = {}; fails = []; best3 = None
    for m in range(mlo, mhi + 1):
        for k in (1, 2):
            for a in range(1, m):
                for b in range(a + 1, m):
                    core = list(range(k*m + a, k*m + b + 1))
                    for x in [None] + list(range(m + 1, 4*m)):
                        if x is not None and x in core: continue
                        r = stats(m, core + ([x] if x else []))
                        if not r or r['q'] < 2: continue
                        cl = r['M'] >= 3*r['n1']
                        key = (cl, r['H'] >= 3)
                        cnt[key] = cnt.get(key, 0) + 1
                        if cl and (best3 is None or r['ratio'] < best3[0]): best3 = (round(r['ratio'], 4), m, k, a, b, x, r['e'], r['q'], r['H'])
                        if r['ratio'] < 1: fails.append((cl, r['H'], round(r['ratio'], 4), m, k, a, b, x, r['e'], r['q'], r['M'], r['n1']))
    print('counts (M>=3n1, H>=3):', cnt)
    f3 = [f for f in fails if f[0]]
    print('CHAIN failures total', len(fails), ' with M >= 3 n1:', len(f3))
    for f in f3[:20]: print('  M3FAIL', f)
    print('min ratio with M >= 3 n1:', best3)
