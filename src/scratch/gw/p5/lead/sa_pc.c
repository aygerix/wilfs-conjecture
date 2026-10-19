/* Adversarial search for violations of the ambient packing statement P(C) at moderate n (lead, 2026-10-19).
   P(C): every set B of n integers with all unordered pair sums (doubles included) distinct satisfies
        F_C(B) = (3s-2) - H(n) + C*ex(B) >= 0,   s = max B - min B + 1,  H(n) = n(C(n,2)+1),
        ex(B) = C(n+2,3) - #(distinct sums b_i+b_j+b_k, i<=j<=k).
   Simulated annealing on F_C over pair-distinct sets; moves relocate one element (Sidon kept exactly).
   Reports the minimum F_C found, the ratio (H-(3s-2))/ex at that set, and the set.  Heuristic search only:
   a negative F_C is a verified violation (the set is printed and rechecked from scratch); a nonnegative
   minimum is evidence, not proof.
   usage: sa_pc n Cnum Cden seed iters [restarts] */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
typedef long long ll;
static int n; static int *b; static int SM; static int *pc, *tc; static ll ex;
static unsigned long long rs=88172645463325252ULL;
static unsigned long long xr(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static double ur(void){ return (xr()>>11)*(1.0/9007199254740992.0); }
static void tri_add(int v,int sg){ if(sg>0){ if(tc[v]++) ex++; } else { if(--tc[v]) ex--; } }
/* add or remove all triples containing element i (value b[i]) exactly once per multiset */
static void tri_elem(int i,int sg){
  int x=b[i];
  tri_add(3*x,sg);
  for(int j=0;j<n;j++) if(j!=i){ tri_add(2*x+b[j],sg); tri_add(x+2*b[j],sg); }
  for(int j=0;j<n;j++) if(j!=i) for(int k=j+1;k<n;k++) if(k!=i) tri_add(x+b[j]+b[k],sg);
}
static void pair_elem(int i,int sg){ int x=b[i]; pc[2*x]+=sg; for(int j=0;j<n;j++) if(j!=i) pc[x+b[j]]+=sg; }
static int span(void){ int mn=b[0],mx=b[0]; for(int i=1;i<n;i++){ if(b[i]<mn) mn=b[i]; if(b[i]>mx) mx=b[i]; } return mx-mn+1; }
static ll Hn(void){ return (ll)n*((ll)n*(n-1)/2+1); }
static ll C3(void){ return (ll)n*(n+1)*(n+2)/6; }
/* recompute ex and Sidon from scratch for verification */
static int verify(ll *exo){
  char *p=calloc(2*SM+2,1); int *t=calloc(3*SM+3,sizeof(int)); int ok=1; ll d=0;
  for(int i=0;i<n;i++) for(int j=i;j<n;j++){ int v=b[i]+b[j]; if(p[v]) ok=0; p[v]=1; }
  for(int i=0;i<n;i++) for(int j=i;j<n;j++) for(int k=j;k<n;k++){ int v=b[i]+b[j]+b[k]; if(!t[v]) d++; t[v]=1; }
  *exo=C3()-d; free(p); free(t); return ok;
}
int main(int argc,char**argv){
  n=atoi(argv[1]); double Cc=atof(argv[2])/atof(argv[3]); rs^=(unsigned long long)atoll(argv[4])*0x9E3779B97F4A7C15ULL; ll iters=atoll(argv[5]);
  int restarts=argc>6?atoi(argv[6]):1;
  ll H=Hn(); SM=(int)(H/3)+4*n+10; b=malloc(n*sizeof(int)); pc=calloc(2*SM+2,sizeof(int)); tc=calloc(3*SM+3,sizeof(int));
  double gbest=1e18; int *gb=malloc(n*sizeof(int)); ll gex=0; int gs=0;
  for(int rr=0;rr<restarts;rr++){
    memset(pc,0,(2*SM+2)*sizeof(int)); memset(tc,0,(3*SM+3)*sizeof(int)); ex=0;
    /* random greedy Sidon start inside [0, W) with W around H/3 */
    int W=(int)(H/3*(0.6+0.5*ur())); if(W>SM-1) W=SM-1; if(W<2*n*n) W=2*n*n<SM-1?2*n*n:SM-1;
    int k=0, tries=0;
    while(k<n){ int v=(int)(ur()*W); int ok=(pc[2*v]==0); for(int j=0;j<k&&ok;j++){ if(b[j]==v||pc[v+b[j]]) ok=0; }
      if(ok){ b[k]=v; pc[2*v]++; for(int j=0;j<k;j++) pc[v+b[j]]++; k++; } if(++tries>10000000){ W=W*2<SM-1?W*2:SM-1; tries=0; } }
    /* build triples */
    for(int i=0;i<n;i++) for(int j=i;j<n;j++) for(int l=j;l<n;l++) tri_add(b[i]+b[j]+b[l],1);
    int s=span(); double F=(3.0*s-2)-H+Cc*ex, best=F; double T0=0.5*n, T=T0;
    for(ll it=0;it<iters;it++){
      T=T0*pow(0.002,(double)it/iters);
      int i=xr()%n; int old=b[i]; int mn=1<<30,mx=-1; for(int j=0;j<n;j++) if(j!=i){ if(b[j]<mn) mn=b[j]; if(b[j]>mx) mx=b[j]; }
      int v; double r=ur();
      if(r<0.5){ int w=1+(int)(ur()*ur()*(mx-mn+1)); v=old+((xr()&1)?w:-w); }        /* local jump */
      else v=mn+(int)(ur()*(mx-mn+1));                                                   /* anywhere inside */
      if(v<0||v>=SM||v==old) continue;
      pair_elem(i,-1); int ok=(pc[2*v]==0); for(int j=0;j<n&&ok;j++) if(j!=i){ if(b[j]==v||pc[v+b[j]]) ok=0; }
      if(!ok){ pair_elem(i,1); continue; }
      tri_elem(i,-1); b[i]=v; tri_elem(i,1); pair_elem(i,1);
      int s2=span(); double F2=(3.0*s2-2)-H+Cc*ex;
      if(F2<=F || ur()<exp((F-F2)/T)){ F=F2; s=s2; if(F<best) best=F;
        if(F<gbest){ gbest=F; memcpy(gb,b,n*sizeof(int)); gex=ex; gs=s; } }
      else { pair_elem(i,-1); tri_elem(i,-1); b[i]=old; tri_elem(i,1); pair_elem(i,1); }
    }
    /* clean out arrays for next restart: done by memset */
  }
  memcpy(b,gb,n*sizeof(int)); ll exv; int ok=verify(&exv); int sv=span(); int mn=b[0]; for(int i=1;i<n;i++) if(b[i]<mn) mn=b[i];
  double Fv=(3.0*sv-2)-H+Cc*exv;
  printf("n=%d C=%.4f H=%lld bestF=%.3f verify: sidon=%d s=%d ex=%lld F=%.3f ratio=(H-(3s-2))/ex=%.4f\n  set:",
         n,Cc,H,gbest,ok,sv,exv,Fv, exv>0? (double)(H-(3LL*sv-2))/exv : 0.0);
  int *srt=malloc(n*sizeof(int)); for(int i=0;i<n;i++) srt[i]=b[i]-mn;
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(srt[j]<srt[i]){ int t=srt[i]; srt[i]=srt[j]; srt[j]=t; }
  for(int i=0;i<n;i++) printf(" %d",srt[i]); printf("\n");
  return 0;
}
