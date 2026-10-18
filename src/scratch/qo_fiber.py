# Doubly-same qO cells (both maximal tops shared with LOWER qO cells in the same direction) on cone sets:
# fiber sizes of the maps x -> (a, top_a(x)) for each of x's two maximal directions a; best = min over the two
# choices of the max fiber (greedy: assign each cell to a direction whose top is least loaded).
import sys, json
sys.path.insert(0, 'src/scratch')
from qo_cone import add, E
def dbl(D):
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
    qO = {}
    for x in D:
        if x in Max: continue
        tp = [top[(x, a)] for a in range(3)]
        if sum(1 for z in tp if z in Max) == 2 and sum(ht[z] for z in tp) == 1:
            c = next(a for a in range(3) if tp[a] not in Max)
            if tp[c] != x: qO[x] = c
    out = []
    for x, c in qO.items():
        dirs = [a for a in range(3) if a != c]
        if all(any(u != x and qO.get(u) is not None and u[a] < x[a] and top[(u, a)] == top[(x, a)] for u in qO) for a in dirs):
            out.append((x, [(a, top[(x, a)]) for a in dirs]))
    load = {}; mx_single = 0
    for x, opts in out:
        for o in opts: load[o] = load.get(o, 0) + 1
    mx_any = max(load.values()) if load else 0
    # greedy assignment
    asg = {}
    for x, opts in sorted(out):
        o = min(opts, key=lambda o: asg.get(o, 0)); asg[o] = asg.get(o, 0) + 1
    return len(out), len(Max), mx_any, max(asg.values()) if asg else 0
if __name__ == '__main__':
    from cls_anneal import build
    if sys.argv[1] == 'tiles':
        from tile_dump import rebuild
        for m in map(int, sys.argv[2:]):
            mx = [0, 0, 0]
            for l in open(f'logs/tiles/m{m}.jsonl'):
                d = json.loads(l)
                if not d['q']: continue
                n, t, a, g = dbl(rebuild(d['h'], d['F'], d['G'], d['q']))
                mx = [max(mx[0], n), max(mx[1], a), max(mx[2], g)]
            print(m, 'max #doubly-same', mx[0], 'max fiber (any dir)', mx[1], 'max fiber (greedy)', mx[2], flush=True)
    else:
        h, F, G, q = [eval(a) for a in sys.argv[1:5]]
        print(dbl(build(h, F, G, q)))
