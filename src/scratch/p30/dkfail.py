r"""Independent check of the DK counterexample (lead, 2026-10-20): brute-force membership from generators."""
from lwfail import brute
import sys
sys.path.insert(0, "../p29")
from dead import info
m = 302; B = [36,37,38,41,42,43,45,51,53,63,65,71,75,97,170,171,175,176,178,183,185,186]
gens = [m] + [m + b for b in B]
b = brute(gens, 4 * m); r = info(gens)
print("brute", b); print("dead.info", {k: r[k] for k in ("m", "e", "c", "g", "W")})
print("DK slack (e-1)L3 - d4 =", (b["e"] - 1) * b["L"] - (b["h"] - b["L"]), " LASTWIN e*L - h =", b["LASTWIN"])
