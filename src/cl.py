r"""Carry Lemma CL (conjecture, 2026-10-17).
D = down-set of chosen factorizations of Ap(S,m) over P' = P \ {m} (graded-lex-min by default; any
monomial order gives a down-set), M = max Ap.  For each direction a, D splits into columns (maximal
segments n, n+e_a, ...).  r'(x) = (M - x) mod m.
   CL:  sum_a sum_{columns C} |C| * r'(top C)  >=  (d-1) m (m-1)/2.
Exact identity:  m W = m * sum_a sum_C |C| depth(top C) + [sum_a sum_C |C| r'(top C) - (d-1)m(m-1)/2],
so CL => Wilf (and CL => TOP'')."""
import sys
sys.path.insert(0, 'src')
from ns import NS, all_by_genus


def factorizations_down_set(s, order='grlex', perm=None):
    m = s.m
    Pp = [p for p in s.P if p != m]
    if perm is not None:
        Pp = [Pp[i] for i in perm]
    d = len(Pp)
    ap = sorted(s.apery()); apset = set(ap)
    best = {0: tuple([0] * d)}
    for w in ap[1:]:
        cands = []
        for a, p in enumerate(Pp):
            if (w - p) in apset:
                v = list(best[w - p]); v[a] += 1; v = tuple(v)
                key = (sum(v), v) if order == 'grlex' else (v,) if order == 'lex' else (tuple(-x for x in v),)
                cands.append((key, v))
        best[w] = min(cands)[1]
    return Pp, best


def cl_value(s, order='grlex', perm=None):
    m = s.m
    Pp, best = factorizations_down_set(s, order, perm)
    d = len(Pp)
    val = {n: w for w, n in best.items()}
    assert len(val) == m
    M = max(val.values())
    lhs = 0
    depth_part = 0
    for a in range(d):
        for n, w in val.items():
            up = list(n); up[a] += 1
            if tuple(up) not in val:          # column top, column length n_a + 1
                lhs += (n[a] + 1) * ((M - w) % m)
                depth_part += (n[a] + 1) * ((M - w) // m)
    target = (d - 1) * m * (m - 1) // 2
    return lhs, target, depth_part


if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    orders = sys.argv[2].split(',') if len(sys.argv) > 2 else ['grlex']
    n = 0; fails = {o: 0 for o in orders}; ex = []; tight = 0
    for g, s in all_by_genus(G):
        if s.m == 1:
            continue
        n += 1
        for o in orders:
            lhs, target, dp = cl_value(s, o)
            assert s.m * s.W == s.m * dp + lhs - target, (s, o)
            if lhs < target:
                fails[o] += 1
                if len(ex) < 8: ex.append((o, s.P, s.c, s.W, lhs, target))
            elif lhs == target and o == orders[0]:
                tight += 1
    print(f'genus<={G}: {n} semigroups; CL failures by order {fails}; tight(first order) {tight}')
    for x in ex: print('  ', x)
