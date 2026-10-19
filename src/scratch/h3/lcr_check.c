/* Check the spike form of MaxCL on EVERY injective labeling of each exported (core, s) case (lead, 2026-10-19).
   Input lines from lcr_export.py:  m s ncells  v:w ...   (v = exponent digits, w = MaxCL coefficient).
   For every p in [1,m-1]^k with the core labels phi(x)=x.p mod m pairwise distinct, and every sigma,
   S_sigma = sum_cells w * ((phi - sigma) mod m) must be >= 0 (spikes carry weight 0).
   usage: lcr_check k < cases.txt */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
int main(int argc,char**argv){
  int k=atoi(argv[1]); int m,s,nc; static int cv[128][8], w[128]; char buf[64];
  ll ncase=0, nreal=0, nlab=0, nph=0, nfail=0, minsl=1LL<<60;
  while(scanf("%d %d %d",&m,&s,&nc)==3){
    for(int i=0;i<nc;i++){ if(scanf("%63s",buf)!=1) return 1; char *c=strchr(buf,':'); *c=0;
      for(int a=0;a<k;a++) cv[i][a]=buf[a]-'0'; w[i]=atoi(c+1); }
    ncase++; int p[8]; for(int a=0;a<k;a++) p[a]=1; int anyreal=0;
    while(1){
      /* labels with early exit */
      static int used[256]; static int lab[128]; int ok=1, i;
      for(i=0;i<nc;i++){ int v=0; for(int a=0;a<k;a++) v+=cv[i][a]*p[a]; v%=m; if(used[v]){ ok=0; break; } used[v]=1; lab[i]=v; }
      for(int j=0;j<i;j++) used[lab[j]]=0;
      if(ok){ anyreal=1; nlab++;
        ll coef[256]; for(int r=0;r<m;r++) coef[r]=0; ll C=0; for(int j=0;j<nc;j++){ coef[lab[j]]=w[j]; C+=w[j]; }
        ll S=0; for(int r=0;r<m;r++) S+=coef[r]*r;
        for(int sg=0;sg<m;sg++){ nph++; if(S<minsl) minsl=S;
          if(S<0){ nfail++; if(nfail<=10){ printf("FAIL m=%d s=%d p=(",m,s); for(int a=0;a<k;a++) printf("%d%s",p[a],a<k-1?",":")"); printf(" sigma=%d S=%lld\n",sg,S); fflush(stdout);} }
          S+=(ll)m*coef[sg]-C; } }
      int a=k-1; while(a>=0 && p[a]==m-1){ p[a]=1; a--; } if(a<0) break; p[a]++;
    }
    nreal+=anyreal;
  }
  printf("k=%d cases=%lld realizable=%lld labelings=%lld phases=%lld FAILURES=%lld minslack=%lld\n",k,ncase,nreal,nlab,nph,nfail,nlab?minsl:-1);
  return 0;
}
