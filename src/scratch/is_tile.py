# Is the down-set D a lattice tile? Search r in (Z/m)^3 with x -> r.x mod m injective on D (|D| = m).
# If D has a full-support minimal non-element q*, r.q* = 0 is necessary (q* in Lambda).
import sys, itertools
def is_tile(D, qstar=None):
    D = list(D); m = len(D)
    for r1 in range(m):
        for r2 in range(m):
            if qstar is not None:
                # solve r3 * q3 = -(r1 q1 + r2 q2) mod m
                rhs = (-(r1 * qstar[0] + r2 * qstar[1])) % m
                cands = [r3 for r3 in range(m) if (r3 * qstar[2]) % m == rhs]
            else:
                cands = range(m)
            for r3 in cands:
                seen = set()
                for x in D:
                    v = (r1 * x[0] + r2 * x[1] + r3 * x[2]) % m
                    if v in seen: break
                    seen.add(v)
                else:
                    return (r1, r2, r3)
    return None
def build(h, F, G, q=None):
    return {(i, j, k) for i in range(len(h)) for j in range(h[i]) for k in range(min(F[i], G[j]))
            if not (q and i >= q[0] and j >= q[1] and k >= q[2])}
if __name__ == '__main__':
    h, F, G = [eval(a) for a in sys.argv[1:4]]; q = eval(sys.argv[4]) if len(sys.argv) > 4 else None
    D = build(h, F, G, q); print('m', len(D), 'tile r:', is_tile(D, q))
