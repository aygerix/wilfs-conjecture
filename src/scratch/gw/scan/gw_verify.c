/* Second, literal, pointwise checker. stdin: d m; n[d]; D[m][d]. */
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
int main(void){
 int d,m,x[104][12],seen[104]={0};int64_t n[12],v[104],g=0,M=0,sum=0;
 if(scanf("%d%d",&d,&m)!=2||d<1||d>12||m<2||m>100)return 1;
 for(int a=0;a<d;a++)if(scanf("%"SCNd64,&n[a])!=1||n[a]<=0)return 1;
 for(int i=0;i<m;i++){
  v[i]=0;for(int a=0;a<d;a++){if(scanf("%d",&x[i][a])!=1||x[i][a]<0)return 1;v[i]+=x[i][a]*n[a];}
  if(seen[v[i]%m]++)return 2;g+=v[i]/m;sum+=v[i];if(v[i]>M)M=v[i];
 }
 int t=0;
 for(int i=0;i<m;i++){
  int maximal=1;
  for(int a=0;a<d;a++){
   int pred=!x[i][a];
   for(int j=0;j<m;j++){
    int less=1,more=1;for(int b=0;b<d;b++){if(x[j][b]!=x[i][b]-(b==a))less=0;if(x[j][b]!=x[i][b]+(b==a))more=0;}
    if(less)pred=1;if(more)maximal=0;
   }
   if(!pred)return 3;
  }
  t+=maximal;
 }
 for(int a=0;a<d;a++){int unit=0;for(int i=0;i<m;i++){int equal=1;for(int b=0;b<d;b++)if(x[i][b]!=(a==b))equal=0;if(equal)unit=1;}if(!unit)return 4;}
 int64_t c=M-m+1,E=d*c-(d+1)*g;
 int64_t B=d*(int64_t)m*M-(d+1)*sum,tau=(d-1)*(int64_t)m*(m-1)/2;
 if(B-tau!=m*E)return 5;
 printf("%"PRId64" %"PRId64" %"PRId64" %"PRId64" %d\n",E,c,g,M,t);
 return 0;
}
