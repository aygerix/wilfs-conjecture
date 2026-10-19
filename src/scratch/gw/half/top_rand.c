/* Random numerical semigroups with larger m: Apery set via Dijkstra mod m.
   For each S with K = floor(maxAp/m) >= KMIN: top-half S_i (i=floor((K+2)/2)), all window inequalities P_j (j<=K),
   and Wilf. usage: top_rand seed trials mmin mmax KMIN */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]),KMIN=atoi(argv[5]);
  static long ap[512]; static int done[512]; static int gens[64];
  long cnt=0,posS=0,pjfail=0,wilffail=0; long worstS=-1000000; 
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1);
    int ng=1+rnd()%6;            /* number of random generators beyond m */
    int span=m*(2+rnd()%10);
    int g0=0; for(int k=0;k<ng;k++){ gens[g0++]=m+1+rnd()%span; }
    /* Dijkstra on residues */
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;   /* gcd>1 */
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    int K=M/m; if(K<KMIN) continue;
    /* embedding dimension: minimal generators = m + Apery elements not sums of two nonzero Apery elements */
    int e=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) e++; }
    int d=e-1; cnt++;
    long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; }
    if(g>(long)d*l){ wilffail++; printf("WILF FAIL m=%d e=%d\n",m,e); }
    for(int j=1;j<=K;j++){ long a=0,b=0; for(int r=0;r<m;r++){ long k1=ap[r]/m,l1=(M-ap[r])/m; a+=k1<j?k1:j; b+=l1<j?l1:j; }
      if(a>(long)d*b){ pjfail++; if(pjfail<=10){ printf("PGW FAIL j=%d K=%d m=%d e=%d gens:",j,K,m,e); for(int k=0;k<g0;k++) printf(" %d",gens[k]); printf("\n"); } } }
    int i=(K+2)/2; long su=0,sl=0; for(int r=0;r<m;r++){ long k1=ap[r]/m,l1=(M-ap[r])/m; if(k1>i) su+=k1-i; if(l1>i) sl+=l1-i; }
    long S=su-(long)d*sl; if(S>worstS) worstS=S;
    if(S>0){ posS++; if(posS<=8){ printf("S_i>0: S=%ld K=%d i=%d m=%d e=%d gens:",S,K,i,m,e); for(int k=0;k<g0;k++) printf(" %d",gens[k]); printf("\n"); } }
  }
  printf("seed=%s sampled(K>=%d)=%ld  S_i>0: %ld (max S_i=%ld)  PGW fails: %ld  Wilf fails: %ld\n",argv[1],KMIN,cnt,posS,worstS,pjfail,wilffail);
  return 0; }
