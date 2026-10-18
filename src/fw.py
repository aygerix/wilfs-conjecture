"""Final-window (FW) criterion for Wilf, all embedding dimensions (2026-10-18 night 17).
Generalizes kseth/wilf-e4 eq. (p:6) from d = 3 to every d = e - 1 (same proof; derivation in NOTEBOOK night 17):
  T = term-order factorization ideal of Ap(S,m) over P' = P \\ {m} (down-set in N^d, |T| = m, lambda(x) = a.x bijective
  onto Ap), lines = maximal segments of T in a coordinate direction, P(T) = #lines = sum_j |pi_j T|,
  Z = {x in T : lambda(x) >= c} (= tau-set, all maximal), E(Z) = sum_Z |z|_1 - sum_j max_Z z_j.
  EXACT:  m W = C(m,2) + sum_lines sigma_l,   sigma_l = L(M - lambda(top)) - sum_{x in l} [M - lambda(x)]_m.
  FW:     m W >= m (P(T) - d|Z|) - (m-1) E(Z).      So P(T) - d|Z| >= E(Z) => Wilf.
This script asserts EXACT and FW on every S of genus <= G and reports how often FW alone proves Wilf."""
import sys
from math import comb
sys.path.insert(0, 'src')
from ns import all_by_genus
from cl import factorizations_down_set
def fw(s, order='grlex'):
    m, c = s.m, s.c
    Pp, best = factorizations_down_set(s, order)
    d = len(Pp)
    if d == 0: return None
    T = set(best.values()); lam = {x: w for w, x in best.items()}
    M = max(lam.values()); W = (d + 1) * (c - s.g) - c
    tot = comb(m, 2); nlines = 0
    for j in range(d):
        for x in T:
            if tuple(x[i] + (i == j) for i in range(d)) in T: continue   # x is a line top in direction j
            L = x[j] + 1; nlines += 1
            pts = [tuple(x[i] - (r if i == j else 0) for i in range(d)) for r in range(L)]
            tot += L * (M - lam[x]) - sum((M - lam[p]) % m for p in pts)
    assert tot == m * W, (s.P, tot, m * W)
    Z = [x for x in T if lam[x] >= c]
    E = sum(sum(z) for z in Z) - sum(max(z[j] for z in Z) for j in range(d))
    bound = m * (nlines - d * len(Z)) - (m - 1) * E
    assert m * W >= bound, (s.P, m * W, bound)
    return dict(e=d + 1, m=m, W=W, P=nlines, tau=len(Z), E=E, bound=bound, deep=nlines - d * len(Z))
if __name__ == '__main__':
    G = int(sys.argv[1]); order = sys.argv[2] if len(sys.argv) > 2 else 'grlex'
    stat = {}; worst = {}; fails = []
    for g, s in all_by_genus(G):
            if g == 0: continue
            r = fw(s, order)
            if r is None: continue
            k = r['e']; st = stat.setdefault(k, [0, 0]); st[0] += 1
            if r['bound'] >= 0: st[1] += 1
            else:
                fails.append((s.P, r['m'], r['tau'], r['E'], r['deep'], r['bound']))
                key = r['bound'] / r['m']
                if k not in worst or key < worst[k][0]: worst[k] = (key, s.P, r)
    for k in sorted(stat):
        n, ok = stat[k]
        print(f'G<={G} {order} e={k}: {n} semigroups, FW proves Wilf for {ok} ({100*ok/n:.1f}%); worst bound/m', worst.get(k, (None,))[0], worst.get(k, (None, None))[1:2])
    print('failures (P, m, tau, E, deep, bound):', len(fails))
    for f in fails[:60]: print('  ', f)
