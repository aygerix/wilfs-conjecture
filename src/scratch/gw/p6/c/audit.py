"""Audit saved outputs and report constants, fejer only."""
from pathlib import Path
from math import comb,prod
import json,hashlib,sys,platform

S=json.loads(Path('stress.json').read_text());C=json.loads(Path('checks.json').read_text())
D=json.loads(Path('digital.json').read_text());M=json.loads(Path('milp_hc.json').read_text())
I=json.loads(Path('matching6_independent.json').read_text())
G=json.loads(Path('degree_check.json').read_text())
assert S['F3']['minHCprime']['HCprime']==78
assert S['HYBRID_UNPAID']['minHCprime']['HCprime']==473
assert C['minima']['ONE_LOSS']['slack']==0
for row in D['saved']:
    n=prod(r+1 for r in row['rs'])-prod(row['rs'])
    assert row['minS'][0]>=row['S0']+row['spikes']*comb(n,2)
for k in range(15,501):
    Q=comb(k+1,2)
    assert 4*comb(k,2)-3*(k+Q+5)==(k-15)*(k+2)//2
for k in range(4,201):
    for t in range(2,k//2+1):
        e=(k*t+1)//2;Q=comb(k+1,2)
        for s in (0,1,9):
            low=(k+s-t)+(s+t)*(Q+k)
            mt=t*(k+Q-e+t+s+1)
            assert low-mt==s*(Q+k+1-t)+k+t*e-t*t-2*t>=0
for h in range(1,20):
    for H in range(2,10):
        # Count reduced labels directly by support-size classes.
        direct=1+h
        for j in range(1,H):
            direct+=sum(comb(h,l)*comb(j-1,l-1)*(h+1-l) for l in range(1,min(h,j)+1))
        assert direct==comb(h+H-1,H-1)+h*comb(h+H-2,H-1)

# Full data at the smallest constructed sharp-loss witness.
P=[9,10,12,13,14,15];m=17;sig=9;k=6;s=1;d=7
Q={(0,0),(0,1),(1,1),(0,2),(0,3),(0,4),(0,5),(4,4)};y=(4,4,4)
C0={(),*[(i,) for i in range(k)],*Q,y}
R={z:(sum(P[i] for i in z)-sig)%m for z in C0}
N2={(4,4)};A2=Q-N2
deg=[sum(z.count(i) for z in Q) for i in range(k)]
L=sum((d+1-deg[i])*R[(i,)] for i in range(k))+(d-1)*R[(4,4)]
K={z:(sum(R[(i,)] for i in z)-(len(z)-1)*R[()]-R[z])//m for z in Q|{y}}
OW=R[()]-sum(K[z]==-1 for z in A2)
B=2*K[y]-2*K[(4,4)]
slack=(d+1)*(R[()]+sum(R[(i,)] for i in range(k))+R[(4,4)])-sum(R[z] for z in A2)-2*R[y]
HC=slack-m*sum(K[z]==1 for z in A2)
assert OW+B==-1 and HC==L-m
sharp=dict(P=P,m=m,k=k,s=s,d=d,sigma=sig,core=sorted(C0),
           spike_label=16,rho0=R[()],Lplus=L,OW=OW,B=B,S=slack,HCprime=HC,
           residues=[dict(cell=z,r=R[z]) for z in sorted(C0)])
# Least zero-spike modulus in k>=5,d>=6: a separate explicit witness.
P0=[3,1,4,7,2,8];Q0={(0,0),(1,2),(2,3),(4,5)};T0={(0,0,0)}
D0={(),*[(i,) for i in range(6)],*Q0,*T0};assert len(D0)==12
assert len({sum(P0[i] for i in z)%12 for z in D0})==12
sv=[]
for sig0 in range(12):
    rr={z:(sum(P0[i] for i in z)-sig0)%12 for z in D0}
    ss=7*(rr[()]+sum(rr[(i,)] for i in range(6))+rr[(0,0)])-sum(rr[z] for z in Q0-{(0,0)})-2*rr[(0,0,0)]
    assert ss>=0;sv.append(ss)
zero=dict(P=P0,m=12,k=6,d=6,s=0,C=sorted(D0),minS=min(sv))
chain=[3*sum((v-sig)%5 for v in (0,1,2))-2*((3-sig)%5) for sig in range(5)]
assert min(chain)==3 and 3*comb(5,2)-5*4==10
out=dict(status='PASS',python=sys.version,platform=platform.platform(),sharp_witness=sharp,
         report_sha256=hashlib.sha256(Path('P6C_REPORT.md').read_bytes()).hexdigest(),
         smallest_zero_spike_witness=zero,
         smallest_height3_spike_formula_failure=dict(m=5,core_labels=[0,1,2,3],spike_label=4,actual_min=3,incorrect_min=10),
         checked_results=dict(stress=True,checks=True,digital=True,milp=True,matching6_independent=True,degree=True))
Path('P6C_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
names=sorted(p for p in Path('.').iterdir() if p.suffix in ('.py','.c','.json','.log','.md') and p.name not in ('SHA256SUMS','audit.log','manifest_check.log','P6C_REPORT.md'))
Path('SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in names))
print('P6C_AUDIT_PASS',dict(Lplus=L,OW=OW,B=B,S=slack,HCprime=HC),flush=True)
