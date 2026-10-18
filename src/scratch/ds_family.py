# Lattice-free family with many doubly-same qO cells at p = (q1, q2) = (1, 1): q = (1, 1, Q)
import sys
sys.path.insert(0, 'src/scratch')
from cls_anneal import build
from corner_anneal import valid
from qo_cone import qo_stats
from qo_fiber import dbl
for Q in range(4, 13):
    L3 = Q + 3
    F = [L3, Q + 1, Q] + list(range(Q - 1, 0, -1))
    G = [L3, Q + 1, Q - 1] + list(range(Q - 2, 0, -1))
    h = [len(G), len(G)] + [2] * (len(F) - 2)
    q = (1, 1, Q)
    D = build(h, F, G, q)
    s = qo_stats(D, q)
    n, t, a, g = dbl(D)
    print(Q, 'm', len(D), 'RCON', valid(h, F, G, list(q), 'cone'), 'conefree', valid(h, F, G, list(q), 'conefree'), s, '#DS', n)
