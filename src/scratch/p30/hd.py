r"""The hard part of DK at P18 depth four (lead, 2026-10-20).  X = S_3 n [0,h), D = [0,h) - S_3.
D_alpha: r - b in N3 for some b <= r;  D_betalow: r + m - b in U2 n [0,h) for some b > r;  H_D = the rest
(every parent of r is in U2 n [h, m), and then all three pair sums of the triple lie in U2 n [h, m)).
Tests: DK (d4 <= k L3), HD1: |H_D| <= k (1 + a1), HD2: |H_D| <= k |S_2 n [0,h)|, and HDW: |H_D| <= waste_X.
usage: hd.py exh k mlo mhi | rnd kmin kmax mlo mhi N seed"""
import sys, itertools, random
from q34 import layers
def an(m, B):
    S = layers(m, B)
    if len(S[4]) != m or len(S[3]) == m: return None
    h = max(r for r in range(m) if r not in S[3]) + 1; k = len(B)
    U2 = S[2] - S[1]; N3 = S[3] - S[2]; D = [r for r in range(h) if r not in S[3]]; X = [u for u in range(h) if u in S[3]]
    Ds = set(D)
    tau = lambda u, b: u + b if u + b < m else u + b - m
    HD = [r for r in D if not any(b <= r and (r - b) in N3 for b in B) and not any(b > r and (r + m - b) in U2 and r + m - b < h for b in B)]
    a1 = sum(1 for b in B if b < h); s2h = sum(1 for u in S[2] if u < h)
    used = sum(1 for u in X for b in B if tau(u, b) in Ds)
    wasteX = k * len(X) - used
    return dict(m=m, B=tuple(B), k=k, h=h, d4=len(D), L3=len(X), HD=len(HD), DK=k * len(X) - len(D),
                HD1=k * (1 + a1) - len(HD), HD2=k * s2h - len(HD), HDW=wasteX - len(HD))
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
    for key in ("DK", "HD1", "HD2", "HDW"):
        bad = [r for r in recs if r[key] < 0]
        print(a, key, "S", len(recs), "fails", len(bad), "min", min((r[key] for r in recs), default=None))
        for r in sorted(recs, key=lambda r: r[key])[:2]: print("   ", r)
