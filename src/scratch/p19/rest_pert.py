"""REST on class A = {M >= 3 n1} in structured families, by m (lead, 2026-10-19).
Families: interval cores <m, km+a..km+b> (k = 1, 2, 3) plus one extra generator x in (m, 4m) (x = None allowed).
For each m prints the max REST/C2 over class-A members, with the example: is sup REST/C2 drifting toward 0 as m grows?
usage: python rest_pert.py mlo mhi"""
import sys
sys.path.insert(0, '../p18')
from chain_interval import apery
def rest_stats(m, gens_in):
    w = apery(m, [m] + gens_in)
    if any(x is None for x in w): return None
    ap = set(w); M = max(w); c = M - m + 1
    gens = sorted(x for x in w if x > 0 and not any(w[j] + w[(x - w[j]) % m] == x for j in range(1, m) if (x - w[j]) % m))
    d = len(gens)
    if d < 2 or M < 3*gens[0]: return None
    rest = 0; Bc = 0
    for g in gens:
        for x in w:
            t = x
            while t + g in ap: t += g
            Bc += M - t
            if x: rest += (M - x) % m - (M - t)
    C2 = m*(m-1)//2
    return rest/C2, Bc/((d-1)*C2), d+1, -(-c//m)
if __name__ == '__main__':
    mlo, mhi = int(sys.argv[1]), int(sys.argv[2])
    for m in range(mlo, mhi + 1):
        best = None; n = 0
        for k in (1, 2, 3):
            for a in range(1, m):
                for b in range(a, m):
                    core = list(range(k*m + a, k*m + b + 1))
                    for x in [None] + list(range(m + 1, 4*m)):
                        if x is not None and x in core: continue
                        r = rest_stats(m, core + ([x] if x else []))
                        if not r: continue
                        n += 1
                        if best is None or r[0] > best[0]: best = (round(r[0], 4), round(r[1], 4), r[2], r[3], k, a, b, x)
        print('m=%d classA=%d max REST/C2=%s' % (m, n, best), flush=True)
