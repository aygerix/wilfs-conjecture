/* Read ALL 3D ideal shapes, test m=2..13 and sorted r, every p. Fejer. */
#include <stdio.h>
#include <stdint.h>
static int C(int v,int p,int m){return v/m+(p<=v%m);}
int main(void){
 int N,f[20][3],R[20],bestN[14],best[14]={0};unsigned long long shapes[14]={0},inj[14]={0},shifts[14]={0},bad[14]={0};
 for(int m=2;m<=13;m++)bestN[m]=999;
 while(scanf("%d",&N)==1){for(int i=0;i<N;i++)for(int a=0;a<3;a++)scanf("%d",&f[i][a]);
  int dec=0;for(int i=0;i<N;i++)dec+=f[i][0]+f[i][1]+f[i][2]>=2;
  for(int m=N>2?N:2;m<=13;m++){
   shapes[m]++;
   for(int r=1;r<m;r++)for(int s=r;s<m;s++)for(int t=s;t<m;t++){
    int rr[]={r,s,t};uint64_t used=0;int ok=1;
    for(int i=0;i<N;i++){R[i]=f[i][0]*r+f[i][1]*s+f[i][2]*t;uint64_t b=1ull<<(R[i]%m);if(used&b){ok=0;break;}used|=b;}if(!ok)continue;
    inj[m]++;
    for(int p=1;p<=m;p++){
     shifts[m]++;int sum=0;for(int i=0;i<N;i++){int v=C(R[i],p,m);for(int a=0;a<3;a++)if(f[i][a])v-=f[i][a]*(C(R[i],p,m)-C(R[i]-rr[a],p,m));sum+=v;}
     int ex=sum-dec;if(ex>0){bad[m]++;if(ex>best[m])best[m]=ex;if(N<bestN[m]){bestN[m]=N;printf("FIRST m=%d N=%d r=%d,%d,%d p=%d sumK=%d dec=%d D=",m,N,r,s,t,p,sum,dec);for(int i=0;i<N;i++)printf("%s(%d,%d,%d)",i?",":"",f[i][0],f[i][1],f[i][2]);puts("");fflush(stdout);}}
    }
   }
  }
 }
 for(int m=2;m<=13;m++)printf("SUMMARY m=%d shapes=%llu injective=%llu shifts=%llu badshifts=%llu minN=%d maxexcess=%d\n",m,shapes[m],inj[m],shifts[m],bad[m],bestN[m],best[m]);return 0;
}
