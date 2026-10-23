#include "apery.hpp"
#ifdef WILF_CUDA
#include "gpu.hpp"
#endif
#include <atomic>
#include <chrono>
#include <iostream>
#include <limits>
#include <mutex>
#include <thread>
#include <unordered_set>

using namespace wilf;
using Clock = std::chrono::steady_clock;
double gpu_context_initialization_ms = 0;
double elapsed(Clock::time_point start) {
    return std::chrono::duration<double, std::milli>(Clock::now() - start).count();
}
struct Random {
    std::uint64_t state;
    std::uint64_t next() {
        std::uint64_t z = (state += UINT64_C(0x9e3779b97f4a7c15));
        z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
        return z ^ (z >> 31);
    }
};
void require(bool value, const std::string& message) {
    if (!value) throw std::runtime_error(message);
}
template<class Function> void safe_parallel(int count, int threads, Function function) {
    std::atomic<int> next{0}; std::atomic<bool> failed{false};
    std::exception_ptr error; std::mutex error_mutex;
    auto worker=[&] {
        try {for(int i; !failed && (i=next.fetch_add(1))<count;)function(i);}
        catch(...) {std::lock_guard<std::mutex> lock(error_mutex);if(!error)error=std::current_exception();failed=true;}
    };
    std::vector<std::thread> pool;
    try {for(int i=1;i<threads;++i)pool.emplace_back(worker);}
    catch(...) {failed=true;for(auto& t:pool)t.join();throw;}
    worker();for(auto& t:pool)t.join();if(error)std::rethrow_exception(error);
}
template<class T> void print_array(const std::vector<T>& values) {
    std::cout << '[';
    for (size_t i = 0; i < values.size(); ++i) std::cout << (i ? "," : "") << values[i];
    std::cout << ']';
}
void basic_equal(const Basic& a, const Basic& b) {
    require(a.m == b.m && a.e == b.e && a.top == b.top && a.finite == b.finite &&
            a.c == b.c && a.g == b.g && a.W == b.W, "GPU/CPU invariants disagree");
}
void emit_case(const char* kind, int m, const std::vector<i64>& G,
               const std::vector<i64>& w, const Support& score) {
    const Basic& b = score.basic;
    const i64 q = (b.c + m - 1) / m;
    std::vector<i64> mu(m);
    std::vector<int> parent(m, -1), generator(m, -1);
    for (int s = 0; s < m; ++s) {
        mu[s] = std::max(i64(0), (b.c - w[s] + m - 1) / m);
        if (!s) continue;
        for (size_t j = 0; j < G.size(); ++j) {
            const int p = (s - static_cast<int>(G[j] % m) + m) % m;
            if (w[p] + G[j] == w[s]) { parent[s] = p; generator[s] = static_cast<int>(j); break; }
        }
        require(parent[s] >= 0, "missing exported predecessor");
    }
    std::cout << "{\"kind\":\"" << kind << "\",\"m\":" << m << ",\"e\":" << b.e
              << ",\"c\":" << b.c << ",\"g\":" << b.g << ",\"W\":" << b.W
              << ",\"q\":" << q << ",\"rho\":" << q * m - b.c << ",\"r\":" << b.top
              << ",\"generators\":"; print_array(score.minimal);
    std::cout << ",\"input_generators\":"; print_array(G);
    std::cout << ",\"w\":"; print_array(w);
    std::cout << ",\"mu\":"; print_array(mu);
    std::cout << ",\"primitive_residues\":"; print_array(score.residues);
    std::cout << ",\"canonical_words\":"; print_array(score.words);
    std::cout << ",\"gamma\":"; print_array(score.gamma);
    std::cout << ",\"predecessor_residue\":"; print_array(parent);
    std::cout << ",\"predecessor_generator_index\":"; print_array(generator);
    std::cout << ",\"Dep\":" << score.Dep << ",\"kappa\":" << score.kappa
              << ",\"N\":" << score.N << ",\"Q\":" << score.Q << ",\"R\":" << score.R
              << ",\"Qmin\":" << score.Qmin << ",\"minimum_top_phase\":" << score.min_phase
              << ",\"tile_hash\":\"" << score.tile_hash << "\"}\n" << std::flush;
}
void self_test(int count) {
    Random rng{UINT64_C(0x57494c465343414e)};
    std::vector<std::pair<int, std::vector<i64>>> cases = {
        {1, {}}, {6, {9, 20}}, {64, {96, 128, 129}}, {63, {84, 126, 128}},
        {19, {39, 41, 50, 52, 53}}, {13, {15, 17, 19}}, {13, {15, 47}},
        {6, {9, 20, 29, 18}}, {17, {10000000019LL, 10000000033LL}},
        {8, {12, 20, 28}}, {5, {7, 14, 21}}
    };
    for (int i = 0; i < count; ++i) {
        const int m = 2 + rng.next() % 1023, k = 1 + rng.next() % 12;
        std::vector<i64> G(k);
        for (auto& p : G) {
            p = i64(m) * (1 + rng.next() % 20) + rng.next() % m;
            if (p == m) p += m;
        }
        cases.emplace_back(m, std::move(G));
    }
    size_t stages = 0, gpu_stages = 0;
    for (const auto& test : cases) {
        const int m = test.first;
        std::vector<i64> prefix;
        for (size_t stage = 0; stage <= test.second.size(); ++stage) {
            if (stage) prefix.push_back(test.second[stage - 1]);
            auto scan = scan_cpu(m, prefix), heap = dijkstra_heap(m, prefix);
            require(scan == heap, "CPU cyclic scan differs from heap Dijkstra");
            std::string error;
            require(certify(m, prefix, scan, &error), "distance certificate: " + error);
            int common = m;
            for (i64 p : prefix) common = std::gcd(common, static_cast<int>(p % m));
            for (int s = 0; s < m; ++s)
                require((scan[s] != INF) == (s % common == 0), "reachable gcd pattern differs");
            Basic basic = invariants(m, prefix, scan);
#ifdef WILF_CUDA
            std::vector<i64> gpu; std::vector<Basic> stats; GpuTiming timing;
            gpu_scan_batch(m, static_cast<int>(prefix.size()), 1, prefix, gpu, stats, timing);
            require(gpu == scan, "GPU cyclic scan differs at a generator prefix");
            basic_equal(basic, stats[0]); ++gpu_stages;
#endif
            if (m > 1 && basic.finite) {
                auto corrupt = scan; corrupt[1] += m;
                require(!certify(m, prefix, corrupt), "corrupt certificate accepted");
            }
            ++stages;
        }
    }
    // Algorithm-only G<m case: do not call the multiplicity-based statistics.
    require(scan_cpu(9, {4, 7}) == dijkstra_heap(9, {4, 7}), "G<m scan case failed");
    for (auto data : std::vector<std::pair<int, std::vector<i64>>>{
             {19, {39,41,50,52,53}}, {13,{15,17,19}}, {6,{7,11}}, {5,{7,14,21}}}) {
        const auto w = scan_cpu(data.first, data.second);
        const auto s = support(data.first, data.second, w);
        require(s.basic.W == s.Q + s.R && s.R >= 0, "support decomposition failed");
        if (data.first == 19) require(s.Q == 5 && s.Dep == 4 && s.basic.W == 32, "OLD19 changed");
        if (data.first == 13) require(s.Q == 15 && s.Dep == 14 && s.basic.W == 48, "advisor k2 changed");
    }
    std::cout << "{\"kind\":\"self_test\",\"lists\":" << cases.size()
              << ",\"prefixes_checked\":" << stages << ",\"gpu_prefixes_checked\":" << gpu_stages
              << ",\"independent_heap\":true,\"corrupt_certificate_rejected\":true}\n";
}
int benchmark(int batch, std::uint64_t seed, int threads, int m, int k,
              const std::vector<i64>& anchor = {}) {
    require(m >= 2 && m <= 1024 && batch > 0 && batch <= 65536 && threads >= 1 && threads <= 128 && k >= 1 && k <= 64,
            "invalid benchmark shape");
    Random rng{seed};
    const auto generation_start=Clock::now();
    std::vector<i64> flat(static_cast<size_t>(batch) * k);
    for(int i=0;i<batch;++i) {
        const int mode=anchor.empty()?3:i%4;
        int unit=1;
        if(mode==1)do {unit=1+rng.next()%(m-1);} while(std::gcd(unit,m)!=1 || (m>2 && unit==1));
        const int changed=rng.next()%k,other=rng.next()%k;
        for(int j=0;j<k;++j) {
            i64 p;
            if(mode==3) {
                const i64 height=1+rng.next()%12;
                const int delta=rng.next()%m;
                p=i64(m)*height+delta;
            }
            else {
                require(anchor[j]>m,"mutation anchor must exceed modulus");
                const int old=anchor[j]%m;
                int delta=old;
                i64 height=anchor[j]/m;
                if(mode==1)delta=(unit*old)%m;
                else if(j==changed || (mode==2 && j==other)) {
                    do {delta=rng.next()%m;} while(delta==old);
                    if(mode==2)height=1+rng.next()%12;
                }
                p=m*height+delta;
            }
            if(p==m)p+=m;
            flat[static_cast<size_t>(i)*k+j]=p;
        }
    }
    const double generation_ms=elapsed(generation_start);
    std::vector<i64> serial(static_cast<size_t>(batch) * m), parallel(serial.size());
    auto scan_batch = [&](std::vector<i64>& out, int workers) {
        const auto start = Clock::now(); std::atomic<int> next{0};
        auto worker = [&] {
            for (int i; (i = next.fetch_add(1)) < batch;) {
                std::vector<i64> G(flat.begin() + static_cast<size_t>(i)*k, flat.begin() + static_cast<size_t>(i+1)*k);
                const auto w = scan_cpu(m, G);
                std::copy(w.begin(), w.end(), out.begin() + static_cast<size_t>(i)*m);
            }
        };
        std::vector<std::thread> pool;
        for (int i = 1; i < workers; ++i) pool.emplace_back(worker);
        worker(); for (auto& t : pool) t.join();
        return elapsed(start);
    };
    const double serial_ms = scan_batch(serial, 1), parallel_ms = scan_batch(parallel, threads);
    require(serial == parallel, "parallel CPU scan differs");
    const int independent_count = std::min(batch, 256);
    const auto heap_start = Clock::now();
    for (int i = 0; i < independent_count; ++i) {
        const std::vector<i64> G(flat.begin()+static_cast<size_t>(i)*k,flat.begin()+static_cast<size_t>(i+1)*k);
        const auto w = dijkstra_heap(m,G);
        require(std::equal(w.begin(),w.end(),serial.begin()+static_cast<size_t>(i)*m), "heap benchmark differs");
    }
    const double heap_ms = elapsed(heap_start);
#ifdef WILF_CUDA
    double gpu_wall = 0; float gpu_kernel = 0;
    std::vector<Basic> gpu_stats;
    std::vector<i64> gpu; GpuTiming timing;
    gpu_scan_batch(m,k,batch,flat,gpu,gpu_stats,timing);
    require(gpu == serial, "full GPU batch differs from CPU scan");
    gpu_wall=timing.wall_ms;gpu_kernel=timing.kernel_ms;
#endif
    int finite = 0, eligible = 0, bad_phases = 0;
    int shape_excluded = 0, residue_excluded = 0, flat_excluded = 0, resistant = 0;
    i64 minimum_Q=std::numeric_limits<i64>::max(),minimum_phase=minimum_Q;
    std::vector<i64> best_G,best_w,phase_G,phase_w;
    Support best,phase_best;
    std::unordered_set<std::uint64_t> tiles,profiles;
    const auto analysis_start=Clock::now();
    for(int i=0;i<batch;++i) {
        const std::vector<i64> G(flat.begin()+static_cast<size_t>(i)*k,flat.begin()+static_cast<size_t>(i+1)*k);
        const std::vector<i64> w(serial.begin()+static_cast<size_t>(i)*m,serial.begin()+static_cast<size_t>(i+1)*m);
        const Basic b=invariants(m,G,w); // Includes independent edge/predecessor certification.
#ifdef WILF_CUDA
        basic_equal(b,gpu_stats[i]);
#endif
        if(!b.finite)continue;
        ++finite;
        if(b.e<4 || 3*b.e>=m || b.c<=4*m)continue;
        ++eligible;
        Support s=support(m,G,w);
        int height=0;i64 support_mass=0;
        const int d=b.e-1;
        for(int residue=0;residue<m;++residue) {
            int degree=0,nonzero=0;
            for(int j=0;j<d;++j) {const int x=s.words[static_cast<size_t>(residue)*d+j];degree+=x;nonzero+=x>0;}
            height=std::max(height,degree);support_mass+=std::max(0,nonzero-1);
        }
        shape_excluded+=s.Dep>=support_mass;residue_excluded+=s.Dep>=s.kappa;flat_excluded+=height<=2;
        resistant+=(s.Dep<s.kappa && height>=3);
        tiles.insert(s.tile_hash);profiles.insert(s.tile_hash ^ (UINT64_C(0x9e3779b97f4a7c15)*b.top));
        if(s.Qmin<0)++bad_phases;
        if(s.Q<minimum_Q || (s.Q==minimum_Q && static_cast<__int128>(b.W)*best.basic.c < static_cast<__int128>(best.basic.W)*b.c)) {
            minimum_Q=s.Q;best=s;best_G=G;best_w=w;
        }
        if(s.Qmin<minimum_phase) {minimum_phase=s.Qmin;phase_best=s;phase_G=G;phase_w=w;}
        if(s.Q<0 || b.W<0) {
            require(dijkstra_heap(m,G)==w,"promoted candidate fails independent heap");
            emit_case(b.W<0?"negative_W_candidate":"negative_Q_candidate",m,G,w,s);
            return b.W<0?4:3;
        }
    }
    const double analysis_ms=elapsed(analysis_start);
    std::cout << "{\"kind\":\"benchmark\",\"batch\":"<<batch<<",\"seed\":"<<seed
              <<",\"m\":"<<m<<",\"supplied_k\":"<<k<<",\"cpu_threads\":"<<threads
              <<",\"generation\":\""<<(anchor.empty()?"uniform_integer":"residue_structural_mutation")<<"\""
              <<",\"generation_ms\":"<<generation_ms
              <<",\"cpu_scan_serial_ms\":"<<serial_ms<<",\"cpu_scan_parallel_ms\":"<<parallel_ms
              <<",\"heap_check_count\":"<<independent_count<<",\"heap_check_ms\":"<<heap_ms
              <<",\"gpu_kernel_ms\":";
#ifdef WILF_CUDA
    std::cout<<gpu_kernel<<",\"gpu_wall_including_transfers_ms\":"<<gpu_wall;
#else
    std::cout<<"null,\"gpu_wall_including_transfers_ms\":null";
#endif
    std::cout<<",\"cpu_canonical_analysis_ms\":"<<analysis_ms
              <<",\"cpu_pipeline_component_sum_ms\":"<<generation_ms+parallel_ms+analysis_ms
              <<",\"gpu_pipeline_component_sum_ms\":";
#ifdef WILF_CUDA
    std::cout<<generation_ms+gpu_wall+analysis_ms;
#else
    std::cout<<"null";
#endif
    std::cout<<",\"cofinite\":"<<finite<<",\"eligible\":"<<eligible
              <<",\"shape_excluded\":"<<shape_excluded<<",\"residue_excluded\":"<<residue_excluded
              <<",\"flat_excluded\":"<<flat_excluded<<",\"residue_resistant_height_ge3\":"<<resistant
              <<",\"diagnostic_tile_hashes\":"<<tiles.size()<<",\"diagnostic_profile_hashes\":"<<profiles.size()
              <<",\"negative_abstract_phase_count\":"<<bad_phases<<",\"minimum_Q\":";
    if(eligible)std::cout<<minimum_Q;else std::cout<<"null";
    std::cout<<",\"minimum_abstract_phase_Q\":";
    if(eligible)std::cout<<minimum_phase;else std::cout<<"null";
    std::cout<<",\"universal_sign_claim\":false}\n";
    if(eligible)emit_case("minimum_actual_Q",m,best_G,best_w,best);
    if(eligible && minimum_phase<0)emit_case("unrealized_negative_phase",m,phase_G,phase_w,phase_best);
    return 0;
}

int neighbor_audit(int threads,int m,const std::vector<i64>& anchor) {
    require(m>=3 && m<=1024 && threads>=1 && threads<=128 && !anchor.empty() && anchor.size()<=64,
            "invalid neighbor audit shape");
    for(i64 p:anchor)require(p>m && p<13LL*m,"neighbor anchor out of height range");
    const auto basew=scan_cpu(m,anchor);const auto base=support(m,anchor,basew);
    const i64 baseF=base.kappa-base.Dep;
    std::vector<std::pair<int,i64>> moves;
    for(int j=0;j<static_cast<int>(anchor.size());++j)
        for(i64 value=m+1;value<13LL*m;++value)if(value!=anchor[j])moves.emplace_back(j,value);
    require(moves.size()==anchor.size()*static_cast<size_t>(12*m-2),"neighbor coverage count wrong");
    std::vector<i64> fitness(moves.size(),std::numeric_limits<i64>::min());
    std::vector<int> finite(moves.size()),eligible(moves.size()),height(moves.size()),codes(moves.size());
    std::vector<int> evaluated(moves.size());std::atomic<bool> discovery{false};
    std::vector<std::uint64_t> hashes(moves.size());
    const auto started=Clock::now();
    safe_parallel(static_cast<int>(moves.size()),threads,[&](int i) {
        if(discovery.load())return;
        evaluated[i]=1;
        auto G=anchor;G[moves[i].first]=moves[i].second;
        const auto w=scan_cpu(m,G);
        if(std::find(w.begin(),w.end(),INF)!=w.end())return;
        const auto score=support(m,G,w);finite[i]=1;
        const auto& b=score.basic;
        if(b.W<0){codes[i]=4;discovery=true;}
        eligible[i]=b.e>=4 && 3*b.e<m && b.c>4*m;
        const int d=b.e-1;
        for(int r=0;r<m;++r){int degree=0;for(int j=0;j<d;++j)degree+=score.words[static_cast<size_t>(r)*d+j];height[i]=std::max(height[i],degree);}
        if(eligible[i] && score.Q<0 && codes[i]!=4){codes[i]=3;discovery=true;}
        if(!eligible[i] || height[i]<3)return;
        hashes[i]=score.tile_hash;fitness[i]=score.kappa-score.Dep;
        if(fitness[i]>0 && codes[i]==0)codes[i]=5;
        if(codes[i])discovery=true;
    });
    const double wall=elapsed(started);
    i64 bestF=std::numeric_limits<i64>::min(),sameF=bestF,changedF=bestF;
    int best=-1,promoted=-1,code=0,accepted=0,better=0,ties=0,finite_count=0;
    std::unordered_set<std::uint64_t> tiles;
    auto priority=[](int value){return value==4?3:value==3?2:value==5?1:0;};
    for(int i=0;i<static_cast<int>(moves.size());++i) {
        finite_count+=finite[i];
        if(priority(codes[i])>priority(code)){promoted=i;code=codes[i];}
        if(!eligible[i] || height[i]<3)continue;
        ++accepted;better+=fitness[i]>baseF;ties+=fitness[i]==baseF;tiles.insert(hashes[i]);
        if(fitness[i]>bestF){bestF=fitness[i];best=i;}
        if(moves[i].second%m==anchor[moves[i].first]%m)sameF=std::max(sameF,fitness[i]);
        else changedF=std::max(changedF,fitness[i]);
    }
    auto field=[](i64 value){if(value==std::numeric_limits<i64>::min())std::cout<<"null";else std::cout<<value;};
    std::cout<<"{\"kind\":\"single_input_plateau_audit\",\"m\":"<<m<<",\"base_F\":"<<baseF
             <<",\"provided_generators\":"<<anchor.size()<<",\"replacements\":"<<moves.size()
             <<",\"evaluated\":"<<std::accumulate(evaluated.begin(),evaluated.end(),0)
             <<",\"cofinite\":"<<finite_count<<",\"domain_eligible_height_ge3\":"<<accepted
             <<",\"improving\":"<<better<<",\"ties\":"<<ties<<",\"maximum_F\":";field(bestF);
    std::cout<<",\"same_residue_maximum_F\":";field(sameF);
    std::cout<<",\"changed_residue_maximum_F\":";field(changedF);
    std::cout<<",\"diagnostic_tiles\":"<<tiles.size()<<",\"wall_ms\":"<<wall
             <<",\"scope\":\"all one-input changes m+1<=p<13m; finite move set only\"}\n";
    const int selected=promoted>=0?promoted:best;
    if(selected>=0) {
        auto G=anchor;G[moves[selected].first]=moves[selected].second;
        const auto w=scan_cpu(m,G);require(w==dijkstra_heap(m,G),"neighbor selected heap check failed");
        const auto score=support(m,G,w);
        emit_case(code==4?"negative_W_candidate":code==3?"negative_Q_candidate":code==5?"support_resistant_candidate":"neighbor_best",m,G,w,score);
    }
    return code;
}

#include "warm.hpp"
#include "adaptive.hpp"
#include "exchange.hpp"
#include "neutral.hpp"
#include "trade_policy.hpp"
#include "boundary.hpp"
int main(int argc,char**argv) {
    try {
#ifdef WILF_CUDA
        const auto gpu_init_started=Clock::now();
        std::cerr<<"GPU "<<gpu_description()<<'\n';
        gpu_context_initialization_ms=elapsed(gpu_init_started);
#endif
        if(argc>=2 && std::string(argv[1])=="--self-test") {self_test(argc>2?std::stoi(argv[2]):1000);return 0;}
        if(argc==2 && std::string(argv[1])=="--archive-test") {adaptive_archive_selftest();return 0;}
        if(argc>=5 && std::string(argv[1])=="--boundary") {
            std::vector<i64> G;for(int i=4;i<argc;++i)G.push_back(std::stoll(argv[i]));
            return boundary_probe(std::stoi(argv[2]),std::stoi(argv[3]),G);
        }
        if(argc==3 && std::string(argv[1])=="--trade-search") return trade_policy_search(std::stoi(argv[2]));
        if(argc>=4 && std::string(argv[1])=="--trade-policy") {
            std::vector<i64> G;for(int i=3;i<argc;++i)G.push_back(std::stoll(argv[i]));
            return trade_policy_case(std::stoi(argv[2]),G);
        }
        if(argc>=3 && std::string(argv[1])=="--case") {
            const int m=std::stoi(argv[2]);std::vector<i64>G;
            for(int i=3;i<argc;++i)G.push_back(std::stoll(argv[i]));
            const auto w=scan_cpu(m,G);require(w==dijkstra_heap(m,G),"case heap mismatch");
            emit_case("case",m,G,w,support(m,G,w));return 0;
        }
        if(argc==7 && std::string(argv[1])=="--bench")
            return benchmark(std::stoi(argv[2]),std::stoull(argv[3]),std::stoi(argv[4]),std::stoi(argv[5]),std::stoi(argv[6]));
        if(argc==8 && std::string(argv[1])=="--warm")
            return warmed_run(std::stoi(argv[2]),std::stoi(argv[3]),std::stoull(argv[4]),std::stoi(argv[5]),std::stoi(argv[6]),std::stoi(argv[7]));
        if(argc>=5 && std::string(argv[1])=="--neighbors") {
            std::vector<i64> anchor;for(int i=4;i<argc;++i)anchor.push_back(std::stoll(argv[i]));
            return neighbor_audit(std::stoi(argv[2]),std::stoi(argv[3]),anchor);
        }
        if(argc>=5 && std::string(argv[1])=="--exchange") {
            std::vector<i64> anchor;for(int i=4;i<argc;++i)anchor.push_back(std::stoll(argv[i]));
            return exchange_audit(std::stoi(argv[2]),std::stoi(argv[3]),anchor);
        }
        if(argc>=5 && std::string(argv[1])=="--neutral") {
            std::vector<i64> anchor;for(int i=4;i<argc;++i)anchor.push_back(std::stoll(argv[i]));
            return neutral_audit(std::stoi(argv[2]),std::stoi(argv[3]),anchor);
        }
        if(argc>=8 && std::string(argv[1])=="--adaptive") {
            std::vector<i64> anchor;for(int i=7;i<argc;++i)anchor.push_back(std::stoll(argv[i]));
            return adaptive_run(std::stoi(argv[2]),std::stoi(argv[3]),std::stoull(argv[4]),std::stoi(argv[5]),std::stoi(argv[6]),anchor);
        }
        if(argc>=7 && std::string(argv[1])=="--mutate") {
            std::vector<i64>anchor;for(int i=6;i<argc;++i)anchor.push_back(std::stoll(argv[i]));
            return benchmark(std::stoi(argv[2]),std::stoull(argv[3]),std::stoi(argv[4]),std::stoi(argv[5]),static_cast<int>(anchor.size()),anchor);
        }
        std::cerr<<"usage: --self-test [lists] | --archive-test | --boundary threads m generators... | --trade-policy m generators... | --trade-search 7 | --case m generators... | --bench batch seed threads m k | --mutate batch seed threads m generators... | --warm batch repeats seed threads m k | --adaptive batch generations seed threads m generators... | --neighbors threads m generators... | --exchange threads m generators... | --neutral threads m generators...\n";
        return 2;
    } catch(const std::exception& error) {std::cerr<<"ERROR "<<error.what()<<'\n';return 2;}
}
