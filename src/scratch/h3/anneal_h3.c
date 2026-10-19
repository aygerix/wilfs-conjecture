/* Adversarial annealer for height-<=3 MaxCL (lead, 2026-10-19).
   State: unit labels P[0..K-1] (distinct, nonzero mod m) and a down-set C of monomials of degree <= 3 in K variables
   containing 0 and every unit, with x -> x.P mod m injective on C.  Missing residues are spikes (weight 0).
   Units without a pair in C are maximal (weight 0, i.e. spikes).  d = K + m - |C| (all directions).
   Slack S(sigma) = sum_C w(x) ((phi(x)-sigma) mod m), w = d+1 on non-maximal cells, -(|x|-1) on maximal cells.
   Objective f = min_sigma S(sigma) (exact).  mode 0: minimize f.  mode 1: minimize f + LAM*(max(0,CR)+max(0,FLAT))
   + penalties pushing to the unproved family (core dimension k >= 5, d >= 6, t >= 1), CR/FLAT as in P6B_REPORT.
   Reports the best f overall and the best f among "unpaid" states (CR < 0, FLAT-CR < 0, k >= 5, d >= 6, t >= 1).
   usage: anneal_h3 K m seed iters restarts mode  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef long long ll;
#define MAXC 400
#define MAXM 1024
static int K, m, nc, ex[MAXC][12], deg[MAXC], up[MAXC][12], lo[MAXC][12], nlo[MAXC], byDeg[4][MAXC], nby[4];
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline double urand(void){ return (rnd()>>11)*(1.0/9007199254740992.0); }
typedef struct { int P[12]; unsigned char in[MAXC]; int own[MAXM]; int lab[MAXC]; } St;
static int find(int *e){ for(int i=0;i<nc;i++){ int ok=1; for(int a=0;a<K;a++) if(ex[i][a]!=e[a]){ok=0;break;} if(ok) return i; } return -1; }
static void build(void){
  nc=0; int e[12];
  for(int dg=0; dg<=3; dg++){
    /* enumerate monomials of degree dg */
    int idx[3];
    if(dg==0){ memset(ex[nc],0,sizeof ex[nc]); deg[nc]=0; byDeg[0][nby[0]++]=nc; nc++; continue; }
    for(idx[0]=0; idx[0]<K; idx[0]++) for(idx[1]=(dg>1?idx[0]:0); idx[1]<(dg>1?K:1); idx[1]++) for(idx[2]=(dg>2?idx[1]:0); idx[2]<(dg>2?K:1); idx[2]++){
      memset(e,0,sizeof e); for(int j=0;j<dg;j++) e[idx[j]]++;
      memcpy(ex[nc],e,sizeof e); deg[nc]=dg; byDeg[dg][nby[dg]++]=nc; nc++; }
  }
  for(int i=0;i<nc;i++){ nlo[i]=0;
    for(int a=0;a<K;a++){ memcpy(e,ex[i],sizeof e); e[a]++; up[i][a]=(deg[i]<3)?find(e):-1;
      if(ex[i][a]>0){ memcpy(e,ex[i],sizeof e); e[a]--; lo[i][nlo[i]++]=find(e); } } }
}
static void relabel(St *s){ for(int i=0;i<nc;i++){ ll L=0; for(int a=0;a<K;a++) L+=(ll)ex[i][a]*s->P[a]; s->lab[i]=(int)(L%m); } }
/* rebuild C after a label change: keep old cells in degree order when lower covers kept and label free */
static int rebuild(St *s, const unsigned char *old){
  for(int r=0;r<m;r++) s->own[r]=-1; memset(s->in,0,sizeof s->in);
  for(int dg=0; dg<=3; dg++) for(int j=0;j<nby[dg];j++){ int i=byDeg[dg][j];
    if(dg<=1){ if(s->own[s->lab[i]]>=0) return 0; s->in[i]=1; s->own[s->lab[i]]=i; continue; }
    if(!old[i]) continue; int ok=1; for(int b=0;b<nlo[i];b++) if(!s->in[lo[i][b]]){ok=0;break;}
    if(ok && s->own[s->lab[i]]<0){ s->in[i]=1; s->own[s->lab[i]]=i; } }
  return 1;
}
typedef struct { ll f, CR, FL, Ct, hc; int k, q, p, t, s, d, nC, unpaid; int sg, hsg; } Ev;
static int TMIN=1, TMAX=1000, DOHC=0, B2=-1;
static Ev eval(St *s){
  Ev v; int nC=0, kk=0, q=0, p=0, t=0, maxu=0; static int w[MAXC]; static ll coef[MAXM];
  for(int i=0;i<nc;i++) if(s->in[i]) nC++;
  int d=K+m-nC;
  for(int i=0;i<nc;i++){ if(!s->in[i]) continue; int mx=1; for(int a=0;a<K;a++){ int u=up[i][a]; if(u>=0 && s->in[u]){mx=0;break;} }
    if(mx){ w[i]=-(deg[i]-1); if(deg[i]==1) maxu++; if(deg[i]==2) q++; if(deg[i]==3) t++; }
    else { w[i]=d+1; if(deg[i]==1) kk++; if(deg[i]==2){ q++; p++; } } }
  if(B2>=0){ int sc=m-(nC-maxu); for(int i=0;i<nc;i++) if(s->in[i]) w[i]=(w[i]>0)? 2*kk+2+B2*sc : 2*w[i]; }
  for(int r=0;r<m;r++) coef[r]=0; ll C=0, S=0;
  for(int i=0;i<nc;i++) if(s->in[i]){ coef[s->lab[i]]=w[i]; C+=w[i]; }
  for(int r=0;r<m;r++) S+=coef[r]*r;
  ll mn=S; int sg=0; for(int g=0; g<m; g++){ if(S<mn){mn=S;sg=g;} S+=(ll)m*coef[g]-C; }
  int core=1+kk+q+t, ss=m-core, a=q-p; ll J=(ll)(1+kk+p)*(kk+p)/2, B=a+2*t;
  v.CR=(ll)(m-q-t)*J-B*(m-1)+(ll)t*(t-1)+(ll)a*t+(ll)a*(a-1)/2;
  v.FL=(ll)ss*kk*(kk-1)/2+(ll)(kk+ss+2)*p*(p-1)/2-3LL*t*(m-1)+(ll)t*(t-1);
  v.f=mn; v.Ct=C; v.k=kk; v.q=q; v.p=p; v.t=t; v.s=ss; v.d=d; v.nC=nC; v.sg=sg;
  v.unpaid=(v.CR<0 && v.FL<0 && kk>=5 && d>=6 && t>=1);
  v.hc=0; v.hsg=-1;
  if(DOHC){ /* HC' = sum_{nonmax units}(d+1-adeg a) rho_a + (d+1) sum_N2 r - 2 sum_T r - (p+t) rho_0 + m*O_W,
               O_W = #residues in [m-rho_0, m) minus #maximal pairs with rho_a+rho_b < rho_0  (all residues: spikes included) */
    static int adeg[12], isN[MAXC]; for(int a=0;a<K;a++) adeg[a]=0;
    for(int i=0;i<nc;i++){ isN[i]=0; if(!s->in[i]) continue; isN[i]=(w[i]>0); if(deg[i]==2 && !isN[i]) for(int a=0;a<K;a++) adeg[a]+=ex[i][a]; }
    ll best=1LL<<60; int bs=0;
    for(int g=0; g<m; g++){ int r0=(m-g)%m; ll h=0; int bm=0;
      for(int i=0;i<nc;i++){ if(!s->in[i]) continue; int r=(s->lab[i]-g+m)%m;
        if(deg[i]==1 && isN[i]){ int a=0; while(!ex[i][a]) a++; h+=(ll)(d+1-adeg[a])*r; }
        else if(deg[i]==2 && isN[i]) h+=(ll)(d+1)*r;
        else if(deg[i]==3) h-=2LL*r;
        else if(deg[i]==2 && !isN[i]){ int u0=-1,u1=-1; for(int a=0;a<K;a++){ if(ex[i][a]==2){u0=u1=a;} else if(ex[i][a]==1){ if(u0<0) u0=a; else u1=a; } }
          int ra=(s->P[u0]-g+m)%m, rb=(s->P[u1]-g+m)%m; if(ra+rb<r0) bm++; } }
      h-=(ll)(p+t)*r0; h+=(ll)m*(r0-bm);
      if(h<best){best=h;bs=g;} }
    v.hc=best; v.hsg=bs; }
  return v;
}
static double obj(Ev *v, int mode){
  if(mode==0) return (double)v->f;
  if(mode==4){ double avg=(double)v->Ct*(m-1)/2.0; double o=(avg>0? v->hc/avg : 1e9);
    o+=1.0*((v->k<3?3-v->k:0)+(v->t<TMIN?TMIN-v->t:0)+(v->t>TMAX?v->t-TMAX:0)); return o; }
  if(mode==3){ double avg=(double)v->Ct*(m-1)/2.0; double o=(avg>0? v->f/avg : 1e9);
    o+=0.001*(((v->CR>0?v->CR:0)+(v->FL>0?v->FL:0))/(double)(m*m));
    o+=1.0*((v->k<5?5-v->k:0)+(v->d<6?6-v->d:0)+(v->t<TMIN?TMIN-v->t:0));
    return o; }
  double o=(double)v->f; double lam=0.05;
  o+=lam*((v->CR>0?v->CR:0)+(v->FL>0?v->FL:0));
  o+=(double)m*m*((v->k<5?5-v->k:0)+(v->d<6?6-v->d:0)+(v->t<TMIN?TMIN-v->t:0));
  return o;
}
static void dump(const char *tag, St *s, Ev *v){
  printf("%s K=%d m=%d f=%lld HC=%lld(hs=%d) ratio=%.4f sigma=%d k=%d q=%d p=%d t=%d s=%d d=%d CR=%lld FLAT=%lld P=(",tag,K,m,v->f,v->hc,v->hsg,(v->Ct>0? v->f/((double)v->Ct*(m-1)/2.0):-1.0),v->sg,v->k,v->q,v->p,v->t,v->s,v->d,v->CR,v->FL);
  for(int a=0;a<K;a++) printf("%d%s",s->P[a],a<K-1?",":")");
  printf(" cells:"); for(int i=0;i<nc;i++) if(s->in[i] && deg[i]>=2){ printf(" "); for(int a=0;a<K;a++) printf("%d",ex[i][a]); }
  printf("\n"); fflush(stdout);
}
int main(int argc, char **argv){
  if(argc<7){ fprintf(stderr,"usage: anneal_h3 K m seed iters restarts mode\n"); return 1; }
  K=atoi(argv[1]); m=atoi(argv[2]); rs=strtoull(argv[3],0,10)*2654435761ULL+88172645463325252ULL; ll iters=atoll(argv[4]); int R=atoi(argv[5]), mode=atoi(argv[6]);
  if(K+1>m || m>=MAXM){ fprintf(stderr,"bad m\n"); return 1; }
  build(); if(getenv("B2")) B2=atoi(getenv("B2")); if(getenv("TMIN")) TMIN=atoi(getenv("TMIN")); if(getenv("TMAX")) TMAX=atoi(getenv("TMAX")); if(mode==4 || getenv("DOHC")) DOHC=1;
  static St cur, nx, best, bestU; Ev ec, en, eb, ebU; int haveU=0, nneg=0;
  if(mode==2){ /* evaluate one given state: argv[7..6+K] = P, then cell exponent strings of degree >= 2 */
    for(int a=0;a<K;a++) cur.P[a]=atoi(argv[7+a]); relabel(&cur); unsigned char f2[MAXC]; memset(f2,0,sizeof f2);
    for(int i=0;i<nc;i++) if(deg[i]<=1) f2[i]=1;
    for(int j=7+K;j<argc;j++){ int e[12]; for(int a=0;a<K;a++) e[a]=argv[j][a]-'0'; int i=find(e); if(i<0){fprintf(stderr,"bad cell\n");return 1;} f2[i]=1; }
    if(!rebuild(&cur,f2)){ printf("units collide\n"); return 1; }
    int nin=0; for(int i=0;i<nc;i++) nin+=cur.in[i]; printf("kept %d cells of %d requested\n",nin,(int)(argc-7-K)+1+K);
    ec=eval(&cur); dump("EVAL",&cur,&ec); return 0; } eb.f=1LL<<60; ebU.f=1LL<<60;
  for(int rep=0; rep<R; rep++){
    /* random distinct nonzero unit labels */
    /* INIT=1: postage-stamp start, unit labels in [1,L] with L ~ (m-1)/3 (labels of degree-j cells in [j, jL]) */
    int Lmax = m-1; if(getenv("INIT") && atoi(getenv("INIT"))==1){ Lmax=(m-1)/3 + (int)(rnd()%3); if(Lmax<K) Lmax=K; if(Lmax>m-1) Lmax=m-1; }
    int clus=(getenv("INIT") && atoi(getenv("INIT"))==2);
    for(;;){ int ok=1; for(int a=0;a<K;a++){ if(clus && a<(K+1)/2){ int Lc=m/12; if(Lc<(K+1)/2+2) Lc=(K+1)/2+2; cur.P[a]=(m/2+1+rnd()%Lc)%m; if(cur.P[a]==0) cur.P[a]=1; } else cur.P[a]=1+rnd()%Lmax; for(int b=0;b<a;b++) if(cur.P[b]==cur.P[a]) ok=0; } if(ok) break; }
    relabel(&cur); unsigned char full[MAXC]; memset(full,0,sizeof full);
    /* random initial density */
    double dens=urand(); for(int i=0;i<nc;i++) full[i]=(deg[i]<=1)||(urand()<dens);
    rebuild(&cur, full); ec=eval(&cur); double oc=obj(&ec,mode);
    double T0=(mode==3?0.05:0.05*(double)m*m), T1=(mode==3?1e-4:0.3);
    for(ll it=0; it<iters; it++){
      double T=T0*pow(T1/T0,(double)it/iters);
      nx=cur; int mv=rnd()%10;
      if(mv<4){ /* add */ int dg=2+(rnd()%2); int i=byDeg[dg][rnd()%nby[dg]];
        if(nx.in[i]) continue; int ok=1; for(int b=0;b<nlo[i];b++) if(!nx.in[lo[i][b]]){ok=0;break;}
        if(!ok || nx.own[nx.lab[i]]>=0) continue; nx.in[i]=1; nx.own[nx.lab[i]]=i; }
      else if(mv<8){ /* remove a maximal cell of degree >= 2 */ int dg=2+(rnd()%2); int i=byDeg[dg][rnd()%nby[dg]];
        if(!nx.in[i]) continue; int ok=1; for(int a=0;a<K;a++){ int u=up[i][a]; if(u>=0 && nx.in[u]){ok=0;break;} }
        if(!ok) continue; nx.in[i]=0; nx.own[nx.lab[i]]=-1; }
      else { /* change one unit label, keep surviving cells, then greedy refill attempts */
        int a=rnd()%K; int v=1+rnd()%(m-1); int ok=1; for(int b=0;b<K;b++) if(b!=a && nx.P[b]==v) ok=0; if(!ok) continue;
        unsigned char old[MAXC]; memcpy(old,cur.in,sizeof old); nx.P[a]=v; relabel(&nx);
        /* cells containing direction a are re-admitted greedily too */
        for(int i=0;i<nc;i++) if(ex[i][a]>0 && deg[i]>=2 && urand()<0.5) old[i]=1;
        if(!rebuild(&nx, old)) continue; }
      en=eval(&nx); double on=obj(&en,mode);
      if(on<=oc || urand()<exp((oc-on)/T)){ cur=nx; ec=en; oc=on;
        if(ec.f<eb.f){ eb=ec; best=cur; }
        if(mode!=4 && ec.unpaid && ec.t>=TMIN && (mode==3 ? (!haveU || ec.f*(double)ebU.Ct < ebU.f*(double)ec.Ct) : ec.f<ebU.f)){ ebU=ec; bestU=cur; haveU=1; }
        if(ec.f<0 && nneg<20){ nneg++; dump("NEGATIVE", &cur, &ec); }
        if(DOHC && ec.hc<0 && nneg<40){ nneg++; dump("HC-NEGATIVE", &cur, &ec); }
        if(mode==4 && (!haveU || ec.hc*(double)ebU.Ct < ebU.hc*(double)ec.Ct) && ec.k>=3 && ec.t>=TMIN && ec.t<=TMAX){ ebU=ec; bestU=cur; haveU=1; } }
    }
  }
  dump("BEST", &best, &eb);
  if(haveU) dump("BEST-UNPAID", &bestU, &ebU); else printf("BEST-UNPAID none K=%d m=%d\n",K,m);
  return 0;
}
