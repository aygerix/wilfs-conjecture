/* Independent dense C Dijkstra and full direction traversal. Fejer only. */
#include "core.h"
int main(void){
 ll g[MM],w[MM];int m,ng=0;if(scanf("%d",&m)!=1||m<2||m>=MM)return 1;
 while(ng<MM&&scanf("%lld",&g[ng])==1)ng++;
 if(!apery(m,ng,g,w))return 2;
 Res r;evaluate(m,w,&r);dump("VERIFIED",&r,w);
 printf("QDef=%lld H2=%lld MFno2=%d AAPay=%lld QBound=%lld\n",r.QDef,r.H2,r.MFno2,r.AAPay,r.QBound);
 return 0;
}
