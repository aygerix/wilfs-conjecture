import sys
def Tdata(m, A):
    gens = sorted(A + [m]); N = 3 * m + 2
    inT = [False] * (N + 1); inT[0] = True
    for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in gens)
    cT = max(x for x in range(N + 1) if not inT[x]) + 1
    lT = sum(1 for x in range(cT) if inT[x])
    eT = sum(1 for g in gens if not any(inT[g - y] and inT[y] for y in range(1, g)))
    return cT, lT, eT
for f in sys.argv[1:]:
    for L in open(f):
        t = L.split()
        if t[0] != 'DUMP': continue
        v = list(map(int, t[1:15])); A = list(map(int, t[15:])); m, e = v[0], v[1]
        cT, lT, eT = Tdata(m, A)
        if eT == e: print('rho=0:', 'm', m, 'A', A, 'gens', ','.join(str(m + a) for a in [0] + A), 'D3', v[2], 'h', v[4], 'hlo', v[5], 'hhi', v[6], 'ne2', v[7], 'ne3', v[8], 'dc', v[9], 'cT', cT, 'lT', lT)
