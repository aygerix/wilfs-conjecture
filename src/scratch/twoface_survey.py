# Survey of two-face e = 4 semigroups: gluing axis, t (e_a + e_b == t e_c mod Lambda), face shapes, Wilf / TOP'' / MaxCL slack.
import sys, itertools, random, collections
from math import gcd
from functools import reduce
sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def info(s):
    m, c = s.m, s.c; P = s.P; d = len(P) - 1; p = P[1:]
    _, best = factorizations_down_set(s, 'grlex'); cells = {v: k for k, v in best.items()}
    D = set(cells)
    faces = [(a, b) for a in range(d) for b in range(a + 1, d) if tuple(int(i in (a, b)) for i in range(d)) not in D]
    if not faces: return None
    a, b = faces[0]; cax = 3 - a - b
    q = tuple(int(i in (a, b)) for i in range(d))
    w = (sum(qi*pi for qi, pi in zip(q, p))) % m
    z = [x for x in D if sum(xi*pi for xi, pi in zip(x, p)) % m == w][0]
    t = z[cax]; assert all(z[i] == 0 for i in range(d) if i != cax)
    L3 = max(x[cax] for x in D) + 1
    F1 = [x for x in D if x[b] == 0]; F2 = [x for x in D if x[a] == 0]
    h1 = max(x[a] for x in D) + 1; h2 = max(x[b] for x in D) + 1
    box1 = len(F1) == h1*L3; box2 = len(F2) == h2*L3
    # MaxCL at sigma = c, TOP''
    A = [x for x in D if all(x[:i] + (x[i] + 1,) + x[i+1:] not in D for i in range(d))]
    r = {x: (cells[x] - c) % m for x in D}
    lhs = sum((d + sum(y))*r[y] for y in A); rhs = (d + 1)*m*(m - 1)//2
    Xq = [u for u in s.apery() if c <= u < c + m]
    top = sum((u - c + 1)*(d + sum(best[u])) for u in Xq); trhs = m*((d + 1)*m + d - 1)//2
    W = s.W if isinstance(s.W, int) else s.W()
    return dict(P=tuple(P), m=m, cax=cax, rank=sorted(p).index(p[cax]), t=t, L3=L3, h=(h1, h2), boxes=(box1, box2),
                nf=len(faces), W=W, Wm=W/m, top=(trhs - top)/trhs, maxcl=(rhs - lhs)/rhs, tau=len(Xq), q=s.q)
if __name__ == '__main__':
    m0, m1, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    R = []
    for m in range(m0, m1 + 1):
        for g3 in itertools.combinations(range(m + 1, K*m), 3):
            if reduce(gcd, (m,) + g3) != 1: continue
            s = NS.from_generators([m, *g3])
            if s.e != 4: continue
            r = info(s)
            if r: R.append(r)
    print('two-face e=4 count', len(R))
    cnt = collections.Counter((r['rank'], r['t']) for r in R); print('(rank of glue gen, t):', sorted(cnt.items()))
    print('nfaces:', collections.Counter(r['nf'] for r in R))
    print('boxes (F1,F2):', collections.Counter(r['boxes'] for r in R))
    for key in ('Wm', 'top', 'maxcl'):
        print(f'--- smallest {key} (m >= 12)')
        for r in sorted([r for r in R if r['m'] >= 12], key=lambda r: r[key])[:8]:
            print('  ', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
    print('MaxCL failures:', sum(r['maxcl'] < 0 for r in R), ' TOP fails', sum(r['top'] < 0 for r in R))
    by = collections.defaultdict(list)
    for r in R: by[r['t']].append(r)
    for t in sorted(by): print('t =', t, 'n', len(by[t]), 'min Wm', round(min(r['Wm'] for r in by[t]), 3), 'min top', round(min(r['top'] for r in by[t]), 3), 'min maxcl', round(min(r['maxcl'] for r in by[t]), 3))
