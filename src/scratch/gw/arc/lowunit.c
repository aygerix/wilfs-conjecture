/* Primary regime 3m<c<=4m, a = #gens in (m,c-2m) >= AMIN, with at least one low unit (2n < c-m).
   Report min W/c by alpha = #low units, and examples. usage: lowunit seed trials mmin mmax AMIN */
#include <stdio.h>
#include <stdlib.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]),AMIN=atoi(argv[5]);
  static long ap[4096]; static int done[4096]; static int gens[64]; static long mg[4096];
  double minr[32]; long nn[32]; for(int i=0;i<32;i++){minr[i]=1e9;nn[i]=0;}
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1);
    int ng=AMIN+rnd()%10; int g0=0;
    int nlow=1+rnd()%3;
    for(int k=0;k<ng;k++){ int gv; if(k<nlow) gv=m+1+rnd()%(m/2); else gv=m+m/3+rnd()%(2*m/3); gens[g0++]=gv; }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(!(c>3*m&&c<=4*m)) continue;
    int nm=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) mg[nm++]=ap[r]; }
    int a=0,al=0; for(int i=0;i<nm;i++){ if(mg[i]<c-2*m){ a++; if(2*mg[i]<c-m) al++; } }
    if(a<AMIN||al<1) continue;
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long l=c-g; long W=(long)(nm+1)*l-c;
    double rr=(double)W/c; int key=al<31?al:31; nn[key]++; if(rr<minr[key]){ minr[key]=rr; }
    if(W<0) printf("WILF FAIL m=%d c=%ld\n",m,c);
  }
  printf("seed=%s:",argv[1]); for(int i=0;i<32;i++) if(nn[i]) printf(" alpha=%d n=%ld minW/c=%.3f |",i,nn[i],minr[i]); printf("\n");
  return 0; }
