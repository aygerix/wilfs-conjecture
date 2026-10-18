# Checks the claims of the Fiber Lemma on cone sets:
#  (A) every doubly-same qO cell x (nonmax dir c, max dirs a, b) lies in B_c = {x_a >= q_a, x_b >= q_b, x_c < q_c};
#  (B) no two doubly-same cells share a maximal top in the same direction;
#  (C) cells whose cycle-closing is due to a cross share number <= |Y|;
#  (D) rank(G_O) <= #cross-only + #doubly-same and qO <= t - 1 + rank.  NOTE (review 2026-10-18): 'Drank' holds by construction
#      and 'Dq' is the identity qO = t - comp + rank, so (D) adds no information; the real tests are (A)-(C) and (E).
#  (E) #DS <= t + |Y|, #cross-only closers <= |Y|, and the theorem's bound qO <= 2t - 1 + 2|Y| (=> 2t + 11 when |Y| <= 6).
import sys, json
sys.path.insert(0, 'src/scratch')
from qo_cone import add, E
def check(D, q):
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
    inK = lambda z: all(z[i] >= q[i] for i in range(3))
    Y = {y for y in Max if any(inK(add(y, E[d])) for d in range(3))}
    qO = {}
    for x in D:
        if x in Max: continue
        tp = [top[(x, a)] for a in range(3)]
        if sum(1 for z in tp if z in Max) == 2 and sum(ht[z] for z in tp) == 1:
            c = next(a for a in range(3) if tp[a] not in Max)
            if tp[c] != x: qO[x] = c
    viol = []
    DS = []
    for x, c in qO.items():
        dirs = [a for a in range(3) if a != c]
        if all(any(qO.get(u) is not None and u != x and u[a] < x[a] and top[(u, a)] == top[(x, a)] for u in qO) for a in dirs):
            DS.append(x)
            a, b = dirs
            if not (x[a] >= q[a] and x[b] >= q[b] and x[c] < q[c]): viol.append(('A', x, c))
    seen = {}
    for x in DS:
        for a in range(3):
            if a == qO[x]: continue
            k = (a, top[(x, a)])
            if k in seen: viol.append(('B', x, seen[k], a))
            seen[k] = x
    # elimination / union-find in increasing |x|
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: par[u] = par[par[u]]; u = par[u]
        return u
    used = {}; cross_only = 0; ds_close = 0; rank = 0; DSs = set(DS)
    for x in sorted(qO, key=sum):
        c = qO[x]; a, b = [d for d in range(3) if d != c]
        u, v = f(top[(x, a)]), f(top[(x, b)])
        if u == v:
            rank += 1
            if x in DSs: ds_close += 1
            else:
                cross_only += 1
                if not any(top[(x, d)] in Y for d in (a, b)): viol.append(('C', x))
        else: par[u] = v
    t = len(Max)
    if rank > cross_only + ds_close: viol.append(('Drank',))
    if len(qO) > t - 1 + rank: viol.append(('Dq',))
    if len(DS) > t + len(Y): viol.append(('E-ds', len(DS), t, len(Y)))
    if cross_only > len(Y): viol.append(('E-cross', cross_only, len(Y)))
    if len(qO) > 2 * t - 1 + 2 * len(Y): viol.append(('final', len(qO), t, len(Y)))
    return viol, len(DS), cross_only, rank, len(qO) - t, len(Y)
if __name__ == '__main__':
    from cls_anneal import build
    if sys.argv[1] == 'tiles':
        from tile_dump import rebuild
        for m in map(int, sys.argv[2:]):
            nv = 0; mx = [0, 0, 0]; n = 0
            for l in open(f'logs/tiles/m{m}.jsonl'):
                d = json.loads(l)
                if not d['q']: continue
                viol, nds, co, rk, qt, ny = check(rebuild(d['h'], d['F'], d['G'], d['q']), tuple(d['q'])); n += 1
                if viol: nv += 1; print('  VIOL', viol[:3], d['h'], d['F'], d['G'], d['q'])
                mx = [max(mx[0], nds), max(mx[1], co), max(mx[2], ny)]
            print(m, 'cone tiles', n, 'violating', nv, 'max #DS', mx[0], 'max cross-only closers', mx[1], 'max |Y|', mx[2], flush=True)
    else:
        h, F, G, q = [eval(a) for a in sys.argv[1:5]]
        print(check(build(h, F, G, q), q))
