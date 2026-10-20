"""Minimal-span B_h sets (all h-fold multiset sums distinct) by DFS, then CORE1 at depth q = h+1 for the densest
placement inside [m/(q-2), m/2) (lead, 2026-10-20). Usage: python b4span.py H KMAX"""
import itertools, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
src = open(__import__('os').path.join(__import__('os').path.dirname(__file__), "core1opt.py")).read().replace("main()\n", "")
ns = {}; exec(compile(src, "core1opt", "exec"), ns); core1 = ns["core1"]
H, KMAX = int(sys.argv[1]), int(sys.argv[2])

def is_bh(A):
    seen = set()
    for c in itertools.combinations_with_replacement(A, H):
        s = sum(c)
        if s in seen: return False
        seen.add(s)
    return True

def min_span(K):
    for L in range(K - 1, 10**6):
        # DFS over sets {0 = a0 < a1 < ... < a_{K-1} = L}
        def dfs(A):
            if len(A) == K - 1:
                B = A + [L]
                return B if is_bh(B) else None
            for x in range(A[-1] + 1, L - (K - 1 - len(A)) + 1):
                if is_bh(A + [x]):
                    r = dfs(A + [x])
                    if r: return r
            return None
        r = dfs([0])
        if r: return r

q = H + 1
for K in range(3, KMAX + 1):
    A = min_span(K); L = A[-1]
    nsum = len({sum(c) for c in itertools.combinations_with_replacement(A, H)})
    print("K=%d B_%d set %s span %d, %d sums in range %d (density %.3f)" % (K, H, A, L, nsum, H * L + 1, nsum / (H * L + 1)), flush=True)
    best = None
    for m in range(3 * L, 30 * L + 200):
        for a in range(m // (q - 2) + 1, (m - 1) // 2 - L + 1):
            O = [a + x for x in A]
            if 2 * O[-1] >= m: continue
            r = core1(m, 0, O, q)
            if r is None: continue
            if best is None or r[0] < best[0][0]: best = (r, m, O)
    print("   min CORE1 (W0+p, W0, p, ell, W) =", best, flush=True)
