/* Generator/truncation annealing; maximizes critical UF cells minus top budget. */
#include "core.h"
#include <math.h>
static uint64_t rs=130013;static unsigned rn(unsigned n){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs%n;}static double ur(void){return rn(1000000)/1000000.0;}
int main(int argc,char**argv){int m=argc>1?atoi(argv[1]):101,starts=argc>2?atoi(argv[2]):40,iters=argc>3?atoi(argv[3]):30000,sparse=argc>4?atoi(argv[4]):0;ll g[MM],w[MM],bestw[MM];Res r,z,br;double best=1e99;unsigned long long tested=0,good=0;
 for(int run=0;run<starts;run++){
  int ng=2+rn(m/4),K=3*m+1+rn(m-1);for(int i=0;i<ng;i++)g[i]=m+1+rn(3*m-1);
  if(run%2==0){ng=m/5+2;for(int i=0;i<ng;i++)g[i]=m+m/5+i;}
  double cur=1e99;
  for(int it=0;it<iters;it++){
   int t=rn(ng+1);ll old=t==ng?K:g[t];
   if(t==ng)K=3*m+1+rn(m-1);else {if(rn(5)==0)g[t]=m+1+rn(4*m-1);else g[t]+=(int)rn(11)-5;if(g[t]<=m||g[t]>=5*m){g[t]=old;continue;}}
   tested++;if(!apery(m,ng,g,w)){if(t==ng)K=old;else g[t]=old;continue;}
   for(int i=1;i<m;i++){ll cap=K+(i-K%m+m)%m;if(w[i]>cap)w[i]=cap;}
   evaluate(m,w,&z);if(z.q!=4||z.d<2||(sparse&&3*(z.d+1)>=m)){if(t==ng)K=old;else g[t]=old;continue;}good++;
   double score=(double)z.TopSlack/m;
   if(score<best){best=score;br=z;memcpy(bestw,w,m*sizeof(ll));dump("RECORD",&z,w);}
   if(z.CuSlack<0||z.PlusSlack<0||z.PoorSlack<0||z.nmfpoor){dump("COUNTEREXAMPLE",&z,w);return 2;}
   if(z.TopSlack<0){dump("TOP_COUNTEREXAMPLE",&z,w);return 3;}
   double T=.01+.2*(1.0-(double)it/iters);
   if(score<cur||ur()<exp((cur-score)/T)){cur=score;r=z;}else{if(t==ng)K=old;else g[t]=old;}
  }
  fprintf(stderr,"RUN %d tested=%llu class=%llu best=%.10f\n",run+1,tested,good,best);fflush(stderr);
 }
 printf("SUMMARY tested=%llu class=%llu best=%.10f\n",tested,good,best);if(best<1e90)dump("BEST",&br,bestw);
}
