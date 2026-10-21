"""R, RT, RT2, RT3, UA, UA2, UA3, TX and W on generator lists, one per line (python list syntax) (lead, 2026-10-21).
usage: /usr/bin/python3 rt3list.py FILE"""
import sys, ast
sys.path.insert(0, '.')
from rt2lib import data, relax
K = ('RT', 'RT2', 'RT3', 'UA', 'UA2', 'UA3', 'TX')
for line in open(sys.argv[1]):
    line = line.strip()
    if not line.startswith('['): continue
    G = ast.literal_eval(line); D = data(G); R = relax(D, K)
    print("m=%d e=%d c=%d q=%d rho=%d h=%d W=%d |" % (D['m'], D['e'], D['c'], D['q'], D['rho'], D['h'], D['W']),
          " ".join("%s=%.2f" % (k, R[k]) for k in K), "| RT2/W=%.3f RT3/W=%.3f UA2/W=%.3f" % (R['RT2'] / D['W'], R['RT3'] / D['W'], R['UA2'] / D['W']),
          "G=%s" % G, flush=True)
