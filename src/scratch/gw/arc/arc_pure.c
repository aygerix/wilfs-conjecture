/* Test of the pure-A arc theorem. Class: 3m < c <= 4m, every minimal generator other than m is < c-2m (pure A),
   and 2*n1 >= c-m. Claims: (a) h=c-3m <= 2*q3+2 (q3 = #distinct Apery elements that are sums of two generators);
   (b) W >= a-1-(a-4)*rA+3*tA with a=e-1, rA=C(a+1,2)-q3, tA=C(a+2,3)-u4, u4=m-1-a-q3; (c) W >= a-1+6rA.
   usage: arc_pure seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[4096]; static int done[4096]; static int gens[64]; static int isgen[4096]; static long mg[4096]; static char ps[4096];
  long cnt=0,cls=0,fa=0,fb=0,fc=0,fid=0,fsh=0; long minW=1L<<40; int amax=0; long hist[64]={0}; long minslack=1L<<40;
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1);
    int ng=2+rnd()%14;
    int lo=m+m/3+rnd()%(m/2+1); int hi=2*m-1-rnd()%(m/4+1); if(hi<=lo) continue;
    int g0=0; for(int k=0;k<ng;k++) gens[g0++]=lo+rnd()%(hi-lo+1);
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; cnt++;
    if(!(c>3*m && c<=4*m)) continue;
    int nm=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } isgen[r]=!dec; if(!dec) mg[nm++]=ap[r]; }
    int pure=1; long n1=1L<<60; for(int i=0;i<nm;i++){ if(mg[i]>=c-2*m) pure=0; if(mg[i]<n1) n1=mg[i]; }
    if(!pure || 2*n1<c-m) continue;
    cls++; int a=nm; if(a>amax) amax=a; if(a<64) hist[a]++;
    long q3=0; for(int r=0;r<m;r++){ ps[r]=0; if(r==0||isgen[r]) continue; for(int i=0;i<nm&&!ps[r];i++) for(int j=i;j<nm;j++) if(mg[i]+mg[j]==ap[r]){ps[r]=1;break;} if(ps[r]) q3++; }
    long Q=(long)a*(a+1)/2, C3=(long)a*(a+1)*(a+2)/6;
    long rA=Q-q3, u4=m-1-a-q3, tA=C3-u4;
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long l=c-g; long W=(long)(a+1)*l-c;
    long h=c-3*m;
    if(h>2*q3+2){ fa++; if(fa<5) printf("FAIL(a) m=%d c=%ld a=%d q3=%ld\n",m,c,a,q3); }
    long bb=a-1-(a-4)*rA+3*tA; if(W<bb){ fb++; if(fb<5) printf("FAIL(b) m=%d c=%ld a=%d W=%ld bound=%ld\n",m,c,a,W,bb); }
    if(W<a-1+6*rA){ fc++; if(fc<5) printf("FAIL(c) m=%d c=%ld a=%d W=%ld rA=%ld\n",m,c,a,W,rA); }
    { long ident=3L*a*a+4L*a+1+(long)(a-2)*q3-3*u4-h; if(W!=ident){ fid++; if(fid<5) printf("FAIL(identity) m=%d c=%ld a=%d W=%ld ident=%ld\n",m,c,a,W,ident);} }
    if(3*u4>(long)(a+2)*q3) fsh++;
    if(W<minW) minW=W; if(W-bb<minslack) minslack=W-bb;
  }
  printf("seed=%s identity_fails=%ld shadow_fails=%ld sampled=%ld class=%ld fails a/b/c=%ld/%ld/%ld minW=%ld min(W-bound_b)=%ld amax=%d\n",argv[1],fid,fsh,cnt,cls,fa,fb,fc,minW,minslack,amax);
  printf("  a-histogram:"); for(int i=0;i<64;i++) if(hist[i]) printf(" %d:%ld",i,hist[i]); printf("\n");
  return 0; }
