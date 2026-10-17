"""E8: localized (flow / Hall) version of TOP''.
cost(u) = pi(u)(ell(u)-1) + 1 for u in X_q;  budget(w) = e*pi(w) - 1 for w in Ap_L = Ap cap [0,c),
pi(x) = ((x - c) mod m) + 1.  Edge u -> w iff w <_S u (u - w in S, w != u).
FLOW holds iff maxflow = sum cost.  (FLOW => TOP'' => Wilf.)"""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from top2 import minlen_apery
from flow import MaxFlow

def flow_test(s):
    m, c, e = s.m, s.c, s.e
    ap = s.apery()
    ml = minlen_apery(s)
    pos = lambda x: ((x - c) % m) + 1
    top = [u for u in ap if u >= c]
    low = [w for w in ap if w < c]
    n = 2 + len(top) + len(low)
    F = MaxFlow(n)
    S_, T_ = 0, 1
    tot = 0
    for i, u in enumerate(top):
        cost = pos(u) * (ml[u] - 1) + 1
        tot += cost
        F.add(S_, 2 + i, cost)
        for k, w in enumerate(low):
            if (u - w) in s:
                F.add(2 + i, 2 + len(top) + k, 10**9)
    for k, w in enumerate(low):
        F.add(2 + len(top) + k, T_, e * pos(w) - 1)
    return F.run(S_, T_) == tot

if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    n = f = 0
    ex = []
    for g, s in all_by_genus(G):
        if s.m == 1:
            continue
        n += 1
        if not flow_test(s):
            f += 1
            if len(ex) < 10:
                ex.append((s.P, s.c, s.q, s.W))
    print(f'genus<={G}: {n} semigroups; FLOW fails {f}')
    for x in ex: print('  fail', x)
