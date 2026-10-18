import sys
sys.path.insert(0, sys.path[0])
E = [(1,0,0),(0,1,0),(0,0,1)]
add = lambda x,e: (x[0]+e[0],x[1]+e[1],x[2]+e[2])
def build(h, F, G, q=None):
    D = {(i,j,k) for i in range(len(h)) for j in range(h[i]) for k in range(min(F[i], G[j]))}
    if q: D = {x for x in D if not all(x[a] >= q[a] for a in range(3))}
    return D
def info(D):
    Max = {x for x in D if all(add(x,e) not in D for e in E)}
    best = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        b = sum(x)
        for e in E:
            z = add(x,e)
            if z in D: b = max(b, best[z])
        best[x] = b
    ht = {x: best[x]-sum(x) for x in D}
    def top(x,a):
        while add(x,E[a]) in D: x = add(x,E[a])
        return x
    lab = {}
    for x in D:
        if x in Max: lab[x] = 'M'; continue
        tops = [top(x,a) for a in range(3)]
        n = sum(tp in Max for tp in tops); hh = sum(ht[tp] for tp in tops)
        if n == 3: lab[x] = 'T'
        elif n == 2 and hh == 1:
            c = [a for a in range(3) if tops[a] not in Max][0]
            lab[x] = ('u' if tops[c] == x else 'o') + str(c+1)
        else: lab[x] = str(min(hh, 9))
    return lab
def show(D):
    lab = info(D)
    L3 = max(x[2] for x in D) + 1; L1 = max(x[0] for x in D)+1; L2 = max(x[1] for x in D)+1
    for k in range(L3):
        print(f'level x3={k}:')
        for j in reversed(range(L2)):
            print('   ' + ' '.join(f'{lab.get((i,j,k), "."):>2}' for i in range(L1)))
if __name__ == '__main__':
    h, F, G = [tuple(map(int, a.split(','))) for a in sys.argv[1:4]]
    q = tuple(map(int, sys.argv[4].split(','))) if len(sys.argv) > 4 else None
    D = build(h, F, G, q); show(D)
