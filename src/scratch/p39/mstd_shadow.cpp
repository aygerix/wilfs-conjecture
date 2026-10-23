// E436: one exact falsification of the staged L_out<=C claim, not a search.
// The underlying MSTD/base-expansion construction is classical; see PROOFS E436.
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <functional>
#include <limits>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <utility>
#include <vector>
using ll=long long;
int main(){
 const int seed[]={0,2,3,4,7,11,12,14};std::vector<int>A;
 for(int a:seed)for(int b:seed)for(int c:seed)A.push_back(a+29*b+29*29*c);
 std::sort(A.begin(),A.end());assert(std::adjacent_find(A.begin(),A.end())==A.end());
 int d=A.size(),R=A.back(),T=R+1;std::vector<int>B;for(int a:A)B.push_back(T+a);
 int m=4*B.back()+2,e=d+1;assert(3*e<m && 2*B.back()<m && 2*B.front()>B.back());
 int common=m;for(int b:B)common=std::gcd(common,m+b);assert(common==1);
 std::set<int>sums,diffs;
 std::map<int,std::pair<int,int>> repr;
 for(int i=0;i<d;i++)for(int j=0;j<d;j++){
  sums.insert(A[i]+A[j]);diffs.insert(A[i]-A[j]);
  if(i<=j){int t=B[i]+B[j];auto pair=std::make_pair(i,j);
   auto it=repr.find(t);if(it==repr.end()||it->second<pair)repr[t]=pair;
  }
 }
 for(int i=0;i<d;i++)assert(repr.at(2*B[i])==std::make_pair(i,i));
 assert(d==512 && sums.size()==17576 && diffs.size()==15625 && R==12194);
 const ll inf=std::numeric_limits<ll>::max()/4;
 std::vector<ll>w(m,inf);w[0]=0;
 using Item=std::pair<ll,int>;std::priority_queue<Item,std::vector<Item>,std::greater<Item>>q;q.push({0,0});
 while(!q.empty()){
  auto [cost,s]=q.top();q.pop();if(cost!=w[s])continue;
  for(int b:B){int t=s+b;if(t>=m)t-=m;ll value=cost+m+b;
   if(value<w[t]){w[t]=value;q.push({value,t});}
  }
 }
 ll M=0,g=0;for(int s=0;s<m;s++){assert(w[s]<inf && w[s]%m==s);M=std::max(M,w[s]);g+=(w[s]-s)/m;}
 ll c=M-m+1,ell=c-g,W=e*ell-c;assert(c>=5LL*m);int rho=(m-c%m)%m;
 std::set<int>pool,P;P.insert(0);for(int b:B)P.insert(b);
 ll F=d,Gamma=0,V=0;for(int b:B){pool.insert(m-b);V+=rho+b>=m;}
 for(const auto&entry:repr){int sum=entry.first,i=entry.second.first,j=entry.second.second;
  assert(w[sum]==2LL*m+sum);
  if(i!=j){F+=2;pool.insert((B[i]-B[j]+m)%m);pool.insert((B[j]-B[i]+m)%m);}
 }
 for(int i=0;i<d;i++)for(int j=0;j<d;j++){
  auto pair=std::minmax(i,j);ll capacity=1+(i==j);
  if(repr.at(B[i]+B[j])!=std::make_pair(pair.first,pair.second))Gamma+=capacity;
  else if((B[i]+rho)%m+B[j]>=m)V+=capacity;
 }
 for(int r:pool)assert(!P.count(r));
 ll s=repr.size(),C=F-s,L=F-pool.size(),gap=L-C;
 assert(gap>=1440 && Gamma==227504 && Gamma+V-gap>=0);
 std::printf("{\"radix\":29,\"power\":3,\"A_size\":%d,\"A_max\":%d,\"shift\":%d,\"sum_count\":%zu,\"difference_count\":%zu,",d,R,T,sums.size(),diffs.size());
 std::printf("\"m\":%d,\"e\":%d,\"c\":%lld,\"g\":%lld,\"ell\":%lld,\"W\":%lld,\"rho\":%d,",m,e,c,g,ell,W,rho);
 std::printf("\"cut_size\":%lld,\"nonmaximal\":%d,\"maximal\":%lld,\"negative_starts\":%lld,\"exterior_images\":%zu,\"internal_aliases\":0,\"raw_carry\":0,",1LL+d+s,1+d,s,F,pool.size());
 std::printf("\"exterior_debt\":%lld,\"unused_starts\":%lld,\"staged_shortfall\":%lld,\"missing_capacity\":%lld,\"wrapped_capacity\":%lld,\"joint_margin\":%lld,\"apery\":[",L,C,gap,Gamma,V,Gamma+V-gap);
 for(int i=0;i<m;i++)std::printf("%s%lld",i?",":"",w[i]);std::puts("]}");
 return 0;
}
