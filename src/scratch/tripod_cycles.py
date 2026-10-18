# Tripod incidence graph B (tripods -- their 3 maximal tops): cycle rank r(B) = 2T - t_B + kappa; 2T <= t - 1 + r(B).
# For a cone set, list tripods with tops (direction-labelled), floor maxima Y_c = {y in Max : y + e_c in K}, and a cycle basis.
import sys
sys.path.insert(0, 'src/scratch'); sys.path.insert(0, 'src/scratch/forest')
from is_tile import build
E = [(1,0,0),(0,1,0),(0,0,1)]
def add(x, e, s=1): return tuple(x[i] + s*e[i] for i in range(3))
def analyze(h, F, G, q, verbose=True):
    D = build(h, F, G, q)
    Max = {x for x in D if all(add(x, e) not in D for e in E)}
    def top(x, a):
        while add(x, E[a]) in D: x = add(x, E[a])
        return x
    inK = lambda z: q is not None and all(z[i] >= q[i] for i in range(3))
    Y = {y: [c for c in range(3) if inK(add(y, E[c]))] for y in Max}
    Y = {y: c for y, c in Y.items() if c}
    tri = []
    for x in D:
        if x in Max: continue
        tp = [top(x, a) for a in range(3)]
        if all(z in Max for z in tp): tri.append((x, tp))
    # union-find for cycle rank
    par = {}
    def f(u):
        par.setdefault(u, u)
        while par[u] != u: par[u] = par[par[u]]; u = par[u]
        return u
    extra = []
    for x, tp in tri:
        for a in range(3):
            u, v = f(('T', x)), f(('M', tp[a]))
            if u == v: extra.append((x, a, tp[a]))
            else: par[u] = v
    tB = len({z for _, tp in tri for z in tp})
    if verbose:
        print(f'm={len(D)} t={len(Max)} T={len(tri)} tB={tB} cycle rank={len(extra)}  2T-t={2*len(tri)-len(Max)}  q={q}')
        print('  floor maxima Y:', Y)
        for x, tp in sorted(tri, key=lambda z: -sum(z[0])):
            print('  tripod', x, 'tops', tp, ['Y%d' % Y[z][0] if z in Y else '' for z in tp])
        print('  cycle-closing edges (tripod, dir, top):', extra)
    return len(extra)
if __name__ == '__main__':
    analyze(eval(sys.argv[1]), eval(sys.argv[2]), eval(sys.argv[3]), eval(sys.argv[4]))
