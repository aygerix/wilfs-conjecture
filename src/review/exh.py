# Exhaustive lattice-free cone (and C) sets: L1, L2, L3 <= M (all lengths and values <= M), every q in Cyl, q >= (1,1,1).
# usage: exh.py M nproc [cone|C|both]
import sys, itertools, time
from multiprocessing import Pool
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from indep import analyse, Cone

def seqs(n, top):
    # nonincreasing sequences of length n with first entry exactly top, entries in [1, top]
    def rec(k, mx):
        if k == 0: yield (); return
        for v in range(1, mx + 1):
            for r in rec(k - 1, v): yield (v,) + r
    for r in rec(n - 1, top): yield (top,) + r

def job(args):
    L1, L2, L3, mode, hh = args
    stats = {}; ex = {}; mx = {}; n = 0
    def upd(k, v, w):
        if k not in mx or v > mx[k][0]: mx[k] = (v, w)
    for h in [hh]:
        for F in seqs(L1, L3):
            for G in seqs(L2, L3):
                S = Cone(h, F, G, None)
                qs = []
                if mode in ('C', 'both'): qs.append(None)
                if mode in ('cone', 'both'): qs += sorted(x for x in S.D if min(x) >= 1)
                for q in qs:
                    o, v = analyse(h, F, G, q)
                    n += 1
                    w = (h, F, G, q)
                    for tag in {x[0] for x in v}:
                        stats[tag] = stats.get(tag, 0) + 1
                        if tag not in ex or o['m'] < ex[tag][0]: ex[tag] = (o['m'], w, [x for x in v if x[0] == tag][:2], o)
                    cls = 'C' if q is None else ('coneT' if max(o['Yd']) <= 2 else 'coneX')
                    t = o['t']
                    upd((cls, 'qO-t'), o['qO'] - t, w)
                    upd((cls, 'qO-(t-1+2Y)'), o['qO'] - (t - 1 + 2 * o['Y']), w)
                    upd((cls, 'qO-(2t-1+2Y)'), o['qO'] - (2 * t - 1 + 2 * o['Y']), w)
                    upd((cls, '2tri-t'), 2 * o['tri'] - t, w)
                    upd((cls, 'qU-t'), o['qU'] - t, w)
                    upd((cls, 't-C'), t - o['C'], w)
                    upd((cls, 'C2-3C+6-6m'), o['C'] ** 2 - 3 * o['C'] + 6 - 6 * o['m'], w)
                    upd((cls, 'LHS-6t'), o['LHS'] - 6 * t, w)
                    upd((cls, 'nDS-t-Y'), o['nDS'] - t - o['Y'], w)
                    upd((cls, 'nDS'), o['nDS'], w)
                    upd((cls, 'crossonly-Y'), o['cross_only'] - o['Y'], w)
                    upd((cls, 'rankO'), o['rankO'], w)
                    upd((cls, 'rankU'), o['rankU'], w)
                    upd((cls, 'Sexc'), o['Sexc'], w)
                    upd((cls, 'Scross'), o['Scross'], w)
                    upd((cls, 'maxPhi'), o['maxPhi'], w)
                    upd((cls, 'Y'), o['Y'], w)
    return n, stats, ex, mx

if __name__ == '__main__':
    M, npr, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    t0 = time.time()
    jobs = [(L1, L2, L3, mode, h) for L1 in range(1, M + 1) for L2 in range(1, M + 1) for L3 in range(1, M + 1) for h in seqs(L1, L2)]
    jobs.sort(key=lambda j: -(j[0] * j[1] * j[2]))
    N = 0; S = {}; EX = {}; MX = {}
    with Pool(npr) as p:
        for n, stats, ex, mx in p.imap_unordered(job, jobs):
            N += n
            for k, v in stats.items(): S[k] = S.get(k, 0) + v
            for k, v in ex.items():
                if k not in EX or v[0] < EX[k][0]: EX[k] = v
            for k, v in mx.items():
                if k not in MX or v[0] > MX[k][0]: MX[k] = v
    print(f'M={M} mode={mode}: {N} sets, {time.time() - t0:.0f}s')
    print('violation counts:', S)
    for k, v in sorted(EX.items()): print('  smallest', k, v)
    for k, v in sorted(MX.items()): print('  max', k, v)
