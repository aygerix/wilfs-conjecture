r"""LOC4 extremals (lead, 2026-10-20): local fakes ((C1),(C3); m -> m_eff) ranked by W_eff, with all terms of
W = E1 + E3_L + T - P_hi - e*delta + 3*delta_hi + 3*omega.  usage: exh k mlo mhi top | rnd k mlo mhi N seed top"""
import sys, itertools, random, heapq
sys.path.insert(0, '.')
from zw import configs
def terms(m, B):
    A = [0] + list(B); X2 = set(p + q for p in A for q in A)
    return X2
heap = []
def rec(m, B, top):
    for r in configs(m, B):
        key = (r["W"], r["m"], r["B"], r["h"])
        if len(heap) < top: heapq.heappush(heap, (-r["W"], key, r))
        elif r["W"] < -heap[0][0]: heapq.heapreplace(heap, (-r["W"], key, r))
a = sys.argv
if a[1] == "exh":
    k, mlo, mhi, top = map(int, a[2:6])
    for m in range(mlo, mhi + 1):
        for B in itertools.combinations(range(1, m), k): rec(m, B, top)
else:
    k, mlo, mhi, N, seed, top = map(int, a[2:8]); random.seed(seed)
    for _ in range(N):
        m = random.randint(mlo, mhi); rec(m, sorted(random.sample(range(1, m), k)), top)
for _, key, r in sorted(heap, key=lambda t: -t[0]):
    print(r["W"], "real" if r["real"] else "fake", "m", r["m"], "B", r["B"], "h", r["h"], "a", r["a"], "E1", r["E1"], "E3", r["E3"], "T", r["T"], "Phi", r["Phi"], "Z", r["Z"])
