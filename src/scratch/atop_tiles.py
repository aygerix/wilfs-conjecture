# ATOP (X = all maximal cells) on every stored non-two-face 3-D lattice tile of logs/tiles/m{m}.jsonl.
import sys, json, time; sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from atop_shape import atop_shape
def rebuild(h, F, G, q):
    S = set()
    for i in range(len(h)):
        for j in range(h[i]):
            for k in range(min(F[i], G[j])):
                if q is None or not (i >= q[0] and j >= q[1] and k >= q[2]): S.add((i, j, k))
    return S
m = int(sys.argv[1]); step = int(sys.argv[2]) if len(sys.argv) > 2 else 1
t0 = time.time(); n = bad = 0; worst = None
for i, line in enumerate(open(f'logs/tiles/m{m}.jsonl')):
    if i % step: continue
    rec = json.loads(line); D = rebuild(rec['h'], rec['F'], rec['G'], rec['q']); assert len(D) == m
    lhs, rhs, _, _, nx = atop_shape(sorted(D)); n += 1
    sl = (rhs - lhs) / rhs
    if sl < -1e-9: bad += 1; print('FAIL', rec['r'], 'cone' if rec['q'] else 'C', f'slack {sl:+.4f}', 'h', rec['h'], 'F', rec['F'], 'G', rec['G'], 'q', rec['q'], flush=True)
    if worst is None or sl < worst[0]: worst = (round(sl, 4), rec['r'], rec['q'])
print(f'm={m} step {step}: {n} tiles, ATOP fails {bad}; worst slack {worst}; {time.time()-t0:.0f}s')
