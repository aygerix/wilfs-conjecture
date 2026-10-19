/* P6b: every height-three core in three directions, with arbitrary spikes.
 * All arithmetic exact.  fejer, nice, single core. No command-line domain.
 * CR proves all m >= its shape threshold.  For smaller m, d<=5 is H3-D5;
 * the loops below cover every remaining m, sorted residue vector, and phase.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long ull;
typedef long long ll;
static int pi[6],pj[6],ca[10],cb[10],cc[10];
static unsigned divs[10];
static ull shapes,rows,nominal_vectors,injective_vectors,phases,realized_rows;
static int max_threshold;
static ll global_min=0x7fffffffffffffffLL;
static void vec(int x,int y,int z){printf("[%d,%d,%d]",x,y,z);}
int main(void){
 int np=0,pid[3][3];
 for(int a=0;a<3;a++)for(int b=a;b<3;b++){
  pi[np]=a;pj[np]=b;pid[a][b]=pid[b][a]=np++;
 }
 int nt=0;
 for(int a=0;a<3;a++)for(int b=a;b<3;b++)for(int c=b;c<3;c++){
  ca[nt]=a;cb[nt]=b;cc[nt]=c;
  divs[nt++]=(1U<<pid[a][b])|(1U<<pid[a][c])|(1U<<pid[b][c]);
 }
 assert(np==6&&nt==10);
 for(unsigned Q=1;Q<64;Q++){
  unsigned support=0,eligible=0;
  for(int j=0;j<6;j++)if(Q>>j&1)support|=(1U<<pi[j])|(1U<<pj[j]);
  if(support!=7)continue;
  for(int j=0;j<10;j++)if((divs[j]&Q)==divs[j])eligible|=1U<<j;
  for(unsigned T=eligible;T;T=(T-1)&eligible){
   shapes++;unsigned N2=0;
   for(int j=0;j<10;j++)if(T>>j&1)N2|=divs[j];
   int q=__builtin_popcount(Q),t=__builtin_popcount(T),p=__builtin_popcount(N2);
   int a=q-p,J=(4+p)*(3+p)/2,B=a+2*t,size=4+q+t;
   assert(J>B);
   int A=J*(q+t)-t*t-t-a*t-a*(a+1)/2;
   int threshold=(A+J-B-1)/(J-B);
   if(threshold>max_threshold)max_threshold=threshold;
   for(int m=size+3;m<threshold;m++){
    assert(m<64);rows++;ull ninj=0,nphase=0;ll mn=0x7fffffffffffffffLL;
    int wp[3]={0},ws=0;
    assert((m-q-t)*J-B*(m-1)+t*(t-1)+a*t+a*(a-1)/2<0);
    for(int x=1;x<m;x++)for(int y=x+1;y<m;y++)for(int z=y+1;z<m;z++){
     nominal_vectors++;int P[3]={x,y,z},rv[20],coef[20],len=0;ull used=1;
     rv[len]=0;coef[len++]=m-q-t;
     for(int j=0;j<3;j++){used|=1ULL<<P[j];rv[len]=P[j];coef[len++]=m-q-t;}
     int valid=1;
     for(int j=0;j<6&&valid;j++)if(Q>>j&1){
      int r=(P[pi[j]]+P[pj[j]])%m;
      if(used>>r&1){valid=0;break;}used|=1ULL<<r;
      rv[len]=r;coef[len++]=(N2>>j&1)?m-q-t:-1;
     }
     for(int j=0;j<10&&valid;j++)if(T>>j&1){
      int r=(P[ca[j]]+P[cb[j]]+P[cc[j]])%m;
      if(used>>r&1){valid=0;break;}used|=1ULL<<r;rv[len]=r;coef[len++]=-2;
     }
     if(!valid)continue;
     assert(len==size);ninj++;injective_vectors++;
     for(int sig=0;sig<m;sig++){
      ll slack=0;for(int j=0;j<len;j++)slack+=(ll)coef[j]*((rv[j]+m-sig)%m);
      phases++;nphase++;
      if(slack<mn){mn=slack;wp[0]=x;wp[1]=y;wp[2]=z;ws=sig;}
      if(slack<global_min)global_min=slack;
      if(slack<0){
       printf("MAXCL_COUNTEREXAMPLE Q=%u T=%u m=%d d=%d p=",Q,T,m,m-q-t-1);
       vec(x,y,z);printf(" sigma=%d slack=%lld\n",sig,slack);return 2;
      }
     }
    }
    if(ninj){realized_rows++;printf("REALIZED Q=%u T=%u q=%d t=%d p=%d m=%d s=%d d=%d injective=%llu phases=%llu min=%lld witness=",Q,T,q,t,p,m,m-size,m-q-t-1,ninj,nphase,mn);vec(wp[0],wp[1],wp[2]);printf(" sigma=%d\n",ws);}
   }
  }
 }
 printf("CORE3_SUMMARY shapes=%llu rows=%llu nominal_vectors=%llu injective_vectors=%llu phases=%llu realized_rows=%llu max_cr_threshold=%d min=%lld FAILURES=0\n",shapes,rows,nominal_vectors,injective_vectors,phases,realized_rows,max_threshold,global_min);
 return 0;
}
