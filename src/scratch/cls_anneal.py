# Simulated annealing over the Loomis-Whitney class C (q*-free cylinders, optionally minus a cone q >= (1,1,1)):
# D = {x2 < h(x1), x3 < min(F(x1), G(x2))} [\ (q + N^3)], maximizing a target among
#   2tri-t, qO-t, Om-C (Om = 2Tri + qO), LHS-4C (LHS = 2t + 2Tri + Q'), LHS-5C, CHT (= LHS - m - 1), C2m (= C - 2 sqrt m)
# with |D| in [M0, M1].  usage: cls_anneal.py target M0 M1 iters seed [cone]
import sys, random, math
E = [(1,0,0),(0,1,0),(0,0,1)]
def build(h, F, G, q):
    D = set()
    for i in range(len(h)):
        for j in range(h[i]):
            for k in range(min(F[i], G[j])):
                if q and i >= q[0] and j >= q[1] and k >= q[2]: continue
                D.add((i, j, k))
    return D
def stats(D):
    best = {}
    for x in sorted(D, key=lambda x: -(x[0]+x[1]+x[2])):
        b = x[0]+x[1]+x[2]
        for e in E:
            z = (x[0]+e[0], x[1]+e[1], x[2]+e[2])
            if z in D and best[z] > b: b = best[z]
        best[x] = b
    ht = {x: best[x] - (x[0]+x[1]+x[2]) for x in D}
    Max = {x for x in D if ht[x] == 0}
    tops = {}
    for a in range(3):
        e = E[a]
        for x in sorted(D, key=lambda x: -x[a]):
            z = (x[0]+e[0], x[1]+e[1], x[2]+e[2])
            tops[(x, a)] = tops[(z, a)] if z in D else x
    tri = qU = qO = 0
    for x in D:
        if x in Max: continue
        tp = [tops[(x, a)] for a in range(3)]
        n = sum(1 for z in tp if z in Max); hh = sum(ht[z] for z in tp)
        if n == 3: tri += 1
        elif n == 2 and hh == 1:
            c = next(a for a in range(3) if tp[a] not in Max)
            if tp[c] == x: qU += 1
            else: qO += 1
    C = 0
    for c in range(3):
        a, b = [i for i in range(3) if i != c]
        P = {(x[a], x[b]) for x in D if x[c] == 0}
        C += sum(1 for (i, j) in P if (i+1, j) not in P and (i, j+1) not in P)
    return dict(t=len(Max), tri=tri, qU=qU, qO=qO, C=C, m=len(D))
def target(s, name):
    t, tri, qU, qO, C, m = s['t'], s['tri'], s['qU'], s['qO'], s['C'], s['m']
    lhs = 2*t + 2*tri + qU + qO
    return {'2tri-t': 2*tri - t, 'qO-t': qO - t, 'Om-C': 2*tri + qO - C, 'LHS-4C': lhs - 4*C, 'LHS-5C': lhs - 5*C,
            'CHT': lhs - m - 1, 'A4b': 2*tri + qU + qO - 2*C, 'K': 2*tri + qU + qO - 2*t, 'Om-C-qU': 2*tri + qO + qU - 2*C, 'C2m': C - 2*math.sqrt(m), 'qU-t': qU - t, 'tri-C': tri - C}[name]
def valid(h, F, G):
    if not h or not G or not F or len(F) != len(h): return False
    if h[0] != len(G) or F[0] != G[0]: return False
    for s in (h, F, G):
        if any(s[i] < s[i+1] for i in range(len(s)-1)) or s[-1] < 1: return False
    return True
def mutate(h, F, G, q, cone, rnd):
    h, F, G = list(h), list(F), list(G)
    r = rnd.random()
    if r < 0.25:   # change h entry
        i = rnd.randrange(1, len(h)) if len(h) > 1 else 0
        h[i] += rnd.choice((-1, 1))
    elif r < 0.45:
        i = rnd.randrange(len(F)); F[i] += rnd.choice((-1, 1))
        if i == 0: G[0] = F[0]
    elif r < 0.65:
        j = rnd.randrange(len(G)); G[j] += rnd.choice((-1, 1))
        if j == 0: F[0] = G[0]
    elif r < 0.75:   # append/remove column (L1)
        if rnd.random() < 0.5 and len(h) > 1: h.pop(); F.pop()
        else: h.append(rnd.randint(1, h[-1])); F.append(rnd.randint(1, F[-1]))
    elif r < 0.85:   # append/remove row (L2)
        if rnd.random() < 0.5 and len(G) > 1: G.pop(); h = [min(v, len(G)) for v in h]; h[0] = len(G)
        else: G.append(rnd.randint(1, G[-1])); h[0] = len(G)
    elif cone:
        q = [max(1, v + rnd.choice((-1, 0, 1))) for v in (q or [1, 1, 1])]
    return h, F, G, q
INIT = None
def run(name, M0, M1, iters, seed, cone):
    rnd = random.Random(seed)
    k = max(2, int(round(M0 ** (1/3))))
    h, F, G, q = [k]*k, [k]*k, [k]*k, ([1, 1, 1] if cone else None)
    if INIT: h, F, G = [list(v) for v in INIT]
    elif seed % 2 == 0:   # staircase start
        n = max(3, int(math.sqrt(M0)))
        G = list(range(n, 0, -1)); h = [n] + list(range(n - 1, 0, -1)); F = [n] + [1] * (n - 1)
    cur = None; best = (-10**9, None)
    for it in range(iters):
        T = max(0.05, 2.0 * (1 - it / iters))
        nh, nF, nG, nq = mutate(h, F, G, q, cone, rnd)
        if not valid(nh, nF, nG): continue
        D = build(nh, nF, nG, nq)
        m = len(D)
        if m < 1: continue
        s = stats(D); v = target(s, name)
        pen = 0 if M0 <= m <= M1 else -abs(m - (M0 if m < M0 else M1)) * 0.5
        sc = v + pen
        if cur is None or sc >= cur or rnd.random() < math.exp((sc - cur) / T):
            h, F, G, q, cur = nh, nF, nG, nq, sc
            if pen == 0 and v > best[0]: best = (v, (tuple(h), tuple(F), tuple(G), tuple(q) if q else None, s))
    return best
if __name__ == '__main__':
    name, M0, M1, iters, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    cone = len(sys.argv) > 6 and sys.argv[6] == 'cone'
    if len(sys.argv) > 7: INIT = eval(sys.argv[7])
    b = run(name, M0, M1, iters, seed, cone)
    print(name, M0, M1, 'seed', seed, 'cone' if cone else 'C', 'best', b, flush=True)
