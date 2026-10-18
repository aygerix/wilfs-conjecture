# per-cell s(z) = sum_a ht(t_a(z)) - 1 (so H - m = sum_z s(z)); maximal cells marked '*'
import sys; sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
def show(gens):
    s = NS.from_generators(gens); p, best = factorizations_down_set(s, 'grlex'); D = set(best.values())
    ht = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        ht[x] = max([ht[add(x, i)] + 1 for i in range(3) if add(x, i) in D], default=0)
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    sz = {x: sum(ht[top(x, i)] for i in range(3)) - 1 for x in D}
    L = [max(x[i] for x in D) + 1 for i in range(3)]
    A = [x for x in D if ht[x] == 0]
    print(gens, 'p', p, 'm', s.m, 'H-(m-1) =', sum(sz.values()) + 1, '|A| =', len(A), 'L', L)
    for k in range(L[2]):
        print(f' x3={k}:')
        for i in range(L[0]-1, -1, -1):
            row = ''.join(('   .' if (i, j, k) not in D else '%3d%s' % (sz[(i, j, k)], '*' if ht[(i, j, k)] == 0 else ' ')) for j in range(L[1]))
            if row.strip(' .'): print('   ', row)
for g in sys.argv[1:]: show([int(t) for t in g.split(',')])
