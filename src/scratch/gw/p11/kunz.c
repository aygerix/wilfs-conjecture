/* P11: exact-q4 Kunz annealing. mode 0 all e; 1 3e<m; 2 exact numeric residual.
 * objective 0 maximizes nonzero bulk; 1 seeks a negative high-generator RC term;
 * objective 2 minimizes CHAIN/need. All final values are integer exact.
 * Usage: seed m steps restarts mode objective. Run on fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define CAP 2048
static uint64_t rng;static int m,mode,obj,w[CAP],G[CAP];
static uint64_t rnd(void){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;}
static double unif(void){return (rnd()>>11)*(1.0/9007199254740992.0);}
/* A shortest-path seed, with a conductor truncation.  This is always a
 * semigroup: <m, n_1,...> union [K,infinity). */
static void seed_semigroup(void){
 int ns=10+rnd()%31,gg[48],used[CAP]={0},done[CAP]={0};
 int style=rnd()%4,span=style==0?m-1:style==1?m/2:style==2?m/3:m/5;
 int shift=style<2?0:rnd()%(m/4+1);
 for(int j=0;j<ns;j++)gg[j]=m+1+(shift+rnd()%span)%(m-1);
 for(int i=0;i<m;i++)w[i]=100000000;w[0]=0;
 for(int it=0;it<m;it++){int z=-1;for(int i=0;i<m;i++)if(!done[i]&&(z<0||w[i]<w[z]))z=i;done[z]=1;
  for(int j=0;j<ns;j++){int i=(z+gg[j])%m;if(w[z]+gg[j]<w[i])w[i]=w[z]+gg[j];}}
 int K=3*m+1+rnd()%m;
 for(int i=1;i<m;i++){int cap=K+(i-K%m+m)%m;if(w[i]>cap)w[i]=cap;}
}
typedef struct {int M,c,e,alpha,a,eta;int64_t bulk,con0,Delta,high,chain,RC,W,ell;double score;} Res;
static int at(int i){for(int j=1;j<m;j++){int k=(i+j)%m;if(k&&w[i]+w[j]<w[k])return 0;int v=(i-j+m)%m;if(v&&w[j]+w[v]<w[i])return 0;}return 1;}
static int eval(Res*r){
 int M=0;for(int i=1;i<m;i++)if(w[i]>M)M=w[i];if(M<4*m||M>=5*m)return 0;
 int d=0;for(int lev=1;lev<=4;lev++)for(int i=1;i<m;i++)if(w[i]/m==lev){int primitive=1;for(int j=0;j<d&&primitive;j++){int z=w[i]-G[j];if(z>0&&w[z%m]==z)primitive=0;}if(primitive)G[d++]=w[i];}
 if(d<2)return 0;
 memset(r,0,sizeof *r);r->M=M;r->c=M-m+1;r->e=d+1;
 int lam[CAP];for(int i=0;i<m;i++){lam[i]=(M-w[i])/m;r->ell+=lam[i];}
 int64_t C2=(int64_t)m*(m-1)/2;r->high=-1000000000000LL;
 r->W=(d+1)*r->ell-r->c;if(r->W<0){printf("WILF_COUNTER m=%d c=%d e=%d W=%lld w=",m,r->c,r->e,(long long)r->W);for(int i=0;i<m;i++)printf("%d,",w[i]);puts("");fflush(stdout);exit(9);}
 for(int a=0;a<d;a++){
  int n=G[a];r->alpha+=2*n<r->c-m;r->a+=n<r->c-2*m;r->eta+=n<2*m;
  int64_t Ra=0;
  for(int i=0;i<m;i++){int t=w[i];while(t+n<=M&&w[(t+n)%m]==t+n)t+=n;int64_t con=t-w[i]-(int64_t)m*lam[i];r->Delta+=con;if(i)r->bulk+=con;else r->con0+=con;r->chain+=M-t;Ra+=(M-w[i])%n;}
  r->RC+=Ra;if(n>=2*m&&C2-Ra>r->high)r->high=C2-Ra;
 }
 if(r->chain!=d*C2-r->Delta){fputs("IDENTITY_FAIL\n",stderr);exit(8);}
 if(obj==0)r->score=-(double)r->bulk/C2;else if(obj==1)r->score=-(double)r->high/C2;else r->score=(double)r->chain/((d-1)*C2);
 return 1;
}
static int domain(Res*r){if(mode>=1&&3*r->e>=m)return 0;if(mode==2&&(m<211||r->alpha<6||r->a<19||r->a>=5*r->alpha*(r->alpha+1)||r->e*(r->eta+2)>=2*m))return 0;return 1;}
static void dump(const char*tag,Res*r){printf("%s m=%d c=%d e=%d alpha=%d a=%d eta=%d bulk=%lld con0=%lld Delta=%lld high=%lld ell=%lld chain=%lld RC=%lld W=%lld C2=%lld gens=",tag,m,r->c,r->e,r->alpha,r->a,r->eta,(long long)r->bulk,(long long)r->con0,(long long)r->Delta,(long long)r->high,(long long)r->ell,(long long)r->chain,(long long)r->RC,(long long)r->W,(long long)m*(m-1)/2);for(int a=0;a<r->e-1;a++)printf("%s%d",a?",":"",G[a]);printf("\n w=");for(int i=0;i<m;i++)printf("%s%d",i?",":"",w[i]);puts("");fflush(stdout);}
int main(int argc,char**argv){if(argc<7)return 2;rng=atoll(argv[1])+0x9e3779b97f4a7c15ULL;m=atoi(argv[2]);long steps=atol(argv[3]);int chains=atoi(argv[4]);mode=atoi(argv[5]);obj=atoi(argv[6]);if(m>=CAP)return 2;long evals=0,starts=0,bulkfail=0,highfail=0;double best=1e99;Res br;int bw[CAP];
 for(int ch=0;ch<chains;ch++){
  Res cur;int found=0;
  for(int attempt=0;attempt<300&&!found;attempt++){seed_semigroup();if(eval(&cur)&&domain(&cur))found=1;}
  if(!found){w[0]=0;for(int i=1;i<m;i++)w[i]=4*m+i;
   for(int j=0;j<400*m&&!found;j++){int i=1+rnd()%(m-1),old=w[i];if(old<2*m)continue;w[i]-=m;if(!at(i)){w[i]=old;continue;}
    int M=0;for(int ii=1;ii<m;ii++)if(w[ii]>M)M=w[ii];if(M<4*m){w[i]=old;continue;}
    if(j%7==0&&eval(&cur)&&domain(&cur))found=1;}}
  if(!found){printf("NO_START chain=%d\n",ch);fflush(stdout);continue;}starts++;
  if(cur.score<best){best=cur.score;br=cur;memcpy(bw,w,m*sizeof(int));dump("START_BEST",&cur);}
  for(long it=0;it<steps;it++){
   int i=1+rnd()%(m-1),old=w[i];w[i]+=((rnd()&1)?m:-m);if(w[i]<m+i||w[i]>=5*m||!at(i)){w[i]=old;continue;}
   Res r;if(!eval(&r)||!domain(&r)){w[i]=old;continue;}evals++;bulkfail+=r.bulk>0;highfail+=r.high>0;
   if(r.score<best){best=r.score;br=r;memcpy(bw,w,m*sizeof(int));dump("BEST",&r);}
   double T=.08*pow(.9996,it)+.0001;
   if(r.score<cur.score||unif()<exp((cur.score-r.score)/T))cur=r;else w[i]=old;
  }
 }
 printf("DONE mode=%d objective=%d starts=%ld evals=%ld bulk_fail=%ld high_fail=%ld\n",mode,obj,starts,evals,bulkfail,highfail);
 if(best<1e90){memcpy(w,bw,m*sizeof(int));eval(&br);dump("FINAL",&br);}return 0;
}
