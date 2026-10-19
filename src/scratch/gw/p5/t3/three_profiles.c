/* Independent integer audit of the bounded profile proof. fejer only. */
#include <stdio.h>
#include <stdint.h>
#include <assert.h>
static long long C2(long long n){return n*(n-1)/2;}
static long long C3(long long n){return n*(n-1)*(n-2)/6;}
static long long H(long long n){return n*(C2(n)+1);}
static long long L2(int n){if(n<=1)return 0;if(n==2)return 2;if(n==3)return 4;if(n==4)return 8;return n%3?3*(n-1):3*n;}
static uint64_t hh=1469598103934665603ULL;
static void mix(int v){hh=(hh^(uint64_t)v)*1099511628211ULL;}
int main(void){
 long long total=0,expanded=0,totalprofiles=0,after16=0;
 for(int a=14;a<=40;a++){
  long long tested=0,surv=0;
  for(int r=0;r<=2;r++)for(int l=0;l<=4-2*r;l++)for(int n0=6-r;n0<=6;n0++){
   int q2=n0+l,F=C3(a+1),tmin=r==0?0:r==1?a:2*a-1;
   int tmax=(F-(a+1)*q2+(a-3)*r-1)/4;
   for(int t=tmin;t<=tmax;t++){
    int D3=3*t-(a+2)*r,star=l*(a+2-l),rough=15-5*a+star+D3;
    if(rough>=0)continue;
    for(int R=0;R<=a-3;R++){
     int cold=a-27+(a+3)*n0+star-2*n0*R-(a+2)*r;
     int raw=a-39+(a+3)*n0+star-2*n0*R+D3;
     int bf=a-7-n0+l,bh=a-7-n0-3*l-2*r,e=l+r;
     assert(bf>=1);
     int BB=2*(13+n0+l+e+C3(e+2)+(n0+3*e)*(a-3))-(a-1)-(a+3)*(n0+l);
     for(int b=0;b<=5*a-16;b++){
      if(rough+b*bf>=0||cold+b*bf>=0||raw+b*bf>=0)continue;
      tested++;
      int upper=BB-D3-b*bh-1,nn=R-l-r,np=R-l-2*r;if(nn<0)nn=0;if(np<0)np=0;
      int first=0,last=0;
      for(int delta=1;delta<=upper;delta++){
       int w=(delta+1)/2;
       if(nn*(nn-1)>delta-1+2*r*(r+1))continue;
       if(C3(nn+2)-t>3*w-2)continue;
       int local=t-tmin;
       if(2*H(np)-L2(np)*local>2*(3*w-2))continue;
       int nw=R-r;if(nw<0)nw=0;
       if(2*H(nw)-L2(nw)*local>2*(3*delta-2))continue;
       if(C3(R+2)-t>3*delta-2)continue;
       if(R*(R-1)>2*delta-2+2*r*(r+1))continue;
       if(!first)first=delta;last=delta;expanded++;
      }
      if(first){
       surv++;mix(a);mix(r);mix(l);mix(n0);mix(t);mix(R);mix(b);mix(first);mix(last);
      }
     }
    }
   }
  }
  total+=surv;totalprofiles+=tested;if(a>=16)after16+=tested;
  printf("a=%d profiles=%lld survive=%lld\n",a,tested,surv);
  if(a>=16)assert(!surv);
 }
 printf("total_profiles=%lld profiles_a_ge16=%lld total_survivors=%lld expanded=%lld hash=%llu\n",totalprofiles,after16,total,expanded,(unsigned long long)hh);
}
