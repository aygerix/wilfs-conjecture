/* Endpoint certificate for the remaining r=l=b=0 strip; fejer only. */
#include <stdio.h>
#include <stdlib.h>
typedef long long I;
static I H(I n){return n*(n*(n-1)/2+1);}
static I mn(I a,I b){return a<b?a:b;}
static I lam2(I n){if(n<2)return 0;if(n==2)return 2;if(n==3)return 4;if(n==4)return 8;return n%3?3*(n-1):3*n;}
static I fd(I a,I b){I q=a/b;if(a%b<0)q--;return q;}
int main(int argc,char **argv){
 int hi=argc>1?atoi(argv[1]):40;
 for(I al=4;al<=hi;al++){
  I Q=al*(al+1)/2,U=al*(al+1)*(al+2)/6,checked=0,surv=0,afirst=0,alast=0,nfirst=0,epfirst=0;
  for(I a=2*al+3;a<2*Q+38;a++){
   if(a<=32)continue;
   I B0=(a-2*al-1)*Q+2*U+2*al-a+1;
   I lo=Q/4+1,hi0=mn(fd((a-2*al-1)*Q-2*a+3*al,6),fd(B0-2,3));
   for(I n=al;n<=a;n++){
    I high=mn(hi0,fd(2*Q*(n-al)-a+2*al+2*U-(a+3)*Q,3));
    if(lo>high)continue;
    checked++;
    I ep=lam2(n)>27?high:lo;
    if(2*H(n)-9*B0+10+(27-lam2(n))*ep<=0){
     surv++;if(!afirst){afirst=a;nfirst=n;epfirst=ep;}alast=a;
    }
   }
  }
  printf("alpha=%lld checked=%lld survivors=%lld a_first=%lld a_last=%lld first_n=%lld first_eps=%lld\n",al,checked,surv,afirst,alast,nfirst,epfirst);fflush(stdout);
 }
}
