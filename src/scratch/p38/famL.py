# famL: scaling test of CU (Delta3 >= c_U - 3mu) and MU-LO on the ladder family
#   L_k: A = {3} u {3 + 15j : 1 <= j <= k} u {m-8, m-6, m-5}, m = 15k + 17  (CU extremals at e = 6, 7, 8 are k = 1, 2, 3),
# plus nearby variants (ladder step 5mu replaced by s*mu, cluster offsets shifted) to see which shape is extremal.
exec(open('rayU0.py').read().split('rng = random.Random')[0])
def cU_of(m, A):
    from itertools import combinations_with_replacement as cwr
    Ap = [0] + A; best = {}
    for k in range(4):
        for c in cwr(Ap[1:], k):
            s = sum(c); cl = s % m
            if cl not in best or s + k * m < best[cl][0]: best[cl] = (s + k * m, s)
    return max(v[1] for v in best.values()) - m + 1
for step in (15, 12, 18, 21):
    for k in range(1, 9):
        m = step * k + 17 + (step - 15)
        for off in ((8, 6, 5), (7, 5, 4), (9, 7, 6)):
            A = sorted(set([3] + [3 + step * j for j in range(1, k + 1)] + [m - o for o in off]))
            if max(A) >= m or len(A) != k + 4: continue
            r = evalS(m, A)
            if not r: continue
            cu = cU_of(m, A); cur = (cu - 3 * r['mu']) / r['D3']
            print(f"step={step} k={k} off={off} e={r['e']} m={m} res={r['h']>0} D3={r['D3']} cU={cu} CUratio={cur:.3f} MUratio={r['ratio']:.3f} W={r['W']}")
