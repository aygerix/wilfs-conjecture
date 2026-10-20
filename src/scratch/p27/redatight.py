r"""Tightest RED-A residuals for a >= 1 (lead, 2026-10-20): rank real P18 depth-four S by reda - (e-2) and print the
pieces.  usage: exh k mlo mhi top | rnd k mlo mhi N seed top"""
import sys, itertools, random, heapq
sys.path.insert(0, '.')
from reda import run as run0
def run(m, B):
    r = run0(m, B)
    return r
heap = []
def rec(r, top):
    if r is None or r["a"] == 0: return
    key = r["reda"] - (r["e"] - 2)
    item = (-key, r["m"], r["B"], r["h"], r)
    if len(heap) < top: heapq.heappush(heap, item)
    elif key < -heap[0][0]: heapq.heapreplace(heap, item)
a = sys.argv
if a[1] == "exh":
    k, mlo, mhi, top = map(int, a[2:6])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k): rec(run(m, B), top)
else:
    k, mlo, mhi, N, seed, top = map(int, a[2:8]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); rec(run(m, sorted(random.sample(range(1, m), k))), top)
for it in sorted(heap, key=lambda t: -t[0]):
    r = it[4]; print("reda-(e-2)=%d" % (-it[0]), {x: r[x] for x in ("m", "B", "h", "e", "a", "W", "reda", "SP0", "comb", "reg")})
