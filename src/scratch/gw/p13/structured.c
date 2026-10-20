/* Interval, arithmetic progression, and power-trade/truncation tests at q=4. */
#include "core.h"
static unsigned long long count,cls,sparse;static ll mincu=LLONG_MAX,minp=LLONG_MAX;
static void test(int m,int ng,ll*g,int trunc){
 ll w[MM];Res r;count++;if(!apery(m,ng,g,w))return;
 if(trunc){ll K=trunc;for(int i=1;i<m;i++){ll v=K+(i-K%m+m)%m;if(w[i]>v)w[i]=v;}}
 evaluate(m,w,&r);if(r.q!=4||r.d<2)return;cls++;if(3*(r.d+1)<m)sparse++;
 if(r.CuSlack<mincu){mincu=r.CuSlack;dump("CU_RECORD",&r,w);}if(r.PlusSlack<minp){minp=r.PlusSlack;dump("PLUS_RECORD",&r,w);}
 if(r.CuSlack<0||r.PoorSlack<0||r.PlusSlack<0||r.nmfpoor){dump("COUNTEREXAMPLE",&r,w);exit(2);}
}
int main(int argc,char**argv){int lo=argc>1?atoi(argv[1]):5,hi=argc>2?atoi(argv[2]):100;ll g[MM];
 for(int m=lo;m<=hi;m++){
  for(int a=1;a<m;a++)for(int b=a+1;b<m;b++){int ng=0;for(int j=a;j<=b;j++)g[ng++]=m+j;test(m,ng,g,0);}
  for(int a=m/2+1;a<5*m/6;a++)for(int width=1;width<=8;width++){
   int ng=0;g[ng++]=2*a;g[ng++]=3*a;for(int j=1;j<=width;j++)g[ng++]=m+1+((a+j*j)% (m-1));
   for(int h=1;h<m;h+=m<30?1:5)test(m,ng,g,3*m+h);
  }
  fprintf(stderr,"DONE m=%d inputs=%llu q4=%llu sparse=%llu minCU=%lld minPLUS=%lld\n",m,count,cls,sparse,mincu,minp);fflush(stderr);
 }
 printf("SUMMARY inputs=%llu q4=%llu sparse=%llu minCU=%lld minPLUS=%lld\n",count,cls,sparse,mincu,minp);
}
