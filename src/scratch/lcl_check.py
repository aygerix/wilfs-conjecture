# Lattice Corner Lemma (LCL) check on dumped tiles.  For the face A3 (columns h), inner corners w = (i, h(i)) with
# h(i-1) > h(i) >= 1; t_w = the unique t in [0, L3) with i*r1 + h(i)*r2 = t*r3 (mod m).  LCL: for corners w_i, w_j
# (x1 increasing) with alpha = dx1, beta = -dx2: t_j > t_i  =>  t_j - t_i >= G(beta);  t_j < t_i  =>  t_i - t_j >= F(alpha).
# Same for the other faces by permuting coordinates.   usage: lcl_check.py m...
import sys, json
def perm(d, c):
    """return (r_a, r_b, r_c, L_a, L_b, L_c, colheights of A_c over a, F_c(alpha) = height in x_c over (alpha e_a), G_c)."""
    r, L, h, F, G = d['r'], d['L'], d['h'], d['F'], d['G']
    # build the down-set D from cylinder data
    q = d['q']; D = set()
    for i in range(L[0]):
        for j in range(h[i]):
            for k in range(min(F[i], G[j])):
                if q is None or not (i >= q[0] and j >= q[1] and k >= q[2]): D.add((i, j, k))
    return D
def check(d, m):
    D = perm(d, 0); r = d['r']; bad = 0; npairs = 0
    for c in range(3):
        a, b = [i for i in range(3) if i != c]
        def pt(xa, xb, xc):
            x = [0, 0, 0]; x[a] = xa; x[b] = xb; x[c] = xc; return tuple(x)
        La = max(x[a] for x in D) + 1; Lc = max(x[c] for x in D) + 1
        col = [sum(1 for y in range(100) if pt(i, y, 0) in D) for i in range(La)]
        Fc = lambda al: sum(1 for z in range(Lc) if pt(al, 0, z) in D)
        Gc = lambda be: sum(1 for z in range(Lc) if pt(0, be, z) in D)
        W = []
        for i in range(1, La):
            if col[i - 1] > col[i] >= 1:
                w = (i, col[i]); val = (w[0] * r[a] + w[1] * r[b]) % m
                ts = [t for t in range(Lc) if (t * r[c]) % m == val]
                assert len(ts) == 1, (d, c, w, ts)
                W.append((w, ts[0]))
        for x in range(len(W)):
            for y in range(x + 1, len(W)):
                (wi, ti), (wj, tj) = W[x], W[y]; al = wj[0] - wi[0]; be = wi[1] - wj[1]; npairs += 1
                ok = (tj - ti >= Gc(be)) if tj > ti else (ti - tj >= Fc(al))
                bad += not ok
    return bad, npairs
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        tb = tp = 0
        for l in open(f'logs/tiles/m{m}.jsonl'):
            b, p = check(json.loads(l), m); tb += b; tp += p
        print(f'm={m}: LCL pairs checked {tp}, violations {tb}')
