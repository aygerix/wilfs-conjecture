# Tripod budget on dumped cone tiles: 2T - t = (2T - t_B) - (t - t_B) and 2T - t_B = r(B) - kappa (bipartite incidence
# graph B: tripods + used maxima).  Reports joint distribution of (r(B), kappa, t - t_B, #floor maxima unused by tripods).
import sys, json
from collections import Counter
sys.path.insert(0, 'src/scratch')
from tile_dump import rebuild
E = [(1,0,0),(0,1,0),(0,0,1)]
def add(x, e): return (x[0]+e[0], x[1]+e[1], x[2]+e[2])
def budget(d):
    D = rebuild(d['h'], d['F'], d['G'], d['q']); q = d['q']
    Max = {x for x in D if all(add(x, e) not in D for e in E)}
    top = {}
    for a in range(3):
        for x in sorted(D, key=lambda z: -z[a]):
            z = add(x, E[a]); top[(x, a)] = top[(z, a)] if z in D else x
    tri = [x for x in D if x not in Max and all(top[(x, a)] in Max for a in range(3))]
    par = {}
    def f(u):
        par.setdefault(u, u)
        while par[u] != u: par[u] = par[par[u]]; u = par[u]
        return u
    r = 0
    for x in tri:
        for a in range(3):
            u, v = f(('T', x)), f(('M', top[(x, a)]))
            if u == v: r += 1
            else: par[u] = v
    used = {top[(x, a)] for x in tri for a in range(3)}
    kappa = len({f(('T', x)) for x in tri})
    inK = lambda z: all(z[i] >= q[i] for i in range(3))
    Y = {y for y in Max if any(inK(add(y, e)) for e in E)}
    return len(tri), len(Max), r, kappa, len(Max) - len(used), len(Y - used), len(Y)
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        cnt = Counter(); worst = None
        for l in open(f'logs/tiles/m{m}.jsonl'):
            d = json.loads(l)
            if not d['q']: continue
            T, t, r, k, un, unY, nY = budget(d)
            if T == 0: continue
            cnt[(r, k, min(un, 9), unY)] += 1
            if r > 0 and (worst is None or 2*T - t > worst[0]): worst = (2*T - t, d['h'], d['F'], d['G'], d['q'], (T, t, r, k, un, unY, nY))
        print(f'm={m}: (r, kappa, unused maxima, unused floor maxima) -> count:', dict(sorted(cnt.items())))
        print('   worst 2T-t among r>0:', worst)
