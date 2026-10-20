# FREE-FULL (W >= E1 + E3full) on interval / AP families of P18 depth four (lead, 2026-10-20)
import sys
sys.path.insert(0, '.')
from p18free import run
from math import gcd
worst = None; neg = 0; tot = 0; shown = 0
for k in range(3, 16):
    for d in (1, 2, 3):
        for u in range(1, 80):
            B = [u + i * d for i in range(k)]
            for m in range(max(B) + 1, max(B) + 1 + 3 * k * d + 40):
                gg = m
                for b in B: gg = gcd(gg, b)
                if gg != 1: continue
                r = run(m, tuple(B))
                if not r: continue
                tot += 1
                if r["Ffull"] < 0:
                    neg += 1
                    if shown < 6: shown += 1; print("FAIL k=%d d=%d" % (k, d), {x: r[x] for x in ("m", "B", "h", "e", "W", "E1", "E3f", "Ffull")})
                if worst is None or r["Ffull"] < worst["Ffull"]: worst = r
print("interval/AP P18 depth-four S:", tot, "FREE-FULL failures:", neg)
print("min Ffull:", {x: worst[x] for x in ("m", "B", "h", "e", "W", "E1", "E3f", "Ffull")})
