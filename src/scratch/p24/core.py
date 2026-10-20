r"""Core regime of P18 depth four (lead, 2026-10-20): all b in [ceil(h/2), h).
Checks (i) W = E1 + E3 + e^2 - h - (e-3)*delta + 3*Omega (exact), (ii) window filling h <= e(e-1) + 2e' - 2delta,
(iii) W >= e - 2e' - (e-5)delta + 3 Omega (+E1+E3); counts the class, delta distribution, and coverage by known criteria
(DEPTH4-EH h <= e; Yang-Zhang e(e+1) >= 2m; DKM (e-1)^2 >= 2m; Eliahou 3e >= m).
usage: python core.py exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random
from math import gcd
sys.path.insert(0, '.')
from p18free import run
def ceil2(h): return (h + 1) // 2
def check(r, m, B):
    h, e = r["h"], r["e"]
    if min(B) < ceil2(h) or max(B) >= h: return None
    A = [0] + list(B)
    W1 = range(h, 3 * ceil2(h))
    ep = sum(1 for a in A if (a + m) in W1)
    ok_i = (r["W"] == r["E1"] + r["E3"] + e * e - h - (e - 3) * r["delta"] + 3 * r["Omega"])
    ok_ii = (h <= e * (e - 1) + 2 * ep - 2 * r["delta"])
    lb = e - 2 * ep - (e - 5) * r["delta"] + 3 * r["Omega"]
    known = (h <= e) or (e * (e + 1) >= 2 * m) or ((e - 1) ** 2 >= 2 * m) or (3 * e >= m)
    return dict(ok_i=ok_i, ok_ii=ok_ii, lb=lb, ep=ep, known=known)
if __name__ == "__main__":
    tot = core = bad_i = bad_ii = negW = new = 0; dl = {}; worst = None
    def handle(m, B):
        global tot, core, bad_i, bad_ii, negW, new, worst
        r = run(m, B)
        if not r: return
        tot += 1; c = check(r, m, B)
        if c is None: return
        core += 1; bad_i += not c["ok_i"]; bad_ii += not c["ok_ii"]; negW += r["W"] < 0
        dl[r["delta"]] = dl.get(r["delta"], 0) + 1
        if not c["known"]:
            new += 1
            if worst is None or r["W"] < worst[0]["W"]: worst = (r, c)
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                gg = m
                for b in B: gg = gcd(gg, b)
                if gg == 1: handle(m, B)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); h0 = random.randint(max(4, m // 2), m)
            B = tuple(sorted(random.sample(range(ceil2(h0), h0), min(k, h0 - ceil2(h0)))))
            if len(B) < k: continue
            gg = m
            for b in B: gg = gcd(gg, b)
            if gg == 1: handle(m, B)
    print("P18 depth-four S:", tot, "| core:", core, "| identity fails:", bad_i, "| window-filling fails:", bad_ii, "| W<0:", negW)
    print("delta distribution in core:", dict(sorted(dl.items())), "| core S not covered by known criteria:", new)
    if worst: print("min W among new:", {x: worst[0][x] for x in ("m", "B", "h", "e", "W", "delta", "Omega")}, worst[1])
