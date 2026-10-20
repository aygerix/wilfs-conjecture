"""Fixed low-generator perturbations of the P12 interval family. Fejer only."""
import json,sys
from fractions import Fraction as F
from family import formula
from sparse_check import sparse_check

def predicted(k,r):
    assert k>3*r and r>=1
    f=formula(k);m=f['m'];g=[m]+list(range(m+1,m+r+1))+f['gens'][1:]
    ap=set(f['Ap']);ap.difference_update(range(4*m+1,4*m+3*r+1))
    ap.update(m+j for j in range(1,r+1))
    ap.update(2*m+j for j in range(r+1,2*r+1))
    ap.update(3*m+j for j in range(2*r+1,3*r+1))
    L=9*sum(f['gens'][1:])+6*m*(k+1)+m*(4*k+3+6*r)
    return g,ap,f['REST']-r*L,L

if __name__=='__main__':
    out=[]
    cases=[(4,1),(10,1),(40,1),(80,1),(100,1),(200,1),(1000,6),(2000,19)]
    if len(sys.argv)>1:cases=[tuple(map(int,x.split(','))) for x in sys.argv[1:]]
    for k,r in cases:
        g,ap,lb,L=predicted(k,r);s=sparse_check(g);m=5*k+2
        assert ap==set(s['apery_by_residue'])
        assert s['ellp']==4*k+3+6*r
        assert s['M']==21*k+8
        assert s['REST']>=lb
        if k>=100*(r+1):
            assert F(L)<=110*k*k
            assert s['REST']>=k*k*(F(5*k,4)-110*r)
            assert s['Delta']>s['C2']
        small={key:s[key] for key in ('m','e','M','n1','ellp','REST','REST_count','con0','Delta','C2','W')}
        small.update(k=k,r=r,REST_lower_bound=lb)
        print(json.dumps(small),flush=True);out.append(small)
        with open('perturb_cases.json','w') as fp:json.dump(out,fp,indent=2)
        if (k,r)==(100,1):
            with open('counter_M4.json','w') as fp:json.dump(s,fp,indent=2)
