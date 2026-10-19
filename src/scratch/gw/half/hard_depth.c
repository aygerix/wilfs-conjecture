/* In the hard class (#PF>=3m > e-1), test per-depth and tail inequalities:
   D_j: |U_j| <= d|L_j| (per depth), for j>=3;  T_j: sum_{k>=j}|U_k| <= d sum_{k>=j}|L_k| (tail from j), j=3;
   also R: sum_{j>=3} |U_j| <= sum_{j>=3} min(pi_j, d)|L_j| + slack(P_2)  (i.e. Wilf via GW-PF capped + P2 slack)
   usage: hard_depth seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+5; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[512]; static int done[512]; int gens[8]; static int ismax[512];
  long nH=0,fD=0,fT=0,fR=0,fT2=0; 
  for(long tt=0;tt<trials;tt++){
    int m=mmin+rnd()%(mmax-mmin+1); int ng=1+rnd()%6; int span=m*(2+rnd()%10);
    for(int k=0;k<ng;k++) gens[k]=m+1+rnd()%span;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1;
      for(int k=0;k<ng;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r]; int K=M/m; if(K<3) continue;
    int e=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) e++; }
    int d=e-1, npf3=0; for(int r=1;r<m;r++){ int mx=1; for(int s=1;s<m&&mx;s++){ int r2=(r+s)%m; if(ap[r2]==ap[r]+ap[s]) mx=0; } ismax[r]=mx; if(mx&&ap[r]-m>=3L*m) npf3++; }
    if(npf3<=d) continue; nH++;
    long U[128]={0},L[128]={0},pi[128]={0};
    for(int r=0;r<m;r++){ long k1=ap[r]/m,l1=(M-ap[r])/m; for(int j=1;j<=k1&&j<128;j++) U[j]++; for(int j=1;j<=l1&&j<128;j++) L[j]++; }
    for(int r=1;r<m;r++) if(ismax[r]){ long f=ap[r]-m; for(int j=1;j<=K;j++) if(f>=(long)(j-1)*m) pi[j]++; }
    int bad=0; for(int j=3;j<=K;j++) if(U[j]>(long)d*L[j]) bad=1; if(bad) fD++;
    long su=0,sl=0; for(int j=3;j<=K;j++){ su+=U[j]; sl+=L[j]; } if(su>(long)d*sl) fT++;
    long s2=(long)d*(L[1]+L[2])-(U[1]+U[2]); long rhs=s2; for(int j=3;j<=K;j++) rhs+=(pi[j]<d?pi[j]:d)*L[j]; if(su>rhs) fR++;
    /* tail from the middle */
    int jm=(K+2)/2; long su2=0,sl2=0; for(int j=jm+1;j<=K;j++){su2+=U[j]; sl2+=L[j];} if(su2>(long)d*sl2) fT2++;
  }
  printf("hard class: %ld | per-depth j>=3 fails: %ld | tail(j>=3) fails: %ld | capped-PF+P2slack fails: %ld | top-half tail fails: %ld\n",nH,fD,fT,fR,fT2);
  return 0; }
