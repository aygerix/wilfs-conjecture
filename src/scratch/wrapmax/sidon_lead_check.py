"""Lead's independent check of the codex P7 Sidon counterexample to H1' (written without reading codex's code).
Builds the tile from the definition (Sidon offsets a_i = 1 + 254 i + (i^2 mod 127), q, m = 2q, core units P_i = q - a_i,
origin + units + all pairs + one cubic per s in 3A \\ A (lex-least triple) + one spike per missing label) in a sparse
representation, checks down-closure, bijectivity of labels, WRAP-MAX, and evaluates S and Lambda_r at phase rho = 2L
DIRECTLY from the definitions:  S = (d+1)M' - sum_A (d+|y|) r(y),  Lambda_r = sum_{t in N} T(t) r(t),
T(t) = sum_{b : t+e_b not in D} (t_b + 1).  Also the crude MaxCL bound at every phase.
usage: python sidon_lead_check.py [q]"""
import sys
from collections import Counter
k = 127
a = [1+254*i+(i*i) % 127 for i in range(k)]
assert all(a[i] < a[i+1] for i in range(k-1))
L = max(a)
ps = Counter(a[i]+a[j] for i in range(k) for j in range(i, k))
assert max(ps.values()) == 1, "not Sidon"
Q = len(ps)
q = int(sys.argv[1]) if len(sys.argv) > 1 else 3*L+1
assert q >= 3*L+1
m = 2*q; P = [q-x for x in a]; Aset = set(a)
cub = {}
for i in range(k):
    for j in range(i, k):
        for l in range(j, k):
            s = a[i]+a[j]+a[l]
            if s not in Aset and s not in cub: cub[s] = (i, j, l)
t = len(cub)
core = [()]+[(i,) for i in range(k)]+[(i, j) for i in range(k) for j in range(i, k)]+sorted(cub.values())
cs = set(core)
v = {x: sum(P[i] for i in x) for x in core}
lab = Counter(v[x] % m for x in core)
assert max(lab.values()) == 1, "core labels collide"
missing = [j for j in range(1, m) if j not in lab]
nspk = len(missing); d = k+nspk
# down-closure of the core (spikes are units over the origin)
for x in core:
    for idx in range(len(x)):
        assert x[:idx]+x[idx+1:] in cs
def upc(x, i): return tuple(sorted(x+(i,)))
maxcore = [x for x in core if x != () and not any(upc(x, i) in cs for i in range(k))]
Ncore = [x for x in core if x == () or any(upc(x, i) in cs for i in range(k))]
assert all(v[x] < m for x in Ncore), "WRAP-MAX fails"
Vw = [x for x in maxcore if v[x] >= m]
M1 = m*(m-1)//2; rho = 2*L; theta = m-rho
r = lambda val: (val+rho) % m
# S: maximal cells = maximal core cells + all spikes (spike value = its label j)
SA = sum((d+len(y))*r(v[y]) for y in maxcore)+sum((d+1)*r(j) for j in missing)
S = (d+1)*M1-SA
# Lambda_r: non-maximal tops are non-maximal core cells; spike directions: t is a top unless t is the origin
Lam = 0
for x in Ncore:
    cnt = Counter(x)
    T = sum(cnt[i]+1 for i in range(k) if upc(x, i) not in cs)
    if x != (): T += nspk          # spike directions: column {x}, length 1
    Lam += T*r(v[x])
print("k=%d L=%d Q=%d t=|3A\\A|=%d 2L+Q=%d q=%d m=%d d=%d spikes=%d |V|=%d |A|=%d |N|=%d" % (
    k, L, Q, t, 2*L+Q, q, m, d, nspk, len(Vw), len(maxcore)+nspk, len(Ncore)))
print("max_V lam =", max(v[y]-m for y in Vw), "< theta =", theta, ":", max(v[y]-m for y in Vw) < theta)
print("S =", S, " Lambda_r =", Lam, " S-Lambda_r =", S-Lam, " (S-Lambda_r)/m =", (S-Lam)/m, " predicted 2L+Q-t =", 2*L+Q-t)
print("MaxCL at this phase: S >= 0:", S >= 0)
# crude MaxCL at every phase: sum_A (|y|-1) r <= (d+1) sum_N r, with sum_N r >= C(|N|,2) (distinct residues)
lhs_max = 2*sum(range(m-1, m-1-len(Vw), -1))+1*(m-1)*sum(1 for y in maxcore if len(y) == 2)
rhs_min = (d+1)*(len(Ncore)*(len(Ncore)-1)//2)
print("crude all-phase MaxCL: max LHS bound", lhs_max, "<= min RHS bound", rhs_min, ":", lhs_max <= rhs_min)
