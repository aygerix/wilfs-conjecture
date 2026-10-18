#pragma once
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <string>
#include <vector>
#include <gmpxx.h>

namespace ht4 {
using I=__int128_t; using U=__uint128_t; using ll=int64_t;
using V=std::array<ll,4>; using Cell=std::array<uint16_t,4>;
using Tile=std::vector<Cell>;
constexpr int LIMIT=256;
constexpr uint64_t P[2]={2305843009213693951ULL,2305843009213693921ULL};
static_assert(sizeof(Cell)==8 && UINT16_MAX>=LIMIT);
inline I absI(I x){return x<0?-x:x;}
inline I gcdI(I a,I b){a=absI(a);b=absI(b);while(b){I t=a%b;a=b;b=t;}return a;}
inline ll checked(I x){assert(x>=INT64_MIN && x<=INT64_MAX);return ll(x);}
inline ll sum(V x){return x[0]+x[1]+x[2]+x[3];}
inline I dot(V a,V b){I z=0;for(int i=0;i<4;i++)z+=I(a[i])*b[i];return z;}
inline int degree(Cell x){return x[0]+x[1]+x[2]+x[3];}
inline V cv(Cell x){return V{x[0],x[1],x[2],x[3]};}
inline V primitive(V x){ll g=0;for(ll a:x)g=std::gcd(g,a);assert(g);for(ll&a:x)a/=g;return x;}
inline V vertex(std::array<I,4>x,int m){I g=0;for(I a:x)g=gcdI(g,a);assert(g);I s=0;for(I&a:x){a/=g;s+=a;}assert(s);if(s<0)for(I&a:x)a=-a;V out;for(int i=0;i<4;i++){out[i]=checked(x[i]);assert(out[i]>=0 && out[i]<=6LL*m*m*m);}return out;}
inline I det3(I a,I b,I c,I d,I e,I f,I g,I h,I i){return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g);}
inline I det4(V a,V b,V c,V d){I z=0;for(int j=0;j<4;j++){int k[3],n=0;for(int i=0;i<4;i++)if(i!=j)k[n++]=i;I q=det3(b[k[0]],b[k[1]],b[k[2]],c[k[0]],c[k[1]],c[k[2]],d[k[0]],d[k[1]],d[k[2]]);z+=(j%2?-1:1)*I(a[j])*q;}return z;}
inline mpz_class z128(I x){bool neg=x<0;U u=neg?U(-x):U(x);uint64_t words[2]={uint64_t(u),uint64_t(u>>64)};mpz_class z;mpz_import(z.get_mpz_t(),2,-1,sizeof(uint64_t),0,0,words);return neg?-z:z;}
inline uint64_t residue(I x,uint64_t p){I r=x%I(p);return uint64_t(r<0?r+p:r);}
inline uint64_t mulmod(uint64_t a,uint64_t b,uint64_t p){return uint64_t(U(a)*b%p);}
inline uint64_t inverse(uint64_t a,uint64_t p){I t=0,u=1;uint64_t r=p,s=a;while(s){uint64_t q=r/s,rs=r%s;I v=t-I(q)*u;t=u;u=v;r=s;s=rs;}assert(r==1);return residue(t,p);}

struct Face{V n;std::vector<V> f;};
using Poly=std::vector<Face>;
inline bool noncollinear(const std::vector<V>&f){if(f.size()<3)return false;V a=f[0],b=f[1];ll sa=sum(a),sb=sum(b);std::array<I,4>u;int pivot=-1;for(int j=0;j<4;j++){u[j]=I(b[j])*sa-I(a[j])*sb;if(u[j] && pivot<0)pivot=j;}assert(pivot>=0);for(size_t k=2;k<f.size();k++){V c=f[k];ll sc=sum(c);std::array<I,4>v;for(int j=0;j<4;j++)v[j]=I(c[j])*sa-I(a[j])*sc;for(int j=0;j<4;j++)if(u[pivot]*v[j]!=v[pivot]*u[j])return true;}return false;}
inline std::vector<V> clip(const std::vector<V>&f,V n,int m){std::vector<I>d;I lo=0,hi=0;for(V x:f){I v=dot(x,n);d.push_back(v);lo=std::min(lo,v);hi=std::max(hi,v);}if(lo>=0)return f;std::vector<V>out;if(hi<=0){for(size_t i=0;i<f.size();i++)if(!d[i])out.push_back(f[i]);return out;}for(size_t i=0;i<f.size();i++){size_t j=(i+1)%f.size();if(d[i]>=0)out.push_back(f[i]);if((d[i]<0 && d[j]>0)||(d[i]>0 && d[j]<0)){std::array<I,4>x;for(int k=0;k<4;k++)x[k]=d[i]*f[j][k]-d[j]*f[i][k];out.push_back(vertex(x,m));}}out.erase(std::unique(out.begin(),out.end()),out.end());if(out.size()>1 && out.front()==out.back())out.pop_back();return out;}
inline Poly polytope(const std::vector<V>&cons,int m){std::array<V,4>ee;for(int a=0;a<4;a++){ee[a]={0,0,0,0};ee[a][a]=1;}Poly poly;for(int a=0;a<4;a++){Face f{ee[a],{}};for(int b=0;b<4;b++)if(a!=b)f.f.push_back(ee[b]);poly.push_back(f);}for(V n:cons){I lo=0,hi=0;for(auto&f:poly)for(V x:f.f){I v=dot(x,n);lo=std::min(lo,v);hi=std::max(hi,v);}if(lo>=0)continue;assert(hi>0);Poly next;std::map<V,std::set<V>>graph;for(auto&f:poly){auto q=clip(f.f,n,m);if(!noncollinear(q))continue;next.push_back({f.n,q});for(size_t i=0;i<q.size();i++){V a=q[i],b=q[(i+1)%q.size()];if(dot(a,n)==0 && dot(b,n)==0){graph[a].insert(b);graph[b].insert(a);}}}assert(graph.size()>=3);for(auto&[x,ns]:graph)assert(ns.size()==2);V start=graph.begin()->first,cur=start,prev{};bool have=false;std::vector<V>cap{start};for(;;){V nxt=*graph[cur].begin();if(have && nxt==prev)nxt=*graph[cur].rbegin();if(nxt==start)break;assert(std::find(cap.begin(),cap.end(),nxt)==cap.end());cap.push_back(nxt);prev=cur;cur=nxt;have=true;}assert(cap.size()==graph.size());next.push_back({n,cap});poly.swap(next);}return poly;}
inline V interior(const std::vector<V>&points){V p{};for(V x:points)for(int a=0;a<4;a++)p[a]=checked(I(p[a])+x[a]);return primitive(p);}
inline std::vector<V> vertices(const Poly&poly){std::set<V>s;for(auto&f:poly)s.insert(f.f.begin(),f.f.end());return {s.begin(),s.end()};}

struct Key{ll p=0,q=0;int deg=0;Cell x{};};
inline bool operator<(const Key&a,const Key&b){if(a.p!=b.p)return a.p<b.p;if(a.q!=b.q)return a.q<b.q;if(a.deg!=b.deg)return a.deg<b.deg;return a.x<b.x;}
struct Heap{Key k;int g;bool operator<(const Heap&b)const{return b.k<k;}};
struct Lattice{
 int m;V r;
 int cls(Cell x)const{ll z=0;for(int a=0;a<4;a++)z+=r[a]*x[a];return z%m;}
 bool in(const Tile&T,Cell x)const{return T[cls(x)]==x;}
 Tile tile(V p,V q={})const{for(ll x:p)assert(x>0);std::vector<Key>best(m);std::vector<char>have(m),done(m);std::priority_queue<Heap>heap;Key z;best[0]=z;have[0]=1;heap.push({z,0});Tile T(m);int found=0;while(!heap.empty()){Heap item=heap.top();heap.pop();int g=item.g;if(done[g])continue;done[g]=1;found++;T[g]=item.k.x;assert(item.k.deg<m);for(int a=0;a<4;a++){int h=(g+r[a])%m;if(done[h])continue;Key k=item.k;k.p=checked(I(k.p)+p[a]);k.q=checked(I(k.q)+q[a]);k.deg++;assert(k.x[a]<UINT16_MAX);k.x[a]++;if(!have[h] || k<best[h]){best[h]=k;have[h]=1;heap.push({k,h});}}}assert(found==m);return T;}
 void check(const Tile&T)const{assert(int(T.size())==m);for(int g=0;g<m;g++){Cell x=T[g];assert(cls(x)==g && degree(x)<m);for(int a=0;a<4;a++){assert(x[a]<m);if(x[a]){Cell y=x;y[a]--;assert(in(T,y));}}}}
 std::vector<V> constraints(const Tile&T)const{std::set<V>out;for(Cell x:T)for(int a=0;a<4;a++){Cell q=x;assert(q[a]<UINT16_MAX);q[a]++;bool skip=false;for(int b=0;b<a;b++)if(q[b])skip=true;if(skip || in(T,q))continue;bool good=true;for(int b=0;b<4;b++)if(q[b]){Cell y=q;y[b]--;if(!in(T,y)){good=false;break;}}if(!good)continue;Cell y=T[cls(q)];V v;for(int b=0;b<4;b++)v[b]=int(q[b])-int(y[b]);out.insert(primitive(v));}return {out.begin(),out.end()};}
 bool eligible(const Tile&T)const{std::set<ll>s(r.begin(),r.end());if(s.size()!=4 || *s.begin()==0)return false;for(int a=0;a<4;a++){Cell x{};x[a]=1;if(!in(T,x))return false;}return true;}
};
struct Metric{ll H=0,R=0,N=0;int t=0,Z=0;bool non_two=true;std::vector<int>height;};
inline Metric metric(const Lattice&L,const Tile&T){
 int m=L.m;Metric z;z.height.assign(m,0);
 std::vector<std::array<int,4>>top(m);std::vector<int>order(m);
 std::iota(order.begin(),order.end(),0);
 std::sort(order.begin(),order.end(),[&](int a,int b){int x=degree(T[a]),y=degree(T[b]);return x==y?a<b:x>y;});
 std::vector<int>maxima;
 for(int g:order){
  int h=0;
  for(int a=0;a<4;a++){Cell y=T[g];y[a]++;int k=L.cls(y);bool inside=T[k]==y;if(inside)h=std::max(h,z.height[k]+1);top[g][a]=inside?top[k][a]:g;}
  z.height[g]=h;if(!h)maxima.push_back(4+degree(T[g]));bool zero=true;
  for(int a=0;a<4;a++){z.H+=z.height[top[g][a]];zero&=z.height[top[g][a]]==0;}
  z.Z+=zero;
 }
 std::sort(maxima.rbegin(),maxima.rend());z.t=maxima.size();
 for(int i=0;i<z.t;i++)z.R+=ll(i)*maxima[i];
 z.N=(m+1)*z.H+z.R;
 for(int a=0;a<4;a++)for(int b=a+1;b<4;b++){
  Cell x{};x[a]=x[b]=1;
  if(!L.in(T,x)){
   z.non_two=false;ll arm_height=0;
   for(int g=0;g<m;g++)if(T[g][a] || T[g][b])arm_height+=z.height[g];
   assert(z.H>=arm_height);
  }
 }
 // Independently derived universal inequalities, checked in exact integers.
 ll S=std::accumulate(maxima.begin(),maxima.end(),0LL);assert(z.H>=4*m-S);
 assert(z.R>=(z.t>=4?3LL*z.t*z.t-7*z.t+10:5LL*z.t*(z.t-1)/2));
 V axes{};for(Cell x:T)for(int a=0;a<4;a++)axes[a]=std::max(axes[a],ll(x[a])+1);
 for(int i=0;i<4;i++){
  I den=1;for(int b=0;b<4;b++)if(b!=i)den*=axes[b];
  I reciprocal_sum=0;for(int b=0;b<4;b++)if(b!=i)reciprocal_sum+=den/axes[b];
  assert(2*I(z.H)*den>=I(axes[i])*axes[i]*reciprocal_sum-3*I(axes[i])*den);
 }
 return z;
}
template<class T>inline void arr(std::ostream&o,const std::array<T,4>&x){o<<'[';for(int a=0;a<4;a++){if(a)o<<',';o<<x[a];}o<<']';}
inline std::string tile_json(Tile T){std::sort(T.begin(),T.end());std::ostringstream o;o<<'[';for(size_t i=0;i<T.size();i++){if(i)o<<',';arr(o,T[i]);}o<<']';return o.str();}
inline std::string ratio(ll n,ll d){ll g=std::gcd(n,d);return std::to_string(n/g)+(d/g==1?"":"/"+std::to_string(d/g));}
inline std::string structure(const Lattice&L,const Tile&T,const Metric&z){std::ostringstream o;o<<"{\"r\":";arr(o,L.r);o<<",\"H\":"<<z.H<<",\"R\":"<<z.R<<",\"t\":"<<z.t<<",\"zero_top_cells\":"<<z.Z<<",\"hcr\":\""<<ratio(z.N,3LL*L.m*(L.m-1)/2)<<"\",\"tile\":"<<tile_json(T)<<",\"levels\":[";std::map<int,int>levels;for(Cell x:T)levels[degree(x)]++;bool first=true;for(auto[k,v]:levels){if(!first)o<<',';first=false;o<<'['<<k<<','<<v<<']';}o<<"],\"maximal\":[";first=true;for(int g=0;g<L.m;g++)if(!z.height[g]){if(!first)o<<',';first=false;arr(o,T[g]);}o<<"],\"two_face_pairs\":[";first=true;for(int a=0;a<4;a++)for(int b=a+1;b<4;b++){Cell x{};x[a]=x[b]=1;if(!L.in(T,x)){if(!first)o<<',';first=false;o<<'['<<a<<','<<b<<']';}}o<<"],\"corners\":[";first=true;for(Cell x:T)for(int a=0;a<4;a++){Cell q=x;q[a]++;bool skip=false;for(int b=0;b<a;b++)if(q[b])skip=true;if(skip || L.in(T,q))continue;bool good=true;for(int b=0;b<4;b++)if(q[b]){Cell y=q;y[b]--;if(!L.in(T,y))good=false;}if(good){if(!first)o<<',';first=false;o<<"{\"q\":";arr(o,q);o<<",\"y\":";arr(o,T[L.cls(q)]);o<<'}';}}o<<"]}";return o.str();}
struct Aggregate{
 int m;ll raw=0,eligible=0,non_two=0,Hmin=INT64_MAX,Nmin=INT64_MAX,Nmin_non_two=INT64_MAX,Zexcess=INT64_MIN,htfail=0;
 std::map<std::pair<ll,int>,ll>joint;std::map<int,ll>by_t;
 std::vector<std::string>Htiles,Ntiles,failures;std::string Nnon_two_tile,Ztile;
 explicit Aggregate(int m):m(m){}
 void add(const Lattice&L,const Tile&T){raw++;if(!L.eligible(T))return;eligible++;Metric z=metric(L,T);ll B=3LL*m*(m-1)/2;non_two+=z.non_two;htfail+=(m+1)*z.H<B;if(z.H<2*m)joint[{z.H,z.t}]++;auto it=by_t.find(z.t);if(it==by_t.end() || z.H<it->second)by_t[z.t]=z.H;std::string s;auto get=[&]()->const std::string&{if(s.empty())s=structure(L,T,z);return s;};if(z.H<Hmin){Hmin=z.H;Htiles.clear();}if(z.H==Hmin)Htiles.push_back(get());if(z.N<Nmin){Nmin=z.N;Ntiles.clear();}if(z.N==Nmin)Ntiles.push_back(get());if(z.non_two && z.N<Nmin_non_two){Nmin_non_two=z.N;Nnon_two_tile=get();}if(z.N<B)failures.push_back(get());if(z.Z-z.t>Zexcess){Zexcess=z.Z-z.t;Ztile=get();}}
 void merge(const Aggregate&b){assert(m==b.m);raw+=b.raw;eligible+=b.eligible;non_two+=b.non_two;htfail+=b.htfail;for(auto[k,n]:b.joint)joint[k]+=n;for(auto[t,h]:b.by_t){auto it=by_t.find(t);if(it==by_t.end() || h<it->second)by_t[t]=h;}if(b.Hmin<Hmin){Hmin=b.Hmin;Htiles.clear();}if(b.Hmin==Hmin)Htiles.insert(Htiles.end(),b.Htiles.begin(),b.Htiles.end());if(b.Nmin<Nmin){Nmin=b.Nmin;Ntiles.clear();}if(b.Nmin==Nmin)Ntiles.insert(Ntiles.end(),b.Ntiles.begin(),b.Ntiles.end());if(b.Nmin_non_two<Nmin_non_two){Nmin_non_two=b.Nmin_non_two;Nnon_two_tile=b.Nnon_two_tile;}if(b.Zexcess>Zexcess){Zexcess=b.Zexcess;Ztile=b.Ztile;}failures.insert(failures.end(),b.failures.begin(),b.failures.end());}
 std::string json()const{std::ostringstream o;auto strings=[&](const std::vector<std::string>&v){o<<'[';for(size_t i=0;i<v.size();i++){if(i)o<<',';o<<v[i];}o<<']';};o<<"{\"m\":"<<m<<",\"raw_tiles\":"<<raw<<",\"e5_tiles\":"<<eligible<<",\"non_two_face\":"<<non_two<<",\"HT4_failures\":"<<htfail<<",\"min_H\":"<<(eligible?Hmin:-1)<<",\"min_H_over_m\":\""<<(eligible?ratio(Hmin,m):"None")<<"\",\"min_HCR\":\""<<(eligible?ratio(Nmin,3LL*m*(m-1)/2):"None")<<"\",\"min_HCR_non_two_face\":\""<<(non_two?ratio(Nmin_non_two,3LL*m*(m-1)/2):"None")<<"\",\"min_H_tiles\":";strings(Htiles);o<<",\"min_HCR_tiles\":";strings(Ntiles);o<<",\"min_HCR_non_two_face_tile\":"<<(Nnon_two_tile.empty()?"null":Nnon_two_tile)<<",\"HCR_failures\":";strings(failures);o<<",\"joint_H_t_below_2m\":[";bool first=true;for(auto[k,n]:joint){if(!first)o<<',';first=false;o<<'['<<k.first<<','<<k.second<<','<<n<<']';}o<<"],\"min_H_by_t\":[";first=true;for(auto[t,h]:by_t){if(!first)o<<',';first=false;o<<'['<<t<<','<<h<<']';}o<<"],\"max_zero_top_minus_t\":"<<Zexcess<<",\"zero_top_extremizer\":"<<(Ztile.empty()?"null":Ztile)<<'}';return o.str();}
};
}
