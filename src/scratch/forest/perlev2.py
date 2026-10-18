# per-level telescoping test of (A4b): S_v = 2 m_v - 2 nu_v + 2 ad_v + 2 bd_v - 2 Tri_v - Q'_v  (levels along direction c)
# sum_v S_v = 2C - 4 - 2Tri - Q'.  (A4b) <=> sum S_v >= 2.
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from hyper import cells
def corners2(U):
    return {p for p in U if (p[0]+1, p[1]) not in U and (p[0], p[1]+1) not in U}
def perlevel(D, c):
    Max, cl = cells(D)
    o = [a for a in range(3) if a != c]
    L = max(x[c] for x in D) + 1
    U = [{(x[o[0]], x[o[1]]) for x in D if x[c] == v} for v in range(L)] + [set()]
    A = [len({p[0] for p in U[v]}) for v in range(L + 1)]
    B = [len({p[1] for p in U[v]}) for v in range(L + 1)]
    S = []
    for v in range(L):
        mv = sum(1 for y in Max if y[c] == v)
        nu = len(corners2(U[v+1]) - corners2(U[v]))
        ad = 1 if v <= L - 2 and A[v+1] < A[v] else 0
        bd = 1 if v <= L - 2 and B[v+1] < B[v] else 0
        tri = sum(1 for k, x, ms in cl if k == 'T' and x[c] == v)
        q = sum(1 for k, x, ms in cl if k in 'UO' and x[c] == v)
        S.append((2*mv - 2*nu + 2*ad + 2*bd - 2*tri - q, mv, nu, ad, bd, tri, q))
    return S
if __name__ == '__main__':
    M = int(sys.argv[1]); worst = {}
    for key, D, C in gen(M):
        for c in range(3):
            S = perlevel(D, c)
            tot = sum(s[0] for s in S)
            mn = min(s[0] for s in S[:-1]) if len(S) > 1 else 99
            for name, val in [('tot', -tot), ('minnontop', -mn), ('top', -S[-1][0])]:
                if name not in worst or val > worst[name][0]: worst[name] = (val, key, c, S)
    for k, v in worst.items(): print(k, -v[0], v[1], 'dir', v[2], v[3])
