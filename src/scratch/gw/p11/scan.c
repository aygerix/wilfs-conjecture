/* P11 first falsification: q=4 BULK0 and HIGH-RC. Run on fejer only.
 * Semigroup-tree recursion follows the project's checked tree convention. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static int G;
static uint64_t nodes[40],q4=0,sparse=0,fail[2][6];
static int ming[2][6];
static int64_t worst[2][6];
static inline int gap(u128 g,int n){return n>=0&&n<128&&((g>>n)&1);}
static void record(int cls,int cand,int genus,int m,int c,int*gens,int e,int64_t val,int64_t C2){
 if(val<=0)return;fail[cls][cand]++;
 if(genus<ming[cls][cand]||val>worst[cls][cand]){
  if(genus<ming[cls][cand])ming[cls][cand]=genus;
  if(val>worst[cls][cand])worst[cls][cand]=val;
  printf("FAIL cls=%d cand=%d genus=%d m=%d c=%d e=%d val=%lld C2=%lld gens=",cls,cand,genus,m,c,e,(long long)val,(long long)C2);
  for(int a=0;a<e;a++)printf("%s%d",a?",":"",gens[a]);puts("");fflush(stdout);
 }
}
static void visit(u128 gm,int F,int m,int*gens,int e,int genus){
 nodes[genus]++;
 if(e>=3&&F>=0&&3*m<F+1&&F+1<=4*m){
  int w[128],M=0,n[128],d=0;for(int i=0;i<m;i++){int v=i;while(gap(gm,v))v+=m;w[i]=v;if(v>M)M=v;}
  for(int a=0;a<e;a++)if(gens[a]!=m)n[d++]=gens[a];
  int64_t C2=(int64_t)m*(m-1)/2,con[128]={0},Rc[128]={0},lay[5]={0};
  for(int i=0;i<m;i++)for(int a=0;a<d;a++){
   int t=w[i];while(t+n[a]<=M&&w[(t+n[a])%m]==t+n[a])t+=n[a];
   con[i]+=(M-w[i])%m-(M-t);Rc[a]+=(M-w[i])%n[a];
  }
  for(int i=0;i<m;i++)lay[(M-w[i])/m]+=con[i];
  int64_t bulk=lay[1]+lay[2]+lay[3],high=0,highB=0,pw=0,decpos=0;
  for(int i=1;i<m;i++)if(con[i]>0){pw+=con[i];int primitive=0;for(int a=0;a<d;a++)primitive|=w[i]==n[a];if(!primitive)decpos+=con[i];}
  for(int a=0;a<d;a++){if(n[a]>=2*m&&C2-Rc[a]>high)high=C2-Rc[a];if(n[a]>=F+1-2*m&&C2-Rc[a]>highB)highB=C2-Rc[a];}
  q4++;if(3*e<m)sparse++;
  int64_t v[6]={bulk,high,highB,pw-(C2-con[0]),decpos,lay[1]+lay[2]};
  for(int k=0;k<6;k++){record(0,k,genus,m,F+1,gens,e,v[k],C2);if(3*e<m)record(1,k,genus,m,F+1,gens,e,v[k],C2);}
 }
 if(genus==G)return;
 int ng[128];
 for(int j=0;j<e;j++){
  int nn=gens[j];if(nn<=F)continue;u128 gm2=gm|((u128)1<<nn);int e2=0,m2;
  if(nn==m){m2=m+1;for(int k=m2;k<2*m2;k++)ng[e2++]=k;}
  else{m2=m;for(int k=0;k<e;k++)if(gens[k]!=nn)ng[e2++]=gens[k];int y=nn+m,dec=0;for(int a=m;a<=y/2&&!dec;a++)if(a!=nn&&y-a!=nn&&!gap(gm2,a)&&!gap(gm2,y-a))dec=1;if(!dec)ng[e2++]=y;}
  visit(gm2,nn,m2,ng,e2,genus+1);
 }
}
int main(int argc,char**argv){G=argc>1?atoi(argv[1]):33;if(G>33)return 2;for(int c=0;c<2;c++)for(int k=0;k<6;k++)ming[c][k]=99;int gen=1;visit(0,-1,1,&gen,1,0);uint64_t all=0;for(int j=0;j<=G;j++)all+=nodes[j];printf("DONE G=%d all=%llu q4=%llu sparse=%llu\n",G,(unsigned long long)all,(unsigned long long)q4,(unsigned long long)sparse);for(int c=0;c<2;c++)for(int k=0;k<6;k++)printf("CAND cls=%d k=%d fail=%llu min_genus=%d max_violation=%lld\n",c,k,(unsigned long long)fail[c][k],ming[c][k],(long long)worst[c][k]);return 0;}
