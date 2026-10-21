r"""CR_DEP and CR (MaxCL crude rearrangement) on given S (lead, 2026-10-20); lex tile.  Prints normalized slacks
(slack / m^2) and the values Dep, |boundary|, |A|.  Usage: python crdep_list.py 'm g1 g2 ...' ..."""
import sys
sys.path.insert(0, '.')
from tile import build
from crdep import crdep
for arg in sys.argv[1:]:
    a = list(map(int, arg.split())); m = a[0]
    c, gens, M = build(m, a[1:]); D = list(M); d = len(gens); Ds = set(D)
    sl, dep = crdep(D, d)
    up = lambda x, b: tuple(x[t] + (t == b) for t in range(d))
    A = [x for x in D if all(up(x, b) not in Ds for b in range(d))]
    T = sorted((d + sum(y) for y in A), reverse=True)
    cr = (d + 1) * m * (m - 1) // 2 - sum(v * (m - 1 - i) for i, v in enumerate(T))
    g = sum(w // m for w in M.values()); W = (d + 1) * (c - g) - c
    print("<%d|%s> c=%d e=%d W=%d  CR_DEP slack/m^2 %.4f  CR slack/m^2 %.4f  Dep=%d |A|=%d" % (m, gens, c, d + 1, W, sl / m / m, cr / m / m, dep, len(A)), flush=True)
