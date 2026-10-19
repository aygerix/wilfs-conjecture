/* w-shift side condition SC_t: F(u+w) + (J-1)*t <= beta + F(delta+Jw),  t = ceil(w/w'), w'=min(w,2q-1)
   over formal PCI instances 0<=u<=beta*w', M in [max(T,u+Jw), ...], 1<=J<i, 0<=beta<i.
   reports fails split by w<2q / w>=2q and delta<q / delta>=q.  usage: sc imax qmax */
#include <stdio.h>
#include <stdlib.h>
static int I;
static long F(long t,long q){ long f=t/q; return f<I?f:I; }
int main(int argc,char**argv){ int imax=atoi(argv[1]); long qmax=atol(argv[2]);
 for(I=3;I<=imax;I++){ long tot[2][2]={{0}},fl[2][2]={{0}};
  for(long q=1;q<=qmax;q++){ long T=(2*I-2)*q-1;
   for(long w=q+1;w<=(long)(2*I)*q+1;w++){ long wp=w<2*q-1?w:2*q-1; long t=(w+wp-1)/wp; int W=w>=2*q;
    for(int b=0;b<I;b++) for(int J=1;J<I;J++) for(long u=0;u<=b*wp;u++){
     long Mlo=T>u+(long)J*w?T:u+(long)J*w;
     for(long M=Mlo;M<=Mlo+u+1;M++){ long d=M-u-(long)J*w; int D=d>=q;
      tot[W][D]++;
      if(F(u+w,q)+(long)(J-1)*t > b+F(d+(long)J*w,q)){ fl[W][D]++;
        if(fl[W][D]<=2) printf("SC fail i=%d q=%ld w=%ld b=%d J=%d u=%ld d=%ld  F(u+w)=%ld F(d+Jw)=%ld\n",I,q,w,b,J,u,d,F(u+w,q),F(d+(long)J*w,q)); }
     }}}}
  printf("i=%d  w<2q: d<q %ld/%ld  d>=q %ld/%ld | w>=2q: d<q %ld/%ld d>=q %ld/%ld\n",I,fl[0][0],tot[0][0],fl[0][1],tot[0][1],fl[1][0],tot[1][0],fl[1][1],tot[1][1]); fflush(stdout);}
 return 0;}
