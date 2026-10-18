# Annealing: maximize C - 2 sqrt(m) (C = c(A1)+c(A2)+c(A3), m = |D|) over
#   'C'    : Loomis-Whitney sets D = {x2 < h(x1), x3 < min(F(x1), G(x2))}  (non-two-face: h(1), F(1), G(1) >= 2)
#   'cone' : D = Cyl \ (q + N^3), q in Cyl, q >= (1,1,1), subject to the PROVED tile constraints Wall + Floor
#   'conefree': cone class without Wall/Floor.
# usage: corner_anneal.py class M0 M1 iters seed
import sys, random, math
def nvals(s): return len(set(s))
def msize(h, F, G, q):
    m = 0
    for i in range(len(h)):
        Fi = F[i]
        for j in range(h[i]):
            v = Fi if Fi < G[j] else G[j]
            if q and i >= q[0] and j >= q[1] and v > q[2]: v = q[2]
            m += v
    return m
def inner(s, lo_a, lo_b):  # inner corners (i, s[i]) of the 2-D down-set with column heights s, with i >= lo_a, s[i] >= lo_b
    return sum(1 for i in range(1, len(s)) if s[i - 1] > s[i] >= 1 and i >= lo_a and s[i] >= lo_b)
def tile_ok(h, F, G, q):
    q1, q2, q3 = q
    # Wall: A3 (heights h over x1), A2 (F over x1), A1 (G over x2)
    if inner(h, q1, q2) > q3 or inner(F, q1, q3) > q2 or inner(G, q2, q3) > q1: return False
    # Floor: slices at x_c = q_c - 1 have <= 1 inner corner >= (q_a, q_b)
    a = sum(1 for v in F if v >= q3); b = sum(1 for v in G if v >= q3)
    s3 = [min(h[i], b) for i in range(a)]
    if inner(s3, q1, q2) > 1: return False
    n2 = sum(1 for v in h if v >= q2); s2 = [min(F[i], G[q2 - 1]) for i in range(n2)]
    if inner(s2, q1, q3) > 1: return False
    s1 = [min(F[q1 - 1], G[j]) for j in range(h[q1 - 1])]
    if inner(s1, q2, q3) > 1: return False
    return True
def valid(h, F, G, q, cls):
    if len(F) != len(h) or len(h) < 2 or len(G) < 2: return False
    if h[0] != len(G) or F[0] != G[0]: return False
    for s in (h, F, G):
        if s[-1] < 1 or any(s[i] < s[i + 1] for i in range(len(s) - 1)): return False
    if h[1] < 2 or F[1] < 2 or G[1] < 2: return False
    if cls == 'C': return True
    q1, q2, q3 = q
    if min(q) < 1 or q1 >= len(h) or q2 >= h[q1] or q3 >= min(F[q1], G[q2]): return False
    return cls == 'conefree' or tile_ok(h, F, G, q)
def mutate(h, F, G, q, rnd):
    h, F, G, q = list(h), list(F), list(G), list(q) if q else None
    r = rnd.random()
    def bump(s, i, d):
        s[i] += d
        # repair monotonicity locally
        for k in range(i - 1, -1, -1):
            if s[k] < s[k + 1]: s[k] = s[k + 1]
        for k in range(i + 1, len(s)):
            if s[k] > s[k - 1]: s[k] = s[k - 1]
    d = rnd.choice((-1, 1)) * (1 if rnd.random() < 0.7 else rnd.randint(2, 4))
    if r < 0.2: bump(h, rnd.randrange(1, len(h)), d)
    elif r < 0.4:
        i = rnd.randrange(len(F)); bump(F, i, d)
        if i == 0: G[0] = F[0]
    elif r < 0.6:
        j = rnd.randrange(len(G)); bump(G, j, d)
        if j == 0: F[0] = G[0]
    elif r < 0.7:
        if rnd.random() < 0.5 and len(h) > 2: h.pop(); F.pop()
        else: h.append(rnd.randint(1, h[-1])); F.append(rnd.randint(1, F[-1]))
    elif r < 0.8:
        if rnd.random() < 0.5 and len(G) > 2: G.pop(); h = [min(v, len(G)) for v in h]
        else: G.append(rnd.randint(1, G[-1]))
        h[0] = len(G)
    elif q is not None:
        k = rnd.randrange(3); q[k] = max(1, q[k] + rnd.choice((-1, 1)))
    if q is None: return h, F, G, None
    return h, F, G, q
def run(cls, M0, M1, iters, seed):
    rnd = random.Random(seed)
    n = max(4, int(math.sqrt(M0)))
    if seed % 3 == 0: h, F, G = [n] + [2] * (n - 1), [n] + list(range(n - 1, 0, -1)), list(range(n, 0, -1))
    elif seed % 3 == 1: h, F, G = [4, 3, 2, 2], [4, 3, 2, 2], [4, 3, 2, 2]
    else: h, F, G = [n] + list(range(n - 1, 0, -1)), [n] + [2] * (n - 1), [n] + list(range(n - 1, 0, -1))
    G = G[:h[0]] + [1] * max(0, h[0] - len(G)); h[0] = len(G)
    q = [1, 1, 1] if cls != 'C' else None
    if cls == 'cone': h, F, G = [3, 2, 2], [3, 2, 2], [3, 2, 2]
    h, F, G = [max(v, 2) if i == 1 else v for i, v in enumerate(h)], F, G
    cur = None; best = (-1e9, None)
    for it in range(iters):
        T = max(0.02, 1.5 * (1 - it / iters))
        nh, nF, nG, nq = mutate(h, F, G, q, rnd)
        if not valid(nh, nF, nG, nq, cls): continue
        m = msize(nh, nF, nG, nq); C = nvals(nh) + nvals(nF) + nvals(nG)
        v = C - 2 * math.sqrt(m)
        pen = 0 if M0 <= m <= M1 else -abs(m - (M0 if m < M0 else M1)) * 0.3
        sc = v + pen
        if cur is None or sc >= cur or rnd.random() < math.exp((sc - cur) / T):
            h, F, G, q, cur = nh, nF, nG, nq, sc
            if pen == 0 and v > best[0]: best = (v, (C, m, tuple(h), tuple(F), tuple(G), tuple(q) if q else None))
    return best
if __name__ == '__main__':
    cls, M0, M1, iters, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    b = run(cls, M0, M1, iters, seed)
    print(cls, M0, M1, 'seed', seed, 'best C-2sqrt(m) = %.3f' % b[0], b[1], flush=True)
