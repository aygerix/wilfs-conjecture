"""Depth-q Eliahou-Fromentin analogue (lead, 2026-10-20): greedy offsets B in [m/(q-2), m/(q-3)) (q = 5: [m/3, m/2))
such that all sums of <= q-1 offsets are pairwise distinct mod m (B_{q-1}-type), rho = 0, T = <m, m+B> u [qm, inf).
Prints m, K, B and runs ./anchqx2 on it (ANCHOR-q parts) plus W0.
Usage: python sidonq.py q m K SEED"""
import itertools, random, subprocess, sys
q, m, K, seed = map(int, sys.argv[1:5])
rnd = random.Random(seed)
lo, hi = -(-m // (q - 2)), m // (q - 3) if q > 3 else m
cands = list(range(lo, hi)); rnd.shuffle(cands)
B = []
def ok(B):
    seen = set()
    for t in range(0, q):
        for comb in itertools.combinations_with_replacement(B, t):
            r = sum(comb) % m
            if r in seen: return False
            seen.add(r)
    return True
for b in cands:
    if len(B) >= K: break
    if ok(B + [b]): B.append(b)
B.sort()
print("q", q, "m", m, "K", len(B), "B", B, flush=True)
out = subprocess.run(["./anchqx2", str(q), str(m), "0", ",".join(map(str, B))], capture_output=True, text=True).stdout
print(out.strip())
# W0 directly
INF = 10**9; w = [INF] * m; w[0] = 0; ch = True
while ch:
    ch = False
    for r in range(m):
        if w[r] == INF: continue
        for b in B:
            v = w[r] + m + b; s = v % m
            if v < w[s]: w[s] = v; ch = True
lev = [x // m for x in w]
ell = sum(q - l for l in lev if l < q); d = sum(1 for l in lev if l <= q)
print("W0 =", (len(B) + 1) * ell - q * d, " p =", m - d, " true depth:", max(lev) >= q)
