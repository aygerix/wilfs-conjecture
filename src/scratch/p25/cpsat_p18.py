r"""Exact CP-SAT search over P18 depth four at fixed multiplicity m (lead, 2026-10-20).
S = <m, m+B>, B c [1, m-1] arbitrary; for each h in [hlo, hhi], depth four with c = 3m + h is encoded exactly by
  [h, m) c T3 = 3A u (2A - m),  h-1 notin T3,  [0, h) c 4A u (3A - m)   (every residue then has finite Kunz level).
Integer sumsets jA are boolean vectors (exact OR-of-AND encodings).  Targets:
  W   = e*l - 3m - h,  l = 1 + e + |2A n [0,m)| + |T3 n [0,h)|
  TB4 = e*y0 + E1 - h - 3*N4,  y0 = |3A_<h|, N4 = |(4A\3A)_<h|, E1 = e(e+1) - 2|2A|
mode W / TB4: feasibility of target <= thr (default -1; INFEASIBLE = certified none at this (m, h));
mode minW / minTB4: minimize the target.  unc=1 restricts to S not covered by h <= e, e(e+1) >= 2m, (e-1)^2 >= 2m, 3e >= m; unc=2 restricts to a = 0 (B >= h);
unc=3: a = 0 and h > e; unc=4: a = 0, h > e and e(e+1) < 2m (mode W/minW: any such S at all?).
Every solution is re-verified independently (Dijkstra Apery set).
usage: python cpsat_p18.py m mode hlo hhi unc timelimit workers [thr]"""
import sys, time, heapq
from ortools.sat.python import cp_model
def verify(m, B):
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d0, r = heapq.heappop(pq)
        if d0 > w[r]: continue
        for x in B:
            v = d0 + m + x; rr = v % m
            if w[rr] is None or v < w[rr]: w[rr] = v; heapq.heappush(pq, (v, rr))
    if any(x is None for x in w): return None
    c = max(w) - m + 1; g = sum(x // m for x in w); e = len(B) + 1
    A = [0] + list(B); X2 = set(p + q for p in A for q in A); X3 = set(s + p for s in X2 for p in A); X4 = set(s + p for s in X3 for p in A)
    h = c - 3 * m
    y0 = sum(1 for s in X3 if s < h); N4 = sum(1 for s in X4 if s < h and s not in X3)
    return dict(c=c, h=h, e=e, W=e * (c - g) - c, TB4=e * y0 + e * (e + 1) - 2 * len(X2) - h - 3 * N4)
def build(m, h, mode, unc, thr):
    M = cp_model.CpModel()
    x = [M.NewConstant(1)] + [M.NewBoolVar(f"x{i}") for i in range(1, m)]
    def OR_of_pairs(pairs, name):
        t = M.NewBoolVar(name); zs = []
        for (a, b) in pairs:
            z = M.NewBoolVar("")
            M.AddImplication(z, a); M.AddImplication(z, b); M.AddBoolOr([a.Not(), b.Not(), z])
            M.AddImplication(z, t); zs.append(z)
        if zs: M.AddBoolOr(zs + [t.Not()])
        else: M.Add(t == 0)
        return t
    L2 = 2 * m
    p2 = [OR_of_pairs([(x[i], x[s - i]) for i in range(max(0, s - m + 1), s // 2 + 1)], f"p2_{s}") for s in range(L2)]
    p3 = [OR_of_pairs([(p2[t], x[s - t]) for t in range(max(0, s - m + 1), min(s, L2 - 1) + 1)], f"p3_{s}") for s in range(m + h)]
    p4 = [OR_of_pairs([(p3[t], x[s - t]) for t in range(0, s + 1)], f"p4_{s}") for s in range(h)]
    for r in range(h, m): M.AddBoolOr([p3[r], p2[r + m]])
    M.Add(p3[h - 1] == 0); M.Add(p2[h - 1 + m] == 0)
    for r in range(h): M.AddBoolOr([p4[r], p3[r + m]])
    e = M.NewIntVar(2, m, "e"); M.Add(e == sum(x))
    n2 = M.NewIntVar(0, L2, "n2"); M.Add(n2 == sum(p2))
    t3 = []
    for r in range(h):
        v = M.NewBoolVar(""); M.AddBoolOr([p3[r], p2[r + m], v.Not()]); M.AddImplication(p3[r], v); M.AddImplication(p2[r + m], v); t3.append(v)
    y0 = M.NewIntVar(0, h, "y0"); M.Add(y0 == sum(p3[r] for r in range(h)))
    n4 = []
    for r in range(h):
        v = M.NewBoolVar(""); M.AddImplication(v, p4[r]); M.AddImplication(v, p3[r].Not()); M.AddBoolOr([p4[r].Not(), p3[r], v]); n4.append(v)
    if mode in ("W", "minW"):
        ell = M.NewIntVar(0, 4 * m, "ell"); M.Add(ell == 1 + e + sum(p2[s] for s in range(m)) + sum(t3))
        prod = M.NewIntVar(0, 4 * m * m, "prod"); M.AddMultiplicationEquality(prod, [e, ell])
        obj = prod - 3 * m - h
    else:
        prod = M.NewIntVar(0, m * h, "prod"); M.AddMultiplicationEquality(prod, [e, y0])
        esq = M.NewIntVar(0, m * m + m, "esq"); M.AddMultiplicationEquality(esq, [e, e])
        obj = prod + esq + e - 2 * n2 - h - 3 * sum(n4)
    if mode.startswith("min"): M.Minimize(obj)
    else: M.Add(obj <= thr)
    if unc in (2, 3, 4):
        for i in range(1, h): M.Add(x[i] == 0)
        if unc >= 3: M.Add(e < h)
        if unc == 4:
            esq4 = M.NewIntVar(0, m * m + m, "esq4"); M.AddMultiplicationEquality(esq4, [e, e]); M.Add(esq4 + e < 2 * m)
    if unc == 1:
        M.Add(e < h); esq2 = M.NewIntVar(0, m * m + m, "esq2"); M.AddMultiplicationEquality(esq2, [e, e])
        M.Add(esq2 + e < 2 * m); M.Add(3 * e < m)
        esq3 = M.NewIntVar(0, m * m, "esq3"); em1 = M.NewIntVar(1, m, "em1"); M.Add(em1 == e - 1); M.AddMultiplicationEquality(esq3, [em1, em1]); M.Add(esq3 < 2 * m)
    return M, x
def main():
    m, mode = int(sys.argv[1]), sys.argv[2]
    hlo, hhi, unc, tl, wk = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
    thr = int(sys.argv[8]) if len(sys.argv) > 8 else -1
    tot0 = time.time()
    for h in range(hlo, hhi + 1):
        t0 = time.time(); M, x = build(m, h, mode, unc, thr)
        S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = tl; S.parameters.num_workers = wk
        st = S.Solve(M); name = S.StatusName(st); msg = ""
        if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            B = [i for i in range(1, m) if S.Value(x[i])]; msg = f"SOLUTION B={B} recheck={verify(m, B)}"
            if mode.startswith("min"): msg = f"opt={S.ObjectiveValue():.0f} bound={S.BestObjectiveBound():.0f} " + msg
        print(f"m={m} mode={mode} h={h} unc={unc}: {name} {time.time() - t0:.1f}s {msg}", flush=True)
    print(f"total {time.time() - tot0:.1f}s")
if __name__ == "__main__": main()
