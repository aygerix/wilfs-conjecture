# level profile: H_J, Macaulay slacks M_J = (e-1)H_J - (J+1)(H_{J+1}-H_J), prefix sums Phi_J, and M_top
import sys
def prof(gens):
    m = min(gens); B = 8000
    inS = [False] * B; inS[0] = True
    for n in range(1, B): inS[n] = any(n >= g and inS[n - g] for g in gens)
    c = max(n for n in range(B - 300) if not inS[n]) + 1
    mins = [n for n in range(1, c + m) if inS[n] and not any(inS[a] and inS[n - a] for a in range(1, n // 2 + 1))]
    e = len(mins); q = -(-c // m); h = c - (q - 1) * m
    H = [sum(1 for z in range(j * m, (j + 1) * m) if inS[z]) for j in range(q + 1)]
    x = sum(1 for z in range((q - 1) * m, c) if inS[z]); nq = h - x
    M = [(e - 1) * H[J] - (J + 1) * (H[J + 1] - H[J]) for J in range(q - 1)]
    Mtop = (e - 1) * x - q * nq
    ell = sum(1 for z in range(c) if inS[z]); W = e * ell - c
    print(mins, "m", m, "c", c, "e", e, "q", q, "h", h, "W", W)
    print("  H  ", H)
    print("  M_J", M, " M_top", Mtop, " sum", sum(M) + Mtop)
    ph = 0; P = []
    for v in M: ph += v; P.append(ph)
    print("  Phi", P)
for gs in [[46, 72, 73, 76], [14, 22, 23], [39, 59, 61, 64, 68]]: prof(gs)
