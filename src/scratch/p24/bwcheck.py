# independent check of BANDWILF Phi_J for given generators (pure python, membership by DP)
import sys
def check(gens):
    m = min(gens); B = 5000
    inS = [False] * B; inS[0] = True
    for n in range(1, B):
        inS[n] = any(n >= g and inS[n - g] for g in gens)
    c = max(n for n in range(B - 200) if not inS[n]) + 1
    # minimal generators
    mins = [n for n in range(1, c + m) if inS[n] and not any(inS[a] and inS[n - a] for a in range(1, n) if a <= n - a)]
    e = len(mins); q = -(-c // m)
    H = [sum(1 for z in range(j * m, (j + 1) * m) if inS[z]) for j in range(q + 1)]
    out = []
    for J in range(1, q + 1):
        phi = e * sum(H[:J]) - J * H[J]; out.append((J, phi))
    ell = sum(1 for z in range(c) if inS[z]); W = e * ell - c
    return dict(m=m, c=c, e=e, q=q, gens=mins, W=W, H=H, phi=out)
for gs in [[14, 22, 23], [27, 68, 70]]:
    r = check(gs); print(r["gens"], "m", r["m"], "c", r["c"], "e", r["e"], "q", r["q"], "W", r["W"]); print("  H", r["H"]); print("  Phi", r["phi"])
print("--- e>=4 BANDWILF candidates")
for gs in [[46, 72, 73, 76], [56, 85, 89, 92], [48, 74, 77, 79]]:
    r = check(gs); bad = [(J, p) for J, p in r["phi"] if p < 0]
    print(r["gens"], "m", r["m"], "c", r["c"], "e", r["e"], "q", r["q"], "W", r["W"], "negative Phi:", bad)
def gbw2(gens):
    m = min(gens); B = 6000
    inS = [False] * B; inS[0] = True
    for n in range(1, B): inS[n] = any(n >= g and inS[n - g] for g in gens)
    c = max(n for n in range(B - 300) if not inS[n]) + 1
    mins = [n for n in range(1, c + m) if inS[n] and not any(inS[a] and inS[n - a] for a in range(1, n // 2 + 1))]
    e = len(mins); worst = None
    for N in range(0, c + 1):
        lhs = e * sum(1 for z in range(N) if inS[z]); rhs = sum(z // m for z in range(N, N + m) if inS[z])
        if worst is None or lhs - rhs < worst[0]: worst = (lhs - rhs, N, lhs, rhs)
    return mins, c, e, worst
print("--- GBW'' candidate")
print(gbw2([39, 59, 61, 64, 68]))
