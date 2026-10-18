import sys
sys.path.insert(0, sys.path[0])
from classify import gen
from perlev2 import perlevel
M = int(sys.argv[1]); want = int(sys.argv[2]); shown = 0; seen = set()
for key, D, C in gen(M):
    S = perlevel(D, 2)
    for v, s in enumerate(S[:-1]):
        if s[0] == 0 and s[5] >= want and (s[1:]) not in seen:
            seen.add(s[1:]); print(key, 'level', v, 'S,m,nu,ad,bd,tri,q =', s); shown += 1
    if shown >= 8: break
