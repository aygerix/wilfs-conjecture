/* Second exact computation of the failed pointwise lower-cover payment. */
#include "core.h"
int main(void){
 ll g[]={10,11,12},w[MM];Res r;apery(8,3,g,w);evaluate(8,w,&r);dump("LOCAL_COUNTER",&r,w);
 for(int v=22;v<=33;v+=11){
  ll E=-v,EU=-v,P=0,L=0;
  for(int a=0;a<3;a++){
   int k=0;ll z=v;
   while(z>=g[a]&&w[(z-g[a])%8]==z-g[a]){k++;z-=g[a];}
   E+=k*g[a];if(k){EU+=g[a];P+=k*(((r.M-v+g[a])%8)-((r.M-v)%8));L+=k*((r.M-v+g[a])/8-(r.M-v)/8);}
  }
  if(EU<0)EU=0;
  printf("v=%d E=%lld EU=%lld P=%lld L1=%lld g=%lld\n",v,E,EU,P,L,v-8*L);
  if(EU>=P)return 2;
 }
 return 0;
}
