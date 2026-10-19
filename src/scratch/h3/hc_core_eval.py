"""Independent Python evaluation of MaxCL slack S and HC' at every phase for a core given by unit labels P and its
cells of degree >= 2 (missing residues are spikes).  Cross-check for anneal_h3.c mode 2 (lead, 2026-10-19).
usage: python hc_core_eval.py m P0,P1,... cell cell ...   (cells as exponent strings, e.g. 2000 1100)"""
import sys
m = int(sys.argv[1]); P = list(map(int, sys.argv[2].split(','))); K = len(P)
cells = [tuple(int(ch) for ch in c) for c in sys.argv[3:]]
C = {tuple([0]*K)} | {tuple(int(i == a) for i in range(K)) for a in range(K)} | set(cells)
lab = {x: sum(x[a]*P[a] for a in range(K)) % m for x in C}
assert len(set(lab.values())) == len(C)
def add(x, a): return tuple(x[i]+(i == a) for i in range(K))
A = {x for x in C if all(add(x, a) not in C for a in range(K))}
d = K + m - len(C)
pairs = [x for x in C if sum(x) == 2]; A2 = [z for z in pairs if z in A]; N2 = [z for z in pairs if z not in A]
T = [y for y in C if sum(y) == 3]; p, t = len(N2), len(T)
adeg = [sum(z[a] for z in A2) for a in range(K)]
E = [tuple(int(i == a) for i in range(K)) for a in range(K)]
core = [a for a in range(K) if E[a] not in A]
mnS = mnH = None
for sg in range(m):
    r = {x: (lab[x]-sg) % m for x in C}; r0 = r[tuple([0]*K)]
    S = (d+1)*sum(r[x] for x in C if x not in A) - sum((sum(y)-1)*r[y] for y in A)
    hc = sum((d+1-adeg[a])*r[E[a]] for a in core) + (d+1)*sum(r[z] for z in N2) - 2*sum(r[y] for y in T) - (p+t)*r0
    bm = 0
    for z in A2:
        u = [a for a in range(K) for _ in range(z[a])]
        if r[E[u[0]]]+r[E[u[1]]] < r0: bm += 1
    hc += m*(r0-bm)
    assert S >= hc
    if mnS is None or S < mnS[0]: mnS = (S, sg)
    if mnH is None or hc < mnH[0]: mnH = (hc, sg)
print("m", m, "d", d, "minS", mnS, "minHC'", mnH)
