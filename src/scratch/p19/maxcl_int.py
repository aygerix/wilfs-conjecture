"""MaxCL (grlex factorization tile) on the CHAIN-H3 counterexample family <m, m+a..m+a+L-1> (lead, 2026-10-19).
Prints the minimum MaxCL slack over sigma, the slack at sigma = c mod m (the one Wilf needs), both / m^2, and W.
usage: python maxcl_int.py  (built-in list)  |  python maxcl_int.py m a L"""
import sys
sys.path.insert(0, '../../h3'); sys.path.insert(0, '/home/jmercedes/wilf/h3')
from maxcl_h3 import check
cases = [(53, 32, 11), (58, 35, 12), (63, 38, 13), (68, 41, 14), (73, 44, 15), (78, 47, 16), (89, 52, 19), (28, 17, 6), (33, 20, 7), (38, 23, 8)]
if len(sys.argv) == 4: cases = [tuple(map(int, sys.argv[1:4]))]
for (m, a, L) in cases:
    gens = list(range(m + a, m + a + L))
    r = check(m, gens)
    if r is None: print(m, a, L, 'skipped'); continue
    H, d, c, W, mn, atc, sg = r
    print('m=%d gens=%d..%d H=%d e=%d c=%d W=%d  MaxCL min slack=%d (%.4f m^2) at sigma=%d; at sigma=c: %d (%.4f m^2)' % (m, m+a, m+a+L-1, H, d+1, c, W, mn, mn/m/m, sg, atc, atc/m/m), flush=True)
