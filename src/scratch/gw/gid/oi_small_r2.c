/* Random stress test of Conjecture WQ (e >= 4): units + window (mu, min(2mu,m-1)] pay every deficit.
   Down-set = graded-lex normal forms (GR=1) or lex (GR=0) of Ap(S,m). c_x = lam*phi + B - gamma (G-ID).
   samplers: 0 band gens, 1 truncated at C (Eliahou-type), 2 uniform gens.  usage: wq_rand seed trials mmin mmax GR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 260
#define DM 200
#define NN (MM+2)
static int cap[NN][NN], fl[NN][NN];
static int maxflow(int n,int s,int t){ int tot=0; static int prev[NN], q[NN]; for(int i=0;i<n;i++) for(int j=0;j<n;j++) fl[i][j]=0;
  while(1){ for(int i=0;i<n;i++) prev[i]=-1; prev[s]=s; int h=0,tl=0; q[tl++]=s;
    while(h<tl&&prev[t]<0){ int u=q[h++]; for(int v=0;v<n;v++) if(prev[v]<0&&cap[u][v]-fl[u][v]>0){ prev[v]=u; q[tl++]=v; } }
    if(prev[t]<0) break; int aug=1<<30; for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; int r=cap[u][v]-fl[u][v]; if(r<aug) aug=r; }
    for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; fl[u][v]+=aug; fl[v][u]-=aug; } tot+=aug; }
  return tot; }
static long cxs[MM];
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[MM]; static int done[MM], gens[64], isg[MM], X[MM][DM]; static long mg[DM]; static int gi[MM];
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+3; long T=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int GR=atoi(argv[5]);
  long tested[3]={0},fails[3]={0}; static long oif[16], oisf[16]; static long h3lc=0,h3lb=0,h3n=0,h3pos=0,h3fu=0,h3fp=0,h3fall=0; static long h3minu=1L<<40,h3minp=1L<<40; static int cdeg[MM]; long dt[16]={0}, df[16]={0}; long dmin[16]; for(int i=0;i<16;i++) dmin[i]=1L<<40; long minq[3]={1L<<40,1L<<40,1L<<40}; long wneg=0; long bigdeg=0;
  for(long t=0;t<T;t++){
    int samp=rnd()%3; int dd=3+rnd()%5; int cmax=(dd+3)*(dd+2)*(dd+1)/6; int m=8+rnd()%(cmax>8?cmax-7:1); if(m>MM-2) m=MM-2; int g0=0; long C=-1; int ng=dd;
    { double lo=1.0+(rnd()%2000)/1000.0, wid=(rnd()%1000)/1000.0*(samp==0?0.3:(samp==1?0.8:1.5)); for(int k=0;k<ng;k++) gens[g0++]=(int)(m*(lo+wid*((rnd()%10000)/10000.0)))+1; }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    if(C>=0){ for(int r=1;r<m;r++){ long f=C+((r-C%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    int d=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } isg[r]=!dec; if(!dec){ if(d>=DM){ok=0;break;} gi[r]=d; mg[d++]=ap[r]; } }
    if(!ok||d<3) continue;
    /* normal forms: process residues by increasing ap value */
    int ord[MM]; for(int r=0;r<m;r++) ord[r]=r; for(int i=1;i<m;i++){ int x=ord[i],j=i-1; while(j>=0&&ap[ord[j]]>ap[x]){ ord[j+1]=ord[j]; j--; } ord[j+1]=x; }
    for(int h=0;h<d;h++) X[0][h]=0;
    for(int ii=1;ii<m;ii++){ int r=ord[ii]; long w=ap[r]; int found=0, bdeg=1<<30; static int best[DM], cand[DM];
      for(int j=0;j<d;j++) if(w>=mg[j]){ int tr=(int)((w-mg[j])%m); if(ap[tr]==w-mg[j]){ int cd=0; for(int h=0;h<d;h++){ cand[h]=X[tr][h]+(h==j); cd+=cand[h]; }
          int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int h=0;h<d;h++) if(cand[h]!=best[h]){ better=cand[h]>best[h]; break; } } }
          if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
      if(!found){ ok=0; break; } for(int h=0;h<d;h++) X[r][h]=best[h]; }
    if(!ok) continue;
    long mu=M%m; long hi=(2*mu<=m-1)?2*mu:m-1; long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)d*l-g;
    long Qwin=0,Qdebt=0,tot=0; int maxdeg=0;
    for(int r=1;r<m;r++){ long lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0; int deg=0;
      for(int a=0;a<d;a++){ deg+=X[r][a]; sr+=(long)X[r][a]*(mg[a]%m); if(X[r][a]) B+=(long)X[r][a]*((eps+mg[a]%m)>=m);
        long nv=ap[r]+mg[a]; int tr=(int)(nv%m); int in=(ap[tr]==nv); if(in){ for(int h=0;h<d;h++) if(X[tr][h]!=X[r][h]+(h==a)){in=0;break;} } if(!in) phi+=X[r][a]+1; }
      long cx=lam*phi+B-sr/m; cxs[r]=cx; cdeg[r]=deg; tot+=cx; if(deg>maxdeg) maxdeg=deg;
      if(deg==1 || (r>mu && r<=hi)) Qwin+=cx; else if(cx<0) Qdebt+=-cx; }
    if(tot!=W){ printf("IDENTITY FAIL\n"); }
    if(maxdeg==3){ int tau=(mu< m-1-mu)?(int)mu:(int)(m-1-mu); long res=0,su=0,sp=0,sc=0; static int used[MM]; for(int r=0;r<m;r++) used[r]=0; int anyd=0;
      for(int x=1;x<m;x++) if(cxs[x]<0){ anyd=1; long dfx=-cxs[x]; int paid=0; if(x<=mu){ int y=x+tau; if(y>mu&&y<m&&cxs[y]>=1){ paid=1; used[y]=1; } } res+=dfx-paid; }
      for(int y=1;y<m;y++) if(cxs[y]>0){ long spv=cxs[y]-used[y]; if(cdeg[y]==1) su+=spv; else if(cdeg[y]==2) sp+=spv; else sc+=spv; }
      if(anyd && res>0){ /* local flow: residual demand of x routed to lower-cover pairs (spare = c - used), or lower pairs at distance (any pair below) */
        for(int mode=0;mode<2;mode++){ int n=m+2,S0=m,T0=m+1; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0; long dm=0;
          for(int x=1;x<m;x++) if(cxs[x]<0){ long dfx=-cxs[x]; int paid=0; if(x<=mu){ int y=x+tau; if(y>mu&&y<m&&cxs[y]>=1) paid=1; } if(dfx-paid>0){ cap[x][T0]=(int)(dfx-paid); dm+=dfx-paid; } }
          for(int y=1;y<m;y++) if(cdeg[y]==2 && cxs[y]-used[y]>0) cap[S0][y]=(int)(cxs[y]-used[y]);
          for(int x=1;x<m;x++) if(cap[x][T0]>0) for(int y=1;y<m;y++) if(cdeg[y]==2&&y!=x){ int le=1,df=0; for(int h=0;h<d;h++){ if(X[y][h]>X[x][h]){le=0;break;} df+=X[x][h]-X[y][h]; } if(le && (mode==1 || df==1)) cap[y][x]=1<<20; }
          int f=maxflow(n,S0,T0); if(f<dm){ if(mode==0) h3lc++; else h3lb++; if(mode==0&&h3lc<=4){ printf("H3 LOCALFAIL m=%d d=%d mu=%ld res=%ld flow=%d gens:",m,d,mu,dm,f); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n"); } } } }
      if(anyd){ h3n++; if(res>0) h3pos++; if(res>su) h3fu++; if(res>sp) h3fp++; if(res>su+sp+sc) h3fall++; if(su-res<h3minu) h3minu=su-res; if(sp-res<h3minp) h3minp=sp-res;
        if(res>su && h3fu<=3){ printf("H3 UNITFAIL m=%d d=%d mu=%ld res=%ld su=%ld sp=%ld gens:",m,d,mu,res,su,sp); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n"); } } }
    { long dem=0; for(int r=1;r<m;r++) if(cxs[r]<0) dem+=-cxs[r];
      if(dem>0){ int tau=(mu< m-1-mu)?(int)mu:(int)(m-1-mu);
        for(int mode=0;mode<2;mode++){ int n=m+2,S0=m,T0=m+1; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0;
          for(int r=1;r<m;r++){ if(cxs[r]>0) cap[S0][r]=(int)cxs[r]; if(cxs[r]<0) cap[r][T0]=(int)(-cxs[r]); }
          for(int x=1;x<m;x++) if(cxs[x]<0){ if(mode==1 && x<=mu){ int y=x+tau; if(y>mu&&y<m&&cxs[y]>0) cap[y][x]+=1<<20; }
            for(int y=1;y<m;y++) if(y!=x&&cxs[y]>0){ int le=1; for(int h=0;h<d;h++) if(X[y][h]>X[x][h]){le=0;break;} if(le) cap[y][x]+=1<<20; } }
          int f=maxflow(n,S0,T0); int md=maxdeg<15?maxdeg:15; if(f<dem){ if(mode==0) oif[md]++; else oisf[md]++; if(0){ printf("SB FAIL maxdeg=%d m=%d d=%d mu=%ld K=%ld W=%ld dem=%ld flow=%d gens:",maxdeg,m,d,mu,M/m,W,dem,f); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n"); }
          if(mode==0 && oif[md]<=0){ printf("OI FAIL maxdeg=%d m=%d d=%d mu=%ld W=%ld dem=%ld flow=%d gens:",maxdeg,m,d,mu,W,dem,f); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n"); } } } } }
    if(W<0){ wneg++; printf("WILF FAIL?! m=%d\n",m); }
    if(maxdeg>=4) bigdeg++;
    { int md=maxdeg<15?maxdeg:15; dt[md]++; long qq=Qwin-Qdebt; if(qq<0) df[md]++; if(qq<dmin[md]) dmin[md]=qq; }
    tested[samp]++; long q=Qwin-Qdebt; if(q<minq[samp]) minq[samp]=q;
    if(q<0){ fails[samp]++; if(fails[samp]<=0){ printf("WQ FAIL samp=%d m=%d d=%d mu=%ld M=%ld K=%ld W=%ld Qwin=%ld Qdebt=%ld maxdeg=%d gens:",samp,m,d,mu,M,M/m,W,Qwin,Qdebt,maxdeg); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n"); } }
  }
  for(int i=1;i<16;i++) if(dt[i]) printf("maxdeg=%d tested=%ld WQfail=%ld minQ=%ld | OI(below) fail=%ld  shift+below fail=%ld\n",i,dt[i],df[i],dmin[i],oif[i],oisf[i]);
  printf("local pair-cover flow fails %ld, pair-below flow fails %ld\n",h3lc,h3lb); printf("height3 with deficit=%ld residual>0=%ld | res>unit spare %ld, res>pair spare %ld, res>all %ld | min(unit-res)=%ld min(pair-res)=%ld\n",h3n,h3pos,h3fu,h3fp,h3fall,h3minu,h3minp);
  printf("seed=%s GR=%d tested band=%ld trunc=%ld unif=%ld | WQ fails %ld %ld %ld | minQ %ld %ld %ld | maxdeg>=4: %ld | Wilf fails %ld\n",argv[1],GR,tested[0],tested[1],tested[2],fails[0],fails[1],fails[2],minq[0],minq[1],minq[2],bigdeg,wneg);
  return 0; }
