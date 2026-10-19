/* min W = e*ell - c over all S of genus <= G, tabulated by (m, e); also min over e = m-1 and e = m.  usage: minw G */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
#define PM 128
static int G; static long minW[PM][PM]; static double minR[PM][PM]; static long cntme[PM][PM];
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  if(m>1){ int c=F+1; int ell=0; for(int x=0;x<c;x++) if(!gapq(gm,x)) ell++; long W=(long)e*ell-c; cntme[m][e]++;
    if(W<minW[m][e]) minW[m][e]=W; double R=(double)W/c; if(R<minR[m][e]) minR[m][e]=R; }
  if(genus==G) return; int ng[PM*2];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); for(int i=0;i<PM;i++) for(int j=0;j<PM;j++){ minW[i][j]=1L<<40; minR[i][j]=1e9; }
  int gens[]={1}; visit(0,-1,1,gens,1,0);
  printf("genus<=%d: min W by m (rows) and e (cols 2..min(m,14)); '.' = none\n",G);
  for(int m=2;m<=G+1&&m<PM;m++){ printf("m=%2d:",m); for(int e=2;e<=m&&e<=14;e++){ if(cntme[m][e]) printf(" %3ld",minW[m][e]); else printf("   ."); } printf("   | e=m-1: %ld  e=m: %ld\n", cntme[m][m-1]?minW[m][m-1]:-999, cntme[m][m]?minW[m][m]:-999); }
  return 0; }
