/* P6c exceptional covered-defect case: k=6, m=26, missing 3 disjoint
   ordinary pairs. All unit sets, all perfect matchings, all possible
   single cubics and all phases. fejer only, nice, one core. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
static int P[6],missing[6][6],nset;static long long sets,matchings,bases,tiles,phases;
static long long minS=1LL<<60,minHC=1LL<<60;
static void fullmatching(void){
  matchings++;int seen[26]={0};seen[0]=1;
  for(int i=0;i<6;i++)seen[P[i]]=1;
  int pair[6][6],free=-1;
  for(int i=0;i<6;i++)for(int j=i;j<6;j++){
    pair[i][j]=(P[i]+P[j])%26;
    if(missing[i][j])continue;
    if(seen[pair[i][j]])return;seen[pair[i][j]]=1;
  }
  bases++;for(int r=0;r<26;r++)if(!seen[r]){if(free>=0)exit(3);free=r;}
  if(free<0)exit(4);
  for(int a=0;a<6;a++)for(int b=a;b<6;b++)for(int c=b;c<6;c++){
    if(missing[a][b]||missing[a][c]||missing[b][c])continue;
    if((P[a]+P[b]+P[c])%26!=free)continue;
    int n2[6][6]={0};n2[a][b]=n2[a][c]=n2[b][c]=1;tiles++;
    for(int sig=0;sig<26;sig++){
      int r0=(26-sig)%26,U[6],pos=0;long long ns=r0,aa=0;
      for(int i=0;i<6;i++){U[i]=(P[i]-sig+26)%26;ns+=U[i];}
      for(int i=0;i<6;i++)for(int j=i;j<6;j++)if(!missing[i][j]){
        int r=(pair[i][j]-sig+26)%26;
        if(n2[i][j])ns+=r;else{aa+=r;if(U[i]+U[j]-r0-r==26)pos++;}
      }
      long long S=7*ns-aa-2*((free-sig+26)%26),H=S-26*pos;
      phases++;if(S<minS)minS=S;if(H<minHC)minHC=H;
      if(S<0){printf("MAXCL_COUNTEREXAMPLE sigma=%d S=%lld P=",sig,S);for(int i=0;i<6;i++)printf(" %d",P[i]);printf(" cube=%d,%d,%d\n",a,b,c);exit(2);}
    }
  }
}
static void matching(int mask){
  if(mask==63){fullmatching();return;}
  int i=0;while(mask>>i&1)i++;
  for(int j=i+1;j<6;j++)if(!(mask>>j&1)){
    missing[i][j]=1;matching(mask|(1<<i)|(1<<j));missing[i][j]=0;
  }
}
static void units(int a,int start){
  if(a==6){sets++;matching(0);return;}
  for(int v=start;v<=25-(5-a);v++){P[a]=v;units(a+1,v+1);}
}
int main(void){units(0,1);printf("sets=%lld matchings=%lld pair_bases=%lld single_cube_tiles=%lld phases=%lld minS=%lld minHC=%lld\n",sets,matchings,bases,tiles,phases,tiles?minS:-1,tiles?minHC:-1);}
