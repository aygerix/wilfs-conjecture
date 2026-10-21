r"""RD on hard families (lead, 2026-10-21): S = <gens> u [C, oo) (Eliahou-Fromentin near misses and random truncations),
T = <m, minimal generators of S mod m>.  Reports W(S), W(T), and W(S) - W(T).  usage: python rdhard.py seed n"""
import sys, random
def props_from_set(inS, N):
    # inS: membership list on [0, N], N beyond conductor + 2m
    m = next(x for x in range(1, N + 1) if inS[x])
    gaps = [x for x in range(N + 1) if not inS[x]]; c = gaps[-1] + 1 if gaps else 0; g = len(gaps)
    els = [x for x in range(1, c + m + 1) if inS[x]]; Ss = set(els)
    gens = [x for x in els if not any((x - y) in Ss for y in els if y <= x // 2)]
    e = len(gens); W = e * (c - g) - c if c > 0 else 0
    return dict(m=m, c=c, g=g, e=e, W=W, gens=gens)
def closure(G, N):
    inS = [False] * (N + 1); inS[0] = True
    for x in range(1, N + 1): inS[x] = any(x >= h and inS[x - h] for h in G)
    return inS
def T_of(D, N):
    m = D['m']; A = sorted(set(x % m for x in D['gens'] if x % m))
    return props_from_set(closure([m] + A, N), N)
def trunc(G, C):
    N = C + 4 * max(G) + 10; inS = closure(G, N)
    for x in range(C, N + 1): inS[x] = True
    return props_from_set(inS, N), N
cases = [((14, 22, 23), 56), ((16, 25, 26), 64), ((17, 26, 28), 68), ((18, 28, 29), 72), ((19, 29, 31), 76)]
for G, C in cases:
    D, N = trunc(G, C); T = T_of(D, N)
    print("near-miss <%s>_%d: m=%d e=%d c=%d W=%d | T gens=%s e=%d c=%d W=%d | W(S)-W(T)=%d" % (",".join(map(str, G)), C, D['m'], D['e'], D['c'], D['W'],
          T['gens'], T['e'], T['c'], T['W'], D['W'] - T['W']))
random.seed(int(sys.argv[1])); n = int(sys.argv[2]); worst = []; fails = 0
for it in range(n):
    m = random.randint(5, 30); k = random.randint(1, 3)
    G = [m] + [random.randint(m + 1, 3 * m) for _ in range(k)]
    C = random.randint(m, 6 * m)
    from math import gcd
    D, N = trunc(G, C)
    if D['m'] != m or D['c'] == 0: continue
    T = T_of(D, N); dif = D['W'] - T['W']
    if dif < 0:
        fails += 1
        if fails <= 5: print("RD FAIL S gens=%s W=%d T=%s W(T)=%d" % (D['gens'], D['W'], T['gens'], T['W']))
    worst.append((dif / max(1, D['W']), dif, D['W'], T['W'], D['gens']))
worst.sort()
print("random truncations: tested %d, RD failures %d; smallest (W(S)-W(T))/W(S):" % (len(worst), fails))
for x in worst[:5]: print("   ratio %.3f diff %d W(S)=%d W(T)=%d S=%s" % x)
