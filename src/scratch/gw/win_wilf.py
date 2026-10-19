# Window-Wilf test on all numerical semigroups of genus <= G (tree of removing generators > F).
#   P(N):  #(gaps < N)  <=  (e-1) * #(S cap [c-N, c))      for N in [m, c]   (N = i*m is the prefix-GW family P_i)
import sys
G = int(sys.argv[1])
def info(gaps_mask, F):
    c = F + 1
    inS = [not (gaps_mask >> z) & 1 for z in range(c + 1)]
    # minimal generators: elements s in (0, c+m) not sum of two nonzero elements
    m = next(z for z in range(1, c + 2) if z > c - 1 or inS[z]) if c > 0 else 1
    top = c + m
    isS = lambda z: z >= c or inS[z]
    gens = [s for s in range(1, top) if isS(s) and not any(isS(a) and isS(s - a) for a in range(1, s // 2 + 1))]
    if c == 0: gens = [1]
    return c, m, gens, isS
fails = {}; tot = 0; minslack = None
stack = [(0, -1)]   # N itself: gaps mask 0, F = -1
while stack:
    mask, F = stack.pop()
    c, m, gens, isS = info(mask, F)
    tot += 1
    e = len(gens); g = bin(mask).count('1')
    if c > 0:
        pre = [0] * (c + 1)   # pre[N] = #gaps < N
        for z in range(c): pre[z + 1] = pre[z] + (0 if isS(z) else 1)
        sl = [0] * (c + 1)    # sl[N] = #S cap [c-N, c)
        for N in range(1, c + 1): sl[N] = sl[N - 1] + (1 if isS(c - N) else 0)
        for N in range(m, c + 1):
            r = (e - 1) * sl[N] - pre[N]
            key = 'mult' if N % m == 0 else 'other'
            if r < 0:
                fails[key] = fails.get(key, 0) + 1
                if fails[key] <= 3: print("FAIL", key, "gens", gens, "c", c, "N", N, "slack", r, flush=True)
    if g < G:
        for n in gens:
            if n > F:
                stack.append((mask | (1 << n), n))
print("G", G, "semigroups", tot, "fails", fails, flush=True)
