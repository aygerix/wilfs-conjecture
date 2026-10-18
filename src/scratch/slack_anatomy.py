# Where does TOP'' get its slack in residual cases?  Loss terms of the tau-criterion bound:
#   L_pos  = sum_u (m - pi(u)) (d + l(u))       (positions vs pi <= m)
#   L_cross= m*(m + P2 - sum(l+1))              (cross overlap bound vs actual)
import sys, itertools
sys.path.insert(0, 'src'); sys.path.insert(0, 'src/scratch')
from ns import NS
from cl import factorizations_down_set
def anat(gens):
    s = NS.from_generators(gens); m, c = s.m, s.c; d = s.e - 1
    ap = sorted(s.apery()); X = [u for u in ap if c <= u < c + m]
    _, best = factorizations_down_set(s, 'grlex')
    Y = {u: best[u] for u in X}; L = {u: sum(Y[u]) for u in X}; pi = {u: u - c + 1 for u in X}
    P2 = sum(1 for u, v in itertools.combinations(X, 2) if sum(1 for a in range(d) if Y[u][a] != Y[v][a]) == 2)
    lhs = sum(pi[u]*(d + L[u]) for u in X); rhs = m*((d + 1)*m + d - 1)//2
    crude = m*(m + P2 + (d - 1)*len(X))
    Lpos = sum((m - pi[u])*(d + L[u]) for u in X); Lcross = m*(m + P2 - sum(L[u] + 1 for u in X))
    print(gens, f'm={m} tau={len(X)} P2={P2} sum(l+1)={sum(L[u]+1 for u in X)} | rhs={rhs} lhs={lhs} crude={crude} | Lpos={Lpos} Lcross={Lcross} | need {crude-rhs}')
    print('   (pi, l, n):', sorted((pi[u], L[u], Y[u]) for u in X))
for g in ([36, 37, 42, 43], [49, 50, 56, 57], [15, 39, 41, 44], [19, 29, 41, 42], [14, 17, 19, 27], [16, 23, 33, 35]):
    anat(g)
