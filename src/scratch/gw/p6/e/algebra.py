"""Reproducible exact algebra and local-case audits; fejer only."""
import json,sys
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement as cwr
from math import comb
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'d'))
from core import evaluate
from payments import few_cutoff,few_cutoff_linked


def local_bad():
    counts={};n=0
    for m in range(2,37):
        for rho in range(m):
            for U in cwr(range(m),3):
                faces=[(U[j]+U[(j+1)%3]-rho)//m for j in range(3)]
                ell=sum(U)-2*rho;K=ell//m;r=ell%m;v=int(r>=m-rho)
                b=2*K-sum(faces)+v;n+=1
                assert b>=-1
                if b==-1:
                    code=(K,v,tuple(sorted(faces)))
                    assert code in [(1,0,(1,1,1)),(-1,1,(0,0,0))],(m,rho,U,code)
                    counts[str(code)]=counts.get(str(code),0)+1
    return dict(cases=n,bad=counts)


def principal(m,U,Q,T):
    V=[0,*U,*[sum(U[i] for i in z)%m for z in Q],*[sum(U[i] for i in y)%m for y in T]]
    return len(V)==len(set(V)) and len(V)<=m


def failures():
    # Each search is exhaustive in m below the first witness, in the stated
    # forced shape. Optional extra cells cannot repair a forced collision.
    out={}
    out['deep_unit_one']=dict(m=4,rho=2,U=[1],Q=[(0,0)],T=[(0,0,0)])
    for m in range(4,25):
        if 'six_forces_binary_quartet' not in out:
            Q={(0,0),(1,1),(2,2),(0,1),(0,2)}
            T={(1,1,1),(2,2,2),(0,0,1),(0,1,1),(0,0,2),(0,2,2)}
            for b,c in combinations(range(m//2+1,m),2):
                for a in range(m//2+1,m):
                    if a in (b,c):continue
                    U=[a,b,c]
                    if all(sum(U[i] for i in y)<2*m for y in T) and principal(m,U,Q,T):
                        out['six_forces_binary_quartet']=dict(m=m,U=U,Q=sorted(Q),T=sorted(T))
                        break
                if 'six_forces_binary_quartet' in out:break
        if 'all_zero_extensions_gain' not in out:
            for rho in range(1,m):
                for u in range(1,m):
                    U=[0,u];Q={(0,1),(1,1)};T={(0,1,1),(1,1,1)}
                    vals=[rho,*U,*[(sum(U[i] for i in z)-rho)%m for z in Q],
                          *[(sum(U[i] for i in y)-2*rho)%m for y in T]]
                    if len(vals)!=len(set(vals)):continue
                    pp=(2*u-rho)//m;rr=(2*u-rho)%m
                    kk=(3*u-2*rho)//m;rt=(3*u-2*rho)%m
                    if pp==1 and rr<rho and kk==1 and rt<m-rho:
                        out['all_zero_extensions_gain']=dict(m=m,rho=rho,U=U,Q=sorted(Q),T=sorted(T))
                        break
                if 'all_zero_extensions_gain' in out:break
        for a,b in combinations(range(m//2+1,m),2):
            U=[a,b];Q=set(cwr(range(2),2));T=set(cwr(range(2),3))
            if 3*b<2*m and principal(m,U,Q,T) and 'beta_le_pplus' not in out:
                out['beta_le_pplus']=dict(m=m,U=U,Q=sorted(Q),T=sorted(T),beta=4,Pplus=3)
        for h in range(m//2+1,m):
            for a,b in combinations(range(1,m//2+1),2):
                U=[h,a,b];Q={(0,0),(0,1),(0,2)};T={(0,0,1),(0,0,2)}
                if h+a>m and h+b>m and 2*h+b<2*m and principal(m,U,Q,T) and 'delete_low_injective' not in out:
                    out['delete_low_injective']=dict(m=m,U=U,Q=sorted(Q),T=sorted(T))
        for a,b in combinations(range(m//2+1,m),2):
            for l in range(1,m//2+1):
                U=[a,b,l];Q={(0,0),(0,1),(1,1),(0,2),(1,2)}
                T={(0,0,2),(0,1,2),(1,1,2)}
                if a+l>m and 2*b+l<2*m and principal(m,U,Q,T):
                    if 'low_link_pseudoforest' not in out:
                        out['low_link_pseudoforest']=dict(m=m,U=U,Q=sorted(Q),T=sorted(T))
                    if 2*l<m and 'low_link_strict' not in out:
                        out['low_link_strict']=dict(m=m,U=U,Q=sorted(Q),T=sorted(T))
        if len(out)==7:break
    return out


def algebra():
    # Optimal-threshold lower bounds for the localized defect mass.
    for v in range(2,501):
        E=F(v*(v+1),6)
        fv=2*E*E/(v+1)-E
        target=F(v*(v+1)*(v-3),18)
        assert fv==target
        q=F(v*(v+1),3)
        dm=q*(q-1)/(2*v)
        assert dm-target==F((v+1)*(4*v-3),18)
    for v in range(1,81):
        N=4*v**4-16*v*v-12*v-1
        R=F(N,8*(5*v+4))
        assert R-F(v*(v+1)*(v-3),10)==F(48*v**3+24*v*v-24*v-10,80*(5*v+4))
        for e in range((v+1)//2,comb(v+1,2)+1):
            q=comb(v+1,2)-e;X=2*e-v
            bound=F(q*(q-1),2*v)+F(v+1,v)*(F(X*X,2*v)-F(X,2))
            square=F(5*v+4,2*v*v)*(F(e)-F(v*(v*v+7*v+5),2*(5*v+4)))**2
            assert bound==R+square
    assert F(19,2880)-F(51,8000)==F(1,4500)
    # The two clean polynomial margins in the k>=80t proof.
    # k=160+x: k^2/100 -123k/80 -1 =9+133x/80+x^2/100.
    for x in range(501):
        k=160+x
        assert F(k*k,100)-F(123*k,80)-1==9+F(133*x,80)+F(x*x,100)
        assert (k*k-1)*(k-7)*20>=19*k**3
    # Coefficient identities for the stronger all-t cutoff 72t+10.
    for t in range(2,401):
        for x in range(26):
            n=36*t+5+x
            f=n**3-(36*t+2)*n*n-(90*t+3)*n-54*t-36*t*t
            poly=(612*t*t+468*t+60+(1296*t*t+486*t+52)*x
                  +(72*t+13)*x*x+x**3)
            assert f==poly and poly>0
            k=72*t+10+x
            D=comb(k,2)-2*k*t-2*t*t-2*t
            assert 2*D==2*(2446*t*t+662*t+45)+(140*t+19)*x+x*x
        k=72*t+9;n=36*t+4
        f=n**3-(36*t+2)*n*n-(90*t+3)*n-54*t-36*t*t
        assert f==-684*t*t+54*t+20 and f<0
        assert few_cutoff(k,t)['closes'] is False
        assert few_cutoff(k+1,t)['closes'] is True
    for t in range(2,401):
        for x in range(26):
            n=20*t+4+x
            G=4*n**4-80*t*n**3-(264*t+16)*n*n-(80*t*t+280*t+12)*n-64*t*t-96*t-1
            P=(20800*t**3+22176*t*t+7120*t+719
               +(32000*t**3+27760*t*t+8488*t+884)*x
               +(4800*t*t+2616*t+368)*x*x+(240*t+64)*x**3+4*x**4)
            assert G==P and P>0
            k=40*t+8+x
            D=comb(k,2)-2*k*t-2*t*t-2*t
            assert 2*D==2*(718*t*t+282*t+28)+(76*t+15)*x+x*x
        k=40*t+7;n=20*t+3
        G=4*n**4-80*t*n**3-(264*t+16)*n*n-(80*t*t+280*t+12)*n-64*t*t-96*t-1
        assert G==-11200*t**3-784*t*t+1008*t+143 and G<0
        assert not few_cutoff_linked(k,t)['closes']
        assert few_cutoff_linked(k+1,t)['closes']
    table=[]
    linked_table=[]
    for t in range(2,21):
        last_fail=max(k for k in range(3,80*t+1) if not (few_cutoff(k,t) or {}).get('closes',False))
        table.append(dict(t=t,all_k_at_least=last_fail+1,checked_through=80*t))
        last_fail=max(k for k in range(3,40*t+9) if not (few_cutoff_linked(k,t) or {}).get('closes',False))
        linked_table.append(dict(t=t,all_k_at_least=last_fail+1,checked_through=40*t+8))
    lows=[]
    for l in range(1,13):
        C0=l+comb(l+1,2)+comb(l+2,3)
        D=2*l*l+4*l-3
        bound=F(2,l+2)*(C0+F(D*D,48))
        form=F(l**3,6)+F(2*l*l,3)+F(5*l,6)+1-F(13,8*(l+2))
        assert bound==form
        J=max(range(D//6+3),key=lambda j:D*j-3*j*j)
        exact=F(4*C0+D*J-3*J*J,2*(l+2))
        lows.append(dict(l=l,real_bound=str(bound),H=(bound.numerator+bound.denominator-1)//bound.denominator,
                         integer_j_bound=str(exact),j=J))
    return dict(few_table=table,linked_few_table=linked_table,small_lows=lows)


if __name__=='__main__':
    out=dict(algebra=algebra(),local=local_bad(),failures=failures())
    out['failure_evaluations']={}
    for name,data in out['failures'].items():
        a=evaluate(data['m'],data['U'],data['Q'],data['T'],data.get('rho',0))
        assert a['S']>=0 and a['HC']>=0
        out['failure_evaluations'][name]=a
    print(json.dumps(out,indent=2),flush=True)
