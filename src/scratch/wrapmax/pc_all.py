"""Pure-counting MaxCL (PC): S(sigma) >= Lam_r(sigma) for EVERY tile and phase, i.e.
  sum_{j>=1} sum_b |B_b(U'_j)| >= sum_{j>=1} |U_j|,  U_j = {v >= jm}, U'_j = {v >= jm - rho0}  (canonical lift v = x.P).
Tested on all 4-D tiles of the E153 certificates.  usage: python pc_all.py mlo mhi certdir"""
import gzip, json, sys
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for m in range(mlo, mhi+1):
    nt = fail = 0; worst = None; failwm = 0
    with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); P = [x % m for x in rec['r']]
            if 0 in P: continue
            d = 4
            for Dl in rec['tile_cells']:
                D = list(map(tuple, Dl)); Ds = set(D); nt += 1
                up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
                A = set(y for y in D if all(up(y, a) not in Ds for a in range(d)))
                v = {x: sum(x[i]*P[i] for i in range(d)) for x in D}
                cols = []
                for b in range(d):
                    for t in D:
                        if up(t, b) in Ds: continue
                        col = [t]; y = list(t)
                        while y[b] > 0: y[b] -= 1; col.append(tuple(y))
                        cols.append((t, col))
                M1 = m*(m-1)//2
                for r0 in range(m):
                    r = {x: (v[x]+r0) % m for x in D}
                    S = (d+1)*M1-sum((d+sum(y))*r[y] for y in A)
                    Lam = sum(len(col)*r[t] for (t, col) in cols if t not in A)
                    if S < Lam:
                        fail += 1
                        wm = all(v[x] < m for x in D if x not in A); failwm += wm
                        if fail <= 2: print("PC FAIL m", m, "P", P, "rho0", r0, "S", S, "Lam", Lam, "wrapmax", wm, "D", sorted(D), flush=True)
                    q = (S-Lam)/m
                    if worst is None or q < worst[0]: worst = (q, P, r0)
    print("m=%d tiles=%d PC_fail(tile,phase)=%d of_which_wrapmax=%d min (S-Lam)/m=%s" % (m, nt, fail, failwm, worst), flush=True)
