"""Exact, independent WRAP-MAX evaluator.  Run research computations on fejer.

Cell tuples are used throughout.  No semigroup code is needed for evaluate().
"""
from collections import Counter


def add(x, a):
    y = list(x)
    y[a] += 1
    return tuple(y)


def sub(x, a):
    y = list(x)
    y[a] -= 1
    return tuple(y)


def evaluate(m, P, cells, phases=True):
    P = tuple(P)
    d = len(P)
    D = set(map(tuple, cells))
    assert D and (0,) * d in D
    assert all(1 <= p < m for p in P)
    assert all(sub(x, a) in D for x in D for a in range(d) if x[a])
    v = {x: sum(a*b for a, b in zip(x, P)) for x in D}
    lab = {x: v[x] % m for x in D}
    assert len(set(lab.values())) == len(D)
    A = {x for x in D if all(add(x, a) not in D for a in range(d))}
    N = D - A
    V = {x for x in A if v[x] >= m}
    wrapmax = all(v[x] < m for x in N)
    complete = len(D) == m
    tops = {(x, a): x for x in D for a in range(d)}
    cols = []
    T = Counter()
    for x in D:
        for a in range(d):
            if add(x, a) in D:
                continue
            col = []
            for j in range(x[a]+1):
                z = list(x)
                z[a] = j
                z = tuple(z)
                col.append(z)
                tops[z, a] = x
            cols.append((a, x, col))
            T[x] += len(col)
    assert sum(T.values()) == d * len(D)
    assert sum(T[x]*v[x] for x in D) == (d+1)*sum(v.values())
    upc = {x: sum(add(x, a) in D for a in range(d)) for x in D}
    sp = {x: sum(z > 0 for z in x) for x in D}
    rows = []
    for theta in range(1, m+1):
        low = {x for x in D if v[x] < theta}
        out = sum(tops[x, a] not in low for x in low for a in range(d))
        exits = sum(add(x, a) in D-low for x in low for a in range(d))
        highV = {y for y in V if lab[y] >= theta}
        lowV = V - highV
        shadow = out - len(lowV) + sum(sum(y)-1 for y in highV)
        exit_slack = exits - len(lowV) + sum(sum(y)-1 for y in highV)
        degslack = (sum(sp[y]-1 for y in V) + sum(sum(y) for y in highV)
                    - sum(upc[x]-sp[x] for x in D-V if v[x] >= theta))
        assert exit_slack == degslack
        rho = m-theta
        W = {x for x in D if lab[x] >= theta}
        window = sum(T[x]-d for x in W) + sum(sum(y)-1 for y in V)
        if wrapmax:
            assert window == shadow
        row = dict(theta=theta, rho=rho, low=len(low), wrapped_low=len(lowV),
                   out=out, exits=exits, shadow=shadow, exit_slack=exit_slack,
                   window=window)
        if complete and phases:
            r = {x: (v[x]+rho) % m for x in D}
            K = {x: (v[x]+rho)//m for x in D}
            S = (d+1)*m*(m-1)//2-sum((d+sum(y))*r[y] for y in A)
            Lam = sum(len(col)*r[t] for a, t, col in cols if t in N)
            levels = sum(sum(K[t]-K[x] for x in col) for a, t, col in cols)
            E = sum(v[x]//m for x in D)
            assert S == Lam + m*(levels-E)
            if wrapmax:
                beta = sum(r[x] >= rho for a, t, col in cols if t in N and r[t] < rho for x in col)
                tau = {y: (sum(y)-1)*K[y] + (r[y] < rho)
                       - sum(r[x] < rho for a, t, col in cols if t == y for x in col if x != y)
                       for y in A}
                assert S-Lam == m*shadow == m*(beta+sum(tau.values()))
                row.update(beta=beta, negative=sum(-z for z in tau.values() if z < 0),
                           surplus=sum(z for z in tau.values() if z > 0))
            row.update(S=S, Lam=Lam, levels=levels, E=E)
        rows.append(row)
    return dict(m=m, P=P, D=sorted(D), V=sorted(V), height=max(map(sum, D)),
                complete=complete, wrapmax=wrapmax, rows=rows)


def brief(result):
    return {k: result[k] for k in ('m', 'P', 'D', 'V', 'height', 'complete', 'wrapmax')}
