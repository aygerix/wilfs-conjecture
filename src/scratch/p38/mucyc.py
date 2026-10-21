# mucyc: print the classes of S along the mu-cycle(s) s -> s + mu (mod m), with sigma, U-level h, type, U-rep,
# T-rep (least length, lex-largest), and whether x_s + e_1 = x_{s+mu} (U-out-edge "|" = column continues).
import sys, heapq
from itertools import combinations_with_replacement as cwr
def run(gens):
    m = gens[0]; A = [g - m for g in gens[1:]]; d = len(A); mu = A[0]
    sig = lambda v: sum(v[i] * A[i] for i in range(d))
    best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            v = tuple(sum(1 for i in c if i == q) for q in range(d)); s = sig(v); cl = s % m
            key = (k * m + s, -k, tuple(-x for x in v))
            if cl not in best or key < best[cl][0]: best[cl] = (key, v)
    X = {c: best[c][1] for c in best}
    # T reps: Dijkstra on (value, length, -lex) over residues
    INF = (10**9,); T = {0: (0, 0, tuple([0] * d))}; pq = [(0, 0, tuple([0] * d), 0)]; done = set()
    while pq:
        val, ln, negv, c = heapq.heappop(pq)
        if c in done: continue
        done.add(c)
        v = tuple(-x for x in negv) if ln else tuple([0] * d)
        for i in range(d):
            w = list(v); w[i] += 1; w = tuple(w); nv = val + A[i]; nc = nv % m; key = (nv, ln + 1, tuple(-x for x in w))
            if nc not in done and (nc not in T or key < T[nc]): T[nc] = key; heapq.heappush(pq, (nv, ln + 1, tuple(-x for x in w), nc))
    lbl = lambda v: '+'.join(str(A[i]) for i in range(d) for _ in range(v[i])) or '0'
    seen = set()
    for s0 in range(m):
        if s0 in seen: continue
        cyc = []; s = s0
        while s not in seen: seen.add(s); cyc.append(s); s = (s + mu) % m
        print(f"cycle from {s0} (length {len(cyc)}):")
        for s in cyc:
            x = X[s]; h = sum(x); sg = sig(x); tv, tl, tneg = T[s]; tau = tv
            typ = 'EQ ' if sg == tau else ('NE2' if h == 2 else 'NE3')
            nxt = X[(s + mu) % m]; y = list(x); y[0] += 1
            edge = '|' if tuple(y) == nxt else ' '
            print(f"  {s:3d} sigma={sg:3d} h={h} {typ} k={tl} x={lbl(x):12s} tau={tau:3d} {edge}")
for a in sys.argv[1:]: run([int(t) for t in a.split(',')])
