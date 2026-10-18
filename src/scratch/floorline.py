# Floor-line statistics on real cone tiles (all 3 directions c):
#  fl_qO : max # qO cells x on one c-line whose c-top w is a floor cell (w + e_c in K), x != w
#  dbl   : max # "doubly realized" levels z in [0, q_c-2]: the a-face profile takes value z+1 at a column >= q_a AND
#          the b-face profile takes value z+1 at a row >= q_b   (necessary for a floor-line qO cell at height z)
#  low_a : max # distinct face heights < q_c at columns >= q_a (face A_b) -- i.e. corners of the faces below the floor
import sys, json
sys.path.insert(0, 'src/scratch')
from tile_dump import rebuild
from qo_cone import add, E
def stats(D, q):
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
    line = {}
    for x in D:
        if x in Max: continue
        tp = [top[(x, a)] for a in range(3)]
        if sum(1 for z in tp if z in Max) == 2 and sum(ht[z] for z in tp) == 1:
            c = next(a for a in range(3) if tp[a] not in Max)
            if tp[c] != x and inK(add(tp[c], E[c])): line[(c, tp[c])] = line.get((c, tp[c]), 0) + 1
    fl = max(line.values()) if line else 0
    dbl = 0; low = 0
    for c in range(3):
        a, b = [d for d in range(3) if d != c]
        # face x_b = 0: heights along a; face x_a = 0: heights along b
        ha = {}
        for x in D:
            if x[b] == 0: ha[x[a]] = max(ha.get(x[a], 0), x[c] + 1)
        hb = {}
        for x in D:
            if x[a] == 0: hb[x[b]] = max(hb.get(x[b], 0), x[c] + 1)
        va = {v for i, v in ha.items() if i >= q[a] and v < q[c]}
        vb = {v for j, v in hb.items() if j >= q[b] and v < q[c]}
        dbl = max(dbl, len(va & vb)); low = max(low, len(va), len(vb))
    return fl, dbl, low
for m in map(int, sys.argv[1:]):
    mx = [0, 0, 0]; cnt = [0, 0]
    for l in open(f'logs/tiles/m{m}.jsonl'):
        d = json.loads(l)
        if not d['q']: continue
        s = stats(rebuild(d['h'], d['F'], d['G'], d['q']), tuple(d['q']))
        mx = [max(u, v) for u, v in zip(mx, s)]; cnt[0] += s[1] >= 1; cnt[1] += s[0] >= 1
    print(m, 'max floor-line qO per line', mx[0], 'max doubly-realized levels', mx[1], 'max low face heights', mx[2],
          '#tiles with dbl>=1', cnt[0], 'with floor-line qO', cnt[1], flush=True)
