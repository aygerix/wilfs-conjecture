# Annealing over RCON (cone class + PROVED Wall + Floor constraints; optional PW = pairwise lattice relaxation)
# maximizing a cls_anneal target (2tri-t, qO-t, qU-t, LHS-5C, LHS-4C, C2m, ...) with |D| in [M0, M1].
# usage: rcon_anneal.py target M0 M1 iters seed [pw]
import sys, random, math
sys.path.insert(0, 'src/scratch')
from cls_anneal import build, stats, target
from corner_anneal import valid, mutate, msize
from lattice_pairwise import feasible
def run(name, M0, M1, iters, seed, pw):
    rnd = random.Random(seed)
    h, F, G, q = [3, 2, 2], [3, 2, 2], [3, 2, 2], [1, 1, 1]
    cur = None; best = (-1e9, None)
    for it in range(iters):
        T = max(0.05, 2.0 * (1 - it / iters))
        nh, nF, nG, nq = mutate(h, F, G, q, rnd)
        if not valid(nh, nF, nG, nq, 'cone'): continue
        m = msize(nh, nF, nG, nq)
        if m > 2 * M1: continue
        D = build(nh, nF, nG, nq); s = stats(D); v = target(s, name)
        pen = 0 if M0 <= m <= M1 else -abs(m - (M0 if m < M0 else M1)) * 0.3
        sc = v + pen
        if cur is None or sc >= cur or rnd.random() < math.exp((sc - cur) / T):
            if pw and not feasible(tuple(nh), tuple(nF), tuple(nG), tuple(nq)): continue
            h, F, G, q, cur = nh, nF, nG, nq, sc
            if pen == 0 and v > best[0]: best = (v, (tuple(h), tuple(F), tuple(G), tuple(q), s))
    return best
if __name__ == '__main__':
    name, M0, M1, iters, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    pw = len(sys.argv) > 6 and sys.argv[6] == 'pw'
    b = run(name, M0, M1, iters, seed, pw)
    print(name, M0, M1, 'seed', seed, 'PW' if pw else 'RCON', 'best', b, flush=True)
