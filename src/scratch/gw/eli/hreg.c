/* Random h-regular semigroups S = <m, Gamma> ∪ [C,∞), Gamma ⊂ [C/h,(C+m)/h). Recompute true c; keep if h*Gamma ⊂ [c,c+m)
   (h-regular w.r.t. true c). Report min W/c and min E by (h,q), counts with E<0. Optionally greedy B_h-ish sets.
   usage: hreg seed trials mmin mmax hmin hmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int hmin=atoi(argv[5]),hmax=atoi(argv[6]);
  static long ap[8192]; static int done[8192]; static long gens[64]; static long mg[8192]; static char seen[8192];
  double minWc[8][12]; long cnt[8][12], neg[8][12]; long minE[8][12];
  for(int i=0;i<8;i++)for(int j=0;j<12;j++){minWc[i][j]=1e9;cnt[i][j]=0;neg[i][j]=0;minE[i][j]=1L<<40;}
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1); int h=hmin+rnd()%(hmax-hmin+1);
    int qq=h+1+rnd()%3; long C=(long)qq*m-(long)(rnd()%m);
    double lo=(double)C/h, hi=(double)(C+m)/h; if(lo<m+1) lo=m+1; if(hi<=lo+2) continue;
    int ng=2+rnd()%12; int g0=0;
    int greedy=rnd()%2;
    for(int tries=0; g0<ng && tries<2000; tries++){
      long gv=(long)lo+(long)(rnd()%(long)(hi-lo)); if(gv<lo) continue;
      int dup=0; for(int k=0;k<g0;k++) if(gens[k]==gv) dup=1; if(dup) continue;
      if(greedy && h<=3){ /* reject if creates a collision mod m among sums of length <= h (cheap check for pairs) */
        memset(seen,0,m); int bad=0; seen[0]=1;
        long tmp[64]; int nt=g0; for(int k=0;k<g0;k++) tmp[k]=gens[k]; tmp[nt++]=gv;
        for(int a=0;a<nt&&!bad;a++){ int r=tmp[a]%m; if(seen[r]) bad=1; seen[r]=1; }
        for(int a=0;a<nt&&!bad;a++) for(int b=a;b<nt&&!bad;b++){ int r=(tmp[a]+tmp[b])%m; if(seen[r]) bad=1; seen[r]=1; }
        if(bad) continue; }
      gens[g0++]=gv; }
    if(g0<2) continue;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    for(int r=1;r<m;r++){ long f=C+((r-C%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; }
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1;
    int nm=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) mg[nm++]=ap[r]; }
    /* left generators other than m */
    long G[64]; int nG=0; int okreg=1; for(int i=0;i<nm;i++) if(mg[i]<c){ if(nG<64) G[nG++]=mg[i]; }
    if(nG<1) continue;
    /* h-regular wrt true c: all h-fold sums in [c,c+m): suffices min h*G >= c and max h*G < c+m */
    long gmin=G[0],gmax=G[0]; for(int i=0;i<nG;i++){ if(G[i]<gmin) gmin=G[i]; if(G[i]>gmax) gmax=G[i]; }
    if(!(h*gmin>=c && h*gmax<c+m)) okreg=0;
    if(!okreg) continue;
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long k=c-g; int e=nm+1;
    int lgen=1+nG, rgen=e-lgen; long q=(c+m-1)/m; long E=k*lgen+q*rgen-c; long W=(long)e*k-c;
    if(q>11) q=11;
    cnt[h][q]++; double wc=(double)W/c; if(wc<minWc[h][q]) minWc[h][q]=wc; if(E<0) neg[h][q]++; if(E<minE[h][q]) minE[h][q]=E;
    if(W<0) printf("WILF FAIL m=%d c=%ld\n",m,c);
  }
  for(int h=0;h<8;h++) for(int q=0;q<12;q++) if(cnt[h][q]) printf("h=%d q=%d: n=%ld  E<0: %ld  minE=%ld  min W/c=%.4f\n",h,q,cnt[h][q],neg[h][q],minE[h][q],minWc[h][q]);
  return 0; }
