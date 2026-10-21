# murun: for each class s, k(s) = least k >= 0 with sigma(s - k mu) < m (small); K = max_s k(s) (inf if some mu-cycle has no
# small class).  If K <= e-1 then s -> (s - k(s) mu, k(s)) injects classes into Z x [0, e-1], so e z >= m (Z1).
# Also kA(s) = least number of steps back by arbitrary a in A along standard values ... (here: BFS over s -> s - a, any a).
import sys
from itertools import combinations_with_replacement as cwr
from collections import Counter
for fn in sys.argv[1:]:
    hist = Counter(); hist_le = Counter(); worst = None; n = 0
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        m = int(t[1]); A = list(map(int, t[15:])); d = len(A); e = d + 1; mu = A[0]; n += 1
        best = {}
        for k in range(4):
            for c in cwr(range(d), k):
                s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
                if cl not in best or key < best[cl]: best[cl] = key
        sg = {cl: best[cl][0] + best[cl][1] * m for cl in best}
        K = 0
        for s in range(m):
            k = 0; x = s
            while sg[x] >= m and k <= m: x = (x - mu) % m; k += 1
            K = max(K, k)
        K = K if K <= m else 999
        hist[K - (e - 1)] += 1
        if mu <= e: hist_le[K - (e - 1)] += 1
        if worst is None or K - (e - 1) > worst[0]: worst = (K - (e - 1), m, A)
    print(fn, n, 'S; histogram of K-(e-1):', sorted(hist.items()), '| mu<=e:', sorted(hist_le.items()), 'worst', worst)
