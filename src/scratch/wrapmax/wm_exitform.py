"""Exit-edge version of H1' (stronger than the shadow version):  Ex(D'_theta) + sum_{y in V, lambda>=theta}(|y|-1) >= |V_theta|
for every theta, on all labelings u*r of all 4-D certificate tiles.  usage: python wm_exitform.py mlo mhi certdir"""
import gzip, json, sys
from math import gcd
from wm_suff import check
mlo, mhi, cdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for m in range(mlo, mhi+1):
    units = [u for u in range(1, m) if gcd(u, m) == 1]
    nwm = fail_ex = fail_out = 0; ex = None
    with gzip.open(f'{cdir}/certificate_all_{m}.jsonl.gz', 'rt') as f:
        for line in f:
            rec = json.loads(line); r0 = [x % m for x in rec['r']]
            if 0 in r0: continue
            for Dl in rec['tile_cells']:
                D = list(map(tuple, Dl))
                for u in units:
                    P = [(u*x) % m for x in r0]
                    res = check(m, P, D)
                    if res is None: continue
                    nwm += 1
                    # res tuple: (H1'_out_slack, Out-|V|, Ex-|V|, theta, |V_th|); rest = H1'_out - (Out-|V|)
                    bad_ex = [t for t in res if t[2]+(t[0]-t[1]) < 0]
                    if any(t[0] < 0 for t in res): fail_out += 1
                    if bad_ex:
                        fail_ex += 1
                        if ex is None: ex = (P, bad_ex[0], sorted(D))
    print("m=%d wrapmax_labelled_tiles(V nonempty)=%d H1'(Out)_fail=%d exit-version_fail=%d first=%s" % (m, nwm, fail_out, fail_ex, ex), flush=True)
