# Checks the claims of Lemma TF-cone (crude tripod bound for cone sets with |Y_d| <= 2):
#  elimination by decreasing |x|; s(x) = # tops already used; shares classified 'same' (an earlier tripod has the same
#  top in the same direction) or 'cross';  claims: (i) <= 1 cross share per floor maximum y in Y; (ii) a tripod with two
#  same shares (dirs a, b) has witness top_c(x + i'e_b) in Y_a or top_c(x + ie_a) in Y_b (P');  (iii) the family
#  Phi(a,b) = {x : same shares a, b, witness via the b-partner in Y_a} lies on one b-line with x_a = q_a - 1;
#  (iv) |Phi(a,b)| <= 2 (header said <= 3 until the 2026-10-18 review; the code tests <= 2);  (v) 2T - t <= -1 + #cross + sum (s_same - 1)^+.
import sys, json
sys.path.insert(0, 'src/scratch')
from tile_dump import rebuild
E = [(1,0,0),(0,1,0),(0,0,1)]
def add(x, e, k=1): return tuple(x[i] + k*e[i] for i in range(3))
def check(h, F, G, q):
    D = rebuild(h, F, G, q)
    Max = {x for x in D if all(add(x, e) not in D for e in E)}
    top = {}
    for a in range(3):
        for x in sorted(D, key=lambda z: -z[a]):
            z = add(x, E[a]); top[(x, a)] = top[(z, a)] if z in D else x
    inK = lambda z: all(z[i] >= q[i] for i in range(3))
    Yd = [{y for y in Max if inK(add(y, E[d]))} for d in range(3)]
    if any(len(Yd[d]) > 2 for d in range(3)): return None
    tri = sorted([x for x in D if x not in Max and all(top[(x, a)] in Max for a in range(3))], key=lambda x: -sum(x))
    seen = {}   # top -> set of directions in which earlier tripods had it
    cross = 0; extra = 0; fam = {}; viol = []
    for x in tri:
        same = []; cr = 0
        for a in range(3):
            y = top[(x, a)]
            if y in seen:
                if a in seen[y]: same.append(a)
                else: cr += 1
        cross += cr; extra += max(0, len(same) - 1)
        if len(same) >= 2:
            for i1 in range(len(same)):
                for i2 in range(len(same)):
                    a, b = same[i1], same[i2]
                    if a == b: continue
                    c = 3 - a - b
                    # partners: u' = x + i'e_b (earlier tripod with same top_b), u = x + ie_a
                    up = [v for v in tri if v != x and top[(v, b)] == top[(x, b)] and v[b] > x[b]]
                    if any(top[(v, c)] in Yd[a] for v in up): fam.setdefault((a, b), []).append(x)
            ok = False
            a, b = same[0], same[1]; c = 3 - a - b
            ua = [v for v in tri if top[(v, a)] == top[(x, a)] and v[a] > x[a]]
            ub = [v for v in tri if top[(v, b)] == top[(x, b)] and v[b] > x[b]]
            if any(top[(v, c)] in Yd[a] for v in ub) or any(top[(v, c)] in Yd[b] for v in ua): ok = True
            if not ok: viol.append(('P', x))
        for a in range(3): seen.setdefault(top[(x, a)], set()).add(a)
    Y = set().union(*Yd)
    if cross > len(Y): viol.append(('cross', cross, len(Y)))
    for (a, b), L in fam.items():
        L = sorted(set(L))
        c = 3 - a - b
        if len({(x[a], x[c]) for x in L}) > 1 or any(x[a] != q[a] - 1 for x in L): viol.append(('line', (a, b), L))
        if len(L) > 2: viol.append(("size", (a, b), L))
    t = len(Max); T = len(tri)
    if 2*T - t > -1 + cross + extra: viol.append(('budget', 2*T - t, cross, extra))
    return viol, cross, extra, max([len(set(L)) for L in fam.values()] or [0]), 2*T - t
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        n = 0; nv = 0; mx = [0, 0, 0, -99]
        for l in open(f'logs/tiles/m{m}.jsonl'):
            d = json.loads(l)
            if not d['q']: continue
            r = check(d['h'], d['F'], d['G'], d['q'])
            if r is None: print('  |Y_d| > 2 ?!', d); continue
            viol, cr, ex, fs, e2 = r; n += 1
            if viol: nv += 1; print('  VIOL', viol, d['h'], d['F'], d['G'], d['q'])
            mx = [max(mx[0], cr), max(mx[1], ex), max(mx[2], fs), max(mx[3], e2)]
        print(f'm={m}: cone tiles {n}, violations {nv}; max cross {mx[0]}, max same-excess {mx[1]}, max |Phi| {mx[2]}, max 2T-t {mx[3]}', flush=True)
