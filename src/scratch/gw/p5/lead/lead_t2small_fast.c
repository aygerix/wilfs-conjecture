/* Lead's C port of lead_t2small.py (independent re-implementation of codex's T2-SMALL / T2-SMALL16 certificate,
   P5_REPORT sections 39, 43, 44, 47, written from the report text only), with optional extra tests:
     MIX  : MIX-GAP completion (section 38)
     LINK : actual minimum cover k of the absent A-pair graph (PAIR-COVER / LINKED-DEF, section 43):
            zeta_A=t-a*r+C(r,2), v_lower=max(0,t0-alpha*r_LL), z=zeta_A-v_lower (z<0 impossible),
            k=0 if r=0, else 1<=k<=min(a,gamma(r,z)); e_k=min(eps,zeta_A-C(k,2)).
            Global: max(LINK-SP, LINK-Q, LINK-PSP) <= m_up.  Intervals (same k): joint n=alpha+R-k on ceil(3delta/2),
            wide n=R-k on delta, short n=R-l-r-k on ceil(delta/2), each by max(SP, Q) with defect e_k.
     PACK : MIX-PACK (section 44).
     E    : E-REPAIR (section 50): fix the minimum cover k first, E_k=min(p,l+min(r-r_LL,r-k+1)) in C_H, B_H, H_cold.
     H    : LOCAL-COVER (section 50): r<=ak-C(k,2); j low cover vertices with r_LL<=f(j); E replaced by Ehat_k.
     G    : early GLOC cap on t per state (necessary condition, P5 section 24; used when Bc>=0 and q>=2alpha).
   usage: lead_t2small amin amax flags [alphamin alphamax]   (flags: any of M, L, P, E, H, G) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef long long ll;
static ll C2(ll n){ return n>=2? n*(n-1)/2:0; }
static ll Cn(ll n,int k){ if(n<k||n<0) return 0; ll r=1; for(int i=0;i<k;i++) r=r*(n-i)/(i+1); return r; }
static ll mac2_slow(ll x){ if(x<=0) return 0; ll k2=2; while(Cn(k2+1,2)<=x) k2++; ll k1=x-Cn(k2,2); return Cn(k2+1,3)+Cn(k1+1,2); }
/* speed-up (2026-10-19): table of mac2 for 0<=x<MAC2N, built incrementally and checked against mac2_slow */
#define MAC2N 4000000
static ll *MAC2T=0;
static void mac2_init(void){ MAC2T=malloc(sizeof(ll)*MAC2N); ll k2=2; MAC2T[0]=0;
  for(ll x=1;x<MAC2N;x++){ while(Cn(k2+1,2)<=x) k2++; MAC2T[x]=Cn(k2+1,3)+Cn(x-Cn(k2,2)+1,2); }
  for(ll x=0;x<MAC2N;x+=(x<100000?1:997)) if(MAC2T[x]!=mac2_slow(x)){ fprintf(stderr,"mac2 table mismatch at %lld\n",x); exit(3); } }
static inline ll mac2(ll x){ if(x<=0) return 0; if(x<MAC2N) return MAC2T[x]; return mac2_slow(x); }
static ll mac3(ll x){ if(x<=0) return 0; ll k3=3; while(Cn(k3+1,3)<=x) k3++; ll rem=x-Cn(k3,3), v=Cn(k3+1,4);
  if(rem>0){ ll k2=2; while(Cn(k2+1,2)<=rem) k2++; ll k1=rem-Cn(k2,2); v+=Cn(k2+1,3)+Cn(k1+1,2); } return v; }
static ll lam2(ll n){ if(n<=1) return 0; if(n==2) return 2; if(n==3) return 4; if(n==4) return 8; return (n%3==0)?3*n:3*(n-1); }
static ll Hn(ll n){ return n*(C2(n)+1); }
static ll psp(ll n,ll r,ll e){ ll er=Cn(r+1,2); return Hn(n)-4*er-9*(n*er+(r+1)*e+C2(e)); }
static ll ceil2(ll x){ return x>=0? (x+1)/2 : -((-x)/2); }   /* ceil(x/2) */
/* lower bound on (capacity) from n pair-injective points with legal defect e: max of SP and Q forms */
static ll packlow(ll n,ll e){ ll sp=ceil2(2*Hn(n)-lam2(n)*e); ll q=Hn(n)-9*Cn(e+1,2); return sp>q?sp:q; }
static int okSP(ll cap,ll n,ll e){ return 2*cap>=2*Hn(n)-lam2(n)*e; }
static ll gcover(ll r,ll z,ll d){ if(r==0) return 0; if(z<0) return -1; ll g=(ll)floor((1+sqrt(1.0+8.0*z))/2+1e-9);
  while(Cn(g+1,2)<=z) g++; while(g>0&&Cn(g,2)>z) g--; if(g>r) g=r;
  ll D0=1+((C2(r)-z)>0? (C2(r)-z+r-1)/r : -((z-C2(r))/r)); if(D0>=3){ ll g2=1+z/(D0-2); if(g2<g) g=g2; } if(g>d) g=d; return g; }
static ll Gamma_raw(ll a,ll d0,ll q,ll r){ ll hi=Cn(d0+1,2)-r-1, best=-1; int f=0; for(ll x=q;x<=hi;x++){ ll v=(d0+2)*x-3*mac2(x); if(!f||v<best){best=v;f=1;} } return f? best-2*(a-1)*r : (1LL<<60); }
/* memo of Gamma_ keyed by (a,d0,q,r): exact cache, full key stored */
#define GH (1<<22)
static ll *GK=0, *GV=0;
static ll Gamma_(ll a,ll d0,ll q,ll r){ if(!GK){ GK=malloc(sizeof(ll)*GH*4); GV=malloc(sizeof(ll)*GH); for(ll i=0;i<GH;i++) GK[4*i]=-1; }
  unsigned long long h=((unsigned long long)a*1000003ULL ^ (unsigned long long)d0*998244353ULL ^ (unsigned long long)q*2654435761ULL ^ (unsigned long long)r*40503ULL)&(GH-1);
  for(int probe=0;probe<64;probe++){ ll i=(h+probe)&(GH-1);
    if(GK[4*i]==-1){ ll v=Gamma_raw(a,d0,q,r); GK[4*i]=a; GK[4*i+1]=d0; GK[4*i+2]=q; GK[4*i+3]=r; GV[i]=v; return v; }
    if(GK[4*i]==a&&GK[4*i+1]==d0&&GK[4*i+2]==q&&GK[4*i+3]==r) return GV[i]; }
  return Gamma_raw(a,d0,q,r); }
static int MIX=0,LINK=0,PACK=0,EREP=0,LCOV=0,GCAP=0; static ll ngcap=0; static ll ALMIN=3, ALMAX=1000000;
static ll nmix=0,nlink=0,npack=0; static ll nbig64=0; /* k-cover ranges longer than 64 (diagnostic) */
#define KCAP 4096
static int mixgap_kills(ll a,ll b,ll r,ll q,ll q2,ll u,ll t,ll K,ll B0){
  ll d0=a+b; ll G=Gamma_(a,d0,q,r); if(B0>=G) return 0;
  ll rem=B0-b*u-2*b*r; if(rem<0) return 1;
  ll tall=t+b*r+rem/3; ll eall=tall-(Cn(d0+2,3)-mac2(Cn(d0+1,2)-r)); if(eall<0) return 1;
  ll ng=d0+1-r; if(ng<0) ng=0; ll ml=ceil2(2*Hn(ng)-lam2(ng)*eall); ll ml2=psp(d0+1,r,eall); if(ml2>ml) ml=ml2;
  ll BB=Cn(b+1,2), base=q+q2+u+a*b+BB, mu=-1; for(ll cc=0;cc*(cc+1+base)<=rem;cc++){ ll ee=(rem-cc*(cc+1+base))/(3*a+2*b+cc+base); ll v=Cn(d0+3,3)-r*(1+b)-t+K+cc*(d0+1)+ee; if(v>mu) mu=v; }
  return ml>mu; }
/* MIX-PACK: returns 1 if the profile is excluded */
static int mixpack_kills(ll a,ll b,ll r,ll q,ll q2,ll u,ll t,ll K,ll D3,ll WAbar,ll Hh){
  ll M=-WAbar-Hh-1-b*u; if(M<0) return 1;
  ll ab=a*b, smin=ab-M; if(smin<0) smin=0; ll num=b*smin+ab-M, tmin=num>0? (num+2*a-1)/(2*a):0;
  ll d0=a+b, Ud0=Cn(d0+2,3), top=Cn(d0+1,2)-r, VA=t-a*r; if(VA<0) VA=0;
  for(ll qg=q+smin+tmin; qg<=top; qg++){
    ll m2=mac2(qg), Dg=(d0+2)*qg-3*m2; if(Dg>M+2*(a-1)*r || Dg>D3+M) continue;
    ll Eg=(D3+M-Dg)/3, rg=Cn(d0+1,2)-qg, Zg=Ud0-m2+Eg-d0*rg+C2(rg);
    if(Zg-VA<0) continue;
    ll kmin=rg>0?1:0, kmax=rg>0? gcover(rg,Zg-VA,d0):0; if(kmax<kmin) continue;
    ll co=qg+q2+u; ll Bc1=Cn(d0+3,3)-r*(1+b)-t+K, Bc2=1+d0+Cn(d0+1,2)-r+m2+K; ll Bc=Bc1<Bc2?Bc1:Bc2;
    ll Ug=-1; for(ll cc=0;cc*(cc+1+co)<=M;cc++){ ll ee=(M-cc*(cc+1+co))/(3*a+2*b+cc+co); ll v=Bc+cc*(d0+1)+ee; if(v>Ug) Ug=v; }
    for(ll k=kmin;k<=kmax;k++){ ll eg=Eg; ll z2=Zg-C2(k); if(z2<eg) eg=z2; if(eg<0) continue;
      ll N=d0+1; ll lo=packlow(N-k,eg); ll l2=psp(N,rg,eg); if(l2>lo) lo=l2;
      if(lo<=Ug) return 0; } }
  return 1; }
int main(int argc,char**argv){ mac2_init();
  int amin=atoi(argv[1]), amax=atoi(argv[2]); if(argc>3){ MIX=strchr(argv[3],'M')!=0; LINK=strchr(argv[3],'L')!=0; PACK=strchr(argv[3],'P')!=0; EREP=strchr(argv[3],'E')!=0; LCOV=strchr(argv[3],'H')!=0; GCAP=strchr(argv[3],'G')!=0; if(LCOV) EREP=1; if(EREP) LINK=1; } if(argc>5){ ALMIN=atoll(argv[4]); ALMAX=atoll(argv[5]); }
  ll tot=0;
  for(ll a=amin;a<=amax;a++){
    ll Q=Cn(a+1,2), U=Cn(a+2,3), F=Cn(a+1,3); ll sq=(ll)floor(sqrt((double)(2*F+1))); while((sq+1)*(sq+1)<=2*F+1) sq++; while(sq*sq>2*F+1) sq--;
    ll nbase=0,nu=0,npre=0,nprof=0,nsurv=0; nmix=nlink=npack=0; nbig64=0;
    for(ll al=(ALMIN>3?ALMIN:3);al<=a&&al<=ALMAX;al++){ ll p=a-al, Qa=Cn(al+1,2), Ua=Cn(al+2,3);
     for(ll r=0;r<=Q;r++){ ll q=Q-r, tf=U-mac2(q);
      for(ll n0=(Qa-r>0?Qa-r:0);n0<=Qa;n0++){ ll rLL=Qa-n0;
       for(ll l=0;l<=al*p;l++){ ll q2=n0+l; if(q2>q) break;
        ll E=p<l+r?p:l+r; ll Smin=0; if(p>0){ ll kk=l/p, zz=l%p; Smin=kk*p*(a+2-p)+zz*(a+2-zz); }
        int CEok=(q+q2+2>=2*(al+E)); int hit=0; ll m2q2=mac2(q2);
        for(ll u0=0;u0<=Ua&&u0<=m2q2;u0++){ ll K0=mac3(u0); ll kb=(al+3)*u0/4; if(kb<K0) K0=kb;
         ll u1max=p*n0; ll t1=(al+1)*l/2; if(t1<u1max) u1max=t1; if(m2q2-u0<u1max) u1max=m2q2-u0;
         for(ll u1=0;u1<=u1max;u1++){ ll K1=(al+2)*u1/3, K=K0+K1, u=u0+u1; ll LCbar=(a+1)*(q2+u)-4*K;
          ll num=F-LCbar+(a-3)*r-1; ll tmax= num>=0? num/4 : -((-num+3)/4); if(U-u0-u1<tmax) tmax=U-u0-u1;
          /* G: early GLOC cap (P5 section 24).  W<0 forces Phi<=-1.  With c0<=min(U_al,n0^<2>), S>=Smin, quartic
             allowances K0>=k0, K1>=k1, a nonnegative b coefficient Bc=a-1+q2+u-2al-2n0 and q>=2al (C/E remainder >=0):
             D3 <= -1-P0, P0=(a-1)-2al-2c0max+(2al+1-a)n0+Smin+(a+1)u0-5K0+(a+3)u1-3K1.  P0 increases with u1
             (a+3>3*ceil((al+2)/3)), so once the cap is below tf every larger u1 fails as well. */
          if(GCAP){ ll Bc=a-1+q2+u-2*al-2*n0; if(Bc>=0 && q>=2*al){ ll c0mx=mac2(n0); if(Ua<c0mx) c0mx=Ua;
              ll P0=(a-1)-2*al-2*c0mx+(2*al+1-a)*n0+Smin+(a+1)*u0-5*K0+(a+3)*u1-3*K1;
              ll tg=-1-P0+(a+2)*r; tg = tg>=0? tg/3 : -((-tg+2)/3); if(tg<tmax){ tmax=tg; ngcap++; }
              if(tg<tf) break; } }
          for(ll t=tf;t<=tmax;t++){ hit=1; nu++;
           if(!CEok){ printf("ASSERT CE fails a=%lld al=%lld r=%lld n0=%lld l=%lld\n",a,al,r,n0,l); }
           ll eps=t-tf, D3=3*t-(a+2)*r, WAbar=-F+LCbar-(a-3)*r+4*t;
           ll c0lo=u0; if(Ua-t>c0lo) c0lo=Ua-t; if(Ua-al*rLL-eps>c0lo) c0lo=Ua-al*rLL-eps;
           ll c0hi=mac2(n0); if(U-t-u1<c0hi) c0hi=U-t-u1;
           for(ll c0=c0lo;c0<=c0hi;c0++){ ll t0=Ua-c0; ll bmx=-1; for(ll be=n0;be>=0;be--) if(mac2(Qa-be)>=Ua-u0-t0){ bmx=be; break; } if(bmx<0) continue;
            /* LINK: k range and global link bound (independent of b,R,delta except through m_up) */
            ll zA=t-a*r+C2(r), vlow=t0-al*rLL; if(vlow<0) vlow=0; ll zz=zA-vlow; ll kmin0=0,kmax0=0; int linkimp=0;
            if(LINK){ if(r>0){ if(zz<0) linkimp=1; else { kmin0=1; kmax0=gcover(r,zz,a); if(kmax0<1) linkimp=1; } } else { if(zz<0) linkimp=1; } }
            /* E-REPAIR: fix the actual minimum cover k first; E_k=min(p,l+min(r-rLL,r-k+1)) (r>0), E_0=min(p,l) */
            static ll kE[KCAP]; int nkE=1; kE[0]=-1; if(kmax0-kmin0+1>64) nbig64++; if(kmax0-kmin0+1>KCAP){ fprintf(stderr,"KCAP overflow\n"); exit(2); }
            if(EREP){ if(linkimp){ nlink++; continue; } nkE=0; for(ll k=kmin0;k<=kmax0;k++) kE[nkE++]=k; }
            for(int ie=0;ie<nkE;ie++){ ll kf=kE[ie]; ll Ek=E;
            if(kf>=0){ if(r>0){ ll m1=r-rLL; if(r-kf+1<m1) m1=r-kf+1; Ek=(p<l+m1)?p:l+m1; } else Ek=(p<l)?p:l; }
            if(LCOV && kf>=1){ /* LOCAL-COVER (section 50): j low vertices in the minimum cover; Ehat_k */
              if(r>a*kf-C2(kf)) continue; ll best=-1;
              ll jlo=kf-p>0?kf-p:0, jhi=al<kf?al:kf;
              for(ll j=jlo;j<=jhi;j++){ ll fj=al*j-C2(j); if(rLL>fj) continue;
                if(j<al){ ll e0=kf-j; if(r-rLL<e0) e0=r-rLL; if(r-kf+1<e0) e0=r-kf+1; if(e0>=0&&e0>best) best=e0; }
                if(j>=1){ ll fj1=al*(j-1)-C2(j-1); ll dL=rLL-fj1; if(dL<0) dL=0; ll e1=r-rLL; if(r-kf+1-dL<e1) e1=r-kf+1-dL; if(e1>=0&&e1>best) best=e1; } }
              if(best<0) continue; ll Eh=l+best; if(Eh>p) Eh=p; if(Eh<Ek) Ek=Eh; }
            ll kmin=kmin0,kmax=kmax0; if(kf>=0){ kmin=kmax=kf; }
            ll brB[2]={0,bmx}, brH[2]={0,0}; int nbr=1;
            if(bmx>=1){ ll hc=Cn(p-Ek+2,3)-t+t0; if(hc<0) hc=0; ll mn=0; int f=0; for(ll j=0;j<=Ek;j++){ ll nj=p-j, rj=r-rLL-(j-l>0?j-l:0); if(rj<0) rj=0; ll v=Cn(nj+2,3)-nj*rj-eps; if(!f||v<mn){mn=v;f=1;} } brH[1]=hc>mn?hc:mn; nbr=2; }
            ll betaH=n0<u0+t0?n0:u0+t0; ll CH=al+n0+c0+l+Ek+Cn(Ek+2,3)+(n0+al*Ek)*p;
            ll Bbig=2*CH-(a-1)-(a+3)*q2-(a+1)*u+5*K, BH=a-1+q2+u-2*(al+Ek+l+betaH);
            ll bc=u+(2*r<2*a-r?2*r:2*a-r); if(bc<0) bc=0; ll ng=a+1-r; if(ng<0) ng=0;
            ll mlow=ceil2(2*Hn(ng)-lam2(ng)*eps); ll ml2=psp(a+1,r,eps); if(ml2>mlow) mlow=ml2;
            for(int ib=0;ib<nbr;ib++){ ll beta=brB[ib], Hh=brH[ib]; if(WAbar+Hh>=0) continue;
             ll B0=-WAbar-Hh-1, Bf=a-1+q2+u-2*al-2*beta; ll bcut=3; if((B0+2)/2>bcut) bcut=(B0+2)/2; if(sq-a>bcut) bcut=sq-a; if(bc>0&&B0/bc<bcut) bcut=B0/bc;
             for(ll R=0;R<=p;R++){ ll fR=D3+a-1-2*al-2*beta-2*c0+(a+3)*n0+Smin-2*n0*R+(a+1)*u0-5*K0+(a+3)*u1-3*K1;
              for(ll b=0;b<=bcut;b++){ if(fR+b*Bf>-1){ if(Bf>0) break; continue; } ll budget=B0-b*bc; if(budget<0) break;
               ll mup=-1; for(ll cc=0;cc*(cc+1+q+q2+u)<=budget;cc++){ ll ee=(budget-cc*(cc+1+q+q2+u))/(3*a+2*b+cc+q+q2+u); ll v=Cn(a+b+3,3)-r*(1+b)-t+K+cc*(a+b+1)+ee; if(v>mup) mup=v; }
               npre++; if(mlow>mup) continue;
               ll dmax=Bbig-D3-b*BH-1; if(mup-2<dmax) dmax=mup-2; ll need=(a-1)*(b+1)+(a+1)*(q2+u)+D3+(b+2)*q2+b*u-3*K+1; ll dmin=need>0?(need+2)/3:-((-need)/3); if(dmin<1) dmin=1;
               if(dmin>dmax) continue; nprof++;
               if(MIX && mixgap_kills(a,b,r,q,q2,u,t,K,B0)){ nmix++; continue; }
               /* LINK global: keep k values whose global bound <= mup */
               static ll klist[KCAP]; int nk=0;
               if(LINK){ if(linkimp){ nlink++; continue; } for(ll k=kmin;k<=kmax;k++){ ll ek=eps; if(zA-C2(k)<ek) ek=zA-C2(k); if(ek<0) continue; ll lo=packlow(a+1-k,ek); ll l2=psp(a+1,r,ek); if(l2>lo) lo=l2; if(lo<=mup) klist[nk++]=k; } if(nk==0){ nlink++; continue; } }
               if(PACK && mixpack_kills(a,b,r,q,q2,u,t,K,D3,WAbar,Hh)){ npack++; continue; }
               int any=0;
               for(ll dl=dmin;dl<=dmax&&!any;dl++){ ll w=(dl+1)/2, sj=(3*dl+1)/2;
                 ll ns=R-l-2*r; if(ns<0) ns=0; ll nw=R-r; if(nw<0) nw=0; ll nc=R-l-r; if(nc<0) nc=0;
                 if(!okSP(3*w-2,ns,eps)) continue; if(!okSP(3*dl-2,nw,eps)) continue;
                 if(Cn(nc+2,3)-t>3*w-2) continue; if(Cn(R+2,3)-t>3*dl-2) continue;
                 if(R*(R-1)>2*dl-2+2*r*(r+1)) continue; if(nc*(nc-1)>2*w-2+2*r*(r+1)) continue;
                 ll nj=al+R-r; if(nj<0) nj=0; if(!okSP(3*sj-2,nj,eps)) continue; if(Cn(al+R+2,3)-t>3*sj-2) continue; if(psp(al+R,r,eps)>3*sj-2) continue;
                 if(LINK){ int okk=0; for(int ik=0;ik<nk&&!okk;ik++){ ll k=klist[ik]; ll ek=eps; if(zA-C2(k)<ek) ek=zA-C2(k);
                     ll nj2=al+R-k; if(nj2<0) nj2=0; ll nw2=R-k; if(nw2<0) nw2=0; ll ns2=R-l-r-k; if(ns2<0) ns2=0;
                     if(packlow(nj2,ek)>3*sj-2) continue; if(packlow(nw2,ek)>3*dl-2) continue; if(packlow(ns2,ek)>3*w-2) continue; okk=1; }
                   if(!okk) continue; }
                 any=1; }
               if(any){ nsurv++; if(nsurv<=10) printf("  SURV a=%lld al=%lld r=%lld n0=%lld l=%lld t=%lld u0=%lld u1=%lld c0=%lld beta=%lld R=%lld b=%lld WAbar=%lld Hh=%lld mup=%lld mlow=%lld k=%lld E=%lld\n",a,al,r,n0,l,t,u0,u1,c0,beta,R,b,WAbar,Hh,mup,mlow,kf,Ek); }
              } } } } } } } }
        if(hit) nbase++; } } } }
    printf("a=%lld base=%lld u=%lld profiles(card test)=%lld nonempty-delta=%lld killed: MIX=%lld LINK=%lld PACK=%lld survivors=%lld krange>64=%lld\n",a,nbase,nu,npre,nprof,nmix,nlink,npack,nsurv,nbig64); fflush(stdout); tot+=nsurv; }
  printf("total survivors %lld\n",tot); return 0; }
