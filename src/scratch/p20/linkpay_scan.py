"""Scan interval families <m, km+a..km+a+L-1> with linkpay: identity checks, CHAIN-U and CHAIN-POOR minima (lead).
usage: python linkpay_scan.py mlo mhi KMAX"""
import sys
from linkpay import linkpay
mlo, mhi, K = map(int, sys.argv[1:4])
bad = 0; cuf = 0; pf = 0; worstU = None; worstP = None; n = 0; chf = 0; wpf = 0; worstW = None
for m in range(mlo, mhi + 1):
    for k in range(1, K + 1):
        for a in range(1, m):
            for L in range(2, m - a + 1):
                r = linkpay(m, list(range(k*m + a, k*m + a + L)))
                if not r: continue
                n += 1; bad += r['idbad']
                if r['chain'] < 1: chf += 1
                if r['chainU'] < 1: cuf += 1
                if r['poor'] > 1: pf += 1
                if r['wplus'] > 1: wpf += 1
                if worstW is None or r['wplus'] > worstW[0]: worstW = (round(r['wplus'], 4), round(r['chain'], 4), m, k, a, L, r['d'] + 1)
                if worstU is None or r['chainU'] < worstU[0]: worstU = (round(r['chainU'], 4), m, k, a, L, r['d'] + 1)
                if worstP is None or r['poor'] > worstP[0]: worstP = (round(r['poor'], 4), round(r['chain'], 4), m, k, a, L, r['d'] + 1, r['nrich'])
    print('m<=%d: S=%d idfail=%d CHAIN=%d CHAIN-U=%d CHAIN-POOR=%d WILF+=%d | min chainU %s | max poor %s | max wplus %s' % (m, n, bad, chf, cuf, pf, wpf, worstU, worstP, worstW), flush=True)
