# Berge-acyclicity via ordering: process hyperedges in a given order; each new edge must meet the union of earlier edges' vertex sets in <= 1 vertex
# AND (for genuine acyclicity w.r.t. components) we just test the stronger "<=1 vertex in union" property.
import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from hyper import cells
ORD = {
 'sum_desc': lambda x: -sum(x), 'sum_asc': lambda x: sum(x),
 'lex_desc': lambda x: tuple(-c for c in x), 'lex_asc': lambda x: x,
 'x3_desc': lambda x: (-x[2], -sum(x)), 'x3_asc': lambda x: (x[2], sum(x)),
 'min_desc': lambda x: (-min(x), -sum(x)), 'max_desc': lambda x: (-max(x), -sum(x)),
}
M = int(sys.argv[1]); fam = sys.argv[2] if len(sys.argv) > 2 else 'T'
bad = {r: 0 for r in ORD}; ex = {}; nD = 0
for key, D, C in gen(M):
    Max, cl = cells(D); nD += 1
    ed = [(x, ms) for (k, x, ms) in cl if k in fam]
    for r, f in ORD.items():
        seen = set(); ok = True
        for x, ms in sorted(ed, key=lambda e: f(e[0])):
            if len(seen & set(ms)) > 1: ok = False; break
            seen |= set(ms)
        if not ok: bad[r] += 1; ex.setdefault(r, key)
print("sets", nD, "family", fam)
for r in ORD: print(r, bad[r], ex.get(r))
