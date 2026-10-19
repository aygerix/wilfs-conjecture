/* Semigroups whose Apery set (w.r.t. m) consists of 0, minimal generators and sums of two minimal generators.
   Report min W/c by K=floor(c/m), type t vs e, and examples. usage: quad_test seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[4096]; static int done[4096]; static int gens[64]; static int isg[4096]; static long mg[4096];
  double minr[64]; long nn[64]; long tge=0; for(int i=0;i<64;i++){minr[i]=1e9;nn[i]=0;}
  long nq=0, wf=0;
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1);
    int ng=2+rnd()%16; int g0=0;
    double lo=1.0+(rnd()%3000)/1000.0; double wid=(rnd()%1000)/1000.0*lo*0.5;
    for(int k=0;k<ng;k++) gens[g0++]=(int)(m*(lo+wid*((rnd()%10000)/10000.0)))+1;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    int nm=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } isg[r]=!dec; if(!dec) mg[nm++]=ap[r]; }
    int quad=1; for(int r=1;r<m&&quad;r++){ if(isg[r]) continue; int f=0; for(int i=0;i<nm&&!f;i++) for(int j=i;j<nm;j++) if(mg[i]+mg[j]==ap[r]){f=1;break;} if(!f) quad=0; }
    if(!quad) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(c<=0) continue; nq++;
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long l=c-g; int e=nm+1; long W=(long)e*l-c;
    /* type: maximal Apery elements */
    int tt=0; for(int r=1;r<m;r++){ int mx=1; for(int s=1;s<m&&mx;s++){ int r2=(r+s)%m; if(r2==0) continue; if(ap[r2]==ap[r]+ap[s]) mx=0; } if(mx) tt++; }
    if(tt>=e) tge++;
    int K=c/m; if(K>63)K=63; nn[K]++; double rr=(double)W/c; if(e>=3 && rr<minr[K]) minr[K]=rr;
    if(W<0){ wf++; printf("WILF FAIL m=%d c=%ld e=%d\n",m,c,e); }
  }
  printf("seed=%s quadratic S=%ld (type>=e: %ld) WilfFail=%ld |",argv[1],nq,tge,wf);
  for(int K=0;K<64;K++) if(nn[K]) printf(" K%d:n=%ld,min=%.3f",K,nn[K],minr[K]); printf("\n");
  return 0; }
