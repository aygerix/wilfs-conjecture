"""Independent endpoint replay of complete C profile hull lists; fejer only.
argv log_path a. Hulls enlarge the C survivor set, so zero is an exclusion.
Uses cover composition, E-DELTA and linked global/interval packing.
"""
from pathlib import Path
import re,json,sys
env={}
exec(Path('frontier_counts.py').read_text().split('amin=')[0],env)
C,H,L2,cd,mac,cover,sp2,excover=(env[x] for x in ('C','H','L2','cd','mac','cover','sp2','exception_cover'))
path=Path(sys.argv[1]);aa=int(sys.argv[2]);out=[];count=0
for line in path.read_text().splitlines():
 if not line.startswith('PROFILE '):continue
 z={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
 if z['a']!=aa:continue
 count+=1
 a,al,r,n0,l,t,u0,u1,c0,beta,R,b,dl,du=(z[x] for x in ('a','alpha','r','n0','l','t','u0','u1','c0','beta','R','b','first','last'))
 p=a-al;QA=C(al+1,2);UA=C(al+2,3);Q=C(a+1,2);U=C(a+2,3);q=Q-r;q2=n0+l;u=u0+u1
 k0=min(mac(u0,3),(al+3)*u0//4);k1=(al+2)*u1//3;K=k0+k1
 assert K==z['k'];WA=-C(a+1,3)+(a+1)*(q2+u)-4*K-(a-3)*r+4*t
 assert WA==z['WA'];tf=U-mac(q);ep=t-tf;assert ep==z['eps']
 D3=3*t-(a+2)*r;t0=UA-c0;rll=QA-n0;E=min(p,l+r);hot=0
 assert q+q2+2>=2*(al+E)
 if beta:
  hot=max(0,C(p-E+2,3)-t+t0,min(C(p-j+2,3)-(p-j)*max(0,r-rll-max(0,j-l))-ep for j in range(E+1)))
 budget=-WA-hot-b*(u+max(0,min(2*r,2*a-r)))-1
 mmax=-1
 for cc in range(max(0,budget//(q+q2+u+2)+1)):
  left=budget-cc*(cc+1+q+q2+u)
  if left<0:break
  ee=left//(3*a+2*b+cc+q+q2+u)
  mmax=max(mmax,C(a+b+3,3)-r*(1+b)-t+K+cc*(a+b+1)+ee)
 zt=t-a*r+C(r,2);cv=min(a,cover(r,zt-max(0,t0-al*rll)));er=C(r+1,2)
 kept=[]
 for kk in range(1 if r else 0,cv+1):
  ek=min(ep,zt-C(kk,2))
  if ek<0:continue
  ex=excover(a,al,r,rll,l,kk)
  if ex<0:continue
  CH=al+n0+c0+l+ex+C(ex+2,3)+(n0+al*ex)*p
  BH=a-1+q2+u-2*(al+ex+l+min(n0,u0+t0))
  upper=min(du,mmax-2,2*CH-(a-1)-(a+3)*q2-(a+1)*u+5*K-D3-b*BH-1)
  if upper<dl:continue
  ng=a+1-kk
  ml=max(cd(sp2(ng,ek),2),H(a+1)-4*er-9*((a+1)*er+(r+1)*ek+C(ek,2)))
  if ml>mmax:continue
  ns=max(0,R-l-r-kk);nw=max(0,R-kk);nj=max(0,al+R-kk)
  if sp2(ns,ek)>2*(3*((upper+1)//2)-2):continue
  if sp2(nw,ek)>2*(3*upper-2):continue
  if sp2(nj,ek)>2*(3*((3*upper+1)//2)-2):continue
  N=al+R
  if H(N)-4*er-9*(N*er+(r+1)*ek+C(ek,2))>3*((3*upper+1)//2)-2:continue
  kept.append(dict(k=kk,e=ek,E=ex,delta=[dl,upper],m_upper=mmax))
 if kept:out.append(dict(profile=z,possible=kept))
result=dict(source=str(path),a=aa,profile_hulls=count,surviving_hulls=len(out),survivors=out)
Path(f'replay{aa}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
