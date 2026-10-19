"""Finite exact small-k certificate for pair-disjoint squarefree cubics.

For fixed k,t,v the missing-pair count e is optimized over an entire real
interval. The spike minimum from rectangle packing has one linear break.
All executions belong on fejer.
"""
import argparse,json
from fractions import Fraction as F
from math import comb
from pathlib import Path


def quadratic_min(a,b,c,lo,hi):
    if lo>hi:return None
    assert a>0
    e=min(hi,max(lo,-b/(2*a)))
    return a*e*e+b*e+c,e


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--start',type=int,default=5)
    ap.add_argument('--end',type=int,default=191)
    ap.add_argument('--output',default='results/small_disjoint.json')
    ap.add_argument('--symmetric',action='store_true')
    args=ap.parse_args();states=0;fail=[];worst=None;per=[]
    for k in range(args.start,args.end+1):
        C=comb(k,2);M0=comb(k+2,2);Q=comb(k+1,2)
        tmax=(k*k+6*k+4)//(9*k+7)
        # Larger t are paid directly, even with e=A=0.
        for t in range(2,min(C//3,tmax)+1):
            p=3*t;cp=comb(p,2);Gs=C+cp-t
            assert Gs>0
            C0=(k+1)*cp-t*(M0+t)
            for v in range(k+1):
                lo=F((v+1)//2);hi=F(min(v*(v+1)//2,Q-p))
                if lo>hi:continue
                if v==0:
                    e=F(0);sp=max(0,C-t)
                    val=F(C0+sp*Gs)
                else:
                    aa=F(5*v+4,2*v*v)
                    bb=-F(v,2)-F(7,2)-F(5,2*v)+t
                    cc=F(v**3,8)+F(v*v,4)+F(7*v,8)+F(3,4)+C0
                    ans=[]
                    lines=[(0,0),(1,C-k*v-t)]
                    if args.symmetric:lines.append((-3,C-v*(v-1)-t))
                    for slope,offset in lines:
                        llo,hhi=lo,hi
                        for os,ob in lines:
                            ds=slope-os;rhs=ob-offset
                            if ds>0:llo=max(llo,F(rhs,ds))
                            elif ds<0:hhi=min(hhi,F(rhs,ds))
                            elif rhs>0:llo,hhi=F(1),F(0)
                        qmin=quadratic_min(aa,bb+Gs*slope,cc+Gs*offset,llo,hhi)
                        if qmin is not None:ans.append(qmin)
                    val,e=min(ans)
                states+=1
                rec=dict(k=k,t=t,v=v,e=str(e),value=str(val))
                if val<0:fail.append(rec)
                if worst is None or val<F(worst['value']):worst=rec
        per.append(dict(k=k,states=states,failures=len(fail)))
        if k%20==0:print('progress',k,states,len(fail),flush=True)
    out=dict(status='FINITE EXACT CONVEX CERTIFICATE',range=[args.start,args.end],
             symmetric_rectangle=args.symmetric,
             intervals=states,negative_intervals=len(fail),failures=fail,
             minimum=worst,progress=per)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',json.dumps({k:v for k,v in out.items() if k not in ['failures','progress']}),flush=True)


if __name__=='__main__':main()
