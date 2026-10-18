# Arms bound for down-sets (exact for the decomposition, lower bound for Gamma_c):
#   3*delta - 3 = sum_c Gamma_c,  Gamma_c = sum_v v * gamma_v,  gamma_v = sum_{u in L_v} (3 ht_{L_v}(u) - 1),
#   L_v = U_v \ U_{v+1},  U_v = {u in A_c : l_c(u) >= v}  (l_c = column length in direction c over the face A_c).
# For cylindrical (q*-free) sets L_v = V (right arm) u Hz (top arm) and gamma_v >= g(V) + g(Hz), g(P) = sum (3 ht_P - 1).
# AB := sum_c sum_v v (g(V_v) + g(Hz_v));  SC := sum of v over singleton arms.  Reports exact sum Gamma, AB, SC.
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def g2(P):
    P = set(P); ht = {}
    for u in sorted(P, key=lambda u: -(u[0] + u[1])):
        ht[u] = max([ht[w] + 1 for w in ((u[0]+1, u[1]), (u[0], u[1]+1)) if w in P], default=0)
    return sum(3*h - 1 for h in ht.values())
def face_data(D, c):
    a, b = [i for i in range(3) if i != c]
    col = {}
    for x in D:
        u = (x[a], x[b]); col[u] = col.get(u, 0) + 1
    return col
def arms(D):
    tot_exact = 0; AB = 0; SC = 0
    for c in range(3):
        col = face_data(D, c)
        vmax = max(col.values())
        for v in range(1, vmax + 1):
            U = {u for u, l in col.items() if l >= v}; U1 = {u for u, l in col.items() if l >= v + 1}
            L = U - U1
            if not L: continue
            # exact gamma_v (heights within L, which is up-closed in U)
            tot_exact += v * g2(L)
            X1 = max([u[0] for u in U1], default=-1) + 1; Y1 = max([u[1] for u in U1], default=-1) + 1
            V = {u for u in L if u[0] >= X1}; Hz = L - V
            for P in (V, Hz):
                if P:
                    gp = g2(P); AB += v * gp
                    if len(P) == 1: SC += v
    return tot_exact, AB, SC
if __name__ == '__main__':
    from heightH import H_of
    from tile_enum import enumerate_tiles
    from tile_cone_peel import qstars
    for m in map(int, sys.argv[1:]):
        worst = None; chk = 0
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            S = set(D)
            if qstars(S): continue
            ex, AB, SC = arms(S)
            assert ex == 3*(H_of(S) - (m - 1)) - 3, (r, ex)
            chk += 1
            if worst is None or AB < worst[0]: worst = (AB, SC, ex, r)
        print(f'm={m}: q*-free non-two-face tiles {chk}; min AB (AB, SC, exact 3delta-3, r) = {worst}', flush=True)
