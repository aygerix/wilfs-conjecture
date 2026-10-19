/* Counterexample-shaped exact primary search, fejer only, nice.
 * a=7, q2=0, all quadratics present, degree<=3, |D|=m=107 or108.
 * Enumerate every increasing A-weight residue in [ceil(h/2),h-1],
 * with B0 pair injectivity. Cover missing residues by eligible cubics.
 * Usage a7_cover m first_rho last_rho.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int m,h,rho,t[7],L,topres,misslimit,minholes;
static uint64_t nodes,pairsets,eligible,topsets,pruned;
static int pop(u128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
static u128 bit(int r){return (u128)1<<r;}
static int forbid_optimistic(int depth,int next){
 int x[7];for(int i=0;i<depth;i++)x[i]=t[i];for(int i=depth;i<7;i++)x[i]=next+i-depth;
 int bad=0;for(int i=0;i<7;i++)for(int j=i;j<7;j++)for(int k=j;k<7;k++)if(x[i]+x[j]+x[k]>L)bad++;
 return bad>misslimit;
}
static void evaluate(u128 seen){
 pairsets++;int good=0,hastop=0;u128 cover=seen;
 for(int i=0;i<7;i++)for(int j=i;j<7;j++)for(int k=j;k<7;k++){
  int sum=t[i]+t[j]+t[k];if(sum>L)continue;good++;int r=sum%m;cover|=bit(r);
  if(sum==L)hastop=1;
 }
 if(good<m-36)return;eligible++;
 if(!hastop)return;topsets++;
 int holes=m-pop(cover);
 if(holes<minholes){
  minholes=holes;printf("BEST m=%d rho=%d h=%d holes=%d eligible_cubics=%d t=",m,rho,h,holes,good);for(int i=0;i<7;i++)printf("%s%d",i?",":"",t[i]);printf("\n");fflush(stdout);
 }
 if(!holes){printf("COVER_COUNTEREXAMPLE_CANDIDATE\n");fflush(stdout);exit(2);}
}
static void dfs(int depth,int next,u128 seen){
 nodes++;
 if(depth==7){evaluate(seen);return;}
 if(next+6-depth>h-1)return;
 if(depth>=2&&forbid_optimistic(depth,next)){pruned++;return;}
 for(int x=next;x<=h-1-(6-depth);x++){
  if(seen&bit(x%m))continue;
  u128 add=bit(x%m);int r=2*x%m;
  if((seen|add)&bit(r))continue;add|=bit(r);int ok=1;
  for(int i=0;i<depth;i++){
   r=(x+t[i])%m;if((seen|add)&bit(r)){ok=0;break;}add|=bit(r);
  }
  if(!ok||((seen|add)&bit(topres)))continue;
  t[depth]=x;dfs(depth+1,x+1,seen|add);
 }
}
int main(int argc,char **argv){
 if(argc!=4)return 1;m=atoi(argv[1]);int first=atoi(argv[2]),last=atoi(argv[3]);if(m<1||m>=128)return 1;
 for(rho=first;rho<=last;rho++){
  h=m-rho;L=m+h-1;topres=(h-1)%m;misslimit=120-m;minholes=m;
  nodes=pairsets=eligible=topsets=pruned=0;dfs(0,(h+1)/2,bit(0));
  printf("SUMMARY m=%d rho=%d nodes=%llu pairsets=%llu eligible=%llu top_eligible=%llu pruned=%llu minholes=%d potential_W=%d\n",m,rho,(unsigned long long)nodes,(unsigned long long)pairsets,(unsigned long long)eligible,(unsigned long long)topsets,(unsigned long long)pruned,minholes,8*53-4*m+rho);fflush(stdout);
 }
}
