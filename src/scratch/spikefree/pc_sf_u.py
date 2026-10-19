"""H-SF test: does Tile-CL (= PC, S >= Lam_r) hold at every phase on every SPIKE-FREE tile (no unit e_b maximal)?
All 4-D tiles of the E153 certificates, every labeling u*r (all units u), every phase. Numpy over phases.
usage: python pc_sf_u.py mlo mhi certdir"""
import gzip, json, sys
from math import gcd
import numpy as np
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
d = 4
for m in range(mlo, mhi+1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    M1 = m*(m-1)//2
    nt = nsf = 0; fail_sf = fail_spk = 0; fails_by_nspk = {}; worst_sf = None; ex = []
    with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r0v = [x % m for x in rec['r']]
            if 0 in r0v: continue
            for Dl in rec['tile_cells']:
                D = list(map(tuple, Dl)); Ds = set(D); idx = {x: i for i, x in enumerate(D)}
                up = lambda x, a: tuple(x[i]+(i == a) for i in range(d))
                Amask = [all(up(y, a) not in Ds for a in range(d)) for y in D]
                nspk = sum(1 for a in range(d) if tuple(int(i == a) for i in range(d)) in Ds
                           and Amask[idx[tuple(int(i == a) for i in range(d))]])
                wA = np.array([(d+sum(y)) if Amask[i] else 0 for i, y in enumerate(D)], dtype=np.int64)
                lam = np.zeros(len(D), dtype=np.int64)       # sum of |C| over non-max tops
                for b in range(d):
                    for t in D:
                        if up(t, b) in Ds or Amask[idx[t]]: continue
                        lam[idx[t]] += t[b]+1
                X = np.array(D, dtype=np.int64)
                ph = np.arange(m, dtype=np.int64)[:, None]
                for u in units:
                    P = np.array([(u*x) % m for x in r0v], dtype=np.int64); nt += 1
                    v = X @ P
                    R = (v[None, :] + ph) % m
                    S = (d+1)*M1 - R @ wA; Lam = R @ lam
                    sl = S - Lam; mn = int(sl.min())
                    if nspk == 0:
                        nsf += 1
                        if worst_sf is None or mn < worst_sf[0]: worst_sf = (mn, P.tolist(), int(sl.argmin()))
                    if mn < 0:
                        fails_by_nspk[nspk] = fails_by_nspk.get(nspk, 0)+1
                        if nspk == 0:
                            fail_sf += 1
                            if len(ex) < 3: ex.append((P.tolist(), int(sl.argmin()), mn, sorted(D)))
    print("m=%d labelled=%d spikefree=%d PC_fail_by_nspikes=%s spikefree_fail=%d min_spikefree_slack=%s" % (
        m, nt, nsf, dict(sorted(fails_by_nspk.items())), fail_sf, worst_sf), flush=True)
    for e in ex: print("  SF-FAIL P", e[0], "rho0", e[1], "slack", e[2], "D", e[3], flush=True)
