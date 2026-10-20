"""[c chosen as the largest c with h Gamma in [c, c+m) and c-1 not in <m, Gamma>; the agent's transcription
c = h max(Gamma) + 1 is inconsistent with h-regularity.] Build Bacher's split collision-free h-regular semigroups S-hat(h, a/b, Delta) (arXiv:2604.25051, Def. 4.4):
  m = [(b+b')h - bb'] delta + b + b',  Gamma = [(a+a')h - a b'] delta + a + a' + Delta,  c = h max(Gamma) + 1,
Delta a B_h set containing 0 (greedy), and verify directly (brute-force membership, independent of ID-q):
collision-freeness below c + m, r (right primitives), E = n_L ell - q d + rho, the difference-body bound
r >= |H| - C(n+h, h), CORE1 (E + r >= 0) and Wilf. Usage: python bacher_build.py HMAX KMAX"""
import sys, itertools
from fractions import Fraction as Fr
from math import comb
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from cfcore_lib import Hsize
HMAX, KMAX = int(sys.argv[1]), int(sys.argv[2])
def greedy_Bh(h, k):
    D = [0]
    x = 1
    while len(D) < k:
        cand = D + [x]; sums = set(); ok = True
        for comb_ in itertools.combinations_with_replacement(cand, h):
            s = sum(comb_)
            if s in sums: ok = False; break
            sums.add(s)
        if ok: D = cand
        x += 1
    return D
def farey_pairs(h):
    fr = sorted({Fr(a, b) for b in range(1, h + 1) for a in range(b, 2 * b + 1)})
    return [(fr[i], fr[i + 1]) for i in range(len(fr) - 1)]
def analyse(m, gens_left, c):
    top = c + 2 * m + 5
    T = [False] * top; T[0] = True; nf = [0] * top; nf[0] = 1
    for x in range(1, top):
        if x >= c: T[x] = True
        else: T[x] = any(g <= x and T[x - g] for g in [m] + gens_left)
    # factorization counts over the left generators (with m) below c + m, for collision-freeness
    G = [m] + gens_left; cnt = [0] * (c + m); cnt[0] = 1
    for g in G:
        for x in range(g, c + m): cnt[x] += cnt[x - g]
    cf = all(cnt[x] <= 1 for x in range(c + m))
    assert not T[c - 1]
    ell = sum(T[:c]); q = -(-c // m); rho = q * m - c
    dec = [x for x in range(c, c + m) if any(T[y] and T[x - y] for y in range(1, x // 2 + 1))]
    d = len(dec); r = m - d; nL = 1 + len(gens_left); E = nL * ell - q * d + rho; W = (nL + r) * ell - c
    return dict(cf=cf, ell=ell, q=q, rho=rho, d=d, r=r, E=E, W=W, CORE1=E + r)
for h in range(3, HMAX + 1):
    for lo, hi in farey_pairs(h):
        a, b, ap, bp = hi.numerator, hi.denominator, lo.numerator, lo.denominator
        if b == 1 or bp == 1: continue
        for k in range(2, KMAX + 1):
            D = greedy_Bh(h, k); delta = D[-1]
            m = ((b + bp) * h - b * bp) * delta + b + bp
            Gam = [((a + ap) * h - a * bp) * delta + a + ap + x for x in D]
            if m > 1500 or h * Gam[-1] > 30000: continue
            # every c with h Gamma in [c, c+m) and c - 1 not in <m, Gamma>
            top = h * Gam[-1] + 2; Sg = [False] * top; Sg[0] = True
            for x in range(1, top): Sg[x] = any(g <= x and Sg[x - g] for g in [m] + Gam)
            cs = [c for c in range(h * Gam[-1] - m + 1, h * Gam[0] + 1) if c > 0 and not Sg[c - 1]]
            if not cs: print("h=%d (%s,%s] Delta=%s m=%d: no valid c" % (h, lo, hi, D, m)); continue
            c = cs[-1]
            res = analyse(m, Gam, c); n = len(Gam)
            lb = Hsize(n, h // 2, h - h // 2) - comb(n + h, h)
            flag = "" if (res['r'] >= lb and res['CORE1'] >= 0 and res['W'] >= 0) else "  <-- CHECK"
            print("h=%d (%s,%s] Delta=%s m=%d c=%d n=%d cf=%s r=%d (DB bound %d) E=%d CORE1=%d W=%d%s" %
                  (h, lo, hi, D, m, c, n, res['cf'], res['r'], lb, res['E'], res['CORE1'], res['W'], flag), flush=True)
