/* Exhaustive loop-graph verification of PAIR-COVER and the cubic identity.
 * n<=6, every subset of the unordered pairs (loops allowed); fejer only. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
typedef long long I;
static I C2(I n){return n*(n-1)/2;}
static I root(I v){I a=0;while((a+1)*(a+1)<=v)a++;return a;}
static I min0(I a,I b){return a<b?a:b;}
static I max0(I a,I b){return a>b?a:b;}
static I excover(I a,I al,I r,I rll,I k){
 if(!r)return !k&&!rll?0:-1;
 if(r>a*k-C2(k))return -1;
 I out=-1,p=a-al;
 for(I cl=max0(0,k-p);cl<=min0(al,k);cl++){
  if(rll>al*cl-C2(cl))continue;
  if(cl<al)out=max0(out,min0(p,min0(k-cl,min0(r-rll,r-k+1))));
  if(cl){I dl=max0(0,rll-(al*(cl-1)-C2(cl-1))),rem=r-k+1-dl;
   if(rem>=0)out=max0(out,min0(p,min0(r-rll,rem)));
  }
 }
 return out;
}
int main(void){
 for(int n=1;n<=6;n++){
  int bit[6][6],x[21],y[21],q=0,deg[6];uint32_t incident[6]={0},cm[64]={0};
  for(int i=0;i<n;i++)for(int j=i;j<n;j++){bit[i][j]=bit[j][i]=q;x[q]=i;y[q]=j;incident[i]|=1U<<q;incident[j]|=1U<<q;q++;}
  for(int s=1;s<(1<<n);s++){int k=__builtin_ctz((unsigned)s);cm[s]=cm[s^(1<<k)]|incident[k];}
  I total=0,tight=0,shape0=0,maximprove=0;
  for(uint32_t g=0;g<(1U<<q);g++){
   int r=__builtin_popcount(g),F=0,tri=0;
   for(int i=0;i<n;i++)deg[i]=__builtin_popcount(g&incident[i]);
   I J=0;for(int i=0;i<n;i++)J+=C2(deg[i]);I D=C2(r)-J;
   for(int i=0;i<n;i++)for(int j=i;j<n;j++)for(int k=j;k<n;k++){
    uint32_t dv=(1U<<bit[i][j])|(1U<<bit[i][k])|(1U<<bit[j][k]);
    /* A repeated variable does not supply its loop unless its exponent is 2. */
    if(i==j&&j!=k)dv=(1U<<bit[i][i])|(1U<<bit[i][k]);
    if(i!=j&&j==k)dv=(1U<<bit[j][j])|(1U<<bit[i][j]);
    F+=(g&dv)!=0;
    if(i<j&&j<k&&(g&dv)==dv)tri++;
   }
   I z=F-n*r+C2(r);assert(z==D+tri&&z>=0);
   int tau=n;for(int s=0;s<(1<<n);s++)if(!(g&~cm[s])){int t=__builtin_popcount((unsigned)s);if(t<tau)tau=t;}
   assert(C2(tau)<=z);I nu=r?(1+root(1+8*z))/2:0;if(nu>r)nu=r;
   if(r)for(int i=0;i<n;i++)assert(deg[i]<=r-tau+1);
   for(int al=1;al<=n;al++){
    int rll=0,cross=0;
    for(int z0=0;z0<q;z0++)if(g&(1U<<z0)){rll+=x[z0]<al&&y[z0]<al;cross+=x[z0]==0&&y[z0]>=al;}
    assert(cross<=excover(n,al,r,rll,tau));
   }
   assert(tau<=nu);total++;tight+=C2(tau)==z;shape0+=z==0;
   if(r-nu>maximprove)maximprove=r-nu;
  }
  printf("n=%d graphs=%lld tight=%lld shape_zero=%lld max_repair_gain=%lld\n",n,total,tight,shape0,maximprove);fflush(stdout);
 }
}
