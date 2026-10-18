# Exhaustive over p for structured cores (triangles, staircases, hooks, L's) + k single-cell spikes; d = 2 + k.
import sys, io, contextlib
sys.path.insert(0, 'src/scratch')
with contextlib.redirect_stdout(io.StringIO()):
    from spikes import tile_slack, with_spikes
def tri(n): return [(x, y) for x in range(n) for y in range(n) if x + y < n]
def stair(rows): return [(x, y) for y, w in enumerate(rows) for x in range(w)]
cores = {}
for n in range(2, 8): cores[f'tri{n}'] = tri(n)
for a in range(2, 7):
    for b in range(2, 7):
        cores[f'hook{a},{b}'] = [(x, 0) for x in range(a)] + [(0, y) for y in range(1, b)]
for rows in ([4, 3, 1], [5, 3, 2], [5, 4, 2, 1], [6, 4, 3, 1], [5, 3, 3, 1], [6, 5, 3, 2, 1], [4, 4, 2, 2], [6, 3, 2, 1]):
    cores['st' + ''.join(map(str, rows))] = stair(rows)
KMAX = int(sys.argv[1])
for name, C in cores.items():
    n = len(C)
    for k in range(1, KMAX + 1):
        m = n + k; fails = 0; worst = 10**9
        for p1 in range(1, m):
            for p2 in range(1, m):
                if len({(x*p1 + y*p2) % m for x, y in C}) != n: continue
                D, p = with_spikes(C, (p1, p2), m)
                mn = min(tile_slack(D, p, m)); worst = min(worst, mn)
                if mn < 0:
                    fails += 1
                    if fails == 1: print(f'FAIL core {name} k={k} d={2+k} m={m} p={p} slack {mn}', flush=True)
        if fails: print(f'   core {name} k={k}: {fails} failing p', flush=True)
print('done')
