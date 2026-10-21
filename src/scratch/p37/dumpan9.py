# joint distribution of rho = e - e_T and h_lo on the residual; min A1-eT slack per rho; max h_lo per rho
import sys
def Tdata(m, A):
    gens = sorted(A + [m]); N = 3 * m + 2
    inT = [False] * (N + 1); inT[0] = True
    for x in range(1, N + 1): inT[x] = any(x >= g and inT[x - g] for g in gens)
    cT = max(x for x in range(N + 1) if not inT[x]) + 1
    lT = sum(1 for x in range(cT) if inT[x])
    eT = sum(1 for g in gens if not any(inT[g - y] and inT[y] for y in range(1, g)))
    return cT, lT, eT
for fn in sys.argv[1:]:
    tab = {}; e = None; mxh = {}
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            v = list(map(int, t[1:15])); A = list(map(int, t[15:])); m = v[0]; e = v[1]
            cT, lT, eT = Tdata(m, A); rho = e - eT; hlo = v[5]; h = v[4]
            tab[(rho, hlo)] = tab.get((rho, hlo), 0) + 1
            mxh[rho] = max(mxh.get(rho, (0, 0)), (hlo, h))
    print(fn, 'e', e)
    for rho in sorted(set(k[0] for k in tab)):
        print('   rho', rho, ' max (hlo, h)', mxh[rho], ' hlo counts:', {k[1]: c for k, c in sorted(tab.items()) if k[0] == rho})
