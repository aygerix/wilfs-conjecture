"""P6c first exact stress tests. Run on fejer only (nice, one core)."""
from itertools import combinations_with_replacement as cwr, product
from math import comb
from pathlib import Path
import json

def core_data(C, P, m):
    C=set(C); k=len(P)
    lab={x:sum(P[i] for i in x)%m for x in C}
    assert len(set(lab.values()))==len(C)
    N={x for x in C if any(tuple(sorted(x+(i,))) in C for i in range(k))}
    assert all((i,) in N for i in range(k))
    A=C-N; Q={x for x in C if len(x)==2}; T={x for x in C if len(x)==3}
    A2=Q&A; N2=Q&N; s=m-len(C); d=k+s
    assert s>=0
    a=len(A2); p=len(N2); q=len(Q); t=len(T)
    J=comb(1+k+p,2); B=a+2*t
    cr=(d+1)*J-B*(m-1)+t*(t-1)+a*t+comb(a,2)
    fc=s*comb(k,2)+(d+2)*comb(p,2)-3*t*(m-1)+t*(t-1)
    vals=[]
    for sig in range(m):
        R={x:(v-sig)%m for x,v in lab.items()}; r0=R[()]
        S=(d+1)*sum(R[x] for x in N)-sum((len(x)-1)*R[x] for x in A)
        K={z:(sum(R[(i,)] for i in z)-r0-R[z])//m for z in Q}
        pos=sum(K[z]==1 for z in A2)
        hc=S-m*pos
        adeg=[sum(z.count(i) for z in A2) for i in range(k)]
        ow=r0-sum(K[z]==-1 for z in A2)
        assert ow>=0
        calc=sum((d+1-adeg[i])*R[(i,)] for i in range(k))+(d+1)*sum(R[z] for z in N2)-2*sum(R[y] for y in T)-(p+t)*r0+m*ow
        assert hc==calc
        assert S>=0,dict(P=P,m=m,C=sorted(C),sigma=sig,S=S)
        vals.append(dict(sigma=sig,S=S,HCprime=hc,P_A_plus=pos,OW=ow))
    return dict(k=k,m=m,d=d,q=q,p=p,t=t,s=s,CR=cr,FLAT_CR=fc,
                minS=min(vals,key=lambda x:x['S']),minHCprime=min(vals,key=lambda x:x['HCprime']),phases=vals)

def digital_star(rs):
    bs=[r+1 for r in rs]; m=1; P=[]; groups=[]
    for r,b in zip(rs,bs):
        g=[]
        for a in range(1,b):g.append(len(P));P.append(a*m)
        groups.append(g);m*=b
    C={tuple(i for i in x if i>=0) for x in product(*[[-1,*g] for g in groups])}
    return C,P,m

out={}
C={(),*[(i,) for i in range(4)],*cwr(range(4),2),(0,0,0)}-{(1,2),(3,3)}
out['F3']=core_data(C,[1,4,6,9],16)
out['F3']['P']=[1,4,6,9];out['F3']['C']=sorted(C)
C={(),*[(i,) for i in range(5)],*cwr(range(5),2),(4,4,4),(3,4,4)}
out['HYBRID_UNPAID']=core_data(C,[1,3,8,12,18],31)
out['digital_stars']=[]
for r in range(1,61):
    m=(r+1)**3;k=3*r;q=p=3*r*r;t=r**3
    J=comb(1+k+p,2)
    cr=(k+1)*J-2*t*(m-1)+t*(t-1)
    # Compute top sums at all phases by an independent phase recurrence.
    top={a+(r+1)*b+(r+1)**2*c for a in range(1,r+1) for b in range(1,r+1) for c in range(1,r+1)}
    top0=sum(top);top_sum=top0; mx=top0;mxphase=0
    for sig in range(m):
        if top_sum>mx:mx=top_sum;mxphase=sig
        top_sum+=m*(sig in top)-t
    assert top_sum==top0
    assert mx==top0,(r,mx,top0,mxphase)
    assert top0==r*r*(r+1)*(m-1)//2
    slack=(k+1)*m*(m-1)//2-(k+3)*mx
    assert slack==(r+1)**2*(4*r+1)*(m-1)//2
    out['digital_stars'].append(dict(r=r,k=k,m=m,q=q,p=p,t=t,s=0,CR=cr,minS=slack,maxTopPhase=mxphase))
    if r<=3:
        C,P,mm=digital_star([r]*3)
        chk=core_data(C,P,mm);assert chk['minS']['S']==slack
out['first_digital_CR_failure']=next(x for x in out['digital_stars'] if x['CR']<0)
Path('stress.json').write_text(json.dumps(out,indent=2)+'\n')
for name in ('F3','HYBRID_UNPAID'):
    print(name,json.dumps({k:v for k,v in out[name].items() if k not in ('phases','C')},sort_keys=True),flush=True)
print('DIGITAL_FIRST_CR_FAILURE',json.dumps(out['first_digital_CR_failure'],sort_keys=True),flush=True)
print('DIGITAL_RANGE',len(out['digital_stars']),'ALL_PASS',flush=True)
