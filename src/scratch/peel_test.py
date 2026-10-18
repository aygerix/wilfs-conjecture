# Peeling: for D' = {x : x + e_c in D},  H(D) = H(D') + sum_{x in F_c} h(x)  (h(x) = sum_a ht(t_a x)), exactly.
# So H(D) - (|D|-1) = [H(D') - (|D'|-1)] + Psi_c(D),  Psi_c(D) = sum_{x in F_c} (h(x) - 1).
# (P1): max_c Psi_c(D) >= 0.  Test on exhaustive q*-free cylindrical sets (sizes <= M) and on tiles.
# usage: peel_test.py cyl M | peel_test.py tiles m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from heightH import H_of
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def psis(D):
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    h = {x: sum(ht[top(x, a)] for a in range(3)) for x in D}
    return [sum(h[x] - 1 for x in D if x[c] == 0) for c in range(3)]
def peel(D, c):
    return {x[:c] + (x[c] - 1,) + x[c+1:] for x in D if x[c] >= 1}
if __name__ == '__main__':
    if sys.argv[1] == 'cyl':
        from cyl_exhaust import stairs
        M = int(sys.argv[2]); worst = {}
        for L1 in range(2, M):
            for L2 in range(2, M):
                if L1 + L2 + 3 > M: break
                for L3 in range(2, M):
                    if L1 + L2 + L3 + 1 > M: break
                    for h in stairs(L1, L2, 2):
                        for f in stairs(L1, L3, 2):
                            for g in stairs(L2, L3, 2):
                                m = sum(min(f[i], g[j]) for i in range(L1) for j in range(h[i]))
                                if m > M: continue
                                D = {(i, j, k) for i in range(L1) for j in range(h[i]) for k in range(min(f[i], g[j]))}
                                v = max(psis(D))
                                if m not in worst or v < worst[m][0]: worst[m] = (v, (h, f, g))
        for m in sorted(worst): print(m, worst[m], flush=True)
    else:
        from tile_enum import enumerate_tiles
        for m in map(int, sys.argv[2:]):
            worst = None; neg = 0
            for r, D, poly in enumerate_tiles(m):
                if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
                v = max(psis(set(D))); neg += v < 0
                if worst is None or v < worst[0]: worst = (v, r)
            print(f'm={m}: max_c Psi_c < 0 for {neg} tiles; min {worst}', flush=True)
