import sys, time
sys.path.insert(0, 'src')
from ns import all_by_genus
from top2 import top2
G = int(sys.argv[1])
t0 = time.time()
n = f = tight = 0
tight_notW0 = 0
mins = {}
for g, s in all_by_genus(G):
    if s.m == 1:
        continue
    lhs2, rhs = top2(s)
    n += 1
    if lhs2 > rhs:
        f += 1
        print('FAIL', s.P, s.c, s.W, flush=True)
    elif lhs2 == rhs:
        tight += 1
        if s.W != 0:
            tight_notW0 += 1
            print('tight but W!=0', s.P, s.W, flush=True)
    if s.W == 0 and lhs2 != rhs:
        print('W=0 but not tight', s.P, flush=True)
print(f"genus<={G}: {n} semigroups; TOP'' fails {f}; tight {tight}; tight-with-W>0 {tight_notW0}; {time.time()-t0:.0f}s", flush=True)
