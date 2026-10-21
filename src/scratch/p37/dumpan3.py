import sys
for fn in sys.argv[1:]:
    R = []
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        v = list(map(int, t[1:15])); R.append(v + [list(map(int, t[15:]))])
    e = R[0][1]; d = e - 1; C2 = d * (d + 1) // 2; C3 = d * (d + 1) * (d + 2) // 6
    by = {}
    for x in R:
        M2T = C2 - x[10]; M3T = C3 - x[11]
        by.setdefault(M2T, []).append((x[3], x[2], x[4], M3T, x))
    print(fn, 'e', e, 'C2', C2, 'C3', C3)
    for k in sorted(by):
        L = by[k]; mn = min(L, key=lambda t: t[0])
        print(f"   M2T={k}: n={len(L)} min DEQ={mn[0]} (D3={mn[1]} h={mn[2]} M3T={mn[3]} m={mn[4][0]} A={mn[4][14]})  min M3T={min(t[3] for t in L)} max h={max(t[2] for t in L)}")
