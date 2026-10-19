/* CP and FS on ALL numerical semigroups of genus <= G (semigroup tree), lex (GRADED=0) or grlex (GRADED=1) tile.
   Delta(x) = sum_b lam(R_b x) - kappa(x)  (column-reflection localization; sum = W).
   CP : deficits paid from cells strictly below (max-flow) <=> every order ideal has sum Delta >= 0.
   FS : each cell x with Delta(x)>0 splits Delta(x) equally among the deficient cells y > x;
        every deficient y must receive >= -Delta(y).  (FS => CP => Wilf.)
   usage: cp_tree G */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
typedef unsigned __int128 u128;
#define PM 100
#ifndef GRADED
#define GRADED 0
#endif
static long sp_n, sp_tight, sp_tight_proper; static long majfail, rectfail, stairfail, pdfail, stairpfail, rectpfail, pnegfail; static int G; static long cnt, nsg, idfail, sgdef, cpfail, fsfail, nsfail, wfail; static double fsmin=1e30; static long defh[8], nonc;
static int cap[PM+2][PM+2], fl[PM+2][PM+2];
static int maxflow(int n,int s,int t){ int tot=0; static int prev[PM+2], q[PM+2]; for(int i=0;i<n;i++) for(int j=0;j<n;j++) fl[i][j]=0;
  while(1){ for(int i=0;i<n;i++) prev[i]=-1; prev[s]=s; int h=0,tl=0; q[tl++]=s;
    while(h<tl&&prev[t]<0){ int u=q[h++]; for(int v=0;v<n;v++) if(prev[v]<0&&cap[u][v]-fl[u][v]>0){ prev[v]=u; q[tl++]=v; } }
    if(prev[t]<0) break; int aug=1<<30; for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; int r=cap[u][v]-fl[u][v]; if(r<aug) aug=r; }
    for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; fl[u][v]+=aug; fl[v][u]-=aug; } tot+=aug; }
  return tot; }
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static int ap[PM], X[PM][PM], ng[PM], m, d, M;
static int up(int r,int a){ int nv=ap[r]+ng[a]; int t=nv%m; if(ap[t]!=nv) return -1; for(int h=0;h<d;h++) if(X[t][h]!=X[r][h]+(h==a)) return -1; return t; }
static int leq(int y,int x){ for(int h=0;h<d;h++) if(X[y][h]>X[x][h]) return 0; return 1; }
static void show(const char*tag,long W){ printf("%s m=%d d=%d M=%d W=%ld gens:",tag,m,d,M,W); for(int a=0;a<d;a++) printf(" %d",ng[a]); printf("\n"); fflush(stdout); }
static void analyze(u128 gm,int F,int mm,int *gens,int e){
  m=mm; d=0; M=0; for(int i=0;i<e;i++) if(gens[i]!=m) ng[d++]=gens[i];
  if(d<1) return;
  for(int r=0;r<m;r++){int w=r;while(gapq(gm,w))w+=m;ap[r]=w;if(w>M)M=w;}
  int ready[PM]={0}; ready[0]=1; for(int h=0;h<d;h++) X[0][h]=0;
  for(int w=1;w<=M;w++){ int r=w%m; if(ap[r]!=w) continue; int found=0; int best[PM]; int bdeg=1<<30;
    for(int j=0;j<d;j++) if(w>=ng[j]){ int t=(w-ng[j])%m; if(ap[t]==w-ng[j]){ assert(ready[t]); int cand[PM]; int cd=0; for(int h=0;h<d;h++){ cand[h]=X[t][h]+(h==j); cd+=cand[h]; }
        int better=0; if(!found) better=1; else if(GRADED && cd<bdeg) better=1; else if(!GRADED || cd==bdeg){ for(int h=0;h<d;h++){ if(cand[h]!=best[h]){ better=(cand[h]>best[h]); break; } } }
        if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
    assert(found); for(int h=0;h<d;h++) X[r][h]=best[h]; ready[r]=1; }
  nsg++;
  long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)d*l-g; if(W<0){ wfail++; show("WILF FAIL",W); }
  /* MAJ: for every k, top-k(kappa) <= d * top-k(lambda) */
  { int kk[PM], ll[PM]; for(int r=0;r<m;r++){ kk[r]=ap[r]/m; ll[r]=(M-ap[r])/m; }
    for(int i=1;i<m;i++){ int x=kk[i],j=i-1; while(j>=0&&kk[j]<x){ kk[j+1]=kk[j]; j--; } kk[j+1]=x; }
    for(int i=1;i<m;i++){ int x=ll[i],j=i-1; while(j>=0&&ll[j]<x){ ll[j+1]=ll[j]; j--; } ll[j+1]=x; }
    long a=0,b=0; int bad=0; long mn=1L<<40; for(int k=0;k<m;k++){ a+=kk[k]; b+=ll[k]; long sl=(long)d*b-a; if(sl<mn) mn=sl; if(sl<0) bad=1; }
    if(bad){ majfail++; if(majfail<=5) show("MAJ FAIL",W); } }
  /* RECT: for all i,k: sum_{j<=i} min(a_j,k) <= d sum_{j<=i} min(b_j,k), a_j=#{kappa>=j}, b_j=#{lambda>=j} */
  { static int a[400], b[400]; int K=M/m; for(int j=0;j<=K+1;j++){ a[j]=0; b[j]=0; }
    for(int r=0;r<m;r++){ int kk=ap[r]/m, ll=(M-ap[r])/m; for(int j=1;j<=kk;j++) a[j]++; for(int j=1;j<=ll;j++) b[j]++; }
    int bad=0; for(int k=1;k<=m&&!bad;k++){ long A=0,B=0; for(int i=1;i<=K;i++){ A+=a[i]<k?a[i]:k; B+=b[i]<k?b[i]:k; if(A>(long)d*B){ bad=1; break; } } }
    if(bad){ rectfail++; if(rectfail<=5) show("RECT FAIL",W); }
    { int pd=0; for(int j=1;j<=K;j++) if(a[j]>(long)d*b[j]) pd=1; if(pd){ pdfail++; if(pdfail<=5) show("PERDEPTH FAIL",W); } }
    /* STAIR: max over staircases z_1>=z_2>=...>=z_K>=0 of sum_j [min(a_j,z_j) - d min(b_j,z_j)] must be <= 0 */
    { static long best[PM+2], nb[PM+2]; for(int z=0;z<=m;z++) best[z]=0; /* best[z] = max value of rows 1..j with z_j = z ... process j=1..K */
      long mx=0; for(int j=1;j<=K;j++){ /* prefix-max over z' >= z of best[z'] (previous row length >= current) */
        long run=-(1L<<40); for(int z=m;z>=0;z--){ if(best[z]>run) run=best[z]; long val=(long)(a[j]<z?a[j]:z)-(long)d*(b[j]<z?b[j]:z); nb[z]=(j==1?0:run)+val; if(j==1) nb[z]=val; }
        for(int z=0;z<=m;z++){ best[z]=nb[z]; if(best[z]>mx) mx=best[z]; } }
      if(mx>0){ stairfail++; if(stairfail<=5) show("STAIR FAIL",W); } }
    /* STAIR-p: p_j=a_j-b_j; max over staircases of sum [min(p_j,z_j) - (d-1) min(b_j,z_j)] <= 0 ; also RECT-p and per-depth-p */
    { static long best[PM+2], nb[PM+2]; for(int z=0;z<=m;z++) best[z]=0; long mx=0; int neg=0;
      for(int j=1;j<=K;j++){ long pj=a[j]-b[j]; if(pj<0) neg=1; long run=-(1L<<40); for(int z=m;z>=0;z--){ if(best[z]>run) run=best[z]; long val=(pj<z?pj:z)-(long)(d-1)*(b[j]<z?b[j]:z); nb[z]=(j==1?val:run+val); }
        for(int z=0;z<=m;z++){ best[z]=nb[z]; if(best[z]>mx) mx=best[z]; } }
      if(neg){ pnegfail++; if(pnegfail<=3) show("p_j<0 ?!",W); }
      if(mx>0){ stairpfail++; if(stairpfail<=5) show("STAIR-p FAIL",W); }
      if(d>=3){ /* best nonzero staircase (z_1>=1) */
        static long bz[PM+2], nz[PM+2]; long NEG=-(1L<<40); long mxz=NEG; long fullv=0; int argK=0;
        for(int j=1;j<=K;j++){ long pj=a[j]-b[j]; long run=NEG; for(int z=m;z>=0;z--){ if(j>1 && bz[z]>run) run=bz[z]; long val=(pj<z?pj:z)-(long)(d-1)*(b[j]<z?b[j]:z);
            if(j==1) nz[z]=(z>=1?val:NEG); else nz[z]=(run==NEG?NEG:run+val); }
          for(int z=0;z<=m;z++){ bz[z]=nz[z]; if(bz[z]>mxz){ mxz=bz[z]; argK=j; } } }
        for(int j=1;j<=K;j++){ long pj=a[j]-b[j]; fullv+=pj-(long)(d-1)*b[j]; }
        sp_n++; if(mxz==0){ sp_tight++; if(fullv<0){ sp_tight_proper++; if(sp_tight_proper<=8){ printf("STAIR-p tight proper (full=%ld, rows=%d) ",fullv,argK); show("",W); } } } } 
      int bad=0; for(int k2=1;k2<=m&&!bad;k2++){ long A=0,B=0; for(int i=1;i<=K;i++){ long pj=a[i]-b[i]; A+=pj<k2?pj:k2; B+=b[i]<k2?b[i]:k2; if(A>(long)(d-1)*B){ bad=1; break; } } } if(bad) rectpfail++; } }
  long Dl[PM]; long tot=0;
  for(int r=0;r<m;r++){ long De=-(ap[r]/m);
    for(int b=0;b<d;b++){ int J=X[r][b], cur=r; while(1){ int nx=up(cur,b); if(nx<0) break; cur=nx; J++; }
      long vR=ap[r]+(long)(J-2*X[r][b])*ng[b]; De+=(M-vR)/m; }
    Dl[r]=De; tot+=De; }
  if(tot!=W){ idfail++; if(idfail<5) show("ID FAIL",W); return; }
  long dem=0; for(int r=0;r<m;r++) if(Dl[r]<0){ dem+=-Dl[r]; int k=(int)(-Dl[r]); defh[k<7?k:7]++; int corner=1; for(int b=0;b<d;b++) if(up(r,b)>=0) corner=0; if(!corner) nonc++; }
  if(dem==0) return; sgdef++;
  /* NS: own lower covers, no sharing */
  { int bad=0; for(int r=0;r<m;r++) if(Dl[r]<0){ long s=0; for(int a=0;a<d;a++) if(X[r][a]>0){ int pv=ap[r]-ng[a]; int pr=pv%m; if(pv>=0&&ap[pr]==pv&&Dl[pr]>0) s+=Dl[pr]; } if(s<-Dl[r]) bad=1; } if(bad) nsfail++; }
  /* FS */
  { double got[PM]; int N[PM]; for(int r=0;r<m;r++){ got[r]=0; N[r]=0; }
    for(int x=0;x<m;x++) if(Dl[x]>0){ for(int y=0;y<m;y++) if(y!=x&&Dl[y]<0&&leq(x,y)) N[x]++; }
    for(int x=0;x<m;x++) if(Dl[x]>0&&N[x]) for(int y=0;y<m;y++) if(y!=x&&Dl[y]<0&&leq(x,y)) got[y]+=(double)Dl[x]/N[x];
    int bad=0; for(int y=0;y<m;y++) if(Dl[y]<0){ double sl=got[y]+Dl[y]; if(sl<fsmin) fsmin=sl; if(sl< -1e-9) bad=1; }
    if(bad){ fsfail++; if(fsfail<=10) show("FS FAIL",W); } }
  /* CP */
  { int n=m+2,S0=m,T0=m+1; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0;
    for(int r=0;r<m;r++){ if(Dl[r]>0) cap[S0][r]=(int)Dl[r]; if(Dl[r]<0) cap[r][T0]=(int)(-Dl[r]); }
    for(int x=0;x<m;x++) if(Dl[x]<0) for(int y=0;y<m;y++) if(y!=x&&Dl[y]>0&&leq(y,x)) cap[y][x]=1<<20;
    int f=maxflow(n,S0,T0); if(f<dem){ cpfail++; if(cpfail<=10) show("CP FAIL",W); } }
}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  cnt++; if(m>1&&m<PM) analyze(gm,F,m,gens,e);
  if(genus==G) return; int ng2[PM*2];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng2[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng2[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng2[e2++]=y; }
    visit(gm2,nn,m2,ng2,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); int gens[]={1}; visit(0,-1,1,gens,1,0);
  printf("GRADED=%d genus<=%d all=%ld analyzed=%ld IDfail=%ld Wilf fails=%ld | S with a deficit %ld | CP fails %ld | FS fails %ld (min FS slack %.4f) | NS fails %ld | noncorner deficient cells %ld | deficit hist:",GRADED,G,cnt,nsg,idfail,wfail,sgdef,cpfail,fsfail,fsmin,nsfail,nonc);
  for(int i=1;i<8;i++) printf(" %ld",defh[i]); printf(" | MAJ fails %ld | RECT fails %ld | STAIR fails %ld | per-depth fails %ld | STAIR-p fails %ld | RECT-p fails %ld | p<0 %ld | e>=4: %ld S, nonzero staircase tight %ld (proper, W>0 side: %ld)\n",majfail,rectfail,stairfail,pdfail,stairpfail,rectpfail,pnegfail,sp_n,sp_tight,sp_tight_proper); return 0; }
