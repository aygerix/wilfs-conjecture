"""Test crude depth-four candidates at P18 (h > e): Q3 >= 4h - (k+4) [=> Wilf since L3 >= 1], and variants."""
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
cands = {"V1: Q3-4h+k+4": lambda r, Q3, k: Q3 - 4 * r["h"] + k + 4,
         "V2: Q3-4(h-L3)+k*L3 (=W)": lambda r, Q3, k: r["W"],
         "V3: Q3-3h": lambda r, Q3, k: Q3 - 3 * r["h"],
         "V4: Q3-4d4": lambda r, Q3, k: Q3 - 4 * (r["h"] - r["y"]),
         "V5: Q3-(k+4)d4/k*? (Q3*k-4k d4+... ) Q3+k*y-4*(h-y)-k*(y-1)": lambda r, Q3, k: Q3 - 4 * (r["h"] - r["y"]) + k}
mins = {c: (10 ** 9, None) for c in cands}; n = 0
for m, B in gen():
    r = jid.info(m, B)
    if not r or r["h"] <= r["e"]: continue
    n += 1; k = r["e"] - 1
    Q3 = r["W"] - (k * r["y"] - 4 * (r["h"] - r["y"]))
    for c, f in cands.items():
        v = f(r, Q3, k)
        if v < mins[c][0]: mins[c] = (v, dict(m=m, B=r["B"], h=r["h"], y=r["y"], W=r["W"], Q3=Q3, p=r["p"], q=r["q"], H4=r["H4"]))
print(sys.argv[1:], "S with h > e:", n)
for c in cands: print(" ", c, "min", mins[c])
