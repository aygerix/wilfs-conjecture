# c(x) = #{a : the a-column top of x is a maximal cell}.  Sum_x c(x) = Sum_A (d + |y|) =: S1.  CR roughly needs S1 <= 2m.
# Reports: S1 - 2m, the number of NON-maximal cells with c(x) = 3, and what is special about them.
import sys, json; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from collections import Counter
def rebuild(h, F, G, q):
    return {(i, j, k) for i in range(len(h)) for j in range(h[i]) for k in range(min(F[i], G[j]))
            if q is None or not (i >= q[0] and j >= q[1] and k >= q[2])}
U = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]; add = lambda x, y: tuple(p + q for p, q in zip(x, y))
def analyse(D):
    A = {y for y in D if all(add(y, u) not in D for u in U)}
    def top(x, a):
        while add(x, U[a]) in D: x = add(x, U[a])
        return x
    c = {x: sum(top(x, a) in A for a in range(3)) for x in D}
    S1 = sum(c.values()); m = len(D); t = len(A)
    three = [x for x in D if x not in A and c[x] == 3]
    return S1 - 2 * m, len(three), t, Counter(c[x] for x in D if x not in A)
for m in (30, 40, 50, 60, 64):
    worst = None; n3 = Counter(); tot = 0; pos = 0
    for line in open(f'logs/tiles/m{m}.jsonl'):
        rec = json.loads(line); D = rebuild(rec['h'], rec['F'], rec['G'], rec['q'])
        ex, k3, t, cnt = analyse(D); tot += 1; n3[k3] += 1; pos += ex > 0
        if worst is None or ex > worst[0]: worst = (ex, t, k3, rec['r'], dict(cnt))
    print(f'm={m}: {tot} tiles; S1 - 2m > 0 in {pos}; max S1-2m {worst[0]} (t={worst[1]}, #nonmax c=3: {worst[2]}, r={worst[3]}, c-hist {worst[4]}); tiles by #nonmax-with-c=3: {dict(sorted(n3.items())[:6])}')
