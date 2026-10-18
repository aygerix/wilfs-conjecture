# L-shapes: class deficits E_tau(s) = #{x in X_tau: rho_x < e_tau} - |X_tau| e_tau/m ; which partial sums are >= 0 ?
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0,'/Users/jmercedes/Desktop/Projects/Research/wilfs-conjecture/src')
from exp_cl_tiling import downsets
M=int(sys.argv[1]); d=2
stats={}
for m in range(4,M+1):
    for D in downsets(m,d):
        Dl=sorted(D); S=set(Dl)
        if any(all(n[a]==0 for n in Dl) for a in range(d)): continue
        A=max(x[0] for x in Dl)+1; B=max(x[1] for x in Dl)+1
        if len(Dl)==A*B: continue   # boxes
        # L-shape params
        bp=min(y for y in range(B) if (A-1,y) not in S)   # rows y<bp have length A
        ap=max(x for x in range(A) if (x,bp) in S)+1
        Q=[x for x in Dl if x[0]<ap and x[1]<bp]; R1=[x for x in Dl if x[0]>=ap]; R2=[x for x in Dl if x[1]>=bp]
        taus={'Q':(A-1,B-1),'R1':(A-1,bp-1),'R2':(ap-1,B-1)}; cls={'Q':Q,'R1':R1,'R2':R2}
        for p in itertools.product(range(1,m),repeat=d):
            res={x:sum(i*j for i,j in zip(x,p))%m for x in Dl}
            if len(set(res.values()))!=m: continue
            for s in range(m):
                E={}
                for k in cls:
                    e=(sum(i*j for i,j in zip(taus[k],p))-s)%m
                    E[k]=Fr(sum(1 for x in cls[k] if (s-res[x])%m<e))-Fr(len(cls[k])*e,m)
                for name,val in [('Q',E['Q']),('R1',E['R1']),('R2',E['R2']),('Q+R1',E['Q']+E['R1']),('Q+R2',E['Q']+E['R2']),('R1+R2',E['R1']+E['R2']),('all',E['Q']+E['R1']+E['R2'])]:
                    st=stats.setdefault(name,[0,0,Fr(0)])
                    st[0]+=1; st[1]+= (val<0); st[2]=min(st[2],val)
    print('m',m,{k:(v[1],str(v[2])) for k,v in stats.items()},flush=True)
