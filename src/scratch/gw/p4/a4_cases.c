/* Independently check saved numerical cases. Run on fejer, stdin file. */
#include "p4_check.h"
#include "a4_extra.h"
int main(void){
 int m,d,n[128],X[128*128],cases=0;
 while(scanf("%d%d",&m,&d)==2){
  assert(m<128&&d<128);
  for(int j=0;j<d;j++)assert(scanf("%d",&n[j])==1);
  for(int i=0;i<m*d;i++)assert(scanf("%d",&X[i])==1);
  p4verify(m,d,X,n);a4verify(m,d,X,n);cases++;
 }
 printf("saved_cases=%d\n",cases);p4summary();a4summary();
}
