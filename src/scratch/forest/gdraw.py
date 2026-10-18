# generic level drawing of a down-set D along direction c, with cell labels: M max, T tripod, uK/oK Q' (K = direction of non-max top), else total h
import sys
sys.path.insert(0, sys.path[0])
from hyper import cells
E = [(1,0,0),(0,1,0),(0,0,1)]
def add(x, a): y = list(x); y[a] += 1; return tuple(y)
def labels(D):
    best = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        b = sum(x)
        for a in range(3):
            z = add(x, a)
            if z in D: b = max(b, best[z])
        best[x] = b
    ht = {x: best[x] - sum(x) for x in D}
    def top(x, a):
        while add(x, a) in D: x = add(x, a)
        return x
    lab = {}
    for x in D:
        if ht[x] == 0: lab[x] = ' M'; continue
        tp = [top(x, a) for a in range(3)]; H = [ht[t] for t in tp]
        n = sum(1 for v in H if v == 0)
        if n == 3: lab[x] = ' T'
        elif n == 2 and sum(H) == 1:
            c = [a for a in range(3) if H[a]][0]
            lab[x] = ('u' if tp[c] == x else 'o') + str(c + 1)
        else: lab[x] = '%2d' % sum(H)
    return lab
def draw(D, c):
    lab = labels(D); o = [a for a in range(3) if a != c]
    L = max(x[c] for x in D) + 1; X = max(x[o[0]] for x in D) + 1; Y = max(x[o[1]] for x in D) + 1
    for v in range(L):
        print('level x%d=%d  (horizontal x%d, vertical x%d)' % (c + 1, v, o[0] + 1, o[1] + 1))
        for y in range(Y - 1, -1, -1):
            row = []
            for x in range(X):
                p = [0, 0, 0]; p[c] = v; p[o[0]] = x; p[o[1]] = y
                row.append(lab.get(tuple(p), ' .'))
            print('   ' + ' '.join(row))
if __name__ == '__main__':
    h, F, G = [eval(a) for a in sys.argv[1:4]]; c = int(sys.argv[4]) - 1
    D = {(i, j, k) for i in range(len(h)) for j in range(h[i]) for k in range(min(F[i], G[j]))}
    draw(D, c)
