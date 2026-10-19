/* count sorted k-sets P in [1,m-1] with {0} u P having all 2-multiset sums distinct mod m (lead re-check of P6b bases) */
#include <stdio.h>
#include <stdlib.h>
static int k,m,P[16],n,used[256]; static long long cnt;
static void dfs(int i,int lo){ if(i==k){cnt++;return;}
  for(int v=lo;v<m;v++){ int ok=1,j,added[40],na=0; P[i+1]=v; /* P[0]=0 */
    for(j=0;j<=i+1;j++){ int s=(P[j]+v)%m; if(used[s]){ok=0;break;} used[s]=1; added[na++]=s; }
    if(ok) dfs(i+1,v+1);
    for(j=0;j<na;j++) used[added[j]]=0; } }
int main(int c,char**v){ k=atoi(v[1]); for(int a=2;a<c;a++){ m=atoi(v[a]); for(int r=0;r<m;r++) used[r]=0; P[0]=0; used[0]=1; cnt=0; dfs(0,1); printf("k=%d m=%d sorted_full_pair_bases=%lld\n",k,m,cnt);} return 0; }
