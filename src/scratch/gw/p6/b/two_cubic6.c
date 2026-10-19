/* Full Q in k=6, two cubics with two-pair shadow: the remaining finite
 * base m=43..45. Exact prefix enumeration of all full quadratic labelings.
 * fejer only, nice single-core. */
#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
typedef unsigned long long ull;
typedef long long ll;
static int m,P[6],pair[6][6];
static ull nodes,bases,instances,phases;static ll minS;
static void leaf(ull used){
 bases++;
 for(int i=0;i<6;i++)for(int j=0;j<6;j++)if(i!=j){
  for(int type=0;type<2;type++){
   if(type==0&&j<i)continue;
   int u=(3*P[i])%m,v=type? (2*P[i]+P[j])%m:(3*P[j])%m;
   if(u==v||(used>>u&1)||(used>>v&1))continue;
   instances++;
   int n1=pair[i][i],n2=type?pair[i][j]:pair[j][j];
   for(int sig=0;sig<m;sig++){
    ll sn=(m-sig)%m,sa=0;
    for(int a=0;a<6;a++)sn+=(P[a]+m-sig)%m;
    for(int a=0;a<6;a++)for(int b=a;b<6;b++){
     int r=(P[a]+P[b])%m,pos=(r+m-sig)%m;
     if(pair[a][b]==n1||pair[a][b]==n2)sn+=pos;else sa+=pos;
    }
    ll S=(m-23)*sn-sa-2*((u+m-sig)%m)-2*((v+m-sig)%m);
    if(S<0){
     printf("MAXCL_COUNTEREXAMPLE m=%d P=",m);for(int a=0;a<6;a++)printf("%d,",P[a]);
     printf(" T=3e%d,type%d(i=%d,j=%d) sigma=%d S=%lld\n",i,type,i,j,sig,S);exit(2);
    }
    phases++;if(S<minS)minS=S;
   }
  }
 }
}
static void rec(int n,int start,ull used){
 nodes++;
 if(n==6){leaf(used);return;}
 for(int x=start;x<=m-(6-n);x++){
  if(used>>x&1)continue;
  ull extra=1ULL<<x;int good=1;
  int a=(2*x)%m;
  if((used|extra)>>a&1)continue;
  extra|=1ULL<<a;
  for(int i=0;i<n;i++){
   a=(x+P[i])%m;if((used|extra)>>a&1){good=0;break;}extra|=1ULL<<a;
  }
  if(good){P[n]=x;rec(n+1,x+1,used|extra);}
 }
}
int main(void){
 int id=0;for(int a=0;a<6;a++)for(int b=a;b<6;b++)pair[a][b]=pair[b][a]=id++;
 for(m=43;m<=45;m++){
  nodes=bases=instances=phases=0;minS=1LL<<60;rec(0,1,1);
  printf("TWO_CUBIC6 m=%d nodes=%llu bases=%llu injections=%llu phases=%llu min=%lld FAILURES=0\n",m,nodes,bases,instances,phases,minS);fflush(stdout);
 }
 printf("TWO_CUBIC6_PASS\n");return 0;
}
