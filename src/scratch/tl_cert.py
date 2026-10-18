# Independent check of a TL failure: own semigroup arithmetic, brute-force grlex factorizations,
# LP via scipy, then an EXACT dual certificate (Fractions): weights beta on cells, sum beta = 1, with
# sum_u (l(u)-1) * min_{splits {x,y} of n(u)} (beta_x + beta_y) > d+1  =>  L* > d+1 by weak duality.
import sys, itertools
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
gens = list(map(int, sys.argv[1].split(',')))
N = 40 * max(gens) ** 2 // min(gens) + 10 * max(gens)
inS = [False] * N; inS[0] = True
for n in range(1, N):
    inS[n] = any(n >= g and inS[n - g] for g in gens)
gaps = [n for n in range(N) if not inS[n]]
c = max(gaps) + 1 if gaps else 0; g = len(gaps); m = min(gens)
assert all(inS[n] for n in range(c, N))
mingens = [p for p in range(1, c + m + 1) if inS[p] and not any(inS[a] and inS[p - a] for a in range(1, p))]
e = len(mingens); ell = c - g
ap = [min(n for n in range(i, N, m) if inS[n]) for i in range(m)]
Pp = [p for p in mingens if p != m]; d = len(Pp)
def facts(w):
    out = []
    def rec(a, rem, v):
        if a == d - 1:
            if rem % Pp[a] == 0: out.append(tuple(v + [rem // Pp[a]]))
            return
        for k in range(rem // Pp[a] + 1): rec(a + 1, rem - k * Pp[a], v + [k])
    rec(0, w, []); return out
best = {}
for w in ap:
    fs = facts(w); assert fs
    best[w] = min(fs, key=lambda v: (sum(v), v))
T = set(best.values()); assert len(T) == m
X = [best[w] for w in ap if w >= c]
X2 = [y for y in X if sum(y) >= 2]
print(f'S=<{",".join(map(str,mingens))}> m={m} e={e} c={c} g={g} ell={ell} W={e*ell-c} m|c={c%m==0} c>3m={c>3*m} |X|={len(X)} |X2|={len(X2)}')
cells = sorted({u for y in X2 for u in itertools.product(*[range(v + 1) for v in y]) if 0 < sum(u) < sum(y)})
assert all(z in T for z in cells)          # down-set
assert not any(z in set(X) for z in cells)  # split cells are non-X
zi = {z: i for i, z in enumerate(cells)}
splits = []
for k, y in enumerate(X2):
    S2 = set()
    for u in itertools.product(*[range(v + 1) for v in y]):
        v = tuple(a - b for a, b in zip(y, u))
        if 0 < sum(u) and 0 < sum(v): S2.add(tuple(sorted((u, v))))
    splits.append(sorted(S2))
cols = [(k, zi[u], zi[v]) for k in range(len(X2)) for (u, v) in splits[k]]
nv = len(cols) + 1
Aeq = np.zeros((len(X2), nv)); beq = np.array([sum(y) - 1 for y in X2], float)
Aub = np.zeros((len(cells), nv))
for j, (k, a, b) in enumerate(cols): Aeq[k, j] = 1; Aub[a, j] += 1; Aub[b, j] += 1
Aub[:, -1] = -1
cost = np.zeros(nv); cost[-1] = 1
r = linprog(cost, A_ub=Aub, b_ub=np.zeros(len(cells)), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * nv, method='highs-ds')
print('primal L* =', r.fun)
beta = -r.ineqlin.marginals  # >= 0, sums to 1
den = 10 ** 6
bq = [F(round(max(0.0, b) * den), den) for b in beta]
tot = sum(bq); bq = [b / tot for b in bq]
val = sum((sum(y) - 1) * min(bq[zi[u]] + bq[zi[v]] for (u, v) in splits[k]) for k, y in enumerate(X2))
print('exact dual bound L* >=', val, '=', float(val), ' d+1 =', d + 1, ' TL FAILS (certified)' if val > d + 1 else ' not certified')
if len(sys.argv) > 2:
    lam = {v: w for w, v in best.items()}
    pi = {v: (w - c) % m + 1 for w, v in best.items()}
    print('p =', Pp, ' p mod m =', [p % m for p in Pp])
    print('X (n(u), l, pi):', sorted(((y, sum(y), pi[y]) for y in X), key=lambda t: -t[2]))
    print('beta>0 cells (cell, beta, pi, kunz):', [(z, float(round(bq[zi[z]], 4)), pi[z], lam[z] // m) for z in cells if bq[zi[z]] > 0])
    # TOP'' slack, residue form
    lhs = sum(pi[y] * (d + sum(y)) for y in X); rhs = m * ((d + 1) * m + d - 1) // 2
    print("TOP'' LHS", lhs, 'RHS', rhs, 'slack', rhs - lhs, ' m*W =', m * (e * ell - c))
    # minimal wrap count over split choices: each u needs l(u)-1 units; nonwrap split iff kunz(x)+kunz(y) = q
    q = c // m; nw = {tuple(y): sum(1 for (u, v) in splits[k] if lam[u] // m + lam[v] // m == q) for k, y in enumerate(X2)}
    print('non-wrapping splits available per u (need l-1):', [(y, sum(y) - 1, nw[tuple(y)]) for y in X2])
