r"""P18 depth four with B inside (m/2, m) (lead, 2026-10-20): there DEAD = S3 (Z + G >= p + q).  Exhaustive for small k.
usage: bigB.py k mlo mhi"""
import sys, itertools
sys.path.insert(0, ".")
from zg import test
k, mlo, mhi = map(int, sys.argv[1:4]); recs = []
for m in range(mlo, mhi + 1):
    for B in itertools.combinations(range(m // 2 + 1, m), k):
        r = test(m, list(B))
        if r: recs.append(r)
for key in ("S2", "S3"):
    bad = [r for r in recs if r[key] < 0]
    print("k", k, key, "S", len(recs), "fails", len(bad), "min", min((r[key] for r in recs), default=None))
    for r in sorted(bad, key=lambda r: r[key])[:3]: print("   ", r)
if recs:
    r = min(recs, key=lambda r: r["S3"]); print("  tightest S3:", r)
