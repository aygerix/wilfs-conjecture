# N-count structure: n(x) = #{a : top_a(x) maximal}; MAXSUM <=> N3 <= N1 + 2 N0 + 1.  For non-maximal x, n(x) = 3 iff x
# is a TRIPOD centre: x + s_a e_a maximal (s_a >= 1) for a = 1,2,3.  So N3 = t + #tripods (t = |Max|).
# Report per m (non-two-face tiles): max #tripods, tiles with tripods, min (N1 + 2N0 + 1 - t), min MAXSUM slack.
# Also the same over the class C (cyl) for comparison when called as: tile_tripod.py cyl M.   usage: tile_tripod.py m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def ncounts(D):
    Max = {y for y in D if all(add(y, a) not in D for a in range(3))}
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    N = [0, 0, 0, 0]; trip = 0
    for x in D:
        k = sum(top(x, a) in Max for a in range(3)); N[k] += 1
        if k == 3 and x not in Max: trip += 1
    return N, len(Max), trip
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        mt = (0, None); ntr = 0; mins = None; msl = None
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            N, t, trip = ncounts(set(D))
            if trip: ntr += 1
            if trip > mt[0]: mt = (trip, r)
            s = N[1] + 2*N[0] + 1 - t
            if mins is None or s < mins[0]: mins = (s, r, N, t, trip)
        print(f'm={m}: tiles with tripods {ntr}, max #tripods {mt}; min N1+2N0+1-t {mins}', flush=True)
