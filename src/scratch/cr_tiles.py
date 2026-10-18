# CR on lattice tiles (shape only): stored non-two-face 3-D tiles (logs/tiles) and exhaustive enumeration (tile_enum).
import sys, json, time; sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
def rebuild(h, F, G, q):
    return {(i, j, k) for i in range(len(h)) for j in range(h[i]) for k in range(min(F[i], G[j]))
            if q is None or not (i >= q[0] and j >= q[1] and k >= q[2])}
def crD(D):
    d = 3; m = len(D); U = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    A = sorted((d + sum(y) for y in D if all(tuple(p + q for p, q in zip(y, u)) not in D for u in U)), reverse=True)
    return sum(t * (m - 1 - i) for i, t in enumerate(A)) / ((d + 1) * m * (m - 1) / 2)
mode = sys.argv[1]
if mode == 'dump':
    for m in (30, 40, 50, 60, 64):
        t0 = time.time(); w = None; bad = 0; n = 0
        for line in open(f'logs/tiles/m{m}.jsonl'):
            rec = json.loads(line); r = crD(rebuild(rec['h'], rec['F'], rec['G'], rec['q'])); n += 1
            bad += r > 1 + 1e-12
            if w is None or r > w[0]: w = (round(r, 4), rec['r'], 'cone' if rec['q'] else 'C')
        print(f'm={m}: {n} non-two-face tiles, CR fails {bad}, worst {w}, {time.time()-t0:.0f}s', flush=True)
else:
    from tile_enum import enumerate_tiles
    for m in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        res = {False: [0, 0, None], True: [0, 0, None]}; seen = set()
        for r, D, poly in enumerate_tiles(m):
            key = frozenset(D)
            if key in seen: continue
            seen.add(key); D = set(D)
            two = any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a + 1, 3))
            v = crD(D); R = res[two]; R[0] += 1; R[1] += v > 1 + 1e-12
            if R[2] is None or v > R[2][0]: R[2] = (round(v, 4), r)
        print(f'm={m}: non-two-face {res[False][0]} tiles, CR fails {res[False][1]}, worst {res[False][2]} | two-face {res[True][0]}, fails {res[True][1]}, worst {res[True][2]}', flush=True)
