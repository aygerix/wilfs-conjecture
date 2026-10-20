"""Check that the digital P18 sets <a^2, a^2+1, a^2+a, a^2+a+1> are NO-WRAP: every Apery element w_i equals
j(i)*m + i, where j(i) is the least number of coins from B* = {1, a, a+1} summing to exactly i (offset sum = i < m)."""
import heapq, sys
def apery(g):
    m = min(g); w = [None]*m; w[0] = 0; h = [(0, 0)]
    while h:
        x, i = heapq.heappop(h)
        if w[i] is not None and w[i] < x: continue
        for n in g:
            j = (i + n) % m; y = x + n
            if w[j] is None or y < w[j]: w[j] = y; heapq.heappush(h, (y, j))
    return w
for a in range(3, 31):
    m = a*a; B = [1, a, a+1]; g = [m] + [m+b for b in B]
    w = apery(g)
    INF = 10**9; jm = [0] + [INF]*(m-1)
    for v in range(1, m):
        jm[v] = min(jm[v-b] + 1 for b in B if b <= v)
    ok = all(w[i] == jm[i]*m + i for i in range(m))
    M = max(w); c = M - m + 1; g_ = sum(x // m for x in w); ell = c - g_
    print(a, m, "nowrap" if ok else "WRAP", "q=%d" % -(-c // m), "ratio=%.4f" % (4*ell/c))
