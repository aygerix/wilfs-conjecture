# MAXSUM <=> #crowded + #tripods <= 1 + 2 N0 + sum_y (priv(y) - 1)^+, where for a maximal y, priv(y) = number of
# non-maximal cells on the cross of y lying on no other cross (c(x) = 1); crowded: priv(y) = 0; N0 = cells on no cross.
# Reports per m: max #crowded, crowded types (support, face-corner step pattern), and the decomposition at the worst tile.
import sys
from collections import Counter
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def decomp(D):
    Max = [y for y in D if all(add(y, a) not in D for a in range(3))]
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    owner = {}
    for x in D:
        owner[x] = {top(x, a) for a in range(3)} & set(Max)
    Mset = set(Max)
    priv = {y: 0 for y in Max}; N0 = 0; trip = 0
    for x in D:
        if x in Mset: continue
        o = owner[x]
        if len(o) == 0: N0 += 1
        elif len(o) == 1: priv[next(iter(o))] += 1
        elif len(o) == 3: trip += 1
    crowded = [y for y in Max if priv[y] == 0]
    excess = sum(max(0, p - 1) for p in priv.values())
    return dict(t=len(Max), crowded=crowded, trip=trip, N0=N0, excess=excess,
                slack=1 + 2*N0 + excess - len(crowded) - trip)
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        types = Counter(); worst = None; maxcr = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            S = set(D); d = decomp(S)
            maxcr = max(maxcr, len(d['crowded']))
            for y in d['crowded']: types[sum(1 for c in range(3) if y[c] > 0)] += 1
            if worst is None or d['slack'] < worst[0]['slack']: worst = (d, r)
        d, r = worst
        print(f"m={m}: max#crowded {maxcr}; crowded by support size {dict(types)}; worst slack {d['slack']} at r={r}: "
              f"t={d['t']} crowded={len(d['crowded'])} trip={d['trip']} N0={d['N0']} excess={d['excess']}", flush=True)
