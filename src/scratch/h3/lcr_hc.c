/* HC test (lead, 2026-10-19): on every injective labeling of every exported (core, s) case and every sigma, evaluate
   the hybrid bound  HC = sum_a (d+1-adeg a) rho_a + (d+1) sum_N2 r - 2 sum_T r - (p+t) rho_0  (S >= HC is proved:
   flat window on maximal pairs).  Reports min HC and how often HC < 0 (then HC alone does not prove MaxCL).
   Built from lcr_check2.c:  Same input/output as lcr_check.c:
   for every p in [1,m-1]^k with the core labels phi(x)=x.p mod m pairwise distinct, and every sigma,
   S_sigma = sum_cells w*((phi - sigma) mod m) must be >= 0 (spikes carry weight 0).
   Coordinates are assigned in order 0..k-1; after p_0..p_a are fixed, every cell whose last nonzero coordinate is a
   is labeled and checked for collisions, so non-injective partial labelings are cut early.  This enumerates exactly
   the same set of labelings as lcr_check.c.
   usage: lcr_check2 k < cases.txt   (LCR_VERBOSE=1 prints the count profile of each realizable case) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static int k, m, s, nc, cv[256][8], w[256], last[256], ord[256], start[9];
static int p[8], lab[256], used[512];
static ll nlab, nph, nfail, minsl; static int anyreal; static ll nhcneg, minhc=1LL<<60, nhc, nhc2neg, minhc2=1LL<<60;
static void full(void){
  anyreal=1; nlab++;
  ll coef[512]; for(int r=0;r<m;r++) coef[r]=0; ll C=0;
  for(int j=0;j<nc;j++){ coef[lab[j]]=w[j]; C+=w[j]; }
  ll S=0; for(int r=0;r<m;r++) S+=coef[r]*r;
  /* HC coefficients per cell */
  int dd=k+s, hgt[256], adeg[8]={0}; int pp=0,tt=0;
  for(int j=0;j<nc;j++){ int h=0; for(int a=0;a<k;a++) h+=cv[j][a]; hgt[j]=h; if(h==2&&w[j]<0) for(int a=0;a<k;a++) adeg[a]+=cv[j][a]; if(h==2&&w[j]>0) pp++; if(h==3) tt++; }
  ll hc[512]; for(int r=0;r<m;r++) hc[r]=0; ll HCC=0;
  for(int j=0;j<nc;j++){ ll c=0; if(hgt[j]==0) c=-(pp+tt); else if(hgt[j]==1){ int a=0; while(!cv[j][a]) a++; c=dd+1-adeg[a]; }
    else if(hgt[j]==2) c= (w[j]>0)? dd+1 : 0; else c=-2; hc[lab[j]]=c; HCC+=c; }
  ll H=0; for(int r=0;r<m;r++) H+=hc[r]*r;
  int ua[8], o=-1; for(int j=0;j<nc;j++){ if(hgt[j]==0) o=j; if(hgt[j]==1){ int a=0; while(!cv[j][a]) a++; ua[a]=j; } }
  for(int sg=0;sg<m;sg++){ nph++; if(S<minsl) minsl=S; nhc++; if(H<minhc) minhc=H; if(H<0) nhcneg++;
    { /* HC' = HC + m * O_W, O_W = cells in [m-rho0, m) other than maximal pairs with K = -1 */
      int r0=((lab[o]-sg)%m+m)%m; ll ow=0;
      for(int j=0;j<nc;j++){ int rj=((lab[j]-sg)%m+m)%m; if(rj<m-r0) continue;
        if(hgt[j]==2 && w[j]<0){ int a=-1,b=-1; for(int x=0;x<k;x++){ if(cv[j][x]==2){a=b=x;} else if(cv[j][x]==1){ if(a<0) a=x; else b=x; } }
          int ra=((lab[ua[a]]-sg)%m+m)%m, rb=((lab[ua[b]]-sg)%m+m)%m; if(ra+rb<r0) continue; }
        ow++; }
      /* spikes are the residues not used by the core: they lie in the window too when their residue is >= m-r0 */
      ow += 0;
      ll H2=H+(ll)m*ow; if(H2<minhc2) minhc2=H2; if(H2<0) nhc2neg++; }
    H+=(ll)m*hc[sg]-HCC;
    if(S<0){ nfail++; if(nfail<=10){ printf("FAIL m=%d s=%d p=(",m,s); for(int a=0;a<k;a++) printf("%d%s",p[a],a<k-1?",":")"); printf(" sigma=%d S=%lld\n",sg,S); fflush(stdout);} }
    S+=(ll)m*coef[sg]-C; }
}
static void dfs(int a){
  if(a==k){ full(); return; }
  for(int v=1;v<m;v++){
    p[a]=v; int ok=1, i;
    for(i=start[a];i<start[a+1];i++){ int j=ord[i]; int L=0; for(int b=0;b<=a;b++) L+=cv[j][b]*p[b]; L%=m;
      if(used[L]){ ok=0; break; } used[L]=1; lab[j]=L; }
    if(ok) dfs(a+1);
    for(int t=start[a];t<i;t++) used[lab[ord[t]]]=0;
  }
}
int main(int argc,char**argv){
  k=atoi(argv[1]); char buf[64]; ll ncase=0,nreal=0; nlab=nph=nfail=0; minsl=1LL<<60;
  while(scanf("%d %d %d",&m,&s,&nc)==3){
    for(int i=0;i<nc;i++){ if(scanf("%63s",buf)!=1) return 1; char *c=strchr(buf,':'); *c=0;
      for(int a=0;a<k;a++) cv[i][a]=buf[a]-'0'; w[i]=atoi(c+1); }
    ncase++;
    /* origin: label 0, fixed; order the other cells by last nonzero coordinate */
    memset(used,0,sizeof used); int o=-1;
    for(int i=0;i<nc;i++){ last[i]=-1; for(int a=0;a<k;a++) if(cv[i][a]) last[i]=a; if(last[i]<0) o=i; }
    if(o<0) return 2; lab[o]=0; used[0]=1;
    int n=0; for(int a=0;a<k;a++){ start[a]=n; for(int i=0;i<nc;i++) if(last[i]==a) ord[n++]=i; } start[k]=n;
    anyreal=0; dfs(0); nreal+=anyreal;
    if(anyreal && getenv("LCR_VERBOSE")){ int np=0,nq=0,nt=0; for(int j=0;j<nc;j++){ int h=0; for(int a=0;a<k;a++) h+=cv[j][a]; if(h==2){ nq++; if(w[j]>0) np++; } if(h==3) nt++; }
      printf("REAL m=%d s=%d |C|=%d q=%d p=%d t=%d maxpairs=%d\n",m,s,nc,nq,np,nt,nq-np); }
  }
  printf("k=%d cases=%lld realizable=%lld labelings=%lld phases=%lld FAILURES=%lld minslack=%lld  HC: min %lld, negative at %lld of %lld phases; HC\x27 (window-exact, core cells only): min %lld, negative at %lld\n",k,ncase,nreal,nlab,nph,nfail,nlab?minsl:-1,minhc,nhcneg,nhc,minhc2,nhc2neg);
  return 0;
}
