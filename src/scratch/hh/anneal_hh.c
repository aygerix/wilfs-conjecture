/* Adversarial annealer for MaxCL at Apery height <= H (lead, 2026-10-19).
   State: unit labels P[0..K-1] (distinct, nonzero mod m) and a down-set C of monomials of degree <= H in K variables,
   containing 0 and every unit, with x -> x.P mod m injective on C.  Missing residues are spikes (weight 0).
   d = K + m - |C|.  S(sigma) = sum_C w(x)((phi(x)-sigma) mod m), w = d+1 on non-maximal cells, -(|x|-1) on maximal.
   Objective: ratio = min_sigma S / (Ctot (m-1)/2)  (Ctot = sum of weights; the sigma-average of S is Ctot(m-1)/2),
   plus penalties unless (#non-maximal units >= KMIN and #cells of degree H >= TMIN).
   Prints every state with S < 0 (MaxCL violation) and the best constrained state.
   usage: anneal_hh K H m seed iters restarts   (env KMIN, TMIN, INIT=1 postage-stamp start) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef long long ll;
#define MAXC 1200
#define MAXM 2048
#define MAXK 10
static int K, H, m, nc, ex[MAXC][MAXK], deg[MAXC], up[MAXC][MAXK], lo[MAXC][MAXK], nlo[MAXC], byDeg[8][MAXC], nby[8];
static int KMIN=3, TMIN=1, SMAX=100000, OBJ=0;
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline double urand(void){ return (rnd()>>11)*(1.0/9007199254740992.0); }
typedef struct { int P[MAXK]; unsigned char in[MAXC]; int own[MAXM]; int lab[MAXC]; } St;
static int find(int *e){ for(int i=0;i<nc;i++){ int ok=1; for(int a=0;a<K;a++) if(ex[i][a]!=e[a]){ok=0;break;} if(ok) return i; } return -1; }
static int cur_e[MAXK];
static void gen(int a, int left, int dg){ /* all exponent vectors of total degree dg */
  if(a==K-1){ cur_e[a]=left; memcpy(ex[nc],cur_e,sizeof cur_e); deg[nc]=dg; byDeg[dg][nby[dg]++]=nc; nc++; return; }
  for(int v=left; v>=0; v--){ cur_e[a]=v; gen(a+1,left-v,dg); } }
static void build(void){
  nc=0; for(int dg=0; dg<=H; dg++) gen(0,dg,dg);
  int e[MAXK];
  for(int i=0;i<nc;i++){ nlo[i]=0;
    for(int a=0;a<K;a++){ memcpy(e,ex[i],sizeof e); e[a]++; up[i][a]=(deg[i]<H)?find(e):-1;
      if(ex[i][a]>0){ memcpy(e,ex[i],sizeof e); e[a]--; lo[i][nlo[i]++]=find(e); } } }
}
static void relabel(St *s){ for(int i=0;i<nc;i++){ ll L=0; for(int a=0;a<K;a++) L+=(ll)ex[i][a]*s->P[a]; s->lab[i]=(int)(L%m); } }
static int rebuild(St *s, const unsigned char *old){
  for(int r=0;r<m;r++) s->own[r]=-1;
  memset(s->in,0,sizeof s->in);
  for(int dg=0; dg<=H; dg++) for(int j=0;j<nby[dg];j++){ int i=byDeg[dg][j];
    if(dg<=1){ if(s->own[s->lab[i]]>=0) return 0; s->in[i]=1; s->own[s->lab[i]]=i; continue; }
    if(!old[i]) continue;
    int ok=1; for(int b=0;b<nlo[i];b++) if(!s->in[lo[i][b]]){ok=0;break;}
    if(ok && s->own[s->lab[i]]<0){ s->in[i]=1; s->own[s->lab[i]]=i; } }
  return 1;
}
typedef struct { ll f, Ct, hc; int k, nC, d, sg, cnt[8], cntA[8]; } Ev;
static int HCH=0;
static Ev eval(St *s){
  Ev v; static int w[MAXC]; static ll coef[MAXM]; int nC=0; memset(v.cnt,0,sizeof v.cnt); memset(v.cntA,0,sizeof v.cntA); v.k=0;
  for(int i=0;i<nc;i++) if(s->in[i]) nC++;
  int d=K+m-nC;
  for(int i=0;i<nc;i++){ if(!s->in[i]) continue; int mx=1; for(int a=0;a<K;a++){ int u=up[i][a]; if(u>=0 && s->in[u]){mx=0;break;} }
    v.cnt[deg[i]]++; if(mx){ w[i]=-(deg[i]-1); v.cntA[deg[i]]++; } else { w[i]=d+1; if(deg[i]==1) v.k++; } }
  for(int r=0;r<m;r++) coef[r]=0;
  ll C=0, S=0;
  for(int i=0;i<nc;i++) if(s->in[i]){ coef[s->lab[i]]=w[i]; C+=w[i]; }
  for(int r=0;r<m;r++) S+=coef[r]*r;
  ll mn=S; int sg=0; for(int g=0; g<m; g++){ if(S<mn){mn=S;sg=g;} S+=(ll)m*coef[g]-C; }
  v.f=mn; v.Ct=C; v.nC=nC; v.d=d; v.sg=sg; v.hc=mn;
  if(HCH){ /* HC'_H(sigma) = S(sigma) - m * #{maximal pairs e_a+e_b with r(e_a)+r(e_b)-r(0) >= m} */
    ll Sg=0; for(int r=0;r<m;r++) Sg+=coef[r]*r; ll best=1LL<<60;
    static int pa[MAXC], pb[MAXC]; int np=0;
    for(int i=0;i<nc;i++) if(s->in[i] && deg[i]==2 && w[i]<0){ int u0=-1,u1=-1; for(int a=0;a<K;a++){ if(ex[i][a]==2){u0=u1=a;} else if(ex[i][a]==1){ if(u0<0) u0=a; else u1=a; } } pa[np]=u0; pb[np]=u1; np++; }
    for(int g=0; g<m; g++){ int r0=(m-g)%m; int bp=0;
      for(int j=0;j<np;j++){ int ra=(s->P[pa[j]]-g+m)%m, rb=(s->P[pb[j]]-g+m)%m; if(ra+rb-r0>=m) bp++; }
      ll h=Sg-(ll)m*bp; if(h<best) best=h; Sg+=(ll)m*coef[g]-C; }
    v.hc=best; }
  return v;
}
static double obj(Ev *v){
  double avg=(double)v->Ct*(m-1)/2.0; ll ff=HCH? v->hc : v->f; double o=(OBJ==1? ff/((double)m*m) : (avg>0? ff/avg : 1e9));
  int s=m-v->nC; o+=1.0*((v->k<KMIN?KMIN-v->k:0)+(v->cnt[H]<TMIN?TMIN-v->cnt[H]:0)+(s>SMAX?s-SMAX:0));
  return o;
}
static int okc(Ev *v){ return v->k>=KMIN && v->cnt[H]>=TMIN && m-v->nC<=SMAX; }
static void dump(const char *tag, St *s, Ev *v){
  printf("%s K=%d H=%d m=%d f=%lld hc=%lld ratio=%.4f sigma=%d k=%d d=%d s=%d counts(deg:all/max)=",tag,K,H,m,v->f,v->hc,(v->Ct>0? v->f/((double)v->Ct*(m-1)/2.0):-1.0),v->sg,v->k,v->d,m-v->nC);
  for(int g=1; g<=H; g++) printf("%d:%d/%d%s",g,v->cnt[g],v->cntA[g],g<H?",":"");
  printf(" P=("); for(int a=0;a<K;a++) printf("%d%s",s->P[a],a<K-1?",":")");
  printf(" cells:"); for(int i=0;i<nc;i++) if(s->in[i] && deg[i]>=2){ printf(" "); for(int a=0;a<K;a++) printf("%d",ex[i][a]); }
  printf("\n"); fflush(stdout);
}
int main(int argc, char **argv){
  if(argc<7){ fprintf(stderr,"usage: anneal_hh K H m seed iters restarts\n"); return 1; }
  K=atoi(argv[1]); H=atoi(argv[2]); m=atoi(argv[3]); rs=strtoull(argv[4],0,10)*2654435761ULL+88172645463325252ULL; ll iters=atoll(argv[5]); int R=atoi(argv[6]);
  if(getenv("HCH")) HCH=atoi(getenv("HCH"));
  if(getenv("SMAX")) SMAX=atoi(getenv("SMAX")); if(getenv("OBJ")) OBJ=atoi(getenv("OBJ"));
  if(getenv("KMIN")) KMIN=atoi(getenv("KMIN")); if(getenv("TMIN")) TMIN=atoi(getenv("TMIN"));
  int init=getenv("INIT")?atoi(getenv("INIT")):0;
  if(K>MAXK || H>7 || K+1>m || m>=MAXM){ fprintf(stderr,"bad parameters\n"); return 1; }
  build(); if(nc>MAXC){ fprintf(stderr,"too many cells\n"); return 1; }
  static St cur, nx, best; Ev ec, en, eb; int have=0, nneg=0;
  for(int rep=0; rep<R; rep++){
    int Lmax=m-1; if(init==1){ Lmax=(m-1)/H+(int)(rnd()%3); if(Lmax<K) Lmax=K; if(Lmax>m-1) Lmax=m-1; }
    for(;;){ int ok=1; for(int a=0;a<K;a++){ cur.P[a]=1+rnd()%Lmax; for(int b=0;b<a;b++) if(cur.P[b]==cur.P[a]) ok=0; } if(ok) break; }
    relabel(&cur); static unsigned char full[MAXC]; double dens=urand();
    for(int i=0;i<nc;i++) full[i]=(deg[i]<=1)||(urand()<dens);
    rebuild(&cur, full); ec=eval(&cur); double oc=obj(&ec);
    double T0=0.05, T1=1e-4;
    for(ll it=0; it<iters; it++){
      double T=T0*pow(T1/T0,(double)it/iters);
      nx=cur; int mv=rnd()%10;
      if(mv<4){ int dg=2+(rnd()%(H-1)); int i=byDeg[dg][rnd()%nby[dg]];
        if(nx.in[i]) continue; int ok=1; for(int b=0;b<nlo[i];b++) if(!nx.in[lo[i][b]]){ok=0;break;}
        if(!ok || nx.own[nx.lab[i]]>=0) continue; nx.in[i]=1; nx.own[nx.lab[i]]=i; }
      else if(mv<8){ int dg=2+(rnd()%(H-1)); int i=byDeg[dg][rnd()%nby[dg]];
        if(!nx.in[i]) continue; int ok=1; for(int a=0;a<K;a++){ int u=up[i][a]; if(u>=0 && nx.in[u]){ok=0;break;} }
        if(!ok) continue; nx.in[i]=0; nx.own[nx.lab[i]]=-1; }
      else { int a=rnd()%K; int v=1+rnd()%(m-1); int ok=1; for(int b=0;b<K;b++) if(b!=a && nx.P[b]==v) ok=0; if(!ok) continue;
        static unsigned char old[MAXC]; memcpy(old,cur.in,sizeof old); nx.P[a]=v; relabel(&nx);
        for(int i=0;i<nc;i++) if(ex[i][a]>0 && deg[i]>=2 && urand()<0.5) old[i]=1;
        if(!rebuild(&nx, old)) continue; }
      en=eval(&nx); double on=obj(&en);
      if(on<=oc || urand()<exp((oc-on)/T)){ cur=nx; ec=en; oc=on;
        { ll fa=HCH?ec.hc:ec.f, fb=HCH?eb.hc:eb.f;
        if(okc(&ec) && (!have || (OBJ==1 ? fa<fb : fa*(double)eb.Ct < fb*(double)ec.Ct))){ eb=ec; best=cur; have=1; } }
        if(ec.f<0 && nneg<20){ nneg++; dump("NEGATIVE", &cur, &ec); }
        if(HCH && ec.hc<0 && nneg<40){ nneg++; dump("HC-NEGATIVE", &cur, &ec); } }
    }
  }
  if(have) dump("BEST", &best, &eb); else printf("BEST none K=%d H=%d m=%d\n",K,H,m);
  return 0;
}
