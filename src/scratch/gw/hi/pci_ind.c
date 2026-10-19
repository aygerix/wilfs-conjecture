/* (1) formal PCI: 0<=u<=beta*min(w,2q-1), M>=max((2i-2)q-1,u+Jw), any J>=1, beta>=0  (all u, not only worst)
   (2) residual R : same but delta=M-u-Jw < q
   (3) crude R': u<=beta*w', u+Jw >= (2i-3)q  ==> sum_j [F(u+jw)-F(jw)] <= J*beta
   usage: pci_ind imax qmax Jmax */
#include <stdio.h>
#include <stdlib.h>
static int I;
static long F(long t,long q){ if(t<0) return -1; long f=t/q; return f<I?f:I; }
int main(int argc,char**argv){
  int imax=atoi(argv[1]); long qmax=atol(argv[2]); int Jmax=atoi(argv[3]);
  for(I=3;I<=imax;I++){ long t1=0,f1=0,t3=0,f3=0;
   for(long q=1;q<=qmax;q++){ long T=(2*I-2)*q-1;
    for(long w=q+1;w<=(long)(2*I)*q+1;w++){ long wp=w<2*q-1?w:2*q-1;
     for(int beta=0;beta<I;beta++) for(int J=1;J<=Jmax;J++) for(long u=0;u<=beta*wp;u++){
       /* (1) all M from max(T,u+Jw) up to +q*2 beyond triviality */
       long Mlo=T>u+(long)J*w?T:u+(long)J*w;
       for(long M=Mlo; M<=Mlo+u+1; M++){ long d=M-u-(long)J*w;
         long L=0; for(int j=1;j<=J;j++) L+=F(u+j*w,q)-F(d+j*w,q);
         long R=(long)J*beta+F(d,q); t1++;
         if(L>R){ f1++; if(f1<=3) printf("PCI FAIL i=%d q=%ld w=%ld b=%d J=%d u=%ld M=%ld\n",I,q,w,beta,J,u,M);} }
       if(u+(long)J*w >= (2*I-3)*q){ long L=0; for(int j=1;j<=J;j++) L+=F(u+j*w,q)-F(j*w,q); t3++;
         if(L>(long)J*beta){ f3++; if(f3<=3) printf("R' FAIL i=%d q=%ld w=%ld b=%d J=%d u=%ld L=%ld\n",I,q,w,beta,J,u,L);} }
     }}}
   printf("i=%d PCI tests=%ld fails=%ld | R' tests=%ld fails=%ld\n",I,t1,f1,t3,f3); fflush(stdout);}
  return 0;}
