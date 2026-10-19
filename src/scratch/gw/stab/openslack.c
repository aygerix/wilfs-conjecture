/* Slack in the open regime of Wilf: 3e < m and c > 3m.  For all S of genus <= G, report min W/c and argmin,
   and min W/c by K = ceil(c/m), plus the same with prime m.  usage: openslack G */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
#define PM 128
static int G; static long n_open, n_open_p; static double mr=1e9, mrp=1e9, mrK[40]; static long nK[40];
static char best[512], bestp[512], bestK[40][256];
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static int isprime(int x){ if(x<2) return 0; for(int p=2;p*p<=x;p++) if(x%p==0) return 0; return 1; }
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  if(m>1){ int c=F+1; if(3*e<m && c>3*m){ int ell=0; for(int x=0;x<c;x++) if(!gapq(gm,x)) ell++; long W=(long)e*ell-c; double r=(double)W/c; n_open++;
      int K=(c+m-1)/m; if(K>39) K=39; nK[K]++;
      if(r<mrK[K]){ mrK[K]=r; int p=0; p+=sprintf(bestK[K]+p,"m=%d e=%d c=%d ell=%d W=%ld gens:",m,e,c,ell,W); for(int j=0;j<e&&p<230;j++) p+=sprintf(bestK[K]+p," %d",gens[j]); }
      if(r<mr){ mr=r; int p=0; p+=sprintf(best+p,"m=%d e=%d c=%d ell=%d W=%ld gens:",m,e,c,ell,W); for(int j=0;j<e;j++) p+=sprintf(best+p," %d",gens[j]); }
      if(isprime(m)){ n_open_p++; if(r<mrp){ mrp=r; int p=0; p+=sprintf(bestp+p,"m=%d e=%d c=%d ell=%d W=%ld gens:",m,e,c,ell,W); for(int j=0;j<e;j++) p+=sprintf(bestp+p," %d",gens[j]); } } } }
  if(genus==G) return; int ng[PM*2];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); for(int k=0;k<40;k++) mrK[k]=1e9; int gens[]={1}; visit(0,-1,1,gens,1,0);
  printf("genus<=%d open regime (3e<m, c>3m): %ld S; min W/c = %.4f  [%s]\n",G,n_open,mr,best);
  printf("  prime m: %ld S; min W/c = %.4f  [%s]\n",n_open_p,mrp,bestp);
  for(int k=0;k<40;k++) if(nK[k]) printf("  K=%d: %ld S, min W/c %.4f [%s]\n",k,nK[k],mrK[k],bestK[k]);
  return 0; }
