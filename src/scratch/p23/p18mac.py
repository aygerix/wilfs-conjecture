r"""P18 at depth four: truncated condensed-Macaulay accounting (lead, 2026-10-20).
S = <m, m+B>, A = {0} u B (integers in [0, m)).  jA = j-fold integer sumset.
Proved tools (Eliahou Thm 5.11 applied to k[C]/(x0, I_{>=L}), C = cone over {1} x A):
  (Ij_L)  j*|(jA \ (j-1)A) n [0,L)| <= |A n (0,L)| * |(j-1)A n [0,L)|.
Reports W and the pieces: E1 = e(e+1) - 2|2A|, E2 = a*|3A n [0,h)| - 4|(4A\3A) n [0,h)|, E3 = (e+2)|2A n [0,m+h)| - 3|3A n [0,m+h)|,
U1 = |3A n [m, m+h)|, U2 = |3A n [m+h, 3m)|, Phi_lo = |2A n [m, m+h)|, Phi_hi = |2A n [m+h, 2m)|, and R = W - E1 - E2 - E3 + U1."""
import sys, itertools, random

def sumset(X, Y):
    return sorted(set(x + y for x in X for y in Y))

def analyze(m, B):
    A = [0] + sorted(B)
    gens = [m] + [m + b for b in B]
    # Apery set by Dijkstra
    import heapq
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for b in B:
            v = d0 + m + b; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    M = max(w); c = M - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; e = len(B) + 1; g = sum(x // m for x in w); ell = c - g; W = e * ell - c
    a = sum(1 for b in B if b < h)
    A2 = set(sumset(A, A)); A3 = set(sumset(A2, A)); A4 = set(sumset(A3, A))
    E1 = e * (e + 1) - 2 * len(A2)
    x3h = sum(1 for s in A3 if s < h); n4nc = sum(1 for s in A4 if s < h and s not in A3)
    E2 = a * x3h - 4 * n4nc
    L = m + h
    E3 = (e + 2) * sum(1 for s in A2 if s < L) - 3 * sum(1 for s in A3 if s < L)
    U1 = sum(1 for s in A3 if m <= s < m + h); U2 = sum(1 for s in A3 if s >= m + h)
    Plo = sum(1 for s in A2 if m <= s < m + h); Phi = sum(1 for s in A2 if s >= m + h)
    R = W - E1 - E2 - E3 + U1
    # chain bound pieces (PROVED: W >= E1+E2+E3-U1 + b*y0 - Phi - (e-4)*delta + 4*nu)
    b_ = e - 1 - a; y0 = x3h
    C2lo = set((s - m) for s in A2 if m <= s < m + h) - A3
    delta = Plo - len(C2lo)
    nu = sum(1 for s in A4 if s < h and s not in A3 and s in C2lo)
    chain = E1 + E2 + E3 - U1 + b_ * y0 - Phi - (e - 4) * delta + 4 * nu
    if chain > W: print("CHAIN BOUND VIOLATED", m, B, W, chain); raise SystemExit
    lhs = U1 + Phi + (e - 4) * delta; rhs = E1 + E2 + E3 + b_ * y0 + 4 * nu
    return dict(m=m, B=tuple(B), h=h, e=e, a=a, W=W, E1=E1, E2=E2, E3=E3, U1=U1, U2=U2, Plo=Plo, Phi=Phi, R=R, y0=y0, delta=delta, nu=nu, slackC=rhs - lhs)

if __name__ == "__main__":
    mode = sys.argv[1]
    recs = []
    if mode == "exh":
        k = int(sys.argv[2]); mlo, mhi = int(sys.argv[3]), int(sys.argv[4])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                from math import gcd
                gg = m
                for b in B: gg = gcd(gg, b)
                if gg != 1: continue
                r = analyze(m, B)
                if r: recs.append(r)
    elif mode == "rnd":
        k = int(sys.argv[2]); mlo, mhi = int(sys.argv[3]), int(sys.argv[4]); N = int(sys.argv[5]); random.seed(int(sys.argv[6]))
        from math import gcd
        for _ in range(N):
            m = random.randint(mlo, mhi)
            sty = random.random()
            if sty < 0.4: B = random.sample(range(1, m), k)
            else:
                h0 = random.randint(m // 4, m - 1)
                B = sorted(set(random.randint(max(1, h0 // 2 - 2), max(2, (2 * h0) // 3 + 2)) for _ in range(k)))
                if len(B) < 2: continue
            gg = m
            for b in B: gg = gcd(gg, b)
            if gg != 1: continue
            r = analyze(m, sorted(B))
            if r: recs.append(r)
    print(len(recs), "depth-four P18 S")
    for key in ["E1", "E2", "E3", "R"]:
        mn = min(recs, key=lambda r: r[key]); print("min", key, mn[key], mn)
    # is R >= 0 always?  and R vs carried pairs / U2
    bad = [r for r in recs if r["R"] < 0]
    print("R<0:", len(bad))
    for r in bad[:10]: print("  ", r)
    # correlation: R - 3*U2
    mn = min(recs, key=lambda r: r["R"] - 3 * r["U2"]); print("min R-3U2", mn["R"] - 3 * mn["U2"], mn)
    mn = min(recs, key=lambda r: r["slackC"]); print("CHAIN-CONJ min slack", mn["slackC"], "neg:", sum(1 for r in recs if r["slackC"] < 0), mn)
    for name, f in [("E2-U1", lambda r: r["E2"] - r["U1"]), ("E1+E2-U1", lambda r: r["E1"] + r["E2"] - r["U1"]), ("E2+E3-U1", lambda r: r["E2"] + r["E3"] - r["U1"]),
                    ("E1+E2+E3-U1", lambda r: r["E1"] + r["E2"] + r["E3"] - r["U1"])]:
        vals = [f(r) for r in recs]; nneg = sum(1 for v in vals if v < 0); mn = min(recs, key=f)
        print(name, "neg:", nneg, "min:", f(mn), mn)
