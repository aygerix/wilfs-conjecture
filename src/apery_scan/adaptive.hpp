#pragma once

// Include after the driver helpers (Random, Clock, elapsed, require, emit_case,
// basic_equal and exception-safe safe_parallel). This is a feedback search, not
// a universal sign claim or a claim that every diagnostic phase is realizable.
#include <array>
#include <set>

struct AdaptiveEntry {
    std::vector<wilf::i64> G, w;
    wilf::Support score;
    wilf::SupportTiming timing;
    int height = 0;
    wilf::i64 F = std::numeric_limits<wilf::i64>::min(), support_mass = 0;
    bool finite = false, eligible = false;
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

inline std::vector<AdaptiveEntry> adaptive_archive(std::vector<AdaptiveEntry> pool,
                                                  int capacity, int m) {
    std::sort(pool.begin(), pool.end(), adaptive_better);
    std::vector<AdaptiveEntry> answer;
    std::set<std::pair<int, std::uint64_t>> selected;
    std::vector<int> by_e(m + 1, 0);
    auto take = [&](int tier, int limit) {
        for (int pass = 0; pass < 2 && static_cast<int>(answer.size()) < limit; ++pass) {
            for (const auto& item : pool) {
                if (static_cast<int>(answer.size()) >= limit) break;
                if (!item.finite || adaptive_tier(item) != tier) continue;
                const auto key = std::make_pair(item.score.basic.e, item.score.tile_hash);
                if (selected.count(key) || (pass == 0 && by_e[key.first] >= 4)) continue;
                selected.insert(key);
                ++by_e[key.first];
                answer.push_back(item);
            }
        }
    };
    const int bridge_reserve = capacity > 1 ? std::max(1, capacity / 4) : 0;
    take(0, capacity - bridge_reserve);
    take(1, std::min(capacity, static_cast<int>(answer.size()) + bridge_reserve));
    take(0, capacity);
    take(1, capacity);
    if (answer.empty()) take(2, capacity); // explicitly reported outside-domain bridges
    std::sort(answer.begin(), answer.end(), adaptive_better);
    return answer;
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
        const int parent_count = static_cast<int>(archive.size());
        for (int i = 0; i < batch; ++i) {
            std::vector<i64> G;
            if (generation > 0 && i < std::min(parent_count, batch / 16)) {
                G = archive[i].G;
                ++copies;
            } else if ((i % 8 == 7) || (generation > 0 && archive.empty())) {
                G = adaptive_migrant(rng, m, k);
                ++migrants;
            } else if (generation == 0 && i == 0) {
                G = anchor;
            } else {
                const AdaptiveEntry* parent = nullptr;
                if (!archive.empty()) {
                    const auto a = rng.next() % archive.size();
                    const auto b = rng.next() % archive.size();
                    parent = &archive[std::min(a, b)]; // score-ranked tournament selection
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
        for (const auto& item : archive) {
            archived_nonflat += item.eligible && item.height >= 3;
            archived_bridges += item.eligible && item.height <= 2;
        }
        auto number_or_null = [](i64 value, i64 sentinel) {
            if (value == sentinel) std::cout << "null"; else std::cout << value;
        };
        std::cout << "{\"kind\":\"adaptive_generation\",\"m\":" << m << ",\"seed\":" << seed
                  << ",\"generation\":" << generation << ",\"batch\":" << batch << ",\"cpu_threads\":" << threads
                  << ",\"parent_archive_epoch\":" << generation - 1 << ",\"scored_parent_archive\":" << parent_count
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
                  << ",\"archive_size\":" << archive.size() << ",\"archive_nonflat\":" << archived_nonflat
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
