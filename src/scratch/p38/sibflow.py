# sibflow: max-flow test of Q3T by sibling slots.  Demand: Q1' class 1, M2' class 2 (total |Q3| + t).  Supply: missing
# slots (x, l) of standard squares x (capacity x_l + 1) and missing squares (capacity 4).  Edges: class s (rep y) -> slot
# (x, l) if x = y - e_i is a parent of y; -> missing square q if q = y - e_i + e_l - e_j ... (rule SIB2: missing squares
# sharing a part with y).  Uses Dinic from flowdiv.py.
import sys
from itertools import combinations_with_replacement as cwr
exec(open('flowdiv.py').read().split('def analyse')[0])
def run(m, A, rule):
    d = len(A); e = d + 1
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl][0]: best[cl] = (key, c)
    sg = {cl: best[cl][0][0] + best[cl][0][1] * m for cl in best}; rep = {cl: best[cl][1] for cl in best}
    D = set(rep.values())
    dem = {}
    for c in sg:
        if sg[c] >= 2 * m: dem[c] = 2
        elif sg[c] >= m and len(rep[c]) == 3 and not any(A[l] > c for l in rep[c]): dem[c] = 1
    nodes = {'S': 0, 'T': 1}; edges = []
    def node(k):
        if k not in nodes: nodes[k] = len(nodes)
        return nodes[k]
    slotcap = {}
    for x in D:
        if len(x) != 2: continue
        for l in range(d):
            y = tuple(sorted(x + (l,)))
            if y not in D: slotcap[(x, l)] = x.count(l) + 1
    msq = [q for q in cwr(range(d), 2) if q not in D]
    for k, cap in slotcap.items(): edges.append((0, node(('sl',) + k), cap))
    for q in msq: edges.append((0, node(('mq', q)), 4))
    tot = 0
    for c, dm in dem.items():
        y = rep[c]; nc = node(('c', c)); edges.append((nc, 1, dm)); tot += dm
        if rule == 'SIB3':
            for (x, l) in slotcap:
                if set(x) & set(y): edges.append((node(('sl', x, l)), nc, 10 ** 6))
        else:
          for i in set(y):
            x = list(y); x.remove(i); x = tuple(x)
            for l in range(d):
                if (x, l) in slotcap: edges.append((node(('sl', x, l)), nc, 10 ** 6))
        if rule in ('SIB2', 'SIB3'):
            for q in msq:
                if set(q) & set(y): edges.append((node(('mq', q)), nc, 10 ** 6))
    f = maxflow(len(nodes), edges, 0, 1) if tot else 0
    return tot, f
rule = sys.argv[1]
for fn in sys.argv[2:]:
    n = bad = 0; worst = None
    for L in open(fn):
        tk = L.split()
        if tk[0] != 'DUMP': continue
        m = int(tk[1]); A = list(map(int, tk[15:])); n += 1
        tot, f = run(m, A, rule)
        if f < tot:
            bad += 1
            if worst is None or tot - f > worst[0]: worst = (tot - f, tot, m, A)
    print(rule, fn, n, 'S; unsaturated', bad, 'worst', worst)
