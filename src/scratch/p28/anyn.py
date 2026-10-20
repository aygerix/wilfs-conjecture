r"""Order-level identity w.r.t. ANY minimal generator n (lead, 2026-10-20).  For n in the minimal generating set,
Ap(S,n) has n elements; level_n(w) = w // n; ord(w) = max # minimal generators in a representation (n never used).
H_j = #{w in Ap(S,n): ord = j} = Hilbert function of gr(R / t^n R) (standard graded, H_1 = e - 1).
c = (q-1) n + h.  Identity:  W = sum_{k=1}^{q-1} E_k + (e-1) h - sum_{j>=q} H_j (e j - (e-1)(q-1)) - e T_c,
T_c = sum (level - ord) (may be NEGATIVE when generators below n exist).
usage: python3 anyn.py gens...   or   python3 anyn.py rnd k mlo mhi N seed  (P18 depth four samples)"""
import sys, random, heapq
def semigroup(gens):
    m = min(gens)
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in gens:
            if x == m: continue
            v = d0 + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    F = c + max(gens) + 5
    S = [False] * F; S[0] = True
    for x in range(1, F):
        S[x] = any(x >= g and S[x - g] for g in gens)
    mingens = [x for x in sorted(set(gens)) if not any(S[x - y] and y <= x - 1 and S[y] for y in range(1, x) if y in set(range(1, x)))]
    # simpler: x minimal iff x not sum of two nonzero elements
    mingens = [x for x in sorted(set(gens)) if not any(S[y] and S[x - y] for y in range(1, x))]
    return c, S, mingens
def analyse_n(c, S, gens, n):
    e = len(gens); F = len(S)
    def inS(x): return x >= c or (0 <= x < F and S[x])
    ap = []
    for r in range(n):
        x = r
        while not inS(x): x += n
        ap.append(x)
    aps = set(ap)
    order = {0: 0}
    for v in sorted(ap)[1:]:
        order[v] = max(order[v - g] + 1 for g in gens if g != n and v - g >= 0 and (v - g) in aps)
    g = sum(1 for x in range(c) if not inS(x))
    q = -(-c // n); h = c - (q - 1) * n
    H = {}
    for v in ap: H[order[v]] = H.get(order[v], 0) + 1
    Tc = sum(v // n - order[v] for v in ap)
    Hl = lambda j: H.get(j, 0)
    E = lambda k: (e - 1) * sum(Hl(i) for i in range(k)) - k * Hl(k)
    W = e * (c - g) - c
    pen = sum(Hl(j) * (e * j - (e - 1) * (q - 1)) for j in H if j >= q)
    F2 = sum(E(k) for k in range(1, q)) + (e - 1) * h - pen - e * Tc
    return dict(n=n, q=q, h=h, Tc=Tc, sumE=sum(E(k) for k in range(1, q)), pen=pen, W=W, ok=(W == F2), maxord=max(H))
if __name__ == "__main__":
    if sys.argv[1] != "rnd":
        gens = list(map(int, sys.argv[1:])); c, S, mg = semigroup(gens)
        print("c", c, "mingens", mg)
        for n in mg: print(analyse_n(c, S, mg, n))
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed); cnt = 0; bad = 0; negbest = 0; zero = 0
        for _ in range(N):
            m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k)); gens = [m] + [m + b for b in B]
            r = semigroup(gens)
            if r is None: continue
            c, S, mg = r
            if not (3 * m < c <= 4 * m): continue
            res = [analyse_n(c, S, mg, n) for n in mg]
            cnt += 1; bad += sum(1 for x in res if not x["ok"])
            best = min(res, key=lambda x: x["Tc"])
            if best["Tc"] < 0: negbest += 1
            if best["Tc"] <= 0: zero += 1
        print("S", cnt, "identity failures", bad, "some generator with Tc<0:", negbest, "with Tc<=0:", zero)
