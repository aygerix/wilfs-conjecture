# which generators of T = <m, A> are redundant on the residual: is m in <A>?  minimal number of A-summands of m.
import sys
for fn in sys.argv[1:]:
    R = []
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            R.append(list(map(int, t[1:15])) + [list(map(int, t[15:]))])
    e = R[0][1]; cnt = {}; nomex = []
    for x in R:
        m, A = x[0], x[14]
        # least number of A-summands of m (inf if m not in <A>)
        INF = 99; best = [INF] * (m + 1); best[0] = 0
        for v in range(1, m + 1):
            for a in A:
                if a <= v and best[v - a] + 1 < best[v]: best[v] = best[v - a] + 1
        k = best[m]
        cnt[k if k < INF else 'not'] = cnt.get(k if k < INF else 'not', 0) + 1
        if k >= INF: nomex.append((m, A))
    print(fn, 'e', e, 'n', len(R), 'least #A-summands of m:', dict(sorted(cnt.items(), key=lambda t: (isinstance(t[0], str), t[0]))))
    for ex in nomex[:3]: print('   m not in <A>:', ex)
