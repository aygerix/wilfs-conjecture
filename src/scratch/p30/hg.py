r"""HG1 at P18 depth four, per interval (lead, 2026-10-20).  Hard = {r in D : r - b in D for every b in B, b < r}.
B_lo = B n [0,h) = {beta_1 < ... < beta_a}, beta_0 = 0, beta_{a+1} = h.  HGI: |Hard n (beta_j, beta_{j+1})| <= k for every j.
Also HGI2: <= #{b in B : b > beta_j}  and  HGI3: <= #{b in B : b >= beta_{j+1}} (b in B with b > every hard r there).
usage: hg.py exh k mlo mhi | rnd kmin kmax mlo mhi N seed"""
import sys, itertools, random
from q34 import layers
def an(m, B):
    S = layers(m, B)
    if len(S[4]) != m or len(S[3]) == m: return None
    h = max(r for r in range(m) if r not in S[3]) + 1; k = len(B)
    D = set(r for r in range(h) if r not in S[3])
    hard = sorted(r for r in D if all((r - b) in D for b in B if b < r))
    lo = [0] + [b for b in B if b < h] + [h]
    worst = {"HGI": 10**9, "HGI2": 10**9, "HGI3": 10**9}
    for j in range(len(lo) - 1):
        cnt = sum(1 for r in hard if lo[j] < r < lo[j + 1])
        worst["HGI"] = min(worst["HGI"], k - cnt)
        worst["HGI2"] = min(worst["HGI2"], sum(1 for b in B if b > lo[j]) - cnt)
        worst["HGI3"] = min(worst["HGI3"], sum(1 for b in B if b >= lo[j + 1]) - cnt)
    return dict(m=m, B=tuple(B), k=k, h=h, d4=len(D), hard=len(hard), HG1=k * (len(lo) - 1) - len(hard), **worst)
if __name__ == "__main__":
    a = sys.argv[1:]; recs = []
    if a[0] == "exh":
        k, mlo, mhi = map(int, a[1:4])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = an(m, list(B))
                if r: recs.append(r)
    else:
        kmin, kmax, mlo, mhi, N, seed = map(int, a[1:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); k = random.randint(kmin, min(kmax, m - 1))
            r = an(m, sorted(random.sample(range(1, m), k)))
            if r: recs.append(r)
    for key in ("HG1", "HGI", "HGI2", "HGI3"):
        bad = [r for r in recs if r[key] < 0]
        print(a, key, "S", len(recs), "fails", len(bad), "min", min((r[key] for r in recs), default=None))
        for r in sorted(recs, key=lambda r: r[key])[:2]: print("   ", r)
