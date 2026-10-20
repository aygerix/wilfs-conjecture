"""Show the TM structure for one lex tile with relabelling (u, lambda) (lead, 2026-10-21).
Usage: python tmshow.py m u lam g1 g2 ..."""
import sys
sys.path.insert(0, '.')
from tile import build
m, u, lam = map(int, sys.argv[1:4]); G = list(map(int, sys.argv[4:]))
c, gens, M = build(m, G); N = len(gens)
up = lambda a, i: tuple(a[t] + (t == i) for t in range(N))
eps = {a: (u * x + lam) % m for a, x in M.items()}
mx = {a for a in M if all(up(a, i) not in M for i in range(N))}
print("m=%d c=%d gens=%s N=%d u=%d lam=%d" % (m, c, gens, N, u, lam))
for a in sorted(M, key=lambda a: -eps[a]):
    tag = "MAX w=%d" % (sum(a) + N) if a in mx else ""
    print("  eps=%2d %-20s phi=%4d %s" % (eps[a], a, M[a], tag))
lhs = sum((sum(a) + N) * eps[a] for a in mx); rhs = (N + 1) * m * (m - 1) // 2
print("LHS=%d RHS=%d ratio=%.4f" % (lhs, rhs, lhs / rhs))
f = []
for k in range(m):
    f.append(sum(sum(a) + N for a in mx if eps[a] >= k) - (N + 1) * (m - k))
print("f(k), k=0..m-1:", f, " sum =", sum(f), "(= LHS - RHS - (N+1)m?)")
