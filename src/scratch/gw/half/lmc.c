/* LMC on random semigroups: sum_r min(i,kappa_r) <= sum_r sum_{k<=d} min(i, h_k(r)),
   h_k(r) = k-th largest floor((w_f - w_r)/m) over maximal w_f with w_r <=_S w_f. Also LW (d*h_1) and MC for comparison.
   usage: lmc seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static int cmpd(const void*a,const void*b){ long x=*(long*)a,y=*(long*)b; return x>y?-1:x<y; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+17; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[512]; static int done[512]; static int ismax[512]; int gens[8];
  long n=0,fL=0,fLW=0,fMC=0, nt=0;
  for(long tt=0;tt<trials;tt++){
    int m=mmin+rnd()%(mmax-mmin+1); int ng=1+rnd()%6; int span=m*(2+rnd()%8); for(int k=0;k<ng;k++) gens[k]=m+1+rnd()%span;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1;
      for(int k=0;k<ng;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r]; int K=M/m;
    int e=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) e++; }
    int d=e-1; int t=0; long V[512];
    for(int r=1;r<m;r++){ int mx=1; for(int s=1;s<m&&mx;s++){ int r2=(r+s)%m; if(ap[r2]==ap[r]+ap[s]) mx=0; } ismax[r]=mx; if(mx) V[t++]=ap[r]; }
    ismax[0]=(m==1); n++; if(t>d) nt++;
    qsort(V,t,sizeof(long),cmpd);
    for(int i=1;i<=K;i++){
      long L=0,Rl=0,Rlw=0,Rmc=0;
      for(int r=0;r<m;r++){ long k1=ap[r]/m; L+=k1<i?k1:i;
        long h[512]; int nh=0;
        for(int f=1;f<m;f++) if(ismax[f]){ long dlt=ap[f]-ap[r]; if(dlt<0) continue; int cl=((f-r)%m+m)%m; if(ap[cl]<=dlt) h[nh++]=dlt/m; }
        qsort(h,nh,sizeof(long),cmpd);
        for(int k=0;k<d&&k<nh;k++) Rl+= h[k]<i?h[k]:i;
        if(nh>0) Rlw+= (long)d*(h[0]<i?h[0]:i);
        for(int k=0;k<d&&k<t;k++){ long l1=(V[k]-ap[r]); l1=l1>=0?l1/m:0; Rmc+= l1<i?l1:i; }
      }
      if(L>Rl){ fL++; if(fL<=4) printf("LMC FAIL i=%d K=%d m=%d e=%d t=%d L=%ld R=%ld\n",i,K,m,e,t,L,Rl); break; }
    }
    /* full (i=K) LW and MC */
    { int i=K; long L=0,Rlw=0,Rmc=0; for(int r=0;r<m;r++){ long k1=ap[r]/m; L+=k1; long best=-1;
        for(int f=1;f<m;f++) if(ismax[f]){ long dlt=ap[f]-ap[r]; if(dlt<0) continue; int cl=((f-r)%m+m)%m; if(ap[cl]<=dlt && dlt/m>best) best=dlt/m; }
        if(best>0) Rlw+=(long)d*best; for(int k=0;k<d&&k<t;k++){ long l1=(V[k]-ap[r]); l1=l1>=0?l1/m:0; Rmc+=l1; } }
      if(L>Rlw) fLW++; if(L>Rmc) fMC++; (void)i; }
  }
  printf("semigroups %ld (t>d: %ld) | LMC (some i) fails %ld | LW fails %ld | MC fails %ld\n",n,nt,fL,fLW,fMC);
  return 0; }
