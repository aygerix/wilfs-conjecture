"""Annealer against ANCHOR-q (models restricted to TRUE depth: lambda(m-1) >= q, so c(T) = qm - rho;
MODE 0: score = slack - 0.01 DEF; MODE 1: score = slack / (DEF + 1)) (lead, 2026-10-20): minimize slack = rho + EXC + U_top + p - DEF over P18 models
(m, rho, B) at fixed depth q. Score = slack - 0.01*DEF (prefer large deficits at equal slack).
Usage: python anchq_anneal.py Q MMAX ITERS SEED MODE [strip]"""
import math, random, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from anchq import parts

def main():
    Q, MMAX, IT, SEED, MODE = map(int, sys.argv[1:6]); strip = len(sys.argv) > 6
    rnd = random.Random(SEED)
    def rand_state():
        m = rnd.randint(12, MMAX); rho = rnd.randint(0, m // 2)
        hi = m if strip else m - rho
        K = rnd.randint(3, min(12, hi - 2))
        B = sorted(rnd.sample(range(max(1, hi // 3), hi), min(K, hi - max(1, hi // 3))))
        return [m, rho, B]
    def score(st):
        m, rho, B = st
        if not B: return None
        hi = m if strip else m - rho
        if any(b <= 0 or b >= hi for b in B): return None
        r = parts(m, rho, B, Q)
        if not r['true_depth']: return None
        sc = r['slack'] - 0.01 * r['DEF'] if MODE == 0 else r['slack'] / (r['DEF'] + 1.0)
        return sc, r
    cur = rand_state(); sc = score(cur)
    while sc is None: cur = rand_state(); sc = score(cur)
    best = (sc[0], cur, sc[1]); T = 3.0
    for it in range(IT):
        m, rho, B = cur[0], cur[1], list(cur[2])
        mv = rnd.random()
        if mv < 0.3 and len(B) > 2: B.remove(rnd.choice(B))
        elif mv < 0.6:
            hi = m if strip else m - rho
            b = rnd.randint(1, hi - 1)
            if b not in B: B.append(b)
        elif mv < 0.8 and B:
            i = rnd.randrange(len(B)); B[i] += rnd.choice([-2, -1, 1, 2])
        elif mv < 0.9: rho = max(0, rho + rnd.choice([-2, -1, 1, 2]))
        else: m = max(10, min(MMAX, m + rnd.choice([-1, 1])))
        if rho >= m - 1: continue
        B = sorted(set(B))
        nxt = [m, rho, B]
        s2 = score(nxt)
        if s2 is None: continue
        if s2[0] <= sc[0] or rnd.random() < math.exp((sc[0] - s2[0]) / T):
            cur, sc = nxt, s2
            if sc[0] < best[0]:
                best = (sc[0], cur, sc[1]); print("best", round(best[0], 3), cur, sc[1], flush=True)
        T = max(0.05, T * 0.9997)
        if it % 20000 == 19999:
            cur = rand_state(); sc = score(cur)
            while sc is None: cur = rand_state(); sc = score(cur)
            T = 3.0
    print("final", best)

main()
