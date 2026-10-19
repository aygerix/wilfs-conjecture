/* Adaptation of arc/arc_mixed.c, constructs and checks actual lex tiles. */
#include "p5_check.h"
static unsigned long long st;
static unsigned long long rnd(void){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
int main(int argc,char**argv){
 assert(argc==5);st=strtoull(argv[1],0,10)*2654435761ULL+1;
 long trials=atol(argv[2]);int lo=atoi(argv[3]),hi=atoi(argv[4]);assert(hi<PMAX);
 for(long it=0;it<trials;it++){
  int m=lo+rnd()%(hi-lo+1),ng=2+rnd()%14,gens[64],ap[PMAX],done[PMAX]={0};
  for(int j=0;j<ng;j++){
   int mode=rnd()%5,l,h;
   if(mode<2){l=m+m/3+rnd()%(m/2+1);h=2*m;}
   else if(mode==2){l=m+1;h=2*m;}
   else if(mode==3){l=2*m;h=3*m;}else{l=3*m;h=5*m;}
   if(h<=l)h=l+1;gens[j]=l+rnd()%(h-l);
  }
  for(int r=0;r<m;r++)ap[r]=-1;ap[0]=0;
  for(int j=0;j<m;j++){
   int rr=-1;for(int r=0;r<m;r++)if(!done[r]&&ap[r]>=0&&(rr<0||ap[r]<ap[rr]))rr=r;
   if(rr<0)break;done[rr]=1;
   for(int k=0;k<ng;k++){int r2=(rr+gens[k])%m,v=ap[rr]+gens[k];if(ap[r2]<0||v<ap[r2])ap[r2]=v;}
  }
  int ok=1,M=0;for(int r=0;r<m;r++){if(ap[r]<0)ok=0;if(ap[r]>M)M=ap[r];}
  if(!ok||M/m!=4)continue;
  int n[PMAX],d=0,X[PMAX*PMAX]={0},ready[PMAX]={0};ready[0]=1;
  for(int r=1;r<m;r++){
   int dec=0;for(int s=1;s<m;s++){int r2=(r-s+m)%m;if(r2&&ap[s]+ap[r2]==ap[r])dec=1;}
   if(!dec)n[d++]=ap[r];
  }
  for(int j=0;j<d;j++)for(int k=j+1;k<d;k++)if(n[k]<n[j]){int x=n[k];n[k]=n[j];n[j]=x;}
  for(int val=1;val<=M;val++){
   int r=val%m;if(ap[r]!=val)continue;int found=0;
   for(int j=0;j<d&&!found;j++)if(val>=n[j]){
    int s=(val-n[j])%m;if(ap[s]==val-n[j]){assert(ready[s]);for(int k=0;k<d;k++)X[r*d+k]=X[s*d+k];X[r*d+j]++;ready[r]=found=1;}
   }
   assert(found);
  }
  for(int r=0;r<m;r++)for(int j=0;j<d;j++)if(X[r*d+j]){
   int s=(ap[r]-n[j])%m;assert(ap[s]==ap[r]-n[j]);
   for(int k=0;k<d;k++)assert(X[s*d+k]==X[r*d+k]-(j==k));
  }
  p5verify(m,d,X,n);
 }
 printf("seed=%s trials=%ld m=%d..%d ",argv[1],trials,lo,hi);p5summary();
}
