"""E10: per-direction excess form of TOP''.
n(u) = graded-lex-min factorization of u in X_q.  For direction a:
   ex_a = sum_{u in X_q} (n_a(u)+1) pi(u) - m(m+1)/2.      TOP'' <=> sum_a ex_a <= m(m-1)/2.
Tests:
  X1 (per direction): ex_a <= sum_{k=1}^{N_a} (k p_a mod m),  N_a = max_u n_a(u)
  X2 (global, set):   sum_a ex_a <= sum_{w in K} (w mod m),   K = {k p_a : 1<=k<=N_a} (as a set)
  X3 (positive part): sum_a max(ex_a,0) <= m(m-1)/2"""
import sys
sys.path.insert(0, 'src')
from ns import all_by_genus
from exp_offsets import shortest_facts

def excess_data(s):
    m, c = s.m, s.c
    Pp, best = shortest_facts(s)
    top = [u for u in s.apery() if u >= c]
    exs, Ns = [], []
    for a, p in enumerate(Pp):
        ex = sum((best[u][a] + 1) * (u - c + 1) for u in top) - m * (m + 1) // 2
        exs.append(ex)
        Ns.append(max((best[u][a] for u in top), default=0))
    return Pp, exs, Ns

if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    cnt = {'X1': 0, 'X2': 0, 'X3': 0, 'TOP': 0}
    ex = {k: [] for k in cnt}
    n = 0
    for g, s in all_by_genus(G):
        if s.m <= 1:
            continue
        n += 1
        m = s.m
        Pp, exs, Ns = excess_data(s)
        C2 = m * (m - 1) // 2
        if sum(exs) > C2:
            cnt['TOP'] += 1
        if any(exs[a] > sum((k * Pp[a]) % m for k in range(1, Ns[a] + 1)) for a in range(len(Pp))):
            cnt['X1'] += 1
            if len(ex['X1']) < 4: ex['X1'].append((s.P, s.c, exs, Ns))
        K = {k * Pp[a] for a in range(len(Pp)) for k in range(1, Ns[a] + 1)}
        if sum(exs) > sum(w % m for w in K):
            cnt['X2'] += 1
            if len(ex['X2']) < 4: ex['X2'].append((s.P, s.c, s.W, exs, sorted(K)))
        if sum(max(x, 0) for x in exs) > C2:
            cnt['X3'] += 1
            if len(ex['X3']) < 4: ex['X3'].append((s.P, s.c, s.W, exs))
    print(f'genus<={G}: {n};', cnt)
    for k, v in ex.items():
        for x in v: print(' ', k, x)
