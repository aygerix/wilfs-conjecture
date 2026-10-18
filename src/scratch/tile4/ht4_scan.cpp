// Build ON FEJER: g++ -O3 -std=c++17 -pthread ht4_scan.cpp -lgmpxx -lgmp -o ht4_scan
// Geometry: int64 primitive vertices, signed 128-bit intermediates, m <= 256.
// Completeness: exact reciprocal facet matching AND two modular volume sums.
// --exact additionally checks the unconditional rational volume sum with GMP.
#include "ht4_core.hpp"
#include <atomic>
#include <chrono>
#include <cstring>
#include <fstream>
#include <mutex>
#include <random>
#include <thread>
#include <unordered_map>
#include <unistd.h>
using namespace ht4;
using Clock=std::chrono::steady_clock;

static std::string key(const Tile&T){return std::string(reinterpret_cast<const char*>(T.data()),T.size()*sizeof(Cell));}
struct Pending{size_t src;V n;std::vector<V>face;};
struct Fan{
 Lattice L;bool exact,dump;Aggregate aggregate;size_t cones=0,facets=0;
 std::array<uint64_t,2>vol{};mpq_class rational=0;
 std::vector<std::string>dump_tiles;
 explicit Fan(Lattice l,bool x,bool d):L(l),exact(x),dump(d),aggregate(l.m){}
 void run(){
  std::vector<Tile>tiles;std::vector<char>processed;std::vector<size_t>todo;
  std::unordered_map<std::string,size_t>ids;
  std::map<std::pair<size_t,size_t>,Pending>unmatched;
  std::unordered_map<ll,std::array<uint64_t,2>>invcache;
  auto insert=[&](const Tile&T){auto[it,yes]=ids.emplace(key(T),tiles.size());if(yes){tiles.push_back(T);processed.push_back(0);todo.push_back(it->second);}return it->second;};
  auto invs=[&](ll s){auto it=invcache.find(s);if(it!=invcache.end())return it->second;assert(s>0 && uint64_t(s)<P[1]);std::array<uint64_t,2>v{inverse(s,P[0]),inverse(s,P[1])};invcache.emplace(s,v);return v;};
  insert(L.tile({1,1,1,1}));
  while(!todo.empty()){
   size_t id=todo.back();todo.pop_back();assert(!processed[id]);processed[id]=1;
   Tile T=tiles[id];L.check(T);auto cons=L.constraints(T);Poly poly=polytope(cons,L.m);auto pts=vertices(poly);assert(pts.size()>=4);V center=interior(pts);for(ll a:center)assert(a>0);for(V n:cons)assert(dot(n,center)>0);
   cones++;aggregate.add(L,T);if(dump)dump_tiles.push_back(tile_json(T));
   V ref=pts[0];auto ir=invs(sum(ref));
   for(const Face&f:poly){
    for(size_t i=1;i+1<f.f.size();i++){
     V a=f.f[0],b=f.f[i],c=f.f[i+1];I n=absI(det4(ref,a,b,c));if(!n)continue;
     auto ia=invs(sum(a)),ib=invs(sum(b)),ic=invs(sum(c));
     for(int k=0;k<2;k++){uint64_t v=residue(n,P[k]);v=mulmod(v,ir[k],P[k]);v=mulmod(v,ia[k],P[k]);v=mulmod(v,ib[k],P[k]);v=mulmod(v,ic[k],P[k]);vol[k]=(vol[k]+v)%P[k];}
     if(exact){mpz_class den=mpz_class(sum(ref))*mpz_class(sum(a))*mpz_class(sum(b))*mpz_class(sum(c));mpq_class q(z128(n),den);q.canonicalize();rational+=q;}
    }
    V p=interior(f.f);bool boundary=false;for(ll a:p)if(!a)boundary=true;
    if(boundary){bool entire=false;for(int a=0;a<4;a++){bool zero=true;for(V v:f.f)zero&=v[a]==0;entire|=zero;}assert(entire);continue;}
    V neg;for(int a=0;a<4;a++)neg[a]=-f.n[a];Tile next=L.tile(p,neg);assert(next!=T);auto cons2=L.constraints(next);bool opposite=false;
    for(V v:cons2){I d=dot(v,p);assert(d>=0);if(!d)assert(dot(v,neg)>0);if(v==primitive(neg))opposite=true;for(V x:f.f)assert(dot(v,x)>=0);}assert(opposite);
    size_t j=insert(next);facets++;auto pair=std::minmax(id,j);std::pair<size_t,size_t>edge{pair.first,pair.second};std::vector<V>face=f.f;std::sort(face.begin(),face.end());auto it=unmatched.find(edge);
    if(it==unmatched.end())unmatched.emplace(edge,Pending{id,primitive(f.n),face});
    else{assert(it->second.src==j);V n=it->second.n;for(ll&a:n)a=-a;assert(n==primitive(f.n) && it->second.face==face);unmatched.erase(it);}
   }
  }
  assert(cones==tiles.size() && unmatched.empty());assert(vol[0]==1 && vol[1]==1);if(exact)assert(rational==1);
 }
 std::string json()const{std::ostringstream o;o<<"{\"m\":"<<L.m<<",\"r\":";arr(o,L.r);o<<",\"cones\":"<<cones<<",\"internal_directed_facets\":"<<facets<<",\"mod_volume\":["<<vol[0]<<','<<vol[1]<<"],\"matched_facets\":true,\"exact_volume\":"<<(exact?"\"1\"":"null")<<",\"metrics\":"<<aggregate.json();if(dump){o<<",\"tiles\":[";for(size_t i=0;i<dump_tiles.size();i++){if(i)o<<',';o<<dump_tiles[i];}o<<']';}o<<'}';return o.str();}
};

static std::vector<V> lattices(int m,bool all){
 std::vector<int>units;for(int u=1;u<m;u++)if(std::gcd(u,m)==1)units.push_back(u);
 std::vector<V>out;
 for(int a=all?0:1;a<m;a++)for(int b=all?a:a+1;b<m;b++)for(int c=all?b:b+1;c<m;c++)for(int d=all?c:c+1;d<m;d++){
  if(std::gcd(std::gcd(std::gcd(std::gcd(m,a),b),c),d)!=1)continue;
  V r{a,b,c,d};bool canonical=true;for(int u:units){V q;for(int j=0;j<4;j++)q[j]=u*r[j]%m;std::sort(q.begin(),q.end());if(q<r){canonical=false;break;}}if(canonical)out.push_back(r);
 }
 return out;
}
static uint64_t power(uint64_t a,uint64_t n,uint64_t p){uint64_t y=1;while(n){if(n&1)y=mulmod(y,a,p);a=mulmod(a,a,p);n>>=1;}return y;}
static bool prime(uint64_t n){if(n<2)return false;for(uint64_t p:{2,3,5,7,11,13,17,19,23,29,31,37}){if(n==p)return true;if(n%p==0)return false;}uint64_t d=n-1,s=0;while(!(d&1)){d>>=1;s++;}for(uint64_t a:{2ULL,325ULL,9375ULL,28178ULL,450775ULL,9780504ULL,1795265022ULL}){a%=n;if(!a)continue;uint64_t x=power(a,d,n);if(x==1||x==n-1)continue;bool good=false;for(uint64_t j=1;j<s;j++){x=mulmod(x,x,n);if(x==n-1){good=true;break;}}if(!good)return false;}return true;}
static void metrics_server(){
 uint32_t m;while(std::cin.read(reinterpret_cast<char*>(&m),4)){
  assert(m>=5 && m<=LIMIT);Aggregate total(m);uint64_t nl=0;
  for(;;){uint32_t n;std::cin.read(reinterpret_cast<char*>(&n),4);assert(std::cin);if(!n)break;V r;for(ll&a:r){uint32_t x;std::cin.read(reinterpret_cast<char*>(&x),4);a=x;}assert(std::cin);Lattice L{int(m),r};nl++;
   for(uint32_t i=0;i<n;i++){Tile points(m),T(m);std::cin.read(reinterpret_cast<char*>(points.data()),m*sizeof(Cell));assert(std::cin);std::vector<char>have(m);for(Cell x:points){int g=L.cls(x);assert(!have[g]);have[g]=1;T[g]=x;}L.check(T);total.add(L,T);}
  }
  std::cout<<"{\"lattices\":"<<nl<<",\"metrics\":"<<total.json()<<"}"<<std::endl;
 }
 assert(std::cin.eof());
}
static void sample_tiles(int m,int draws,uint64_t seed){
 assert(m>=5 && m<=LIMIT && draws>0);std::mt19937_64 rng(seed);Aggregate total(m);
 for(int i=0;i<draws;i++){
  V r;for(;;){for(ll&a:r)a=1+rng()%(m-1);std::set<ll>s(r.begin(),r.end());if(s.size()==4 && std::gcd(std::gcd(std::gcd(std::gcd(ll(m),r[0]),r[1]),r[2]),r[3])==1)break;}
  V secondary;for(ll&a:secondary)a=ll(rng()%21)-10;
  Lattice L{m,r};Tile T=L.tile({1,1,1,1},secondary);L.check(T);total.add(L,T);
 }
 std::cout<<"{\"complete_enumeration\":false,\"m\":"<<m<<",\"draws\":"<<draws<<",\"seed\":"<<seed<<",\"metrics\":"<<total.json()<<"}"<<std::endl;
}
int main(int argc,char**argv){
 char host[256];assert(!gethostname(host,sizeof(host)));assert(std::string(host).rfind("fejer",0)==0);assert(prime(P[0]) && prime(P[1]));
 if(argc==2 && std::string(argv[1])=="--metrics"){metrics_server();return 0;}
 if(argc==5 && std::string(argv[1])=="--sample"){sample_tiles(std::stoi(argv[2]),std::stoi(argv[3]),std::stoull(argv[4]));return 0;}
 if(argc<2){std::cerr<<"usage: ht4_scan m [--all] [--dump] [--exact] [--threads N] [--out PREFIX] [--lattice a b c d]\n";return 1;}
 int m=std::stoi(argv[1]),threads=1;assert(m>=5 && m<=LIMIT);bool all=false,dump=false,exact=false,single=false;V r{};std::string prefix;
 for(int i=2;i<argc;i++){std::string a=argv[i];if(a=="--all")all=true;else if(a=="--dump")dump=true;else if(a=="--exact")exact=true;else if(a=="--threads")threads=std::stoi(argv[++i]);else if(a=="--out")prefix=argv[++i];else if(a=="--lattice"){single=true;for(ll&x:r)x=std::stoi(argv[++i]);}else{std::cerr<<"unknown option "<<a<<'\n';return 2;}}
 assert(threads>=1 && threads<=8);auto start=Clock::now();auto lat=single?std::vector<V>{r}:lattices(m,all);std::atomic<size_t>index{0};std::mutex output;Aggregate total(m);uint64_t cones=0,facets=0;std::ofstream lattice_file;if(!prefix.empty())lattice_file.open(prefix+".lattices.jsonl");
 auto work=[&](){for(;;){size_t i=index.fetch_add(1);if(i>=lat.size())return;Fan f(Lattice{m,lat[i]},exact,dump);f.run();std::lock_guard<std::mutex>lock(output);if(dump)std::cout<<f.json()<<std::endl;if(lattice_file){lattice_file<<"{\"m\":"<<m<<",\"r\":";arr(lattice_file,f.L.r);lattice_file<<",\"cones\":"<<f.cones<<",\"internal_directed_facets\":"<<f.facets<<",\"matched_facets\":true,\"mod_volume\":[1,1],\"exact_volume\":"<<(exact?"\"1\"":"null")<<"}\n";}total.merge(f.aggregate);cones+=f.cones;facets+=f.facets;}};
 std::vector<std::thread>pool;for(int i=0;i<threads;i++)pool.emplace_back(work);for(auto&t:pool)t.join();
 auto elapsed=std::chrono::duration<double>(Clock::now()-start).count();std::ostringstream o;o<<"{\"m\":"<<m<<",\"domain\":\""<<(all?"all":"distinct-nonzero")<<"\",\"lattices\":"<<lat.size()<<",\"cones\":"<<cones<<",\"internal_directed_facets\":"<<facets<<",\"matched_facets\":true,\"mod_primes\":["<<P[0]<<','<<P[1]<<"],\"mod_volume_defects\":0,\"exact_volume\":"<<(exact?"true":"false")<<",\"threads\":"<<threads<<",\"seconds\":"<<elapsed<<",\"metrics\":"<<total.json()<<'}';
 if(!prefix.empty()){std::ofstream f(prefix+".json");f<<o.str()<<'\n';}if(!dump)std::cout<<o.str()<<std::endl;else std::cerr<<"SUMMARY "<<o.str()<<std::endl;
}
