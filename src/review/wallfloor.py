# Check on real cone tiles: (0) D is a fundamental domain for x -> r.x mod m; (1) Wall Lemma: every non-axis inner corner
# w >= (q_a, q_b) of face A_c has (w,0) == t_w e_c with t_w in [L_c - q_c, L_c - 1], distinct; (2) Floor Lemma: slice at
# x_c = q_c - 1 has <= 1 inner corner w >= (q_a, q_b); |Y_c| <= 2.  (3) q* in Lambda.
import sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from indep import Cone, add
P = '/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/logs/tiles/'
for m in map(int, sys.argv[1:]):
    n = 0; bad = {}
    for line in open(P + f'm{m}.jsonl'):
        d = json.loads(line)
        if not d['q']: continue
        S = Cone(d['h'], d['F'], d['G'], d['q']); D = S.D; q = S.q; r = d['r']; n += 1
        res = {}
        for x in D:
            k = sum(r[i] * x[i] for i in range(3)) % m
            if k in res: bad['notFD'] = bad.get('notFD', 0) + 1
            res[k] = x
        if len(D) != m: bad['size'] = bad.get('size', 0) + 1
        if sum(r[i] * q[i] for i in range(3)) % m != 0: bad['qLambda'] = bad.get('qLambda', 0) + 1
        L = [sum(1 for k in range(60) if add((0, 0, 0), c, k) in D) for c in range(3)]
        for c in range(3):
            a, b = [i for i in range(3) if i != c]
            ts = []
            for x in D:
                if x[c] != 0: continue
                for (da, db) in ((1, 0), (0, 1)):
                    pass
            # inner corners of face A_c
            face = {(x[a], x[b]) for x in D if x[c] == 0}
            cand = {(i + 1, j) for (i, j) in face} | {(i, j + 1) for (i, j) in face}
            for (i, j) in cand:
                if (i, j) in face or i < 1 or j < 1: continue
                if (i - 1, j) in face and (i, j - 1) in face and i >= q[a] and j >= q[b]:
                    g = [0, 0, 0]; g[a] = i; g[b] = j
                    kg = sum(r[s] * g[s] for s in range(3)) % m
                    tw = [k for k in range(L[c]) if (r[c] * k) % m == kg]
                    if len(tw) != 1 or not (L[c] - q[c] <= tw[0] <= L[c] - 1): bad['wall_t'] = bad.get('wall_t', 0) + 1
                    else: ts.append(tw[0])
            if len(ts) != len(set(ts)) or len(ts) > q[c]: bad['wall_count'] = bad.get('wall_count', 0) + 1
            # floor slice
            sl = {(x[a], x[b]) for x in D if x[c] == q[c] - 1}
            cand = {(i + 1, j) for (i, j) in sl} | {(i, j + 1) for (i, j) in sl}
            nin = sum(1 for (i, j) in cand if (i, j) not in sl and i >= q[a] and j >= q[b] and (i - 1, j) in sl and (i, j - 1) in sl)
            if nin > 1: bad['floor'] = bad.get('floor', 0) + 1
    print(f'm={m}: cone tiles {n}, failures {bad}', flush=True)
