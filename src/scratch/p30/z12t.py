"""Tight cases of Z12 (OVF + y0 >= |3A n [h,2h)|) with core elements (regime 2h <= m; lead, 2026-10-20).
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, r4
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    gen = ((m, sorted(random.sample(range(1, m), k))) for m in (random.randint(mlo, mhi) for _ in range(N)))
rows = []; hist = {}
for m, B in gen:
    d = r4.ev(m, B)
    if not d: continue
    key = (min(d["core"], 9), min(d["Z12"], 9)); hist[key] = hist.get(key, 0) + 1
    if d["core"] > 0: rows.append((d["Z12"] - d["core"], d["Z12"], d))
rows.sort(key=lambda t: (t[0], t[1]))
print(sys.argv[1:], "hist (core, Z12):", sorted(hist.items()))
for _, z, d in rows[:12]:
    print(" Z12", z, {x: d[x] for x in ("m", "B", "h", "y0", "core", "extra", "big", "OVF", "q", "p", "phi", "a", "W")})
