/* PCI*: worst-case base u* = min(beta*min(w,2q-1), M-Jw) (monotonicity in u).
   usage: pcistar imax qmax [thr_offset]   thr = (2i-2)q - 1 + thr_offset */
#include <stdio.h>
#include <stdlib.h>
static int I;
static long F(long t, long q){ long f=t/q; return f<I?f:I; }
int main(int argc,char**argv){
  int imax=atoi(argv[1]); long qmax=atol(argv[2]); long off=argc>3?atol(argv[3]):0;
  long tests=0,fails=0,tight=0;
  for(I=3;I<=imax;I++){ long ft=0,ff=0,fti=0;
   for(long q=1;q<=qmax;q++){ long thr=(2*I-2)*q-1+off;
    for(long w=q+1;w<=(long)(2*I)*q+1;w++){ long wp=w<2*q-1?w:2*q-1;
     for(int beta=1;beta<I;beta++) for(int J=1;J<I;J++){
      long Mlo=thr; if(beta*q+(long)J*w>Mlo) Mlo=beta*q+(long)J*w;
      long Mhi=2*beta*wp+(long)J*w+ (long)(2*I+2)*q;
      for(long M=Mlo;M<=Mhi;M++){
        long u=beta*wp; if(M-(long)J*w<u) u=M-(long)J*w;
        if(u<beta*q) continue;
        long d=M-u-(long)J*w;
        long L=0; for(int j=1;j<=J;j++) L+=F(u+j*w,q)-F(d+j*w,q);
        long R=(long)J*beta+F(d,q);
        ft++; if(L>R){ ff++; if(ff<=5) printf("FAIL i=%d q=%ld w=%ld beta=%d J=%d M=%ld u=%ld d=%ld L=%ld R=%ld\n",I,q,w,beta,J,M,u,d,L,R);}
        else if(L==R){ fti++; if(getenv("SHOWT")&&fti<=8) printf("TIGHT i=%d q=%ld w=%ld beta=%d J=%d M=%ld u=%ld d=%ld L=%ld\n",I,q,w,beta,J,M,u,d,L);}
      }}}}
   printf("i=%d tests=%ld fails=%ld tight=%ld\n",I,ft,ff,fti); fflush(stdout);
   tests+=ft; fails+=ff; tight+=fti; }
  printf("TOTAL tests=%ld fails=%ld tight=%ld\n",tests,fails,tight); return 0; }
