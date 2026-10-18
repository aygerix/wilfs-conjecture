# Adversarial search for GW counterexamples.  State: (m, s, D, k): D a down-set in N^d with x.s mod m bijective,
# weights n = s + m*k (k in [-KB,KB]^d, any signs).  Minimise E = d*max v - (d+1)*sum floor(v/m) - d*(m-1).
# Moves: flip (remove a corner y, add an addable y' with the same residue), k_a += -1/+1, s -> u*s mod m (unit u).
# Start: Groebner tile of the weight order (v, lex) for random n.  Reports any E < 0 immediately (with full data).
import sys, random, heapq
from math import gcd, exp
seed, d, m0, m1, iters, KB = map(int, sys.argv[1:7]); rnd = random.Random(seed)
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
dot = lambda x, y: sum(p * q for p, q in zip(x, y))
def tile(m, n):
    seen = {}; h = [(0, (0,) * d)]; D = set()
    while h and len(D) < m:
        val, x = heapq.heappop(h)
        if x in D: continue
        r = val % m
        if r in seen: continue
        seen[r] = x; D.add(x)
        for u in U:
            y = add(x, u)
            if y not in D: heapq.heappush(h, (val + dot(u, n), y))
    return D if len(D) == m else None
def E(D, n, m):
    V = [dot(x, n) for x in D]
    return d * max(V) - (d + 1) * sum(v // m for v in V) - d * (m - 1)
def flips(D, s, m):
    res = lambda x: dot(x, s) % m; out = []
    corners = [y for y in D if any(y) and all(add(y, u) not in D for u in U)]
    for y in corners:
        Dm = D - {y}; ry = res(y)
        for x in Dm:
            for u in U:
                z = add(x, u)
                if z in Dm or z == y or res(z) != ry: continue
                if all(z[a] == 0 or sub(z, U[a]) in Dm for a in range(d)): out.append((y, z))
    return out
best_overall = None
for trial in range(10 ** 9):
    m = rnd.randint(m0, m1)
    s = None
    for _ in range(200):
        c = tuple(rnd.randint(1, m - 1) for _ in range(d))
        if gcd(m, *c) == 1: s = c; break
    if s is None: continue
    k = [rnd.randint(0, 1) for _ in range(d)]
    D = tile(m, [si + m * ki for si, ki in zip(s, k)])
    if D is None or any(u not in D for u in U): continue
    cur = E(D, [si + m * ki for si, ki in zip(s, k)], m); best = (cur, None); T = 2.0
    for it in range(iters):
        T = max(0.05, T * 0.999)
        mv = rnd.random()
        if mv < 0.6:
            F = flips(D, s, m)
            if not F: continue
            y, z = rnd.choice(F); D2 = (D - {y}) | {z}; s2, k2 = s, k
            if any(u not in D2 for u in U): continue
        elif mv < 0.9:
            a = rnd.randrange(d); k2 = list(k); k2[a] += rnd.choice((-1, 1))
            if abs(k2[a]) > KB: continue
            D2, s2 = D, s
        else:
            u = rnd.choice([u for u in range(2, m) if gcd(u, m) == 1] or [1])
            s2 = tuple(u * si % m for si in s); D2, k2 = D, k
            if 0 in s2: continue
        n2 = [si + m * ki for si, ki in zip(s2, k2)]
        e2 = E(D2, n2, m)
        if e2 <= cur or rnd.random() < exp(-(e2 - cur) / T):
            D, s, k, cur = D2, s2, k2, e2
            if cur < best[0]: best = (cur, (m, s, tuple(k), sorted(D)))
        if cur < 0:
            print('COUNTEREXAMPLE', cur, 'm', m, 's', s, 'k', k, 'n', n2, 'D', sorted(D), flush=True); sys.exit(0)
    if best_overall is None or best[0] < best_overall[0]: best_overall = best
    if trial % 20 == 0:
        print(f"trial {trial}: best E this trial {best[0]}; overall {best_overall[0]} {best_overall[1][:3] if best_overall[1] else ''}", flush=True)
