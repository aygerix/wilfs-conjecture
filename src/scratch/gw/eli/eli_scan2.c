/* Random search for Eliahou semigroups (E = k*l + q*r - c < 0; k = #S∩[0,c), l = #min gens < c incl. m,
   r = #min gens >= c, q = ceil(c/m)), and coverage by the lead's proved criteria:
   EL: c<=3m (Eliahou; then E>=0 anyway), G24: 3m<c<=4m and a<=6 (a = #gens in (m,c-2m)),
   G25: 3m<c<=4m, pure A, 2n1>=c-m; G26c: 3m<c<=4m, 2n1>=c-m (conjectural GW-26);
   G20: #PF>=3m <= e-1;  TAU: #PF in [c-m,c) ... (not used).  usage: eli_scan seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[4096]; static int done[4096]; static int gens[64]; static long mg[4096]; static int isg[4096];
  long found=0, byq[16]={0}, cov24=0,cov25=0,cov26=0,cov20=0,uncov=0, wneg=0, litcov=0; double minWc=1e9, minWfront=1e9;
  for(long t=0;t<trials;t++){
    int h=2+rnd()%3; int ng=3+rnd()%10;
    /* m ~ C(ng+h-1,h) * factor */
    double cnt=1; for(int i=0;i<h;i++) cnt=cnt*(ng+i)/(i+1);
    int m=(int)(cnt*(0.4+(rnd()%1000)/1000.0*1.2)); if(m<mmin) m=mmin; if(m>mmax) continue;
    int qq=h+(rnd()%3); long C=(long)qq*m-(long)(rnd()%m); if(C<=3*m) continue;
    double lo=(double)C/h, hi=(double)(C+m)/h; if(lo<=m+1) lo=m+1; if(hi<=lo+1) continue;
    int g0=0; for(int k=0;k<ng;k++){ long gv=(long)(lo+(hi-lo)*((rnd()%10000)/10000.0)); gens[g0++]=(int)gv; }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    for(int r=0;r<m;r++){ long f=C+((r-C%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=(r==0?0:f); }
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(c<=3*m) continue;
    int nm=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } isg[r]=!dec; if(!dec) mg[nm++]=ap[r]; }
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long k=c-g; int e=nm+1;
    int lgen=1,rgen=0; for(int i=0;i<nm;i++){ if(mg[i]<c) lgen++; else rgen++; }
    long q=(c+m-1)/m; long E=k*lgen+q*rgen-c; if(E>=0) continue;
    found++; if(q<16) byq[q]++;
    long W=(long)e*k-c; if(W<0){ wneg++; printf("WILF COUNTEREXAMPLE?! m=%d c=%ld\n",m,c); }
    double wc=(double)W/c; if(wc<minWc) minWc=wc;
    /* PF numbers: w - m for w maximal in Ap (w + n not in Ap for all min gens... use: w maximal iff no w' in Ap with w'-w in S\{0}) */
    int npf3=0; for(int r=1;r<m;r++){ int maxl=1; for(int s=1;s<m&&maxl;s++){ int r2=(r+s)%m; if(r2==0) continue; if(ap[r2]==ap[r]+ap[s]) maxl=0; } if(maxl && ap[r]-m>=3*m) npf3++; }
    int c24=0,c25=0,c26=0,c20=(npf3<=e-1);
    long n1=1L<<60; int na=0,pure=1; for(int i=0;i<nm;i++){ if(mg[i]<n1) n1=mg[i]; if(mg[i]<c-2*m) na++; else pure=0; }
    if(c<=4*m){ if(na<=6) c24=1; if(2*n1>=c-m){ c26=1; if(pure) c25=1; } }
    cov24+=c24; cov25+=c25; cov26+=c26; cov20+=c20;
    /* literature criteria */
    long rho=q*m-c; int lit21=(3*e>=m); int lit18=(k<=12);
    int lit15=0; if(q>=4){ lit15=1; for(int i=0;i<nm;i++) if(mg[i]<c && !(mg[i]<m+(double)(m-rho)/(q-1))) lit15=0; }
    long s2=0; for(int r=1;r<m;r++) if(ap[r]<2*m) s2++; /* |S∩(m,2m)| = #Apery in (m,2m) */
    int lit33=(q>2 && (double)s2*s2>= (double)q*m/(q-2));
    int lit=lit21||lit18||lit15||lit33;
    litcov+=lit;
    if(!(c24||c25||c20||lit)){ uncov++; if(W<minWfront*(double)c) minWfront=(double)W/c; if(uncov<=12) printf("UNCOVERED m=%d c=%ld q=%ld e=%d lgen=%d r=%d E=%ld W=%ld W/c=%.3f na=%d npf3=%d s2=%ld\n",m,c,q,e,lgen,rgen,E,W,wc,na,npf3,s2); }
  }
  printf("seed=%s Eliahou found=%ld Wneg=%ld minW/c=%.4f | covered: G24=%ld G25=%ld G26(conj)=%ld G20=%ld | lit(3e>=m,|L|<=12,E7.2,DKM)=%ld | uncovered by ours+lit=%ld (min W/c %.3f) | by q:",argv[1],found,wneg,minWc,cov24,cov25,cov26,cov20,litcov,uncov,minWfront);
  for(int i=0;i<16;i++) if(byq[i]) printf(" q%d:%ld",i,byq[i]); printf("\n");
  return 0; }
