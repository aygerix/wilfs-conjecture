r"""Residual U != T at q = 5, height <= 3, level 1 (lead, 2026-10-21): profile min A, |A n [1, m/4)|, ell_U, c_U,
slack e*l_U - c_U, and the smallest slack / c_U ratio.  usage: python resid.py d mlo mhi"""
import sys, itertools, heapq
d, mlo, mhi = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
def apery(mod, G):
    w = [None] * mod; w[0] = 0; h = [(0, 0)]; done = [False] * mod
    while h:
        v, s = heapq.heappop(h)
        if done[s]: continue
        done[s] = True
        for x in G:
            t = (v + x) % mod
            if w[t] is None or v + x < w[t]: w[t] = v + x; heapq.heappush(h, (v + x, t))
    return w
for m in range(mlo, mhi + 1):
    rows = []; nq5 = 0; mono = []
    for A in itertools.combinations(range(1, m), d):
        # quick covering filter
        cov = {0}
        for i in A:
            cov.add(i % m)
            for j in A:
                cov.add((i + j) % m)
                for k in A: cov.add((i + j + k) % m)
        if len(cov) < m: continue
        G = [m + a for a in A]; w = apery(m, G)
        if max(w) >= 6 * m or max(w) < 5 * m: continue
        # height <= 3 for all factorizations: w_s - g in Ap chains; max length via DP in increasing order
        order = sorted(range(m), key=lambda s: w[s]); hmx = {0: 0}; ok = True
        for s in order[1:]:
            best = -1
            for g in G:
                t = (s - g) % m
                if w[t] == w[s] - g: best = max(best, hmx[t] + 1)
            hmx[s] = best
            if best > 3: ok = False; break
        if not ok: continue
        nq5 += 1
        sig = [w[s] - m * hmx[s] for s in range(m)]; tau = apery(m, list(A))
        if sig == tau: continue
        e = d + 1; r = max(range(m), key=lambda s: w[s])
        cU = max(sig) - m + 1; lU = cU - sum(x // m for x in sig)
        cT = max(tau) - m + 1; lT = cT - sum(x // m for x in tau)
        rows.append((e * lU - cU, (e * lU - cU) / cU, min(A), sum(1 for a in A if 4 * a < 2 * m + r), lU, cU, A))
        # e(T): minimal generators of T from its Apery set w.r.t. m
        Ts = set(); N = max(tau) + m
        inT = [False] * (N + 1)
        for x in tau:
            for z in range(x, N + 1, m): inT[z] = True
        Tel = [z for z in range(1, N + 1) if inT[z]]; Tset = set(Tel)
        eT = sum(1 for z in Tel if not any((z - y) in Tset for y in Tel if y <= z // 2))
        WT = eT * lT - cT if cT > 0 else 0
        mono.append(((e * lU - cU) - WT, eT, A))
    rows.sort()
    mono.sort()
    print("d=%d m=%d q5-S=%d residual(U!=T)=%d  MONO* min We(U)-W(T) (e_T) = %s" % (d, m, nq5, len(rows), mono[0] if mono else None), flush=True)
    for x in rows[:3]: print("   slack=%d ratio=%.3f minA=%d #a<(2m+r)/4=%d lU=%d cU=%d A=%s" % x, flush=True)
