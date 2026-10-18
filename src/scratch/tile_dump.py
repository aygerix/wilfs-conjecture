# Dump every non-two-face 3-D Apery tile of index m as its cylinder data (h, F, G, q*) plus invariants.
# One JSON line per tile: r, L, h, F, G, q (or null), k (outer corners of faces A1, A2, A3), C, t (#maximal cells).
# Faces: A3 = {x3 = 0} (column heights h(x1)), A2 = {x2 = 0} (F(x1) = height in x3), A1 = {x1 = 0} (G(x2)).
# Each record is checked: rebuild(h, F, G, q) == D.   usage: tile_dump.py m...  -> logs/tiles/m{m}.jsonl
import sys, json
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from tile_cone_peel import qstars
def faces(D):
    L = [max(x[a] for x in D) + 1 for a in range(3)]
    h = [sum(1 for j in range(L[1]) if (i, j, 0) in D) for i in range(L[0])]
    F = [sum(1 for k in range(L[2]) if (i, 0, k) in D) for i in range(L[0])]
    G = [sum(1 for k in range(L[2]) if (0, j, k) in D) for j in range(L[1])]
    return L, h, F, G
def rebuild(h, F, G, q):
    S = set()
    for i in range(len(h)):
        for j in range(h[i]):
            for k in range(min(F[i], G[j])):
                if q is None or not (i >= q[0] and j >= q[1] and k >= q[2]): S.add((i, j, k))
    return S
def kcorners(seq):  # outer corners of a 2-D down-set given by its nonincreasing column heights = #distinct values
    return len(set(seq))
if __name__ == '__main__':
    for m in map(int, sys.argv[1:]):
        n = 0
        with open(f'logs/tiles/m{m}.jsonl', 'w') as out:
            for r, D, poly in enumerate_tiles(m):
                if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
                D = set(D); Q = qstars(D); assert len(Q) <= 1
                q = list(Q[0]) if Q else None
                L, h, F, G = faces(D)
                assert rebuild(h, F, G, q) == D, (r, h, F, G, q)
                t = sum(1 for x in D if all(tuple(x[s] + (s == a) for s in range(3)) not in D for a in range(3)))
                k = [kcorners(G), kcorners(F), kcorners(h)]
                out.write(json.dumps({'r': list(r), 'L': L, 'h': h, 'F': F, 'G': G, 'q': q, 'k': k, 'C': sum(k), 't': t}) + '\n')
                n += 1
        print(f'm={m}: {n} non-two-face tiles dumped', flush=True)
