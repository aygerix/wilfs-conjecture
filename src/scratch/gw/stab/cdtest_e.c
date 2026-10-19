/* Viability of a Cauchy-Davenport route for prime multiplicity m.
   Layers A_j = #(S cap [jm,(j+1)m)), j>=0.  Lower bound A*_j from: A*_0=1; A*_j >= A*_{j-1};
   A*_j >= 1 + #{generators n != m with floor(n/m) <= j}; A*_{i+j+1} >= min(m, A*_i + A*_j - 1) (CD, prime m).
   Capped at m-1 for j <= K-2 (layers below F-m contain a gap).  ell_CD = sum_{j<=K-2} A*_j + 1 (lossy last layer).
   Report fraction of prime-m S (e>=3) with e*ell_CD >= c, and compare with the true layer sums.  usage: cdtest G */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
#define PM 128
static int nshow; static int G; static long tot, ok_cd, ok_true_lossy, tot_e3; static long byK[40], okK[40]; static long byE[64], failE[64], failE3[64];
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static int isprime(int x){ if(x<2) return 0; for(int p=2;p*p<=x;p++) if(x%p==0) return 0; return 1; }
static void analyze(u128 gm,int F,int m,int *gens,int e){
  if(!isprime(m)||e<3) return; int c=F+1; int K=(c+m-1)/m+1; /* layers 0..K-1, conductor in layer K-2 or so */
  int Kl=c/m; /* full layers below c: j=0..Kl-1 are [jm,(j+1)m) subset [0,c) */
  long A[64]={0}; for(int j=0;j<Kl;j++){ for(int x=j*m;x<(j+1)*m;x++) if(!gapq(gm,x)) A[j]++; }
  long ell=0; for(int x=0;x<c;x++) if(!gapq(gm,x)) ell++;
  long rest=ell; for(int j=0;j<Kl;j++) rest-=A[j]; /* elements in the partial layer [Kl m, c) */
  long As[64]; for(int j=0;j<Kl;j++){ As[j]=1; int cntg=0; for(int a=0;a<e;a++) if(gens[a]!=m && gens[a]/m<=j) cntg++; if(1+cntg>As[j]) As[j]=1+cntg; if(j>0&&As[j-1]>As[j]) As[j]=As[j-1];
    for(int i=0;i+1<=j;i++){ int k=j-1-i; if(k<0) continue; long v=As[i]+As[k]-1; if(v>m) v=m; if(v>As[j]) As[j]=v; }
    if(As[j]>m-1) As[j]=m-1; }
  long ellcd=0; for(int j=0;j<Kl;j++) ellcd+=As[j];
  tot++; int KK=Kl<39?Kl:39; byK[KK]++; byE[e<63?e:63]++;
  if((long)e*ellcd>=c){ ok_cd++; okK[KK]++; }
  else { failE[e<63?e:63]++; if(Kl>=3) failE3[e<63?e:63]++; }
  if((long)e*ellcd<c && Kl>=3 && e>=5 && nshow<40){ nshow++; printf("CDFAIL m=%d e=%d c=%d ell=%ld ellcd=%ld (need %d) Kl=%d partial=%ld gens:",m,e,c,ell,ellcd,(c+e-1)/e,Kl,rest); for(int a=0;a<e;a++) printf(" %d",gens[a]); printf("\n   A  :"); for(int j=0;j<Kl;j++) printf(" %ld",A[j]); printf("\n   A* :"); for(int j=0;j<Kl;j++) printf(" %ld",As[j]); printf("\n"); }
  /* sanity: true layers satisfy the CD lower bound */
  for(int j=0;j<Kl;j++) if(A[j]<As[j]){ printf("CD BOUND VIOLATED m=%d j=%d A=%ld As=%ld\n",m,j,A[j],As[j]); break; }
}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  if(m>1) analyze(gm,F,m,gens,e);
  if(genus==G) return; int ng[PM*2];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); int gens[]={1}; visit(0,-1,1,gens,1,0);
  printf("genus<=%d prime m, e>=3: %ld S; CD-only bound proves Wilf for %ld (%.2f%%)\n",G,tot,ok_cd,100.0*ok_cd/(tot?tot:1));
  for(int k=0;k<64;k++) if(byE[k]) printf("  e=%d: %ld S, CD fails %ld (with >=3 full layers: %ld)\n",k,byE[k],failE[k],failE3[k]);
  for(int k=0;k<40;k++) if(byK[k]) printf("  full layers below c = %d: %ld S, CD proves %ld (%.1f%%)\n",k,byK[k],okK[k],100.0*okK[k]/byK[k]);
  return 0; }
