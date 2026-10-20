/* Semigroup-tree test of the NEW UF top-budget conjecture, q exactly four.
 * The standard remove-an-effective-generator recursion is adapted from the
 * lead's m3_tree2.c. No genus computation is done locally. */
#include "core.h"
typedef unsigned __int128 u128;
static int G;static unsigned long long total,q4,topbad;static ll mintop=LLONG_MAX;
static int gap(u128 g,int x){return x<128&&((g>>x)&1);}
static void visit(u128 gm,int F,int m,int*gens,int e,int genus){
 total++;
 if(m>=2&&F+1>3*m&&F+1<=4*m){ll w[MM];for(int i=0;i<m;i++){int x=i;while(gap(gm,x))x+=m;w[i]=x;}Res r;evaluate(m,w,&r);q4++;
  if(r.TopSlack<mintop){mintop=r.TopSlack;dump("TOP_RECORD",&r,w);}
  if(r.CuSlack<0||r.PlusSlack<0||r.PoorSlack<0||r.nmfpoor){dump("COUNTEREXAMPLE",&r,w);exit(2);}
  if(r.TopSlack<0){topbad++;if(topbad<=3)dump("TOP_COUNTEREXAMPLE",&r,w);}
 }
 if(genus==G)return;int ng[128];
 for(int j=0;j<e;j++){int n=gens[j];if(n<=F)continue;u128 g2=gm|((u128)1<<n);int e2=0,m2;
  if(n==m){m2=m+1;for(int k=m2;k<2*m2;k++)ng[e2++]=k;}
  else{m2=m;for(int k=0;k<e;k++)if(gens[k]!=n)ng[e2++]=gens[k];int y=n+m,dec=0;for(int a=m;a<=y/2&&!dec;a++)if(a!=n&&!gap(g2,a)&&y-a!=n&&!gap(g2,y-a))dec=1;if(!dec)ng[e2++]=y;}
  visit(g2,n,m2,ng,e2,genus+1);
 }
}
int main(int argc,char**argv){G=argc>1?atoi(argv[1]):27;if(G>50)return 4;int a[1]={1};visit(0,-1,1,a,1,0);printf("SUMMARY G=%d total=%llu q4=%llu minTOP=%lld topfail=%llu\n",G,total,q4,mintop,topbad);}
