# Independent referee checker for the cone-tile lemmas (written from the statements in PROOFS.md / NOTEBOOK.md,
# not from the project's code).  D = Cyl(h,F,G) \ (q + N^3).
#   Cyl = {x : x2 < h(x1), x3 < F(x1), x3 < G(x2)}  (membership by the three projections)
# Returns a dict of numbers and a list of violations (tag, data).
import itertools

E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def add(x, d, k=1):
    y = list(x); y[d] += k; return tuple(y)


class Cone:
    def __init__(self, h, F, G, q):
        self.h, self.F, self.G, self.q = tuple(h), tuple(F), tuple(G), (tuple(q) if q else None)
        L1, L2, L3 = len(h), len(G), F[0]
        assert h[0] == L2 and G[0] == L3 and len(F) == L1
        self.L = (L1, L2, L3)
        cells = []
        for x1 in range(L1):
            for x2 in range(L2):
                for x3 in range(L3):
                    x = (x1, x2, x3)
                    if self.inD(x): cells.append(x)
        self.D = set(cells)
        self.m = len(cells)

    def inK(self, x):
        q = self.q
        return q is not None and x[0] >= q[0] and x[1] >= q[1] and x[2] >= q[2]

    def inCyl(self, x):
        x1, x2, x3 = x
        if min(x) < 0: return False
        if x1 >= len(self.h) or x2 >= self.h[x1]: return False
        if x3 >= self.F[x1]: return False
        if x2 >= len(self.G) or x3 >= self.G[x2]: return False
        return True

    def inD(self, x):
        return self.inCyl(x) and not self.inK(x)


def analyse(h, F, G, q, order_tie=0, full=True):
    S = Cone(h, F, G, q)
    D = S.D; q = S.q; inK = S.inK
    viol = []
    # reach(y) = max |z| over z in D, z >= y
    reach = {}
    for x in sorted(D, key=lambda z: -sum(z)):
        r = sum(x)
        for d in range(3):
            y = add(x, d)
            if y in D and reach[y] > r: r = reach[y]
        reach[x] = r
    ht = {x: reach[x] - sum(x) for x in D}
    Max = {x for x in D if all(add(x, d) not in D for d in range(3))}
    assert Max == {x for x in D if ht[x] == 0}
    t = len(Max)

    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    T = {x: tuple(top(x, a) for a in range(3)) for x in D}
    hfun = {x: sum(ht[y] for y in T[x]) for x in D}
    Tri, qU, qO = [], [], {}
    for x in D:
        if x in Max: continue
        n = sum(1 for y in T[x] if y in Max)
        if n == 3: Tri.append(x)
        elif n == 2 and hfun[x] == 1:
            c = next(a for a in range(3) if T[x][a] not in Max)
            if T[x][c] == x: qU.append((x, c))
            else: qO[x] = c
    # faces and corners C
    def outer(P):
        return sum(1 for (i, j) in P if (i + 1, j) not in P and (i, j + 1) not in P)
    A3 = {(x[0], x[1]) for x in D if x[2] == 0}
    A2 = {(x[0], x[2]) for x in D if x[1] == 0}
    A1 = {(x[1], x[2]) for x in D if x[0] == 0}
    C = outer(A1) + outer(A2) + outer(A3)
    m = len(D)
    H = sum(hfun.values()); delta = H - (m - 1)
    LHS = 2 * t + 2 * len(Tri) + len(qU) + len(qO)
    # Y
    Yd = [{y for y in Max if inK(add(y, d))} for d in range(3)]
    Y = Yd[0] | Yd[1] | Yd[2]
    out = dict(m=m, t=t, tri=len(Tri), qU=len(qU), qO=len(qO), C=C, delta=delta, LHS=LHS,
               Y=len(Y), Yd=tuple(len(s) for s in Yd))
    # ---- CHT, T', B
    if delta < m + 1 - LHS: viol.append(('CHT', delta, m, LHS))
    if q is not None and t > C: viol.append(('Tprime', t, C))
    if q is None and t > C - 2: viol.append(('T', t, C))
    if C * C - 3 * C + 6 > 6 * m: viol.append(('B', C, m))
    if sum(len(s) for s in Yd) != len(Y): viol.append(('Ydisjoint',))
    if not full:
        return out, viol
    # ---- column-height functions in direction c:  psi_c(p) for p = (x_a, x_b), and face profiles f(c, a, s)
    def col(c, x):  # number of z with x with coordinate c replaced by z lying in D (x's c-coordinate ignored)
        y = list(x); y[c] = 0; n = 0
        while tuple(y) in D: n += 1; y[c] += 1
        return n
    def f(c, a, s):  # length of c-column over s e_a
        y = [0, 0, 0]; y[a] = s
        return col(c, tuple(y))
    def inQuad(c, x):
        if q is None: return False
        return all(x[i] >= q[i] for i in range(3) if i != c)
    def gamma(c, x):  # = ht of top_c(x)
        return ht[T[x][c]]
    # ---- S': all cells with all +e_d in D
    inner = [x for x in D if all(add(x, d) in D for d in range(3))]
    users = {}
    for x in inner:
        for a in range(3):
            y = T[x][a]
            if y in Max: users.setdefault(y, set()).add(a)
    for y, ds in users.items():
        if len(ds) >= 2:
            for a, b in itertools.combinations(sorted(ds), 2):
                c = 3 - a - b
                if not inK(add(y, c)): viol.append(('Sprime', y, a, b))
        if len(ds) == 3: viol.append(('three_dirs', y))
    # ---- Peak' in all orientations: p in A_c-projection, p + e_a in projection, gamma = 0
    for x in D:
        for c in range(3):
            if x[c] != 0: continue
            for a in range(3):
                if a == c: continue
                b = 3 - a - c
                xa = add(x, a)
                if xa not in D: continue
                if gamma(c, x) != 0: continue
                if f(c, a, x[a] + 1) < f(c, b, x[b]): continue
                ok = (q is not None and x[a] + 1 == q[a] and x[b] >= q[b] and inK(add(T[x][c], a)))
                if not ok: viol.append(('Peak', x, c, a))
    # ---- P' for all tripod pairs and all ordered planes (al, be), third ga
    triset = set(Tri)
    for U in Tri:
        for U2 in Tri:
            if U == U2: continue
            for al in range(3):
                for be in range(3):
                    if al == be: continue
                    ga = 3 - al - be
                    if U[al] < U2[al] and U[be] > U2[be]:
                        if not (inK(add(T[U][ga], al)) or inK(add(T[U2][ga], be))):
                            viol.append(('Pprime', U, U2, al, be))
    # ---- QF-pair lemma, all orientations: v qO nonmax c, partner dir a (maximal for v), u = v - i e_a qO
    for v, c in qO.items():
        for a in range(3):
            if a == c: continue
            b = 3 - a - c
            for i in range(1, v[a] + 1):
                u = add(v, a, -i)
                if u not in qO: continue
                assert T[u][a] == T[v][a]
                cu = qO[u]
                if f(c, a, v[a]) < f(c, b, v[b]): continue
                alpha = (cu == b and inK(add(T[u][c], a)))
                beta = (cu == c and inQuad(c, v) and not inQuad(c, u) and col(c, v) == q[c]) if q else False
                if not (alpha or beta): viol.append(('QFpair', v, c, a, u))
    # ---- DS, location, fiber
    DS = {}
    for x, c in qO.items():
        dirs = [d for d in range(3) if d != c]
        ok = True
        for d in dirs:
            if not any(add(x, d, -i) in qO for i in range(1, x[d] + 1)): ok = False
        if ok: DS[x] = c
    for x, c in DS.items():
        a, b = [d for d in range(3) if d != c]
        if not (q is not None and x[a] >= q[a] and x[b] >= q[b] and x[c] < q[c]): viol.append(('Location', x, c))
    seen = {}
    for x, c in DS.items():
        for a in range(3):
            if a == c: continue
            k = (a, T[x][a])
            if k in seen: viol.append(('Fiber', x, seen[k], a))
            seen[k] = x
    # DS map to top of smaller maximal direction
    img = {}
    for x, c in DS.items():
        a = min(d for d in range(3) if d != c)
        img.setdefault(T[x][a], []).append(x)
    for y, L in img.items():
        if len(L) > 1 and y not in Y: viol.append(('DSmapY', y))
        if len(L) > 2: viol.append(('DSmap2', y))
    nDS = len(DS)
    if nDS > t + len(Y): viol.append(('nDS', nDS, t, len(Y)))
    # ---- G_O elimination in increasing |x|
    par = {}
    def fnd(u):
        while par.setdefault(u, u) != u:
            par[u] = par[par[u]]; u = par[u]
        return u
    key = (lambda z: (sum(z), z)) if order_tie == 0 else (lambda z: (sum(z), tuple(-w for w in z)))
    used = {}   # y -> set of directions used so far
    rank = 0; cross_only = 0; ds_close = 0; c2map = {}
    for x in sorted(qO, key=key):
        c = qO[x]; a, b = [d for d in range(3) if d != c]
        ya, yb = T[x][a], T[x][b]
        ra, rb = fnd(ya), fnd(yb)
        if ra == rb:
            rank += 1
            case = {}
            for d, y in ((a, ya), (b, yb)):
                if y not in used: viol.append(('closer_unused', x)); case[d] = None; continue
                case[d] = 1 if d in used[y] else 2
                if case[d] == 2:
                    if y not in Y: viol.append(('case2notY', x, y))
                    c2map.setdefault(y, []).append(x)
            if case[a] == 1 and case[b] == 1:
                ds_close += 1
                if x not in DS: viol.append(('closer_notDS', x))
            else: cross_only += 1
        else:
            par[ra] = rb
        for d, y in ((a, ya), (b, yb)): used.setdefault(y, set()).add(d)
    for y, L in c2map.items():
        if len(L) > 1: viol.append(('case2multi', y, L))
    if cross_only > len(Y): viol.append(('crossonly', cross_only, len(Y)))
    comps = len({fnd(y) for y in Max})
    if len(qO) != t - comps + rank: viol.append(('qOident',))
    if len(qO) > 2 * t - 1 + 2 * len(Y): viol.append(('qO_2t', len(qO), t, len(Y)))
    if len(qO) > t - 1 + 2 * len(Y) and qO: viol.append(('qO_headline', len(qO), t, len(Y)))
    out.update(nDS=nDS, cross_only=cross_only, rankO=rank)
    # ---- qU graph, rank, level structure in direction 3
    edges = []
    for x, c in qU:
        a, b = [d for d in range(3) if d != c]
        if not (add(x, a) in Max and add(x, b) in Max): viol.append(('qU_unit', x))
        edges.append((x, c, add(x, a), add(x, b)))
    par.clear()
    rankU_by_level = {}
    crossL = {}
    for (x, c, y1, y2) in sorted(edges, key=lambda e: -e[0][2]):
        v = x[2] + 1
        if c != 2: crossL[(v, c)] = crossL.get((v, c), 0) + 1
        r1, r2 = fnd(y1), fnd(y2)
        if r1 == r2: rankU_by_level[v] = rankU_by_level.get(v, 0) + 1
        else: par[r1] = r2
    rankU = sum(rankU_by_level.values())
    q3 = q[2] if q else None
    for (v, c), k in crossL.items():
        if k > (2 if v == q3 else 1): viol.append(('qU_levelcount', v, c, k))
    for v, k in rankU_by_level.items():
        if v != q3: viol.append(('qU_cycle_off_q3', v, k))
    if rankU > 3: viol.append(('rankU', rankU))
    if q is not None and len(qU) > t + 2: viol.append(('Fcone', len(qU), t))
    if q is None and len(qU) > t - 1 and qU: viol.append(('F', len(qU), t))
    out.update(rankU=rankU)
    # ---- tripod elimination (decreasing |x|)
    keyT = (lambda z: (-sum(z), z)) if order_tie == 0 else (lambda z: (-sum(z), tuple(-w for w in z)))
    seenT = {}
    Scross = 0; Sexc = 0; Phi = {}; crossY = []
    order = sorted(Tri, key=keyT)
    for x in order:
        same = [a for a in range(3) if T[x][a] in seenT and a in seenT[T[x][a]]]
        cr = [a for a in range(3) if T[x][a] in seenT and a not in seenT[T[x][a]]]
        Scross += len(cr); Sexc += max(0, len(same) - 1)
        for a in cr:
            if T[x][a] not in Y: viol.append(('TFcrossY', x))
            crossY.append(T[x][a])
        if len(same) >= 2:
            for a in same:
                for b in same:
                    if a == b: continue
                    c = 3 - a - b
                    ups_b = [add(x, b, i) for i in range(1, 99) if add(x, b, i) in triset]
                    ups_a = [add(x, a, i) for i in range(1, 99) if add(x, a, i) in triset]
                    # (ii) for every partner pair
                    for u in ups_a:
                        for u2 in ups_b:
                            if not (T[u2][c] in Yd[a] or T[u][c] in Yd[b]): viol.append(('TFii', x, a, b))
                    if any(T[u2][c] in Yd[a] for u2 in ups_b): Phi.setdefault((a, b), set()).add(x)
        for a in range(3): seenT.setdefault(T[x][a], set()).add(a)
    if len(crossY) != len(set(crossY)): viol.append(('TFcross_multi',))
    if Scross > len(Y): viol.append(('TFcross', Scross, len(Y)))
    nT = len(Tri)
    if nT and 2 * nT - t > -1 + Scross + Sexc: viol.append(('TFbudget', 2 * nT - t, Scross, Sexc))
    if Sexc > sum(len(s) for s in Phi.values()): viol.append(('TFphi_acc', Sexc))
    for (a, b), L in Phi.items():
        c = 3 - a - b
        for x in L:
            if not (q is not None and x[a] == q[a] - 1 and x[c] < q[c]): viol.append(('TFiii', x, a, b))
        if len({(x[a], x[c]) for x in L}) > 1: viol.append(('TFiv', a, b, sorted(L)))
        low = [x for x in L if q is None or x[b] < q[b]]
        hi = [x for x in L if q is not None and x[b] >= q[b]]
        if len(low) > 1: viol.append(('TFv_low', a, b, sorted(L)))
        if len(hi) > max(0, len(Yd[a]) - 1): viol.append(('TFv_hi', a, b, sorted(L), len(Yd[a])))
        if len(L) > 2 and len(Yd[a]) <= 2: viol.append(('TFv', a, b, sorted(L)))
    if max(out['Yd']) <= 2 and 2 * nT > t + 17: viol.append(('TF17', nT, t))
    out.update(Scross=Scross, Sexc=Sexc, maxPhi=max([len(s) for s in Phi.values()] or [0]))
    # final for tile-like (|Y_d| <= 2): LHS <= 6t + 30
    if max(out['Yd']) <= 2 and LHS > 6 * t + 30: viol.append(('LHS6t30', LHS, t))
    return out, viol


if __name__ == '__main__':
    import sys
    h, F, G, q = [eval(a) for a in sys.argv[1:5]]
    print(analyse(h, F, G, q))
