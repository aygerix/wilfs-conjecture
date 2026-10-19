/* Lead's independent check of P4_REPORT sec.19 (a=7, pure A, all AA in I3, q2=0).
   Parameter sets: (m=107,t=13,rho=0..3), (m=108,t=12,rho=0..7). h=m-rho.
   Weights ceil(h/2)<=t_1<...<t_7<h; 36 lower cells (0, units, 28 AA) with distinct residues.
   Eligible cubic: T<=m+h-1. Need #eligible>=84-t, some T==m+h-1, and lower U eligible residues = Z/m. */
#include <stdio.h>
#include <string.h>
static int m,h,need; static int t[7]; static long npi,nenough,nmax,ncover; static int bestunc;
static int seen[128];
static void leaf(void){
  npi++;
  int cov[128]; memcpy(cov,seen,sizeof cov);
  int nel=0,hasmax=0;
  for(int i=0;i<7;i++)for(int j=i;j<7;j++)for(int k=j;k<7;k++){int T=t[i]+t[j]+t[k]; if(T<=m+h-1){nel++; cov[T%m]=1; if(T==m+h-1)hasmax=1;}}
  if(nel<need) return; nenough++;
  if(!hasmax) return; nmax++;
  int unc=0; for(int r=0;r<m;r++) if(!cov[r]) unc++;
  if(unc<bestunc){bestunc=unc;}
  if(unc==0){ncover++; printf("COVER m=%d h=%d t=",m,h); for(int i=0;i<7;i++)printf("%d ",t[i]); printf("\n");}
}
static void rec(int depth,int lo){
  if(depth==7){leaf();return;}
  for(int x=lo;x<h;x++){
    /* add residues x, 2x, x+t_i */
    int add[9],na=0,ok=1;
    int cand[9]; int nc=0; cand[nc++]=x%m; cand[nc++]=(2*x)%m; for(int i=0;i<depth;i++) cand[nc++]=(x+t[i])%m;
    for(int c=0;c<nc&&ok;c++){ if(seen[cand[c]]) ok=0; else {seen[cand[c]]=1; add[na++]=cand[c];} }
    if(ok){t[depth]=x; rec(depth+1,x+1);}
    for(int c=0;c<na;c++) seen[add[c]]=0;
  }
}
int main(void){
  int sets[][3]={{107,13,0},{107,13,1},{107,13,2},{107,13,3},{108,12,0},{108,12,1},{108,12,2},{108,12,3},{108,12,4},{108,12,5},{108,12,6},{108,12,7}};
  for(int s=0;s<12;s++){
    m=sets[s][0]; int tt=sets[s][1]; int rho=sets[s][2]; h=m-rho; need=84-tt;
    npi=nenough=nmax=ncover=0; bestunc=1000; memset(seen,0,sizeof seen); seen[0]=1;
    rec(0,(h+1)/2);
    printf("m=%d t=%d rho=%d: pair-injective=%ld enough=%ld +max=%ld cover=%ld best_uncovered=%d\n",m,tt,rho,npi,nenough,nmax,ncover,bestunc);
    fflush(stdout);
  }
  return 0;
}
