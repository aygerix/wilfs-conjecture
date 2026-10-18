# incidence-forest tests: bipartite graph (cells of chosen types) x (maxima), edges = cell -> its maximal tops
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
E = [(1,0,0),(0,1,0),(0,0,1)]
add = lambda x,e: (x[0]+e[0],x[1]+e[1],x[2]+e[2])
def cells(D):
    best = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        b = sum(x)
        for e in E:
            z = add(x,e)
            if z in D: b = max(b, best[z])
        best[x] = b
    ht = {x: best[x]-sum(x) for x in D}
    Max = {x for x in D if ht[x] == 0}
    def top(x,a):
        while add(x,E[a]) in D: x = add(x,E[a])
        return x
    out = []
    for x in D:
        if x in Max: continue
        tp = [top(x,a) for a in range(3)]
        mt = [z for z in tp if z in Max]
        n = len(mt); hh = sum(ht[z] for z in tp)
        if n == 3: out.append(('T', x, mt))
        elif n == 2 and hh == 1:
            c = [a for a in range(3) if tp[a] not in Max][0]
            out.append(('U' if tp[c] == x else 'O', x, mt))
    return Max, out
def excess(Max, edges):   # cyclomatic number of bipartite incidence graph
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: par[u] = par[par[u]]; u = par[u]
        return u
    cyc = 0
    for (cell, ms) in edges:
        for y in ms:
            a, b = f(('c', cell)), f(('m', y))
            if a == b: cyc += 1
            else: par[a] = b
    return cyc
if __name__ == '__main__':
    M = int(sys.argv[1]); worst = {}
    for key, D, C in gen(M):
        Max, cl = cells(D)
        for name, types in [('T', 'T'), ('TO', 'TO'), ('TU', 'TU'), ('TOU', 'TOU'), ('O', 'O'), ('OU', 'OU')]:
            ed = [(x, ms) for (k, x, ms) in cl if k in types]
            cy = excess(Max, ed)
            if name not in worst or cy > worst[name][0]: worst[name] = (cy, key)
    for k, v in worst.items(): print('cycles in incidence graph', k, v)
    