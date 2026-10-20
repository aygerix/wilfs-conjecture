"""L1 in the regime 2h <= m (where L1 implies P18 depth-four Wilf): minimum of incU + incC - qres and tight cases."""
import sys, itertools, random, jid
mode = sys.argv[1]
def gen():
    if mode == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5])
        for m in range(mlo, mhi + 1):
            for B in itertools.combinations(range(1, m), k): yield m, B
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        for _ in range(N):
            m = random.randint(mlo, mhi); yield m, sorted(random.sample(range(1, m), k))
n = 0; nq = 0; mn = None; hist = {}
for m, B in gen():
    r = jid.info(m, B)
    if not r or 2 * r["h"] > m: continue
    n += 1
    if r["qres"] == 0: continue
    nq += 1; sl = r["incU"] + r["incC"] - r["qres"]
    hist[min(sl, 20)] = hist.get(min(sl, 20), 0) + 1
    if mn is None or sl < mn[0]: mn = (sl, r)
print(sys.argv[1:], "S with 2h<=m:", n, "with qres>0:", nq, "min L1 slack:", mn, "hist:", sorted(hist.items())[:8])
