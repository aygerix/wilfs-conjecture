"""Independent lead check of codex P9 (PAIR-SPAN12, SUMSET-MODULUS) on P18 semigroups.
Own code: Apery set by Dijkstra mod m, membership x in S iff x >= w[x % m].
usage: python p9_lead_check.py exh MMAX        (all offset sets, 2 <= m <= MMAX)
       python p9_lead_check.py rnd SEED TRIALS (random, small spans to trigger SM)"""
import sys, heapq, random, math
from fractions import Fraction as Fr

def apery(m, gens):
    w = [None] * m; w[0] = 0; pq = [(0, 0)]
    while pq:
        d, r = heapq.heappop(pq)
        if d > w[r]: continue
        for n in gens:
            r2 = (r + n) % m
            if w[r2] is None or d + n < w[r2]:
                w[r2] = d + n; heapq.heappush(pq, (d + n, r2))
    return w

stats = {}; fails = []
def bump(k): stats[k] = stats.get(k, 0) + 1
def fail(tag, data):
    bump('FAIL_' + tag)
    if len(fails) < 20: fails.append((tag, data))

def check(m, A):
    B = [0] + sorted(A); k = len(A); e = k + 1; beta = B[-1]
    if math.gcd(m, *A) != 1: return
    gens = [m] + [m + b for b in A]
    w = apery(m, gens)
    inS = lambda x: x >= 0 and x >= w[x % m]
    c = max(w) - m + 1
    if c <= 0: return
    bump('S')
    ell = sum(1 for x in range(c) if inS(x)); W = e * ell - c
    q = -(-c // m); rho = q * m - c
    g = 0
    for b in A: g = math.gcd(g, b)
    a = beta // g
    # C1
    if c < m * (-(-(m - 1) // a)) + (g - 1) * (m - 1): fail('C1', (m, A))
    two = sorted(set(x + y for x in B for y in B))
    s2 = sum(1 for t in two if t < m)
    Th = [sum(1 for r in range(1, m) if inS(t * m + r)) for t in range(q + 1)]
    if Th[1] != k: fail('Th1', (m, A))
    if q >= 3 and Th[2] != s2 - 1: fail('Th2', (m, A))
    # P4
    for t in range(2, q):
        bump('P4')
        if Th[t] < s2 - 1 + ((s2 + 1) // 2) * ((t - 2) // 3): fail('P4', (m, A, t))
    if q >= 4 and k >= 2:
        bump('PQ')
        rhs = Fr(q) + Fr(s2 * q * (q - 1), 12) if rho > 0 else Fr(q) + Fr(s2 * q * q, 12)
        if ell < rhs: fail('PQ', (m, A))
        if 12 * a <= e * s2:
            bump('PS12')
            if W < k * q + rho: fail('PS12', (m, A, W))
    if 12 * a <= e * s2 and W < 0: fail('PS12any', (m, A))
    # SUMSET-MODULUS, every j >= 2 with m > (2j-1) beta
    N = m + beta; D = -(-c // N)
    jB = {0}
    for j in range(1, 40):
        jB = set(x + y for x in jB for y in B)
        if j < 2: continue
        if not m > (2 * j - 1) * beta: break
        sj = len(jB); Tj = e * (sj - 1)
        bump('MB')
        RN = [sum(1 for r in range(N) if inS(H * N + r)) for H in range(D + 1)]
        if RN[0] != e: fail('R0', (m, A))
        for H in range(j - 1, D):
            if RN[H] < sj + (sj - 1) * ((H - j + 1) // j): fail('MB2', (m, A, j, H))
        n = D - j
        if n < 0: fail('Dj', (m, A, j)); continue
        bb = n % j
        if Fr(ell) < e + n + (sj - 1) * Fr(D * (D - j) + bb * (j - bb), 2 * j): fail('IB', (m, A, j))
        smq = Tj * (m * (m - 1) - j * a * N) >= 2 * j * a * N * N
        if smq:
            bump('SMQ_%d' % j)
            if W < e * (e + D - j): fail('SMW', (m, A, j, W))
        sml = Tj > 2 * j * a and m * (Tj - 2 * j * a) >= 2 * j * beta * (Tj + 3 * a)
        if sml:
            bump('SML_%d' % j)
            if not smq: fail('SML_not_SMQ', (m, A, j))
            if W < 0: fail('SML_W', (m, A, j))

mode = sys.argv[1]
if mode == 'exh':
    MM = int(sys.argv[2])
    for m in range(2, MM + 1):
        for mask in range(1, 1 << (m - 1)):
            A = [i + 1 for i in range(m - 1) if mask >> i & 1]
            check(m, A)
else:
    rng = random.Random(int(sys.argv[2])); T = int(sys.argv[3])
    for _ in range(T):
        m = rng.randint(20, 400)
        typ = rng.random()
        if typ < 0.5:   # small span: beta <= m/(2j)
            beta = rng.randint(2, max(2, m // rng.choice([5, 7, 9, 12, 20])))
        else:
            beta = rng.randint(2, m - 1)
        k = rng.randint(2, min(12, beta))
        A = sorted(set(rng.sample(range(1, beta), k - 1)) | {beta}) if beta > k else list(range(1, beta + 1))
        check(m, A)
print(sorted(stats.items()))
print('fails:', fails)
