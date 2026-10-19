/* For a given semigroup (generators on the command line), compute the Apery down-set under many weight term orders
   (weight vector w > 0, ties by lex), the G-ID cells, and test OI (below) and shift+below flow feasibility.
   usage: order_test ntrials m n1 n2 ... */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 400
#define DM 32
#define NN (MM+2)
static int cap[NN][NN], fl[NN][NN];
static int maxflow(int n,int s,int t){ int tot=0; static int prev[NN], q[NN]; for(int i=0;i<n;i++) for(int j=0;j<n;j++) fl[i][j]=0;
  while(1){ for(int i=0;i<n;i++) prev[i]=-1; prev[s]=s; int h=0,tl=0; q[tl++]=s;
    while(h<tl&&prev[t]<0){ int u=q[h++]; for(int v=0;v<n;v++) if(prev[v]<0&&cap[u][v]-fl[u][v]>0){ prev[v]=u; q[tl++]=v; } }
    if(prev[t]<0) break; int aug=1<<30; for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; int r=cap[u][v]-fl[u][v]; if(r<aug) aug=r; }
    for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; fl[u][v]+=aug; fl[v][u]-=aug; } tot+=aug; }
  return tot; }
static unsigned long long st=88172645463325252ULL; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){ int T=atoi(argv[1]); int m=atoi(argv[2]); int d=argc-3; long mg[DM]; for(int i=0;i<d;i++) mg[i]=atol(argv[3+i]);
  static long ap[MM]; static int done[MM];
  for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
  for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<d;k++){ int r2=(b+mg[k])%m; long v=ap[b]+mg[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
  long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r]; long mu=M%m; int tau=(mu<m-1-mu)?(int)mu:(int)(m-1-mu);
  int ord[MM]; for(int r=0;r<m;r++) ord[r]=r; for(int i=1;i<m;i++){ int x=ord[i],j=i-1; while(j>=0&&ap[ord[j]]>ap[x]){ ord[j+1]=ord[j]; j--; } ord[j+1]=x; }
  int okOI=0, okSB=0;
  for(int t=0;t<T;t++){ double w[DM]; for(int i=0;i<d;i++) w[i]= (t==0)?1.0 : (t==1? (double)mg[i] : (t==2? 1.0/mg[i] : 0.05+(rnd()%10000)/1000.0));
    static int X[MM][DM];
    for(int h=0;h<d;h++) X[0][h]=0;
    for(int ii=1;ii<m;ii++){ int r=ord[ii]; long wv=ap[r]; int found=0; double bw=1e300; int best[DM],cand[DM];
      for(int j=0;j<d;j++) if(wv>=mg[j]){ int tr=(int)((wv-mg[j])%m); if(ap[tr]==wv-mg[j]){ double cw=0; for(int h=0;h<d;h++){ cand[h]=X[tr][h]+(h==j); cw+=w[h]*cand[h]; }
        int better=!found; if(found){ if(cw<bw-1e-9) better=1; else if(cw<bw+1e-9){ for(int h=0;h<d;h++) if(cand[h]!=best[h]){ better=cand[h]>best[h]; break; } } }
        if(better){ memcpy(best,cand,sizeof(int)*d); bw=cw; found=1; } } }
      for(int h=0;h<d;h++) X[r][h]=best[h]; }
    long cx[MM]; long W=0; for(int r=1;r<m;r++){ long lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0;
      for(int a=0;a<d;a++){ sr+=(long)X[r][a]*(mg[a]%m); if(X[r][a]) B+=(long)X[r][a]*((eps+mg[a]%m)>=m); long nv=ap[r]+mg[a]; int tr=(int)(nv%m); int in=(ap[tr]==nv); if(in){ for(int h=0;h<d;h++) if(X[tr][h]!=X[r][h]+(h==a)){in=0;break;} } if(!in) phi+=X[r][a]+1; }
      cx[r]=lam*phi+B-sr/m; W+=cx[r]; }
    long dem=0; for(int r=1;r<m;r++) if(cx[r]<0) dem+=-cx[r];
    int res[2]={1,1};
    if(dem>0) for(int mode=0;mode<2;mode++){ int n=m+2,S0=m,T0=m+1; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0;
      for(int r=1;r<m;r++){ if(cx[r]>0) cap[S0][r]=(int)cx[r]; if(cx[r]<0) cap[r][T0]=(int)(-cx[r]); }
      for(int x=1;x<m;x++) if(cx[x]<0){ if(mode==1&&x<=mu){ int y=x+tau; if(y>mu&&y<m&&cx[y]>0) cap[y][x]+=1<<20; }
        for(int y=1;y<m;y++) if(y!=x&&cx[y]>0){ int le=1; for(int h=0;h<d;h++) if(X[y][h]>X[x][h]){le=0;break;} if(le) cap[y][x]+=1<<20; } }
      res[mode]=(maxflow(n,S0,T0)==dem); }
    okOI+=res[0]; okSB+=res[1];
    if(t<3) printf("order %s: W=%ld deficit=%ld OI=%d SB=%d\n", t==0?"grlex":(t==1?"weight=n":"weight=1/n"),W,dem,res[0],res[1]);
  }
  printf("m=%d d=%d: %d orders, OI feasible in %d, shift+below feasible in %d\n",m,d,T,okOI,okSB);
  return 0; }
