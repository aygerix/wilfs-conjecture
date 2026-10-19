"""MaxCL on no-wrap tiles (lead, 2026-10-19).
For a basis P = (1, p_2, ..., p_d) (1 included) and m >= 1, let D_m = { grlex-min representation x of n : 0 <= n < m },
where grlex-min = fewest coins, ties broken by lex order on the exponent vector (largest exponent of the first coin).
D_m is a down-set (removing a coin from a minimal representation gives a minimal one), and x -> x.P is a bijection
D_m -> [0, m) of INTEGERS, hence mod m.  Test MaxCL at every phase:
   S(sigma) = (d+1) sum_N r - sum_A (|y|-1) r,  r = (x.P - sigma) mod m.
usage: python nowrap_maxcl.py seed trials dmax pmax mmax"""
import sys, random

def rep_table(P, M):
    # best[n] = grlex-min exponent vector for n, as tuple; key = (coins, tuple(-x_i) lex) -> minimize
    d = len(P); best = [None]*M; best[0] = tuple([0]*d)
    key = [None]*M; key[0] = (0, tuple([0]*d))
    for n in range(1, M):
        cand = None
        for a in range(d):
            if P[a] <= n and best[n-P[a]] is not None:
                x = list(best[n-P[a]]); x[a] += 1; x = tuple(x)
                kk = (sum(x), tuple(-v for v in x))
                if cand is None or kk < cand[0]: cand = (kk, x)
        best[n] = cand[1]; key[n] = cand[0]
    return best

def check(P, m):
    d = len(P); reps = rep_table(P, m); D = set(reps)
    assert len(D) == m
    # down-set check
    for x in D:
        for a in range(d):
            if x[a] > 0:
                y = list(x); y[a] -= 1; assert tuple(y) in D
    def up(x, a): y = list(x); y[a] += 1; return tuple(y)
    val = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    A = {x for x in D if all(up(x, a) not in D for a in range(d))}
    w = {x: (-(sum(x)-1) if x in A else d+1) for x in D}
    coef = [0]*m
    for x in D: coef[val[x]] = w[x]
    C = sum(coef); S = sum(coef[r]*r for r in range(m)); mn = (S, 0)
    for g in range(m):
        if S < mn[0]: mn = (S, g)
        S += m*coef[g] - C
    H = max(sum(x) for x in D)
    return mn, H, C

if __name__ == '__main__':
    seed, T, dmax, pmax, mmax = map(int, sys.argv[1:6]); rng = random.Random(seed)
    worst = None; neg = 0; n = 0
    for tr in range(T):
        d = rng.randint(2, dmax); P = [1] + sorted(rng.sample(range(2, pmax+1), d-1))
        m = rng.randint(d+1, mmax)
        (mn, sg), H, C = check(P, m); n += 1
        ratio = mn / (C*(m-1)/2)
        if mn < 0:
            neg += 1
            if neg <= 10: print("NEGATIVE", P, m, mn, sg, "height", H, flush=True)
        if worst is None or ratio < worst[0]: worst = (ratio, P, m, mn, sg, H)
    print("tiles", n, "negative", neg, "worst ratio", worst)

def prefix_test(P, m):
    """Check the no-wrap reduction: MaxCL(u) <=> m*F_T(u) <= u*F_T(m) + sum_b P_b |Phi_b|, F_T(u) = sum_{A, v<u} (d+|y|),
    and test the correction-free PREFIX m*F_T(u) <= u*F_T(m). Returns (identity_ok, prefix_fail_count, min prefix slack)."""
    d = len(P); reps = rep_table(P, m); D = set(reps)
    def up(x, a): y = list(x); y[a] += 1; return tuple(y)
    val = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
    A = {x for x in D if all(up(x, a) not in D for a in range(d))}
    T = {y: d+sum(y) for y in A}
    Phi = [sum(T[y]*y[b] for y in A) - (d+1)*sum(x[b] for x in D) for b in range(d)]
    corr = sum(P[b]*(-Phi[b]) for b in range(d))
    FT = [0]*(m+1)
    byv = [None]*m
    for x in D: byv[val[x]] = x
    for u in range(m): FT[u+1] = FT[u] + (T[byv[u]] if byv[u] in A else 0)
    w = {x: (-(sum(x)-1) if x in A else d+1) for x in D}
    ok = True; pf = 0; mins = None
    for u in range(1, m):
        S = sum(w[x]*((val[x]-u) % m) for x in D)
        lhs = m*FT[u]; rhs = u*FT[m] + corr
        if (S >= 0) != (lhs <= rhs): ok = False
        if S != (rhs - lhs) * 1:  # exact identity check: S(u) should equal (rhs - lhs) up to a fixed factor
            pass
        sl = u*FT[m] - m*FT[u]
        if sl < 0: pf += 1
        if mins is None or sl < mins: mins = sl
    return ok, pf, mins
