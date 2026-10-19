/* P5g heavy-fibre adversary. Compile/run on fejer, nice, one core.
 * args: seed g free span iterations restarts objective_constant. Preserves the
 * g disjoint triples of common sum P, and all unordered pair sums.
 * Annealing is heuristic; the final counts are recomputed exactly.
 */
#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static uint64_t rs;
static uint64_t rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static double ur(void){return (rnd()>>11)*(1.0/9007199254740992.0);}
static int n,g,fr,S,Pv,b[128],act[128],*pc,*tc;
static ll ex;
static void ta(int x,int sg){if(sg>0){if(tc[x]++)ex++;}else{assert(tc[x]);if(--tc[x])ex--;}}
static void elem(int i,int sg){
 int x=b[i];pc[2*x]+=sg;ta(3*x,sg);
 for(int j=0;j<n;j++)if(j!=i&&act[j]){
  pc[x+b[j]]+=sg;ta(2*x+b[j],sg);ta(x+2*b[j],sg);
 }
 for(int j=0;j<n;j++)if(j!=i&&act[j])for(int k=j+1;k<n;k++)if(k!=i&&act[k])ta(x+b[j]+b[k],sg);
}
static int canadd(int x){
 if(x<0||x>=S||pc[2*x])return 0;
 for(int j=0;j<n;j++)if(act[j]&&pc[x+b[j]])return 0;
 return 1;
}
static int start(void){
 for(int tries=0;tries<100;tries++){
  memset(act,0,sizeof act);memset(pc,0,(2*S+2)*sizeof(int));memset(tc,0,(3*S+3)*sizeof(int));ex=0;
  Pv=S+(int)(ur()*S);int ok=1;
  for(int i=0;i<g&&ok;i++){
   int done=0;
   for(int tr=0;tr<100000&&!done;tr++){
    int x=rnd()%S,y=rnd()%S,z=Pv-x-y;
    if(!canadd(x))continue;
    b[3*i]=x;elem(3*i,1);act[3*i]=1;
    if(canadd(y)){
     b[3*i+1]=y;elem(3*i+1,1);act[3*i+1]=1;
     if(canadd(z)){b[3*i+2]=z;elem(3*i+2,1);act[3*i+2]=1;done=1;}
     else{elem(3*i+1,-1);act[3*i+1]=0;}
    }
    if(!done){elem(3*i,-1);act[3*i]=0;}
   }
   if(!done)ok=0;
  }
  for(int i=3*g;i<n&&ok;i++){
   int done=0;for(int tr=0;tr<100000&&!done;tr++){int x=rnd()%S;if(canadd(x)){b[i]=x;elem(i,1);act[i]=1;done=1;}}
   if(!done)ok=0;
  }
  if(ok)return 1;
 }
 return 0;
}
static int span(void){int lo=b[0],hi=b[0];for(int i=1;i<n;i++){if(b[i]<lo)lo=b[i];if(b[i]>hi)hi=b[i];}return hi-lo+1;}
static ll H(void){return (ll)n*((ll)n*(n-1)/2+1);}
static void final(int *best,int common,ll steps){
 memcpy(b,best,n*sizeof(int));int lo=b[0],hi=b[0];for(int i=0;i<n;i++){if(b[i]<lo)lo=b[i];if(b[i]>hi)hi=b[i];}
 int *pairs=calloc(2*S+2,sizeof(int)),*trip=calloc(3*S+3,sizeof(int));unsigned char *sig=calloc(3*S+3,1);
 ll e=0,ns=0;int maxg=0;
 for(int i=0;i<n;i++)for(int j=i;j<n;j++)assert(++pairs[b[i]+b[j]]==1);
 for(int i=0;i<n;i++)for(int j=i;j<n;j++)for(int k=j;k<n;k++)if(trip[b[i]+b[j]+b[k]]++)e++;
 for(int v=0;v<3*S;v++)if(trip[v]>maxg)maxg=trip[v];
 for(int i=0;i<g;i++)assert(b[3*i]+b[3*i+1]+b[3*i+2]==common);
 for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=i;j<n;j++)if(i!=k&&j!=k){int v=b[i]+b[j]-b[k]+S;assert(v>=0&&v<3*S);if(!sig[v]){sig[v]=1;ns++;}}
 for(int i=0;i<n;i++)if(!sig[b[i]+S]){sig[b[i]+S]=1;ns++;}
 ll cap=3LL*(hi-lo+1)-2,sl=cap-H()+47*e;
 printf("g=%d free=%d n=%d max_span=%d span=%d P=%d iterations=%lld H=%lld ex=%lld maxfiber=%d signed=%lld holes=%lld F47=%lld ratio=%.9f\nset:",g,fr,n,S,hi-lo+1,common-3*lo,steps,H(),e,maxg,ns,cap-ns,sl,e?(double)(H()-cap)/e:0);
 for(int i=0;i<n;i++)printf(" %d",b[i]-lo);puts("");fflush(stdout);
 free(pairs);free(trip);free(sig);
}
int main(int ac,char**av){
 assert(ac==8);rs=strtoull(av[1],0,10)*2654435761ULL+9;g=atoi(av[2]);fr=atoi(av[3]);S=atoi(av[4]);ll iters=atoll(av[5]);int restarts=atoi(av[6]);int Cc=atoi(av[7]);
 n=3*g+fr;assert(n<=128&&S>n*n);pc=calloc(2*S+2,sizeof(int));tc=calloc(3*S+3,sizeof(int));
 int best[128],bestP=0;ll bestobj=1LL<<62;
 for(int rr=0;rr<restarts;rr++){
  assert(start());ll cur=3LL*span()-2-H()+Cc*ex;
  if(cur<bestobj){bestobj=cur;memcpy(best,b,n*sizeof(int));bestP=Pv;}
  for(ll it=0;it<iters;it++){
   int i=rnd()%(2*g+fr),j=-1;
   if(i<2*g){i=3*(i/2)+(i%2);j=3*(i/3)+2;}else i=3*g+i-2*g;
   int oi=b[i],oj=j<0?0:b[j];elem(i,-1);act[i]=0;
   if(j>=0){elem(j,-1);act[j]=0;}
   int x;
   if(ur()<.5){int w=1+rnd()%(1+(int)(S*ur()*ur()));x=oi+((rnd()&1)?w:-w);}else x=rnd()%S;
   int y=j<0?0:Pv-x-b[3*(i/3)+(i%3==0?1:0)];int good=canadd(x),added=0;
   if(good){b[i]=x;elem(i,1);act[i]=1;added=1;if(j>=0){good=canadd(y);if(good){b[j]=y;elem(j,1);act[j]=1;}}}
   ll obj=good?3LL*span()-2-H()+Cc*ex:1LL<<61;
   double temp=(5.0*n)*pow(.0001,(double)it/iters)+.03;
   int accept=good&&(obj<=cur||ur()<exp((cur-obj)/temp));
   if(accept){cur=obj;if(cur<bestobj){bestobj=cur;memcpy(best,b,n*sizeof(int));bestP=Pv;}}
   else{
    if(j>=0&&act[j]){elem(j,-1);act[j]=0;}
    if(added){elem(i,-1);act[i]=0;}
    b[i]=oi;elem(i,1);act[i]=1;
    if(j>=0){b[j]=oj;elem(j,1);act[j]=1;}
   }
  }
 }
 final(best,bestP,iters*restarts);return 0;
}
