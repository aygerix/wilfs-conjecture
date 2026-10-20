/* Semigroup-tree test of P14's depth-five classification and GEN-EH.
 * The standard remove-an-effective-generator recursion is adapted from the
 * lead's m3_tree2.c. No genus computation is done locally. */
#include "core.h"
typedef unsigned __int128 u128;
static int G;static unsigned long long total,q4,topbad;static ll mintop=LLONG_MAX;
static unsigned long long high1,betacases,mfzero;static int minmfzero=9999;
static void show5(const char*tag,int m,int d,ll*n,ll*w,ll v,ll K){
 printf("%s m=%d v=%lld K=%lld gens=[%d",tag,m,v,K,m);for(int a=0;a<d;a++)printf(",%lld",n[a]);printf("] Ap=[");for(int i=0;i<m;i++)printf("%s%lld",i?",":"",w[i]);puts("]");fflush(stdout);
}
static void check5(int m,ll*w,int*gens,int e){
 ll n[128];int d=0;for(int a=0;a<e;a++)if(gens[a]!=m)n[d++]=gens[a];
 ll M=0;for(int i=0;i<m;i++)if(w[i]>M)M=w[i];int h=M-5*m+1;
 ll ell=0,Ltop=0,kv[128],ev[128],lv[128];int jd[128]={0},nf[128]={0};ll fac[128][5];
 for(int i=0;i<m;i++){
  ll v=w[i];ell+=(M-v)/m;ev[i]=-v;lv[i]=0;
  for(int a=0;a<d;a++){
   ll u=v;int j=0;while(u>=n[a]&&w[(u-n[a])%m]==u-n[a]){j++;u-=n[a];}
   ev[i]+=j*n[a];jd[i]+=j;
   for(int t=0;t<j&&nf[i]<5;t++)fac[i][nf[i]++]=n[a];
   if(j)lv[i]+=j*((M-v+n[a])/m-(M-v)/m);
   u=v;while(w[(u+n[a])%m]==u+n[a])u+=n[a];Ltop+=(M-u)/m;
  }
  kv[i]=5-(M-v)/m-lv[i];
  if(kv[i]>2||(ev[i]>0&&kv[i]>0)){show5("D5_CLASS_FAIL",m,d,n,w,v,kv[i]);exit(5);}
  if(ev[i]>0&&kv[i]==0){mfzero++;if(m<minmfzero){minmfzero=m;show5("MF_ZERO_RECORD",m,d,n,w,v,0);}}
 }
 int beta=0,H=0;for(int a=0;a<d;a++)if(2*n[a]>3*m+h-1&&n[a]<2*m)H++;
 for(int i=0;i<m;i++)if(kv[i]==2){
  beta++;ll v=w[i];int hc=0;
  if(ev[i]||jd[i]!=3||(M-v)/m!=0||lv[i]!=3){show5("D5_BETA_FAIL",m,d,n,w,v,2);exit(5);}
  for(int a=0;a<3;a++){
   ll n0=fac[i][a],p=v-n0;
   if(!(m+h<n0&&n0<2*m)||(M-p)/m!=1||kv[p%m]!=0||ev[p%m]){show5("D5_FACE_FAIL",m,d,n,w,v,2);exit(5);}
   if(2*n0>3*m+h-1)hc++;
  }
  if(hc<2||(M-v)%m>=(m-h)/2){show5("D5_ARC_FAIL",m,d,n,w,v,2);exit(5);}
 }
 ll W=e*ell-(M-m+1),sl=W-e+h;
 ll sumK=0;for(int i=0;i<m;i++)sumK+=kv[i];if(W!=(m-h)+Ltop-sumK){puts("D5_K_ID_FAIL");exit(5);}
 if(sl<mintop){mintop=sl;show5("GEN_EH_RECORD",m,d,n,w,0,sl);}
 if(H<=1){high1++;if(sl<0){show5("HIGH1_THEOREM_FAIL",m,d,n,w,0,sl);exit(5);}}
 if(beta)betacases++;
 if(sl<0){show5("GEN_EH_COUNTEREXAMPLE",m,d,n,w,0,sl);exit(4);}
}
static int gap(u128 g,int x){return x<128&&((g>>x)&1);}
static void visit(u128 gm,int F,int m,int*gens,int e,int genus){
 total++;
 if(m>=2&&F+1>4*m&&F+1<=5*m){ll w[MM];for(int i=0;i<m;i++){int x=i;while(gap(gm,x))x+=m;w[i]=x;}q4++;check5(m,w,gens,e);
 }
 if(genus==G)return;int ng[128];
 for(int j=0;j<e;j++){int n=gens[j];if(n<=F)continue;u128 g2=gm|((u128)1<<n);int e2=0,m2;
  if(n==m){m2=m+1;for(int k=m2;k<2*m2;k++)ng[e2++]=k;}
  else{m2=m;for(int k=0;k<e;k++)if(gens[k]!=n)ng[e2++]=gens[k];int y=n+m,dec=0;for(int a=m;a<=y/2&&!dec;a++)if(a!=n&&!gap(g2,a)&&y-a!=n&&!gap(g2,y-a))dec=1;if(!dec)ng[e2++]=y;}
  visit(g2,n,m2,ng,e2,genus+1);
 }
}
int main(int argc,char**argv){G=argc>1?atoi(argv[1]):28;if(G>40)return 4;int a[1]={1};visit(0,-1,1,a,1,0);printf("SUMMARY G=%d total=%llu q5=%llu high1=%llu K2cases=%llu MFzero_values=%llu minGENEH=%lld\n",G,total,q4,high1,betacases,mfzero,mintop);}
