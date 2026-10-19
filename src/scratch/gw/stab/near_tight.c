/* Near-equality Wilf semigroups: list all S of genus <= G with W = e*ell - c <= WMAX and 3 <= e <= m-2.
   Prints m, e, c, ell, W, K=ceil(c/m), generators.  usage: near_tight G WMAX */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
#define PM 128
static int G, WMAX; static long cnt, hits; static long byW[64];
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  cnt++;
  if(m>1){ int c=F+1; int ell=0; for(int x=0;x<c;x++) if(!gapq(gm,x)) ell++; long W=(long)e*ell-c;
    if(W<=WMAX && e>=3 && e<=m-2){ hits++; if(W>=0&&W<64) byW[W]++; printf("W=%ld m=%d e=%d c=%d ell=%d K=%d g=%d gens:",W,m,e,c,ell,(c+m-1)/m,genus); for(int j=0;j<e;j++) printf(" %d",gens[j]); printf("\n"); } }
  if(genus==G) return; int ng[PM*2];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); WMAX=atoi(argv[2]); int gens[]={1}; visit(0,-1,1,gens,1,0);
  fprintf(stderr,"genus<=%d all=%ld hits(3<=e<=m-2, W<=%d)=%ld  byW:",G,cnt,WMAX,hits); for(int i=0;i<=WMAX&&i<64;i++) fprintf(stderr," %ld",byW[i]); fprintf(stderr,"\n"); return 0; }
