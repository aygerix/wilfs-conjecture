"""Per-cell column reflection Delta(x) = sum_b lambda(R_b x) - kappa(x) on the lex-min factorization down-set of
Ap(S,m), for all numerical semigroups of genus <= G.  sum_x Delta(x) = (e-1)*ell - g (GW slack).
Tests whether deficits (Delta < 0, at corners) can be paid by surplus (Delta > 0) along restricted edge sets, via
max-flow:  rule 'cover': x = y - e_b;  'below': x < y (componentwise);  'column': x in a column of y (same b-column).
Run on fejer.  Usage: transfer.py G"""
import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
G = int(sys.argv[1])

def children(gaps, F, m, gens):
    """semigroup tree: remove a generator > F from S (add it to the gaps)."""
    out = []
    for n in gens:
        if n <= F: continue
        out.append(n)
    return out

def analyze(S_has, m, c, gens):
    # Apery set
    ap = {}
    for r in range(m):
        w = r
        while not S_has(w): w += m
        ap[r] = w
    M = max(ap.values()); d = len(gens) - 1
    ng = sorted(g for g in gens if g != m)
    # lex-min factorization: minimize x_0, then x_1, ...  rep[k] = set of values representable by ng[k:]
    rep = [None] * (d + 1); rep[d] = {0}
    for k in range(d - 1, -1, -1):
        s = set()
        for v in rep[k + 1]:
            t = v
            while t <= M: s.add(t); t += ng[k]
        rep[k] = s
    cells = {}
    for w in ap.values():
        x = []; rem = w
        for k in range(d):
            t = 0
            while rem - t * ng[k] not in rep[k + 1]: t += 1
            x.append(t); rem -= t * ng[k]
        cells[tuple(x)] = w
    D = set(cells)
    for x in D:  # down-set check
        for b in range(d):
            if x[b] and tuple(x[i] - (i == b) for i in range(d)) not in D: raise SystemExit(f"not a down-set {gens}")
    lam = lambda v: (M - v) // m
    Delta = {}
    for x, v in cells.items():
        s = 0
        for b in range(d):
            J = x[b]
            while tuple(x[i] + (i == b) * (J - x[b] + 1) for i in range(d)) in D: J += 1
            y = tuple(J - x[b] if i == b else x[i] for i in range(d))
            s += lam(cells[y])
        Delta[x] = s - v // m
    return D, cells, Delta, d, M

def flow_ok(D, Delta, rule, d):
    Y = [y for y in D if Delta[y] < 0]; X = [x for x in D if Delta[x] > 0]
    need = sum(-Delta[y] for y in Y)
    if need == 0: return True, 0
    nX, nY = len(X), len(Y); N = 2 + nX + nY; src, snk = 0, 1
    ii, jj, vv = [], [], []
    for i, x in enumerate(X): ii.append(src); jj.append(2 + i); vv.append(Delta[x])
    for k, y in enumerate(Y): ii.append(2 + nX + k); jj.append(snk); vv.append(-Delta[y])
    for k, y in enumerate(Y):
        for i, x in enumerate(X):
            if rule == 'cover': ok = sum(y) - sum(x) == 1 and all(x[t] <= y[t] for t in range(d))
            elif rule == 'below': ok = all(x[t] <= y[t] for t in range(d))
            elif rule == 'column': ok = sum(x[t] != y[t] for t in range(d)) == 1
            else: ok = True
            if ok: ii.append(2 + i); jj.append(2 + nX + k); vv.append(10**6)
    Gm = csr_matrix((np.array(vv, dtype=np.int32), (ii, jj)), shape=(N, N))
    val = maximum_flow(Gm, src, snk).flow_value
    return val >= need, need - val

# semigroup tree with gap sets as Python ints
stats = {r: [0, 0] for r in ('cover', 'below', 'column', 'any')}; total = 0; withdef = 0; ex = {}
stack = [(0, -1, 1, [1], 0)]  # (gapmask, F, m, gens, genus)
while stack:
    gm, F, m, gens, g = stack.pop()
    c = F + 1
    if c > 0 and m > 1:
        has = lambda z, gm=gm: not ((gm >> z) & 1) if z >= 0 else False
        D, cells, Delta, d, M = analyze(has, m, c, gens)
        total += 1
        # deterministic rules: corner y pays from x = y - e_b*, b* = argmax / argmin n_b over supp(y); (a) own covers sum
        for key in ('nosh', 'max', 'min', 'last', 'first', 'eachx', 'eqsplit'):
            stats.setdefault(key, [0, 0])
        defy = [y for y in D if Delta[y] < 0]
        if defy:
            okA = all(-Delta[y] <= sum(max(0, Delta.get(tuple(y[i] - (i == b) for i in range(d)), 0)) for b in range(d) if y[b]) for y in defy)
            stats['nosh'][0 if okA else 1] += 1
            if not okA and 'nosh' not in ex: ex['nosh'] = (gens, [(y, Delta[y]) for y in defy])
            ngs = sorted(g for g in gens if g != m)
            for key, pick in (('max', lambda y: max((b for b in range(d) if y[b]), key=lambda b: ngs[b])),
                              ('min', lambda y: min((b for b in range(d) if y[b]), key=lambda b: ngs[b])),
                              ('last', lambda y: max(b for b in range(d) if y[b])),
                              ('first', lambda y: min(b for b in range(d) if y[b]))):
                load = {}
                for y in defy:
                    b = pick(y); x = tuple(y[i] - (i == b) for i in range(d)); load[x] = load.get(x, 0) - Delta[y]
                ok = all(Delta[x] >= l for x, l in load.items())
                stats[key][0 if ok else 1] += 1
                if not ok and key not in ex: ex[key] = (gens, M, m, sorted(D), {str(k): v for k, v in Delta.items() if v})
            load = {}
            for y in defy:
                sup = [b for b in range(d) if y[b]]
                for b in sup:
                    x = tuple(y[i] - (i == b) for i in range(d)); load[x] = load.get(x, 0) - Delta[y] / len(sup)
            okq = all(max(0, Delta[x]) + 1e-9 >= l for x, l in load.items())
            stats['eqsplit'][0 if okq else 1] += 1
            if not okq and 'eqsplit' not in ex: ex['eqsplit'] = (gens, M, m, {str(k): v for k, v in Delta.items() if v})
            okE = all(Delta[x] >= sum(-Delta[y] for b in range(d) for y in [tuple(x[i] + (i == b) for i in range(d))] if y in Delta and Delta[y] < 0) for x in D if Delta[x] >= 0)
            stats['eachx'][0 if okE else 1] += 1
            if not okE and 'eachx' not in ex: ex['eachx'] = (gens,)
        if any(v < 0 for v in Delta.values()):
            withdef += 1
            for r in ('cover', 'below', 'column', 'any'):
                ok, short = flow_ok(D, Delta, r, d)
                stats[r][0] += ok; stats[r][1] += (not ok)
                if not ok and r not in ex: ex[r] = (gens, short)
    if g < G:
        for n in gens:
            if n <= F: continue
            gm2 = gm | (1 << n)
            if n == m:
                m2 = m + 1; ng = list(range(m2, 2 * m2))
            else:
                m2 = m; ng = [k for k in gens if k != n]
                y = n + m
                dec = any(a != n and not ((gm2 >> a) & 1) and (y - a) != n and not ((gm2 >> (y - a)) & 1) for a in range(m, y // 2 + 1))
                if not dec: ng.append(y)
            stack.append((gm2, n, m2, ng, g + 1))
print(f"genus<={G}: semigroups {total}, with corner deficits {withdef}")
for r, (a, b) in stats.items(): print(f"  rule {r:7s}: payable {a}, NOT payable {b}  first failure {ex.get(r)}")
