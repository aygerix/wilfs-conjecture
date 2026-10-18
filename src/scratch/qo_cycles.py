# Classify the cycle-closing qO cells (union-find in increasing |x| order) on cone sets:
#  'cross'  : one of its maximal tops was used earlier by a qO cell in another direction (then that top is a floor max, S')
#  'same2'  : both tops used earlier in the same directions (doubly-same; the C-proof of QF forbids this)
#  'fresh?' : impossible (a cycle-closing edge has both endpoints already present)
# For 'same2' also report the defect type of each partner (1a: partner's nonmax dir is the other maximal dir and
# partner's c-top touches K; 1b: partner's nonmax dir is c and proj(x) in the c-quadrant, proj(partner) not).
import sys, json
sys.path.insert(0, 'src/scratch')
from qo_cone import add, E
def analyze(D, q):
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
    qO = {}
    for x in D:
        if x in Max: continue
        tp = [top[(x, a)] for a in range(3)]
        if sum(1 for z in tp if z in Max) == 2 and sum(ht[z] for z in tp) == 1:
            c = next(a for a in range(3) if tp[a] not in Max)
            if tp[c] != x: qO[x] = c
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: par[u] = par[par[u]]; u = par[u]
        return u
    seen = {}; out = []
    for x in sorted(qO, key=sum):
        c = qO[x]; a, b = [d for d in range(3) if d != c]
        kinds = []
        for d in (a, b):
            y = top[(x, d)]
            kinds.append('new' if y not in seen else ('same' if d in seen[y] else 'cross'))
        u, v = f(top[(x, a)]), f(top[(x, b)])
        if u == v:
            if 'cross' in kinds: out.append(('cross', x))
            else:
                # c-top in floor? (top_c(x) + e_c in K)
                fl = inK(add(top[(x, c)], E[c]))
                out.append(('same2', x, 'floor' if fl else 'nofloor', c))
        else: par[u] = v
        for d in (a, b): seen.setdefault(top[(x, d)], set()).add(d)
    return out, len(qO), len(Max)
if __name__ == '__main__':
    from cls_anneal import build
    if sys.argv[1] == 'tiles':
        from tile_dump import rebuild
        for m in map(int, sys.argv[2:]):
            agg = {}
            for l in open(f'logs/tiles/m{m}.jsonl'):
                d = json.loads(l)
                if not d['q']: continue
                out, _, _ = analyze(rebuild(d['h'], d['F'], d['G'], d['q']), tuple(d['q']))
                for o in out: k = o[0] + ('' if o[0] == 'cross' else '/' + o[2]); agg[k] = agg.get(k, 0) + 1
            print(m, agg, flush=True)
    else:
        h, F, G, q = [eval(a) for a in sys.argv[1:5]]
        out, nq, t = analyze(build(h, F, G, q), q)
        print('qO', nq, 't', t, out)
