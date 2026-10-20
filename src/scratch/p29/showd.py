r"""Display the DEAD bookkeeping of one S (lead, 2026-10-20): Apery elements with level, order, carry, L, rays,
slots per direction, carry units (degrees), twins, maximal elements.  usage: showd.py gens..."""
import sys
sys.path.insert(0, ".")
from twin import build
gens = list(map(int, sys.argv[1:])); D = build(gens)
m, w, aps, gen, e, order, car, rep, q, h, W = (D[k] for k in "m w aps gen e order car rep q h W".split())
top = lambda u: q if u % m < h else q - 1
lam = {(u, b): next(j for j in range(m + 1) if (u + (j + 1) * g) not in aps) for u in w for b, g in enumerate(gen)}
mx = [u for u in w if all((u + g) not in aps for g in gen)]
print("m", m, "gens", gen, "e", e, "c", D["c"], "q", q, "h", h, "W", W, "maximal", sorted(mx))
tot_sl = tot_t = 0
for u in sorted(w):
    L = top(u) - u // m; t = car[u]
    sl = {b: [order[u] + j for j in range(lam[u, b] + 1, L + 1)] for b in range(e - 1)}
    ns = sum(len(v) for v in sl.values()); tot_sl += ns; tot_t += t
    fac = "+".join(str(gen[b]) + ("^%d" % a if a > 1 else "") for b, a in sorted(rep[u].items()))
    units = list(range(top(u) - t + 1, top(u) + 1))
    print("%5d r=%3d x=%d o=%d t=%d L=%d top=%d [%s] slots=%s units=%s" % (u, u % m, u // m, order[u], t, L, top(u), fac,
          {gen[b]: v for b, v in sl.items() if v}, units))
print("total slots", tot_sl, "T_c", tot_t, "slots - T_c", tot_sl - tot_t)
