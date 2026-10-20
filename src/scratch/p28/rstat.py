r"""Size of the residual class R (carried triples with b1 + b2 >= h) by regime h/m, P18 depth four (lead, 2026-10-20).
Reports max |R|, max |R|/e^2, and max |R| - (#unused tokens (0,x,k)) by regime.  usage: rstat.py rnd k mlo mhi N seed | exh k mlo mhi"""
import sys, itertools, random
from match4 import build
def stat(m, B):
    D = build(m, B)
    if D is None: return None
    w, car, unused, e, g, rep, h = D["w"], D["car"], D["unused"], D["e"], D["g"], D["rep"], D["h"]
    R = 0
    for v in w:
        if car[v] and len(rep[v]) == 3:
            b = sorted(B[i] for i in rep[v])
            if b[0] + b[1] >= h: R += 1
    z = sum(1 for t in unused if t[0] == 0)
    reg = "third" if 3 * h <= m else ("mid" if 2 * h <= m else "half")
    return reg, R, e, z
st = {}
def add(r, m, B):
    reg, R, e, z = r
    s = st.setdefault(reg, [0, 0, 0.0, -10**9, None])
    s[0] += 1; s[1] = max(s[1], R); s[2] = max(s[2], R / e ** 2)
    if R - z > s[3]: s[3] = R - z; s[4] = (m, tuple(B))
if sys.argv[1] == "exh":
    k, mlo, mhi = map(int, sys.argv[2:5])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k):
            r = stat(m, list(B))
            if r: add(r, m, B)
else:
    k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); B = sorted(random.sample(range(1, m), k))
        r = stat(m, B)
        if r: add(r, m, B)
for reg, s in st.items(): print(sys.argv[1:], reg, "S", s[0], "max|R|", s[1], "max|R|/e^2 %.3f" % s[2], "max(|R| - zero-tokens)", s[3], s[4])
