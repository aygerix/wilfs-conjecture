# U != T extremal family check: A = {1} u {3d, 3d+2, 3d+5, ..., 3d+2+3(d-3)}, m = 6d-4 (independent of trunc3n)
from itertools import combinations_with_replacement as cwr
def stats(A, m):
    A0 = [0] + list(A); S3 = set(sum(t) for t in cwr(A0, 3))
    sig = {}
    for v in sorted(S3):
        sig.setdefault(v % m, v)
    if len(sig) < m: return None
    M = max(sig.values()); c = max(M - m + 1, 0)
    U = lambda x: x >= sig[x % m]
    l = sum(1 for x in range(c) if U(x))
    # T = <A, m> membership by DP up to c + m
    N = c + 2 * m; inT = [False] * N; inT[0] = True
    for x in range(1, N): inT[x] = any(x >= g and inT[x - g] for g in list(A) + [m])
    ne = any(inT[x] and not U(x) for x in range(N))
    return c, l, ne
for d in range(4, 16):
    A = [1, 3 * d] + [3 * d + 2 + 3 * i for i in range(d - 2)]
    m = 6 * d - 4
    r = stats(A, m)
    if r is None: print(d, 'not covering', A, m); continue
    c, l, ne = r; e = d + 1
    print(f"d={d} m={m} A={A} c={c} l={l} U!=T={ne} e*l={e*l} ratio={e*l/c:.4f} 4(d+1)/(3d)={4*(d+1)/(3*d):.4f}")
