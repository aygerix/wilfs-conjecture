r"""Necessity audit of the LAYER3 surplus at P18 depth four (lead, 2026-10-20).
Exact: W = Q3 + Q4, Q4 = k*L3 - 4*d4 (k = e - 1), and from the LAYER3 proof
  Q3 = sigT + 3*(Pw - p) + 2*(Pu - u2) + Pw,   sigT = k*u2 + 2*Pu - 3|T| >= 0.
For every subset X of the four components, test W - sum(X) >= 0 (i.e. is X dispensable?).  Also reports, on S with
Q4 < 0, the share of each component.  usage: exh k mlo mhi | rnd k mlo mhi N seed | list m b1 b2 ..."""
import sys, itertools, random, heapq
NAMES = ("sigT", "Pwp3", "Puu2", "Pw")
def comps(m, B):
    B = sorted(B); k = len(B)
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1
    if not (3 * m < c <= 4 * m): return None
    h = c - 3 * m; lv = [x // m for x in w]
    pairs = [B[i] + B[j] for i in range(k) for j in range(i, k)]
    Pu = sum(1 for s in pairs if s < m); Pw = len(pairs) - Pu
    u2 = sum(1 for r in range(m) if lv[r] == 2)          # in P18 every level-2 residue is an unwrapped pair sum
    n3 = [r for r in range(m) if lv[r] == 3]
    S2 = set(r for r in range(m) if lv[r] <= 2)
    T = [r for r in n3 if any(r - b in S2 and lv[r - b] == 2 and r - b >= 0 for b in B) or False]
    # carried pairs: level-3 residues r with r + m a pair sum and r not an unwrapped triple
    trip = set(B[i] + B[j] + B[l] for i in range(k) for j in range(i, k) for l in range(j, k))
    Tset = set(r for r in n3 if r in trip); p = len(n3) - len(Tset)
    sigT = k * u2 + 2 * Pu - 3 * len(Tset)
    L3 = sum(1 for r in range(h) if lv[r] <= 3); d4 = sum(1 for r in range(m) if lv[r] == 4)
    e = k + 1; W = e * (c - sum(lv)) - c
    Q3 = sigT + 3 * (Pw - p) + 2 * (Pu - u2) + Pw; Q4 = k * L3 - 4 * d4
    assert W == Q3 + Q4, (m, B, W, Q3, Q4)
    assert sigT >= 0 and Pw >= p and Pu >= u2
    return dict(m=m, B=tuple(B), e=e, h=h, W=W, Q3=Q3, Q4=Q4, sigT=sigT, Pwp3=3 * (Pw - p), Puu2=2 * (Pu - u2), Pw=Pw, L3=L3, d4=d4, p=p)
SUBS = [X for r in range(1, 5) for X in itertools.combinations(NAMES, r)]
if __name__ == "__main__":
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
    elif sys.argv[1] == "rnd":
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        gen = ((m, sorted(random.sample(range(1, m), k))) for m in (random.randint(mlo, mhi) for _ in range(N)))
    else:
        gen = [(int(sys.argv[2]), list(map(int, sys.argv[3:])))]
    n = nneg = 0; fails = {X: 0 for X in SUBS}; worst = {}; share = {x: 0 for x in NAMES}
    for m, B in gen:
        d = comps(m, B)
        if not d: continue
        n += 1
        if sys.argv[1] == "list": print(d)
        if d["Q4"] < 0:
            nneg += 1
            for x in NAMES: share[x] += d[x] / d["Q3"] if d["Q3"] else 0
        for X in SUBS:
            v = d["W"] - sum(d[x] for x in X)
            if v < 0:
                fails[X] += 1
                if X not in worst or v < worst[X][0]: worst[X] = (v, d)
    print(sys.argv[1:], "S:", n, "with Q4<0:", nneg, "mean Q3 share on Q4<0:", {x: round(share[x] / max(nneg, 1), 3) for x in NAMES})
    for X in SUBS:
        print("  drop", "+".join(X), ": failures", fails[X], ("worst " + str(worst[X][0]) + " " + str({y: worst[X][1][y] for y in ("m", "B", "h", "W", "Q3", "Q4", "sigT", "Pwp3", "Puu2", "Pw")})) if X in worst else "")
