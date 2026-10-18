# test parent-designation rules for tripods (2 children each) and qO edges (1 child each):
# rule valid on D if every maximum is a child at most once (per family).
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from hyper import cells
E = [(1,0,0),(0,1,0),(0,0,1)]
def arms(x, tops):
    return [sum(tops[a]) - sum(x) for a in range(3)]
def toplist(D, x):
    out = []
    for a in range(3):
        y = x
        while tuple(y[i] + E[a][i] for i in range(3)) in D: y = tuple(y[i] + E[a][i] for i in range(3))
        out.append(y)
    return out
TRULES = {
 'longest': lambda k: max(range(3), key=lambda a: (k[a], a)),
 'longest_r': lambda k: max(range(3), key=lambda a: (k[a], -a)),
 'shortest': lambda k: min(range(3), key=lambda a: (k[a], a)),
 'dir3': lambda k: 2, 'dir1': lambda k: 0,
 'zeroarm': lambda k: ([a for a in range(3) if k[a] == 0] or [max(range(3), key=lambda a: k[a])])[0],
}
M = int(sys.argv[1])
bad = {r: 0 for r in TRULES}; ex = {}
qbad = {r: 0 for r in ['longest', 'shortest', 'dir_lo', 'dir_hi']}; qex = {}
nD = 0
for key, D, C in gen(M):
    Max, cl = cells(D); nD += 1
    tr = []
    for kind, x, ms in cl:
        if kind == 'T':
            tp = toplist(D, x); tr.append((x, tp, arms(x, tp)))
    for r, f in TRULES.items():
        cnt = {}
        for x, tp, k in tr:
            p = f(k)
            for a in range(3):
                if a != p: cnt[tp[a]] = cnt.get(tp[a], 0) + 1
        if any(v > 1 for v in cnt.values()):
            bad[r] += 1; ex.setdefault(r, key)
    qo = []
    for kind, x, ms in cl:
        if kind == 'O':
            tp = toplist(D, x); k = arms(x, tp)
            dirs = [a for a in range(3) if tp[a] in Max]
            qo.append((x, tp, k, dirs))
    for r in qbad:
        cnt = {}
        for x, tp, k, dirs in qo:
            a, b = dirs
            if r == 'longest': ch = a if k[a] < k[b] or (k[a] == k[b] and a < b) else b
            elif r == 'shortest': ch = a if k[a] > k[b] or (k[a] == k[b] and a < b) else b
            elif r == 'dir_lo': ch = a
            else: ch = b
            cnt[tp[ch]] = cnt.get(tp[ch], 0) + 1
        if any(v > 1 for v in cnt.values()): qbad[r] += 1; qex.setdefault(r, key)
print("sets", nD)
for r in TRULES: print("tripod rule", r, "bad", bad[r], ex.get(r))
for r in qbad: print("qO rule", r, "bad", qbad[r], qex.get(r))
