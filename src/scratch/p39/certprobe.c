/* Backwards Wilf audit: exact integer semigroup data and sparse optimized LP certificates.
 * Reuses p37/enumlp3.c's RT3/UA3 rows; no height/depth filter.
 * usage: certprobe m g1 ... (generating list, not assumed minimal).
 * JSON output includes all primal/dual data for independent rational checking.
 * build: gcc -O2 certprobe.c -I.../include -L.../lib -lgurobi130 -lm -o certprobe
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <limits.h>
#include <math.h>
#include "gurobi_c.h"
#define CHECK(call) do { int err=(call); if(err){fprintf(stderr,"Gurobi error %d at line %d\n",err,__LINE__);exit(2);} }while(0)
typedef long long ll;
typedef struct { int i,j,s,J,tau,lo,up; } Pair;
typedef struct { int n,ind[3],pair,kind; double val[3],rhs; char sense; } Row;
static void *alloc(size_t n,size_t s){void *p=calloc(n,s);if(!p){fprintf(stderr,"allocation failed\n");exit(2);}return p;}
static int cmp(const void *a,const void*b){int x=*(const int*)a,y=*(const int*)b;return (x>y)-(x<y);}
static Row pairrow(Pair p,int pi,char sense,int rhs){
 Row R={.pair=pi,.kind=0,.sense=sense,.rhs=rhs};
 int ix[3]={p.i-1,p.j-1,p.s-1},co[3]={1,1,-1};
 for(int k=0;k<3;k++){int u=0;while(u<R.n&&R.ind[u]!=ix[k])u++;
  if(u==R.n){R.ind[u]=ix[k];R.n++;}R.val[u]+=co[k];}
 return R;
}
int main(int argc,char **argv){
 if(argc<3){fprintf(stderr,"usage: certprobe m g1 ...\n");return 1;}
 int ng=argc-1,*G=alloc(ng,sizeof(int));
 for(int i=0;i<ng;i++){char *end;long v=strtol(argv[i+1],&end,10);if(*end||v<2||v>10000000){fprintf(stderr,"invalid generator\n");return 1;}G[i]=(int)v;}
 qsort(G,ng,sizeof(int),cmp);int m=G[0];if(m>2048){fprintf(stderr,"m > 2048 implementation limit\n");return 1;}
 ll *w=alloc(m,sizeof(ll));int *done=alloc(m,sizeof(int)),*gen=alloc(m,sizeof(int)),*mu=alloc(m,sizeof(int)),*rp=alloc(m,sizeof(int)),*height=alloc(m,sizeof(int)),*order=alloc(m,sizeof(int));
 for(int s=1;s<m;s++)w[s]=LLONG_MAX/4;
 for(int k=0;k<m;k++){int u=-1;for(int s=0;s<m;s++)if(!done[s]&&(u<0||w[s]<w[u]))u=s;
  if(w[u]==LLONG_MAX/4){fprintf(stderr,"not a numerical semigroup (gcd > 1)\n");return 1;}done[u]=1;order[k]=u;
  for(int a=1;a<ng;a++){ll v=w[u]+G[a];int s=(int)(v%m);if(v<w[s])w[s]=v;}}
 int r=0;ll genus=0;for(int s=1;s<m;s++){if(w[s]>w[r])r=s;gen[s]=1;genus+=w[s]/m;}
 ll c=w[r]-m+1;if(c<=0){fprintf(stderr,"unsupported boundary\n");return 1;}int q=(int)((c+m-1)/m),rho=(int)(q*(ll)m-c);
 for(int s=0;s<m;s++){rp[s]=(int)((w[s]-c)%m);if(rp[s]<0)rp[s]+=m;mu[s]=(int)((c-w[s]+m-1)/m);if(w[s]>=c)mu[s]=0;}
 int maxpairs=m*(m-1)/2,np=0;Pair *P=alloc(maxpairs,sizeof(Pair));
 for(int i=1;i<m;i++)for(int j=i;j<m;j++){int s=(i+j)%m;if(!s)continue;ll diff=w[i]+w[j]-w[s];if(diff<0||diff%m){fprintf(stderr,"Kunz invariant failed\n");return 2;}
  int tau=(rp[i]+rp[j]-rp[s]-rho)/m,lo=(rp[s]>=m-rho&&i>r&&j>r),up=(rp[s]<=m-rho-2&&i<=r&&j<=r);
  int expected=(i+j>m)+(s>r)-(i>r)-(j>r);
  if(tau!=expected||mu[i]+mu[j]-mu[s]!=q-diff/m+tau){fprintf(stderr,"tau invariant failed\n");return 2;}
  P[np++]=(Pair){i,j,s,(int)(diff/m),tau,lo,up};if(!diff)gen[s]=0;}
 int e=1;for(int s=1;s<m;s++)e+=gen[s];ll W=(ll)e*(c-genus)-c,ell=0;for(int s=0;s<m;s++)ell+=mu[s];
 if(ell!=c-genus){fprintf(stderr,"ell invariant failed\n");return 2;}
 for(int a=1;a<m;a++){int s=order[a];height[s]=gen[s];for(int p=0;p<np;p++)if(P[p].s==s&&!P[p].J){int v=height[P[p].i]+height[P[p].j];if(v>height[s])height[s]=v;}}
 GRBenv *env=NULL;CHECK(GRBemptyenv(&env));CHECK(GRBsetintparam(env,"OutputFlag",0));CHECK(GRBsetintparam(env,"Threads",1));CHECK(GRBstartenv(env));
 CHECK(GRBsetdblparam(env,"FeasibilityTol",1e-9));CHECK(GRBsetdblparam(env,"OptimalityTol",1e-9));
 printf("{\"m\":%d,\"e\":%d,\"c\":%lld,\"g\":%lld,\"W\":%lld,\"q\":%d,\"rho\":%d,\"r\":%d,\"generators\":[%d",m,e,c,genus,W,q,rho,r,m);
 for(int s=1;s<m;s++)if(gen[s])printf(",%lld",w[s]);printf("],\"w\":[");for(int s=0;s<m;s++)printf("%s%lld",s?",":"",w[s]);printf("],\"mu\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",mu[s]);
 printf("],\"height\":[");for(int s=0;s<m;s++)printf("%s%d",s?",":"",height[s]);printf("],\"pairs\":[");
 for(int p=0;p<np;p++){Pair t=P[p];printf("%s[%d,%d,%d,%d,%d,%d,%d]",p?",":"",t.i,t.j,t.s,t.J,t.tau,t.lo,t.up);}printf("],\"models\":{");
 const char *names[]={"RT3","UA3","TX","AM3","FACE"};
 for(int mode=0;mode<5;mode++){
  int fixed=mode==1||mode==3,exact=mode==2||mode==4,full=mode>=3;
  GRBmodel *M=NULL;double *obj=alloc(m-1,sizeof(double)),*lb=alloc(m-1,sizeof(double)),*ub=alloc(m-1,sizeof(double));
  for(int s=1;s<m;s++){obj[s-1]=e;ub[s-1]=(mode==4)?q-1-(s>r):GRB_INFINITY;}
  CHECK(GRBnewmodel(env,&M,names[mode],m-1,obj,lb,ub,NULL,NULL));
  Row *rows=alloc(2*np+m,sizeof(Row));int nr=0;
  for(int p=0;p<np;p++){
   Pair t=P[p];if(!t.J){if(exact)rows[nr++]=pairrow(t,p,GRB_EQUAL,q+t.tau);
    else{rows[nr++]=pairrow(t,p,GRB_GREATER_EQUAL,q-t.lo);rows[nr++]=pairrow(t,p,GRB_LESS_EQUAL,q+t.up);}}
   else if(full)rows[nr++]=pairrow(t,p,GRB_LESS_EQUAL,q-1+t.tau);
  }
  if(fixed)for(int s=1;s<m;s++)if(gen[s]){Row R={.n=1,.ind={s-1},.val={1},.rhs=mu[s],.sense=GRB_EQUAL,.pair=-1,.kind=1};rows[nr++]=R;}
  for(int a=0;a<nr;a++){Row R=rows[a];CHECK(GRBaddconstr(M,R.n,R.ind,R.val,R.sense,R.rhs,NULL));}
  CHECK(GRBoptimize(M));int status;CHECK(GRBgetintattr(M,GRB_INT_ATTR_STATUS,&status));if(status!=GRB_OPTIMAL){fprintf(stderr,"LP %s status %d\n",names[mode],status);return 3;}
  double val,*Y=alloc(m-1,sizeof(double)),*pi=alloc(nr,sizeof(double)),*rc=alloc(m-1,sizeof(double));
  CHECK(GRBgetdblattr(M,GRB_DBL_ATTR_OBJVAL,&val));CHECK(GRBgetdblattrarray(M,GRB_DBL_ATTR_X,0,m-1,Y));CHECK(GRBgetdblattrarray(M,GRB_DBL_ATTR_PI,0,nr,pi));CHECK(GRBgetdblattrarray(M,GRB_DBL_ATTR_RC,0,m-1,rc));
  printf("%s\"%s\":{\"value\":%.17g,\"y\":[",mode?",":"",names[mode],val+(ll)(e-m)*q+rho);
  for(int s=1;s<m;s++)printf("%s%.17g",s>1?",":"",Y[s-1]);printf("],\"rc\":[");for(int s=1;s<m;s++)printf("%s%.17g",s>1?",":"",rc[s-1]);
  printf("],\"ub\":[");for(int s=1;s<m;s++)printf("%s%.17g",s>1?",":"",ub[s-1]);printf("],\"rows\":[");
  for(int a=0;a<nr;a++){Row R=rows[a];printf("%s{\"pair\":%d,\"kind\":%d,\"sense\":\"%c\",\"b\":%.17g,\"pi\":%.17g,\"a\":[",a?",":"",R.pair,R.kind,R.sense,R.rhs,pi[a]);
   for(int k=0;k<R.n;k++)printf("%s[%d,%.17g]",k?",":"",R.ind[k]+1,R.val[k]);printf("]}");}printf("]}");
  free(rows);free(obj);free(lb);free(ub);free(Y);free(pi);free(rc);GRBfreemodel(M);
 }
 printf("}}\n");GRBfreeenv(env);return 0;
}
