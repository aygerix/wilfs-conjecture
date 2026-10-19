/* Random semigroups (m in [mmin,mmax]); hard class H = {#PF >= 3m  > e-1}.
   Report distribution of normalized Wilf slack W/c, type t, e, and the 10 tightest members of H.
   usage: hard_class seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
typedef struct { double r; int m,e,t,K; long c,g,W; int ng; int gens[8]; } rec;
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+7; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[512]; static int done[512]; int gens[8];
  rec best[10]; int nb=0; long nH=0,nAll=0; long hist[11]={0}, histAll[11]={0};
  for(long tt=0;tt<trials;tt++){
    int m=mmin+rnd()%(mmax-mmin+1); int ng=1+rnd()%6; int span=m*(2+rnd()%10);
    for(int k=0;k<ng;k++) gens[k]=m+1+rnd()%span;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1;
      for(int k=0;k<ng;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r]; int K=M/m; if(K<3) continue;
    int e=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) e++; }
    int t=0,npf3=0; for(int r=1;r<m;r++){ int mx=1; for(int s=1;s<m&&mx;s++){ int r2=(r+s)%m; if(ap[r2]==ap[r]+ap[s]) mx=0; } if(mx){ t++; if(ap[r]-m>=3L*m) npf3++; } }
    long c=M-m+1, g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long l=c-g; long W=(long)e*l-c;
    double rr=(double)W/c; int bin=(int)(rr*10); if(bin>10) bin=10; if(bin<0) bin=0;
    nAll++; histAll[bin]++;
    if(npf3>e-1){ nH++; hist[bin]++;
      rec R; R.r=rr; R.m=m; R.e=e; R.t=t; R.K=K; R.c=c; R.g=g; R.W=W; R.ng=ng; for(int k=0;k<ng;k++) R.gens[k]=gens[k];
      if(nb<10){ best[nb++]=R; } else { int w=0; for(int k=1;k<10;k++) if(best[k].r>best[w].r) w=k; if(R.r<best[w].r) best[w]=R; } }
  }
  printf("all K>=3: %ld   hard class (#PF>=3m > e-1): %ld\n",nAll,nH);
  printf("W/c histogram (bins of 0.1)  all:"); for(int b=0;b<=10;b++) printf(" %ld",histAll[b]); printf("\n");
  printf("                              hard:"); for(int b=0;b<=10;b++) printf(" %ld",hist[b]); printf("\n");
  for(int k=0;k<nb;k++){ rec*R=&best[k]; printf("tight hard: W/c=%.4f W=%ld c=%ld m=%d e=%d t=%d K=%d gens: %d",R->r,R->W,R->c,R->m,R->e,R->t,R->K,R->m); for(int j=0;j<R->ng;j++) printf(" %d",R->gens[j]); printf("\n"); }
  return 0; }
