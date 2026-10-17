r"""Conjecture TOP'' (2026-10-17).  S != N, m >= 2, P' = P \ {m}, d = |P'|, X_q = Ap(S,m) cap [c, c+m),
pi(u) = u - c + 1, ell(u) = min number of elements of P' summing to u.
   TOP'':  2 * sum_{u in X_q} pi(u) (d + ell(u)) <= m ((d+1) m + d - 1)
TOP'' => Wilf (chain identity CH; see PROOFS.md)."""
import sys
sys.path.insert(0, 'src')
from ns import NS, all_by_genus


def minlen_apery(s):
    """min factorization length over P' of each Apery element (all factorizations of Apery
    elements pass through Apery elements)."""
    m = s.m
    Pp = [p for p in s.P if p != m]
    ap = sorted(s.apery())
    apset = set(ap)
    ml = {0: 0}
    for w in ap[1:]:
        ml[w] = 1 + min(ml[w - p] for p in Pp if (w - p) in apset)
    return ml


def top2(s):
    m, c = s.m, s.c
    d = s.e - 1
    ml = minlen_apery(s)
    Xq = [w for w in s.apery() if w >= c]
    lhs2 = 2 * sum((u - c + 1) * (d + ml[u]) for u in Xq)
    rhs = m * ((d + 1) * m + d - 1)
    return lhs2, rhs


if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    n = f = 0
    ex = []
    tight = 0
    for g, s in all_by_genus(G):
        if s.m == 1:
            continue
        lhs2, rhs = top2(s)
        n += 1
        if lhs2 > rhs:
            f += 1
            if len(ex) < 10:
                ex.append((s.P, s.m, s.c, s.q, s.W, (lhs2 - rhs) / 2))
        elif lhs2 == rhs:
            tight += 1
    print(f"genus<={G}: {n} semigroups; TOP'' fails {f}; tight {tight}")
    for x in ex:
        print('  fail', x)
