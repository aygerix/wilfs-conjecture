# qO structure on cone sets: elimination excess (increasing |x|), cycle rank of the qO graph G_O on Max
# (edge {top_a x, top_b x} per qO cell, a, b its maximal-top directions), defect types of doubly-same cells
# (1a: x' = x - i e_a has nonmax dir b and top_c(x') + e_a in K; 1b: x' has nonmax dir c, proj(x) in quadrant, proj(x') not),
# and the per-column multiplicity (# doubly-same qO cells on one c-line).
# usage as module: qo_stats(D, q) ; CLI: anneal target in {exc, rank, col} over RCON (Wall+Floor) sets.
import sys, random, math
sys.path.insert(0, 'src/scratch')
from cls_anneal import build, stats
from corner_anneal import valid, mutate, msize
E = [(1,0,0),(0,1,0),(0,0,1)]
def add(x, e, k=1): return (x[0]+k*e[0], x[1]+k*e[1], x[2]+k*e[2])
def qo_stats(D, q):
    best = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        b = sum(x)
        for e in E:
            z = add(x, e)
            if z in D and best[z] > b: b = best[z]
        best[x] = b
    ht = {x: best[x] - sum(x) for x in D}
    Max = {x for x in D if ht[x] == 0}
    top = {}
    for a in range(3):
        for x in sorted(D, key=lambda z: -z[a]):
            z = add(x, E[a]); top[(x, a)] = top[(z, a)] if z in D else x
    inK = lambda z: q is not None and all(z[i] >= q[i] for i in range(3))
    qO = {}
    for x in D:
        if x in Max: continue
        tp = [top[(x, a)] for a in range(3)]
        if sum(1 for z in tp if z in Max) == 2 and sum(ht[z] for z in tp) == 1:
            c = next(a for a in range(3) if tp[a] not in Max)
            if tp[c] != x: qO[x] = c
    # elimination by increasing |x|
    seen = {}; exc = 0; dbl = []
    for x in sorted(qO, key=sum):
        c = qO[x]; dirs = [a for a in range(3) if a != c]
        same = 0; cross = 0
        for a in dirs:
            y = top[(x, a)]
            if y in seen:
                if a in seen[y]: same += 1
                else: cross += 1
        exc += cross + max(0, same - 1)
        if same == 2: dbl.append(x)
        for a in dirs: seen.setdefault(top[(x, a)], set()).add(a)
    # cycle rank of G_O via union-find
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: par[u] = par[par[u]]; u = par[u]
        return u
    rank = 0
    for x, c in qO.items():
        a, b = [d for d in range(3) if d != c]
        u, v = f(top[(x, a)]), f(top[(x, b)])
        if u == v: rank += 1
        else: par[u] = v
    col = {}
    for x in dbl:
        c = qO[x]; key = (c, tuple(x[i] for i in range(3) if i != c)); col[key] = col.get(key, 0) + 1
    return dict(t=len(Max), qO=len(qO), exc=exc, rank=rank, ndbl=len(dbl), col=max(col.values()) if col else 0)
INIT = None
def run(name, M0, M1, iters, seed, pw=False):
    from lattice_pairwise import feasible
    rnd = random.Random(seed)
    h, F, G, q = [3, 2, 2], [3, 2, 2], [3, 2, 2], [1, 1, 1]
    if INIT: h, F, G, q = [list(v) for v in INIT]
    cur = None; best = (-1e9, None)
    for it in range(iters):
        T = max(0.05, 2.0 * (1 - it / iters))
        nh, nF, nG, nq = mutate(h, F, G, q, rnd)
        if not valid(nh, nF, nG, nq, 'cone'): continue
        m = msize(nh, nF, nG, nq)
        if m > 2 * M1: continue
        D = build(nh, nF, nG, nq); s = qo_stats(D, nq)
        if name in ('trk', 'texc'): s['C'] = stats(D)['C']
        v = {'exc': s['exc'], 'rank': s['rank'], 'col': s['col'], 'qO-t': s['qO'] - s['t'], 'ndbl': s['ndbl'], 'rk-t': s['rank'] + s['qO'] - s['t'], 'trk': s.get('C') is not None and s['t'] + s['rank'] - s['C'], 'texc': s.get('C') is not None and s['t'] + s['exc'] - s['C']}[name]
        pen = 0 if M0 <= m <= M1 else -abs(m - (M0 if m < M0 else M1)) * 0.3
        sc = v + pen
        if cur is None or sc >= cur or rnd.random() < math.exp((sc - cur) / T):
            if pw and not feasible(tuple(nh), tuple(nF), tuple(nG), tuple(nq)): continue
            h, F, G, q, cur = nh, nF, nG, nq, sc
            if pen == 0 and v > best[0]: best = (v, (tuple(h), tuple(F), tuple(G), tuple(q), s))
    return best
if __name__ == '__main__':
    name, M0, M1, iters, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    pw = len(sys.argv) > 6 and sys.argv[6] == 'pw'
    if len(sys.argv) > 7: INIT = eval(sys.argv[7])
    print(name, M0, M1, 'seed', seed, 'PW' if pw else 'RCON', 'best', run(name, M0, M1, iters, seed, pw), flush=True)
