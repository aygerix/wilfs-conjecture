/* Stress test of conjecture LSP* (3s-2 >= H(n) - 13.5*ex) on sets with a planted heavy fiber.
   B = t triples {x_i, y_i, sigma - x_i - y_i} (one common sum, disjoint) plus f free elements, n = 3t+f, all in [0,s),
   all pair sums (loops included) distinct.  Annealing minimizes ex (triple-collision excess) at fixed s.
   Reports the LSP* slack (3s-2) - (H - 13.5 ex), the LSP slack with lambda_n, and NS (exact signed count).
   usage: planted_fiber seed t f s iters */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static int t,f,n,s,sig; static int X[32],Y[32],F[32],B[96];
static int build(void){ n=0; for(int i=0;i<t;i++){ int z=sig-X[i]-Y[i]; if(z<0||z>=s) return 0; B[n++]=X[i]; B[n++]=Y[i]; B[n++]=z; } for(int i=0;i<f;i++) B[n++]=F[i];
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(B[i]==B[j]) return 0;
  static unsigned char u[65536]; memset(u,0,2*s); for(int i=0;i<n;i++) for(int j=i;j<n;j++){ int v=B[i]+B[j]; if(u[v]) return 0; u[v]=1; } return 1; }
static long excess(void){ static int cnt[100000]; memset(cnt,0,sizeof(int)*3*s); long ex=0;
  for(int i=0;i<n;i++) for(int j=i;j<n;j++) for(int k=j;k<n;k++){ int v=B[i]+B[j]+B[k]; if(cnt[v]++) ex++; } return ex; }
static long signedcount(void){ static unsigned char u[100000]; memset(u,0,3*s+2); long ns=0;
  for(int r=0;r<n;r++) for(int i=0;i<n;i++) for(int j=i;j<n;j++){ if(i==r||j==r) continue; int v=B[i]+B[j]-B[r]+s; if(!u[v]){u[v]=1;ns++;} }
  for(int i=0;i<n;i++){ int v=B[i]+s; if(!u[v]){u[v]=1;ns++;} } return ns; }
int main(int argc,char**argv){ st=strtoull(argv[1],0,10)*2654435761ULL+5; t=atoi(argv[2]); f=atoi(argv[3]); s=atoi(argv[4]); long iters=atol(argv[5]);
  int ok=0; for(long tr=0;tr<5000000&&!ok;tr++){ sig=s+rnd()%s; for(int i=0;i<t;i++){ X[i]=rnd()%s; Y[i]=rnd()%s; } for(int i=0;i<f;i++) F[i]=rnd()%s; ok=build(); }
  if(!ok){ printf("t=%d f=%d s=%d: no start\n",t,f,s); return 0; }
  long cur=excess(), best=cur; static int bX[32],bY[32],bF[32]; int bsig=sig; memcpy(bX,X,sizeof X); memcpy(bY,Y,sizeof Y); memcpy(bF,F,sizeof F);
  double T=3.0;
  for(long it=0;it<iters;it++){ int ox=0,oy=0,of=0,osig=sig,which=rnd()%(2*t+f+1),i=0;
    if(which<t){ i=which; ox=X[i]; X[i]=rnd()%s; } else if(which<2*t){ i=which-t; oy=Y[i]; Y[i]=rnd()%s; } else if(which<2*t+f){ i=which-2*t; of=F[i]; F[i]=rnd()%s; } else sig=s+rnd()%s;
    int good=build(); long e2= good? excess() : 1L<<40;
    double acc = e2<=cur ? 1.0 : exp(-(double)(e2-cur)/T);
    if(good && (double)(rnd()%1000000)/1e6 < acc){ cur=e2; if(e2<best){ best=e2; bsig=sig; memcpy(bX,X,sizeof X); memcpy(bY,Y,sizeof Y); memcpy(bF,F,sizeof F); } }
    else { if(which<t) X[i]=ox; else if(which<2*t) Y[i]=oy; else if(which<2*t+f) F[i]=of; else sig=osig; build(); }
    T*=0.99997; if(T<0.05) T=0.05; }
  sig=bsig; memcpy(X,bX,sizeof X); memcpy(Y,bY,sizeof Y); memcpy(F,bF,sizeof F); build();
  long ex=excess(), ns=signedcount(); long H=(long)n*((long)n*(n-1)/2+1);
  long lam2 = n<=4? (long[]){0,0,2,4,8}[n] : (n%3==0? 3L*n : 3L*(n-1));
  printf("t=%d f=%d n=%d s=%d H=%ld 3s-2=%d  ex=%ld NS=%ld (H-NS=%ld)  LSP*slack=%.1f  LSPslack=%.1f\n",t,f,n,s,H,3*s-2,ex,ns,H-ns,(3*s-2)-(H-13.5*ex),((2.0*(3*s-2))-(2.0*H-lam2*ex))/2);
  return 0; }
