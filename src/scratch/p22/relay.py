# RELAY test (lead, 2026-10-20). At the true shift, K(x) = q - lambda(x) - sum_a nu_a(x)(lambda(x-n_a)-lambda(x)).
# Deficits: x with K(x) >= 2 (capacity K-1). Credits: decomposable y with K(y) <= 0 (capacity 1-K).
# Variant COVER: y = x - n_a for some a with nu_a(x) >= 1.  Variant BELOW: y <_S x (x - y in S), y decomposable.
# Reports S where max flow < total deficit, for each variant.
import sys
sys.path.insert(0, '.')
from t1an import semigroup
def maxflow_bip(left, right, edges):
    # left: dict node->cap, right: dict node->cap, edges: dict left->list right. Simple augmenting paths with capacities.
    flow_r = {r: 0 for r in right}; assign = {}  # (l, r) -> units
    total = 0
    for l, cap in left.items():
        for _ in range(cap):
            # find augmenting path from l: BFS over alternating structure (unit capacities expanded)
            seen = set(); parent = {}
            stack = [('L', l)]; found = None
            while stack and found is None:
                side, u = stack.pop()
                if side == 'L':
                    for r in edges.get(u, []):
                        if r in seen: continue
                        seen.add(r); parent[r] = u
                        if flow_r[r] < right[r]: found = r; break
                        for (l2, r2), k in assign.items():
                            if r2 == r and k > 0 and ('L', l2) not in seen:
                                seen.add(('L', l2)); parent[('L', l2)] = r; stack.append(('L', l2))
            if found is None: return total
            r = found; flow_r[r] += 1
            u = parent[r]
            while True:
                assign[(u, r)] = assign.get((u, r), 0) + 1
                if u == l: break
                r_prev = parent[('L', u)]
                assign[(u, r_prev)] -= 1
                r = r_prev; u = parent[r]
            total += 1
    return total
def run_p(gens):
    gens = sorted(gens); m = gens[0]; N = m * max(gens) * 2 + 10
    S = semigroup(gens, N)
    Ap = [next(x for x in range(i, N, m) if S[x]) for i in range(m)]
    P = [g for g in gens[1:] if not any(S[g - h] and g - h > 0 for h in gens if h < g)]
    M = max(Ap); c = M - m + 1; q = -(-c // m)
    lam = lambda v: (M - v) // m
    def nu(a, x):
        k = 0
        while x - (k + 1) * a >= 0 and S[x - (k + 1) * a]: k += 1
        return k
    K = {}
    for x in Ap:
        K[x] = q - lam(x) - sum(nu(a, x) * (lam(x - a) - lam(x)) for a in P if nu(a, x) > 0)
    dec = [x for x in Ap if x and x not in P]
    deficit = {x: K[x] - 1 for x in dec if K[x] >= 2}
    credit = {y: 1 - K[y] for y in dec if K[y] <= 0}
    tot = sum(deficit.values())
    cov = {x: [x - a for a in P if nu(a, x) > 0 and (x - a) in credit] for x in deficit}
    bel = {x: [y for y in credit if y < x and S[x - y]] for x in deficit}
    f1 = maxflow_bip(deficit, credit, cov); f2 = maxflow_bip(deficit, credit, bel)
    return tot, f1, f2, sum(credit.values())
def run_all(gens):
    gens = sorted(gens); m = gens[0]; N = m * max(gens) * 2 + 10
    S = semigroup(gens, N)
    Ap = [next(x for x in range(i, N, m) if S[x]) for i in range(m)]
    P = [g for g in gens[1:] if not any(S[g - h] and g - h > 0 for h in gens if h < g)]
    def nu(a, x):
        k = 0
        while x - (k + 1) * a >= 0 and S[x - (k + 1) * a]: k += 1
        return k
    NU = {(a, x): nu(a, x) for a in P for x in Ap}
    cnt = lambda u, v, p: (v - p) // m - (u - p) // m
    dec = [x for x in Ap if x and x not in P]
    worst = []
    for p in range(1, m + 1):
        K = {x: cnt(0, x, p) - sum(NU[(a, x)] * cnt(x - a, x, p) for a in P) for x in Ap}
        deficit = {x: K[x] - 1 for x in dec if K[x] >= 2}
        if not deficit: continue
        credit = {y: 1 - K[y] for y in dec if K[y] <= 0}
        tot = sum(deficit.values())
        bel = {x: [y for y in credit if y < x and S[x - y]] for x in deficit}
        f2 = maxflow_bip(deficit, credit, bel)
        if f2 < tot: worst.append((p, tot, f2))
    return worst

if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "all":
    n = 0; bad = 0
    for line in open(sys.argv[1]):
        if not line.startswith('K2 '): continue
        gens = [int(t) for t in line[3:].strip().split(',')]
        w = run_all(gens); n += 1
        if w:
            bad += 1
            if bad <= 8: print("BELOW(all p) fails", gens, w[:3])
    print("tested", n, "S; BELOW failures at some shift:", bad)
elif __name__ == "__main__":
    n = 0; bad1 = bad2 = 0
    for line in open(sys.argv[1]):
        if not line.startswith('K2 '): continue
        gens = [int(t) for t in line[3:].strip().split(',')]
        tot, f1, f2, cr = run_p(gens); n += 1
        if f1 < tot:
            bad1 += 1
            if bad1 <= 5: print("COVER fails", gens, "deficit", tot, "flow", f1, "credit", cr)
        if f2 < tot:
            bad2 += 1
            if bad2 <= 5: print("BELOW fails", gens, "deficit", tot, "flow", f2, "credit", cr)
    print("tested", n, "COVER failures", bad1, "BELOW failures", bad2)
