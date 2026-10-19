/* Exhaustive search over truncations S = <m, a1..ak> u [C, inf) (k = 2 or 3 left generators besides m),
   for Eliahou semigroups (E = |L|*lgen + q*r - c < 0) with 3e < m (would refute H_E: E<0 => 3e>=m).
   usage: he_trunc mmax k Cmult_max */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static long ap[512]; static int done_[512];
static int MMAX,KG,CM; static long nE=0,nHE=0,tot=0; static double minWc=1e9; static long minEm=0;
static void test(int m,int *g,int k,long C){
  for(int r=0;r<m;r++){ ap[r]=-1; done_[r]=0; } ap[0]=0;
  for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done_[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done_[b]=1; for(int j=0;j<k;j++){ int r2=(b+g[j])%m; long v=ap[b]+g[j]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
  for(int r=1;r<m;r++){ long f=C+((r-C%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; }
  long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
  long c=M-m+1; if(c<=3L*m) return; tot++;
  int lgen=1,rgen=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec){ if(ap[r]<c) lgen++; else rgen++; } }
  long g2=0; for(int r=0;r<m;r++) g2+=ap[r]/m; long kL=c-g2; long q=(c+m-1)/m; long E=kL*lgen+q*rgen-c; int e=lgen+rgen;
  if(E<0){ nE++; double wc=(double)((long)e*kL-c)/c; if(wc<minWc) minWc=wc; if(E<minEm) minEm=E;
    if(3*e<m){ nHE++; if(nHE<=20){ printf("HE FAIL m=%d gens:",m); for(int j=0;j<k;j++) printf(" %d",g[j]); printf(" C=%ld c=%ld q=%ld e=%d (l=%d r=%d) |L|=%ld E=%ld W=%ld\n",C,c,q,e,lgen,rgen,kL,E,(long)e*kL-c);} } }
}
int main(int argc,char**argv){ MMAX=atoi(argv[1]); KG=atoi(argv[2]); CM=atoi(argv[3]);
  int g[4];
  for(int m=4;m<=MMAX;m++){
    for(int a=m+1;a<3*m;a++){ g[0]=a;
      if(KG==1){ for(long C=3L*m;C<=(long)CM*m;C++) test(m,g,1,C); continue; }
      for(int b=a+1;b<3*m;b++){ g[1]=b;
        if(KG==2){ for(long C=3L*m+1;C<=(long)CM*m;C++) test(m,g,2,C); continue; }
        for(int cc=b+1;cc<3*m;cc++){ g[2]=cc; for(long C=3L*m+1;C<=(long)CM*m;C+=1) test(m,g,3,C); } } } }
  printf("mmax=%d k=%d Cmax=%dm: truncations with c>3m: %ld, Eliahou: %ld (min E %ld), with 3e<m: %ld, min W/c among Eliahou %.4f\n",MMAX,KG,CM,tot,nE,minEm,nHE,minWc);
  return 0; }
