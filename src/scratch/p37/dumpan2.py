import sys
for fn in sys.argv[1:]:
    R = []
    for L in open(fn):
        t = L.split()
        if t[0] != 'DUMP': continue
        v = list(map(int, t[1:15])); A = list(map(int, t[15:]))
        R.append(v + [A])
    e = R[0][1]; d = e - 1
    h1 = [x for x in R if x[4] == 1]
    h1.sort(key=lambda x: x[2])
    print(fn, 'e', e, 'h=1 count', len(h1), 'min D3', h1[0][2] if h1 else None)
    for x in h1[:3]: print('   ', 'm', x[0], 'D3', x[2], 'DEQ', x[3], 'ne2', x[7], 'ne3', x[8], 'dc', x[9], 'n2eq', x[10], 'n3eq', x[11], 'cT', x[12], 'r', x[13], 'gens', ','.join(str(x[0] + a) for a in [0] + x[14]))
    # D3 lower bound vs m?  min D3 - alpha*h  for alpha in 3..e+3
    for al in range(0, e + 4):
        mn = min(x[2] - al * x[4] for x in R); print('   alpha', al, 'min D3 - alpha h =', mn, end=';')
    print()
    print('   min D3 by m:', ' '.join(f"{mm}:{min(x[2] for x in R if x[0]==mm)}" for mm in sorted(set(x[0] for x in R))))
