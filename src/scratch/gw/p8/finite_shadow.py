"""Exact convex count certificate below the analytic shadow cutoff.

Run on fejer only. This is a certificate for all real e in each displayed
interval, not a sample of labelings or of e. Geometry enters through the
linked missing-pair moment and rectangle packing.
"""
import argparse
import json
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path
from certify import parameters


def minimum(k, v, h, symmetric=False):
    lo = F((v+1)//2)
    if symmetric:
        lo=max(lo,F(1,3)*(F(k*k,2)-F(5*k,4)-v*(v-1)))
        hi=min(F(v*(v+1),2),F(k*v)-F(k*k,2)+F(5*k,4))
        lo=F(ceil(lo))
    else:
        hi = min(F(v*(v+1),2), F(k*v)-F(k*k,2)+F(7*k,8))
    hi = F(floor(hi))
    if hi < lo:
        return None
    D = 2*(h*h*(k+1)-2*h*(3-h))
    linear=F(9,4) if symmetric else F(15,8)
    Z = F(k*k,2)+linear*k+1+h*F(k+1,2)
    a = F(5*v+4,2*v*v)-1/D
    b = -F(v,2)-F(7,2)-F(5,2*v)+2*Z/D
    c = F(v**3,8)+F(v*v,4)+F(7*v,8)+F(3,4)-Z*Z/D
    assert a > 0
    e = min(hi,max(lo,-b/(2*a)))
    value = a*e*e+b*e+c
    return value,e,lo,hi


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--h',default='3')
    ap.add_argument('--start',type=int,default=150)
    ap.add_argument('--end',type=int)
    ap.add_argument('--output',default='results/finite_shadow.json')
    ap.add_argument('--symmetric',action='store_true')
    args=ap.parse_args(); h=F(args.h)
    assert (F(13,6) if args.symmetric else F(72,25))<=h<=3 and args.start>=150
    if args.symmetric:
        assert args.end is not None
        cutoff={F(9,4):3250,F(11,5):6500,F(13,6):162500}.get(h)
        assert cutoff is not None
    else:cutoff=parameters(h)['cutoff']
    end=args.end if args.end is not None else cutoff-1
    failures=[]; byk=[]; states=0; worst=None
    for k in range(args.start,end+1):
        mink=None
        shift=F(5,4) if args.symmetric else F(7,8)
        for v in range(max(1,ceil(F(k,2)-shift)),k+1):
            ans=minimum(k,v,h,args.symmetric)
            if ans is None:continue
            val,e,lo,hi=ans; states+=1
            rec=dict(k=k,v=v,e=str(e),value=str(val),lo=str(lo),hi=str(hi))
            if mink is None or val<F(mink['value']):mink=rec
        assert mink is not None
        byk.append(mink)
        if F(mink['value'])<0:failures.append(mink)
        if worst is None or F(mink['value'])<F(worst['value']):worst=mink
        if k%100==0:print('progress',k,states,len(failures),flush=True)
    closed_from=1+max([args.start-1]+[x['k'] for x in failures])
    out=dict(status='FINITE EXACT CONVEX CERTIFICATE',h=str(h),symmetric_rectangle=args.symmetric,
             range=[args.start,end],analytic_cutoff=cutoff,
             intervals=states,negative_k_count=len(failures),
             closed_from=closed_from,worst=worst,failures=failures,
             minima_by_k=byk)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',json.dumps({k:v for k,v in out.items() if k not in ['minima_by_k','failures']}),flush=True)


if __name__=='__main__':main()
