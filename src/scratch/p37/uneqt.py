r"""Inspect q = 5, height <= 3, level-1 S with U = 3A' + mN != T = <m, A> (lead, 2026-10-21).
For each such S: T \ U, E3 slack e*l_U - c_U, W(T), and the residues where sigma_s (max-length) > tau_s.
usage: python uneqt.py d m"""
import sys, itertools, heapq
d, m = int(sys.argv[1]), int(sys.argv[2])
def apery(mod, G):
    w = [None] * mod; w[0] = 0; h = [(0, 0)]; done = [False] * mod
    while h:
        v, s = heapq.heappop(h)
        if done[s]: continue
        done[s] = True
        for x in G:
            t = (v + x) % mod
            if w[t] is None or v + x < w[t]: w[t] = v + x; heapq.heappush(h, (v + x, t))
    return w
def lens(x, G, inS, memo):
    if x == 0: return {0}
    if x in memo: return memo[x]
    out = set()
    for g in G:
        if x - g >= 0 and inS(x - g):
            for L in lens(x - g, G, inS, memo): out.add(L + 1)
    memo[x] = out; return out
cnt = 0
for A in itertools.combinations(range(1, m), d):
    G = [m + a for a in A]
    w = apery(m, G)
    if any(x is None for x in w) or max(w) >= 6 * m or max(w) < 5 * m: continue
    W_ = set(w); inS = lambda x: x >= 0 and x >= w[x % m]
    memo = {}; L = [lens(w[s], G, inS, memo) for s in range(m)]
    if max(max(l) for l in L) > 3: continue
    r = max(range(m), key=lambda s: w[s]); e = d + 1
    sig = [w[s] - m * max(L[s]) for s in range(m)]
    tau = apery(m, list(A))
    if sig == tau: continue
    cnt += 1
    c = w[r] - m + 1; g = sum(x // m for x in w); W = e * (c - g) - c
    cU = max(sig) - m + 1; gU = sum(x // m for x in sig); lU = cU - gU
    cT = max(tau) - m + 1; gT = sum(x // m for x in tau); lT = cT - gT
    TminusU = sorted(t + k * m for t_, (t, sg) in enumerate(zip(tau, sig)) for k in range((sg - t) // m))
    bad = [(s, sig[s], tau[s]) for s in range(m) if sig[s] != tau[s]]
    print("S=<%d,%s> r=%d W=%d | U: c=%d l=%d e*l-c=%d | T: c=%d l=%d | T\\U=%s | (s, sigma, tau)=%s" % (m, ",".join(map(str, G)), r, W, cU, lU, e * lU - cU, cT, lT, TminusU, bad))
print("count", cnt)
