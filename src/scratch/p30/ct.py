"""Claim CT (regime 2h <= m, P18 depth four; lead, 2026-10-20): for a residual carried triple r (every representation
r + m = x + y + z has all pair sums >= h), r + h is not core, i.e. r + h in (T_s + B) u CP, T_s = 3A n [0, h).
If CT holds, q <= OVF + p_hi (Z1) by the injection r -> token of r + h (or the carried pair r + h); C_ii pay with their
own pair tokens (sum r + m >= 2h).  Also tests CTall (every carried triple) and reports the injection deficit.
usage: exh k mlo mhi | rnd k mlo mhi N seed"""
import sys, itertools, random, jid
def ev(m, B):
    r = jid.info(m, B)
    if not r or 2 * r["h"] > m: return None
    h = r["h"]; A = [0] + sorted(B)
    X2 = set(a + b for i, a in enumerate(A) for b in A[i:]); X3 = set(s + a for s in X2 for a in A)
    S2 = set(v for v in X2 if v < m) | set(A); T = set(v for v in X3 if v < m) - S2
    CP = set(v - m for v in X2 if v >= m) - S2 - T
    Ts = set(t for t in X3 if t < h)
    TB = set(t + b for t in Ts for b in B)
    fs = set(t + x for t in X3 if t < m for x in B if t + x < m)
    lv = {}
    C = [x for x in range(h) if x not in X3 and x not in CP and x not in fs]
    ts = {}
    for i in range(len(B)):
        for j in range(i, len(B)):
            for l in range(j, len(B)): ts.setdefault(B[i] + B[j] + B[l], []).append((B[i], B[j], B[l]))
    bad_res = bad_all = 0; ex = None
    for x in C:
        assert x + m in ts
        res = all(min(a + b2, a + c2, b2 + c2) >= h for (a, b2, c2) in ts[x + m])
        ok = (x + h) in TB or (x + h) in CP
        if not ok:
            bad_all += 1
            if res: bad_res += 1; ex = ex or (x, ts[x + m])
    return dict(bad_res=bad_res, bad_all=bad_all, m=m, B=tuple(B), h=h, q=len(C), ex=ex)
if __name__ == "__main__":
    if sys.argv[1] == "exh":
        k, mlo, mhi = map(int, sys.argv[2:5]); gen = ((m, B) for m in range(mlo, mhi + 1) for B in itertools.combinations(range(1, m), k))
    else:
        k, mlo, mhi, N, seed = map(int, sys.argv[2:7]); random.seed(seed)
        gen = ((m, sorted(random.sample(range(1, m), k))) for m in (random.randint(mlo, mhi) for _ in range(N)))
    n = fr = fa = 0; shown = 0
    for m, B in gen:
        d = ev(m, B)
        if not d: continue
        n += 1
        if d["bad_res"]: fr += 1
        if d["bad_all"]: fa += 1
        if d["bad_res"] and shown < 6: shown += 1; print("CT fails", d, flush=True)
    print(sys.argv[1:], "S:", n, "CT(res) failures:", fr, "CT(all) failures:", fa)
