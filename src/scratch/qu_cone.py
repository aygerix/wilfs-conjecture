# qU graph G_U on cone sets (edge {x+e_a, x+e_b} per qU cell x; x+e_c not in D): cycle rank, and the number of
# cross-level edges per level transition v -> v+1 in direction 3 (claim: <= 2 for v != q3, <= 4 at v = q3).
import sys, json
sys.path.insert(0, 'src/scratch')
from qo_cone import add, E
def qu_stats(D, q):
    best = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        b = sum(x)
        for e in E:
            z = add(x, e)
            if z in D and best[z] > b: b = best[z]
        best[x] = b
    ht = {x: best[x] - sum(x) for x in D}
    Max = {x for x in D if ht[x] == 0}
    edges = []; cross = {}
    for x in D:
        if x in Max: continue
        out = [d for d in range(3) if add(x, E[d]) not in D]
        if len(out) != 1: continue
        c = out[0]; a, b = [d for d in range(3) if d != c]
        if add(x, E[a]) in Max and add(x, E[b]) in Max:
            edges.append((add(x, E[a]), add(x, E[b])))
            if c != 2: cross[x[2]] = cross.get(x[2], 0) + 1
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: par[u] = par[par[u]]; u = par[u]
        return u
    rank = 0
    for u, v in edges:
        u, v = f(u), f(v)
        if u == v: rank += 1
        else: par[u] = v
    bad = [(z, k) for z, k in cross.items() if k > (4 if q and z == q[2] - 1 else 2)]
    return len(edges), len(Max), rank, bad
if __name__ == '__main__':
    from tile_dump import rebuild
    for m in map(int, sys.argv[1:]):
        mx = [0, -99]; nb = 0
        for l in open(f'logs/tiles/m{m}.jsonl'):
            d = json.loads(l)
            if not d['q']: continue
            qu, t, r, bad = qu_stats(rebuild(d['h'], d['F'], d['G'], d['q']), tuple(d['q']))
            mx = [max(mx[0], r), max(mx[1], qu - t)]; nb += bool(bad)
            if bad: print('  BAD', bad, d)
        print(m, 'max rank G_U', mx[0], 'max qU-t', mx[1], 'level-count violations', nb, flush=True)
