r"""DEAD on truncated semigroups <A>_c = <A> u [c, oo) (lead, 2026-10-20): the Eliahou-number near-misses
(Fromentin's five W_0 = -1 cases, <30,44,48,49>_118), Delgado's S(p) = <mu, gamma, gamma+1>_{p mu}, and a random sweep.
usage: nearmiss.py fixed | delgado | rnd mlo mhi amin amax qlo qhi N seed"""
import sys, random
from dead import info
def trunc(A, c):
    m = min(A)
    return sorted(set(A) | set(range(c, c + m)))
if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "fixed":
        for A, c in [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((17, 27, 28), 68), ((18, 28, 29), 72), ((30, 44, 48, 49), 118)]:
            r = info(trunc(A, c)); print(A, c, {k: r[k] for k in ("m", "e", "c", "g", "W", "Lam", "O", "D")})
    elif a[0] == "delgado":
        worst = None; n = 0
        for mu in range(5, 40):
            for gam in range(mu + 1, 3 * mu):
                for p in range(3, 9):
                    r = info(trunc((mu, gam, gam + 1), p * mu))
                    if r is None or r["c"] != p * mu: continue
                    n += 1
                    if worst is None or r["D"] < worst["D"]: worst = r
        print("delgado S", n, "worst", worst)
    else:
        mlo, mhi, amin, amax, qlo, qhi, N, seed = map(int, a[1:9]); random.seed(seed)
        n = bad = 0; worst = None
        for _ in range(N):
            m = random.randint(mlo, mhi); na = random.randint(amin, amax)
            A = [m] + random.sample(range(m + 1, 3 * m), na); c = random.randint(qlo * m, qhi * m)
            r = info(trunc(A, c))
            if r is None: continue
            n += 1; bad += r["D"] < 0
            if worst is None or r["D"] < worst["D"]: worst = r
        print(a, "S", n, "DEAD fails", bad, "worst", worst)
