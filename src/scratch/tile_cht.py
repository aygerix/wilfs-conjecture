# CHT (counting HT): #{h >= 2} >= #{h = 0} - 1  <=>  2t + 2|Tri| + Q' <= m + 1  (PROVED equivalence, any down-set):
#   {h = 0} = Max u Tripods; h = 1 iff n(x) = 2 and the third top has height 1; n <= 1 => h >= 2.
#   Q' = #{x : n(x) = 2, ht(top_c x) = 1} (c = the direction whose ray does not end at a maximum).
# Q' split: Q0 = third ray trivial (x is a c-top; then ht(x) >= max steps to the two maxima => both steps are 1),
#           Q1 = third ray nontrivial.  Reports per m: min slack m+1-(2t+2Tri+Q'), and max of t, Tri, Q0, Q1.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def cht(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    t = tri = q0 = q1 = 0
    for x in D:
        tops = [top(x, a) for a in range(3)]; hs = [ht[z] for z in tops]
        n = sum(1 for z in hs if z == 0)
        if ht[x] == 0: t += 1
        elif n == 3: tri += 1
        elif n == 2 and sum(hs) == 1:
            c = next(a for a in range(3) if hs[a] == 1)
            if tops[c] == x: q0 += 1
            else: q1 += 1
    return t, tri, q0, q1
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        worst = None; mx = [0, 0, 0, 0]
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            t, tri, q0, q1 = cht(set(D))
            mx = [max(u, v) for u, v in zip(mx, (t, tri, q0, q1))]
            s = m + 1 - (2*t + 2*tri + q0 + q1)
            if worst is None or s < worst[0]: worst = (s, r, t, tri, q0, q1)
        print(f'm={m}: min slack {worst}; max (t, Tri, Q0, Q1) = {mx}', flush=True)
