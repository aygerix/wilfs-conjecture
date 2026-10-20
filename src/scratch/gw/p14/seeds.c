/* Build modular full-A-cubic simplex seeds; preserve RA>pA. Fejer only. */
#include "core.h"
static uint64_t rs=140061;static unsigned rn(unsigned n){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs%n;}
static int ok(int m,int a,int*x){
 int seen[MM]={0};seen[0]=1;
 for(int i=0;i<a;i++){int t=x[i]%m;if(seen[t])return 0;seen[t]=1;}
 for(int i=0;i<a;i++)for(int j=i;j<a;j++){int t=(x[i]+x[j])%m;if(seen[t])return 0;seen[t]=1;}
 for(int i=0;i<a;i++)for(int j=i;j<a;j++)for(int k=j;k<a;k++){int t=(x[i]+x[j]+x[k])%m;if(seen[t])return 0;seen[t]=1;}
 return 1;
}
int main(void){
 int ms[]={61,101,211,401};ll w[MM];
 for(int mi=0;mi<4;mi++){
  int m=ms[mi],found=0;
  for(int tr=0;tr<100000&&!found;tr++){
   int h=4+rn(m-4),a=4+(mi>1?rn(2):0),x[8],got=0;
   for(int att=0;att<200&&got<a;att++){
    int low=(h+1)/2,high=(m+h-1)/3;if(high>=h)high=h-1;if(high<low)break;
    x[got]=low+rn(high-low+1);if(ok(m,got+1,x))got++;
   }
   if(got!=a)continue;
   int cap=3*m+h;for(int i=1;i<m;i++)w[i]=cap+(i-cap%m+m)%m;w[0]=0;
   for(int i=0;i<a;i++){ll v=m+x[i];w[v%m]=v;}
   for(int i=0;i<a;i++)for(int j=i;j<a;j++){ll v=2*m+x[i]+x[j];w[v%m]=v;}
   for(int i=0;i<a;i++)for(int j=i;j<a;j++)for(int k=j;k<a;k++){ll v=3*m+x[i]+x[j]+x[k];w[v%m]=v;}
   Res r;evaluate(m,w,&r);if(r.q!=4||r.RA<=r.pA)continue;
   char fn[80];snprintf(fn,sizeof(fn),"seed_%d.txt",m);FILE*f=fopen(fn,"w");for(int i=0;i<m;i++)fprintf(f,"%lld%c",w[i],i==m-1?'\n':' ');fclose(f);
   dump("SEED",&r,w);found=1;
  }
  if(!found)printf("NO_SEED m=%d\n",m);
 }
}
