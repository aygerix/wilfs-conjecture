# Conjecture (K): 2|Tri| + |Q'| <= 2t - 2.  Per m over non-two-face tiles (split q*-free / cone):
# max(2Tri + Q' - 2t), max(t - (m+3)/4) [CHT holds if 4t - 3 <= m given (K)].   usage: tile_K.py m...
import sys
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_cht import cht
from tile_cone_peel import qstars
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        st = {}
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            S = set(D); t, tri, q0, q1 = cht(S); hq = bool(qstars(S))
            k = 2*tri + q0 + q1 - 2*t
            a = st.setdefault(hq, [k, r, t, r, 0]); a[4] += 1
            if k > a[0]: a[0], a[1] = k, r
            if t > a[2]: a[2], a[3] = t, r
        for hq in sorted(st):
            a = st[hq]
            print(f'm={m} {"cone" if hq else "C   "} n={a[4]}: max(2Tri+Q-2t) {a[0]} [r={a[1]}]  max t {a[2]} [r={a[3]}]  (m+3)/4 = {(m+3)/4}', flush=True)
