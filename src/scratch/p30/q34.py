r"""Layer form of Wilf at P18 depth four (lead, 2026-10-20).  S = <m, m+B>, B c [1, m-1], k = |B|.
Layers S_j = {r : jm + r in S} satisfy S_{j+1} = S_j u (S_j + B)_{<m} u ((S_{j-1} + B)_{>=m} - m) exactly.
Depth four: S_3 contains [h, m), h-1 not in S_3, S_4 = [0, m).  d_j = |S_j - S_{j-1}|, L3 = |S_3 n [0, h)|.
Identity: W = Q3 + Q4 with Q3 = 2k^2 + 2k + (k-2) d2 - 3 d3 and Q4 = k L3 - 4 d4.
usage: q34.py exh k mlo mhi | rnd kmin kmax mlo mhi N seed"""
import sys, itertools, random
sys.path.insert(0, "../p29")
from dead import info
def layers(m, B):
    S = [{0}, {0} | set(B)]
    for j in range(1, 4):
        nxt = set(S[j]) | {u + b for u in S[j] for b in B if u + b < m} | {u + b - m for u in S[j - 1] for b in B if u + b >= m}
        S.append(nxt)
    return S
def test(m, B, check=False):
    S = layers(m, B)
    if len(S[4]) != m or len(S[3]) == m: return None
    h = max(r for r in range(m) if r not in S[3]) + 1
    if any(r not in S[3] for r in range(h, m)): raise AssertionError("S_3 must contain [h, m)")
    k = len(B); d = [len(S[0])] + [len(S[j]) - len(S[j - 1]) for j in range(1, 5)]
    L3 = sum(1 for r in S[3] if r < h)
    Q3 = 2 * k * k + 2 * k + (k - 2) * d[2] - 3 * d[3]; Q4 = k * L3 - 4 * d[4]
    W = (k + 1) * (sum(len(S[j]) for j in range(3)) + L3) - (3 * m + h)
    assert W == Q3 + Q4 and Q3 >= 0
    U2 = S[2] - S[1]; N3 = S[3] - S[2]; D4 = set(range(m)) - S[3]; Bs = set(B)
    Pw = sum(1 for i, x in enumerate(B) for y in B[i:] if x + y >= m)
    a1 = sum(1 for b in B if b < h); a2 = sum(1 for s in U2 if s < h); a3 = sum(1 for u in N3 if u < h)
    I = {r: sum(1 for b in B if (r + m - b) in U2) + sum(1 for b in B if b <= r and (r - b) in N3 and r - b < h) for r in D4}
    free = Pw + k * (1 + a1 + a2)
    RESs = free + sum(I[r] - 4 for r in D4); RESp = free - sum(max(0, 4 - I[r]) for r in D4)
    assert W >= RESs, (m, B, W, RESs)
    Pu = k * (k + 1) // 2 - Pw
    Jge = sum(1 for u in U2 for b in B if u + b >= m); Jlt = k * d[2] - Jge
    T = {u for u in N3 if any((u - b) in U2 for b in B if b <= u)}; Rp = N3 - T
    GT = 4 * Pu - 2 * d[2] + Jlt - 3 * len(T); GR = 4 * Pw - 3 * len(Rp); G4 = Jge + k * a3 - 4 * d[4]; F = k * (1 + a1 + a2)
    assert W == GT + GR + G4 + F and GT >= 0 and GR >= Pw, (m, B, W, GT, GR, G4, F)
    STAR = Pw + Jge + k * h - (k + 4) * d[4]
    if check:
        r = info([m] + [m + b for b in B]); assert r["W"] == W and r["c"] == 3 * m + h, (m, B, r, W)
    return dict(m=m, B=tuple(B), k=k, h=h, d2=d[2], d3=d[3], d4=d[4], L3=L3, Q3=Q3, Q4=Q4, W=W, Pw=Pw, a1=a1, a2=a2, a3=a3, RESs=RESs, RESp=RESp, STAR=STAR, GT=GT, GR=GR, G4=G4, F=F, Jge=Jge, Imin=min(I.values()))
if __name__ == "__main__":
    a = sys.argv[1:]; recs = []
    if a[0] == "exh":
        k, mlo, mhi = map(int, a[1:4])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = test(m, list(B), check=(m < 25))
                if r: recs.append(r)
    else:
        kmin, kmax, mlo, mhi, N, seed = map(int, a[1:7]); random.seed(seed)
        for i in range(N):
            m = random.randint(mlo, mhi); k = random.randint(kmin, min(kmax, m - 1))
            r = test(m, sorted(random.sample(range(1, m), k)), check=(i % 50 == 0))
            if r: recs.append(r)
    for key in ("W", "RESs", "STAR"):
        bad = [r for r in recs if r[key] < 0]
        print(a, key, "S", len(recs), "fails", len(bad), "min", min((r[key] for r in recs), default=None))
        for r in sorted(recs, key=lambda r: r[key])[:2]: print("   ", r)
