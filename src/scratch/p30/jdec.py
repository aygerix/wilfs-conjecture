r"""Token anatomy of Conjecture J at P18 depth four (lead, 2026-10-20).
S = <m, m+B>, depth four, h = c - 3m.  X = {r < h : level <= 3}, y = |X|.  Degree-4 power tokens (u, b) with u in Ap,
r(u) in X, b in B; target t(u, b) = u + (4 - o(u)) (m + b).  4*H4 of them are used (one fixed maximal representation
per order-4 element); the rest are unused, of types
  CP : u a carried pair (level 3, order 2): target level >= 5;
  WR : u uncarried, the target wraps (level >= 5);
  HI : u uncarried, no wrap, target residue >= h (target not Apery);
  INX: u uncarried, no wrap, target residue in X (target not Apery);
  ALT: target is an order-4 Apery element, token not in its fixed representation (collision).
J = E2 + (e-1) y - 4 H4 - q - 3 qQ - p  =  E2 + CP + WR + HI + INX + ALT - q - 3 qQ - p.
usage: exh k mlo mhi [Jmax]   (prints tight cases with h > e and the type totals)"""
import sys, itertools, heapq
def info(m, B):
    k = len(B); e = k + 1
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
    ap = {v: v % m for v in w}
    order = {0: 0}; rep = {0: ()}
    for v in sorted(w)[1:]:
        best = -1; br = None
        for x in B:
            u = v - m - x
            if u >= 0 and u in ap and order.get(u, -1) >= 0 and order[u] + 1 > best:
                best = order[u] + 1; br = rep[u] + (x,)
        order[v] = best; rep[v] = tuple(sorted(br))
    lv = [w[r] // m for r in range(m)]; od = [order[w[r]] for r in range(m)]
    X = [r for r in range(h) if lv[r] <= 3]; y = len(X)
    H2 = sum(1 for r in range(m) if od[r] == 2)
    H4 = sum(1 for r in range(m) if od[r] == 4)
    p = sum(1 for r in range(m) if lv[r] == 3 and od[r] == 2)
    carp = set(r for r in range(m) if lv[r] == 3 and od[r] == 2)
    q = qQ = 0
    for r in range(m):
        if lv[r] == 4 and od[r] == 3:
            q += 1
            if any(b <= r and (r - b) in carp for b in B): qQ += 1
    used = set()
    for r in range(m):
        if od[r] == 4:
            R = list(rep[w[r]]); cnt = {}
            for b in R: cnt[b] = cnt.get(b, 0) + 1
            for b, a in cnt.items():
                for j in range(1, a + 1): used.add((w[r] - j * (m + b), b))
    T = dict(CP=0, WR=0, HI=0, INX=0, ALT=0, USED=0)
    for r in X:
        u = w[r]
        for b in B:
            if (u, b) in used: T["USED"] += 1; continue
            if lv[r] == 3 and od[r] == 2: T["CP"] += 1; continue
            rt = r + (4 - od[r]) * b
            if rt >= m: T["WR"] += 1
            elif rt >= h: T["HI"] += 1
            elif lv[rt] <= 3: T["INX"] += 1
            else:
                assert od[rt] == 4, (m, B, r, b)
                T["ALT"] += 1
    E2 = e * (e - 1) - 2 * H2
    J = E2 + (e - 1) * y - 4 * H4 - q - 3 * qQ - p
    assert T["USED"] == 4 * H4 and J == E2 + T["CP"] + T["WR"] + T["HI"] + T["INX"] + T["ALT"] - q - 3 * qQ - p
    g = sum(lv); W = e * (c - g) - c
    a = sum(1 for b in B if b < h)
    return dict(m=m, B=tuple(B), e=e, h=h, W=W, J=J, E2=E2, y=y, H4=H4, q=q, qQ=qQ, p=p, a=a, **T)
def _main():
    k, mlo, mhi = map(int, sys.argv[2:5]); Jmax = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    n = 0; tot = {}; mn = None; shown = 0
    cands = {"C1=CP+WR-q-3qQ-p": lambda r: r["CP"] + r["WR"] - r["q"] - 3 * r["qQ"] - r["p"],
             "C2=CP+WR+E2-q-3qQ-p": lambda r: r["CP"] + r["WR"] + r["E2"] - r["q"] - 3 * r["qQ"] - r["p"],
             "C3=CP+WR+HI-q-3qQ-p": lambda r: r["CP"] + r["WR"] + r["HI"] - r["q"] - 3 * r["qQ"] - r["p"],
             "C4=E2+HI+INX+ALT-q": lambda r: r["E2"] + r["HI"] + r["INX"] + r["ALT"] - r["q"],
             "C5=CP-3qQ-p_lo": lambda r: r["CP"] - 3 * r["qQ"]}
    cmin = {key: (10 ** 9, None) for key in cands}
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k):
            r = info(m, B)
            if not r: continue
            n += 1
            for key, f in cands.items():
                v = f(r)
                if v < cmin[key][0]: cmin[key] = (v, r)
            if r["h"] > r["e"]:
                if mn is None or r["J"] < mn["J"]: mn = r
                if r["J"] <= Jmax and shown < 40: print(r); shown += 1
    print(sys.argv[1:], "depth-four S:", n, "min J over h > e:", mn)
    for key in cands: print("  ", key, "min", cmin[key][0], cmin[key][1])
if __name__ == "__main__":
    _main()
