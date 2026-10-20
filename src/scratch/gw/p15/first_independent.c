/* Independent literal-count C confirmation of P15's first witnesses. */
#include <stdio.h>
#include <limits.h>
static long long C(long long y,int p){long long out=0;for(long long z=p;z<=y;z+=14)out++;return out;}
static void run(int*g,int e){
 long long w[14];int used[14]={0};for(int i=0;i<14;i++)w[i]=LLONG_MAX/4;w[0]=0;
 for(int it=0;it<14;it++){
  int j=-1;for(int i=0;i<14;i++)if(!used[i]&&(j<0||w[i]<w[j]))j=i;
  used[j]=1;for(int a=1;a<e;a++){int k=(j+g[a])%14;if(w[k]>w[j]+g[a])w[k]=w[j]+g[a];}
 }
 long long M=0,ell=0;for(int i=0;i<14;i++)if(w[i]>M)M=w[i];
 for(int i=0;i<14;i++)ell+=(M-w[i])/14;
 printf("GENS");for(int a=0;a<e;a++)printf(" %d",g[a]);printf("\nAP");for(int i=0;i<14;i++)printf(" %lld",w[i]);printf("\nM=%lld c=%lld pstar=%lld ell=%lld W=%lld\n",M,M-13,M%14+1,ell,e*ell-(M-13));
 for(int p=1;p<=14;p++){
  long long sum=0;for(int i=0;i<14;i++){
   long long x=w[i],k=C(x,p);
   for(int a=1;a<e;a++){int nu=0;while(x-(nu+1)*g[a]>=0&&w[(x-(nu+1)*g[a])%14]<=x-(nu+1)*g[a])nu++;if(nu)k-=nu*(C(x,p)-C(x-g[a],p));}
   sum+=k;
  }
  if(sum>14-e)printf("T1FAIL p=%d sumK=%lld bound=%d\n",p,sum,14-e);
 }
}
int main(void){int a[]={14,22,23,57,61,62,63},b[]={14,22,23,61,62,63,71};run(a,7);run(b,7);return 0;}
