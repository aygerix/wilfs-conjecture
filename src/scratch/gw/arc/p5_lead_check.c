/* Primary regime 3m<c<=4m with 2n1>=c-m, e>=3. Classes by generator band: A: n<c-2m, B: [c-2m,c-m), C: [c-m,c), E: [c,c+m).
   Report min W, min W/c, and the crude arc bound slack, split by (b,c,e) presence; print smallest-W examples with outside dirs.
   usage: arc_mixed seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[4096]; static int done[4096]; static int gens[64]; static long mg[4096];
  long npure=0,nmix=0; double minr_p=1e9,minr_x=1e9; long minW_p=1L<<40,minW_x=1L<<40; int shown=0;
  long nbcount[8]={0}; long p5fail=0,p5ok=0,p5minsl=1L<<40;
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1);
    int ng=2+rnd()%14;
    int g0=0;
    for(int k=0;k<ng;k++){ int mode=rnd()%4; int lo,hi;
      if(mode<2){ lo=m+m/3+rnd()%(m/2+1); hi=2*m-1; } else if(mode==2){ lo=2*m; hi=3*m; } else { lo=3*m; hi=5*m; }
      if(hi<=lo) hi=lo+1; gens[g0++]=lo+rnd()%(hi-lo); }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(!(c>3*m && c<=4*m)) continue;
    int nm=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) mg[nm++]=ap[r]; }
    if(nm<2) continue;
    long n1=1L<<60; int na=0,nb=0,nc=0,ne=0; for(int i=0;i<nm;i++){ if(mg[i]<n1) n1=mg[i]; if(mg[i]<c-2*m) na++; else if(mg[i]<c-m) nb++; else if(mg[i]<c) nc++; else ne++; }
    if(2*n1<c-m) continue;
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long l=c-g; long W=(long)(nm+1)*l-c;
    double rr=(double)W/c;
    if(na>=1){ long bnd=(long)(na-1)*(nb+1)+(long)nc*(nc+ne+1)+(long)ne*(3*na+2*nb-1); if(W<bnd){ p5fail++; printf("P5 FAIL m=%d c=%ld a=%d b=%d c=%d e=%d W=%ld bound=%ld\n",m,c,na,nb,nc,ne,W,bnd);} else p5ok++; if(W-bnd<p5minsl) p5minsl=W-bnd; }
    if(nb+nc+ne==0){ npure++; if(rr<minr_p) minr_p=rr; if(W<minW_p) minW_p=W; }
    else { nmix++; if(rr<minr_x) minr_x=rr; if(W<minW_x) minW_x=W; int key=(nb>0)+2*(nc>0)+4*(ne>0); nbcount[key]++;
      if(W<0 || (rr<0.06 && shown<10)){ shown++; printf("small: m=%d c=%ld e=%d a=%d b=%d c=%d e=%d W=%ld W/c=%.3f\n",m,c,nm+1,na,nb,nc,ne,W,rr); } }
  }
  printf("seed=%s pure: n=%ld minW=%ld minW/c=%.4f | mixed: n=%ld minW=%ld minW/c=%.4f | mixed by (B,C,E) mask:",argv[1],npure,minW_p,minr_p,nmix,minW_x,minr_x);
  for(int k=1;k<8;k++) printf(" %d:%ld",k,nbcount[k]); printf("\n  P5 weak bound checks: ok=%ld fail=%ld min slack=%ld\n",p5ok,p5fail,p5minsl);
  return 0; }
