/* Every loop graph on k<=6 vertices: upper cubic shadow >= k*cover number.
 * fejer only, nice, one core. Does not establish the unbounded theorem.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long ull;
int main(void){
 for(int k=1;k<=6;k++){
  int np=0,pi[21],pj[21];ull up[21]={0};
  for(int a=0;a<k;a++)for(int b=a;b<k;b++){pi[np]=a;pj[np++]=b;}
  int id=0;
  for(int a=0;a<k;a++)for(int b=a;b<k;b++)for(int c=b;c<k;c++){
   for(int j=0;j<np;j++){
    int x[6]={0};x[a]++;x[b]++;x[c]++;x[pi[j]]--;x[pj[j]]--;
    int ok=1;for(int v=0;v<k;v++)if(x[v]<0)ok=0;
    if(ok)up[j]|=1ULL<<id;
   }id++;
  }
  assert(id<=56);
  unsigned cover[64];int order[64],norder=0;
  for(int s=0;s<(1<<k);s++){
   unsigned z=0;for(int j=0;j<np;j++)if((s>>pi[j]&1)||(s>>pj[j]&1))z|=1U<<j;
   cover[s]=z;
  }
  for(int size=0;size<=k;size++)for(int s=0;s<(1<<k);s++)if(__builtin_popcount((unsigned)s)==size)order[norder++]=s;
  unsigned num=1U<<np;ull *shadow=calloc(num,sizeof(ull));assert(shadow);
  int min=1000000;ull count=0;
  for(unsigned E=0;E<num;E++){
   if(E){unsigned prev=E&(E-1);shadow[E]=shadow[prev]|up[__builtin_ctz(E)];}
   int tau=-1;for(int j=0;j<norder;j++)if((E&cover[order[j]])==E){tau=__builtin_popcount((unsigned)order[j]);break;}
   int r=__builtin_popcountll(shadow[E]),slack=r-k*tau;assert(tau>=0&&slack>=0);
   if(slack<min)min=slack;
   count++;
  }
  printf("SHADOW_COVER k=%d graphs=%llu min=%d FAILURES=0\n",k,count,min);fflush(stdout);free(shadow);
 }
 printf("SHADOW_COVER_ALL_PASS\n");return 0;
}
