# ancflow: does the per-class ZW2 budget phi (4e-5, 3e-5, 2e-5 small sq, e-5 large sq / small cube) pay every large
# level-3 class (demand 5) through divisibility?  Rule ANC: a large standard cube y may draw from every standard
# monomial x < y (proper divisor, including 0).  Rule ANC1: only from its square divisors and the singletons in supp(y).
# Max flow (Dinic, from flowdiv.py); prints saturation counts and worst deficits.
import sys
from itertools import combinations_with_replacement as cwr
exec(open('flowdiv.py').read().split('def analyse')[0].split('import sys')[1] if False else open('flowdiv.py').read().split('def analyse')[0])
def analyse(m, A, rule):
    d = len(A); e = d + 1; best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k, c)
            if cl not in best or key < best[cl]: best[cl] = key
    vec = lambda c: tuple(sum(1 for t in c if t == i) for i in range(d))
    rep = {cl: vec(best[cl][2]) for cl in best}; h = {cl: sum(rep[cl]) for cl in best}; sg = {cl: best[cl][0] - h[cl] * m for cl in best}
    D = {rep[cl]: cl for cl in best}
    def phi(x):
        cl = D[x]; k = sum(x); small = sg[cl] < m
        return {0: 4 * e - 5, 1: 3 * e - 5}.get(k, (2 * e - 5) if (k == 2 and small) else (e - 5 if (k == 2 or small) else -5))
    nodes = {('S',): 0, ('T',): 1}; edges = []; dem = 0
    for x in D:
        if phi(x) > 0: nodes[x] = len(nodes); edges.append((0, nodes[x], phi(x)))
    for y in D:
        if sum(y) != 3 or sg[D[y]] < m: continue
        ny = len(nodes); nodes[('y', y)] = ny; edges.append((ny, 1, 5)); dem += 5
        divs = set()
        if rule == 'ANC':
            for k in range(3):
                for c in cwr(range(d), k):
                    x = vec(c)
                    if all(x[i] <= y[i] for i in range(d)) and x in D: divs.add(x)
        else:
            for i in range(d):
                if y[i]:
                    divs.add(tuple(y[j] - (j == i) for j in range(d))); divs.add(tuple(int(j == i) for j in range(d)))
        for x in divs:
            if x in nodes and phi(x) > 0: edges.append((nodes[x], ny, 10 ** 6))
    f = maxflow(len(nodes), edges, 0, 1)
    tot = sum(phi(x) for x in D)
    return dict(e=e, dem=dem, flow=f, zw2=tot)
rule = sys.argv[1]; rows = []
for fn in sys.argv[2:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:])), rule); r['m'] = int(t[1]); r['A'] = list(map(int, t[15:])); rows.append(r)
bad = [r for r in rows if r['flow'] < r['dem']]
print(f"{rule} {sys.argv[2]}: {len(rows)} S, saturated {len(rows) - len(bad)}")
for r in sorted(bad, key=lambda r: r['flow'] - r['dem'])[:4]:
    print(f"   deficit {r['dem'] - r['flow']} (demand {r['dem']}, ZW2 {r['zw2']}) m={r['m']} A={r['A']}")
