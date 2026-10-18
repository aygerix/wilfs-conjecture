"""Top-layer cross lemma and the tau-criterion for Wilf (2026-10-18).
X_q = Ap(S,m) ∩ [c, c+m),  tau = |X_q|,  y(u) = grlex-least (= a shortest) factorization of u over P' = P \\ {m}.
CROSS LEMMA (claimed):  sum_{u in X_q} (l(u) + 1) <= m + P2,   P2 = #{pairs {u,u'} : y(u), y(u') differ in exactly 2 coords}.
TAU-CRITERION (claimed): if d = e-1 >= 2 and m + 1 >= 2 tau + 2 P2/(d-1)  then TOP'' holds, hence Wilf (Lean: wilf_of_TOP2).
This script asserts every step on all semigroups of genus <= G (independent shortest-length DP for l(u))."""
import sys, itertools
sys.path.insert(0, 'src')
from ns import all_by_genus
from cl import factorizations_down_set
def check(s):
    m, c = s.m, s.c
    P = s.P; Pp = [p for p in P if p != m]; e = len(P); d = e - 1
    if d < 1: return None
    ap = sorted(s.apery())
    Xq = [u for u in ap if c <= u < c + m]
    _, best = factorizations_down_set(s, 'grlex')
    cells = set(best.values()); assert len(cells) == m
    # independent shortest factorization length over P'
    top = max(Xq)
    INF = 10**9; ml = [INF]*(top + 1); ml[0] = 0
    for x in range(1, top + 1):
        ml[x] = min([ml[x - p] + 1 for p in Pp if p <= x and ml[x - p] < INF] or [INF])
    Y = [best[u] for u in Xq]
    for u, y in zip(Xq, Y): assert sum(y) == ml[u], (s.P, u)
    cnt = {}
    for y in Y:
        cr = set()
        for a in range(d):
            for k in range(y[a] + 1):
                x = list(y); x[a] -= k; cr.add(tuple(x))
        assert len(cr) == sum(y) + 1 and cr <= cells
        for x in cr: cnt[x] = cnt.get(x, 0) + 1
    over = sum(v - 1 for v in cnt.values())
    P2 = sum(1 for y, z in itertools.combinations(Y, 2) if sum(1 for a in range(d) if y[a] != z[a]) == 2)
    assert over <= P2 and len(cnt) <= m
    lhs_cross = sum(sum(y) + 1 for y in Y); assert lhs_cross <= m + P2
    top2 = sum((u - c + 1)*(d + sum(y)) for u, y in zip(Xq, Y)) <= m*((d + 1)*m + d - 1)//2
    cond = d >= 2 and (d - 1)*(m + 1) >= 2*(d - 1)*len(Xq) + 2*P2
    if cond: assert top2, ('criterion holds but TOP2 fails', s.P)
    return e, len(Xq), cond, top2, s.t()
if __name__ == '__main__':
    G = int(sys.argv[1]); from collections import Counter
    tot = Counter(); n = 0
    for g, s in all_by_genus(G):
        if g == 0: continue
        r = check(s)
        if r is None: continue
        e, tau, cond, top2, t = r; n += 1
        tot['S'] += 1; tot['cond'] += cond; tot['TOP2'] += top2
        if cond and t >= e: tot['cond & t>=e (outside FGH)'] += 1
        if cond and e == 4: tot['cond & e=4'] += 1
        if e == 4: tot['e=4'] += 1
    print(f'genus <= {G}:', dict(tot))
