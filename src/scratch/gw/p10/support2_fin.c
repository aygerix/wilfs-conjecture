/* Exact certificate for support-at-most-two down-sets, 40 <= m <= 63.
 * Variables: six positive-face antichain sizes and the maximal-axis mask.
 * Run on fejer; no modular labeling hypotheses are used. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int edge[6][2]={{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}};
static int a[6], degree[7][64], partitions=0;
static long long states=0, survivors=0, minslack=1LL<<60;
static long long per_m[64],bad_m[64],min_m[64];
static int desc(const void*x,const void*y){return *(const int*)y-*(const int*)x;}
static long long rankterm(int*w,int n){int b[64];memcpy(b,w,n*sizeof(int));qsort(b,n,sizeof(int),desc);long long R=0;for(int i=0;i<n;i++)R+=(long long)i*b[i];return R;}
static int choose2(int n){return n*(n-1)/2;}
static int jfloor(int S,int q){if(S<=0)return 0;int v=S/q,r=S%q;return q*choose2(v)+r*v;}
static void test(int vol,int f,int t2){
 partitions++;int inc[4]={0};for(int e=0;e<6;e++)for(int j=0;j<2;j++)if(a[e]>inc[edge[e][j]])inc[edge[e][j]]=a[e];
 for(int mask=0;mask<16;mask++){
  int L[4],n1min=0,t1=0,ok=1;
  for(int b=0;b<4;b++){int maximal=(mask>>b)&1;t1+=maximal;if(!inc[b]&&!maximal)ok=0;L[b]=inc[b]?inc[b]+maximal:1;n1min+=L[b];}
  if(!ok||1+n1min+vol>63)continue;
  int w[64],nw=0;
  for(int e=0;e<6;e++)for(int j=0;j<a[e];j++)w[nw++]=5+a[e];
  for(int b=0;b<4;b++)if((mask>>b)&1)w[nw++]=4+L[b];
  long long R0=rankterm(w,nw);
  for(int m=40;m<=63;m++)for(int n2=vol;n2<=m-1-n1min;n2++){
   if(!f&&n2)continue;
   int n1=m-1-n2, H=(12*m-15*t1-24*t2+3)/4;
   int hh=degree[f][n2]+jfloor(3*n1-n2-f,12);if(hh>H)H=hh;if(H<0)H=0;
   long long R=R0;
   if(mask==15){
    R=1LL<<60;
    for(int b=0;b<4;b++){int extra=n1-n1min;int z[64],nz=0;
     for(int e=0;e<6;e++)for(int j=0;j<a[e];j++)z[nz++]=5+a[e];
     for(int c=0;c<4;c++)z[nz++]=4+L[c]+(c==b?extra:0);
     long long rr=rankterm(z,nz);if(rr<R)R=rr;
    }
   }
   states++;per_m[m]++;long long slack=(m+1LL)*H+R-3LL*m*(m-1)/2;if(slack<min_m[m])min_m[m]=slack;
   if(slack<minslack)minslack=slack;
   if(slack<0){survivors++;bad_m[m]++;if(survivors<=30){printf("SURV m=%d n1=%d n2=%d a=",m,n1,n2);for(int e=0;e<6;e++)printf("%s%d",e?",":"",a[e]);printf(" mask=%d H=%d R=%lld slack=%lld\n",mask,H,R,slack);}}
  }
 }
}
static void dfs(int e,int vol,int f,int t2){if(e==6){test(vol,f,t2);return;}for(int v=0;vol+v*(v+1)/2<=58;v++){a[e]=v;dfs(e+1,vol+v*(v+1)/2,f+(v>0),t2+v);}}
int main(void){for(int m=0;m<64;m++)min_m[m]=1LL<<60;for(int f=1;f<=6;f++)for(int n=0;n<64;n++){int left=n,d=0,s=0;while(left){int take=f*(d+1);if(take>left)take=left;s+=d*take;left-=take;d++;}degree[f][n]=s;}dfs(0,0,0,0);for(int m=40;m<=63;m++)printf("M %d states=%lld survivors=%lld min_slack=%lld\n",m,per_m[m],bad_m[m],min_m[m]);printf("DONE edge_profiles=%d states=%lld survivors=%lld min_slack=%lld\n",partitions,states,survivors,minslack);return 0;}
