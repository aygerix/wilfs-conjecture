/* Stage 1 of the CASEB-FLAT height-3 search (lead, 2026-10-20).  Anneals d-subsets delta of Z/m \ 0 to maximize the
   upper bound for "height-2 tile + triples on the 2-sum holes":
     UB = 3(cov - 1 - d) - d(d+1) - forced - sum_{u in U} cost(u),
   cov = |{0} u delta + {0} u delta|, U = Z/m minus that sumset (the holes), forced = residues whose only 2-sum
   representations are loops 2*delta_a (each needs a loop cell), cost(u) = d - 1 if u = 3*delta_a (a cube), 2d - 3 if
   u = 2*delta_a + delta_b, 3d + 1 if u = delta_a + delta_b + delta_c, and 10^4 if u is no 3-sum (no height-3 tile).
   Prints every distinct delta with |U| >= 1 (a height-3 cell is forced) and UB >= THR.  Exact mu for each printed
   delta is then computed by the fixed-delta MILP (caseb_fix.py).
   usage: anncover d m ITERS RESTARTS SEED THR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static int d, m, dl[32];
static unsigned long long rs;
static unsigned rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int score(int *nU_out){
  int cnt[256], loopcnt[256], other[256]; memset(cnt,0,sizeof(int)*m); memset(loopcnt,0,sizeof(int)*m); memset(other,0,sizeof(int)*m);
  other[0]=1; for(int a=0;a<d;a++) other[dl[a]]=1;
  for(int a=0;a<d;a++) for(int b=a+1;b<d;b++) other[(dl[a]+dl[b])%m]=1;
  for(int a=0;a<d;a++) loopcnt[(2*dl[a])%m]=1;
  int cov=0, forced=0; for(int r=0;r<m;r++){ if(other[r]||loopcnt[r]) cov++; if(!other[r]&&loopcnt[r]) forced++; }
  int nU=0, cost=0;
  for(int u=0;u<m;u++) if(!other[u]&&!loopcnt[u]){
    nU++; int best=10000;
    for(int a=0;a<d&&best>d-1;a++) for(int b=a;b<d;b++) for(int c=b;c<d;c++) if((dl[a]+dl[b]+dl[c])%m==u){
      int cs = (a==b&&b==c)? d-1 : (a==b||b==c)? 2*d-3 : 3*d+1; if(cs<best) best=cs; }
    cost+=best; }
  *nU_out=nU;
  return 3*(cov-1-d) - d*(d+1) - forced - cost;
}
int main(int argc,char**argv){
  d=atoi(argv[1]); m=atoi(argv[2]); long iters=atol(argv[3]); int R=atoi(argv[4]); rs=atoll(argv[5])*2654435761ULL+1; int THR=atoi(argv[6]);
  static unsigned long long seen[200000]; int nseen=0; int bestall=-1000000;
  for(int rr=0; rr<R; rr++){
    int used[256]; memset(used,0,sizeof used); used[0]=1;
    for(int a=0;a<d;a++){ int v; do v=1+rnd()%(m-1); while(used[v]); used[v]=1; dl[a]=v; }
    int nU; int cur=score(&nU); double T=8.0;
    for(long it=0; it<iters; it++){
      T = 8.0*(1.0 - (double)it/iters) + 0.05;
      int a=rnd()%d, v; do v=1+rnd()%(m-1); while(used[v]);
      int old=dl[a]; dl[a]=v; int nU2; int s=score(&nU2);
      if(s>=cur || exp((s-cur)/T) > (rnd()%1000000)/1e6){ used[old]=0; used[v]=1; cur=s; nU=nU2;
        if(cur>bestall) bestall=cur;
        if(cur>=THR && nU>=1){
          int srt[32]; memcpy(srt,dl,sizeof(int)*d);
          for(int i=0;i<d;i++) for(int j=i+1;j<d;j++) if(srt[j]<srt[i]){int t=srt[i];srt[i]=srt[j];srt[j]=t;}
          unsigned long long h=1469598103934665603ULL; for(int i=0;i<d;i++){ h^=srt[i]; h*=1099511628211ULL; }
          int dup=0; for(int i=0;i<nseen;i++) if(seen[i]==h){dup=1;break;}
          if(!dup && nseen<200000){ seen[nseen++]=h; printf("UB=%d nU=%d delta=",cur,nU); for(int i=0;i<d;i++) printf("%d%s",srt[i],i<d-1?",":"\n"); fflush(stdout); }
        } }
      else dl[a]=old;
    }
  }
  fprintf(stderr,"d=%d m=%d best UB seen %d, printed %d\n",d,m,bestall,nseen);
  return 0;
}
