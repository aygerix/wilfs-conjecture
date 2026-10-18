# Level-telescoping slack of Lemma T' along direction c: slices U_v = {p : (p, v-1) in D} (p in the (a,b)-plane),
# M_v = corners of U_v not in U_{v+1}; nu_v = #corners of U_{v+1} that are not corners of U_v; d_v = #drops of the two
# face profiles between v and v+1 (a_v = #{i: F(i) >= v} etc).  t = kappa(U_1) + sum nu_v; C - t = sum slack.
import sys
sys.path.insert(0, 'src/scratch')
from cls_anneal import build
def corners(U):
    return {p for p in U if (p[0]+1, p[1]) not in U and (p[0], p[1]+1) not in U}
def slices(D, c):
    a, b = [d for d in range(3) if d != c]
    L = max(x[c] for x in D) + 1
    return [{(x[a], x[b]) for x in D if x[c] == v - 1} for v in range(1, L + 2)], a, b
def face_vals(D, c, a, b):
    # a_v = # a-columns of face x_b = 0 with height >= v ; b_v similarly
    Fa = {}; Gb = {}
    for x in D:
        if x[b] == 0: Fa[x[a]] = max(Fa.get(x[a], 0), x[c] + 1)
        if x[a] == 0: Gb[x[b]] = max(Gb.get(x[b], 0), x[c] + 1)
    return Fa, Gb
def report(D, c, verbose=True):
    U, a, b = slices(D, c)
    Fa, Gb = face_vals(D, c, a, b)
    av = lambda v: sum(1 for i in Fa if Fa[i] >= v); bv = lambda v: sum(1 for j in Gb if Gb[j] >= v)
    out = []
    for v in range(1, len(U)):
        if not U[v - 1]: break
        Uv, Uw = U[v - 1], U[v] if v < len(U) else set()
        cv, cw = corners(Uv), corners(Uw)
        nu = len(cw - cv); d = (av(v + 1) < av(v)) + (bv(v + 1) < bv(v))
        out.append((v, d, nu, d - nu))
    if verbose:
        print('direction', c, 'kappa(U1)', len(corners(U[0])), 'levels with d != nu:', [(v, d, nu) for v, d, nu, s in out if s != 0])
    return out
if __name__ == '__main__':
    h, F, G, q = [eval(a) for a in sys.argv[1:5]]
    D = build(h, F, G, q)
    for c in range(3): report(D, c)
