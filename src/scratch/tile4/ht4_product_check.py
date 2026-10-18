#!/usr/bin/python3
"""Exact finite part of the HT4 theorem for 2+2 Cartesian products."""
import sys
sys.dont_write_bytecode=True
import json
import socket
from fractions import Fraction as F
from pathlib import Path
from ht4_tasks import reference


def partitions(n,cap=None):
    if not n:
        yield ();return
    for a in range(min(n,n if cap is None else cap),0,-1):
        for tail in partitions(n-a,a):yield (a,)+tail


def planar(shape):
    D={(x,y) for y,L in enumerate(shape) for x in range(L)}
    ht={x:max(sum(y)-sum(x) for y in D if all(a<=b for a,b in zip(x,y))) for x in D}
    H=0
    for x in D:
        for a in range(2):
            top=x
            while top[:a]+(top[a]+1,)+top[a+1:] in D:top=top[:a]+(top[a]+1,)+top[a+1:]
            H+=ht[top]
    return D,H,sum(ht.values())


def main():
    assert socket.gethostname().split('.')[0]=='fejer'
    M=38
    ideals={n:[(p,*planar(p)) for p in partitions(n) if p[0]>=2 and len(p)>=2] for n in range(3,13)}
    count=0;worst=None;minimum=None
    for n in range(3,13):
        for s in range(3,13):
            m=n*s
            if m>=M:continue
            for a,A,Ha,Sa in ideals[n]:
                for b,B,Hb,Sb in ideals[s]:
                    H=s*Ha+n*Hb+2*s*Sa+2*n*Sb
                    D={x+y for x in A for y in B}
                    assert reference(D)[0]==H
                    slack=2*(m+1)*H-3*m*(m-1)
                    assert slack>=0,(a,b,H,m)
                    ratio=F((m+1)*H,3*m*(m-1)//2)
                    if minimum is None or ratio<minimum:
                        minimum=ratio;worst=dict(m=m,n=n,s=s,shape_A=a,shape_B=b,H=H)
                    count+=1
    result=dict(status='PASS',execution_host=socket.gethostname(),
                analytic_threshold=M,checked_ordered_pairs=count,
                exact_HT4_min_ratio=str(minimum),worst=worst,
                coverage='All planar order ideals A,B containing both unit vectors, |A|>=3, |B|>=3, |A||B|<38. Integer partitions encode all planar down-sets. Sizes of either factor are at most 12.')
    here=Path(__file__).resolve().parent
    (here/'ht4_product_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
