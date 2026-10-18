# Do the C-lemmas (S: same-direction sharing; P: tripod projection chain; A: no tripods beyond x on two rays;
# Q2: no qO cells below x on both max rays; qU forest) hold verbatim on real cone tiles?
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_cone_peel import qstars
from collections import defaultdict, Counter
def add(x, a, d=1): y = list(x); y[a] += d; return tuple(y)
def check(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    Max = {x for x in D if ht[x] == 0}
    tri, qO, qU = [], [], []
    for x in D:
        if x in Max: continue
        tp = [top(x, a) for a in range(3)]; hs = [ht[z] for z in tp]; n = sum(1 for z in hs if z == 0)
        if n == 3: tri.append((x, tp))
        elif n == 2 and sum(hs) == 1:
            c = next(a for a in range(3) if hs[a] == 1)
            (qU if tp[c] == x else qO).append((x, tp, c))
    bad = Counter()
    inc = defaultdict(set)
    for x, tp in tri:
        for a in range(3): inc[tp[a]].add(a)
    for x, tp, c in qO:
        for a in range(3):
            if a != c: inc[tp[a]].add(a)
    bad['S'] = sum(1 for s in inc.values() if len(s) > 1)
    T = [x for x, tp in tri]
    bad['P'] = sum(1 for (a, b) in [(0,1),(0,2),(1,2)] for x in T for y in T if x[a] < y[a] and x[b] > y[b])
    Tset = set(T)
    for x, tp in tri:
        dirs = [a for a in range(3) if any(add(x, a, i) in Tset for i in range(1, tp[a][a] - x[a] + 1))]
        if len(dirs) > 1: bad['A'] += 1
    Oset = {x: (tp, c) for x, tp, c in qO}
    for x, tp, c in qO:
        dirs = [a for a in range(3) if a != c and any(add(x, a, -i) in Oset and Oset[add(x, a, -i)][0][a] == tp[a] for i in range(1, x[a] + 1))]
        if len(dirs) > 1: bad['Q2'] += 1
    # qU forest: edges {x+e_a, x+e_b}
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: par[u] = par[par[u]]; u = par[u]
        return u
    cyc = 0
    for x, tp, c in qU:
        u, v = [add(x, a) for a in range(3) if a != c]
        if f(u) == f(v): cyc += 1
        else: par[f(u)] = f(v)
    bad['qUcyc'] = cyc
    return bad, len(Max), len(tri), len(qO), len(qU)
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        tot = Counter(); ex = {}; n = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            D = set(D); Q = qstars(D); kind = 'cone' if Q else 'C'
            bad, t, tr, qo, qu = check(D); n += 1
            for k, v in bad.items():
                if v: tot[(kind, k)] += 1; ex.setdefault((kind, k), (r, Q))
        print(f'm={m} tiles {n}: sets violating each lemma {dict(tot)}; ex {ex}', flush=True)
