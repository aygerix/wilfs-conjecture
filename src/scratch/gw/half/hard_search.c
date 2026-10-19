/* Adversarial local search: minimize W/c over the hard class (#PF >= j0*m  > e-1).
   State: generator list (m fixed), moves: change/add/remove one generator. Restarts.
   usage: hard_search seed m j0 iters restarts */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[1024]; static int done[1024];
static int m,j0;
/* returns 1 if valid, fills e,t,npf,c,W */
static int eval(int*g,int ng,int*e,int*npf,long*c,long*W,int*K){
  for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
  for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1;
    for(int k=0;k<ng;k++){ int r2=(b+g[k])%m; long v=ap[b]+g[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
  for(int r=0;r<m;r++) if(ap[r]<0) return 0;
  long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r]; *K=M/m;
  int ee=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) ee++; }
  int np=0; for(int r=1;r<m;r++){ int mx=1; for(int s=1;s<m&&mx;s++){ int r2=(r+s)%m; if(ap[r2]==ap[r]+ap[s]) mx=0; } if(mx&&ap[r]-m>=(long)j0*m) np++; }
  long cc=M-m+1,gg=0; for(int r=0;r<m;r++) gg+=ap[r]/m; *e=ee; *npf=np; *c=cc; *W=(long)ee*(cc-gg)-cc; return 1; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+11; m=atoi(argv[2]); j0=atoi(argv[3]); long iters=atol(argv[4]); int rest=atoi(argv[5]);
  double gbest=1e9; int G[16],gb[16]; int ngb=0;
  for(int R=0;R<rest;R++){
    int g[16]; int ng=2+rnd()%5; for(int k=0;k<ng;k++) g[k]=m+1+rnd()%(m*8);
    int e,np,K; long c,W; double cur=1e9;
    if(eval(g,ng,&e,&np,&c,&W,&K)&&np>e-1) cur=(double)W/c;
    for(long it=0;it<iters;it++){
      int h[16]; int nh=ng; for(int k=0;k<ng;k++) h[k]=g[k];
      int mv=rnd()%3;
      if(mv==0||nh>=12) h[rnd()%nh]=m+1+rnd()%(m*8);
      else if(mv==1) h[nh++]=m+1+rnd()%(m*8);
      else if(nh>1){ int k=rnd()%nh; h[k]=h[--nh]; }
      if(rnd()%4==0){ int k=rnd()%nh; h[k]+= (int)(rnd()%7)-3; if(h[k]<=m) h[k]=m+1; }
      if(!eval(h,nh,&e,&np,&c,&W,&K)) continue;
      double val = (np>e-1)? (double)W/c : 1e9;
      if(val<=cur){ cur=val; ng=nh; for(int k=0;k<nh;k++) g[k]=h[k]; }
    }
    if(cur<gbest){ gbest=cur; ngb=ng; for(int k=0;k<ng;k++) gb[k]=g[k]; }
  }
  int e,np,K; long c,W; eval(gb,ngb,&e,&np,&c,&W,&K);
  printf("m=%d j0=%d  min W/c over hard class = %.4f  (W=%ld c=%ld e=%d #PF>=%dm=%d K=%d) gens:",m,j0,gbest,W,c,e,j0,np,K);
  for(int k=0;k<ngb;k++) printf(" %d",gb[k]); printf("\n"); return 0; }
