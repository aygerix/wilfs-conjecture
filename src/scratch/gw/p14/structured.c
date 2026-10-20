/* P14: adversarial upper-half B3/Sidon A offsets, B/C completions.
 * Usage: structured cases seed. Run nice on fejer. */
#include "core.h"
static uint64_t rs=140014;
static unsigned rn(unsigned n){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs%n;}
static int unique_sums(int *x,int a,int mode){
 static int seen[8*MM];memset(seen,0,sizeof(seen));
 if(mode==0){for(int i=0;i<a;i++)for(int j=i;j<a;j++)for(int k=j;k<a;k++){int t=x[i]+x[j]+x[k];if(seen[t])return 0;seen[t]=1;}}
 else{for(int i=0;i<a;i++)for(int j=i;j<a;j++){int t=x[i]+x[j];if(seen[t])return 0;seen[t]=1;}}
 return 1;
}
int main(int argc,char**argv){
 int N=argc>1?atoi(argv[1]):1000;if(argc>2)rs=strtoull(argv[2],0,10);
 ll g[MM],w[MM],bw[MM];Res r,br;ll best=LLONG_MAX;int kept=0,positive=0,sparse=0,front=0;int ms[]={61,101,211,401,809,1601,2003};
 for(int it=0;it<N;it++){
  int m=ms[rn(7)],h=4+rn(m-4),mode=it%3,a=mode==2?19:4+rn(7),x[64],got=0;
  for(int tries=0;tries<3000&&got<a;tries++){
   int t;
   if(mode==2&&got<6)t=1+rn((h-1)/2);
   else t=(h+1)/2+rn(h-(h+1)/2);
   int du=0;for(int j=0;j<got;j++)if(x[j]==t)du=1;if(du)continue;
   x[got]=t;if(unique_sums(x,got+1,mode))got++;
  }
  if(got<3)continue;int ng=0;g[ng++]=m;
  for(int j=0;j<got;j++)g[ng++]=m+x[j];
  int nb=1+rn(12),nc=rn(5);
  if(it%4==0){nb=m/10+rn(m/7+1);int lo=h+rn(m/2);for(int j=0;j<nb;j++)g[ng++]=m+lo+j;}
  else for(int j=0;j<nb;j++)g[ng++]=m+h+rn(m);
  for(int j=0;j<nc;j++)g[ng++]=2*m+h+rn(m);
  static char reach[6*MM];memset(reach,0,sizeof(reach));reach[0]=1;int cap=3*m+h,M=cap+m-1;
  for(int v=0;v<=M;v++)if(reach[v])for(int j=0;j<ng;j++)if(v+g[j]<=M)reach[v+g[j]]=1;
  for(int i=0;i<m;i++)w[i]=LLONG_MAX/8;
  for(int v=0;v<=M;v++)if(reach[v]&&w[v%m]>v)w[v%m]=v;
  int complete=it%2;
  if(complete){for(int i=1;i<m;i++){ll u=cap+(i-cap%m+m)%m;if(w[i]>u)w[i]=u;}}
  int valid=1;for(int i=0;i<m;i++)if(w[i]==LLONG_MAX/8)valid=0;if(!valid)continue;
  evaluate(m,w,&r);if(r.q!=4)continue;kept++;if(r.RA)positive++;if(3*(r.d+1)<m)sparse++;if(r.alpha>=6&&r.a>=19&&3*(r.d+1)<m)front++;
  if(r.RA&&r.Relay<best){best=r.Relay;br=r;memcpy(bw,w,m*sizeof(ll));dump("RA_RECORD",&r,w);}
  if(r.Relay<0){dump("UF_RELAY_COUNTEREXAMPLE",&r,w);return 4;}
  if(r.W<0){dump("WILF_COUNTEREXAMPLE",&r,w);return 5;}
 }
 printf("SUMMARY inputs=%d q4=%d RApositive=%d sparse=%d frontier=%d minRArelay=%lld\n",N,kept,positive,sparse,front,best);if(best<LLONG_MAX)dump("BEST",&br,bw);
}
