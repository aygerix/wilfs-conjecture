# Shared lower bounds for H on a finite down-set D in N^3 (set of tuples).
#   H   = sum_{(x,a)} ht(t_a x)                      (exact height sum)
#   Hs  = sum_{(x,a)} max_{b != a} r_b(t_a x)          (straight runs from tops; r_b = plateau)
#   Pi  = sum_{(x,a)} sum_{b != a} r_b(t_a x)          (Pi/2 <= Hs <= H)
#   LB2 = sum_a max_{b != a} sum_x r_b(t_a x)
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def all_bounds(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    topc = {}
    def top(x, a):
        k = (x, a)
        if k in topc: return topc[k]
        t = x
        while add(t, a) in D: t = add(t, a)
        topc[k] = t
        return t
    runc = {}
    def run(t, b):
        k = (t, b)
        if k in runc: return runc[k]
        j = 0; s = t
        while add(s, b) in D: s = add(s, b); j += 1
        runc[k] = j
        return j
    H = Hs = Pi = 0; P = [[0]*3 for _ in range(3)]
    for x in D:
        for a in range(3):
            t = top(x, a); H += ht[t]
            rs = {b: run(t, b) for b in range(3) if b != a}
            Hs += max(rs.values()); Pi += sum(rs.values())
            for b, v in rs.items(): P[a][b] += v
    LB2 = sum(max(P[a][b] for b in range(3) if b != a) for a in range(3))
    return dict(H=H, Hs=Hs, Pi=Pi, LB2=LB2)
