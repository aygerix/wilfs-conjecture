"""Tiny exact LP feasibility (Phase-I simplex, Bland's rule, Fractions).
feasible(A, b): is there x >= 0 with A x = b ?  Returns a solution (list of Fractions) or None."""
from fractions import Fraction as Fr

def feasible(A, b):
    m = len(A); n = len(A[0]) if m else 0
    # make b >= 0
    A = [[Fr(v) for v in row] for row in A]; b = [Fr(v) for v in b]
    for i in range(m):
        if b[i] < 0:
            A[i] = [-v for v in A[i]]; b[i] = -b[i]
    # tableau with artificials n..n+m-1
    T = [A[i] + [Fr(1) if j == i else Fr(0) for j in range(m)] + [b[i]] for i in range(m)]
    basis = [n + i for i in range(m)]
    N = n + m
    # objective: minimize sum of artificials -> reduced costs
    def obj_row():
        r = [Fr(0)] * (N + 1)
        for j in range(n, N): r[j] = Fr(1)
        for i in range(m):
            bi = basis[i]
            if r[bi] != 0:
                c = r[bi]
                r = [r[k] - c * T[i][k] for k in range(N + 1)]
        return r
    r = obj_row()
    while True:
        enter = next((j for j in range(N) if r[j] < 0), None)
        if enter is None: break
        best = None
        for i in range(m):
            if T[i][enter] > 0:
                ratio = T[i][N] / T[i][enter]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None: return None  # unbounded (cannot happen in phase I)
        i = best[1]; piv = T[i][enter]
        T[i] = [v / piv for v in T[i]]
        for k in range(m):
            if k != i and T[k][enter] != 0:
                c = T[k][enter]; T[k] = [T[k][q] - c * T[i][q] for q in range(N + 1)]
        c = r[enter]; r = [r[q] - c * T[i][q] for q in range(N + 1)]
        basis[i] = enter
    if -r[N] != 0:  # optimal phase-I value = -r[N]
        return None
    x = [Fr(0)] * n
    for i in range(m):
        if basis[i] < n: x[basis[i]] = T[i][N]
    return x

def maximize(c, A, b):
    """max c.x s.t. A x = b, x >= 0 (exact, Bland). Returns (value, x) or (None, None) if infeasible;
    ('unbounded', None) if unbounded."""
    m = len(A); n = len(c)
    A = [[Fr(v) for v in row] for row in A]; b = [Fr(v) for v in b]; c = [Fr(v) for v in c]
    for i in range(m):
        if b[i] < 0:
            A[i] = [-v for v in A[i]]; b[i] = -b[i]
    N = n + m
    T = [A[i] + [Fr(1) if j == i else Fr(0) for j in range(m)] + [b[i]] for i in range(m)]
    basis = [n + i for i in range(m)]
    def run(cost, allowed):
        # cost: list length N (minimize cost.x); reduced costs row
        r = cost[:] + [Fr(0)]
        for i in range(m):
            bi = basis[i]
            if r[bi] != 0:
                cc = r[bi]; r = [r[k] - cc * T[i][k] for k in range(N + 1)]
        while True:
            enter = next((j for j in range(N) if allowed[j] and r[j] < 0), None)
            if enter is None: return r
            best = None
            for i in range(m):
                if T[i][enter] > 0:
                    ratio = T[i][N] / T[i][enter]
                    if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                        best = (ratio, i)
            if best is None: return 'unbounded'
            i = best[1]; piv = T[i][enter]
            T[i] = [v / piv for v in T[i]]
            for k in range(m):
                if k != i and T[k][enter] != 0:
                    cc = T[k][enter]; T[k] = [T[k][q] - cc * T[i][q] for q in range(N + 1)]
            cc = r[enter]; r = [r[q] - cc * T[i][q] for q in range(N + 1)]
            basis[i] = enter
    r = run([Fr(0)] * n + [Fr(1)] * m, [True] * N)
    if -r[N] != 0: return None, None
    # drive artificials out of basis where possible
    for i in range(m):
        if basis[i] >= n:
            j = next((j for j in range(n) if T[i][j] != 0), None)
            if j is not None:
                piv = T[i][j]; T[i] = [v / piv for v in T[i]]
                for k in range(m):
                    if k != i and T[k][j] != 0:
                        cc = T[k][j]; T[k] = [T[k][q] - cc * T[i][q] for q in range(N + 1)]
                basis[i] = j
    r = run([-v for v in c] + [Fr(0)] * m, [True] * n + [False] * m)
    if r == 'unbounded': return 'unbounded', None
    x = [Fr(0)] * n
    for i in range(m):
        if basis[i] < n: x[basis[i]] = T[i][N]
    return sum(ci * xi for ci, xi in zip(c, x)), x
