/* P18 depth four: test the split of Wilf (*) into M3': 3*tau3 <= e(1+e+tau2) and M4': 4*n4 <= (e-1)*x.
   S = <m, m+B>, B subset [1,m-1], gcd(m,B)=1. Exhaustive over |B| = k for m in [mlo,mhi].
   tau_j = #{r : w_r <= j*m + r}, n4 = m - tau3, h = c - 3m, x = #{r < h : r in T_3}.
   (*): e(1+e+tau2) + (e-1)x >= 3 tau3 + 4 n4  <=> Wilf.  usage: ./p18split mlo mhi k */
#include <stdio.h>
#include <stdlib.h>
static int m, k, B[16], w[4096];
static long cnt, d4, failM3, failM4, failW, failBoth;
static long minM3 = 1L<<40, minM4 = 1L<<40;
static int gcd(int a, int b){ while(b){int t=a%b;a=b;b=t;} return a; }
static void eval(void){
  int g = m; for(int i=0;i<k;i++) g = gcd(g, B[i]); if(g!=1) return;
  for(int r=0;r<m;r++) w[r] = 1<<29; w[0]=0;
  /* Dijkstra-free: Bellman-style relaxation over generators m+b (all < 2m), iterate until stable */
  int changed=1;
  while(changed){ changed=0;
    for(int r=0;r<m;r++){ if(w[r]>=(1<<29)) continue;
      for(int i=0;i<k;i++){ int v=w[r]+m+B[i]; int rr=v%m; if(v<w[rr]){w[rr]=v;changed=1;} } } }
  int M=0; for(int r=0;r<m;r++) if(w[r]>M) M=w[r];
  int c = M - m + 1; cnt++;
  if(!(c > 3*m && c <= 4*m)) return;
  d4++;
  int h = c - 3*m, e = k+1;
  long tau2=0, tau3=0, x=0, ell=0;
  for(int r=0;r<m;r++){
    if(w[r] <= 2*m + r) tau2++;
    if(w[r] <= 3*m + r){ tau3++; if(r<h) x++; }
    ell += (M - w[r]) / m;
  }
  long n4 = m - tau3;
  long W = (long)e*ell - c;
  long sW = (long)e*(1+e+tau2) + (long)(e-1)*x - 3*tau3 - 4*n4;
  if(sW != W){ printf("IDENTITY FAIL m=%d\n", m); exit(1); }
  long s3 = (long)e*(1+e+tau2) - 3*tau3, s4 = (long)(e-1)*x - 4*n4;
  if(s3<0) failM3++; if(s4<0) failM4++; if(s3<0&&s4<0) failBoth++; if(W<0) failW++;
  if(s3 < minM3){ minM3=s3; printf("minM3 %ld m=%d k=%d h=%d tau2=%ld tau3=%ld x=%ld n4=%ld W=%ld B=",s3,m,k,h,tau2,tau3,x,n4,W); for(int i=0;i<k;i++) printf("%d ",B[i]); printf("\n"); }
  if(s4 < minM4){ minM4=s4; printf("minM4 %ld m=%d k=%d h=%d tau2=%ld tau3=%ld x=%ld n4=%ld W=%ld B=",s4,m,k,h,tau2,tau3,x,n4,W); for(int i=0;i<k;i++) printf("%d ",B[i]); printf("\n"); }
}
static void rec(int pos, int start){
  if(pos==k){ eval(); return; }
  for(int b=start;b<m;b++){ B[pos]=b; rec(pos+1,b+1); }
}
int main(int argc, char**argv){
  int mlo=atoi(argv[1]), mhi=atoi(argv[2]); k=atoi(argv[3]);
  for(m=mlo;m<=mhi;m++) rec(0,1);
  printf("DONE k=%d m=%d..%d: S=%ld depth4=%ld failM3=%ld failM4=%ld both=%ld failW=%ld minM3=%ld minM4=%ld\n",k,mlo,mhi,cnt,d4,failM3,failM4,failBoth,failW,minM3,minM4);
}
