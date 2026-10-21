# zwid: exact identity e z - m = N_< + N_ns + Ov - |Q'| for the pair map Z x A -> values (Z = classes with sigma < m),
#   N_<  = #{(t,a): sigma_t + a < m},  N_ns = #{(t,a): v = sigma_t + a >= m, v != sigma_{v mod m}},
#   Ov   = sum over large classes s (sigma_s >= m) of (hit(s) - 1)^+,  Q' = large classes with hit(s) = 0.
# ZW <=> Delta3 + N_< + N_ns + Ov >= (r + 1) + |Q'|,  r + 1 = c_U - m.  Tests sub-inequalities on the dumps.
import sys, heapq, collections
from itertools import combinations_with_replacement as cwr
def analyse(m, A):
    d = len(A); e = d + 1; mu = A[0]; best = {}
    for k in range(4):
        for c in cwr(range(d), k):
            s = sum(A[i] for i in c); cl = s % m; key = (k * m + s, -k)
            if cl not in best or key < best[cl]: best[cl] = key
    sg = {cl: best[cl][0] + best[cl][1] * m for cl in best}; hS = {cl: -best[cl][1] for cl in best}
    D3 = 3 * (e - 1) * m - e * sum(hS.values())
    Z = [s for s in range(m) if sg[s] < m]; z = len(Z)
    Nlt = Nns = 0; hit = collections.Counter()
    for t in Z:
        for a in A:
            v = sg[t] + a
            if v < m: Nlt += 1
            elif v != sg[v % m]: Nns += 1
            else: hit[v % m] += 1
    large = [s for s in range(m) if sg[s] >= m]
    Qp = sum(1 for s in large if hit[s] == 0); Ov = sum(hit[s] - 1 for s in large if hit[s] > 1)
    assert e * z - m == Nlt + Nns + Ov - Qp, (m, A)
    cU = max(sg.values()) - m + 1; r1 = cU - m
    Q3 = sum(1 for s in large if hit[s] == 0 and hS[s] == 3)
    return dict(e=e, mu=mu, z=z, D3=D3, Nlt=Nlt, Nns=Nns, Ov=Ov, Qp=Qp, Q3=Q3, r1=r1, cU=cU)
rows = []
for fn in sys.argv[1:]:
    for f in fn.split('+'):
        for L in open(f):
            t = L.split()
            if t[0] != 'DUMP': continue
            r = analyse(int(t[1]), list(map(int, t[15:]))); r['m'] = int(t[1]); r['A'] = list(map(int, t[15:])); rows.append(r)
R = [r for r in rows if r['mu'] <= r['e']]
print(f"{sys.argv[1]}: {len(rows)} S (mu <= e: {len(R)}), e = {rows[0]['e']}; identity asserted")
tests = {
 'S1: N_< >= r+1+|Q\'|': lambda r: r['Nlt'] - r['r1'] - r['Qp'],
 'S2: N_< + Ov >= r+1+|Q\'|': lambda r: r['Nlt'] + r['Ov'] - r['r1'] - r['Qp'],
 'S3: N_< >= r+1': lambda r: r['Nlt'] - r['r1'],
 'S4: Delta3 >= |Q\'|': lambda r: r['D3'] - r['Qp'],
 'S5: N_< + N_ns >= r+1+|Q\'|': lambda r: r['Nlt'] + r['Nns'] - r['r1'] - r['Qp'],
}
for lab, Rs in (('mu<=e', R), ('all', rows)):
    for k, f in tests.items():
        v = min(Rs, key=f)
        print(f"  [{lab}] {k}: fails {sum(1 for r in Rs if f(r) < 0)}, min slack {f(v)} at m={v['m']} A={v['A']} (N<={v['Nlt']} Nns={v['Nns']} Ov={v['Ov']} Q'={v['Qp']} r+1={v['r1']} D3={v['D3']})")
avg = lambda k: sum(r[k] for r in R) / len(R)
print('  means (mu<=e):', {k: round(avg(k), 1) for k in ('Nlt', 'Nns', 'Ov', 'Qp', 'r1', 'D3', 'z')})
