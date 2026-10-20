r"""Per-degree split of the Carry Lemma on P18 depth four (lead, 2026-10-20). usage: cl4b.py k mlo mhi
U_unc = U2 + U3 + U4 (unused power tokens with uncarried first coordinate, by degree); T_c = p + q.
Tests: A: p+q <= U2+U4 ; B: p+q <= U3+U4 ; C: q <= U4 ; D: p <= U2+U3 ; E: p <= U3 ; F: q <= U4 + U2"""
import sys, itertools
from carry import analyse
k, mlo, mhi = map(int, sys.argv[1:4]); n = 0
tests = {"A": lambda U, p, q: U[2] + U[4] - p - q, "B": lambda U, p, q: U[3] + U[4] - p - q, "C": lambda U, p, q: U[4] - q,
         "D": lambda U, p, q: U[2] + U[3] - p, "E": lambda U, p, q: U[3] - p, "F": lambda U, p, q: U[4] + U[2] - q,
         "G": lambda U, p, q: U[2] - p, "H": lambda U, p, q: U[3] + U[4] - q}
st = {t: [0, 10**9, None] for t in tests}
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(1, m), k):
        r = analyse([m] + [m + b for b in B])
        if r is None or r["q"] != 4 or r["h"] <= r["e"]: continue
        n += 1; U = {d: r["Ud"].get(d, 0) for d in (2, 3, 4)}; p = r["ncar"].get(2, 0); q = r["ncar"].get(3, 0)
        for t, f in tests.items():
            v = f(U, p, q)
            if v < 0: st[t][0] += 1
            if v < st[t][1]: st[t][1] = v; st[t][2] = (r["gens"], r["h"], U, p, q)
print(sys.argv[1:], "S (h>e)", n)
for t in tests: print(" ", t, "fails", st[t][0], "min", st[t][1], st[t][2])
