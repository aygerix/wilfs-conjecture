/* Smallest class-III A face in the stated parameter family, fejer only.
 * All cubic monomials and the fourth power of the unique low direction.
 * Complete the uncovered residues with class-E unit directions.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char **argv){
 int last=argc>1?atoi(argv[1]):160;
 uint64_t tried=0,checked=0;
 for(int m=36;m<=last;m++){
  uint64_t found=0;
  for(int h=13;h<=m;h++)for(int t=3;4*t<h;t++)
   for(int u=h-t;u<h;u++)for(int v=u+1;v<h;v++)for(int w=v+1;w<h;w++){
    tried++;if(3*w>m+h-1)continue;checked++;
    int s[5]={0,t,u,v,w},seen[512]={0},ok=1,reservebad=0;
    for(int i=0;i<5&&ok;i++)for(int j=i;j<5&&ok;j++)for(int k=j;k<5;k++){
     int sum=s[i]+s[j]+s[k],r=sum%m;if(seen[r]){ok=0;break;}seen[r]=1;
     int value=m*((i>0)+(j>0)+(k>0))+sum;
     if(r==(h-1)%m&&value!=4*m+h-1)reservebad=1;
    }
    if(!ok||seen[4*t%m]||reservebad)continue;
    if(4*t%m==(h-1)%m&&4*t!=h-1)continue;
    found++;
    if(found<=5)printf("FOUND m=%d h=%d rho=%d t=%d,%d,%d,%d W_E=%d\n",m,h,m-h,t,u,v,w,25*m-h-868);
   }
  printf("m=%d tried=%llu checked=%llu found=%llu\n",m,(unsigned long long)tried,(unsigned long long)checked,(unsigned long long)found);fflush(stdout);
  if(found)return 0;
 }
 return 0;
}
