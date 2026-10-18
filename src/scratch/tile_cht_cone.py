# Cone tiles vs class C: per m, over non-two-face tiles split by q* present / absent:
#   max(t - C), max(2Tri + Q' - 2C), max(LHS - 4C) (LHS = 2t + 2Tri + Q'), min CHT slack m + 1 - LHS, max C/sqrt(m).
# usage: tile_cht_cone.py m...
import sys, math
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from tile_cht import cht
from cht_corners import corners
from tile_cone_peel import qstars
if __name__ == '__main__':
    from tile_enum import enumerate_tiles
    for m in map(int, sys.argv[1:]):
        st = {False: None, True: None}
        for r, D, poly in enumerate_tiles(m):
            if any(tuple(int(i in (a, b)) for i in range(3)) not in D for a in range(3) for b in range(a+1, 3)): continue
            S = set(D); t, tri, q0, q1 = cht(S); C = corners(S); hq = bool(qstars(S))
            lhs = 2*t + 2*tri + q0 + q1
            v = (t - C, 2*tri + q0 + q1 - 2*C, lhs - 4*C, -(m + 1 - lhs), C / math.sqrt(m))
            if st[hq] is None: st[hq] = [list(v), [r]*5, 0]
            for i in range(5):
                if v[i] > st[hq][0][i]: st[hq][0][i] = v[i]; st[hq][1][i] = r
            st[hq][2] += 1
        for hq in (False, True):
            if st[hq] is None: continue
            a = st[hq][0]
            print(f'm={m} {"cone" if hq else "C   "} n={st[hq][2]}: max(t-C) {a[0]} max(2Tri+Q-2C) {a[1]} max(LHS-4C) {a[2]} [r={st[hq][1][2]}] '
                  f'min CHT slack {-a[3]} [r={st[hq][1][3]}] max C/sqrt(m) {a[4]:.2f}', flush=True)
