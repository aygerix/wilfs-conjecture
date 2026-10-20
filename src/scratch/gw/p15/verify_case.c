/* Generic independent literal-count check. Input: e, then minimal generators.
 * All shifts if m<=60; otherwise true shift only. Fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
static int m;
static long long C(long long y,int p){long long out=0;for(long long z=p;z<=y;z+=m)out++;return out;}
int main(void){int e;if(scanf("%d",&e)!=1)return 2;long long*g=calloc(e,sizeof(long long));for(int i=0;i<e;i++)scanf("%lld",g+i);m=g[0];long long*w=malloc(m*sizeof(long long));int*used=calloc(m,sizeof(int));for(int i=0;i<m;i++)w[i]=LLONG_MAX/4;w[0]=0;
 for(int z=0;z<m;z++){int u=-1;for(int i=0;i<m;i++)if(!used[i]&&(u<0||w[i]<w[u]))u=i;if(w[u]==LLONG_MAX/4)return 3;used[u]=1;for(int a=1;a<e;a++){int j=(u+g[a])%m;if(w[j]>w[u]+g[a])w[j]=w[u]+g[a];}}
 long long M=0,ell=0,LT=0;for(int i=0;i<m;i++)if(w[i]>M)M=w[i];for(int i=0;i<m;i++)ell+=(M-w[i])/m;
 for(int a=1;a<e;a++){if(w[g[a]%m]!=g[a]){puts("NON_AP_GENERATOR");return 4;}for(int b=1;b<e;b++)if(a!=b&&g[a]>=g[b]&&w[(g[a]-g[b])%m]<=g[a]-g[b]){puts("NON_MIN_GENERATOR");return 4;}}
 for(int i=0;i<m;i++)for(int a=1;a<e;a++){long long t=w[i];while(w[(t+g[a])%m]==t+g[a])t+=g[a];LT+=(M-t)/m;}
 printf("VERIFIED m=%d e=%d M=%lld c=%lld genus=%lld pstar=%lld ell=%lld Lambda=%lld W=%lld\n",m,e,M,M-m+1,M-m+1-ell,M%m+1,ell,LT,e*ell-(M-m+1));
 if(m<=60){printf("AP");for(int i=0;i<m;i++)printf(" %lld",w[i]);puts("");}
 int ps=M%m+1;for(int p=1;p<=m;p++){if(m>60&&p!=ps)continue;long long sum=0;
  for(int i=0;i<m;i++){long long x=w[i],k=C(x,p);for(int a=1;a<e;a++){int nu=0;while(x-(nu+1)*g[a]>=0&&w[(x-(nu+1)*g[a])%m]<=x-(nu+1)*g[a])nu++;if(nu)k-=nu*(C(x,p)-C(x-g[a],p));}sum+=k;}
  if(sum>m-e||p==ps)printf("SHIFT p=%d sumK=%lld bound=%d excess=%lld%s\n",p,sum,m-e,sum-(m-e),p==ps?" TRUE":"");
 }
 return 0;
}
