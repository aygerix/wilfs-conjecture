/* Payment-flow test for the G-ID decomposition W = sum_x c_x (exhaustive semigroup tree, genus <= G).
   Sources: cells with c>0 (capacity c). Sinks: cells with c<0 (demand -c).
   Edge types: (S) shift: window cell at residue s+tau pays crown cell at residue s (tau=min(mu,m-1-mu), s<=mu);
               (L) lower cover: y pays x if y = x - e_a (y in D);
               (P) any lower element: y pays x if y <= x (componentwise), y != x   [option].
   Reports feasibility counts for: S only, L only, S+L, S+P, P only; by max degree.  usage: gflow G GR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
typedef unsigned __int128 u128;
#define PM 72
#define NN (PM+2)
static int G, GR; static long cnt;
static int cap[NN][NN], fl[NN][NN];
static int maxflow(int n,int s,int t){ int tot=0; static int prev[NN], q[NN]; for(int i=0;i<n;i++) for(int j=0;j<n;j++) fl[i][j]=0;
  while(1){ for(int i=0;i<n;i++) prev[i]=-1; prev[s]=s; int h=0,tl=0; q[tl++]=s;
    while(h<tl&&prev[t]<0){ int u=q[h++]; for(int v=0;v<n;v++) if(prev[v]<0&&cap[u][v]-fl[u][v]>0){ prev[v]=u; q[tl++]=v; } }
    if(prev[t]<0) break; int aug=1<<30; for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; int r=cap[u][v]-fl[u][v]; if(r<aug) aug=r; }
    for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; fl[u][v]+=aug; fl[v][u]-=aug; } tot+=aug; }
  return tot; }
static long nS[8],okS[8],okL[8],okSL[8],okSP[8],okP[8],ndef[8]; static long tightmin=1L<<40; static long tighthist[20];
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static void analyze(u128 gm,int m,int *gens,int e){
  int ap[PM],M=0,ng[PM],d=0; static int X[PM][PM];
  for(int i=0;i<e;i++) if(gens[i]!=m) ng[d++]=gens[i];
  if(d<3) return;
  for(int r=0;r<m;r++){int w=r;while(gapq(gm,w))w+=m;ap[r]=w;if(w>M)M=w;}
  int ord[PM]; for(int r=0;r<m;r++) ord[r]=r; for(int i=1;i<m;i++){ int x=ord[i],j=i-1; while(j>=0&&ap[ord[j]]>ap[x]){ ord[j+1]=ord[j]; j--; } ord[j+1]=x; }
  for(int h=0;h<d;h++) X[0][h]=0;
  for(int ii=1;ii<m;ii++){ int r=ord[ii]; int w=ap[r]; int found=0,bdeg=1<<30; int best[PM],cand[PM];
    for(int j=0;j<d;j++) if(w>=ng[j]){ int t=(w-ng[j])%m; if(ap[t]==w-ng[j]){ int cd=0; for(int h=0;h<d;h++){ cand[h]=X[t][h]+(h==j); cd+=cand[h]; }
      int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int h=0;h<d;h++) if(cand[h]!=best[h]){ better=cand[h]>best[h]; break; } } }
      if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
    assert(found); for(int h=0;h<d;h++) X[r][h]=best[h]; }
  int mu=M%m; int tau = mu < m-1-mu ? mu : m-1-mu;
  long cx[PM]; int deg[PM]; int maxdeg=0; int anydef=0;
  for(int r=0;r<m;r++){ cx[r]=0; deg[r]=0; }
  for(int r=1;r<m;r++){ int lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0; int dg=0;
    for(int a=0;a<d;a++){ dg+=X[r][a]; sr+=(long)X[r][a]*(ng[a]%m); if(X[r][a]) B+=(long)X[r][a]*((eps+ng[a]%m)>=m);
      int t=(ap[r]+ng[a])%m; int in=(ap[t]==ap[r]+ng[a]); if(in){ for(int h=0;h<d;h++) if(X[t][h]!=X[r][h]+(h==a)){in=0;break;} } if(!in) phi+=X[r][a]+1; }
    cx[r]=(long)lam*phi+B-sr/m; deg[r]=dg; if(dg>maxdeg) maxdeg=dg; if(cx[r]<0) anydef=1; }
  int md=maxdeg<7?maxdeg:7; nS[md]++;
  if(maxdeg==3 && anydef){ /* closure: min sum_L c over down-sets L containing x */
    long best=1L<<40; int bx=-1;
    for(int x=1;x<m;x++) if(cx[x]<0){ int n=m+2,S0=m,T0=m+1; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0;
      long posum=0; for(int r=1;r<m;r++){ long w=-cx[r]; if(r==x) w=1<<22; if(w>0) cap[S0][r]=(int)w; else if(w<0) cap[r][T0]=(int)(-w); if(w>0) posum+=w; }
      for(int v=1;v<m;v++) for(int u=1;u<m;u++) if(u!=v){ int le=1; for(int h=0;h<d;h++) if(X[u][h]>X[v][h]){le=0;break;} if(le) cap[v][u]=1<<28; }
      long f=maxflow(n,S0,T0); long maxw=posum-f; long val=-(maxw-(1<<22)-cx[x]) ; /* min sum_L c with x forced */
      if(val<best){best=val;bx=x;} }
    if(best<tightmin){ tightmin=best; printf("TIGHT min_L(sum c)=%ld m=%d d=%d mu=%d M=%d gens:",best,m,d,mu,M); for(int a=0;a<d;a++) printf(" %d",ng[a]); printf("  x=(" ); for(int h=0;h<d;h++) printf("%d",X[bx][h]); printf(")\n"); }
    int bi=best<19?(int)best:19; if(bi<0) bi=0; tighthist[bi]++; } if(!anydef){ okS[md]++; okL[md]++; okSL[md]++; okSP[md]++; okP[md]++; return; }
  ndef[md]++;
  int n=m+2, S=m, T=m+1; long dem=0; for(int r=1;r<m;r++) if(cx[r]<0) dem+=-cx[r];
  for(int mode=0;mode<5;mode++){ /* 0:S 1:L 2:S+L 3:S+P 4:P */
    for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0;
    for(int r=1;r<m;r++){ if(cx[r]>0) cap[S][r]=(int)cx[r]; if(cx[r]<0) cap[r][T]=(int)(-cx[r]); }
    for(int x=1;x<m;x++) if(cx[x]<0){
      if(mode==0||mode==2||mode==3){ if(x<=mu){ int y=x+tau; if(y>mu && y<m && cx[y]>0) cap[y][x]+=1<<20; } }
      for(int y=1;y<m;y++) if(y!=x && cx[y]>0){ int le=1, cover=0; int diff=0; for(int h=0;h<d;h++){ if(X[y][h]>X[x][h]){le=0;break;} diff+=X[x][h]-X[y][h]; }
        if(!le) continue; cover=(diff==1);
        if((mode==1||mode==2)&&cover) cap[y][x]+=1<<20;
        if((mode==3||mode==4)) cap[y][x]+=1<<20; } }
    int f=maxflow(n,S,T); int ok=(f==dem);
    if(mode==0) okS[md]+=ok; else if(mode==1) okL[md]+=ok; else if(mode==2) okSL[md]+=ok; else if(mode==3) okSP[md]+=ok; else okP[md]+=ok; }
}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  cnt++; if(m>1&&m<PM) analyze(gm,m,gens,e);
  if(genus==G) return; int ng[2*PM];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); GR=atoi(argv[2]); int gens[]={1}; visit(0,-1,1,gens,1,0);
  printf("genus<=%d GR=%d all=%ld (d>=3 only)\n",G,GR,cnt); printf("height-3 tightness histogram:"); for(int i=0;i<20;i++) printf(" %d:%ld",i,tighthist[i]); printf("\n");
  for(int md=1;md<8;md++) if(nS[md]) printf(" maxdeg=%d S=%ld with-deficit=%ld | feasible: shift %ld, cover %ld, shift+cover %ld, shift+below %ld, below %ld\n",md,nS[md],ndef[md],okS[md],okL[md],okSL[md],okSP[md],okP[md]);
  return 0; }
