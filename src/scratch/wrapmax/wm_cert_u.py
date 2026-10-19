"""H1' on EVERY labeling of every 4-D lattice tile: the E153 certificates list one residue vector r per lattice up to
units, so loop over all units u (labels u*r mod m; same tile D, same lattice).  Every phase.
usage: python wm_cert_u.py mlo mhi certdir"""
import gzip, json, sys
from math import gcd
from wm_pay import instances
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for m in range(mlo, mhi+1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    nt = nwm = ninst = fail = 0; worst = None
    with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r0 = [x % m for x in rec['r']]
            if 0 in r0: continue
            for Dl in rec['tile_cells']:
                D = list(map(tuple, Dl))
                for u in units:
                    r = [(u*x) % m for x in r0]; nt += 1
                    res = instances(m, r, D)
                    if res is None: continue
                    nwm += 1
                    for R in res:
                        ninst += 1; slack = R['beta']+R['tauplus']-len(R['F'])
                        if slack < 0:
                            fail += 1
                            if fail <= 3: print("FAIL", R, "D", sorted(D), flush=True)
                        if worst is None or slack < worst[0]: worst = (slack, R['r0'], r, len(R['F']))
    print("m=%d labelled_tiles=%d wrapmax=%d inst_with_F=%d H1'_fail=%d min_slack=%s" % (m, nt, nwm, ninst, fail, worst), flush=True)
