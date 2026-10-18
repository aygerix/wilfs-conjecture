# classify h<=1 cells for Loomis-Whitney sets (class C) and cone class; verify t <= C-2 proof ingredients
import sys, itertools
sys.path.insert(0, sys.path[0])
def stairs(L, top):
    def rec(prefix):
        if len(prefix) == L: yield tuple(prefix); return
        for v in range(prefix[-1], 0, -1): yield from rec(prefix + [v])
    yield from rec([top])
def analyze(D):
    E = [(1,0,0),(0,1,0),(0,0,1)]
    add = lambda x,e: (x[0]+e[0],x[1]+e[1],x[2]+e[2])
    Max = {x for x in D if all(add(x,e) not in D for e in E)}
    # ht via memo: ht(y) = max over z>=y in D of |z|-|y|
    best = {}
    for x in sorted(D, key=lambda x: -sum(x)):
        b = sum(x)
        for e in E:
            z = add(x,e)
            if z in D: b = max(b, best[z])
        best[x] = b
    ht = {x: best[x]-sum(x) for x in D}
    def top(x,a):
        while True:
            z = add(x,E[a])
            if z not in D: return x
            x = z
    res = dict(t=len(Max), tri=0, q=0, qU=0, qO=0)
    for x in D:
        if x in Max: continue
        tops = [top(x,a) for a in range(3)]
        n = sum(tp in Max for tp in tops)
        h = sum(ht[tp] for tp in tops)
        if n == 3: res['tri'] += 1
        elif n == 2 and h == 1:
            res['q'] += 1
            c = [a for a in range(3) if tops[a] not in Max][0]
            if tops[c] == x: res['qU'] += 1
            else: res['qO'] += 1
    return res
def corners(P):  # P: nonincreasing positive list
    return len(set(P))
def gen(M):
    for L1 in range(1, M+1):
        for L2 in range(1, M+1):
            if L1 + L2 - 1 > M: break
            for L3 in range(1, M+1):
                if L1 + L2 + L3 - 2 > M: break
                for h in stairs(L1, L2):
                    if sum(h) + L3 - 1 > M: continue
                    for F in stairs(L1, L3):
                        for G in stairs(L2, L3):
                            m = sum(min(F[i], G[j]) for i in range(L1) for j in range(h[i]))
                            if m > M: continue
                            D = {(i,j,k) for i in range(L1) for j in range(h[i]) for k in range(min(F[i],G[j]))}
                            yield (h,F,G), D, corners(h)+corners(F)+corners(G)
if __name__ == '__main__':
    M = int(sys.argv[1]); worst = {}
    for key, D, C in gen(M):
        r = analyze(D)
        assert r['t'] <= C - 2, (key, r, C)
        for name, val in [('t-C', r['t']-C), ('tri-C', r['tri']-C), ('q-C', r['q']-C), ('qU-t', r['qU']-r['t']), ('qO-C', r['qO']-C),
                          ('2tri+q-2C', 2*r['tri']+r['q']-2*C), ('qU+tri-t', r['qU']+r['tri']-r['t']), ('2tri+qO-C', 2*r['tri']+r['qO']-C)]:
            if name not in worst or val > worst[name][0]: worst[name] = (val, key, r, C)
    for k, v in worst.items(): print(k, v)
