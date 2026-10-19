/* Heavy-fiber experiment for the uniform-alpha packing question (NOTEBOOK 2026-10-19 night).
   B = n integers in [0,s) with all pair sums (loops included) distinct.  Fibers = classes of formal triples
   (multisets) with equal ordinary sum; g = class size; excess ex = sum (g-1).
   Exact signed-label count: NS = #distinct values among {p+q-r : p<=q, r not in {p,q}} U B  (all in (-s,2s)).
   SP says 3s-2 >= NS >= H(n) - loss.  Heavy loss HL = sum_{g>=4} [9C(g,2) - 13.5(g-1)].
   Simulated annealing maximizes  score = (H(n) - NS) - 13.5*ex  (signed loss beyond what D3=3ex covers via delta <= B-D3, s=1.5 delta),
   i.e. looks for sets where collisions destroy more signed labels than the arcs' D3 payment covers.
   usage: fiber_search seed n s iters */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static int n,s,MODE; static int B[64];
static int pairok(void){ static unsigned char u[16384]; memset(u,0,2*s); for(int i=0;i<n;i++) for(int j=i;j<n;j++){ int v=B[i]+B[j]; if(u[v]) return 0; u[v]=1; } return 1; }
static long eval(long *ex_o,long *ns_o,int *gmax_o,long *hl_o){
  static int cnt[24576]; memset(cnt,0,sizeof(int)*3*s);
  for(int i=0;i<n;i++) for(int j=i;j<n;j++) for(int k=j;k<n;k++) cnt[B[i]+B[j]+B[k]]++;
  long ex=0,hl=0; int gmax=0; for(int v=0;v<3*s;v++) if(cnt[v]){ ex+=cnt[v]-1; if(cnt[v]>gmax) gmax=cnt[v]; if(cnt[v]>=4) hl+=9L*cnt[v]*(cnt[v]-1)/2*2-27L*(cnt[v]-1); }
  static unsigned char u[3*24576]; memset(u,0,3*s+2); long ns=0; int off=s;
  for(int r=0;r<n;r++) for(int i=0;i<n;i++) for(int j=i;j<n;j++){ if(i==r||j==r) continue; int v=B[i]+B[j]-B[r]+off; if(!u[v]){u[v]=1;ns++;} }
  for(int i=0;i<n;i++){ int v=B[i]+off; if(!u[v]){u[v]=1;ns++;} }
  *ex_o=ex; *ns_o=ns; *gmax_o=gmax; *hl_o=hl; /* hl doubled */
  long H=(long)n*((long)n*(n-1)/2+1);
  if(MODE==1) return -2*ex;  /* mode 1: minimize the excess at fixed s (tests LSP-13.5) */
  return 2*(H-ns)-27*ex;   /* doubled score: signed loss beyond the 13.5 per unit excess that D3 covers */ }
int main(int argc,char**argv){ st=strtoull(argv[1],0,10)*2654435761ULL+99; n=atoi(argv[2]); s=atoi(argv[3]); long iters=atol(argv[4]); MODE=argc>5?atoi(argv[5]):0;
  /* random Sidon start */
  int tries=0; do{ for(int i=0;i<n;i++) B[i]=rnd()%s; B[0]=0; tries++; int dup=0; for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(B[i]==B[j]) dup=1; if(!dup&&pairok()) break; }while(tries<1000000);
  if(tries>=1000000){ printf("no Sidon start\n"); return 0; }
  long ex,ns,hl; int gm; long cur=eval(&ex,&ns,&gm,&hl), best=cur; static int bestB[64]; memcpy(bestB,B,sizeof B); long bex=ex,bns=ns,bhl=hl; int bgm=gm;
  double T=20.0;
  for(long it=0;it<iters;it++){ int i=1+rnd()%(n-1); int old=B[i]; int nv=rnd()%s; int dup=0; for(int j=0;j<n;j++) if(B[j]==nv) dup=1; if(dup) continue; B[i]=nv;
    if(!pairok()){ B[i]=old; continue; }
    long e2,n2,h2; int g2; long sc=eval(&e2,&n2,&g2,&h2);
    double acc = sc>=cur ? 1.0 : __builtin_exp((sc-cur)/T);
    if((double)(rnd()%1000000)/1e6 < acc){ cur=sc; if(sc>best){ best=sc; memcpy(bestB,B,sizeof B); bex=e2; bns=n2; bhl=h2; bgm=g2; } } else B[i]=old;
    T*=0.99995; if(T<0.05) T=0.05; }
  long H=(long)n*((long)n*(n-1)/2+1);
  printf("n=%d s=%d H=%ld 3s-2=%d  best: NS=%ld ex=%ld gmax=%d heavyloss=%.1f  score(H-NS-13.5ex)=%.1f  set:",n,s,H,3*s-2,bns,bex,bgm,bhl/2.0,best/2.0);
  for(int i=0;i<n;i++) printf(" %d",bestB[i]);
  { long lam2 = n<=1?0: n==2?2: n==3?4: n==4?8: (n%3==0? 3L*n : 3L*(n-1));
    printf("\n   LSP slack (lambda_n): %.1f   LSP-13.5 slack: %.1f   count slack (C(n+2,3)-ex <= 3s-2): %ld\n",
      (2.0*(3*s-2)-(2.0*H-lam2*bex))/2.0, (3*s-2)-(H-13.5*bex), (long)(3*s-2)-((long)n*(n+1)*(n+2)/6-bex)); }
  return 0; }
