/* CASEB-FLAT on every height-<=3 lattice tile (lead, 2026-10-20), adapted from ../h3/h3_tiles_dfs.c (H3-D5 check).
   Same exhaustive enumeration; per tile computes mu = Sigma_supp - Dep (case B iff mu > 0), counts case-B tiles with
   and without a cubic cell, and checks the closed form mu = 3P + 2R - d(d+1) - p_l - sum_{N2}(d+2-tau) when every
   unit is non-maximal.  Original header follows.
   Enumerates EVERY tile of height <= 3 with exactly d active directions (all e_a in D) by a direct depth-first
   assignment of one cell to every residue -- no faces, containers, forced sets or dominance -- and tests MaxCL
       S_sigma = (d+1) sum_N r - sum_A (|y|-1) r >= 0      for every sigma,  r = (phi - sigma) mod m.
   Domain: m in [mmin, mmax], all 1 <= p_1 < ... < p_d < m (coordinate permutations only).
   Output per m: residue sets, sets with <=3-fold coverage, tiles, distinct pair-faces (flat / height 3), failures,
   minimum slack.  A failure prints the full tile.
   usage: caseb_h3 d mmin mmax [PRINTMIN]  (prints up to 10 height-3 tiles per run with mu >= PRINTMIN; default 1) */
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

static ll ncaseB2, ncaseB3, nform_bad; static ll maxmu3, maxmu2; static int nprint; static int PRINTMIN=1;
static int id3[8][8][8], id2g[8][8];
static void check_tile(void){
  int inD[MAXC]; memset(inD,0,sizeof inD);
  for(int r=0;r<m;r++) if(asg[r]>=0) inD[asg[r]]=1;
  int ncub=0, P=0, R=0, pl=0; for(int c=0;c<nc;c++) if(inD[c]){ if(csz[c]==2){ P++; if(cv[c][0]==cv[c][1]) pl++; } else { ncub++; R++; } }
  /* Dep and Sigma_supp, generic from the cell list (height <= 3) */
  ll dep=0, ss=0;
  /* units */
  for(int a=0;a<d;a++){ int nonmax=0; ll t=0;
    for(int b=0;b<d;b++){ int x=a<b?a:b, y=a<b?b:a; if(inD[id2g[x][y]]) nonmax=1; else t += 1+(b==a); }
    if(nonmax) dep+=t; }
  /* pairs */
  ll sumtau_term=0; int n2=0;
  for(int c=0;c<nc;c++) if(inD[c]&&csz[c]==2){ int a=cv[c][0], b=cv[c][1]; if(a!=b) ss++;
    int nonmax=0, tau=0; ll t=0;
    for(int e=0;e<d;e++){ int s[3]={a,b,e}; /* sort */ for(int i=0;i<2;i++) for(int j=0;j<2-i;j++) if(s[j]>s[j+1]){int z=s[j];s[j]=s[j+1];s[j+1]=z;}
      if(inD[id3[s[0]][s[1]][s[2]]]){ nonmax=1; tau++; } else t += 1+(e==a)+(e==b); }
    if(nonmax){ dep+=t; n2++; sumtau_term += d+2-tau; } }
  for(int c=0;c<nc;c++) if(inD[c]&&csz[c]==3){ int a=cv[c][0], b=cv[c][1], e=cv[c][2]; ss += (a!=b)+(b!=e); }
  ll mu = ss - dep;
  /* closed form (all units non-max): mu = 3P + 2R - d(d+1) - pl - sum_N2 (d+2-tau) */
  int allnm=1; for(int a=0;a<d;a++){ int nm=0; for(int b=0;b<d;b++){ int x=a<b?a:b,y=a<b?b:a; if(inD[id2g[x][y]]) nm=1; } if(!nm) allnm=0; }
  if(allnm && mu != 3LL*P+2LL*R-(ll)d*(d+1)-pl-sumtau_term) nform_bad++;
  ntiles++; if(ncub) nt3++;
  if(ncub){ if(mu>maxmu3) maxmu3=mu; } else { if(mu>maxmu2) maxmu2=mu; }
  if(mu>0){ if(ncub) ncaseB3++; else ncaseB2++; }
  if(mu>=PRINTMIN){
    if(ncub && nprint<10){ nprint++; printf("CASEB-H3 m=%d p=(",m); for(int a=0;a<d;a++) printf("%d%s",p[a],a<d-1?",":")");
      printf(" mu=%lld dep=%lld ss=%lld cells:",mu,dep,ss); for(int r=0;r<m;r++) if(asg[r]>=0){ int c=asg[r]; printf(" [");
        for(int i=0;i<csz[c];i++) printf("%d",cv[c][i]); printf("]"); } printf("\n"); fflush(stdout); } }
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
  d=atoi(argv[1]); int mmin=atoi(argv[2]), mmax=atoi(argv[3]); if(argc>4) PRINTMIN=atoi(argv[4]);
  ll gt=0, gf=0;
  for(m=mmin;m<=mmax;m++){
    ll nsets=0,ncov=0; ntiles=0; nt3=0; nfail=0; nfaces_flat=0; nfaces_h3=0; minslack=1LL<<60; ncaseB2=ncaseB3=nform_bad=0; maxmu3=maxmu2=-(1LL<<60);
    for(int a=0;a<d;a++) p[a]=a+1;
    while(1){
      if(p[d-1]<m){
        nsets++;
        /* build candidate cells */
        nc=0; int id2[8][8];
        for(int a=0;a<d;a++) for(int b=a;b<d;b++){ csz[nc]=2; cv[nc][0]=a; cv[nc][1]=b; clab[nc]=(p[a]+p[b])%m; id2[a][b]=nc; id2g[a][b]=nc; nc++; }
        for(int a=0;a<d;a++) for(int b=a;b<d;b++) for(int c=b;c<d;c++){ csz[nc]=3; cv[nc][0]=a; cv[nc][1]=b; cv[nc][2]=c;
          clab[nc]=(p[a]+p[b]+p[c])%m; id3[a][b][c]=nc; int fs[3][2]={{b,c},{a,c},{a,b}}; nface[nc]=0;
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
    printf("d=%d m=%d sets=%lld covered=%lld tiles=%lld h3tiles=%lld caseB_flat=%lld caseB_h3=%lld max_mu_flat=%lld max_mu_h3=%lld closedform_mismatch=%lld\n",
           d,m,nsets,ncov,ntiles,nt3,ncaseB2,ncaseB3,maxmu2,maxmu3,nform_bad); fflush(stdout);
  }
  printf("TOTAL d=%d tiles=%lld failures=%lld\n",d,gt,gf);
  return 0;
}
