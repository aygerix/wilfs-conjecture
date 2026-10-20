r"""Adversarial construction (lead, 2026-10-20): B_3-like core U subset [h/2, 2h/3) plus greedily added high elements,
aiming at a REAL depth-four P18 semigroup <m, m+B> with c = 3m + h, 3h <= m.  Reports W, TB4, RED-A residual, SP0.
Greedy: maintain B; repeatedly take the smallest residue r violating the target covering (r in [h,m) not in R3, or
r in [0,h) not in 4A u (3A n [m,m+h) - m)) and add the element x in [h, m) (not breaking the gap h-1 notin 3A,
h-1+m notin 2A) that covers r and the most other missing residues.  usage: b3core a h_factor m_factor seed tries"""
import sys, random, heapq
sys.path.insert(0, '.')
from reda import run as redarun
def b3set(a, seed):
    rnd = random.Random(seed); best = None
    for _ in range(400):
        C = [0]; x = 0
        while len(C) < a:
            x += 1 + (rnd.random() < 0.3)
            cand = C + [x]
            s3 = [p + q + r for i, p in enumerate(cand) for j, q in enumerate(cand[i:]) for r in cand[i + j:]]
            s2 = [p + q for i, p in enumerate(cand) for q in cand[i:]]
            if len(set(s3)) == len(s3) and len(set(s2)) == len(s2): C = cand
        if best is None or C[-1] < best[-1]: best = C
    return best
def sums(A, k):
    S = {0}
    for _ in range(k): S = {s + x for s in S for x in A}
    return S
def missing(m, h, A):
    X2 = sums(A, 2); X3 = sums(A, 3); X4 = sums(A, 4)
    R3 = {s for s in X3 if s < m} | {s - m for s in X2 if m <= s < 2 * m}
    miss = [r for r in range(h, m) if r not in R3] + [r for r in range(h) if r not in X4 and (r + m) not in X3]
    gap_ok = (h - 1) not in X3 and (h - 1 + m) not in X2
    return miss, gap_ok
a, hf, mf, seed, tries = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
C = b3set(a, seed); D = C[-1]
h = max(int(hf * 6 * (D + 1)), 2 * a + 2); off = h // 2 + 1
U = [off + c for c in C]; assert U[-1] < 2 * h / 3 + 1, (U, h)
m = int(mf * h)
print("a", a, "C", C, "h", h, "U", U, "m", m)
rnd = random.Random(seed)
best = None
for t in range(tries):
    B = list(U)
    while True:
        A = [0] + B; miss, ok = missing(m, h, A)
        if not ok: break
        if not miss: break
        r = miss[0] if rnd.random() < 0.7 else rnd.choice(miss)
        X2 = sums(A, 2)
        cands = set()
        for s in X2:
            for target in (r, r + m, r + 2 * m):
                x = target - s
                if h <= x < m and x not in B: cands.add(x)
        for s in sums(A, 1):
            for target in (r + m,):
                pass
        if not cands: break
        scored = []
        for x in rnd.sample(sorted(cands), min(len(cands), 25)):
            A2 = A + [x]; miss2, ok2 = missing(m, h, A2)
            if ok2: scored.append((len(miss2), x))
        if not scored: break
        scored.sort(); B.append(scored[0][1])
    A = [0] + B; miss, ok = missing(m, h, A)
    if miss or not ok: continue
    r = redarun(m, sorted(B))
    if r is None or r["h"] != h: continue
    if best is None or r["reda"] < best["reda"]: best = r
    print("  try", t, "e", r["e"], "W", r["W"], "reda", r["reda"], "SP0", r["SP0"], "comb", r["comb"], "B", r["B"]); sys.stdout.flush()
print("BEST", best)
