# FREE-A stress test on structured all-A families: B = arithmetic progressions {u + i d}, and APs with one or two
# perturbations; all m. Prints min FREE-A slack F and min W, and any F < 0.  (lead, 2026-10-20)
import sys
sys.path.insert(0, '.')
from allA import run
from math import gcd
worstF = None; worstW = None; neg = 0; tot = 0
for k in range(3, 12):
    for d in range(1, 6):
        for u in range(1, 60):
            Bfull = [u + i * d for i in range(k)]
            variants = [Bfull]
            for j in range(k):
                for s in (-1, 1):
                    v = list(Bfull); v[j] += s
                    if len(set(v)) == k and min(v) > 0: variants.append(sorted(v))
            for B in variants:
                for m in range(max(B) + 1, 4 * max(B) + 4):
                    gg = m
                    for b in B: gg = gcd(gg, b)
                    if gg != 1: continue
                    r = run(m, tuple(B))
                    if not r: continue
                    tot += 1
                    if r["F"] < 0:
                        neg += 1
                        if neg <= 8: print("FREE-A FAIL", r)
                    if worstF is None or r["F"] < worstF["F"]: worstF = r
                    if worstW is None or r["W"] < worstW["W"]: worstW = r
print("structured all-A depth-four S:", tot, "FREE-A failures:", neg)
print("min F:", worstF); print("min W:", worstW)
