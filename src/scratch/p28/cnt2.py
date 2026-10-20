r"""Two-term count for the P18 depth-four residual (lead, 2026-10-20):
  |R| + p <= (a+1)*|B >= h/3| + D3gen,   D3gen = #{(b, x) in B x B : b + 2x >= m + h}  (ordered pairs).
If true, CL4 (hence Wilf) follows: these tokens are dead, disjoint from rho's, and pi uses at most p of them.
usage: cnt2.py exh k mlo mhi | rnd k mlo mhi N seed | pts m b1 b2 ..."""
import sys, itertools, random
from match4 import build
def test(m, B):
    D = build(m, B)
    if D is None: return None
    w, car, e, rep, h = D["w"], D["car"], D["e"], D["rep"], D["h"]
    R = p = 0
    for v in w:
        if car[v] == 0: continue
        if len(rep[v]) == 2: p += 1
        else:
            b = sorted(B[i] for i in rep[v])
            if b[0] + b[1] >= h: R += 1
    a = sum(1 for b in B if b < h); n3 = sum(1 for x in B if 3 * x >= h)
    D3 = sum(1 for b in B for x in B if b + 2 * x >= m + h)
    Ps = sum(1 for i in range(len(B)) for j in range(i, len(B)) if B[i] + B[j] >= m)
    Rs = len(set(B[i] + B[j] + B[l] for i in range(len(B)) for j in range(i, len(B)) for l in range(j, len(B))
                 if B[i] + B[j] >= h and m <= B[i] + B[j] + B[l] < m + h))
    pure = (a + 1) * n3 + D3 - Ps - Rs
    y = sum(1 for r in range(h) if w[r] // m <= 3)
    lvl4 = h - y
    win = (a + 1) * n3 + D3 - p - lvl4
    return dict(win=win, lvl4=lvl4, pure=pure, Ps=Ps, Rs=Rs, m=m, B=tuple(B), e=e, h=h, a=a, W=D["W"], R=R, p=p, G4=(a + 1) * n3, D3=D3, slack=(a + 1) * n3 + D3 - R - p)
if __name__ == "__main__":
    recs = []
    if sys.argv[1] == "pts":
        print(test(int(sys.argv[2]), list(map(int, sys.argv[3:])))); sys.exit()
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k):
                r = test(m, list(B))
                if r: recs.append(r)
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
            r = test(m, B)
            if r: recs.append(r)
    badw = [r for r in recs if r["win"] < 0]
    print("  WINDOW version (h - y + p <= G4 + D3) fails", len(badw), "(h>e:", sum(1 for r in badw if r["h"] > r["e"]), ") min", min((r["win"] for r in recs), default=None))
    for r in sorted(badw, key=lambda r: r["win"])[:3]: print("    ", r)
    badp = [r for r in recs if r["pure"] < 0]
    print("  PURE version fails", len(badp), "(h>e:", sum(1 for r in badp if r["h"] > r["e"]), ") min", min((r["pure"] for r in recs), default=None))
    for r in sorted(badp, key=lambda r: r["pure"])[:3]: print("    ", r)
    bad = [r for r in recs if r["slack"] < 0]
    print(sys.argv[1:], "S", len(recs), "fails", len(bad), "(h>e:", sum(1 for r in bad if r["h"] > r["e"]), ")", "min slack", min((r["slack"] for r in recs), default=None))
    for r in sorted(bad, key=lambda r: r["slack"])[:4]: print("  ", r)
