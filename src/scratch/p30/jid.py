r"""Carry identity at P18 depth four (lead, 2026-10-20).
S = <m, m+B>, |B| = k, depth four, h = c - 3m.  T = new unwrapped triples (level 3, order 3); CP = carried pairs
(level 3, order 2), p = |CP|, p_lo = |CP n [0,h)|; C = carried triples (level 4, order 3), q = |C|; H4 = order-4.
Incidence pool: (s, b) with s in U2 u (m + CP_lo), b in B, k(d2 + p_lo) of them; repeat-deficit pool: ordered pairs
(x, z), x != z, and two copies of each singleton x: k(k+1) entries.  Each t in T u C (value t or m + r) uses
|P(t)| incidences of one chosen representation (distinct summands when possible) and 3 - |P(t)| deficit entries.
  slA = k(d2 + p_lo) + k(k+1) - 3(|T| + q) >= 0,   slB = k(y - p_lo) - 4 H4 >= 0,   d2el = C(k+1,2) - d2 - p >= 0.
IDENTITY: W = 2 d2el - p - q + slA + slB.   Wilf <=> p + q <= 2 d2el + slA + slB.
Also splits slA = incU (unused U2-incidences) + incC (unused CP-incidences) + defU (unused deficit entries).
usage: exh k mlo mhi | rnd k mlo mhi N seed | list m b1 b2 ..."""
import sys, itertools, random, heapq
def info(m, B):
    B = sorted(B); k = len(B); e = k + 1
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
    h = c - 3 * m
    lv = [w[r] // m for r in range(m)]
    inB = set(B)
    ps = {}  # pair sum value -> list of (x, y)
    for i in range(k):
        for j in range(i, k): ps.setdefault(B[i] + B[j], []).append((B[i], B[j]))
    ts = {}
    for i in range(k):
        for j in range(i, k):
            for l in range(j, k): ts.setdefault(B[i] + B[j] + B[l], []).append((B[i], B[j], B[l]))
    S2 = set([0]) | inB | set(s for s in ps if s < m)
    U2 = set(s for s in ps if s < m and s not in inB)
    T = set(t for t in ts if t < m and t not in S2)
    CP = set(s - m for s in ps if s >= m and (s - m) not in S2 and (s - m) not in T)
    q4s = set(v - m for v in ts if m <= v < m + h and lv[v - m] == 4)
    C = set(r for r in q4s if r not in set(t for t in ts if t < m))  # level 4, order 3 (no 4-rep: else order 4)
    # order-4 residues: level 4 and in 4B (< m)
    fs = set()
    for t in ts:
        if t < m:
            for x in B:
                if t + x < m: fs.add(t + x)
    H4set = set(r for r in range(h) if lv[r] == 4 and r in fs)
    C = set(r for r in range(h) if lv[r] == 4 and r not in fs)
    assert all((r + m) in ts for r in C)
    d2 = len(U2); p = len(CP); q = len(C); H4 = len(H4set)
    assert sum(1 for r in range(m) if lv[r] == 3) == len(T) + p and sum(1 for r in range(m) if lv[r] == 4) == H4 + q
    plo = sum(1 for u in CP if u < h)
    y = sum(1 for r in range(h) if lv[r] <= 3)
    usedI = set(); usedD = set()
    for val in list(T) + [m + r for r in C]:
        reps = ts[val]
        dist = [t for t in reps if t[0] < t[1] < t[2]]
        rep = dist[0] if dist else reps[0]
        x, yy, z = rep
        if x < yy < z:
            for (s, b) in ((x + yy, z), (x + z, yy), (yy + z, x)): usedI.add((s, b))
        elif x == yy == z:
            usedI.add((2 * x, x)); usedD.add((x, x, 0)); usedD.add((x, x, 1))
        else:
            a2 = x if x == yy else z; o1 = z if x == yy else x
            usedI.add((2 * a2, o1)); usedI.add((a2 + o1, a2)); usedD.add((a2, o1, 0))
    for (s, b) in usedI:
        assert (s < m and s in U2) or (s >= m and (s - m) in CP and s - m < h), (m, B, s, b)
    incU = k * d2 - sum(1 for (s, b) in usedI if s < m)
    incC = k * plo - sum(1 for (s, b) in usedI if s >= m)
    defU = k * (k + 1) - len(usedD)
    slA = k * (d2 + plo) + k * (k + 1) - 3 * (len(T) + q)
    assert slA == incU + incC + defU, (slA, incU, incC, defU)
    slB = k * (y - plo) - 4 * H4
    d2el = k * (k + 1) // 2 - d2 - p
    # self-payments: (i) carried pair u = x + y - m (x <= y, some rep) with u + y >= h owns the unused entry (y, x);
    # (ii) carried triple with some rep having a pair sum s < h owns the unused wrapped token (s, third) in slB.
    ni = 0
    for u in CP:
        if any(u + yy >= h for (x, yy) in ps[u + m]): ni += 1
    nii = 0; qbig = []
    for r in C:
        if any(min(a + b2, a + c2, b2 + c2) < h for (a, b2, c2) in ts[r + m]): nii += 1
        else: qbig.append(r)
    pres = p - ni; qres = q - nii
    # overshoot incidences: pool incidences (s, b) with s + b >= m + h (all unused)
    pool = list(U2) + [m + u for u in CP if u < h]
    Nover = sum(1 for s0 in pool for b in B if s0 + b >= m + h)
    # swap incidences of residual triples: (y+z, z) for a rep x<=y<=z with x<z; count distinct ones that are unused
    usedset = usedI
    swapU = set()
    for r0 in qbig:
        for (a1, b1, c1) in ts[r0 + m]:
            if a1 < c1 and (b1 + c1, c1) not in usedset: swapU.add((b1 + c1, c1))
    qQbig = sum(1 for r in qbig if any(a + b2 >= m or a + c2 >= m or b2 + c2 >= m for (a, b2, c2) in ts[r + m]))
    g = sum(lv); W = e * (c - g) - c
    assert W == 2 * d2el - p - q + slA + slB, (m, B, W)
    assert slB >= 0 and d2el >= 0 and incU >= 0 and incC >= 0
    return dict(m=m, B=tuple(B), e=e, h=h, W=W, p=p, plo=plo, q=q, H4=H4, d2el=d2el, slA=slA, incU=incU, incC=incC,
                defU=defU, slB=slB, y=y, d2=d2, T=len(T), ni=ni, nii=nii, pres=pres, qres=qres, qQbig=qQbig, Nover=Nover, swapU=len(swapU),
                a=sum(1 for b in B if b < h))
def _main():
    recs = []
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = info(m, B)
                if r: recs.append(r)
    elif sys.argv[1] == "rnd":
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
            r = info(m, B)
            if r: recs.append(r)
    else:
        m = int(sys.argv[2]); B = list(map(int, sys.argv[3:])); r = info(m, B); print(r); return
    print(sys.argv[1:], "depth-four S:", len(recs), "(identity asserted on all)")
    cands = {"K1: slA+slB-p-q (no pair redundancy)": lambda r: r["slA"] + r["slB"] - r["p"] - r["q"],
             "K2: 2d2el+defU+slB-p-q (no unused incidences)": lambda r: 2 * r["d2el"] + r["defU"] + r["slB"] - r["p"] - r["q"],
             "K3: 2d2el+incU+incC+slB-p-q (no deficit slack)": lambda r: 2 * r["d2el"] + r["incU"] + r["incC"] + r["slB"] - r["p"] - r["q"],
             "K4: 2d2el+slA-p-q (no token slack)": lambda r: 2 * r["d2el"] + r["slA"] - r["p"] - r["q"],
             "K5: defU-p (deficit pays carried pairs)": lambda r: r["defU"] - r["p"],
             "K6: defU+incC-p-q": lambda r: r["defU"] + r["incC"] - r["p"] - r["q"],
             "L1: incU+incC-qres": lambda r: r["incU"] + r["incC"] - r["qres"],
             "L2: incU+incC+2d2el-qres-pres": lambda r: r["incU"] + r["incC"] + 2 * r["d2el"] - r["qres"] - r["pres"],
             "L3: incU-qres": lambda r: r["incU"] - r["qres"],
             "L4: (defU-ni)+(slB-nii)-qres-pres": lambda r: r["defU"] - r["ni"] + r["slB"] - r["nii"] - r["qres"] - r["pres"],
             "L5: incC-qQbig": lambda r: r["incC"] - r["qQbig"],
             "L6: incU-(qres-qQbig)": lambda r: r["incU"] - r["qres"] + r["qQbig"],
             "O1: Nover-qres": lambda r: r["Nover"] - r["qres"],
             "O1h: Nover-qres (2h<=m only)": lambda r: r["Nover"] - r["qres"] if 2 * r["h"] <= r["m"] else 10 ** 9,
             "O2: Nover-q": lambda r: r["Nover"] - r["q"],
             "O3: swapU-qres": lambda r: r["swapU"] - r["qres"],
             "pres>0 count (needs 2h>m)": lambda r: -r["pres"],
             "qres>0 count": lambda r: -r["qres"]}
    for key, f in cands.items():
        vals = [(f(r), r) for r in recs]
        bad = sum(1 for v, r in vals if v < 0)
        mn = min(vals, key=lambda t: t[0]) if vals else None
        print(" ", key, "failures", bad, "min", mn[0] if mn else None, mn[1] if mn and mn[0] < 0 else "")
if __name__ == "__main__":
    _main()
