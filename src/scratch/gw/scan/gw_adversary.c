/* Independent structured search and same-residue flip annealing.
 * gcc -O3 -std=c11 gw_adversary.c -lm -o gw_adversary
 * Deterministic xorshift64* PRNG; no external project code/data. */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <time.h>
#include <math.h>
#define A 12
#define N 104
#define H 2048
typedef __uint128_t Pt;
typedef struct {int d,m,s[A],k[A];Pt p[N];} Tile;
typedef struct {int64_t E,c,g,M;int t;} Metric;
typedef struct {Tile T;Metric q;char family[32];} Record;
static uint64_t rng=UINT64_C(916734891233);
static Record best[10],best_nonminimal[10];static int nb,nn;
static uint64_t tests,eligible,failures,shapes[5],valid[5],nodes[5],flips,accepted,walksteps,walkseeds,stuck;
static int htab[H],residx[N];static int64_t axsum[A];static int corner[N],nt;
static double started;
static double tm(clockid_t c){struct timespec t;clock_gettime(c,&t);return t.tv_sec+t.tv_nsec*1e-9;}
static uint64_t rnd(void){rng^=rng>>12;rng^=rng<<25;rng^=rng>>27;return rng*UINT64_C(2685821657736338717);}
static int ri(int n){return rnd()%(unsigned)n;}
static Pt un(int a){return (Pt)1<<(7*a);}
static int co(Pt p,int a){return (p>>(7*a))&127;}
static unsigned hash(Pt p){uint64_t x=(uint64_t)p^(uint64_t)(p>>64);x^=x>>33;x*=UINT64_C(0xff51afd7ed558ccd);x^=x>>33;return x&(H-1);}
static int lookup(const Tile*T,Pt p){unsigned h=hash(p);while(htab[h]){int i=htab[h]-1;if(T->p[i]==p)return i;h=(h+1)&(H-1);}return -1;}
static int residue(const Tile*T,Pt p){int r=0;for(int a=0;a<T->d;a++)r+=co(p,a)*T->s[a];return r%T->m;}
static void setup(const Tile*T){
 memset(htab,0,sizeof(htab));memset(axsum,0,sizeof(axsum));nt=0;
 for(int i=0;i<T->m;i++){unsigned h=hash(T->p[i]);while(htab[h])h=(h+1)&(H-1);htab[h]=i+1;residx[residue(T,T->p[i])]=i;for(int a=0;a<T->d;a++)axsum[a]+=co(T->p[i],a);}
 for(int i=0;i<T->m;i++){int max=1;for(int a=0;a<T->d;a++)if(lookup(T,T->p[i]+un(a))>=0){max=0;break;}if(max)corner[nt++]=i;}
}
static int valid_tile(const Tile*T){
 if(T->m<2||T->m>100||T->d<1||T->d>A)return 0;
 int seen[N]={0};setup(T);
 for(int a=0;a<T->d;a++)if(T->s[a]<1||T->s[a]>=T->m||lookup(T,un(a))<0)return 0;
 for(int i=0;i<T->m;i++){int r=residue(T,T->p[i]);if(seen[r]++)return 0;for(int a=0;a<T->d;a++)if(co(T->p[i],a)&&lookup(T,T->p[i]-un(a))<0)return 0;}
 return 1;
}
static Metric metric(const Tile*T){
 Metric q={0};q.t=nt;int64_t sum=0;
 for(int a=0;a<T->d;a++)sum+=axsum[a]*(T->s[a]+T->m*T->k[a]);
 q.g=(sum-(int64_t)T->m*(T->m-1)/2)/T->m;
 for(int j=0;j<nt;j++){int64_t v=0;for(int a=0;a<T->d;a++)v+=(int64_t)co(T->p[corner[j]],a)*(T->s[a]+T->m*T->k[a]);if(v>q.M)q.M=v;}
 q.c=q.M-T->m+1;q.E=T->d*q.c-(T->d+1)*q.g;return q;
}
static int minimal(const Tile*T){
 int64_t ds[N];int done[N]={0};for(int i=0;i<T->m;i++)ds[i]=INT64_MAX/4;ds[0]=0;
 for(int j=0;j<T->m;j++){int r=-1;for(int i=0;i<T->m;i++)if(!done[i]&&(r<0||ds[i]<ds[r]))r=i;done[r]=1;
  for(int a=0;a<T->d;a++){int z=(r+T->s[a])%T->m;int64_t v=ds[r]+T->s[a]+T->m*T->k[a];if(v<ds[z])ds[z]=v;}}
 for(int i=0;i<T->m;i++){int64_t v=0;for(int a=0;a<T->d;a++)v+=(int64_t)co(T->p[i],a)*(T->s[a]+T->m*T->k[a]);if(v!=ds[residue(T,T->p[i])])return 0;}return 1;
}
static void dump(FILE*f,const Record*r){
 const Tile*T=&r->T;const Metric*q=&r->q;
 fprintf(f,"{\"family\":\"%s\",\"d\":%d,\"m\":%d,\"n\":[",r->family,T->d,T->m);
 for(int a=0;a<T->d;a++)fprintf(f,"%s%d",a?",":"",T->s[a]+T->m*T->k[a]);
 fprintf(f,"],\"E\":%lld,\"c\":%lld,\"g\":%lld,\"M\":%lld,\"corners\":%d,\"minimal\":%s,\"D\":[",(long long)q->E,(long long)q->c,(long long)q->g,(long long)q->M,q->t,minimal(T)?"true":"false");
 for(int i=0;i<T->m;i++){fprintf(f,"%s[",i?",":"");for(int a=0;a<T->d;a++)fprintf(f,"%s%d",a?",":"",co(T->p[i],a));fputc(']',f);}fprintf(f,"]}\n");
}
static int same(const Record*r,const Tile*T){
 if(r->T.d!=T->d||r->T.m!=T->m)return 0;
 for(int a=0;a<T->d;a++)if(r->T.s[a]+T->m*r->T.k[a]!=T->s[a]+T->m*T->k[a])return 0;
 for(int i=0;i<T->m;i++){int found=0;for(int j=0;j<T->m;j++)if(T->p[i]==r->T.p[j]){found=1;break;}if(!found)return 0;}return 1;
}
static void insert(Record*b,int*sz,const Tile*T,Metric q,const char*f){
 int pos=0;while(pos<*sz&&b[pos].q.E*q.c<=q.E*b[pos].q.c)pos++;if(pos>=10)return;
 for(int j=0;j<*sz;j++)if(same(&b[j],T))return;
 if(*sz<10)(*sz)++;for(int j=*sz-1;j>pos;j--)b[j]=b[j-1];b[pos].T=*T;b[pos].q=q;snprintf(b[pos].family,32,"%s",f);
}
static void consider(const Tile*T,Metric q,const char*f){
 tests++;if(q.E<0){Record r={.T=*T,.q=q};snprintf(r.family,32,"%s",f);FILE*out=fopen("FAILURE.jsonl","w");dump(out,&r);fclose(out);failures++;exit(2);}
 if(q.c<T->m||q.t<=T->d)return;eligible++;
 insert(best,&nb,T,q,f);
 if((nn<10||q.E*best_nonminimal[nn-1].q.c<best_nonminimal[nn-1].q.E*q.c)&&!minimal(T))insert(best_nonminimal,&nn,T,q,f);
}
static void all_lifts(Tile*T,const char*f){
 setup(T);uint64_t count=1;for(int a=0;a<T->d;a++)count*=4;
 int full=T->d<=6;if(!full)count=512;
 for(uint64_t j=0;j<count;j++){uint64_t z=j;for(int a=0;a<T->d;a++){T->k[a]=full?(z&3):ri(4);z>>=2;}consider(T,metric(T),f);}
}
/* All possible same-residue single-cell exchanges from the present tile. */
static int moves(const Tile*T,Pt*out,int*rem){
 setup(T);int count=0,ismax[N]={0};for(int j=0;j<nt;j++)ismax[corner[j]]=1;
 for(int i=0;i<T->m;i++)for(int a=0;a<T->d;a++){
  Pt z=T->p[i]+un(a);if(lookup(T,z)>=0)continue;
  int y=residx[residue(T,z)];if(!ismax[y])continue;
  int unit=0;for(int b=0;b<T->d;b++)if(T->p[y]==un(b))unit=1;if(unit)continue;
  int ok=1;for(int b=0;b<T->d;b++)if(co(z,b)){int p=lookup(T,z-un(b));if(p<0||p==y){ok=0;break;}}
  if(!ok)continue;int dup=0;for(int j=0;j<count;j++)if(out[j]==z){dup=1;break;}if(dup)continue;
  out[count]=z;rem[count++]=y;
 }
 return count;
}
static int seed_tile(Tile*T){
 int done[N]={0};int64_t ds[N];Pt p[N];for(int i=0;i<T->m;i++){ds[i]=INT64_MAX/4;p[i]=0;}ds[0]=0;
 for(int j=0;j<T->m;j++){
  int r=-1;for(int i=0;i<T->m;i++)if(!done[i]&&(r<0||ds[i]<ds[r]))r=i;if(ds[r]>=INT64_MAX/8)return 0;done[r]=1;
  for(int a=0;a<T->d;a++){int z=(r+T->s[a])%T->m;int64_t v=ds[r]+T->m+T->s[a];Pt q=p[r]+un(a);if(v<ds[z]||(v==ds[z]&&q<p[z])){ds[z]=v;p[z]=q;}}
 }
 for(int i=0;i<T->m;i++)T->p[i]=p[i];return valid_tile(T);
}
static void random_s(Tile*T){for(int a=0;a<T->d;a++){int ok;do{ok=1;T->s[a]=1+ri(T->m-1);for(int b=0;b<a;b++)if(T->s[b]==T->s[a])ok=0;}while(!ok);T->k[a]=ri(4);}}
static const char*fnames[]={"nearstar","arms","boxes","box_one_flip","product"};
static int category,limit,found;static uint64_t budget;static int groups[A][N],ng[A];
static void structured_residues(Tile*T,int a,unsigned char*mask){
 if(!budget||found>=limit)return;budget--;nodes[category]++;
 if(a==T->d){valid[category]++;found++;all_lifts(T,fnames[category]);return;}
 int offset=ri(T->m-1);
 for(int j=0;j<T->m-1&&budget&&found<limit;j++){
  int t=1+(offset+j)%(T->m-1),duplicate=0;for(int b=0;b<a;b++)if(T->s[b]==t)duplicate=1;if(duplicate)continue;T->s[a]=t;
  unsigned char next[N];memcpy(next,mask,T->m);int ok=1;
  for(int h=0;h<ng[a];h++){int i=groups[a][h],r=0;for(int b=0;b<=a;b++)r+=co(T->p[i],b)*T->s[b];r%=T->m;if(next[r]){ok=0;break;}next[r]=1;}
  if(ok)structured_residues(T,a+1,next);
 }
}
static void search_shape(Tile*T,int cat,int cap,int nodecap){
 category=cat;shapes[cat]++;limit=cap;found=0;budget=nodecap;memset(ng,0,sizeof(ng));
 for(int i=0;i<T->m;i++)if(T->p[i]){int a=T->d-1;while(!co(T->p[i],a))a--;groups[a][ng[a]++]=i;}
 unsigned char mask[N]={1};structured_residues(T,0,mask);
}
static void nearstars(int trials){
 for(int run=0;run<trials;run++){
  Tile T={0};T.d=3+ri(10);T.m=T.d+2+ri((T.d*(T.d+1))/2);if(T.m>100)T.m=100;random_s(&T);
  T.p[0]=0;for(int a=0;a<T.d;a++)T.p[a+1]=un(a);
  int present[N]={0};present[0]=1;for(int a=0;a<T.d;a++)present[T.s[a]]=1;
  int ok=1;for(int r=0;r<T.m;r++)if(!present[r]){
   Pt candidates[A*A];int c=0;for(int a=0;a<T.d;a++)for(int b=a;b<T.d;b++)if((T.s[a]+T.s[b])%T.m==r)candidates[c++]=un(a)+un(b);
   if(!c){ok=0;break;}
   int i=T.d+1;while(i<T.m&&T.p[i])i++;T.p[i]=candidates[ri(c)];
  }
  shapes[0]++;if(ok&&valid_tile(&T)){valid[0]++;all_lifts(&T,"nearstar");}
 }
}
static void arms(int trials){
 for(int run=0;run<trials;run++){
  Tile T={0};T.d=3+ri(3);int longarms=2+ri(2);if(longarms>T.d)longarms=T.d;
  int lengths[A];for(int a=0;a<T.d;a++)lengths[a]=1;
  int target=20+ri(81),q=ri(5);if(target-q<T.d+1)continue;
  for(int j=T.d+1;j<target-q;j++)lengths[ri(longarms)]++;
  int z=1;T.p[0]=0;for(int a=0;a<T.d;a++)for(int j=1;j<=lengths[a];j++)T.p[z++]=j*un(a);
  for(int j=0;j<q;j++){int a=ri(longarms),b=ri(longarms);if(a==b){j--;continue;}Pt p=un(a)+un(b);int dup=0;for(int i=0;i<z;i++)if(T.p[i]==p)dup=1;if(dup)break;T.p[z++]=p;}
  T.m=z;search_shape(&T,1,8,12000);
 }
}
static void boxes(void){
 for(int d=3;d<=5;d++)for(int a=2;a<=6;a++)for(int b=2;b<=6;b++)for(int c=2;c<=6;c++){
  int lens[A]={a,b,c,2,2};int m=1;for(int j=0;j<d;j++)m*=lens[j];if(m>100)continue;
  Tile T={.d=d,.m=m};for(int i=0;i<m;i++){int z=i;Pt p=0;for(int j=0;j<d;j++){p+=un(j)*(z%lens[j]);z/=lens[j];}T.p[i]=p;}
  search_shape(&T,2,8,6000);
  Pt max=0;for(int j=0;j<d;j++)max+=(lens[j]-1)*un(j);
  for(int j=0;j<d;j++){Tile U=T;for(int i=0;i<m;i++)if(U.p[i]==max)U.p[i]=lens[j]*un(j);search_shape(&U,3,2,4000);}
 }
}
static void products(int trials){
 for(int run=0;run<trials;run++){
  Tile B={.d=3,.m=7+ri(19)};random_s(&B);if(!seed_tile(&B))continue;int L=2+ri(3);if(B.m*L>100)continue;
  Tile T={.d=4,.m=B.m*L};for(int i=0;i<B.m;i++)for(int j=0;j<L;j++)T.p[i*L+j]=B.p[i]+j*un(3);
  for(int a=0;a<3;a++)T.s[a]=B.s[a];T.s[3]=B.m;
  /* This mixed-radix map is valid because the base weights are lifted
   * to their actual distinct residue values before taking the product. */
  search_shape(&T,4,8,16000);
 }
}
static void walk(int count,int steps){
 for(int run=0;run<count;run++){
  Tile T={.d=3+ri(4),.m=20+ri(81)};random_s(&T);if(!seed_tile(&T)){run--;continue;}walkseeds++;
  all_lifts(&T,"walk_seed");for(int a=0;a<T.d;a++)T.k[a]=ri(4);setup(&T);Metric q=metric(&T);
  Pt move[N*A];int rem[N*A];int options=moves(&T,move,rem);if(!options)stuck++;
  for(int step=0;step<steps;step++){
   Tile U=T;int flip=options&&(step<steps/3||ri(10)<7);if(flip){int j=ri(options);U.p[rem[j]]=move[j];}else U.k[ri(U.d)]=ri(4);
   setup(&U);Metric p=metric(&U);consider(&U,p,step<steps/3?"random_flip":"local_search");walksteps++;
   double old=q.c>=T.m&&q.t>T.d?(double)q.E/q.c:10.0;
   double neu=p.c>=U.m&&p.t>U.d?(double)p.E/p.c:10.0;
   double temperature=0.03*(1.0-(double)step/steps)+0.001;
   int accept=step<steps/3||neu<=old||(double)(rnd()>>11)*0x1.0p-53<exp((old-neu)/temperature);
   if(accept){T=U;q=p;accepted++;if(flip){flips++;options=moves(&T,move,rem);}}
   if(step%1000==999){int saved[A];memcpy(saved,T.k,sizeof(saved));all_lifts(&T,"walk_lifts");memcpy(T.k,saved,sizeof(saved));setup(&T);q=metric(&T);}
  }
  if(run%8==7){printf("progress seeds=%llu tests=%llu flips=%llu wall=%.3f\n",(unsigned long long)walkseeds,(unsigned long long)tests,(unsigned long long)flips,tm(CLOCK_MONOTONIC)-started);fflush(stdout);}
 }
}
int main(int argc,char**argv){
 int scale=argc>1?atoi(argv[1]):1;if(argc>2)rng=strtoull(argv[2],0,10);started=tm(CLOCK_MONOTONIC);double cpu=tm(CLOCK_PROCESS_CPUTIME_ID);
 printf("seed=%llu scale=%d\n",(unsigned long long)rng,scale);fflush(stdout);
 nearstars(12000*scale);arms(200*scale);boxes();products(150*scale);walk(64*scale,9000);
 FILE*f=fopen("top10.jsonl","w");for(int i=0;i<nb;i++)dump(f,&best[i]);fclose(f);
 f=fopen("top10_nonminimal.jsonl","w");for(int i=0;i<nn;i++)dump(f,&best_nonminimal[i]);fclose(f);
 printf("family,shape_attempts,residue_pairs,node_visits\n");for(int i=0;i<5;i++)printf("%s,%llu,%llu,%llu\n",fnames[i],(unsigned long long)shapes[i],(unsigned long long)valid[i],(unsigned long long)nodes[i]);
 printf("tests=%llu eligible=%llu failures=%llu seeds=%llu steps=%llu accepted=%llu flips=%llu initial_no_flip=%llu wall=%.6f cpu=%.6f\n",(unsigned long long)tests,(unsigned long long)eligible,(unsigned long long)failures,(unsigned long long)walkseeds,(unsigned long long)walksteps,(unsigned long long)accepted,(unsigned long long)flips,(unsigned long long)stuck,tm(CLOCK_MONOTONIC)-started,tm(CLOCK_PROCESS_CPUTIME_ID)-cpu);fflush(stdout);return 0;
}
