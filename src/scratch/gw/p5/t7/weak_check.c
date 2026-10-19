/* Exact checks for P5g's weak-Sidon signed-label lemmas. Run on fejer.
 * args: max_span max_n. Enumerates ALL normalized weak-Sidon subsets
 * of {0,...,max_span-1}, 1 <= n <= max_n. No annealing, no floats.
 */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static int S,N,b[32],pc[2048];
static ll ct[32],strictct[32],sfct[32],cross_nonzero,repeat_nonzero;
static ll mindiff=1000000000,minrep=1000000000,minlabel=1000000000;
static ll choose2(ll x){return x*(x-1)/2;}
static void check(int n){
 int diff[2048]={0},f[4096]={0},r[4096]={0},sig[4096]={0},proper[4096]={0};
 int pfull[2048]={0},weak=1,G=0,ns=0,units=0;
 ll rp=0,fr=0,fp=0,eps=0,cp=0,ur=0;
 ct[n]++;
 for(int i=0;i<n;i++)for(int j=i;j<n;j++)if(++pfull[b[i]+b[j]]>1)weak=0;
 strictct[n]+=weak;
 for(int i=0;i<n;i++)for(int j=0;j<i;j++)diff[b[i]-b[j]]++;
 for(int d=1;d<S;d++){
  assert(diff[d]<=2);if(weak)assert(diff[d]<=1);
  if(2-diff[d]<mindiff)mindiff=2-diff[d];
 }
 for(int i=0;i<n;i++)for(int j=i;j<n;j++)for(int k=j;k<n;k++){
  int v=b[i]+b[j]+b[k];if(i<j&&j<k)f[v]++;else r[v]++;
 }
 for(int v=0;v<3*S;v++){
  if(f[v]>G)G=f[v];
  if(f[v]>0)eps+=f[v]-1;
  rp+=choose2(r[v]);fr+=(ll)f[v]*r[v];fp+=choose2(f[v]);
 }
 assert(rp<=2*choose2(n));if(weak)assert(rp<=choose2(n));
 if(2*choose2(n)-rp<minrep)minrep=2*choose2(n)-rp;
 repeat_nonzero+=rp>0;cross_nonzero+=fr>0;
 for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=i;j<n;j++)if(i!=k&&j!=k){
  int v=b[i]+b[j]-b[k]+S;sig[v]=1;if(i<j)proper[v]++;
 }
 for(int i=0;i<n;i++){
  ur+=proper[b[i]+S];sig[b[i]+S]=1;units++;
 }
 for(int v=0;v<3*S;v++){ns+=sig[v];cp+=choose2(proper[v]);}
 assert(ur<=n);if(weak)assert(ur==0);
 assert(cp<=9*fp+6*fr+4*rp);
 if(9*fp+6*fr+4*rp-cp<minlabel)minlabel=9*fp+6*fr+4*rp-cp;
 ll H=(ll)n*(choose2(n)+1),loss=H-ns;
 assert(loss<=n*(n-1)+cp+ur);
 if(G<=1){
  sfct[n]++;
  assert(loss<=11LL*n*n-4*n);
  if(weak)assert(loss<=9LL*n*n-3*n);
 }
 if(G>0){
  assert(2*loss<=9LL*G*eps+2LL*(6*G+5)*n*n-8*n);
  if(weak)assert(2*loss<=9LL*G*eps+2LL*(6*G+3)*n*n-6*n);
 }
 if(G<=10){
  assert(loss<=45*eps+65LL*n*n-4*n);
  if(weak)assert(loss<=45*eps+63LL*n*n-3*n);
 }
 assert(ns<=3*(b[n-1]-b[0]+1)-2);
 (void)units;
}
static void dfs(int n,int start){
 check(n);if(n==N)return;
 for(int x=start;x<S;x++){
  int ok=1;for(int j=0;j<n;j++)if(pc[x+b[j]]){ok=0;break;}
  if(!ok)continue;
  for(int j=0;j<n;j++)pc[x+b[j]]=1;
  b[n]=x;dfs(n+1,x+1);
  for(int j=0;j<n;j++)pc[x+b[j]]=0;
 }
}
int main(int ac,char**av){
 assert(ac==3);S=atoi(av[1]);N=atoi(av[2]);assert(S<=500&&N<=20);
 b[0]=0;dfs(1,1);
 for(int n=1;n<=N;n++)printf("n=%d weak=%lld strict=%lld sf_unique=%lld\n",n,ct[n],strictct[n],sfct[n]);
 printf("nonzero_repeat_pairs=%lld nonzero_sf_repeat=%lld min_diff_slack=%lld min_repeat_slack=%lld min_label_slack=%lld FAILURES=0\n",repeat_nonzero,cross_nonzero,mindiff,minrep,minlabel);
 return 0;
}
