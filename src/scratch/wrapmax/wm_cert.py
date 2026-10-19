"""H1' (WRAP-MAX pure counting: beta_N + sum_A tau >= 0, i.e. S >= Lam_r) on EVERY 4-D lattice tile from the E153
certificates (all primitive residue vectors, all tiles), every phase.  Includes tiles outside the e = 5 domain.
usage: python wm_cert.py mlo mhi certdir"""
import gzip, json, sys
from wm_pay import instances
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for m in range(mlo, mhi+1):
    nt = nwm = ninst = fail = 0; worst = None
    with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r = [x % m for x in rec['r']]
            if 0 in r: continue
            for Dl in rec['tile_cells']:
                D = list(map(tuple, Dl)); nt += 1
                res = instances(m, r, D)
                if res is None: continue
                nwm += 1
                for R in res:
                    ninst += 1; slack = R['beta']+R['tauplus']-len(R['F'])
                    if slack < 0:
                        fail += 1
                        if fail <= 3: print("FAIL", R, flush=True)
                    if worst is None or slack < worst[0]: worst = (slack, R['r0'], r, len(R['F']))
    print("m=%d tiles=%d wrapmax=%d inst_with_F=%d H1'_fail=%d min_slack=%s" % (m, nt, nwm, ninst, fail, worst), flush=True)
