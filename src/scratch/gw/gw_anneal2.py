# Adversarial search v2 for GW.  Minimise the relative Wilf number E/c (E = (d+1)l - c = d c - (d+1) g) over
# residue-complete down-sets with c >= m (at least one full level of carries), n = s + m k with k in [0,KB]^d.
# Moves: flip (corner y -> addable z, same residue); k_a +-1; unit rescale s -> u s; re-seed s_a -> random (new
# lattice, D = Groebner tile of the weight order (v, lex)).  Prints every new record and any E < 0.
import sys, random, heapq
from math import gcd, exp
seed, d, m0, m1, iters, KB, hours = map(float, sys.argv[1:8]); seed, d, m0, m1, iters, KB = map(int, (seed, d, m0, m1, iters, KB))
rnd = random.Random(seed)
import time; T_END = time.time() + hours * 3600
U = [tuple(int(i == a) for i in range(d)) for a in range(d)]
add = lambda x, y: tuple(p + q for p, q in zip(x, y)); sub = lambda x, y: tuple(p - q for p, q in zip(x, y))
dot = lambda x, y: sum(p * q for p, q in zip(x, y))
def tile(m, n):
    seen = set(); h = [(0, (0,) * d)]; D = set()
    while h and len(D) < m:
        val, x = heapq.heappop(h)
        if x in D or val % m in seen: continue
        seen.add(val % m); D.add(x)
        for u in U:
            y = add(x, u)
            if y not in D: heapq.heappush(h, (val + dot(u, n), y))
    return D if len(D) == m else None
def stats(D, n, m):
    V = [dot(x, n) for x in D]; M = max(V); c = M - m + 1; g = sum(v // m for v in V)
    return d * c - (d + 1) * g, c
def score(D, n, m):
    E, c = stats(D, n, m)
    return (E / c if c >= m else 10.0), E, c
def flips(D, s, m):
    res = lambda x: dot(x, s) % m; out = []
    for y in D:
        if not any(y) or any(add(y, u) in D for u in U): continue
        Dm = D - {y}; ry = res(y)
        for x in Dm:
            for u in U:
                z = add(x, u)
                if z in Dm or z == y or res(z) != ry: continue
                if all(z[a] == 0 or sub(z, U[a]) in Dm for a in range(d)): out.append((y, z))
    return out
def rand_s(m):
    while True:
        c = tuple(rnd.randint(1, m - 1) for _ in range(d))
        if gcd(m, *c) == 1: return c
rec = (9.9, None)
trial = 0
while time.time() < T_END:
    trial += 1; m = rnd.randint(m0, m1); s = rand_s(m); k = [rnd.randint(0, KB) for _ in range(d)]
    n = [si + m * ki for si, ki in zip(s, k)]; D = tile(m, n)
    if D is None or any(u not in D for u in U): continue
    cur = score(D, n, m); T = 0.05
    for it in range(iters):
        T = max(0.002, T * 0.998); mv = rnd.random(); D2, s2, k2 = D, s, k
        if mv < 0.55:
            F = flips(D, s, m)
            if not F: continue
            y, z = rnd.choice(F); D2 = (D - {y}) | {z}
            if any(u not in D2 for u in U): continue
        elif mv < 0.85:
            a = rnd.randrange(d); k2 = list(k); k2[a] += rnd.choice((-1, 1))
            if not 0 <= k2[a] <= KB: continue
        elif mv < 0.95:
            us = [u for u in range(2, m) if gcd(u, m) == 1]
            if not us: continue
            u = rnd.choice(us); s2 = tuple(u * si % m for si in s)
            if 0 in s2: continue
        else:
            s2 = list(s); s2[rnd.randrange(d)] = rnd.randint(1, m - 1); s2 = tuple(s2)
            if gcd(m, *s2) != 1: continue
            D2 = tile(m, [si + m * ki for si, ki in zip(s2, k2)])
            if D2 is None or any(u not in D2 for u in U): continue
        n2 = [si + m * ki for si, ki in zip(s2, k2)]
        if len({dot(x, s2) % m for x in D2}) != m: continue
        sc = score(D2, n2, m)
        if sc[0] <= cur[0] or rnd.random() < exp(-(sc[0] - cur[0]) / T):
            D, s, k, cur = D2, s2, k2, sc
            if cur[1] < 0:
                print('COUNTEREXAMPLE', cur, 'm', m, 'n', n2, 'D', sorted(D), flush=True); sys.exit(0)
            if cur[0] < rec[0]:
                rec = (cur[0], (m, tuple(n2), cur[1], cur[2], sorted(D)))
                print(f"trial {trial} record E/c={cur[0]:.4f} E={cur[1]} c={cur[2]} m={m} n={tuple(n2)} t={sum(all(add(y,u) not in D for u in U) for y in D)}", flush=True)
print('done; best', rec[0], rec[1], flush=True)
