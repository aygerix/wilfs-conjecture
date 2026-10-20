/* Exhaust ALL two-dimensional ideals of size <=m, all r, all p. Fejer. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int m,N,row[80],height,R[80],deg[80],X[80],Y[80];
static unsigned long long shapes,injective,shifts,bad;static int minsize,minp,minr,mins,best;
static int C(int y,int p){return y/m+(p<=y%m);}
static void test(void){
 int n=0;for(int j=0;j<height;j++)for(int i=0;i<row[j];i++){X[n]=i;Y[n]=j;deg[n++]=i+j;}
 shapes++;
 for(int r=1;r<m;r++)for(int s=r;s<m;s++){
  uint64_t used=0;int ok=1;for(int i=0;i<N;i++){R[i]=X[i]*r+Y[i]*s;uint64_t b=1ull<<(R[i]%m);if(used&b){ok=0;break;}used|=b;}if(!ok)continue;
  injective++;int dec=0;for(int i=0;i<N;i++)dec+=deg[i]>=2;
  for(int p=1;p<=m;p++){
   shifts++;int sum=0;for(int i=0;i<N;i++){int k=C(R[i],p);if(X[i])k-=X[i]*(C(R[i],p)-C(R[i]-r,p));if(Y[i])k-=Y[i]*(C(R[i],p)-C(R[i]-s,p));sum+=k;}
   int ex=sum-dec;if(ex>0){bad++;if(N<minsize){minsize=N;minp=p;minr=r;mins=s;printf("FIRST m=%d N=%d r=%d,%d p=%d sumK=%d dec=%d rows=",m,N,r,s,p,sum,dec);for(int j=0;j<height;j++)printf("%s%d",j?",":"",row[j]);puts("");fflush(stdout);}if(ex>best)best=ex;}
  }
 }
}
static void parts(int remaining,int cap,int j){
 if(!remaining){height=j;test();return;}
 for(int z=remaining<cap?remaining:cap;z>=1;z--){row[j]=z;parts(remaining-z,z,j+1);}
}
int main(int argc,char**argv){int lo=argc>1?atoi(argv[1]):2,hi=argc>2?atoi(argv[2]):16;if(hi>60)return 2;
 for(m=lo;m<=hi;m++){shapes=injective=shifts=bad=0;minsize=999;best=0;for(N=1;N<=m;N++)parts(N,N,0);printf("SUMMARY m=%d shapes=%llu injective=%llu shifts=%llu badshifts=%llu minN=%d maxexcess=%d\n",m,shapes,injective,shifts,bad,minsize,best);fflush(stdout);}return 0;}
