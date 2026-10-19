/* Exact finite exceptional profile: a=6,m=74,rho=0 or1,
 * q2=0,q3=20,u3=k=0,u4=47. Fejer only, nice.
 * All weights n=m+t are distinct. Enumerate every possible omitted AA.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
static int m=74,h,rho,L,u,v,t[6],best;
static uint64_t nodes,pairsets,eligible,topsets;
static u128 bit(int r){return (u128)1<<r;}
static int pop(u128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
static int forbidden(int i,int j,int k){
 int x[6]={0};x[i]++;x[j]++;x[k]++;
 return u==v?x[u]>=2:(x[u]&&x[v]);
}
static void leaf(u128 seen){
 pairsets++;int good=0,hastop=0;u128 cover=seen;
 for(int i=0;i<6;i++)for(int j=i;j<6;j++)for(int k=j;k<6;k++){
  if(forbidden(i,j,k))continue;
  int T=t[i]+t[j]+t[k];if(T>L)continue;
  if(T<h){fprintf(stderr,"unexpected low cubic\n");exit(3);}
  good++;cover|=bit(T%m);if(T==L)hastop=1;
 }
 if(good<47)return;eligible++;
 if(!hastop)return;topsets++;
 int holes=m-pop(cover);
 printf("CASE rho=%d missing_pair=%d,%d holes=%d eligible_cubics=%d t=",rho,u,v,holes,good);
 for(int i=0;i<6;i++)printf("%s%d",i?",":"",t[i]);printf("\n");
 if(holes<best){
  best=holes;printf("BEST rho=%d missing_pair=%d,%d holes=%d eligible_cubics=%d t=",rho,u,v,holes,good);
  for(int i=0;i<6;i++)printf("%s%d",i?",":"",t[i]);printf("\n");fflush(stdout);
 }
 if(!holes){printf("COUNTEREXAMPLE_CANDIDATE\n");fflush(stdout);exit(2);}
}
static void dfs(int depth,int next,u128 seen){
 nodes++;
 if(depth==6){leaf(seen);return;}
 for(int x=next;x<=h-1-(5-depth);x++){
  int r=x%m;if(seen&bit(r))continue;u128 add=bit(r);int ok=1;
  for(int j=0;j<=depth;j++){
   if(j==u&&depth==v)continue;
   int s=x+(j==depth?x:t[j]);
   if(s<h){ok=0;break;}
   r=s%m;if((seen|add)&bit(r)){ok=0;break;}add|=bit(r);
  }
  if(!ok||((seen|add)&bit(h-1)))continue;
  t[depth]=x;dfs(depth+1,x+1,seen|add);
 }
}
int main(void){
 for(rho=0;rho<=1;rho++){
  h=m-rho;L=m+h-1;best=m;nodes=pairsets=eligible=topsets=0;
  for(u=0;u<6;u++)for(v=u;v<6;v++){
   int first=(u==0&&v==0)?1:(h+1)/2;dfs(0,first,bit(0));
  }
  printf("SUMMARY m=%d rho=%d nodes=%llu pairsets=%llu eligible=%llu top_eligible=%llu minholes=%d W=%d\n",m,rho,(unsigned long long)nodes,(unsigned long long)pairsets,(unsigned long long)eligible,(unsigned long long)topsets,best,-2+rho);fflush(stdout);
 }
}
