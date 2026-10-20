r"""Exact DEAD bookkeeping on the sharp family F(s, m): S = <m, m+s, ..., m+2s-1>, 2s-1 <= m <= 3s-1 (lead, 2026-10-20).
Prints W, Lam - O, D = W - (Lam - O) and the closed-form guesses.  usage: famF.py smax"""
import sys
sys.path.insert(0, ".")
from dead import info
smax = int(sys.argv[1])
for s in range(3, smax + 1):
    row = []
    for m in range(2 * s - 1, 3 * s):
        r = info([m] + list(range(m + s, m + 2 * s)))
        if r is None: continue
        row.append((m, r["W"], r["Lam"] - r["O"], r["D"], r["c"], r["e"]))
    best = min(row, key=lambda t: t[3])
    print("s", s, "min D", best[3], "at m", best[0], "(W %d, Lam-O %d)" % (best[1], best[2]), " D by m:", [t[3] for t in row])
