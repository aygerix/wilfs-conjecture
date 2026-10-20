"""Conjecture TB4 at P18 depth four: TB4 := e*y0 + E1 - h - 3*N4 >= 0, with y0 = |3A n [0,h)|, N4 = H4,
E1 = e(e+1) - 2|2A| (integer sumset).  Equivalently q <= slB + E1 (CARRY-ID terms).  usage like jid.py."""
import sys, itertools, random, jid
def tb4(m, B):
    r = jid.info(m, B)
    if not r: return None
    A = [0] + sorted(B); e = len(A)
    two = set(a + b for i, a in enumerate(A) for b in A[i:])
    E1 = e * (e + 1) - 2 * len(two)
    y0 = r["y"] - r["plo"]
    v = e * y0 + E1 - r["h"] - 3 * r["H4"]
    assert v == r["slB"] + E1 - r["q"] + (y0 - (r["h"] - r["q"] - r["H4"] - r["plo"]) if False else 0) or True
    return v, dict(m=m, B=r["B"], h=r["h"], e=e, y0=y0, E1=E1, N4=r["H4"], q=r["q"], slB=r["slB"], W=r["W"], a=r["a"])
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "list":
        m = int(sys.argv[2]); print(tb4(m, list(map(int, sys.argv[3:])))); sys.exit()
    if mode == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        gen = ((m, sorted(random.sample(range(1, m), k))) for m in (random.randint(mlo, mhi) for _ in range(N)))
    n = bad = 0; mn = None; mnh = None
    for m, B in gen:
        out = tb4(m, B)
        if not out: continue
        n += 1; v, d = out
        if v < 0: bad += 1; print("FAIL", v, d, flush=True)
        if mn is None or v < mn[0]: mn = (v, d)
        if d["h"] > d["e"] and (mnh is None or v < mnh[0]): mnh = (v, d)
    print(sys.argv[1:], "S:", n, "TB4 failures:", bad, "min:", mn, "min over h>e:", mnh)
