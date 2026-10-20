# Independent check of the external review's counterexamples to Lemma U and T1-DOWN (lead, 2026-10-20).
import sys
from math import gcd
from functools import reduce

def Cp(y, p, m):
    # #{z in (0, y] : z = p mod m}
    if y <= 0: return 0
    return (y - p) // m + 1 if y >= p else 0

def lemmaU(m, r, p, heights):
    D = [(i, j) for i, h in enumerate(heights) for j in range(h)]
    Ds = set(D)
    assert all(((i - 1, j) in Ds or i == 0) and ((i, j - 1) in Ds or j == 0) for i, j in D), "not down-set"
    res = [(i * r[0] + j * r[1]) % m for i, j in D]
    assert len(set(res)) == len(res), "not injective"
    tot = 0
    for f in D:
        R = f[0] * r[0] + f[1] * r[1]
        K = Cp(R, p, m) - sum(f[a] * (Cp(R, p, m) - Cp(R - r[a], p, m)) for a in range(2))
        tot += K
    dec = sum(1 for f in D if sum(f) >= 2)
    return len(D), tot, dec

def semigroup(gens):
    m = min(gens)
    F = m * max(gens) + 10 * m
    mem = [False] * (F + 1); mem[0] = True
    for x in range(1, F + 1):
        mem[x] = any(x >= g and mem[x - g] for g in gens)
    ap = []
    for i in range(m):
        x = i
        while not mem[x]: x += m
        ap.append(x)
    minimal = sorted(g for g in gens if not any(g - h >= 0 and mem[g - h] and h != g and g - h != 0 for h in gens if h < g)
                     and not any(mem[g - h] and g - h > 0 for h in gens if h < g))
    # minimal generators: elements not sums of two nonzero elements
    mg = [x for x in sorted(set(gens)) if not any(mem[y] and mem[x - y] for y in range(1, x))]
    M = max(ap); c = M - m + 1
    g = sum((w - i) // m for i, w in enumerate(ap))
    return m, mem, ap, mg, c, g

def nu(x, n, mem):
    k = 0
    while x - (k + 1) * n >= 0 and mem[x - (k + 1) * n]: k += 1
    return k

def t1down(gens, D, p):
    m, mem, ap, mg, c, g = semigroup(gens)
    P = [n for n in mg if n != m]
    e = len(mg)
    aps = set(ap)
    assert set(D) <= aps, "D not in Ap"
    for x in D:
        for y in ap:
            if x - y >= 0 and mem[x - y]: assert y in D, ("not down-set", x, y)
    def K(x): return Cp(x, p, m) - sum(nu(x, n, mem) * (Cp(x, p, m) - Cp(x - n, p, m)) for n in P)
    sD = sum(K(x) for x in D)
    dec = sum(1 for x in D if x != 0 and x not in mg)
    full = sum(K(x) for x in ap)
    M = max(ap); q = M // m; mu = M % m
    allp = [sum(Cp(x, pp, m) - sum(nu(x, n, mem) * (Cp(x, pp, m) - Cp(x - n, pp, m)) for n in P) for x in ap) for pp in range(1, m + 1)]
    return dict(m=m, e=e, c=c, g=g, ell=c - g, W=e * (c - g) - c, mingens=mg, pstar=mu + 1, sumK_D=sD, dec_D=dec,
                sumK_full=full, m_minus_e=m - e, maxfull_over_p=max(allp), argmax=allp.index(max(allp)) + 1)

if __name__ == "__main__": print("LemmaU m=83 r=(19,18) p=2 heights (9,9,8,7,5,5,2,1):", lemmaU(83, (19, 18), 2, (9, 9, 8, 7, 5, 5, 2, 1)))
if __name__ == "__main__": D = [0, 33, 36, 66, 69, 72, 99, 102, 105, 108, 144]
if __name__ == "__main__": print("T1-DOWN <20,33,36> p=6:", t1down([20, 33, 36], [0, 33, 36, 66, 69, 72, 99, 102, 105, 108, 144], 6))
if __name__ == "__main__": print("T1-DOWN <20,33,36,147> p=6:", t1down([20, 33, 36, 147], [0, 33, 36, 66, 69, 72, 99, 102, 105, 108, 144], 6))
