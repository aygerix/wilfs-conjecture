r"""Identity CH-lambda (2026-10-17).  D = down-set of chosen factorizations (graded-lex-min) of Ap over
P' = P \ {m} (|D| = m), lambda(w) = floor((w+rho)/m) (shifted level), delta = q - lambda (depth),
kappa_a(n) = lambda(n+e_a) - lambda(n) - lambda(e_a) in {-1,0,1}  (carry; = floor((r(n)+r_a-rho)/m),
r(x) = (x+rho) mod m), kappa(n) = lambda(n) - sum_a n_a lambda(e_a).
   W = sum_a sum_{columns C} |C| delta(top C)  +  rho  +  K  -  sum_{n in D} kappa(n),
   K = sum_a sum_{n : n+e_a in D} (n_a + 1) kappa_a(n).
"""
import sys
sys.path.insert(0, 'src')
from ns import NS, all_by_genus
from exp_offsets import shortest_facts


def carry_data(s, D_choice='gl'):
    m, q, rho = s.m, s.q, s.rho
    Pp, best = shortest_facts(s)          # graded-lex-min factorizations (down-set)
    d = len(Pp)
    lam = lambda w: (w + rho) // m
    val = {}                               # exponent vector -> value
    for w, n in best.items():
        val[n] = w
    lam_e = [lam(p) for p in Pp]
    A1 = 0
    K = 0
    for a in range(d):
        for n, w in val.items():
            up = list(n); up[a] += 1; up = tuple(up)
            if up in val:
                kap = lam(val[up]) - lam(w) - lam_e[a]
                assert kap in (-1, 0, 1)
                K += (n[a] + 1) * kap
            else:                           # n is a column top; column length n_a + 1
                A1 += (n[a] + 1) * (q - lam(w))
    sumkappa = sum(lam(w) - sum(n[a] * lam_e[a] for a in range(d)) for n, w in val.items())
    return dict(A1=A1, rho=rho, K=K, sumkappa=sumkappa)


if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    n = 0; bad_strong = 0; ex = []
    for g, s in all_by_genus(G):
        if s.m == 1:
            continue
        cd = carry_data(s)
        assert s.W == cd['A1'] + cd['rho'] + cd['K'] - cd['sumkappa'], (s, cd)
        n += 1
        if cd['sumkappa'] - cd['K'] > cd['rho']:
            bad_strong += 1
            if len(ex) < 8: ex.append((s.P, s.c, s.q, s.rho, s.W, cd))
    print(f'Identity CH-lambda verified on {n} semigroups (genus<={G}).')
    print(f'Strong carry claim  sum kappa - K <= rho  fails in {bad_strong}')
    for x in ex: print('  ', x)
