# Classify non-two-face tiles by q* (full-support minimal non-element): none / (1,1,1) [three-face] / other.
# Report count and min H-(m-1) per class.   usage: m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_enum import enumerate_tiles, min_nonelements
from heightH import H_of
for m in map(int, sys.argv[1:]):
    st = {}
    for r, D, poly in enumerate_tiles(m):
        if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
        D = set(D)
        qs = [q for q in min_nonelements(D) if min(q) > 0]
        cl = 'none' if not qs else ('111' if qs[0] == (1, 1, 1) else 'other')
        v = H_of(D) - (m - 1)
        c, best = st.get(cl, (0, None))
        st[cl] = (c + 1, best if best is not None and best[0] <= v else (v, r, qs))
    print(f'm={m}:', st, flush=True)
