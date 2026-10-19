/* Test Marashdeh's Conj 5.2 (arXiv:2608.12531): if t>=e, d=t+1-e: Theta >= sum_{i<=d} lambda_S(f_i),
   Theta = sum_{gaps x}(nu(x)-1), nu(x)=#{f in PF: f-x in S}, lambda_S(y)=|S cap [0,y]|, f_1<...<f_t.
   Random semigroups m in [mmin,mmax]. usage: marashdeh seed trials mmin mmax cmax */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static int cmp(const void*a,const void*b){ long x=*(long*)a,y=*(long*)b; return x<y?-1:x>y; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+13; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); long cmax=atol(argv[5]);
  static long ap[512]; static int done[512]; int gens[8]; static long pf[512];
  long n_te=0,fails=0,n_all=0,topfail=0; double worstunc=0; double worst=1e18;
  for(long tt=0;tt<trials;tt++){
    int m=mmin+rnd()%(mmax-mmin+1); int ng=1+rnd()%6; int span=m*(2+rnd()%8);
    for(int k=0;k<ng;k++) gens[k]=m+1+rnd()%span;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1;
      for(int k=0;k<ng;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r]; long F=M-m; long c=F+1; if(c>cmax||c<=0) continue;
    int e=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) e++; }
    int t=0; for(int r=1;r<m;r++){ int mx=1; for(int s=1;s<m&&mx;s++){ int r2=(r+s)%m; if(ap[r2]==ap[r]+ap[s]) mx=0; } if(mx) pf[t++]=ap[r]-m; }
    n_all++; if(t<e) continue; n_te++;
    qsort(pf,t,sizeof(long),cmp);
    long Theta=0;
    for(long x=1;x<=F;x++){ if(x>=ap[x%m]) continue; /* x in S */ int nu=0; for(int k=0;k<t;k++){ long y=pf[k]-x; if(y>=0 && y>=ap[y%m]) nu++; } Theta+=nu-1; }
    int dd=t+1-e; long rhs=0; for(int i=0;i<dd;i++){ long y=pf[i]; long cnt=0; for(int r=0;r<m;r++) if(ap[r]<=y) cnt+=(y-ap[r])/m+1; rhs+=cnt; }
    /* top-d covering: every gap covered by one of the e-1 largest PF numbers */
    { int dtop=e-1; long unc=0; for(long x=1;x<=F;x++){ if(x>=ap[x%m]) continue; int cv=0; for(int k=t-1;k>=t-dtop&&k>=0&&!cv;k--){ long y=pf[k]-x; if(y>=0&&y>=ap[y%m]) cv=1; } if(!cv) unc++; }
      if(unc>0){ topfail++; if(unc*1.0/c>worstunc) worstunc=unc*1.0/c; if(topfail<=3){ printf("TOPCOVER FAIL m=%d e=%d t=%d c=%ld uncovered=%ld gens:",m,e,t,c,unc); for(int k=0;k<ng;k++) printf(" %d",gens[k]); printf("\n"); } } }
    double marg=(double)(Theta-rhs)/c; if(marg<worst) worst=marg;
    if(Theta<rhs){ fails++; if(fails<=6){ printf("CONJ5.2 FAIL m=%d e=%d t=%d c=%ld Theta=%ld rhs=%ld gens:",m,e,t,c,Theta,rhs); for(int k=0;k<ng;k++) printf(" %d",gens[k]); printf("\n"); } }
  }
  printf("seed=%s sampled=%ld with t>=e: %ld  Conj5.2 fails: %ld  min (Theta-rhs)/c = %.4f | top-d covering fails: %ld (max uncovered/c %.3f)\n",argv[1],n_all,n_te,fails,worst,topfail,worstunc);
  return 0; }
