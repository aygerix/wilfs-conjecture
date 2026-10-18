# list the k NON-two-face tiles with smallest H - (m-1) for given m (complete enumeration), with shape summary
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles
from heightH import H_of
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def summary(D):
    L = [max(x[i] for x in D) + 1 for i in range(3)]
    core = sum(1 for x in D if min(x) >= 1)
    A = [x for x in D if all(add(x, i) not in D for i in range(3))]
    B = [sum(1 for x in D if x[c] == 0) for c in range(3)]
    return dict(L=L, core=core, A=len(A), TA=sum(sum(y) + 3 for y in A), faces=B)
m = int(sys.argv[1]); k = int(sys.argv[2]); out = []
for r, D, poly in enumerate_tiles(m):
    if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
    out.append((H_of(set(D)) - (m - 1), r, D))
out.sort(key=lambda t: t[0])
for sl, r, D in out[:k]:
    print(sl, r, summary(D))
    if len(sys.argv) > 3: print('   ', sorted(D))
