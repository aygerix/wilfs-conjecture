# On dumped cone tiles: count tripod S-failures (top_a(x) = top_b(x'), a != b) and P-failures (tripods u, u' with
# u_a < u'_a, u_b > u'_b for some a != b), plus qO-cell S-failures; report cycle rank of the tripod incidence graph.
import sys, json
sys.path.insert(0, 'src/scratch')
from tile_dump import rebuild
E = [(1,0,0),(0,1,0),(0,0,1)]
def add(x, e): return (x[0]+e[0], x[1]+e[1], x[2]+e[2])
def run(d):
    D = rebuild(d['h'], d['F'], d['G'], d['q'])
    Max = {x for x in D if all(add(x, e) not in D for e in E)}
    top = {}
    for a in range(3):
        for x in sorted(D, key=lambda z: -z[a]):
            z = add(x, E[a]); top[(x, a)] = top[(z, a)] if z in D else x
    tri = [x for x in D if x not in Max and all(top[(x, a)] in Max for a in range(3))]
    owner = {}
    sf = 0
    for x in tri:
        for a in range(3):
            owner.setdefault(top[(x, a)], []).append((x, a))
    for y, L in owner.items():
        if len({a for _, a in L}) > 1: sf += 1
    pf = 0
    for i in range(len(tri)):
        for j in range(i + 1, len(tri)):
            u, v = tri[i], tri[j]
            for a in range(3):
                for b in range(3):
                    if a != b and u[a] < v[a] and u[b] > v[b]: pf += 1
    return len(tri), sf, pf
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        n = nS = nP = 0; maxT = 0; exP = None
        for l in open(f'logs/tiles/m{m}.jsonl'):
            d = json.loads(l)
            if not d['q']: continue
            T, s, p = run(d); n += 1; nS += s > 0; nP += p > 0; maxT = max(maxT, T)
            if p and exP is None: exP = (d['h'], d['F'], d['G'], d['q'], T, p)
        print(f'm={m}: cone tiles {n}, with tripod S-failure {nS}, with tripod P-failure {nP}, max Tri {maxT}; ex P {exP}', flush=True)
