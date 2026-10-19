# Candidate PCI counterexample at i=12, q=20: base = e1+e2+e3 (weights 39), column direction weight 46, J=7.
import itertools
i,q=12,20
def F(t): return min(i,t//q)
u,w,J,beta=117,46,7,3
M=u+J*w
L=sum(F(u+j*w) for j in range(1,J+1)); R=J*beta+sum(F(M-u-j*w) for j in range(0,J+1))
print('PCI column: M=%d T=%d L=%d R=%d  fails=%s'%(M,(2*i-2)*q-1,L,R,L>R))
# the actual down-set: box [0,1]^3 x [0,7], weights (39,39,39,46); P_12 at scale q
n=(39,39,39,46); d=4
cells=[x for x in itertools.product(range(2),range(2),range(2),range(8))]
v=[sum(a*b for a,b in zip(x,n)) for x in cells]; MM=max(v)
lhs=sum(F(t) for t in v); rhs=d*sum(F(MM-t) for t in v)
print('down-set box: |D|=%d M=%d  P_12: lhs=%d  d*rhs=%d  holds=%s'%(len(cells),MM,lhs,rhs,lhs<=rhs))
# per-column budget with d replaced by 1 (pure dominant-column decomposition test)
print('with d=1 (no slack from multiplicity):', lhs, sum(F(MM-t) for t in v))
