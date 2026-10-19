/* Arc lemma tests. Random S = <m, gens>, Apery via Dijkstra.
   (i) |A_{<=2}| >= min(m, 3n_1 - c), A_{<=2} = {w in Ap : w = 0, a min generator, or a sum of two min generators}.
   (ii) class 2n_1 >= c - m: min W/c per K = floor(c/m) band; Wilf failures.
   usage: arc_test seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[2048]; static int done[2048]; static int gens[64]; static int isgen[2048]; static long mg[2048];
  long cnt=0,arcfail=0,cls=0,wf=0; double minr[16]; long ncls[16]; for(int i=0;i<16;i++){minr[i]=1e9;ncls[i]=0;}
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1);
    int ng=1+rnd()%14;
    /* generators in [lo, hi] with lo ~ m*(1+u), hi ~ lo + span */
    int lo=m+1+rnd()%(2*m); int span=1+rnd()%(3*m);
    int g0=0; for(int k=0;k<ng;k++){ gens[g0++]=lo+rnd()%span; }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(c<=0) continue;
    int e=1,nm=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } isgen[r]=!dec; if(!dec){ e++; mg[nm++]=ap[r]; } }
    int d=e-1; cnt++;
    long n1=1L<<60; for(int i=0;i<nm;i++) if(mg[i]<n1) n1=mg[i];
    /* A_{<=2} */
    long a2=0; for(int r=0;r<m;r++){ if(r==0||isgen[r]){a2++;continue;} int f=0; for(int i=0;i<nm&&!f;i++) for(int j=i;j<nm;j++) if(mg[i]+mg[j]==ap[r]){f=1;break;} if(f) a2++; }
    long need=3*n1-c; if(need>m) need=m;
    if(a2<need){ arcfail++; if(arcfail<5) printf("ARC FAIL m=%d c=%ld n1=%ld a2=%ld\n",m,c,n1,a2); }
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long l=c-g; long W=(long)e*l-c;
    if(2*n1>=c-m){ cls++; int K=c/m; if(K>15)K=15; ncls[K]++; double rr=(double)W/c; if(rr<minr[K]) minr[K]=rr; if(W<0){wf++; printf("WILF FAIL m=%d c=%ld e=%d\n",m,c,e);} }
  }
  printf("seed=%s sampled=%ld arc_fail=%ld class(2n1>=c-m)=%ld wilf_fail=%ld\n",argv[1],cnt,arcfail,cls,wf);
  for(int K=0;K<16;K++) if(ncls[K]) printf("  K=floor(c/m)=%d: n=%ld min W/c=%.4f\n",K,ncls[K],minr[K]);
  return 0; }
