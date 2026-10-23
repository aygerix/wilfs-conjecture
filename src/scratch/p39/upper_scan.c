/* Deterministic adversarial sampling for the universal upper-side certificate bound.
 * No LP solver. Every accepted sample is a genuine semigroup with e >= 4,
 * c > 4m and 3e < m; no height/depth restriction. Stop on first negative assignment-corrected bound.
 * usage: upper_scan NS SEED [MIN_E=4]
 * --capacity-audit m g...: audit whether an optimal cover fits actual repair caps.
 * --wilf-climb-wide / --wilf-negative-wide m g...: minimize actual W/c,
 *   with the latter retaining only B<0 (a necessary condition for W<0).
 * --position-audit MAXM: exhaustively check the algebraic penalty identity (MAXM<=128).
 * --individual-search NS SEED [MIN_E]: falsify the integer individual-payment bound.
 * --transport-audit m g...: three exact graph relaxations with path witnesses.
 * --unit-search NS SEED [MIN_E]: stop on a capped-unpaid envelope above one.
 * --interior-unit-search NS SEED [MIN_E]: restrict that target to cells whose
 *   addition by every non-multiplicity primitive remains in the Apéry set.
 * --axis-flow FILE: exact integer min-cost flow for weighted column transport;
 *   exports a feasible flow and residual potentials for independent checking.
 * --axis-seed m g...: export exact seed invariants/rows without optimization.
 * --supp-audit m g...: canonical support/column counts and SUPP-WILF identities.
 * --partial-support-audit m g...: test unit missing-residue credit on principal
 *   upset deletions and value prefixes inside this genuine canonical tile.
 * --support-cut m g...: exact minimum completion budget over ALL down-sets of
 *   this tile, with a maximum-flow/minimum-cut certificate (no LP solver).
 * --support-pool-cut m g...: falsify the E433 directional residue-pool payment
 *   on every down-set of this tile; a negative result is not a Wilf failure.
 * --support-frozen-cut m g...: test extension of the fixed NONWRAPPING partial
 *   allocation (E434); negative means this stronger allocation fails, not Wilf.
 * --supp-climb weighted|cycle ITER m g...: bounded local falsification of
 *   the weighted support budget or proposed cycle-excess bound; no LP solver.
 * --residue-audit G...: reconstruct S and T from MINIMAL-generator residues.
 * --odd-audit G...: exact S and additive closure of its normalized odd ideal.
 * --differential-audit G...: independent binomial derivative rows modulo conductor.
 * --odd-climb STEPS G...: one bounded falsification of W(S)>=W(odd closure).
 * --residue-climb ITER m g...: bounded general RD falsification, all heights/
 *   depths, retaining c>4m,3e<m,W(T)>0 and the necessary genus-bound filter.
 * --unit-audit m g...: export that integer envelope (an upper bound, not a feasible x).
 * --weighted-search NS SEED [MIN_E]: test W-e sum U>=0, stopping at first failure.
 * --weighted-audit m g...: add an exact assignment certificate on the residual core.
 * --integer-weighted-audit m g...: additionally floor repeated-parent bounds;
 *   this certifies the integer capped model and actual W, not the real capped LP.
 * --equality-weighted-audit m g...: complete pair demands across forced-equal classes.
 * --combined-climb-wide m g...: minimize the integer combined bound/c, retaining B<0.
 * This is sampling, not exhaustive enumeration and not a proof of Wilf.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifndef MM
#define MM 256
#endif
#define GG 32
#include "assignment.h"
typedef long long ll;
static uint64_t state;
static long nbneg;
static ll ratio_num,ratio_den=1;
static int need_e,kunz_cap;
static int individual_audit;
static int unit_audit;
static int combined_audit;
typedef struct {int u,v,cap,cost;} FlowArc;
static int axis_flow(const char *path){
 FILE *in=fopen(path,"r");int n,na,source,sink,need;
 if(!in||fscanf(in,"%d%d%d%d%d",&n,&na,&source,&sink,&need)!=5||n<2||n>8194||na<0||na>1000000||source<0||source>=n||sink<0||sink>=n||source==sink||need<0||need>1000000)return 2;
 FlowArc *a=calloc((size_t)2*na+1,sizeof(*a));int *initial=calloc((size_t)na+1,sizeof(int));
 long long *dist=calloc(n,sizeof(long long));int *prev=calloc(n,sizeof(int));
 if(!a||!initial||!dist||!prev)return 2;
 for(int j=0;j<na;j++){
  int u,v,cap,cost;if(fscanf(in,"%d%d%d%d",&u,&v,&cap,&cost)!=4||u<0||u>=n||v<0||v>=n||cap<0||cap>1000000||cost < -1000000||cost>1000000)return 2;
  a[2*j]=(FlowArc){u,v,cap,cost};a[2*j+1]=(FlowArc){v,u,0,-cost};initial[j]=cap;
 }fclose(in);
 int sent=0;long long cost=0,inf=LLONG_MAX/4;
 while(sent<need){
  for(int v=0;v<n;v++){dist[v]=inf;prev[v]=-1;}dist[source]=0;
  for(int k=0;k<n-1;k++){int changed=0;for(int j=0;j<2*na;j++)if(a[j].cap&&dist[a[j].u]!=inf&&dist[a[j].v]>dist[a[j].u]+a[j].cost){dist[a[j].v]=dist[a[j].u]+a[j].cost;prev[a[j].v]=j;changed=1;}if(!changed)break;}
  if(prev[sink]<0){fprintf(stderr,"axis flow infeasible\n");return 3;}
  int delta=need-sent,v=sink,steps=0;
  while(v!=source){int j=prev[v];if(j<0||++steps>n)return 3;if(a[j].cap<delta)delta=a[j].cap;v=a[j].u;}
  for(v=sink;v!=source;){int j=prev[v];a[j].cap-=delta;a[j^1].cap+=delta;v=a[j].u;}
  sent+=delta;cost+=(long long)delta*dist[sink];
 }
 /* A super-source at zero distance checks ALL residual components, including
  * ones no longer reachable from the original source after saturation. */
 for(int v=0;v<n;v++)dist[v]=0;
 for(int k=0;k<n;k++){int changed=0;for(int j=0;j<2*na;j++)if(a[j].cap&&dist[a[j].v]>dist[a[j].u]+a[j].cost){dist[a[j].v]=dist[a[j].u]+a[j].cost;changed=1;}if(!changed)break;if(k==n-1){fprintf(stderr,"negative residual cycle\n");return 3;}}
 long long primal=0,dual=(long long)need*(dist[sink]-dist[source]);
 for(int j=0;j<na;j++){int f=initial[j]-a[2*j].cap;long long reduced=a[2*j].cost+dist[a[2*j].u]-dist[a[2*j].v];primal+=(long long)f*a[2*j].cost;if(reduced<0)dual+=(long long)initial[j]*reduced;}
 if(primal!=cost||dual!=cost){fprintf(stderr,"axis flow dual mismatch\n");return 3;}
 printf("{\"nodes\":%d,\"arcs\":%d,\"flow\":%d,\"cost\":%lld,\"flows\":[",n,na,sent,cost);
 for(int j=0;j<na;j++)printf("%s%d",j?",":"",initial[j]-a[2*j].cap);
 printf("],\"potential\":[");for(int v=0;v<n;v++)printf("%s%lld",v?",":"",dist[v]);printf("]}\n");
 free(a);free(initial);free(dist);free(prev);return 0;
}
static ll last_num,last_den,last_corrected,last_B,last_M,last_W;
static ll last_individual;
static ll last_propagated;
static int last_e,last_c,last_q,last_h;
static uint64_t rnd(void){state^=state>>12;state^=state<<25;state^=state>>27;return state*2685821657736338717ULL;}
static int pick(int n){return (int)(rnd()%(unsigned)n);}
static int root(int *p,int a){while(p[a]!=a){p[a]=p[p[a]];a=p[a];}return a;}
typedef struct {int m,e,c,G[MM];ll genus,W;} ResidueStats;
/* Generic generator reconstruction, also when the multiplicity drops below the
 * original m. Extract MINIMAL generators before forming their residues: residues
 * of redundant input generators would define a different, generally larger T. */
static int residue_stats(int *G,int ng,ResidueStats *R){
 int m=INT_MAX;for(int j=0;j<ng;j++){if(G[j]<=0)return 0;if(G[j]<m)m=G[j];}
 if(m<1||m>=MM)return 0;int w[MM],done[MM]={0},primitive[MM]={0};
 for(int s=0;s<m;s++)w[s]=s?INT_MAX/4:0;
 for(int k=0;k<m;k++){
  int u=-1;for(int s=0;s<m;s++)if(!done[s]&&(u<0||w[s]<w[u]))u=s;
  if(w[u]==INT_MAX/4)return 0;done[u]=1;
  for(int j=0;j<ng;j++){if(G[j]>=INT_MAX/4-w[u])return 0;int v=w[u]+G[j],s=v%m;if(v<w[s])w[s]=v;}
 }
 int M=0;ll genus=0;for(int s=1;s<m;s++){if(w[s]>M)M=w[s];genus+=w[s]/m;primitive[s]=1;}
 for(int i=1;i<m;i++)for(int j=i;j<m;j++){int s=(i+j)%m;if(s&&w[i]+w[j]==w[s])primitive[s]=0;}
 *R=(ResidueStats){.m=m,.e=1,.c=M-m+1,.genus=genus};R->G[0]=m;
 for(int s=1;s<m;s++)if(primitive[s])R->G[R->e++]=w[s];
 R->W=(ll)R->e*(R->c-genus)-R->c;return 1;
}
static int residue_compare(int *G,int ng,ResidueStats *S,ResidueStats *T){
 if(!residue_stats(G,ng,S))return 0;int A[MM];A[0]=S->m;
 for(int j=1;j<S->e;j++)A[j]=S->G[j]%S->m;
 if(!residue_stats(A,S->e,T))return 0;
 if(S->W<0||T->W<0){
  ResidueStats *R=S->W<0?S:T;
  fprintf(stderr,"POTENTIAL_NEGATIVE_W needs independent membership audit: W=%lld G=[",R->W);
  for(int j=0;j<R->e;j++)fprintf(stderr,"%s%d",j?",":"",R->G[j]);fprintf(stderr,"]\n");exit(4);
 }
 return 1;
}
static void print_odd_stats(ResidueStats *S,ResidueStats *U,int a);
/* E443: selected exact relation witnesses. A rank exceeding W alone refutes the
 * proposed conductor differential bound; no completeness claim is needed then. */
typedef struct {int e,c,N,P[10],z[10],first[10],chosen[10][10],active[10],seen,rank;ll basis[10][10];unsigned char *member;} DiffAudit;
static ll diff_gcd(ll a,ll b){if(a<0)a=-a;if(b<0)b=-b;while(b){ll t=a%b;a=b;b=t;}return a;}
static void diff_factor(DiffAudit *D,int j,int left){
 if(j==D->e){
  if(left)return;
  if(!D->seen){memcpy(D->first,D->z,D->e*sizeof(int));D->seen=1;return;}
  ll row[10];for(int k=0;k<D->e;k++)row[k]=D->active[k]?D->z[k]-D->first[k]:0;
  for(int k=0;k<D->e;k++)if(row[k]){
   if(!D->basis[k][k]){memcpy(D->basis[k],row,D->e*sizeof(ll));memcpy(D->chosen[D->rank++],D->z,D->e*sizeof(int));return;}
   ll x=row[k],p=D->basis[k][k];
   for(int l=k;l<D->e;l++){__int128 v=(__int128)row[l]*p-(__int128)D->basis[k][l]*x;if(v>=LLONG_MAX||v<=-LLONG_MAX){fprintf(stderr,"differential integer overflow\n");exit(3);}row[l]=(ll)v;}
   ll g=0;for(int l=0;l<D->e;l++)g=diff_gcd(g,row[l]);if(g>1)for(int l=0;l<D->e;l++)row[l]/=g;
  }return;
 }
 for(int n=0;n<=left/D->P[j];n++){D->z[j]=n;diff_factor(D,j+1,left-n*D->P[j]);}
}
static int differential_audit(int *G,int ng){
 ResidueStats S;if(!residue_stats(G,ng,&S)||S.m==1||S.e>10)return 2;
 if(S.W<0){fprintf(stderr,"POTENTIAL_NEGATIVE_W requires independent membership audit\n");return 4;}
 int mx=0;for(int j=0;j<S.e;j++)if(S.G[j]>mx)mx=S.G[j];int cap=S.c+mx;
 if(cap>4096)return 2;unsigned char member[4096]={0};member[0]=1;
 for(int n=1;n<cap;n++)for(int j=0;j<S.e;j++)if(n>=S.G[j]&&member[n-S.G[j]]){member[n]=1;break;}
 int ell=0;for(int n=0;n<S.c;n++)ell+=member[n];assert(S.W==(ll)S.e*ell-S.c);
 printf("{\"G\":[");for(int j=0;j<S.e;j++)printf("%s%d",j?",":"",S.G[j]);
 printf("],\"c\":%d,\"g\":%lld,\"e\":%d,\"ell\":%d,\"W\":%lld,\"free_dimension\":%d,\"blocks\":[",S.c,S.genus,S.e,ell,S.W,S.e*ell);
 int count=0,total=0,stopped=0;
 for(int N=S.m;N<cap;N++){
  DiffAudit D={.e=S.e,.c=S.c,.N=N,.member=member};memcpy(D.P,S.G,S.e*sizeof(int));
  int active=0;for(int j=0;j<S.e;j++)if(N>=S.G[j]&&N-S.G[j]<S.c&&member[N-S.G[j]]){D.active[j]=1;active++;}
  if(!active)continue;diff_factor(&D,0,N);assert(D.seen);if(!D.rank)continue;
  printf("%s{\"N\":%d,\"active\":[",count++?",":"",N);for(int j=0;j<S.e;j++)printf("%s%d",j?",":"",D.active[j]);
  printf("],\"base\":[");for(int j=0;j<S.e;j++)printf("%s%d",j?",":"",D.first[j]);printf("],\"trades\":[");
  for(int k=0;k<D.rank;k++){printf("%s[",k?",":"");for(int j=0;j<S.e;j++)printf("%s%d",j?",":"",D.chosen[k][j]);printf("]");}printf("],\"rank\":%d}",D.rank);
  total+=D.rank;if(total>S.W){stopped=1;break;}
 }
 printf("],\"selected_relation_rank\":%d,\"differential_dimension_upper_bound\":%d,\"stopped_at_failure\":%s}\n",total,S.e*ell-total,stopped?"true":"false");return 0;
}
static int odd_compare(int *G,int ng,ResidueStats *S,ResidueStats *U,int *least_odd){
 if(!residue_stats(G,ng,S))return 0;
 if(S->m==1)return 0; /* The descent is for proper S; U=N is allowed. */
 int a=INT_MAX,A[MM],n=0;
 for(int j=0;j<S->e;j++)if((S->G[j]&1)&&S->G[j]<a)a=S->G[j];
 if(a==INT_MAX)return 0;A[n++]=a;
 for(int j=0;j<S->e;j++){
  int p=S->G[j];if(!(p&1))A[n++]=p/2;else if(p>a)A[n++]=(p-a)/2;
 }
 assert(n==S->e);if(!residue_stats(A,n,U))return 0;
 assert(U->e<=S->e&&U->genus<S->genus);*least_odd=a;
 if(S->W<0||U->W<0)print_odd_stats(S,U,a);
 return 1;
}
static void print_odd_stats(ResidueStats *S,ResidueStats *U,int a){
 printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"g\":%lld,\"W\":%lld,\"G\":[",S->m,S->e,S->c,S->genus,S->W);
 for(int j=0;j<S->e;j++)printf("%s%d",j?",":"",S->G[j]);
 printf("],\"least_odd\":%d,\"odd_closure\":{\"m\":%d,\"e\":%d,\"c\":%d,\"g\":%lld,\"W\":%lld,\"G\":[",a,U->m,U->e,U->c,U->genus,U->W);
 for(int j=0;j<U->e;j++)printf("%s%d",j?",":"",U->G[j]);
 printf("]},\"margin\":%lld}\n",S->W-U->W);fflush(stdout);
 if(S->W<0||U->W<0){fprintf(stderr,"POTENTIAL_NEGATIVE_W requires independent audit\n");exit(4);}
}
static void print_residue_stats(ResidueStats *S,ResidueStats *T){
 printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"g\":%lld,\"W\":%lld,\"G\":[",S->m,S->e,S->c,S->genus,S->W);
 for(int j=0;j<S->e;j++)printf("%s%d",j?",":"",S->G[j]);
 printf("],\"residue\":{\"m\":%d,\"e\":%d,\"c\":%d,\"g\":%lld,\"W\":%lld,\"G\":[",T->m,T->e,T->c,T->genus,T->W);
 for(int j=0;j<T->e;j++)printf("%s%d",j?",":"",T->G[j]);
 printf("]},\"margin\":%lld}\n",S->W-T->W);fflush(stdout);
}
/* Canonical tile uses primitive RESIDUE order and first-coordinate lex minimum,
 * matching verify_probe.factor_basis. No restriction on factorization height. */
static ll supp_dep,supp_support,supp_credit,supp_kappa;
static int supp_height,supp_lowmax;
typedef struct {int u,v,next;ll cap,initial;} ClosureEdge;
typedef struct {int n,ne,*head,*level,*it,*queue;ClosureEdge *edge;} ClosureGraph;
static void closure_add(ClosureGraph *G,int u,int v,ll cap){
 G->edge[G->ne]=(ClosureEdge){u,v,G->head[u],cap,cap};G->head[u]=G->ne++;
 G->edge[G->ne]=(ClosureEdge){v,u,G->head[v],0,0};G->head[v]=G->ne++;
}
/* Dinic pattern reused from p28/genM.c, with 64-bit capacities and an exported
 * primal flow / source-side cut checked independently by verify_probe.py. */
static int closure_bfs(ClosureGraph *G,int source,int sink){
 for(int v=0;v<G->n;v++)G->level[v]=-1;int head=0,tail=0;G->queue[tail++]=source;G->level[source]=0;
 while(head<tail){int u=G->queue[head++];for(int a=G->head[u];a>=0;a=G->edge[a].next){ClosureEdge *E=&G->edge[a];if(E->cap&&G->level[E->v]<0){G->level[E->v]=G->level[u]+1;G->queue[tail++]=E->v;}}}
 return G->level[sink]>=0;
}
static ll closure_dfs(ClosureGraph *G,int u,int sink,ll amount){
 if(u==sink)return amount;
 for(int *a=&G->it[u];*a>=0;*a=G->edge[*a].next){ClosureEdge *E=&G->edge[*a];if(E->cap&&G->level[E->v]==G->level[u]+1){
  ll got=closure_dfs(G,E->v,sink,amount<E->cap?amount:E->cap);if(got){E->cap-=got;G->edge[*a^1].cap+=got;return got;}
 }}return 0;
}
static void completion_cut(int m,int e,int c,int r,int *w,int *gr,int F[MM][MM],int pool){
 int d=e-1,rho=m-r-1,inv[MM][MM],next[MM][MM],co[MM],omega[MM],original_co[MM],original_omega[MM];ll benefit=0;
 for(int s=0;s<m;s++)for(int j=0;j<d;j++){
  inv[s][j]=0;for(int k=1;k<=F[s][j];k++){int u=(s-(k*gr[j])%m+m)%m;inv[s][j]+=(u+rho)%m>(s+rho)%m;}
  int t=(s+gr[j])%m;next[s][j]=t;
  for(int a=0;a<d;a++)if(F[t][a]!=F[s][a]+(a==j)){next[s][j]=-1;break;}
 }
 for(int s=0;s<m;s++){
  int eta=0,degree=0,axes=0;for(int j=0;j<d;j++){
   int p=(s-gr[j]+m)%m;eta+=inv[s][j]-(F[s][j]?inv[p][j]:0);degree+=F[s][j];axes+=(F[s][j]*gr[j])%m;
  }omega[s]=d+degree;co[s]=eta-axes/m-degree-1;assert(co[s]<0);benefit-=co[s];
 }
 for(int s=0;s<m;s++){original_co[s]=co[s];original_omega[s]=omega[s];}
 if(pool==2){
  benefit=0;
  for(int s=0;s<m;s++){
   int raw=0;for(int j=0;j<d;j++)raw+=F[s][j]*gr[j];
   co[s]=s?-(1+raw/m):0;benefit-=co[s];
   for(int j=0;j<d;j++)if(next[s][j]>=0&&(s+rho)%m+gr[j]<m)omega[s]-=F[s][j]+1;
   assert(omega[s]>=0);
  }
 }
 int n=(pool?3:2)*m+2,source=n-2,sink=source+1;ll infinity=benefit+1;
 ClosureGraph G={.n=n};G.head=malloc(n*sizeof(int));G.level=malloc(n*sizeof(int));G.it=malloc(n*sizeof(int));G.queue=malloc(n*sizeof(int));G.edge=calloc((size_t)(6*m+8*d*m+8),sizeof(ClosureEdge));
 if(!G.head||!G.level||!G.it||!G.queue||!G.edge){perror("completion cut allocation");exit(2);}
 for(int v=0;v<n;v++)G.head[v]=-1;
 for(int s=0;s<m;s++){if(co[s]<0)closure_add(&G,source,s,-co[s]);else if(co[s]>0)closure_add(&G,s,sink,co[s]);closure_add(&G,m+s,sink,omega[s]);}
 if(pool)for(int s=0;s<m;s++)closure_add(&G,2*m+s,sink,s!=0);
 for(int s=0;s<m;s++)for(int j=0;j<d;j++)if(next[s][j]>=0){
  int t=next[s][j];closure_add(&G,t,s,infinity);closure_add(&G,t,m+s,infinity);
  if(pool){closure_add(&G,t,2*m+s,infinity);if(!F[s][j])closure_add(&G,t,2*m+(s-gr[j]+m)%m,infinity);}
 }
 ll flow=0;while(closure_bfs(&G,source,sink)){for(int v=0;v<n;v++)G.it[v]=G.head[v];ll sent;while((sent=closure_dfs(&G,source,sink,LLONG_MAX/4)))flow+=sent;}
 ll cut=0,selected_cost=0;int size=0;for(int a=0;a<G.ne;a+=2){ClosureEdge E=G.edge[a];if(G.level[E.u]>=0&&G.level[E.v]<0)cut+=E.initial;}
 for(int s=0;s<m;s++){if(G.level[s]>=0){selected_cost+=co[s];size++;}if(G.level[m+s]>=0)selected_cost+=omega[s];}
 ll global_budget=m;
 for(int s=0;s<m;s++){if(G.level[s]>=0)global_budget+=original_co[s];if(G.level[m+s]>=0)global_budget+=original_omega[s];}
 if(pool)for(int s=1;s<m;s++)if(G.level[2*m+s]>=0)selected_cost++;
 ll constant=pool==2?0:pool?1:m;
 assert(cut==flow&&constant+selected_cost==constant+flow-benefit);
 printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"rho\":%d,\"pool_mode\":%s,\"frozen_nonwrap\":%s,\"global_completion_budget\":%lld,\"budget\":%lld,\"size\":%d,\"negative_mass\":%lld,\"cut_capacity\":%lld,\"weights\":[",m,e,c,rho,pool?"true":"false",pool==2?"true":"false",global_budget,constant+flow-benefit,size,benefit,flow);
 for(int s=0;s<m;s++)printf("%s%d",s?",":"",co[s]);printf("],\"omega\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",omega[s]);printf("],\"kept\":[");int printed=0;
 for(int s=0;s<m;s++)if(G.level[s]>=0)printf("%s%d",printed++?",":"",s);printf("],\"cut\":[");printed=0;for(int v=0;v<n;v++)if(G.level[v]>=0)printf("%s%d",printed++?",":"",v);printf("],\"arcs\":[");
 for(int a=0;a<G.ne;a+=2){ClosureEdge E=G.edge[a];printf("%s[%d,%d,%lld,%lld]",a?",":"",E.u,E.v,E.initial,E.initial-E.cap);}printf("]}\n");fflush(stdout);
 int failure=constant+flow-benefit<0;free(G.head);free(G.level);free(G.it);free(G.queue);free(G.edge);if(failure)exit(5);
}
static void partial_support(int m,int e,int c,int r,int *w,int *ord,int *gr,int F[MM][MM]){
 int d=e-1,next[MM][MM],top[MM][MM],active[MM],best_active[MM],best_n=0,best_cut=-1,best_kind=-1;
 ll best=LLONG_MAX,best_dep=0,best_kappa=0,best_N=0;int rho=m-r-1,checked=0;
 for(int s=0;s<m;s++)for(int j=0;j<d;j++){
  int t=(s+gr[j])%m;next[s][j]=t;
  for(int a=0;a<d;a++)if(F[t][a]!=F[s][a]+(a==j)){next[s][j]=-1;break;}
 }
 for(int kind=0;kind<2;kind++)for(int cut=-1;cut<m;cut++){
  if(kind&&cut<0)continue;int n=0;
  for(int s=0;s<m;s++){
   active[s]=1;
   if(cut>=0){
    if(kind)active[s]=w[s]<=w[cut];
    else {int above=1;for(int j=0;j<d;j++)if(F[s][j]<F[cut][j]){above=0;break;}active[s]=!above;}
   }n+=active[s];
  }if(!n)continue;checked++;
  ll dep=0,kappa=0,N=0;
  for(int k=m-1;k>=0;k--){
   int s=ord[k];if(!active[s])continue;int maximal=1,gamma=0,axes=0;
   for(int j=0;j<d;j++){
    int t=next[s][j],successor=t>=0&&active[t];top[s][j]=successor?top[t][j]:s;
    if(successor)maximal=0;else gamma+=F[s][j]+1;
    axes+=(F[s][j]*gr[j])%m;
    N+=(s+rho)%m>(top[s][j]+rho)%m;
   }
   if(!maximal)dep+=gamma;kappa+=axes/m;
  }
  ll value=dep+N-kappa+(m-n);
  if(value<best){best=value;best_n=n;best_cut=cut;best_kind=kind;best_dep=dep;best_kappa=kappa;best_N=N;memcpy(best_active,active,m*sizeof(int));}
  if(value<0)goto finished;
 }
finished:
 printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"rho\":%d,\"checked\":%d,\"cut_kind\":\"%s\",\"cut_residue\":%d,\"size\":%d,\"missing\":%d,\"Dep\":%lld,\"N\":%lld,\"kappa\":%lld,\"budget\":%lld,\"G\":[%d",m,e,c,rho,checked,best_kind?"value_prefix":"principal_upset",best_cut,best_n,m-best_n,best_dep,best_N,best_kappa,best,m);
 for(int j=0;j<d;j++)printf(",%d",w[gr[j]]);printf("],\"kept\":[");int printed=0;
 for(int s=0;s<m;s++)if(best_active[s])printf("%s%d",printed++?",":"",s);printf("]}\n");fflush(stdout);
 if(best<0)exit(5);
}
static void supp_geometry(int m,int e,int c,int r,int *w,int *mu,int *ord,int *gen,int dump){
 int d=e-1,gr[MM],F[MM][MM]={{0}},gamma[MM]={0},maximal[MM]={0},at=0;
 for(int s=1;s<m;s++)if(gen[s])gr[at++]=s;assert(at==d);
 for(int k=1;k<m;k++){
  int s=ord[k],found=0;
  for(int j=0;j<d;j++){
   int t=(s-gr[j]+m)%m;if(w[t]+w[gr[j]]!=w[s])continue;
   int take=!found;
   if(found)for(int a=0;a<d;a++){
    int v=F[t][a]+(a==j);if(v!=F[s][a]){take=v<F[s][a];break;}
   }
   if(take)for(int a=0;a<d;a++)F[s][a]=F[t][a]+(a==j);found=1;
  }assert(found);
 }
 if(dump==2){partial_support(m,e,c,r,w,ord,gr,F);return;}
 if(dump==3||dump==4||dump==5){completion_cut(m,e,c,r,w,gr,F,dump==5?2:dump==4);return;}
 supp_dep=supp_support=supp_credit=supp_kappa=0;supp_height=supp_lowmax=0;
 ll dist_credit=0;
 for(int s=0;s<m;s++){
  int support=0,degree=0,axes=0;maximal[s]=1;
  for(int j=0;j<d;j++){
   support+=F[s][j]>0;degree+=F[s][j];axes+=(F[s][j]*gr[j])%m;
   int t=(s+gr[j])%m,successor=1;
   for(int a=0;a<d;a++)if(F[t][a]!=F[s][a]+(a==j)){successor=0;break;}
   if(successor)maximal[s]=0;else gamma[s]+=F[s][j]+1;
  }
  if(degree>supp_height)supp_height=degree;
  if(support)supp_support+=support-1;supp_kappa+=axes/m;
  if(!maximal[s])supp_dep+=gamma[s];else if(mu[s])supp_lowmax++;
  supp_credit+=(ll)gamma[s]*mu[s];dist_credit+=(ll)gamma[s]*((r-s+m)%m);
 }
 ll C=(ll)(e-2)*m*(m-1)/2,genus=0;for(int s=1;s<m;s++)genus+=w[s]/m;
 ll W=(ll)e*(c-genus)-c;assert((dist_credit-C)%m==0);
 assert(W==supp_credit+(dist_credit-C)/m);
 if(dump){
  printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"g\":%lld,\"W\":%lld,\"canonical_height\":%d,\"Dep\":%lld,\"support_sum\":%lld,\"kappa\":%lld,\"gamma_mu\":%lld,\"low_maximal\":%d,\"G\":[%d",m,e,c,genus,W,supp_height,supp_dep,supp_support,supp_kappa,supp_credit,supp_lowmax,m);
  for(int j=0;j<d;j++)printf(",%d",w[gr[j]]);
  printf("],\"gamma\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",gamma[s]);printf("]}\n");fflush(stdout);
 }
}
static ll residual_assignment(int m,int *w,int *mu,int *U,int q,int rho,int r,
 int *count,int *res,int *perm,ll *alpha,ll *beta,int equality){
 int ix[MM],n=0;for(int s=0;s<m;s++){ix[s]=-1;if(U[s]){ix[s]=n;res[n++]=s;}}
 int cls[MM];for(int s=0;s<m;s++)cls[s]=s;
 if(equality)for(int i=1;i<m;i++)for(int j=i;j<m;j++){
  int s=(i+j)%m;if(!s||w[i]+w[j]!=w[s])continue;
  int rp=(w[s]-(q*m-rho))%m;if(rp<0)rp+=m;
  int lo=rp>=m-rho&&i>r&&j>r,up=rp<=m-rho-2&&i<=r&&j<=r,tau=mu[i]+mu[j]-mu[s]-q;
  if(tau+lo||up-tau)continue;
  if(!U[i])cls[root(cls,j)]=root(cls,s);
  if(!U[j])cls[root(cls,i)]=root(cls,s);
 }
 int (*H)[MM]=calloc(MM,sizeof(*H));if(!H){perror("residual assignment");exit(2);}
 for(int i=1;i<m;i++)for(int j=i;j<m;j++){
  int s=(i+j)%m;if(!s||w[i]+w[j]!=w[s])continue;
  int rp=(w[s]-(q*m-rho))%m;if(rp<0)rp+=m;
  int lo=rp>=m-rho&&i>r&&j>r,tau=mu[i]+mu[j]-mu[s]-q;
  int d=U[i]+U[j]-U[s]-tau-lo;if(d<=0)continue;assert(ix[i]>=0&&ix[j]>=0);
  if(d>H[ix[i]][ix[j]])H[ix[i]][ix[j]]=H[ix[j]][ix[i]]=d;
 }
 if(equality){
  int (*Q)[MM]=calloc(MM,sizeof(*Q));if(!Q){perror("equality assignment");exit(2);}
  for(int a=0;a<n;a++)for(int b=0;b<n;b++){
   int x=root(cls,res[a]),y=root(cls,res[b]);assert(U[x]==U[res[a]]&&U[y]==U[res[b]]);
   if(H[a][b]>Q[x][y])Q[x][y]=H[a][b];
  }
  for(int a=0;a<n;a++)for(int b=0;b<n;b++)H[a][b]=Q[root(cls,res[a])][root(cls,res[b])];
  free(Q);
 }
 ll M=assignment(n,H,perm,alpha,beta);free(H);*count=n;return M;
}
static int eval(int m,int *G,int ng,int mine,int dump,ll *best){
 int w[MM],done[MM]={0},ord[MM],gen[MM],mu[MM],z[MM],h[MM]={0};
 w[0]=0;for(int s=1;s<m;s++)w[s]=1<<28;
 for(int k=0;k<m;k++){int u=-1;for(int s=0;s<m;s++)if(!done[s]&&(u<0||w[s]<w[u]))u=s;
  if(w[u]==1<<28)return 0;done[u]=1;ord[k]=u;
  for(int a=1;a<ng;a++){int v=w[u]+G[a],s=v%m;if(v<w[s])w[s]=v;}}
 int r=0;ll genus=0;for(int s=1;s<m;s++){if(w[s]>w[r])r=s;genus+=w[s]/m;gen[s]=1;}
 for(int i=1;i<m;i++)for(int j=i;j<m;j++){int s=(i+j)%m;if(s&&w[i]+w[j]==w[s])gen[s]=0;}
 int e=1;for(int s=1;s<m;s++)e+=gen[s];int c=w[r]-m+1;if(e<mine||c<=4*m||3*e>=m||(need_e&&e!=need_e)||(kunz_cap&&w[r]/m>kunz_cap))return 0;
 int q=(c+m-1)/m,rho=q*m-c;mu[0]=z[0]=q;
 for(int s=1;s<m;s++)mu[s]=w[s]>=c?0:(c-w[s]+m-1)/m;
 int hh=0;
 for(int k=1;k<m;k++){int s=ord[k];z[s]=gen[s]?mu[s]:0;h[s]=gen[s];
  for(int i=1;i<m;i++){int j=(s-i+m)%m;if(!j||j<i||w[i]+w[j]!=w[s])continue;
   int rp=(w[s]-c)%m;if(rp<0)rp+=m;int up=rp<=m-rho-2&&i<=r&&j<=r;
   int v=z[i]+z[j]-q-up;if(v>z[s])z[s]=v;v=h[i]+h[j];if(v>h[s])h[s]=v;
  }if(h[s]>hh)hh=h[s];if(z[s]>mu[s]){fprintf(stderr,"invalid bound\n");exit(2);}}
 ll Z=0;for(int s=0;s<m;s++)Z+=z[s];ll B=e*Z-c,W=(ll)e*(c-genus)-c;
 if(dump>=11&&dump<=16){supp_geometry(m,e,c,r,w,mu,ord,gen,dump==16?5:dump==15?4:dump==14?3:dump==13?2:dump==11);last_e=e;last_c=c;last_W=W;return 1;}
 if(dump==10){
  printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"g\":%lld,\"W\":%lld,\"q\":%d,\"rho\":%d,\"r\":%d,\"generators\":[%d",m,e,c,genus,W,q,rho,r,m);
  for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);
  printf("],\"w\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",w[s]);
  printf("],\"mu\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",mu[s]);
  printf("],\"height\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",h[s]);
  printf("],\"pairs\":[");int printed=0;
  for(int i=1;i<m;i++)for(int j=i;j<m;j++){
   int s=(i+j)%m;if(!s)continue;int rp=(w[s]-c)%m;if(rp<0)rp+=m;
   int lo=rp>=m-rho&&i>r&&j>r,up=rp<=m-rho-2&&i<=r&&j<=r;
   int J=(w[i]+w[j]-w[s])/m,tau=mu[i]+mu[j]-mu[s]-q+J;
   printf("%s[%d,%d,%d,%d,%d,%d,%d]",printed++?",":"",i,j,s,J,tau,lo,up);
  }printf("],\"models\":{}}\n");return 1;
 }
 if(unit_audit||combined_audit||dump==6||dump==7||dump==8||dump==9){
  /* Nonnegative capped x obeys xi<=xs+alpha, xj<=xs+alpha and
   * xs<=xi+xj+kappa. Starting at delta gives valid integer upper bounds.
   * Real mode uses the weaker repeated-parent rule xi<=xs+alpha.
   * Integer modes additionally floor the exact repeated-parent constraint. */
  int U[MM],changed=1,sweeps=0;for(int s=0;s<m;s++)U[s]=mu[s]-z[s];
  while(changed){changed=0;sweeps++;
   for(int i=1;i<m;i++)for(int j=i;j<m;j++){
    int s=(i+j)%m;if(!s||w[i]+w[j]!=w[s])continue;
    int rp=(w[s]-c)%m;if(rp<0)rp+=m;
    int lo=rp>=m-rho&&i>r&&j>r,up=rp<=m-rho-2&&i<=r&&j<=r;
    int tau=mu[i]+mu[j]-mu[s]-q,a=tau+lo,k=up-tau;
    if(U[i]>U[s]+a){U[i]=U[s]+a;changed=1;}
    if(U[j]>U[s]+a){U[j]=U[s]+a;changed=1;}
    if(U[s]>U[i]+U[j]+k){U[s]=U[i]+U[j]+k;changed=1;}
    if((dump==8||dump==9||combined_audit)&&i==j&&U[i]>(U[s]+a)/2){U[i]=(U[s]+a)/2;changed=1;}
   }
  }
  ll unpaid=0;int target=0;for(int s=1;s<m;s++){
   unpaid+=U[s];int eligible=1;
   if(unit_audit==3)for(int g=1;g<m;g++)if(gen[g]&&w[s]+w[g]!=w[(s+g)%m]){eligible=0;break;}
   if(eligible&&U[s]>U[target])target=s;
  }
  ll bound=W-e*unpaid;
  int n=0,res[MM],perm[MM];ll alpha[MM],beta[MM],M=0;
  if(dump==7||dump==8||dump==9||combined_audit)M=residual_assignment(m,w,mu,U,q,rho,r,&n,res,perm,alpha,beta,dump==9);
  ll phi=bound+e*((M+1)/2);
  if(dump==6||dump==7||dump==8||dump==9||((unit_audit==1||unit_audit==3)&&U[target]>1)||(unit_audit==2&&(bound<*best||bound<0))){
   printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"W\":%lld,\"B\":%lld,\"integer\":%s,\"equality\":%s,\"bound\":%lld,\"unpaid\":%lld,\"target\":%d,\"max_upper\":%d,\"sweeps\":%d,\"G\":[%d",m,e,c,W,B,(dump==8||dump==9)?"true":"false",dump==9?"true":"false",bound,unpaid,target,U[target],sweeps,m);
   for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("],\"b\":[");
   for(int s=0;s<m;s++)printf("%s%d",s?",":"",z[s]);printf("],\"u\":[");
   for(int s=0;s<m;s++)printf("%s%d",s?",":"",U[s]);printf("]");
   if(unit_audit==3)printf(",\"interior_target\":true");
   if(dump==7||dump==8||dump==9){
    printf(",\"residual_matching\":{\"M\":%lld,\"rounded_bound\":%lld,\"residues\":[",M,bound+e*((M+1)/2));
    for(int a=0;a<n;a++)printf("%s%d",a?",":"",res[a]);printf("],\"permutation\":[");
    for(int a=0;a<n;a++)printf("%s%d",a?",":"",perm[a]);printf("],\"alpha\":[");
    for(int a=0;a<n;a++)printf("%s%lld",a?",":"",alpha[a]);printf("],\"beta\":[");
    for(int a=0;a<n;a++)printf("%s%lld",a?",":"",beta[a]);printf("]}");
   }
   printf("}\n");fflush(stdout);
  }
  if(combined_audit){
   last_W=W;last_B=B;last_M=M;last_corrected=last_individual=phi;last_propagated=bound;
   last_e=e;last_c=c;last_q=q;last_h=hh;last_num=0;last_den=1;
   if(phi<0){printf("COMBINED_BOUND_FAILURE phi=%lld W=%lld G=[%d",phi,W,m);for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("]\n");return -5;}
   return 1;
  }
  if(unit_audit==2){if(bound<*best)*best=bound;if(B<0)nbneg++;return bound<0?-4:1;}
  return (unit_audit==1||unit_audit==3)&&U[target]>1?-3:1;
 }
 int ix[MM],res[MM],n=0;for(int s=1;s<m;s++){ix[s]=-1;if(!gen[s]){ix[s]=n;res[n++]=s;}}
 if(dump==5){
  printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"W\":%lld,\"B\":%lld,\"G\":[%d",m,e,c,W,B,m);
  for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("],\"b\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",z[s]);printf("],\"transport\":{");
  for(int mode=0;mode<3;mode++){
   int *cost=malloc((size_t)m*m*sizeof(int));if(!cost){perror("transport graph");exit(2);}
   for(size_t k=0;k<(size_t)m*m;k++)cost[k]=INT_MAX/4;
   int dist[MM],parent[MM],settled[MM]={0},used_anchor[MM]={0};
   for(int i=1;i<m;i++)for(int j=i;j<m;j++){
    int s=(i+j)%m;if(!s||w[i]+w[j]!=w[s])continue;
    int rp=(w[s]-c)%m;if(rp<0)rp+=m;
    int lo=rp>=m-rho&&i>r&&j>r,up=rp<=m-rho-2&&i<=r&&j<=r;
    int tau=mu[i]+mu[j]-mu[s]-q,a=tau+lo,k=up-tau;
    assert(a>=0&&a<=1&&k>=0&&k<=1);
    for(int side=0;side<2;side++){
     int anchor=side?i:j,v=side?j:i;
     if(mode<2&&!(mode?mu[anchor]==z[anchor]:gen[anchor]))continue;
     used_anchor[anchor]=1;
     int forward=k+(mode==2?mu[anchor]-z[anchor]:0);
     if(a<cost[s*m+v])cost[s*m+v]=a;
     if(forward<cost[v*m+s])cost[v*m+s]=forward;
    }
   }
   for(int s=0;s<m;s++){dist[s]=mu[s]-z[s];parent[s]=-1;}
   for(int t=0;t<m;t++){
    int u=-1;for(int s=0;s<m;s++)if(!settled[s]&&(u<0||dist[s]<dist[u]))u=s;
    settled[u]=1;
    for(int v=0;v<m;v++)if(!settled[v]&&cost[u*m+v]<INT_MAX/4&&dist[u]+cost[u*m+v]<dist[v]){
     dist[v]=dist[u]+cost[u*m+v];parent[v]=u;
    }
   }
   ll unpaid=0;int composites=0;for(int s=0;s<m;s++){unpaid+=dist[s];if(s&&!gen[s]&&used_anchor[s])composites++;}
   const char *name=mode==0?"generators":mode==1?"zero_loss":"capped_pairs";
   printf("%s\"%s\":{\"bound\":%lld,\"unpaid\":%lld,\"used_composite_summands\":%d,\"u\":[",mode?",":"",name,W-e*unpaid,unpaid,composites);
   for(int s=0;s<m;s++)printf("%s%d",s?",":"",dist[s]);printf("],\"parent\":[");
   for(int s=0;s<m;s++)printf("%s%d",s?",":"",parent[s]);printf("]}");free(cost);
  }
  printf("}}\n");return 1;
 }
 if(dump==3){
  /* A feasible pair cover is an UPPER bound on M/2, not a Wilf lower bound.
   * Large Apéry elements cannot pair with one another. Reduce their cover to
   * the generator-forced demand, then pay every low/high edge at its low end. */
  ll v[MM]={0},total=0;
  for(int a=0;a<n;a++){int s=res[a];if(2LL*w[s]<=w[r])v[a]=mu[s]-z[s];}
  for(int i=1;i<m;i++)if(gen[i])for(int a=0;a<n;a++){
   int j=res[a],s=(i+j)%m;if(!s||w[i]+w[j]!=w[s])continue;
   int rp=(w[s]-c)%m;if(rp<0)rp+=m;int lo=rp>=m-rho&&i>r&&j>r;
   ll d=q-lo-z[i]-z[j]+z[s];if(d>v[a])v[a]=d;
  }
  for(int a=0;a<n;a++)if(2LL*w[res[a]]<=w[r])for(int b=0;b<n;b++)if(2LL*w[res[b]]>w[r]){
   int i=res[a],j=res[b],s=(i+j)%m;if(!s||w[i]+w[j]!=w[s])continue;
   int rp=(w[s]-c)%m;if(rp<0)rp+=m;int lo=rp>=m-rho&&i>r&&j>r;
   ll d=q-lo-z[i]-z[j]+z[s];if(d-v[b]>v[a])v[a]=d-v[b];
  }
  for(int a=0;a<n;a++)total+=v[a];
  printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"W\":%lld,\"B\":%lld,\"cover_sum\":%lld,\"matching_bound_upper\":%lld,\"G\":[%d",m,e,c,W,B,total,B+e*total,m);
  for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("],\"b\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",z[s]);
  printf("],\"residues\":[");for(int a=0;a<n;a++)printf("%s%d",a?",":"",res[a]);
  printf("],\"cover\":[");for(int a=0;a<n;a++)printf("%s%lld",a?",":"",v[a]);printf("]}\n");
  if(B+e*total<0)printf("BOUND_FAILURE_CERTIFIED_BY_COVER W=%lld upper=%lld\n",W,B+e*total);
  return 1;
 }
 static int (*A)[MM];if(!A){A=calloc(MM,sizeof(*A));if(!A){perror("assignment matrix");exit(2);}}
 memset(A,0,MM*sizeof(*A));int perm[MM];ll alpha[MM],beta[MM],match=0;
 if(B<0||dump==2||dump==4){
  for(int i=1;i<m;i++)for(int j=i;j<m;j++){int s=(i+j)%m;if(!s||w[i]+w[j]!=w[s])continue;
   int rp=(w[s]-c)%m;if(rp<0)rp+=m;int lo=rp>=m-rho&&i>r&&j>r;
   int demand=q-lo-z[i]-z[j]+z[s];if(demand<=0)continue;
   int a=ix[i],b=ix[j];if(a<0&&b<0){fprintf(stderr,"impossible generator demand\n");exit(2);}
   if(a<0||b<0){int k=a<0?b:a;if(2*demand>A[k][k])A[k][k]=2*demand;}
   else if(demand>A[a][b]){A[a][b]=A[b][a]=demand;}
  }
  match=assignment(n,A,perm,alpha,beta);
 }
 int individual_lower[MM]={0};ll individual_sum=0,individual_bound=B;
 if((individual_audit&&B<0)||dump==4){
  for(int a=0;a<n;a++){
   individual_lower[a]=(A[a][a]+1)/2;
   for(int b=0;b<n;b++){int v=A[a][b]-(mu[res[b]]-z[res[b]]);if(v>individual_lower[a])individual_lower[a]=v;}
   individual_sum+=individual_lower[a];
  }
  individual_bound=B+e*individual_sum;
 }
 ll corrected=B+(ll)e*((match+1)/2);
 last_num=B<0?-2*B:0;last_den=B<0?e*match:1;
 last_corrected=corrected;last_B=B;last_M=match;last_W=W;
 last_individual=individual_bound;
 last_e=e;last_c=c;last_q=q;last_h=hh;
 if(B<0){
  nbneg++;
  ll num=-2*B,den=e*match;
  if(dump==1&&num*ratio_den>ratio_num*den){
   ratio_num=num;ratio_den=den;
   printf("REPAIR_TIGHT ratio=%lld/%lld corrected=%lld B=%lld M=%lld W=%lld G=[%d",num,den,corrected,B,match,W,m);
   for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("]\n");
  }
 }
 if(corrected<*best){*best=corrected;if(dump==1)printf("NEW_MIN corrected=%lld B=%lld M=%lld W=%lld m=%d e=%d q=%d h=%d\n",corrected,B,match,W,m,e,q,hh);}
 if(dump==2||dump==4){
  printf("{\"m\":%d,\"e\":%d,\"c\":%d,\"W\":%lld,\"B\":%lld,\"M\":%lld,\"corrected\":%lld,\"G\":[%d",m,e,c,W,B,match,corrected,m);
  for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("],\"b\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",z[s]);
  printf("],\"residues\":[");for(int a=0;a<n;a++)printf("%s%d",a?",":"",res[a]);
  printf("],\"permutation\":[");for(int a=0;a<n;a++)printf("%s%d",a?",":"",perm[a]);
  printf("],\"alpha\":[");for(int a=0;a<n;a++)printf("%s%lld",a?",":"",alpha[a]);
  printf("],\"beta\":[");for(int a=0;a<n;a++)printf("%s%lld",a?",":"",beta[a]);printf("]");
  if(dump==4){
   int lower[MM]={0};ll sumlower=0;
   for(int a=0;a<n;a++)for(int b=0;b<n;b++){
    int v=A[a][b]-(mu[res[b]]-z[res[b]]);if(v>lower[a])lower[a]=v;
   }
   for(int a=0;a<n;a++){sumlower+=lower[a];for(int b=0;b<n;b++){
    A[a][b]-=lower[a]+lower[b];if(A[a][b]<0)A[a][b]=0;
   }}
   ll residual=assignment(n,A,perm,alpha,beta);
   printf(",\"individual_bound\":%lld,\"individual_lower\":[",individual_bound);
   for(int a=0;a<n;a++)printf("%s%d",a?",":"",individual_lower[a]);
   printf("],\"capacity_M\":%lld,\"capacity_value_twice\":%lld,\"capacity_gap_twice\":%lld,\"capacity_lower\":[",residual,2*sumlower+residual,2*sumlower+residual-match);
   for(int a=0;a<n;a++)printf("%s%d",a?",":"",lower[a]);
   printf("],\"capacity_permutation\":[");for(int a=0;a<n;a++)printf("%s%d",a?",":"",perm[a]);
   printf("],\"capacity_alpha\":[");for(int a=0;a<n;a++)printf("%s%lld",a?",":"",alpha[a]);
   printf("],\"capacity_beta\":[");for(int a=0;a<n;a++)printf("%s%lld",a?",":"",beta[a]);printf("]");
  }
  printf("}\n");
 }
 if(W<0||corrected<0){printf("%s corrected=%lld B=%lld M=%lld W=%lld m=%d e=%d c=%d q=%d rho=%d h=%d G=[%d",W<0?"WILF_FAILURE":"BOUND_FAILURE",corrected,B,match,W,m,e,c,q,rho,hh,m);
  for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("]\n");fflush(stdout);return -1;}

 if(individual_audit&&B<0&&individual_bound<0){
  printf("INDIVIDUAL_BOUND_FAILURE individual=%lld B=%lld M=%lld corrected=%lld W=%lld c=%d G=[%d",individual_bound,B,match,corrected,W,c,m);
  for(int s=1;s<m;s++)if(gen[s])printf(",%d",w[s]);printf("]\n");fflush(stdout);return -2;
 }
 return 1;
}
int main(int argc,char **argv){
 if(argc>2&&!strcmp(argv[1],"--differential-audit")){
  int ng=argc-2,G[MM];if(ng>MM)return 2;for(int j=0;j<ng;j++)G[j]=atoi(argv[j+2]);return differential_audit(G,ng);
 }
 if(argc>2&&!strcmp(argv[1],"--odd-audit")){
  int G[MM],ng=argc-2,a;if(ng>MM)return 2;for(int j=0;j<ng;j++)G[j]=atoi(argv[j+2]);
  ResidueStats S,U;if(!odd_compare(G,ng,&S,&U,&a))return 2;print_odd_stats(&S,&U,a);return 0;
 }
 if(argc>5&&!strcmp(argv[1],"--odd-climb")){
  int limit=atoi(argv[2]),ng=argc-3,G[MM];if(limit<0||limit>20||ng>MM)return 2;
  for(int j=0;j<ng;j++)G[j]=atoi(argv[j+3]);long calls=0,accepted=0;
  for(int iter=0;;iter++){
   ResidueStats S,U;int a;
   if(!odd_compare(G,ng,&S,&U,&a)||S.m!=G[0]||3*S.e>=S.m||S.c<=4*S.m)return 2;
   ll num=S.W-U.W;int den=S.c;ll W0=S.W;int c0=S.c;
   printf("ODD_CLIMB iter=%d calls=%ld accepted=%ld score=%lld/%d\n",iter,calls,accepted,num,den);print_odd_stats(&S,&U,a);
   if(num<0||iter==limit){printf("ODD_STOP reason=%s\n",num<0?"descent_inequality_failure":"iteration_limit");return 0;}
   int found=0,BG[MM];
   for(int j=0;j<ng;j++){
    int lo=j?G[0]+1:3,hi=j?8*G[0]:MM-1;if(!j)for(int b=1;b<ng;b++)if(G[b]-1<hi)hi=G[b]-1;
    for(int v=lo;v<=hi;v++){
     if(v==G[j])continue;int A[MM];memcpy(A,G,ng*sizeof(int));A[j]=v;calls++;
     if(!odd_compare(A,ng,&S,&U,&a)||S.m!=A[0]||3*S.e>=S.m||S.c<=4*S.m)continue;accepted++;
     ll nn=S.W-U.W;int dd=S.c;
     if((__int128)nn*den<(__int128)num*dd||((__int128)nn*den==(__int128)num*dd&&(__int128)S.W*c0<(__int128)W0*S.c)){num=nn;den=dd;W0=S.W;c0=S.c;memcpy(BG,A,ng*sizeof(int));found=1;}
     if(nn<0){print_odd_stats(&S,&U,a);printf("ODD_STOP reason=descent_inequality_failure calls=%ld\n",calls);return 0;}
    }
   }
   if(!found){printf("ODD_STOP reason=local_optimum calls=%ld accepted=%ld\n",calls,accepted);return 0;}
   memcpy(G,BG,ng*sizeof(int));
  }
 }
 if(argc>2&&!strcmp(argv[1],"--residue-audit")){
  int G[MM],ng=argc-2;if(ng>MM)return 2;for(int j=0;j<ng;j++)G[j]=atoi(argv[j+2]);
  ResidueStats S,T;if(!residue_compare(G,ng,&S,&T))return 2;print_residue_stats(&S,&T);return 0;
 }
 if(argc>5&&!strcmp(argv[1],"--residue-climb")){
  int limit=atoi(argv[2]),ng=argc-3,G[MM];if(limit<0||limit>30||ng>MM)return 2;
  for(int j=0;j<ng;j++)G[j]=atoi(argv[j+3]);long calls=0,accepted=0;
  for(int iter=0;;iter++){
   ResidueStats S,T;if(!residue_compare(G,ng,&S,&T)||S.m!=G[0]||3*S.e>=S.m||S.c<=4*S.m||T.W<=0||2*S.W>=(ll)(T.e-2)*T.c)return 2;
   ll num=S.W-T.W;int den=S.c;ll W0=S.W;int c0=S.c;
   printf("RESIDUE_CLIMB iter=%d calls=%ld accepted=%ld score=%lld/%d\n",iter,calls,accepted,num,den);print_residue_stats(&S,&T);
   if(num<0||iter==limit){printf("RESIDUE_STOP reason=%s\n",num<0?"descent_inequality_failure":"iteration_limit");return 0;}
   int found=0,BG[MM];
   for(int a=0;a<ng;a++){
    int lo=a?G[0]+1:3,hi=a?8*G[0]:MM-1;if(!a)for(int b=1;b<ng;b++)if(G[b]-1<hi)hi=G[b]-1;
    for(int v=lo;v<=hi;v++){
     if(v==G[a])continue;int A[MM];memcpy(A,G,ng*sizeof(int));A[a]=v;calls++;
     if(!residue_compare(A,ng,&S,&T)||S.m!=A[0]||3*S.e>=S.m||S.c<=4*S.m||T.W<=0||2*S.W>=(ll)(T.e-2)*T.c)continue;accepted++;
     ll nn=S.W-T.W;int dd=S.c;
     if((__int128)nn*den<(__int128)num*dd||((__int128)nn*den==(__int128)num*dd&&(__int128)S.W*c0<(__int128)W0*S.c)){num=nn;den=dd;W0=S.W;c0=S.c;memcpy(BG,A,ng*sizeof(int));found=1;}
     if(nn<0){print_residue_stats(&S,&T);printf("RESIDUE_STOP reason=descent_inequality_failure calls=%ld\n",calls);return 0;}
    }
   }
   if(!found){printf("RESIDUE_STOP reason=local_optimum calls=%ld accepted=%ld\n",calls,accepted);return 0;}
   memcpy(G,BG,ng*sizeof(int));
  }
 }
 if(argc>6&&!strcmp(argv[1],"--supp-climb")){
  /* Bounded falsification only. mode=cycle tests Delta<=binom(d,2);
   * mode=weighted tests Gamma.mu>=support_sum after the proved shape/flat
   * exclusions. Neither a positive run nor a local optimum is a theorem. */
  int weighted=!strcmp(argv[2],"weighted"),limit=atoi(argv[3]),ng=argc-4,G[MM];
  if((!weighted&&strcmp(argv[2],"cycle"))||limit<0||limit>30||ng>MM)return 2;
  for(int a=0;a<ng;a++)G[a]=atoi(argv[a+4]);ll unused=LLONG_MAX;long calls=0,accepted=0;
  if(G[0]<2||G[0]>=MM)return 2;
  for(int a=1;a<ng;a++)if(G[a]<=G[0])return 2;
  for(int iter=0;;iter++){
   if(!eval(G[0],G,ng,2,12,&unused))return 2;calls++;
   if(supp_dep>=supp_support||(weighted&&supp_height<=2)){fprintf(stderr,"seed excluded by shape/flat theorem\n");return 2;}
   ll num=weighted?supp_credit-supp_support:supp_support-supp_dep-(ll)(last_e-1)*(last_e-2)/2;
   int den=weighted?last_c:1;ll W0=last_W;int c0=last_c;
   printf("SUPP_CLIMB mode=%s iter=%d calls=%ld accepted=%ld score=%lld/%d\n",argv[2],iter,calls,accepted,num,den);
   eval(G[0],G,ng,2,11,&unused);
   if((weighted?num<0:num>0)||iter==limit){printf("SUPP_STOP reason=%s\n",(weighted?num<0:num>0)?"intermediate_inequality_failure":"iteration_limit");return 0;}
   int found=0,BG[MM];
   for(int a=0;a<ng;a++){
    int lo=a?G[0]+1:3*(ng-1)+1,hi=a?8*G[0]:MM-1;
    if(!a)for(int b=1;b<ng;b++)if(G[b]-1<hi)hi=G[b]-1;
    for(int v=lo;v<=hi;v++){
     if(v==G[a])continue;int T[MM];memcpy(T,G,ng*sizeof(int));T[a]=v;
     calls++;if(!eval(T[0],T,ng,2,12,&unused))continue;
     if(supp_dep>=supp_support||(weighted&&supp_height<=2))continue;accepted++;
     ll nn=weighted?supp_credit-supp_support:supp_support-supp_dep-(ll)(last_e-1)*(last_e-2)/2;
     int dd=weighted?last_c:1;
     int better=weighted?nn*den<num*dd:nn>num;
     if((ll)nn*den==(ll)num*dd&&last_W*c0<W0*last_c)better=1;
     if(better){num=nn;den=dd;W0=last_W;c0=last_c;memcpy(BG,T,ng*sizeof(int));found=1;}
     if(weighted?nn<0:nn>0){eval(T[0],T,ng,2,11,&unused);printf("SUPP_STOP reason=intermediate_inequality_failure calls=%ld\n",calls);return 0;}
    }
   }
   if(!found){printf("SUPP_STOP reason=local_optimum calls=%ld accepted=%ld\n",calls,accepted);return 0;}
   memcpy(G,BG,ng*sizeof(int));
  }
 }
 if(argc>3&&(!strcmp(argv[1],"--supp-audit")||!strcmp(argv[1],"--partial-support-audit")||!strcmp(argv[1],"--support-cut")||!strcmp(argv[1],"--support-pool-cut")||!strcmp(argv[1],"--support-frozen-cut"))){
  int G[MM],ng=argc-2;ll unused=LLONG_MAX;if(ng>MM)return 2;
  for(int a=0;a<ng;a++)G[a]=atoi(argv[a+2]);if(G[0]<2||G[0]>=MM)return 2;
  for(int a=1;a<ng;a++)if(G[a]<=G[0])return 2;
  return eval(G[0],G,ng,2,!strcmp(argv[1],"--support-frozen-cut")?16:!strcmp(argv[1],"--support-pool-cut")?15:!strcmp(argv[1],"--support-cut")?14:!strcmp(argv[1],"--partial-support-audit")?13:11,&unused)?0:2;
 }
 if(argc==3&&!strcmp(argv[1],"--axis-flow"))return axis_flow(argv[2]);
 if(argc>1&&!strcmp(argv[1],"--weighted-search")){unit_audit=2;argc--;argv++;}
 if(argc>1&&!strcmp(argv[1],"--unit-search")){unit_audit=1;argc--;argv++;}
 if(argc>1&&!strcmp(argv[1],"--interior-unit-search")){unit_audit=3;argc--;argv++;}
 if(argc>1&&!strcmp(argv[1],"--individual-search")){individual_audit=1;argc--;argv++;}
 if(argc==3&&!strcmp(argv[1],"--position-audit")){
  int maxm=atoi(argv[2]);if(maxm<2||maxm>128)return 1;ll checks=0;
  for(int m=2;m<=maxm;m++)for(int r=0;r<m;r++)for(int i=1;i<m;i++)for(int j=i;j<m;j++){
   int s=(i+j)%m;if(!s)continue;int rho=m-r-1,rp=(s+rho)%m;
   int up=rp<=r-1&&i<=r&&j<=r;
   int tau=(i+j>m)+(s>r)-(i>r)-(j>r),k=up-tau;
   int closed=(i<=r&&j<=r&&i+j<=2*r-m)+(i>r&&j>r&&i+j<=m+r);
   assert(k==closed);
   int lo=rp>=r+1&&i>r&&j>r,a=tau+lo;
   int lower=(i<=r&&j<=r&&i+j>r)+(i>r&&j>r&&i+j>m+2*r+1);
   assert(a==lower);
   if((i<=r)!=(j<=r))assert(a==0&&k==0);
   if(r==m-1&&a==0&&k==0)assert(s==r);
   if((i<=r&&i>=2*r-m)||(j<=r&&j>=2*r-m))assert(k==0);
   if(j==m-1&&k)assert(s==r);
   checks++;
  }
  printf("POSITION_IDENTITY_CHECKED max_m=%d pairs=%lld\n",maxm,checks);return 0;
 }
 if(argc>4&&(!strcmp(argv[1],"--climb")||!strcmp(argv[1],"--climb-wide")||!strcmp(argv[1],"--wilf-climb")||!strcmp(argv[1],"--wilf-climb-wide")||!strcmp(argv[1],"--wilf-negative-wide")||!strcmp(argv[1],"--individual-climb-wide")||!strcmp(argv[1],"--combined-climb-wide"))){
  combined_audit=strstr(argv[1],"combined")!=NULL;
  int indiv=strstr(argv[1],"individual")!=NULL||combined_audit;
  int wide=strstr(argv[1],"wide")!=NULL,wilf=strstr(argv[1],"wilf")!=NULL||indiv,negative=strstr(argv[1],"negative")!=NULL||indiv;
  if(indiv&&!combined_audit)individual_audit=1;
  int ng=argc-2,G0[GG],m=atoi(argv[2]);if(ng>GG||m<2||m>=MM)return 1;
  for(int a=0;a<ng;a++)G0[a]=atoi(argv[a+2]);
  ll best0=1LL<<60;
  int initial=eval(m,G0,ng,4,0,&best0);if(initial<=0)return initial?0:1;
  if(negative&&last_B>=0)return 1;
  need_e=last_e;int iter=0,announced=0;long calls=1;
  for(;;){
   int ret=eval(m,G0,ng,4,0,&best0);if(ret<0)return 0;
   ll num=last_num,den=last_den,W0=last_W,I0=last_individual;int c0=last_c;
   if(combined_audit)printf("COMBINED_CLIMB iter=%d phi=%lld propagated=%lld residual_M=%lld W=%lld c=%d q=%d h=%d G=[",iter,last_individual,last_propagated,last_M,last_W,last_c,last_q,last_h);
   else printf("%s iter=%d ratio=%lld/%lld corrected=%lld B=%lld M=%lld W=%lld c=%d q=%d h=%d G=[",indiv?"INDIVIDUAL_CLIMB":wilf?"WILF_CLIMB":"CLIMB",iter,num,den,last_corrected,last_B,last_M,last_W,last_c,last_q,last_h);
   for(int a=0;a<ng;a++)printf("%s%d",a?",":"",G0[a]);printf("]");if(indiv&&!combined_audit)printf(" individual=%lld",I0);printf("\n");fflush(stdout);
   if(negative&&!indiv&&2*last_W<last_c&&!announced){printf("NEGATIVE_BASELINE_DICHOTOMY_FAILURE\n");announced=1;}
   if(iter++>=100){printf("ITERATION_LIMIT calls=%ld\n",calls);return 0;}
   int BG[GG],found=0;
   for(int a=0;a<ng;a++){
    int minm=3*need_e+1,maxm=MM-1;for(int b=1;b<ng;b++)if(G0[b]-1<maxm)maxm=G0[b]-1;
    if(wilf&&minm<20)minm=20; /* m<=19 is already proved; diagnostic search only. */
    int limit=wide?(a==0?maxm-minm+1:7*m):10;
    for(int k=0;k<limit;k++){
     int step=wide?0:(int[]){-m,-8,-4,-2,-1,1,2,4,8,m}[k];
     if(!wide&&a==0&&step!=1&&step!=-1)continue;
     int T[GG];memcpy(T,G0,ng*sizeof(int));T[a]=wide?(a==0?minm+k:m+1+k):T[a]+step;int mm=T[0];
    if(mm<4||mm>=MM||(wilf&&mm<20))continue;
    int ok=1;for(int b=1;b<ng;b++)if(T[b]<=mm)ok=0;if(!ok)continue;
    ret=eval(mm,T,ng,4,0,&best0);calls++;if(ret<0){printf("CLIMB_FAILURE calls=%ld\n",calls);return 0;}if(!ret||(negative&&last_B>=0))continue;
    ll nn=last_num,dd=last_den;
    int improve=indiv?(last_individual*c0<I0*last_c||(last_individual*c0==I0*last_c&&last_W*c0<W0*last_c)):wilf?(last_W*c0<W0*last_c||(last_W*c0==W0*last_c&&last_W<W0)):(nn*den>num*dd||(nn*den==num*dd&&last_W*c0<W0*last_c));
    if(improve){
     num=nn;den=dd;W0=last_W;I0=last_individual;c0=last_c;memcpy(BG,T,ng*sizeof(int));found=1;
    }
    }
   }
   if(!found){printf("LOCAL_OPTIMUM calls=%ld\n",calls);return 0;}
   memcpy(G0,BG,ng*sizeof(int));m=G0[0];
  }
 }
 if(argc==4&&!strcmp(argv[1],"--truncscan")){
  long N=atol(argv[2]);state=strtoull(argv[3],NULL,10);if(!state)state=1;
  long accepted=0;ll best0=1LL<<60;
  for(long t=0;t<N;t++){
   int m=20+pick(141),G0[MM+GG],d=2+pick(7),used[MM]={0},cut=(5+pick(12))*m-pick(m);G0[0]=m;
   if(t%2==0){d=2;int a=m+1+pick(m-2);G0[1]=a;G0[2]=a+1;}
   else for(int a=0;a<d;a++){int z;do{z=1+pick(m-1);}while(used[z]);used[z]=1;G0[a+1]=(1+pick(4))*m+z;}
   for(int a=0;a<m;a++)G0[d+1+a]=cut+a;
   int z=eval(m,G0,m+d+1,4,1,&best0);if(z)accepted++;if(z<0){printf("TRUNC_STOP sample=%ld accepted=%ld seed=%s\n",t+1,accepted,argv[3]);return 0;}
  }
  printf("TRUNC_DONE samples=%ld accepted=%ld seed=%s min_corrected=%lld Bnegative=%ld max_repair_ratio=%lld/%lld\n",N,accepted,argv[3],best0,nbneg,ratio_num,ratio_den);return 0;
 }
 if(argc==5&&!strcmp(argv[1],"--enum")){
  int m=atoi(argv[2]),e=atoi(argv[3]),K=atoi(argv[4]),d=e-1;
  if(m<2||m>=MM||d<1||d>=GG||3*e>=m||K<1)return 1;
  need_e=e;kunz_cap=K;int s[GG],k[GG],G0[GG];G0[0]=m;for(int a=0;a<d;a++)s[a]=a+1;
  long cand=0,acc=0;ll best0=1LL<<60;
  for(;;){
   for(int a=0;a<d;a++)k[a]=1;
   for(;;){
    for(int a=0;a<d;a++)G0[a+1]=m*k[a]+s[a];cand++;
    int z=eval(m,G0,d+1,e,1,&best0);if(z)acc++;if(z<0){printf("STOP candidates=%ld accepted=%ld\n",cand,acc);return 0;}
    int a=d-1;while(a>=0&&k[a]==K){k[a]=1;a--;}if(a<0)break;k[a]++;
   }
   int a=d-1;while(a>=0&&s[a]==m-d+a)a--;if(a<0)break;s[a]++;for(int j=a+1;j<d;j++)s[j]=s[j-1]+1;
  }
  printf("ENUM_DONE m=%d e=%d K=%d candidates=%ld accepted=%ld Bnegative=%ld min_corrected=%lld max_repair_ratio=%lld/%lld\n",m,e,K,cand,acc,nbneg,best0,ratio_num,ratio_den);return 0;
 }
 if(argc>3&&(!strcmp(argv[1],"--case")||!strcmp(argv[1],"--cover")||!strcmp(argv[1],"--capacity-audit")||!strcmp(argv[1],"--transport-audit")||!strcmp(argv[1],"--unit-audit")||!strcmp(argv[1],"--weighted-audit")||!strcmp(argv[1],"--integer-weighted-audit")||!strcmp(argv[1],"--equality-weighted-audit")||!strcmp(argv[1],"--axis-seed"))){
  int ng=argc-2,G0[MM+GG],m0=INT_MAX;if(ng>MM+GG)return 1;for(int k=0;k<ng;k++){G0[k]=atoi(argv[k+2]);if(G0[k]<m0)m0=G0[k];}
  if(m0<2||m0>=MM)return 1;
  int at=0;while(G0[at]!=m0)at++;int tmp=G0[0];G0[0]=G0[at];G0[at]=tmp;
  int mode=!strcmp(argv[1],"--cover")?3:!strcmp(argv[1],"--capacity-audit")?4:!strcmp(argv[1],"--transport-audit")?5:!strcmp(argv[1],"--unit-audit")?6:!strcmp(argv[1],"--weighted-audit")?7:!strcmp(argv[1],"--integer-weighted-audit")?8:!strcmp(argv[1],"--equality-weighted-audit")?9:!strcmp(argv[1],"--axis-seed")?10:2;
  ll best0=1LL<<60;return eval(m0,G0,ng,2,mode,&best0)==0?1:0;
 }
 if(argc<3)return 1;long N=atol(argv[1]);state=strtoull(argv[2],NULL,10);if(!state)state=1;int mine=argc>3?atoi(argv[3]):4;
 ll best=1LL<<60;long accepted=0;int G[GG];
 for(long t=0;t<N;t++){
  int mode=t%6,m=20+pick(141),d=3+pick(14),used[MM]={0},base=1+pick(8);G[0]=m;
  for(int a=0;a<d;a++){
   int s;
   if(mode==2)s=a+1;else if(mode==5)s=(a+1)*2-1;else if(mode==3&&a==0)s=1;else{do{s=1+pick(m-1);}while(used[s]);}
   if(s>=m){d=a;break;}used[s]=1;
   int k=mode==1||mode==2?1:mode==4?base:1+pick(8);if(mode==3&&a==0)k=1;
   G[a+1]=k*m+s;
  }
  int z=eval(m,G,d+1,mine,1,&best);if(z)accepted++;if(z<0){printf("STOP sample=%ld accepted=%ld seed=%s min_e=%d\n",t+1,accepted,argv[2],mine);return 0;}
 }
 printf("DONE samples=%ld accepted=%ld seed=%s min_e=%d min_bound=%lld Bnegative=%ld max_repair_ratio=%lld/%lld\n",N,accepted,argv[2],mine,best,nbneg,ratio_num,ratio_den);return 0;
}
