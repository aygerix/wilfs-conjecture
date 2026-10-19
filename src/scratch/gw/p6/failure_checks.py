"""Preserved false intermediate claims; exact tiny checks on fejer."""
from pathlib import Path
import json
def slack(D,p,m,sig):
    D=set(D);d=len(p)
    def residue(x):return sum(p[a] for a in x)%m
    assert len(D)==m and len({residue(x) for x in D})==m
    assert all(tuple(x[:a]+x[a+1:]) in D for x in D for a in range(len(x)))
    A=[x for x in D if not any(tuple(sorted(x+(a,))) in D for a in range(d))]
    return (d+1)*m*(m-1)//2-sum((d+len(x))*((residue(x)-sig)%m) for x in A)

# pairform_h3.py's stated cubic carry range missed -2.
D=[(),(0,),(0,0),(0,0,0)];m=4;p=[3];sig=2
r=[(len(x)*3-sig)%m for x in D]
kap=(3*r[2]-r[0]-2*r[3])//m
assert r==[2,1,0,3] and kap==-2 and slack(D,p,m,sig)==0
print('PAIRFORM_RANGE',dict(m=m,p=p,sigma=sig,residues=r,kappa=kap,slack=0))

# No choice of the TWO origin lifts necessarily removes all carries.
sig=0;r=[(len(x)*3-sig)%m for x in D];r0=r[0];ru=r[1]
K0=[((1-len(x))*r0+len(x)*ru-r[i])//m for i,x in enumerate(D)]
K1=[K0[i]+len(x)-1 for i,x in enumerate(D)]
assert K0==[0,0,1,2] and K1==[-1,0,2,4]
print('TWO_BASES_NOT_ENOUGH',dict(m=m,p=p,sigma=sig,K0=K0,K1=K1,slack=slack(D,p,m,sig)))

# Intersections of cubic divisor sets do not by themselves certify all faces.
m=6;p=[1,5];base=[(),(0,),(1,),(0,0),(1,1)]
Ds=[base+[(0,0,0)],base+[(1,1,1)]]
vals=[[slack(D,p,m,s) for s in range(m)] for D in Ds]
fake=(2+1)*m*(m-1)//2-4*((2-5)%6)-4*((4-5)%6)-5*((3-5)%6)
assert fake==-7 and [v[5] for v in vals]==[5,13] and [min(v) for v in vals]==[5,4]
print('FORCED_ONLY_FALSE',dict(m=m,p=p,sigma=5,forced_bound=fake,actual_slacks=[v[5] for v in vals],actual_phase_minima=[min(v) for v in vals]))

named=json.loads(Path('charging_named.json').read_text())
z=next(z for z in named if z['name']=='E47');a=z['phaseparts'][0]
assert (a['r0'],a['Lplus'],a['Br0'],a['slack'])==(0,104,-1,90)
assert z['UL3']
print('E47_ESSENTIAL_LINEAR_SLACK',a)
center=next(z for z in named if z['name']=='centered_worst')['phaseparts'][2]
assert (center['r0'],center['Lplus'],center['Br0'],center['Br1'],center['slack'])==(12,36,-10,0,64)
print('CENTERED_EXACT_PAYMENT',center)
print('FAILURE_CHECKS_PASS')
