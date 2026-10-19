/* Independent exact verification of the 64..143 count certificate.
 * Rank term is evaluated as sum of pairwise minima, not sorted ranks. */
#include <stdio.h>
#include <limits.h>
static int best[144][48],a[6],parts=0;
static int D(int n){int h=0,out=0;while(n){int k=6*(h+1);if(k>n)k=n;out+=k*h;n-=k;h++;}return out;}
static int J(int n){if(n<0)n=0;int q=n/12,r=n%12;return 6*q*(q-1)+r*q;}
static void accept(void){int n=0,v=0,w[48],nn=0;for(int i=0;i<6;i++){n+=a[i];v+=a[i]*(a[i]+1)/2;for(int j=0;j<a[i];j++)w[nn++]=a[i]+5;}if(v>138)return;parts++;int R=0;for(int i=0;i<nn;i++)for(int j=0;j<i;j++)R+=w[i]<w[j]?w[i]:w[j];for(int n2=v;n2<143;n2++)if(R<best[n2][n])best[n2][n]=R;}
static void dfs(int i,int lo,int sum,int vol){if(i==6){accept();return;}for(int v=lo;sum+v*(6-i)<=41&&vol+v*(v+1)/2<=138;v++){a[i]=v;dfs(i+1,v,sum+v,vol+v*(v+1)/2);}}
int main(void){for(int j=0;j<144;j++)for(int t=0;t<48;t++)best[j][t]=INT_MAX;dfs(0,0,0,0);long long count=0,fail=0,min=1LL<<60;int arg[7]={0};for(int m=64;m<=143;m++)for(int n2=0;n2<=m-5;n2++)for(int t1=0;t1<=4;t1++)for(int t2=0;t2<48;t2++){if(t2*t2+6*t2>12*n2||best[n2][t2]==INT_MAX)continue;count++;int n1=m-1-n2,H=D(n2)+J(3*n1-n2-6),b=(12*m-15*t1-24*t2+3)/4;if(b>H)H=b;if(H<0)H=0;long long R=best[n2][t2]+5LL*(t1*t2+t1*(t1-1)/2),s=(m+1LL)*H+R-3LL*m*(m-1)/2;if(s<min){min=s;arg[0]=m;arg[1]=n1;arg[2]=n2;arg[3]=t1;arg[4]=t2;arg[5]=H;arg[6]=R;}fail+=s<0;}printf("partitions=%d states=%lld failures=%lld min_slack=%lld arg=%d,%d,%d,%d,%d,%d,%d\n",parts,count,fail,min,arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6]);return fail?1:0;}
