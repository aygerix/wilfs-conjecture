# Lambda-criterion: Lam := sum over (cell x, direction a) of lamL(t_a x), lamL(t) = ceil((c - w(t))/m)^+ = #left elements
# in the class of w(t).  Exact: W = Lam + d m - P/m - (d-1)(m-1)/2, P = sum pos(t_a x).  Wilf <= Lam >= (d-1)(m-1)/2.
import sys, itertools, random
from math import gcd
from functools import reduce
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS, all_by_genus
from cl import factorizations_down_set
def lam(s):
    m, c = s.m, s.c; d = s.e - 1
    _, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}
    S = set(cells); L = P = 0
    for x in cells:
        for a in range(d):
            t = x
            while True:
                y = t[:a] + (t[a] + 1,) + t[a+1:]
                if y in S: t = y
                else: break
            w = cells[t]; L += max(0, -(-(c - w)//m)); P += ((w - c) % m) + 1
    assert m*s.W == m*L + d*m*m - P - (d - 1)*m*(m - 1)//2
    return L, P, m, d
if __name__ == '__main__':
    mode = sys.argv[1]; res = []
    if mode == 'genus':
        for g, s in all_by_genus(int(sys.argv[2])):
            if g and s.e >= 3: res.append((s.P, s.e) + lam(s))
    elif mode == 'box':
        m0, m1, K = map(int, sys.argv[2:5])
        for m in range(m0, m1 + 1):
            for a, b, cc in itertools.combinations(range(m + 1, K*m), 3):
                if gcd(gcd(m, a), gcd(b, cc)) != 1: continue
                s = NS.from_generators([m, a, b, cc])
                if s.e == 4: res.append((s.P, 4) + lam(s))
    for e in sorted(set(r[1] for r in res)):
        R = [r for r in res if r[1] == e]
        F = [r for r in R if r[2] < (r[5] - 1)*(r[4] - 1)/2]
        ms = sorted(set(r[4] for r in F))
        print(f'e={e}: n={len(R)} Lambda-criterion fails {len(F)}; failing m values {ms[:12]}{"..." if len(ms)>12 else ""}; max failing m {max(ms) if ms else None}')
        for r in sorted(F, key=lambda r: -r[4])[:3]: print('    ', r[0], 'Lam', r[2], 'need', (r[5]-1)*(r[4]-1)/2, 'm', r[4])
