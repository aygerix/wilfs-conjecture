# show a 3-D tile slice by slice (x3 = k), each cell labelled by c(z) = #{a : column top t_a(z) is maximal}; '*' = maximal
import sys; sys.path.insert(0, 'src')
from ns import NS
from cl import factorizations_down_set
def tile(gens):
    s = NS.from_generators(gens); p, best = factorizations_down_set(s, 'grlex'); return s, p, {v: k for k, v in best.items()}
def show(gens):
    s, p, cells = tile(gens); D = set(cells)
    add = lambda x, i: x[:i] + (x[i]+1,) + x[i+1:]
    def top(x, i):
        while add(x, i) in D: x = add(x, i)
        return x
    A = {x for x in D if all(add(x, i) not in D for i in range(3))}
    cz = {x: sum(top(x, i) in A for i in range(3)) for x in D}
    L = [max(x[i] for x in D) + 1 for i in range(3)]
    print(gens, 'p', p, 'm', s.m, 'c', s.c, 'T(A)-2m =', sum(cz.values()) - 2*s.m, ' #c=3:', sum(v == 3 for v in cz.values()), ' #c<=1:', sum(v <= 1 for v in cz.values()), ' #c=0:', sum(v == 0 for v in cz.values()))
    for k in range(L[2]):
        print(f' x3={k}:')
        for i in range(L[0]-1, -1, -1):
            print('   ', ''.join(('   .' if (i, j, k) not in D else '%3d%s' % (cz[(i, j, k)], '*' if (i, j, k) in A else ' ')) for j in range(L[1])))
for g in sys.argv[1:]: show([int(t) for t in g.split(',')])
