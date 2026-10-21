"""RT3 on the S of obs3 files where RT2 equals the RT window fake, and on a fixed list (lead, 2026-10-21).
usage: /usr/bin/python3 rt3chk.py FILE..."""
import sys, re, ast
sys.path.insert(0, '.')
from rt2lib import data, relax
W5 = ('RT', 'RT2', 'RT3', 'UA', 'UA2', 'UA3')
def show(G, tag=''):
    D = data(G); R = relax(D, W5)
    print(tag, "m=%d e=%d c=%d q=%d rho=%d h=%d W=%d |" % (D['m'], D['e'], D['c'], D['q'], D['rho'], D['h'], D['W']),
          " ".join("%s=%.3f" % (k, R[k]) for k in W5), "G=%s" % sorted(G), flush=True)
    return D, R
for G in ([37, 75, 78, 80, 88, 89], [55, 76, 77, 81, 83, 91, 94], [55, 71, 79, 83, 90, 92, 93], [15, 21, 29, 32],
          [13, 17, 27, 36], [16, 19, 21], [13, 17, 20], [77, 102, 111, 121, 126, 133, 134, 137]):
    show(G, 'list')
for f in sys.argv[1:]:
    n = 0
    for line in open(f):
        mm = re.match(r's=\[([0-9, ]+)\] K=\(([0-9, ]+)\) (\{.*\})', line.strip())
        if not mm: continue
        d = ast.literal_eval(mm.group(3))
        if not (d.get('window_RT2') and abs(d['RT2'] - d['window']) < 1e-6): continue
        s = [int(t) for t in mm.group(1).split(',')]; K = [int(t) for t in mm.group(2).split(',') if t.strip()]
        m = d['m']; show([m] + [m * k + x for k, x in zip(K, s)], f); n += 1
        if n >= 8: break
