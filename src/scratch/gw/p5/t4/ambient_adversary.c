/* Adversarial test of ambient SP12, not a proof. fejer, single core. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
static uint64_t st=202610194ULL;
static uint64_t rnd(void){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
static int cmp(const void*a,const void*b){return *(const int*)a-*(const int*)b;}
static int seen[100000],tri[100000],A[40],best[40];
static int evaluate(int n,int *fiber){
 memset(seen,0,sizeof(seen));
 for(int i=0;i<n;i++)for(int j=i;j<n;j++){int z=A[i]+A[j];if(seen[z]++)return -1;}
 memset(tri,0,sizeof(tri));int eps=0,mx=1;
 for(int i=0;i<n;i++)for(int j=i;j<n;j++)for(int k=j;k<n;k++){int z=A[i]+A[j]+A[k];if(tri[z]++)eps++;if(tri[z]>mx)mx=tri[z];}
 *fiber=mx;return eps;
}
int main(void){
 int ratios[]={40,60,80,95};long evals=0,valid=0;int worstnum=0,worstden=1;
 for(int n=9;n<=30;n+=3)for(int ri=0;ri<4;ri++){
  int H=n*(n*(n-1)/2+1),N=(H+2)*ratios[ri]/300,ebest=1000000,gmax=0,starts=0;
  for(int rep=0;rep<2;rep++){
   int got=0;
   for(int restart=0;restart<20&&!got;restart++){
    int k=0;
    for(int tries=0;tries<1000&&k<n;tries++){
     A[k]=rnd()%N;int bad=0;for(int i=0;i<k;i++)bad|=A[i]==A[k];if(bad)continue;
     int f;if(evaluate(k+1,&f)>=0)k++;
    }
    got=k==n;
   }
   if(!got)continue;starts++;
   int f,cur=evaluate(n,&f);
   for(int it=0;it<2000;it++){
    int j=rnd()%n,old=A[j];A[j]=rnd()%N;
    int eq=0;for(int k=0;k<n;k++)if(k!=j&&A[k]==A[j])eq=1;
    evals++;int e=eq?-1:evaluate(n,&f);
    if(e>=0){valid++;if(e<ebest){ebest=e;gmax=f;memcpy(best,A,n*sizeof(int));}}
    if(e>=0&&(e<=cur||(e<=cur+2&&rnd()%128==0)))cur=e;else A[j]=old;
   }
  }
  if(ebest==1000000){printf("n=%d interval=%d no_initial_set\n",n,N);continue;}
  qsort(best,n,sizeof(int),cmp);int span=best[n-1]-best[0]+1,need=H-(3*span-2);
  assert(ebest>0||need<=0);
  if(ebest>0&&need*worstden>worstnum*ebest){worstnum=need;worstden=ebest;}
  printf("n=%d N=%d starts=%d epsilon=%d max_fiber=%d span=%d needed_C=%d/%d set=",n,N,starts,ebest,gmax,span,need,ebest);
  for(int j=0;j<n;j++)printf("%s%d",j?",":"",best[j]);puts("");fflush(stdout);
  if(need>12*ebest){puts("COUNTEREXAMPLE TO UNPROVED AMBIENT-SP12");return 1;}
 }
 printf("evaluations=%ld pair_distinct=%ld max_needed_C=%d/%d no_SP12_failure\n",evals,valid,worstnum,worstden);
}
