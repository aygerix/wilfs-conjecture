/* P6 coverage reconnaissance. ALL compute on fejer, nice, one core.
 * Enumerate residue vectors up to coordinate permutation only.
 * No group automorphism normalization: numerical r-values matter.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long ull;
static int d,m,p[8],pairi[32],pairj[32],pr[32],np;
static ull nr,ncov,nallow;
static void check(void){
 nr++;ull cov=1,allow=1,units=1;
 for(int i=0;i<d;i++)units|=1ULL<<p[i];
 cov=allow=units;
 int bad[32],pid[8][8];np=0;
 for(int i=0;i<d;i++)for(int j=i;j<d;j++){
  pairi[np]=i;pairj[np]=j;pid[i][j]=pid[j][i]=np;
  pr[np]=(p[i]+p[j])%m;bad[np]=(units>>pr[np])&1;
  cov|=1ULL<<pr[np];if(!bad[np])allow|=1ULL<<pr[np];np++;
 }
 for(int i=0;i<d;i++)for(int j=i;j<d;j++)for(int k=j;k<d;k++){
  int r=(p[i]+p[j]+p[k])%m;cov|=1ULL<<r;
  int a=pid[i][j],b=pid[i][k],c=pid[j][k];
  if(bad[a]||bad[b]||bad[c])continue;
  if((a!=b&&pr[a]==pr[b])||(a!=c&&pr[a]==pr[c])||(b!=c&&pr[b]==pr[c]))continue;
  allow|=1ULL<<r;
 }
 ull all=(1ULL<<m)-1;
 ncov+=cov==all;nallow+=allow==all;
}
static void rec(int k,int start){
 if(k==d){check();return;}
 for(int x=start;x<=m-(d-k);x++){p[k]=x;rec(k+1,x+1);}
}
int main(int ac,char**av){
 assert(ac==2);d=atoi(av[1]);assert(2<=d&&d<=5);
 int mx=(d+1)*(d+2)*(d+3)/6;
 for(m=d+1;m<=mx;m++){
  nr=ncov=nallow=0;rec(0,1);
  printf("d=%d m=%d residue_sets=%llu three_cover=%llu legal_cover=%llu\n",d,m,nr,ncov,nallow);fflush(stdout);
 }
 return 0;
}
