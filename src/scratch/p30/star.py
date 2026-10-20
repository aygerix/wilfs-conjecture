r"""Anatomy of STAR at P18 depth four (lead, 2026-10-20).  Notation as in q34.py.
STAR = P_w + J_ge + k L3 - 4 d4 = P_w + k(1 + a1) + F_rest + W2' + W3 + sum_{r in D} (loc(r) - 4), where for r in D
  alpha(r) = #{b <= r : r - b in N3}  (all such r - b are < h),  beta(r) = #{b > r : r + m - b in U2},
  betalow(r) = #{b > r : r + m - b in U2 n [0,h)}  (these incidences are counted in J_ge AND in k a2),
  w2(r) = #{b > r : r + m - b in N3 n [0,h)}  (outgoing wrapped incidence of an N3 element below h: waste of k L3),
  loc(r) = alpha + beta + betalow + w2;  F_rest = k a2 - sum betalow;  W2' = (waste of k a3) - sum w2;  W3 = J_ge - sum beta.
Tested: LD := sum_r (4 - loc(r))^+ <= k(1 + a1) + P_w  [LOC]  and  <= k(1 + a1) + P_w + W3  [LOC3].
usage: star.py exh k mlo mhi | rnd kmin kmax mlo mhi N seed"""
import sys, itertools, random
from q34 import layers
def anat(m, B):
    S = layers(m, B)
    if len(S[4]) != m or len(S[3]) == m: return None
    h = max(r for r in range(m) if r not in S[3]) + 1; k = len(B)
    U2 = S[2] - S[1]; N3 = S[3] - S[2]; D = sorted(set(range(m)) - S[3])
    a1 = sum(1 for b in B if b < h); a2 = sum(1 for s in U2 if s < h); a3 = sum(1 for u in N3 if u < h)
    Pw = sum(1 for i, x in enumerate(B) for y in B[i:] if x + y >= m)
    Jge = sum(1 for u in U2 for b in B if u + b >= m); L3 = sum(1 for r in S[3] if r < h)
    STAR = Pw + Jge + k * L3 - 4 * len(D)
    sa = sb = sbl = sw = 0; LD = 0
    for r in D:
        al = sum(1 for b in B if b <= r and (r - b) in N3)
        be = sum(1 for b in B if b > r and (r + m - b) in U2)
        bl = sum(1 for b in B if b > r and (r + m - b) in U2 and r + m - b < h)
        w2 = sum(1 for b in B if b > r and (r + m - b) in N3 and r + m - b < h)
        sa += al; sb += be; sbl += bl; sw += w2; LD += max(0, 4 - al - be - bl - w2)
    W2p = k * a3 - sa - sw; W3 = Jge - sb; Frest = k * a2 - sbl
    assert STAR == Pw + k * (1 + a1) + Frest + W2p + W3 + (sa + sb + sbl + sw) - 4 * len(D)
    return dict(m=m, B=tuple(B), k=k, h=h, d4=len(D), STAR=STAR, LD=LD, free=k * (1 + a1), Pw=Pw, W3=W3, W2p=W2p, Frest=Frest,
                LOC=k * (1 + a1) + Pw - LD, LOC3=k * (1 + a1) + Pw + W3 - LD)
if __name__ == "__main__":
    a = sys.argv[1:]; recs = []
    if a[0] == "exh":
        k, mlo, mhi = map(int, a[1:4])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = anat(m, list(B))
                if r: recs.append(r)
    else:
        kmin, kmax, mlo, mhi, N, seed = map(int, a[1:7]); random.seed(seed)
        for i in range(N):
            m = random.randint(mlo, mhi); k = random.randint(kmin, min(kmax, m - 1))
            r = anat(m, sorted(random.sample(range(1, m), k)))
            if r: recs.append(r)
    for key in ("STAR", "LOC", "LOC3"):
        bad = [r for r in recs if r[key] < 0]
        print(a, key, "S", len(recs), "fails", len(bad), "min", min((r[key] for r in recs), default=None))
        for r in sorted(recs, key=lambda r: r[key])[:2]: print("   ", r)
