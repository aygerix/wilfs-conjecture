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
 if(argc>3&&(!strcmp(argv[1],"--case")||!strcmp(argv[1],"--cover")||!strcmp(argv[1],"--capacity-audit")||!strcmp(argv[1],"--transport-audit")||!strcmp(argv[1],"--unit-audit")||!strcmp(argv[1],"--weighted-audit")||!strcmp(argv[1],"--integer-weighted-audit")||!strcmp(argv[1],"--equality-weighted-audit"))){
  int ng=argc-2,G0[MM+GG],m0=INT_MAX;if(ng>MM+GG)return 1;for(int k=0;k<ng;k++){G0[k]=atoi(argv[k+2]);if(G0[k]<m0)m0=G0[k];}
  if(m0<2||m0>=MM)return 1;
  int at=0;while(G0[at]!=m0)at++;int tmp=G0[0];G0[0]=G0[at];G0[at]=tmp;
  int mode=!strcmp(argv[1],"--cover")?3:!strcmp(argv[1],"--capacity-audit")?4:!strcmp(argv[1],"--transport-audit")?5:!strcmp(argv[1],"--unit-audit")?6:!strcmp(argv[1],"--weighted-audit")?7:!strcmp(argv[1],"--integer-weighted-audit")?8:!strcmp(argv[1],"--equality-weighted-audit")?9:2;
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
