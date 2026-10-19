/* w>=2q: test row-pairing bounds over formal instances 0<=u<=beta*(2q-1), M>=max(T,u+Jw)
   P1: term_j + term_{J+1-j} <= 2beta (+ [j==J+1-j] adj)   P2: per-k c_k<=beta and sum trivial? 
   also verify trapezoid-proof claim for w<2q: sum_k c_k <= J*beta (no F(delta))  usage: wbig imax qmax */
#include <stdio.h>
#include <stdlib.h>
static int I;
static long F(long t,long q){ long f=t/q; return f<I?f:I; }
int main(int argc,char**argv){ int imax=atoi(argv[1]); long qmax=atol(argv[2]);
 for(I=3;I<=imax;I++){ long tp=0,fp=0,tw=0,fw=0,tq=0,fq=0;
  for(long q=1;q<=qmax;q++){ long T=(2*I-2)*q-1;
   for(long w=q+1;w<=(long)(2*I+2)*q;w++){ long wp=w<2*q-1?w:2*q-1;
    for(int b=1;b<I;b++) for(int J=1;J<=I+1;J++) for(long u=0;u<=b*wp;u++){
     long Mlo=T>u+(long)J*w?T:u+(long)J*w;
     for(long M=Mlo;M<=Mlo+u+1;M++){ long d=M-u-(long)J*w; if(d>=u) break;
      long tm[64]; long S=0; for(int j=1;j<=J;j++){ tm[j]=F(u+j*w,q)-F(d+j*w,q); S+=tm[j]; }
      if(w<2*q){ tw++; if(S>(long)J*b){ fw++; if(fw<=3) printf("TRAP FAIL i=%d q=%ld w=%ld b=%d J=%d u=%ld d=%ld S=%ld\n",I,q,w,b,J,u,d,S);} }
      else { tp++; int bad=0; for(int j=1;j<=J;j++){ int jj=J+1-j; long lim=(j==jj)?b:2*b; long val=(j==jj)?tm[j]:tm[j]+tm[jj]; if(val>lim) bad=1; }
        if(bad){ fp++; if(fp<=3){ printf("PAIR FAIL i=%d q=%ld w=%ld b=%d J=%d u=%ld d=%ld terms:",I,q,w,b,J,u,d); for(int j=1;j<=J;j++) printf(" %ld",tm[j]); printf("\n");} }
        tq++; if(S>(long)J*b+F(d,q)) { fq++; } }
     }}}}
  printf("i=%d  w<2q trapezoid(sum<=J*beta): %ld/%ld fails | w>=2q pairing: %ld/%ld fails | w>=2q PCI: %ld/%ld\n",I,fw,tw,fp,tp,fq,tq); fflush(stdout);}
 return 0;}
