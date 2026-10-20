/* Exhaust every loop graph through n=6. Run nice on fejer. */
#include <stdio.h>
#include <stdint.h>
static long long mac(int x){int r=1;while((r+1)*r/2<=x)r++;int s=x-r*(r-1)/2;return (long long)(r+1)*r*(r-1)/6+(long long)(s+1)*s/2;}
int main(void){
 unsigned long long total=0;int first=0;
 for(int n=1;n<=6;n++){
  int es=n*(n+1)/2;unsigned lim=1u<<es;long long maxgap=-999999;
  for(unsigned mask=0;mask<lim;mask++){
   int a[6][6]={{0}},k=0,E=0;
   for(int i=0;i<n;i++)for(int j=i;j<n;j++,k++)if(mask&(1u<<k)){a[i][j]=a[j][i]=1;E++;}
   int color[6],f=0,fn=0,Eb=0,Vactive=0;long long locmac=0;for(int i=0;i<n;i++)color[i]=-1;
   for(int v=0;v<n;v++){int d=0;for(int j=0;j<n;j++)d+=a[v][j];if(d)Vactive++;}
   for(int root=0;root<n;root++)if(color[root]<0){
    int q[6],lo=0,hi=0,vs=0,ee=0,nb=0;q[hi++]=root;color[root]=0;
    while(lo<hi){int v=q[lo++];vs++;
     for(int w=0;w<n;w++)if(a[v][w]){
      if(w>=v)ee++;
      if(color[w]<0){color[w]=1-color[v];q[hi++]=w;}
      else if(color[w]==color[v])nb=1;
     }
    }
    if(ee>vs)f+=ee-vs;
    if(nb){fn+=ee-vs;locmac+=mac(ee-vs);}else Eb+=ee;
   }
   int T=0;for(int i=0;i<n;i++)for(int j=i;j<n;j++)for(int z=j;z<n;z++)if(a[i][j]&&a[i][z]&&a[j][z])T++;
   long long gap=T-E-mac(fn)+Eb;if(gap>maxgap)maxgap=gap;
   if(gap>0){printf("GRAPH_BOUND_FAIL n=%d mask=%u E=%d T=%d fn=%d Eb=%d\n",n,mask,E,T,fn,Eb);return 2;}
   if(T-E>locmac-Eb){puts("COMPONENT_BOUND_FAIL");return 2;}
   if(f==0&&T>E){puts("PSEUDO_FAIL");return 2;}
   for(int alpha=0;alpha<=10;alpha++)if(T-E+alpha*(E-Vactive)>mac(fn)-Eb+alpha*f){puts("LOW_LINK_FAIL");return 2;}
   if(!first&&E<=n&&T>E){first=1;printf("FALSE_GLOBAL n=%d mask=%u E=%d T=%d\n",n,mask,E,T);}
   total++;
  }
  printf("SUMMARY n=%d graphs=%u max(T-E-M(fn)+Eb)=%lld\n",n,lim,maxgap);
 }
 printf("TOTAL graphs=%llu failures=0\n",total);return 0;
}
