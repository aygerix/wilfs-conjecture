/* Lead's independent check of codex P5b Theorem T2.1 (one low A unit) ingredients, on semigroups with 3m<c<=4m.
   Setting (P4/P5 notation): M=c+m-1, rho=5m-1-M, h=c-3m, unit offsets t=n-m; classes A:[1,h) B:[h,h+m) C:[h+m,h+2m) E:[h+2m,h+3m).
   Cell of degree j: tau = v - j m.  Low A unit: 2t<h.  Arc: theta=ceil(3h/2), Y=[h,min(theta,m)) u [1,theta-m) (residues v mod m).
   Allowed occupants of Y: AA with tau>=h (q3), B/C/E units, AB with tau>=m+h (s4), BB with tau>=m+h (t4). Others: intruders J; pure-A: J_A.
   Checks (only when a>=6 and exactly one low A unit x):
     OL:     2 J_A <= (a-1) + LC + 2 q2 + k,   LC=(a+1)(q2+u3)-4k, q2=#AA tau<h, u3=#AAA tau<h, k=#quartics.
     OLout:  J - J_A <= b(1+eps2) + c,  eps2=[x^2 in D].
     FINAL:  W >= (a-1)(b+1) + G0 + LC + b u3 - max(0, 2J - (b+2) q2 - k),  G0=c(c+e+1)+e(3a+2b-1).
   Also checks every pure-A intruder is one of: x, x^2, x^3, x^4 (cold), or hot x^3, x^2 y, x y z (y,z high).
   Down-set: grlex normal forms (GR=1) or lex (GR=0).  usage: lead_t2_check seed trials mmin mmax GR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 400
#define DM 64
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[MM]; static int done[MM], gens[DM], X[MM][DM]; static long mg[DM];
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+11; long T=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int GR=atoi(argv[5]);
  long tested=0, fOL=0, fOUT=0, fFIN=0, fTYPE=0, fW=0; long minOL=1L<<40, minFIN=1L<<40;
  for(long t=0;t<T;t++){
    int m=mmin+rnd()%(mmax-mmin+1); int h=1+rnd()%(m-1); long C=3L*m+h; /* target conductor */
    int na=6+rnd()%8, nb=rnd()%4, ncc=rnd()%3, ne=rnd()%3; int g0=0;
    /* one low A unit, the rest high A */
    { int L=1+rnd()%((h-1)/2>0?(h-1)/2:1); if(2*L>=h) continue; gens[g0++]=m+L; }
    for(int k=1;k<na;k++){ int lo=(h+1)/2, hi=h-1; if(hi<lo) break; gens[g0++]=m+lo+rnd()%(hi-lo+1); }
    for(int k=0;k<nb;k++) gens[g0++]=m+h+rnd()%m;
    for(int k=0;k<ncc;k++) gens[g0++]=2*m+h+rnd()%m;
    for(int k=0;k<ne;k++) gens[g0++]=3*m+h+rnd()%m;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    /* truncate at C so the conductor is at most C (adds E-type generators) */
    for(int r=1;r<m;r++){ long f=C+((r-C%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; }
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(!(c>3L*m && c<=4L*m)) continue;
    int d=0, ok=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec){ if(d>=DM){ok=0;break;} mg[d++]=ap[r]; } }
    if(!ok) continue;
    long H=c-3L*m; int cls[DM]; int a=0,b=0,cc=0,e=0,nlow=0,xl=-1;
    for(int i=0;i<d;i++){ long tt=mg[i]-m; if(tt<H){cls[i]=0;a++; if(2*tt<H){nlow++; xl=i;}} else if(tt<H+m){cls[i]=1;b++;} else if(tt<H+2*m){cls[i]=2;cc++;} else {cls[i]=3;e++;} }
    if(a<6||nlow!=1) continue;
    /* normal forms */
    int ord[MM]; for(int r=0;r<m;r++) ord[r]=r; for(int i=1;i<m;i++){ int x=ord[i],j=i-1; while(j>=0&&ap[ord[j]]>ap[x]){ ord[j+1]=ord[j]; j--; } ord[j+1]=x; }
    for(int hh=0;hh<d;hh++) X[0][hh]=0;
    for(int ii=1;ii<m&&ok;ii++){ int r=ord[ii]; long w=ap[r]; int found=0,bdeg=1<<30; static int best[DM],cand[DM];
      for(int j=0;j<d;j++) if(w>=mg[j]){ int tr=(int)((w-mg[j])%m); if(ap[tr]==w-mg[j]){ int cd=0; for(int q=0;q<d;q++){ cand[q]=X[tr][q]+(q==j); cd+=cand[q]; }
        int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int q=0;q<d;q++) if(cand[q]!=best[q]){ better=cand[q]>best[q]; break; } } }
        if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
      if(!found) ok=0; else for(int q=0;q<d;q++) X[r][q]=best[q]; }
    if(!ok) continue;
    long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)d*l-g;
    if(W<0){ fW++; printf("WILF FAIL m=%d\n",m); }
    long q2=0,u3=0,k=0; int eps2=0;
    for(int r=1;r<m;r++){ int deg=0, allA=1; for(int q=0;q<d;q++){ deg+=X[r][q]; if(X[r][q]&&cls[q]!=0) allA=0; }
      long tau=ap[r]-(long)deg*m;
      if(deg==2&&allA&&tau<H) q2++; if(deg==3&&allA&&tau<H) u3++; if(deg==4) k++; if(deg==2&&X[r][xl]==2) eps2=1; }
    long theta=(3*H+1)/2; long J=0,JA=0;
    for(int r=1;r<m;r++){ int inY=( (r>=H && r<theta && r<m) || (r>=1 && r<theta-m) ); if(!inY) continue;
      int deg=0, allA=1, nA=0,nB=0,nC=0,nE=0; for(int q=0;q<d;q++){ deg+=X[r][q]; if(X[r][q]){ if(cls[q]==0) nA+=X[r][q]; else { allA=0; if(cls[q]==1) nB+=X[r][q]; else if(cls[q]==2) nC+=X[r][q]; else nE+=X[r][q]; } } }
      long tau=ap[r]-(long)deg*m; int allowed=0;
      if(deg==2&&allA&&tau>=H) allowed=1;
      if(deg==1&&!allA) allowed=1;
      if(deg==2&&nA==1&&nB==1&&tau>=m+H) allowed=1;
      if(deg==2&&nB==2&&tau>=m+H) allowed=1;
      if(allowed) continue;
      J++; if(allA){ JA++;
        /* type check */
        int xa=X[r][xl]; int nhigh=deg-xa; int okt=0;
        if(nhigh==0 && xa>=1 && xa<=4) okt=1; /* x^j */
        if(deg==3 && xa>=1) okt=1;            /* x^2 y or x y z */
        if(!okt){ fTYPE++; if(fTYPE<5){ printf("TYPE FAIL m=%d deg=%d xa=%d tau=%ld\n",m,deg,xa,tau);} } } }
    long LC=(long)(a+1)*(q2+u3)-4*k;
    long olr=(a-1)+LC+2*q2+k-2*JA; if(olr<0){ fOL++; if(fOL<5) printf("OL FAIL m=%d a=%d JA=%ld q2=%ld u3=%ld k=%ld\n",m,a,JA,q2,u3,k);} if(olr<minOL) minOL=olr;
    if(J-JA>(long)b*(1+eps2)+cc){ fOUT++; if(fOUT<5) printf("OLOUT FAIL m=%d J=%ld JA=%ld b=%d c=%d eps2=%d\n",m,J,JA,b,cc,eps2); }
    long G0=(long)cc*(cc+e+1)+(long)e*(3*a+2*b-1); long loss=2*J-(long)(b+2)*q2-k; if(loss<0) loss=0;
    long fin=W-((long)(a-1)*(b+1)+G0+LC+(long)b*u3-loss); if(fin<0){ fFIN++; if(fFIN<5) printf("FINAL FAIL m=%d W=%ld\n",m,W);} if(fin<minFIN) minFIN=fin;
    tested++;
  }
  printf("seed=%s GR=%d tested(one low unit, a>=6)=%ld | OL fails %ld (min slack %ld) | OLout fails %ld | type fails %ld | FINAL fails %ld (min slack %ld) | Wilf fails %ld\n",argv[1],GR,tested,fOL,minOL,fOUT,fTYPE,fFIN,minFIN,fW);
  return 0; }
