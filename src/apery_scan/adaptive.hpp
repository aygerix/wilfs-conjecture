#pragma once

// Include after the driver helpers (Random, Clock, elapsed, require, emit_case,
// basic_equal and exception-safe safe_parallel). This is a feedback search, not
// a universal sign claim or a claim that every diagnostic phase is realizable.
#include <array>
#include <set>
#include <map>
#include <tuple>
#include <cmath>

struct AdaptiveEntry {
    std::vector<wilf::i64> G, w;
    wilf::Support score;
    wilf::SupportTiming timing;
    int height = 0;
    wilf::i64 F = std::numeric_limits<wilf::i64>::min(), support_mass = 0;
    bool finite = false, eligible = false;
    bool diversity_ready = false;
    std::vector<wilf::i64> primitive_heights, mixed_slacks;
    double boundary_distance = std::numeric_limits<double>::infinity();
};

inline int adaptive_tier(const AdaptiveEntry& item) {
    return item.eligible ? (item.height >= 3 ? 0 : 1) : 2;
}

inline bool adaptive_better(const AdaptiveEntry& a, const AdaptiveEntry& b) {
    if (adaptive_tier(a) != adaptive_tier(b)) return adaptive_tier(a) < adaptive_tier(b);
    if (a.F != b.F) return a.F > b.F;
    const auto ac = std::max(wilf::i64(1), a.score.basic.c);
    const auto bc = std::max(wilf::i64(1), b.score.basic.c);
    const __int128 left = static_cast<__int128>(a.score.basic.W) * bc;
    const __int128 right = static_cast<__int128>(b.score.basic.W) * ac;
    if (left != right) return left < right;
    if (a.score.basic.e != b.score.basic.e) return a.score.basic.e < b.score.basic.e;
    if (a.score.tile_hash != b.score.tile_hash) return a.score.tile_hash < b.score.tile_hash;
    return a.G < b.G;
}

inline wilf::i64 adaptive_value(int m, wilf::i64 height, int residue) {
    height = std::max(wilf::i64(1), std::min(wilf::i64(12), height));
    residue = (residue % m + m) % m;
    if (height == 1 && residue == 0) height = 2;
    return height * m + residue;
}

inline std::vector<wilf::i64> adaptive_migrant(Random& rng, int m, int k) {
    std::vector<wilf::i64> result(k);
    for (auto& p : result) {
        const wilf::i64 height = 1 + rng.next() % 12;
        const int residue = rng.next() % m;
        p = adaptive_value(m, height, residue);
    }
    return result;
}

// The returned operation bucket is logged. Residue changes, +/-m changes,
// correlated transforms and deliberate redundancy all change genuine input
// semigroups; no fixed-tile or fixed-actual-embedding-dimension constraint is used.
inline std::vector<wilf::i64> adaptive_mutate(Random& rng, int m,
                                            const std::vector<wilf::i64>& parent,
                                            int& operation) {
    auto result = parent;
    const int k = static_cast<int>(result.size());
    const int chosen = rng.next() % k;
    const int other = rng.next() % k;
    const int draw = rng.next() % 100;
    if (draw < 35) {
        operation = 0;
        int residue;
        do { residue = rng.next() % m; } while (residue == parent[chosen] % m);
        result[chosen] = adaptive_value(m, parent[chosen] / m, residue);
    } else if (draw < 55) {
        operation = 1; // primitive/canonical boundaries by one modulus
        const int step = rng.next() % 2 ? 1 : -1;
        result[chosen] = adaptive_value(m, parent[chosen] / m + step, parent[chosen] % m);
    } else if (draw < 70) {
        operation = 2;
        const wilf::i64 first_height = 1 + rng.next() % 12;
        const int first_residue = rng.next() % m;
        result[chosen] = adaptive_value(m, first_height, first_residue);
        const wilf::i64 second_height = 1 + rng.next() % 12;
        const int second_residue = rng.next() % m;
        result[other] = adaptive_value(m, second_height, second_residue);
    } else if (draw < 78) {
        operation = 3;
        const int shift = 1 + rng.next() % (m - 1);
        for (auto& p : result) p = adaptive_value(m, p / m, (p % m + shift) % m);
    } else if (draw < 84) {
        operation = 4;
        for (auto& p : result) p = adaptive_value(m, p / m, (m - p % m) % m);
    } else if (draw < 90) {
        operation = 5;
        int unit;
        do { unit = 1 + rng.next() % (m - 1); }
        while (std::gcd(unit, m) != 1 || (m > 2 && unit == 1));
        for (auto& p : result) p = adaptive_value(m, p / m, (p % m * unit) % m);
    } else if (draw < 96) {
        operation = 6; // creates/removes redundant supplied generators
        const auto sum = parent[chosen] + parent[other];
        result[chosen] = adaptive_value(m, sum / m, sum % m);
    } else {
        operation = 7;
        const int step = rng.next() % 2 ? 1 : -1;
        for (auto& p : result) p = adaptive_value(m, p / m + step, p % m);
        result[chosen] = adaptive_value(m, result[chosen] / m, rng.next() % m);
    }
    // Boundary clipping or a mirror can be an identity. Force a genuine change
    // in the proposed value vector rather than claiming passive copies as feedback.
    if (result == parent)
        result[chosen] = adaptive_value(m, parent[chosen] / m, (parent[chosen] % m + 1) % m);
    return result;
}

// Exact structural identity; the diagnostic hash is NEVER used for grouping.
using AdaptiveKey = std::tuple<int, std::vector<int>, std::vector<int>>;
inline AdaptiveKey adaptive_key(const AdaptiveEntry& item) {
    return {item.score.basic.e, item.score.residues, item.score.words};
}
inline std::vector<std::vector<int>> adaptive_groups(const std::vector<AdaptiveEntry>& entries) {
    std::map<AdaptiveKey, int> index;
    std::vector<std::vector<int>> groups;
    for (int i = 0; i < static_cast<int>(entries.size()); ++i) {
        const auto key = adaptive_key(entries[i]);
        auto found = index.find(key);
        if (found == index.end()) {
            const int at = static_cast<int>(groups.size());
            index.emplace(key, at); groups.push_back({i});
        } else groups[found->second].push_back(i);
    }
    return groups;
}
inline void adaptive_prepare_diversity(AdaptiveEntry& item, int m) {
    if (item.diversity_ready) return;
    item.diversity_ready = true;
    const int d = static_cast<int>(item.score.residues.size());
    for (int r : item.score.residues) item.primitive_heights.push_back(item.w[r] / m);
    for (int s = 0; s < m; ++s) for (int j = 0; j < d; ++j) {
        const int t = (s + item.score.residues[j]) % m;
        bool positive = false, negative = false;
        double norm2 = 0;
        for (int k = 0; k < d; ++k) {
            const int coefficient = item.score.words[static_cast<std::size_t>(s)*d+k] + (k == j)
                                  - item.score.words[static_cast<std::size_t>(t)*d+k];
            positive |= coefficient > 0; negative |= coefficient < 0;
            norm2 += double(coefficient) * coefficient;
        }
        // Identity and one-sign rows do not give a nontrivial positive-orthant
        // crossing. Mixed signs are necessary, not sufficient, for accessibility.
        if (!positive || !negative) continue;
        const wilf::i64 gap = item.w[s] + item.w[item.score.residues[j]] - item.w[t];
        require(gap >= 0 && gap % m == 0, "invalid primitive-edge slack");
        item.mixed_slacks.push_back(gap / m);
        // Distance in primitive HEIGHT coordinates to the trade hyperplane
        // gap=0. Tight rows remain in the diversity vector, not this strict-row
        // minimum. This heuristic does not certify that crossing is attainable.
        if (gap > 0)
            item.boundary_distance = std::min(item.boundary_distance,
                double(gap / m) / std::sqrt(norm2));
    }
}
inline wilf::i64 adaptive_l1(const std::vector<wilf::i64>& a, const std::vector<wilf::i64>& b) {
    require(a.size() == b.size(), "same structural group has incompatible diversity coordinates");
    wilf::i64 result = 0;
    for (std::size_t i = 0; i < a.size(); ++i) result += a[i] > b[i] ? a[i]-b[i] : b[i]-a[i];
    return result;
}
inline bool adaptive_ratio_better(const AdaptiveEntry& a, const AdaptiveEntry& b) {
    const __int128 left = static_cast<__int128>(a.score.basic.W) * std::max(wilf::i64(1), b.score.basic.c);
    const __int128 right = static_cast<__int128>(b.score.basic.W) * std::max(wilf::i64(1), a.score.basic.c);
    return left != right ? left < right : adaptive_better(a,b);
}
inline std::vector<AdaptiveEntry> adaptive_representatives(std::vector<AdaptiveEntry> candidates, int m) {
    std::sort(candidates.begin(), candidates.end(), adaptive_better);
    std::set<std::vector<wilf::i64>> height_keys;
    std::vector<AdaptiveEntry> unique;
    for (auto& item : candidates) {
        adaptive_prepare_diversity(item,m);
        if (height_keys.insert(item.primitive_heights).second) unique.push_back(std::move(item));
    }
    std::vector<int> chosen;
    auto add = [&](int i) {
        if (i >= 0 && chosen.size() < 4 && std::find(chosen.begin(),chosen.end(),i)==chosen.end()) chosen.push_back(i);
    };
    add(0); // Preserve the original best eligible/F/W/c representative.
    int ratio_best = 0;
    for (int i=1;i<static_cast<int>(unique.size());++i)
        if(adaptive_ratio_better(unique[i],unique[ratio_best]))ratio_best=i;
    add(ratio_best); // Also preserve unconditional best W/c if eligibility differs.
    int farthest = -1; wilf::i64 farthest_distance = -1;
    for(int i=0;i<static_cast<int>(unique.size());++i) {
        const auto distance=adaptive_l1(unique[i].primitive_heights,unique[0].primitive_heights);
        if(distance>farthest_distance){farthest=i;farthest_distance=distance;}
    }
    add(farthest); // A distant same-tile height state survives even with worse W/c.
    while(chosen.size()<4 && chosen.size()<unique.size()) {
        int best=-1; double boundary=std::numeric_limits<double>::infinity();
        wilf::i64 diversity=-1, height_diversity=-1;
        for(int i=0;i<static_cast<int>(unique.size());++i) {
            if(std::find(chosen.begin(),chosen.end(),i)!=chosen.end())continue;
            wilf::i64 row_distance=std::numeric_limits<wilf::i64>::max();
            wilf::i64 height_distance=row_distance;
            for(int j:chosen) {
                row_distance=std::min(row_distance,adaptive_l1(unique[i].mixed_slacks,unique[j].mixed_slacks));
                height_distance=std::min(height_distance,adaptive_l1(unique[i].primitive_heights,unique[j].primitive_heights));
            }
            if(best<0 || unique[i].boundary_distance<boundary ||
               (unique[i].boundary_distance==boundary && (row_distance>diversity ||
                (row_distance==diversity && height_distance>height_diversity)))) {
                best=i;boundary=unique[i].boundary_distance;diversity=row_distance;height_diversity=height_distance;
            }
        }
        add(best);
    }
    std::vector<AdaptiveEntry> answer;
    for(int i:chosen)answer.push_back(std::move(unique[i]));
    return answer;
}

// capacity counts EXACT STRUCTURAL GROUPS; returned flat entries contain up to
// four representatives per group, at most 4*capacity. Group order is score rank,
// and each group's first entry is its original best representative.
inline std::vector<AdaptiveEntry> adaptive_archive(std::vector<AdaptiveEntry> pool,
                                                  int capacity, int m) {
    require(capacity>=1 && capacity<=64,"archive group capacity must be1..64");
    std::sort(pool.begin(),pool.end(),adaptive_better);
    std::map<AdaptiveKey,int> index;
    std::vector<std::vector<AdaptiveEntry>> groups;
    for(auto& item:pool)if(item.finite) {
        auto key=adaptive_key(item);
        auto found=index.find(key);
        if(found==index.end()) {
            const int at=static_cast<int>(groups.size());index.emplace(std::move(key),at);
            groups.push_back({});groups.back().push_back(std::move(item));
        } else groups[found->second].push_back(std::move(item));
    }
    std::vector<int> selected;std::set<int> used;std::vector<int> by_e(m+1,0);
    auto take=[&](int tier,int limit) {
        for(int pass=0;pass<2 && static_cast<int>(selected.size())<limit;++pass)
            for(int i=0;i<static_cast<int>(groups.size()) && static_cast<int>(selected.size())<limit;++i) {
                const auto& first=groups[i][0];const int e=first.score.basic.e;
                if(adaptive_tier(first)!=tier || used.count(i) || (pass==0 && by_e[e]>=4))continue;
                used.insert(i);++by_e[e];selected.push_back(i);
            }
    };
    const int bridge_reserve=capacity>1?std::max(1,capacity/4):0;
    take(0,capacity-bridge_reserve);
    take(1,std::min(capacity,static_cast<int>(selected.size())+bridge_reserve));
    take(0,capacity);take(1,capacity);if(selected.empty())take(2,capacity);
    std::sort(selected.begin(),selected.end(),[&](int a,int b){return adaptive_better(groups[a][0],groups[b][0]);});
    std::vector<AdaptiveEntry> answer;
    for(int i:selected) {
        auto reps=adaptive_representatives(std::move(groups[i]),m);
        for(auto& item:reps)answer.push_back(std::move(item));
    }
    require(answer.size()<=static_cast<std::size_t>(4*capacity),"archive representative budget exceeded");
    return answer;
}

inline void adaptive_archive_selftest() {
    using namespace wilf;
    const int m=63;
    const std::vector<i64> base_G={307,438,440,454,461,474,475,477,482,486,492};
    auto make_entry=[&](const std::vector<i64>& G) {
        AdaptiveEntry item;item.G=G;item.w=scan_cpu(m,G);
        require(item.w==dijkstra_heap(m,G),"archive control heap mismatch");
        item.score=support(m,G,item.w);item.finite=true;
        item.eligible=item.score.basic.e>=4 && 3*item.score.basic.e<m && item.score.basic.c>4*m;
        item.F=item.score.kappa-item.score.Dep;
        const int d=item.score.basic.e-1;
        for(int s=0;s<m;++s) {
            int degree=0;for(int j=0;j<d;++j)degree+=item.score.words[static_cast<std::size_t>(s)*d+j];
            item.height=std::max(item.height,degree);
        }
        return item;
    };
    auto base=make_entry(base_G);
    auto neutral_G=base_G;neutral_G[5]=348;
    auto neutral=make_entry(neutral_G);
    require(base.score.basic.W==708 && neutral.score.basic.W==1020,"archive fixed control invariants changed");
    require(adaptive_key(base)==adaptive_key(neutral) && base.score.gamma==neutral.score.gamma,
            "archive fixed neutral control changed exact tile");
    require(adaptive_ratio_better(base,neutral),"archive control best W/c is not the base");
    // A genuine generator-removal neighbor, with ONLY its diagnostic hash
    // overwritten, proves that a collision cannot merge different exact keys.
    auto different_G=base_G;different_G[5]=475;
    auto different=make_entry(different_G);
    require(adaptive_key(base)!=adaptive_key(different),"archive collision control has same exact key");
    different.score.tile_hash=base.score.tile_hash;
    auto archive=adaptive_archive({base,neutral,different},64,m);
    const auto groups=adaptive_groups(archive);
    require(groups.size()==2 && archive.size()==3,"archive exact grouping/representative retention failed");
    bool kept_base=false,kept_neutral=false;
    for(const auto& group:groups)if(adaptive_key(archive[group[0]])==adaptive_key(base)) {
        require(archive[group[0]].score.basic.W==708,"archive original W/c best was displaced");
        for(int at:group){kept_base|=archive[at].G==base_G;kept_neutral|=archive[at].G==neutral_G;}
    }
    require(kept_base && kept_neutral,"archive lost the higher-W neutral height representative");
    adaptive_prepare_diversity(base,m);adaptive_prepare_diversity(neutral,m);
    require(base.primitive_heights!=neutral.primitive_heights,"archive controls have identical primitive heights");
    std::cout<<"{\"kind\":\"archive_self_test\",\"groups\":"<<groups.size()
             <<",\"representatives\":"<<archive.size()<<",\"exact_grouping\":true"
             <<",\"synthetic_hash_collision_test\":true,\"genuine_semigroups\":true"
             <<",\"best_W\":708,\"neutral_W\":1020,\"best_preserved\":true,\"neutral_retained\":true"
             <<",\"base_primitive_heights\":";print_array(base.primitive_heights);
    std::cout<<",\"neutral_primitive_heights\":";print_array(neutral.primitive_heights);
    std::cout<<",\"base_strict_boundary_distance\":"<<base.boundary_distance
             <<",\"neutral_strict_boundary_distance\":"<<neutral.boundary_distance
             <<",\"distance_is_accessibility_heuristic_only\":true}\n"<<std::flush;
}

inline int adaptive_run(int batch, int generations, std::uint64_t seed, int threads,
                        int m, const std::vector<wilf::i64>& anchor) {
    using namespace wilf;
    require(m >= 3 && m <= 1024 && batch >= 1 && batch <= 1024 &&
            generations >= 1 && generations <= 150 && threads >= 1 && threads <= 128 &&
            !anchor.empty() && anchor.size() <= 64, "invalid adaptive shape/budget");
    validate_inputs(m, anchor);
    for (i64 p : anchor) require(p > m && p / m >= 1 && p / m <= 12,
                                "adaptive anchor must have heights 1..12 and exceed m");
    const int k = static_cast<int>(anchor.size());
    Random rng{seed};
    const auto total_start = Clock::now();
    std::vector<AdaptiveEntry> archive;
    const int archive_capacity = std::max(1, std::min(64, batch / 8));
#ifdef WILF_CUDA
    GpuWorkspace workspace(m, k, batch);
    std::vector<Basic> gpu_stats;
    const auto setup = workspace.setup_timing();
    std::cout << "{\"kind\":\"adaptive_setup\",\"m\":" << m
              << ",\"allocation_ms\":" << setup.allocation_ms
              << ",\"setup_ms\":" << setup.setup_ms << "}\n" << std::flush;
#endif
    std::vector<i64> weights(static_cast<std::size_t>(batch) * m);
    std::vector<i64> flat(static_cast<std::size_t>(batch) * k);
    i64 best_seen = std::numeric_limits<i64>::min();
    std::uint64_t total_feedback = 0;
    for (int generation = 0; generation < generations; ++generation) {
        const auto proposal_start = Clock::now();
        int feedback = 0, migrants = 0, copies = 0, outside_parent = 0, bridge_parent = 0;
        std::array<int, 8> operations{};
        const auto parent_groups = adaptive_groups(archive);
        const int parent_count = static_cast<int>(parent_groups.size());
        const int parent_representatives = static_cast<int>(archive.size());
        const int elite_count = generation > 0 && batch > 1 ?
            std::min(parent_count, std::max(1,batch/16)) : 0;
        for (int i = 0; i < batch; ++i) {
            std::vector<i64> G;
            if (i < elite_count) {
                G = archive[parent_groups[i][0]].G;
                ++copies;
            } else if ((i % 8 == 7) || (generation > 0 && archive.empty())) {
                G = adaptive_migrant(rng, m, k);
                ++migrants;
            } else if (generation == 0 && i == 0) {
                G = anchor;
            } else {
                const AdaptiveEntry* parent = nullptr;
                if (!archive.empty()) {
                    const auto a = rng.next() % parent_groups.size();
                    const auto b = rng.next() % parent_groups.size();
                    const auto& group = parent_groups[std::min(a,b)];
                    parent = &archive[group[rng.next()%group.size()]]; // ranked-group tournament, uniform representative
                    ++feedback;
                    outside_parent += !parent->eligible;
                    bridge_parent += parent->eligible && parent->height <= 2;
                }
                int operation = 0;
                G = adaptive_mutate(rng, m, parent ? parent->G : anchor, operation);
                ++operations[operation];
            }
            std::copy(G.begin(), G.end(), flat.begin() + static_cast<std::size_t>(i) * k);
        }
        const double proposal_ms = elapsed(proposal_start);
        total_feedback += feedback;
        const auto engine_start = Clock::now();
#ifdef WILF_CUDA
        GpuTiming gpu_time;
        workspace.run(batch, flat, weights, gpu_stats, gpu_time);
#else
        safe_parallel(batch, threads, [&](int i) {
            const std::vector<i64> G(flat.begin() + static_cast<std::size_t>(i) * k,
                                     flat.begin() + static_cast<std::size_t>(i + 1) * k);
            const auto w = scan_cpu(m, G);
            std::copy(w.begin(), w.end(), weights.begin() + static_cast<std::size_t>(i) * m);
        });
#endif
        const double engine_ms = elapsed(engine_start);
        const auto scoring_start = Clock::now();
        std::vector<AdaptiveEntry> scored(batch);
        safe_parallel(batch, threads, [&](int i) {
            auto& entry = scored[i];
            entry.G.assign(flat.begin() + static_cast<std::size_t>(i) * k,
                           flat.begin() + static_cast<std::size_t>(i + 1) * k);
            entry.w.assign(weights.begin() + static_cast<std::size_t>(i) * m,
                           weights.begin() + static_cast<std::size_t>(i + 1) * m);
            if (std::find(entry.w.begin(), entry.w.end(), INF) != entry.w.end()) {
                std::string error;
                require(certify(m, entry.G, entry.w, &error), "adaptive noncofinite certificate: " + error);
#ifdef WILF_CUDA
                require(!gpu_stats[i].finite, "GPU finite flag differs");
#endif
                return;
            }
            entry.score = support(m, entry.G, entry.w, &entry.timing);
            entry.finite = true;
#ifdef WILF_CUDA
            basic_equal(entry.score.basic, gpu_stats[i]);
#endif
            const auto& basic = entry.score.basic;
            entry.eligible = basic.e >= 4 && 3 * basic.e < m && basic.c > 4 * m;
            entry.F = entry.score.kappa - entry.score.Dep;
            for (int s = 0; s < m; ++s) {
                int degree = 0, nonzero = 0;
                for (int j = 0; j < basic.e - 1; ++j) {
                    const int value = entry.score.words[static_cast<std::size_t>(s) * (basic.e - 1) + j];
                    degree += value;
                    nonzero += value > 0;
                }
                entry.height = std::max(entry.height, degree);
                entry.support_mass += std::max(0, nonzero - 1);
            }
        });
        const double scoring_ms = elapsed(scoring_start);
        const auto audit_start = Clock::now();
        // Bounded independent samples per generation; never a serial CPU replay
        // of the whole GPU population. Every promoted record is checked below.
        const int heap_checks = std::min(batch, 2);
        for (int check = 0; check < heap_checks; ++check) {
            const int i = (generation + check * std::max(1, batch / 2)) % batch;
            require(dijkstra_heap(m, scored[i].G) == scored[i].w,
                    "adaptive bounded independent heap audit failed");
        }
        const double audit_ms = elapsed(audit_start);
        int finite = 0, eligible = 0, bridges = 0, shape_excluded = 0, residue_excluded = 0;
        int height_ge3 = 0, resistant = 0, promotion = -1, promotion_code = 0;
        int best_nonflat = -1, negative_abstract_phases = 0;
        i64 current_best = std::numeric_limits<i64>::min(), bridge_best = current_best;
        i64 minimum_Q = std::numeric_limits<i64>::max();
        i64 minimum_abstract_Q = minimum_Q;
        double certification_sum = 0, canonical_sum = 0, score_sum = 0;
        std::set<std::uint64_t> tile_hashes, profile_hashes;
        std::set<int> actual_e;
        for (int i = 0; i < batch; ++i) {
            const auto& item = scored[i];
            certification_sum += item.timing.certification_ms;
            canonical_sum += item.timing.canonical_ms;
            score_sum += item.timing.scoring_ms;
            if (!item.finite) continue;
            ++finite;
            actual_e.insert(item.score.basic.e);
            tile_hashes.insert(item.score.tile_hash);
            profile_hashes.insert(item.score.tile_hash ^ (UINT64_C(0x9e3779b97f4a7c15) * item.score.basic.top));
            if (item.score.basic.W < 0 && promotion_code != 4) { promotion = i; promotion_code = 4; }
            if (!item.eligible) continue;
            ++eligible;
            shape_excluded += item.score.Dep >= item.support_mass;
            residue_excluded += item.F <= 0;
            minimum_Q = std::min(minimum_Q, item.score.Q);
            minimum_abstract_Q = std::min(minimum_abstract_Q, item.score.Qmin);
            negative_abstract_phases += item.score.Qmin < 0;
            if (item.height <= 2) { ++bridges; bridge_best = std::max(bridge_best, item.F); }
            else {
                ++height_ge3;
                current_best = std::max(current_best, item.F);
                resistant += item.F > 0;
                if (best_nonflat < 0 || adaptive_better(item, scored[best_nonflat])) best_nonflat = i;
            }
            if (item.score.Q < 0 && promotion_code != 4) { promotion = i; promotion_code = 3; }
            else if (item.height >= 3 && item.F > 0 && promotion_code == 0) { promotion = i; promotion_code = 5; }
        }
        best_seen = std::max(best_seen, current_best);
        const auto archive_start = Clock::now();
        std::vector<AdaptiveEntry> pool = archive;
        for (const auto& item : scored) if (item.finite) pool.push_back(item);
        archive = adaptive_archive(std::move(pool), archive_capacity, m);
        const double archive_ms = elapsed(archive_start);
        int archived_nonflat = 0, archived_bridges = 0;
        const auto archived_groups = adaptive_groups(archive);
        for (const auto& group : archived_groups) {
            const auto& item=archive[group[0]];
            archived_nonflat += item.eligible && item.height >= 3;
            archived_bridges += item.eligible && item.height <= 2;
        }
        auto number_or_null = [](i64 value, i64 sentinel) {
            if (value == sentinel) std::cout << "null"; else std::cout << value;
        };
        std::cout << "{\"kind\":\"adaptive_generation\",\"m\":" << m << ",\"seed\":" << seed
                  << ",\"generation\":" << generation << ",\"batch\":" << batch << ",\"cpu_threads\":" << threads
                  << ",\"parent_archive_epoch\":" << generation - 1 << ",\"scored_parent_archive\":" << parent_count
                  << ",\"parent_archive_groups\":" << parent_count << ",\"parent_archive_representatives\":" << parent_representatives
                  << ",\"parent_dependent_proposals\":" << feedback << ",\"total_parent_dependent_proposals\":" << total_feedback
                  << ",\"elite_copies\":" << copies << ",\"forced_migrants\":" << migrants
                  << ",\"outside_domain_parent_proposals\":" << outside_parent << ",\"flat_bridge_parent_proposals\":" << bridge_parent
                  << ",\"mutation_operation_counts\":";
        print_array(std::vector<int>(operations.begin(), operations.end()));
        std::cout << ",\"cofinite\":" << finite << ",\"domain_eligible\":" << eligible
                  << ",\"flat_bridge_count\":" << bridges << ",\"eligible_height_ge3\":" << height_ge3
                  << ",\"shape_excluded\":" << shape_excluded << ",\"residue_excluded\":" << residue_excluded
                  << ",\"resistant_height_ge3\":" << resistant << ",\"actual_embedding_dimensions\":";
        print_array(std::vector<int>(actual_e.begin(), actual_e.end()));
        std::cout << ",\"diagnostic_tile_hashes\":" << tile_hashes.size() << ",\"diagnostic_profile_hashes\":" << profile_hashes.size()
                  << ",\"archive_size\":" << archived_groups.size()
                  << ",\"archive_groups\":" << archived_groups.size() << ",\"archive_representatives\":" << archive.size()
                  << ",\"archive_group_capacity\":" << archive_capacity << ",\"representatives_per_group_limit\":4"
                  << ",\"parent_selection\":\"ranked_group_tournament_then_uniform_representative\"" << ",\"archive_nonflat\":" << archived_nonflat
                  << ",\"archive_flat_bridges\":" << archived_bridges << ",\"best_F_height_ge3\":";
        number_or_null(current_best, std::numeric_limits<i64>::min());
        std::cout << ",\"best_F_height_ge3_so_far\":"; number_or_null(best_seen, std::numeric_limits<i64>::min());
        std::cout << ",\"best_F_flat_bridge\":"; number_or_null(bridge_best, std::numeric_limits<i64>::min());
        std::cout << ",\"minimum_actual_Q\":"; number_or_null(minimum_Q, std::numeric_limits<i64>::max());
        std::cout << ",\"minimum_abstract_phase_Q\":"; number_or_null(minimum_abstract_Q, std::numeric_limits<i64>::max());
        std::cout << ",\"negative_abstract_phase_count\":" << negative_abstract_phases << ",\"best_nonflat\":";
        if (best_nonflat < 0) std::cout << "null";
        else {
            const auto& item = scored[best_nonflat];
            std::cout << "{\"F\":" << item.F << ",\"e\":" << item.score.basic.e << ",\"height\":" << item.height
                      << ",\"c\":" << item.score.basic.c << ",\"W\":" << item.score.basic.W
                      << ",\"Q\":" << item.score.Q << ",\"R\":" << item.score.R << ",\"Qmin\":" << item.score.Qmin
                      << ",\"actual_top_residue\":" << item.score.basic.top
                      << ",\"minimum_abstract_top_residue\":" << item.score.min_phase << '}';
        }
        std::cout << ",\"proposal_ms\":" << proposal_ms << ",\"engine_wall_ms\":" << engine_ms
                  << ",\"canonical_scoring_parallel_wall_ms\":" << scoring_ms
                  << ",\"certification_thread_sum_ms\":" << certification_sum
                  << ",\"canonical_thread_sum_ms\":" << canonical_sum << ",\"scoring_thread_sum_ms\":" << score_sum
                  << ",\"heap_audit_count\":" << heap_checks << ",\"heap_audit_ms\":" << audit_ms
                  << ",\"archive_update_ms\":" << archive_ms;
#ifdef WILF_CUDA
        std::cout << ",\"gpu_upload_ms\":" << gpu_time.upload_ms << ",\"gpu_kernel_ms\":" << gpu_time.kernel_ms
                  << ",\"gpu_download_ms\":" << gpu_time.download_ms << ",\"gpu_host_ms\":" << gpu_time.host_ms;
#endif
        std::cout << ",\"total_elapsed_ms\":" << elapsed(total_start) << ",\"universal_sign_claim\":false}\n" << std::flush;
        if (promotion >= 0) {
            const auto& item = scored[promotion];
            require(dijkstra_heap(m, item.G) == item.w, "adaptive promoted independent heap audit failed");
            std::cout << "{\"kind\":\"adaptive_promotion\",\"m\":" << m << ",\"generation\":" << generation
                      << ",\"exit_code\":" << promotion_code << ",\"height\":" << item.height
                      << ",\"F\":" << item.F << ",\"already_covered_flat\":" << (item.height <= 2 ? "true" : "false")
                      << ",\"independent_heap\":true,\"coin_column_verification_required\":true}\n" << std::flush;
            emit_case(promotion_code == 4 ? "negative_W_candidate" : promotion_code == 3 ? "negative_Q_candidate" :
                      "support_resistant_candidate", m, item.G, item.w, item.score);
            return promotion_code;
        }
    }
    if (!archive.empty()) {
        const auto& item = archive.front();
        require(dijkstra_heap(m, item.G) == item.w, "adaptive final-best heap audit failed");
        emit_case("adaptive_best", m, item.G, item.w, item.score);
    }
    std::cout << "{\"kind\":\"adaptive_complete\",\"m\":" << m << ",\"generations\":" << generations
              << ",\"batch\":" << batch << ",\"seed\":" << seed
              << ",\"total_parent_dependent_proposals\":" << total_feedback
              << ",\"elapsed_ms\":" << elapsed(total_start) << ",\"universal_sign_claim\":false}\n" << std::flush;
    return 0;
}
