r"""RT, its large-q slope lead and K_inf (rtasym.py) on the project's adversarial families (lead, 2026-10-20):
Fromentin's five W_0 = -1 semigroups, <30,44,48,49>_118, the E343 (B) counterexample (h = 3 regular, E = -56), the E340 T1
counterexamples, Backelin <213,216,226,227>, and Delgado's S(p) = <mu, gamma, gamma+1>_{p mu} with negative Eliahou number
E = |L||P cap L| + q|P cap [c, c+m)| - c  (mu <= MU, p <= PMAX).  <A>_c means <A> u [c, oo).
usage: /usr/bin/python3 rtfam.py MU PMAX"""
import sys
sys.path.insert(0, '.')
from rtasym import asym
from kunz_face import apery
def trunc(A, c):
    m = min(A); G = list(A) + list(range(c, c + m)); w = apery(m, G); return G
def eliahou(G):
    m = min(G); w = apery(m, G); Ws = set(w); c = max(w) - m + 1; q = -(-c // m)
    gens = [w[s] for s in range(1, m) if not any(w[s] - w[i] in Ws and 0 < w[s] - w[i] for i in range(1, m) if w[i] < w[s])]
    P = [m] + gens; L = sum(1 for x in range(c) if x >= w[x % m])
    return L * sum(1 for p in P if p < c) + q * sum(1 for p in P if c <= p < c + m) - c
fam = [('Fromentin', [14, 22, 23], 56), ('Fromentin', [16, 25, 26], 64), ('Fromentin', [17, 26, 28], 68),
       ('Fromentin', [17, 27, 28], 68), ('Fromentin', [18, 28, 29], 72), ('q5', [30, 44, 48, 49], 118),
       ('E343-B', [798, 1205, 1206, 1209, 1218, 1237, 1276, 1329], 3192),
       ('T1cex', [66, 67, 71, 72, 98, 103, 128], None), ('T1cex', [61, 62, 63, 67, 88, 89, 112], None),
       ('T1cex', [64, 65, 69, 75, 95, 100], None), ('Backelin', [213, 216, 226, 227], None)]
for name, A, c in fam:
    G = trunc(A, c) if c else A
    R = asym(G); R['G'] = A; R['E'] = eliahou(G); print(name, R, flush=True)
MU, PMAX = int(sys.argv[1]), int(sys.argv[2]); worst = []
for mu in range(5, MU + 1):
    for gam in range(mu + 1, 2 * mu):
        for p in range(3, PMAX + 1):
            if gam + 1 >= p * mu: continue
            G = trunc([mu, gam, gam + 1], p * mu); E = eliahou(G)
            if E >= 0: continue
            R = asym(G); R['G'] = [mu, gam, gam + 1, p * mu]; R['E'] = E; worst.append(R)
            if R['RT'] < 0: print("NEGATIVE RT", R, flush=True)
print("Delgado with E < 0: %d" % len(worst))
for R in sorted(worst, key=lambda R: R['RT'])[:6]: print("  minRT", R)
for R in sorted(worst, key=lambda R: R['RT'] / R['q'])[:4]: print("  minRT/q", R)
