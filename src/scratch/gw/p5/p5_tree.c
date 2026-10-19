/* Semigroup tree, genus <= G; verify minimal factorization tiles in K4.
 * Compile/run on fejer. Usage: p4_tree G. Single core, nice.
 */
#include "p5_check.h"
typedef unsigned __int128 u128;
static int G;
static uint64_t cnt;
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
 cnt++;int c=F+1;
 if(c>3*m&&c<=4*m){
  int ap[PMAX],M=0,ng[PMAX],d=0,X[PMAX*PMAX]={0};
  for(int i=0;i<e;i++)if(gens[i]!=m)ng[d++]=gens[i];
  for(int r=0;r<m;r++){int w=r;while(gapq(gm,w))w+=m;ap[r]=w;if(w>M)M=w;}
  /* Least generator removal gives lexicographically largest factorization.
   * By induction its divisors are the same chosen representatives. */
  int ready[PMAX]={0};ready[0]=1;
  for(int w=1;w<=M;w++){
   int r=w%m;if(ap[r]!=w)continue;int found=0;
   for(int j=0;j<d;j++)if(w>=ng[j]){
    int t=(w-ng[j])%m;
    if(ap[t]==w-ng[j]){
     assert(ready[t]);for(int h=0;h<d;h++)X[r*d+h]=X[t*d+h];X[r*d+j]++;ready[r]=found=1;break;
    }
   }
   assert(found);
  }
  /* Check downward closure independently of the representation algorithm. */
  for(int r=0;r<m;r++)for(int j=0;j<d;j++)if(X[r*d+j]){
   int t=(ap[r]-ng[j])%m;assert(ap[t]==ap[r]-ng[j]);
   for(int h=0;h<d;h++)assert(X[t*d+h]==X[r*d+h]-(h==j));
  }
  p5verify(m,d,X,ng);
 }
 if(genus==G)return;
 int ng[PMAX];
 for(int j=0;j<e;j++){
  int n=gens[j];if(n<=F)continue;
  u128 gm2=gm|((u128)1<<n);int e2=0,m2;
  if(n==m){m2=m+1;for(int k=m2;k<=2*m2-1;k++)ng[e2++]=k;}
  else{
   m2=m;for(int k=0;k<e;k++)if(gens[k]!=n)ng[e2++]=gens[k];
   int y=n+m,dec=0;
   for(int a=m;a<=y/2&&!dec;a++)if(!gapq(gm2,a)&&!gapq(gm2,y-a))dec=1;
   if(!dec)ng[e2++]=y;
  }
  visit(gm2,n,m2,ng,e2,genus+1);
 }
}
int main(int argc,char**argv){assert(argc==2);G=atoi(argv[1]);assert(G<40);int gens[]={1};visit(0,-1,1,gens,1,0);printf("genus<=%d all=%llu ",G,(unsigned long long)cnt);p5summary();}
