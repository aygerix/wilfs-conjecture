import sys; sys.path.insert(0,'.')
from shapes import parts_in, extend, cells
from tk import classify, counts, face_corners, H_of
from collections import Counter
def allpp(n):
    big=(n,)*n
    for k0 in range(1,n+1):
        for lam0 in parts_in(big,k0):
            yield from extend([lam0], n-k0)
N=int(sys.argv[1]); st=Counter(); worst=Counter()
for n in range(1,N+1):
    for L in allpp(n):
        D=cells(L); kind,q,full=classify(D)
        st[kind]+=1
        if kind=='other': continue
        t,Tri,qU,qO=counts(D); C=sum(face_corners(D,c) for c in range(3)); m=n
        d=H_of(D)-(m-1)
        assert d>=m+1-(2*t+2*Tri+qU+qO)
        assert C*C-3*C+6<=6*m
        if kind=='C':
            assert t<=C-2,(D,'T'); assert 2*Tri<=t-1,(D,'TF'); assert qU<=t-1,(D,'F'); assert qO<=t-1,(D,'QF')
            worst['C:t-C']=max(worst['C:t-C'],t-C); worst['C:2Tri-t']=max(worst['C:2Tri-t'],2*Tri-t)
            worst['C:qU-t']=max(worst['C:qU-t'],qU-t); worst['C:qO-t']=max(worst['C:qO-t'],qO-t)
        else:
            assert t<=C,(D,"T'")
print('all down-sets |D|<=',N,dict(st)); print('max over C:',dict(worst))
