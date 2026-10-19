# Lead's independent implementation of the a=6 full-AA count certificate (P4_REPORT sec.18),
# written from the lead's own derivation of the necessary conditions.
from math import comb, gcd
from itertools import combinations_with_replacement
def mac(h,j):
    res=0;i=j
    while h>0 and i>0:
        a=i
        while comb(a+1,i)<=h: a+=1
        res+=comb(a+1,i+1); h-=comb(a,i); i-=1
    return res
def Lsp(s):
    if s<=4: return {2:1,3:2,4:4}.get(s,0)
    return 1.5*s if s%3==0 else 1.5*(s-1)
def H(d): return comb(d+3,3)+2*comb(d+1,3)
def sp_bound(d0,r): return H(d0)-Lsp(d0+1)*r
def hp_bound(d0,r,m):
    s=d0+1
    if s%3 or s<6: return -10**9
    k=s//3
    return H(d0)-(1.5*s-3)*r-3*(k-1)*gcd(k,m)
profiles=[]
for q2 in range(0,5):
    for u3 in range(0,mac(q2,2)+1):
        for k in range(0,mac(u3,3)+1):
            L=7*(q2+u3)-4*k
            for t in range(0,9):
                if L+4*t<=34: profiles.append((q2,u3,k,t))
print("profiles",len(profiles))
MULTI=[(),(1,),(2,),(3,),(4,),(5,),(6,),(1,1),(1,2)]
cnt=0; excl=[0,0,0,0]; surv=[]
for (q2,u3,k,t) in profiles:
    q3=21-q2; L=7*(q2+u3)-4*k; budget=34-L-4*t; u4=56-t-u3
    for b in range(0,12):
        d=6+b; B=b*(b+1)//2; Z=comb(b+2,3)
        for ms in MULTI:
            if len(ms)>b: continue
            p=sum(ms); s3=6*b-p
            ellost=sum(21-comb(7-pj,2) for pj in ms)
            pj=list(ms)+[0]*(b-len(ms))
            pairbounds=sorted([max(pj[x],pj[y]) for x in range(b) for y in range(x,b)],reverse=True)
            for l in range(0,min(q2*len(ms),ellost)+1):
                cap2=b*q2-l; cap3=b*q3-ellost+l
                if cap2<0 or cap3<0: continue
                for rAB in range(0,p+1):
                    s4=p-rAB
                    for rBB in range(0,min(B,budget//4)+1):
                        for t4 in range(0,B-rBB+1):
                            t3=B-rBB-t4; qq=rBB+t4
                            Lkeep=sum(pairbounds[qq:])
                            capw=min(6*t3-Lkeep,((b+1)*s3)//2)
                            if capw<0: continue
                            capz=min(mac(t3,2),Z-b) if qq>0 else Z
                            capz=min(capz,((b+2)*t3)//3)
                            if capz<0: continue
                            base=p+b*u3+4*rAB+4*rBB+(2*b*q2+b*q3+7*s3-4*cap2-3*cap3)+(6*t3+(b+1)*s3-3*capw)+((b+2)*t3-3*capz)
                            if base>budget: continue
                            sl=budget-base
                            for dv2 in range(0,min(cap2,sl//4)+1):
                                for dv3 in range(0,min(cap3,(sl-4*dv2)//3)+1):
                                    for dw in range(0,min(capw,(sl-4*dv2-3*dv3)//3)+1):
                                        for dz in range(0,min(capz,(sl-4*dv2-3*dv3-3*dw)//3)+1):
                                            v2=cap2-dv2;v3=cap3-dv3;w=capw-dw;z=capz-dz
                                            cnt+=1
                                            N=q2+q3+s3+s4+t3+t4+u3+u4+v2+v3+w+z+k
                                            m=1+d+N
                                            r=comb(d+2,3)-(u3+u4+v2+v3+w+z)
                                            # E1 pure-A face
                                            if m<sp_bound(6,t): excl[0]+=1; continue
                                            q0=rAB+rBB
                                            if q0==0:
                                                if m<sp_bound(d,r): excl[1]+=1; continue
                                                if m<hp_bound(d,r,m): excl[2]+=1; continue
                                            else:
                                                d0=d-q0
                                                if d0>=1:
                                                    rr=r-(q0*d-comb(q0,2))
                                                    if rr>=0 and m<max(sp_bound(d0,rr),hp_bound(d0,rr,m)): excl[3]+=1; continue
                                            surv.append(dict(q2=q2,u3=u3,k=k,t=t,b=b,bad=ms,l=l,rAB=rAB,rBB=rBB,t4=t4,v2=v2,v3=v3,w=w,z=z,m=m,r=r))
print("vectors",cnt,"excluded",excl,"survivors",len(surv))
for s in surv: print(s)
