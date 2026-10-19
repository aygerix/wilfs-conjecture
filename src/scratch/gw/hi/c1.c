/* C1 (residual delta<q): beta*w' + J*w + delta >= (2i-2)q-1  ==>  sum_{s=1}^{min(beta,J)} D(delta+s*w) <= J*beta
   also C1full: for all delta (not only <q): sum_{s<=min(beta,J)} D(delta+sw) <= J*beta + F(delta)
   D(t)=max(0,i-floor(t/q)).  usage: c1 imax qmax */
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char**argv){ int imax=atoi(argv[1]); long qmax=atol(argv[2]);
 for(int i=3;i<=imax;i++){ long t=0,f=0,tf=0,ff=0;
  for(long q=1;q<=qmax;q++){ long T=(2*i-2)*q-1;
   for(long w=q+1;w<=(long)(2*i)*q+1;w++){ long wp=w<2*q-1?w:2*q-1;
    for(int b=1;b<i;b++) for(int J=1;J<i;J++){ int p=b<J?b:J;
     for(long d=0; d<(long)i*q; d++){
      if(b*wp+(long)J*w+d < T) continue;
      long L=0; for(int s=1;s<=p;s++){ long k=(d+s*w)/q; if(k<i) L+=i-k; }
      long Fd=d/q<i?d/q:i;
      if(d<q){ t++; if(L>(long)J*b){ f++; if(f<=4) printf("C1 FAIL i=%d q=%ld w=%ld b=%d J=%d d=%ld L=%ld\n",i,q,w,b,J,d,L);} }
      tf++; if(L>(long)J*b+Fd){ ff++; if(ff<=4) printf("C1full FAIL i=%d q=%ld w=%ld b=%d J=%d d=%ld L=%ld R=%ld\n",i,q,w,b,J,d,L,(long)J*b+Fd);} }}}}
  printf("i=%d C1(d<q) tests=%ld fails=%ld | C1full tests=%ld fails=%ld\n",i,t,f,tf,ff); fflush(stdout);}
 return 0;}
