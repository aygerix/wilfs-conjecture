/* Independent check of codex P6 Theorem H3-D5 (lead, 2026-10-19).
   Enumerates EVERY tile of height <= 3 with exactly d active directions (all e_a in D) by a direct depth-first
   assignment of one cell to every residue -- no faces, containers, forced sets or dominance -- and tests MaxCL
       S_sigma = (d+1) sum_N r - sum_A (|y|-1) r >= 0      for every sigma,  r = (phi - sigma) mod m.
   Domain: m in [mmin, mmax], all 1 <= p_1 < ... < p_d < m (coordinate permutations only).
   Output per m: residue sets, sets with <=3-fold coverage, tiles, distinct pair-faces (flat / height 3), failures,
   minimum slack.  A failure prints the full tile.
   usage: h3_tiles_dfs d mmin mmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
#define MAXC 128
static int d, m, p[8];
static int nc, csz[MAXC], cv[MAXC][3], clab[MAXC];   /* candidate cells: pairs and cubics (multisets) */
static int face[MAXC][3], nface[MAXC];                /* pair faces of cubics (cell ids) */
static int asg[64];                                   /* residue -> cell id (-2 = origin/unit, -1 = free) */
static int unitres[8];
static ll ntiles, nt3, nfail, nfaces_flat, nfaces_h3; static ll minslack;
/* face dedup: hash of pair-set masks per residue vector */
static unsigned long long seenQ[4096]; static int nseen;

static void check_tile(void){
  int inD[MAXC]; memset(inD,0,sizeof inD);
  for(int r=0;r<m;r++) if(asg[r]>=0) inD[asg[r]]=1;
  /* maximality */
  int unitmax[8]; for(int a=0;a<d;a++) unitmax[a]=1;
  int pairmax[MAXC]; unsigned long long Q=0; int ncub=0;
  for(int c=0;c<nc;c++) if(inD[c]){
    if(csz[c]==2){ unitmax[cv[c][0]]=0; unitmax[cv[c][1]]=0; pairmax[c]=1; Q|=1ULL<<c; }
    else ncub++; }
  for(int c=0;c<nc;c++) if(inD[c]&&csz[c]==3) for(int f=0;f<nface[c];f++) pairmax[face[c][f]]=0;
  /* coefficient per cell: N -> d+1, A -> -(|y|-1) */
  ll coef[64]; for(int r=0;r<m;r++) coef[r]=0;
  coef[0]=d+1;
  for(int a=0;a<d;a++) coef[unitres[a]]= unitmax[a]? 0 : d+1;
  for(int r=0;r<m;r++) if(asg[r]>=0){ int c=asg[r];
    if(csz[c]==2) coef[r]= pairmax[c]? -1 : d+1; else coef[r]=-2; }
  ll Ctot=0; for(int r=0;r<m;r++) Ctot+=coef[r];
  ll S=0; for(int r=0;r<m;r++) S+=coef[r]*r;           /* sigma = 0 */
  for(int sg=0;sg<m;sg++){
    if(S<minslack) minslack=S;
    if(S<0){ nfail++; if(nfail<=5){ printf("FAIL m=%d p=(",m); for(int a=0;a<d;a++) printf("%d%s",p[a],a<d-1?",":")");
        printf(" sigma=%d slack=%lld cells:",sg,S); for(int r=0;r<m;r++) if(asg[r]>=0){ int c=asg[r]; printf(" [");
          for(int i=0;i<csz[c];i++) printf("%d",cv[c][i]); printf("]"); } printf("\n"); fflush(stdout);} }
    S += (ll)m*coef[sg] - Ctot;                        /* advance sigma -> sigma+1: residue sg wraps to m-1 */
  }
  ntiles++; if(ncub) nt3++;
  /* distinct faces */
  int seen=0; for(int i=0;i<nseen;i++) if(seenQ[i]==Q){ seen=1; break; }
  if(!seen && nseen>=4096){ fprintf(stderr,"face table overflow\n"); exit(2); }
  if(!seen && nseen<4096){ seenQ[nseen++]=Q; if(ncub) nfaces_h3++; else nfaces_flat++; }
}

static void dfs(int r){
  while(r<m && asg[r]!=-1) r++;
  if(r==m){ check_tile(); return; }
  for(int c=0;c<nc;c++) if(clab[c]==r){
    if(csz[c]==2){ asg[r]=c; dfs(r+1); asg[r]=-1; }
    else {
      /* cubic: every pair face must be assigned exactly to its residue */
      int setl[3], ns=0, ok=1;
      for(int f=0;f<nface[c]&&ok;f++){ int z=face[c][f], rz=clab[z];
        if(asg[rz]==z) continue; if(asg[rz]!=-1){ ok=0; break; } asg[rz]=z; setl[ns++]=rz; }
      if(ok){ asg[r]=c; dfs(r+1); asg[r]=-1; }
      for(int i=0;i<ns;i++) asg[setl[i]]=-1;
    }
  }
}

int main(int argc,char**argv){
  d=atoi(argv[1]); int mmin=atoi(argv[2]), mmax=atoi(argv[3]);
  ll gt=0, gf=0;
  for(m=mmin;m<=mmax;m++){
    ll nsets=0,ncov=0; ntiles=0; nt3=0; nfail=0; nfaces_flat=0; nfaces_h3=0; minslack=1LL<<60;
    for(int a=0;a<d;a++) p[a]=a+1;
    while(1){
      if(p[d-1]<m){
        nsets++;
        /* build candidate cells */
        nc=0; int id2[8][8];
        for(int a=0;a<d;a++) for(int b=a;b<d;b++){ csz[nc]=2; cv[nc][0]=a; cv[nc][1]=b; clab[nc]=(p[a]+p[b])%m; id2[a][b]=nc; nc++; }
        for(int a=0;a<d;a++) for(int b=a;b<d;b++) for(int c=b;c<d;c++){ csz[nc]=3; cv[nc][0]=a; cv[nc][1]=b; cv[nc][2]=c;
          clab[nc]=(p[a]+p[b]+p[c])%m; int fs[3][2]={{b,c},{a,c},{a,b}}; nface[nc]=0;
          for(int f=0;f<3;f++){ int z=id2[fs[f][0]][fs[f][1]]; int dup=0; for(int g=0;g<nface[nc];g++) if(face[nc][g]==z) dup=1; if(!dup) face[nc][nface[nc]++]=z; }
          nc++; }
        for(int r=0;r<m;r++) asg[r]=-1;
        asg[0]=-2; int bad=0; for(int a=0;a<d;a++){ unitres[a]=p[a]; asg[p[a]]=-2; }
        /* coverage */
        int cov[64]; memset(cov,0,sizeof cov); cov[0]=1; for(int a=0;a<d;a++) cov[p[a]]=1; for(int c=0;c<nc;c++) cov[clab[c]]=1;
        for(int r=0;r<m;r++) if(!cov[r]) bad=1;
        if(!bad){ ncov++; nseen=0; dfs(1); }
      }
      int i=d-1; while(i>=0 && p[i]>=m-(d-i)) i--;   /* next combination with p_{d-1} <= m-1 */
      if(i<0) break; p[i]++; for(int j=i+1;j<d;j++) p[j]=p[j-1]+1;
    }
    gt+=ntiles; gf+=nfail;
    printf("d=%d m=%d sets=%lld covered=%lld tiles=%lld h3tiles=%lld faces(flat)=%lld faces(h3)=%lld FAILURES=%lld minslack=%lld\n",
           d,m,nsets,ncov,ntiles,nt3,nfaces_flat,nfaces_h3,nfail, ntiles?minslack:-1); fflush(stdout);
  }
  printf("TOTAL d=%d tiles=%lld failures=%lld\n",d,gt,gf);
  return 0;
}
