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
