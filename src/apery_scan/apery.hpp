#pragma once

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace wilf {

using i64 = long long;
constexpr i64 INF = 1LL << 60;

// Keep this layout in sync with the CUDA result record.
struct Basic {
    int m = 0, e = 0, top = 0, finite = 0;
    i64 c = 0, g = 0, W = 0;
};
static_assert(sizeof(int) == 4 && sizeof(i64) == 8 && sizeof(Basic) == 40,
              "Basic requires four int32 fields followed by three int64 fields");
static_assert(offsetof(Basic, c) == 16 && offsetof(Basic, W) == 32,
              "Basic host/device field offsets differ");

struct Support {
    Basic basic;
    i64 Dep = 0, kappa = 0, N = 0, Q = 0, R = 0, Qmin = 0;
    // min_phase is a TOP RESIDUE, not rho=(-c) mod m. Its rho is m-1-min_phase.
    int min_phase = 0;
    std::uint64_t tile_hash = 0; // Diagnostic only; never a certificate of equality.
    std::vector<i64> minimal;
    std::vector<int> residues, words, gamma;
};

struct SupportTiming {
    double certification_ms = 0, canonical_ms = 0, scoring_ms = 0;
};

inline void validate_inputs(int m, const std::vector<i64>& G) {
    if (m < 1 || m > 8192)
        throw std::invalid_argument("modulus must lie in [1,8192]");
    i64 largest = 1;
    for (i64 g : G) {
        if (g <= 0) throw std::invalid_argument("generators must be positive");
        largest = std::max(largest, g);
    }
    if (static_cast<__int128>(8) * m * m * largest >= INF)
        throw std::invalid_argument("8*m*m*max(G) must be strictly below INF");
}

// Add one generator at a time. On each residue cycle, old[j]-j*g has a
// prefix minimum for nonwrapping paths and a suffix minimum for wrapping paths.
// No shortest path needs a full positive-weight turn, so lengths 0,...,L-1 suffice.
inline std::vector<i64> scan_cpu(int m, const std::vector<i64>& G) {
    validate_inputs(m, G);
    std::vector<i64> w(m, INF);
    w[0] = 0;
    for (i64 g : G) {
        const int r = static_cast<int>(g % m);
        if (r == 0) continue;
        const int cycles = std::gcd(m, r), L = m / cycles;
        std::vector<i64> next(w), prefix(L), suffix(L + 1, INF);
        std::vector<int> cycle(L);
        for (int base = 0; base < cycles; ++base) {
            int s = base;
            i64 best = INF;
            for (int j = 0; j < L; ++j) {
                cycle[j] = s;
                if (w[s] != INF) best = std::min(best, w[s] - j * g);
                prefix[j] = best;
                s = (s + r) % m;
            }
            suffix[L] = INF;
            for (int j = L - 1; j >= 0; --j) {
                suffix[j] = suffix[j + 1];
                if (w[cycle[j]] != INF)
                    suffix[j] = std::min(suffix[j], w[cycle[j]] - j * g);
            }
            for (int j = 0; j < L; ++j) {
                i64 value = INF;
                if (prefix[j] != INF) value = prefix[j] + j * g;
                if (suffix[j + 1] != INF)
                    value = std::min(value, suffix[j + 1] + (j + L) * g);
                next[cycle[j]] = value;
            }
        }
        w.swap(next);
    }
    return w;
}

// Independent shortest-path implementation: it does not use generator-addition
// scans or their prefix/suffix recurrences.
inline std::vector<i64> dijkstra_heap(int m, const std::vector<i64>& G) {
    validate_inputs(m, G);
    using Item = std::pair<i64, int>;
    std::priority_queue<Item, std::vector<Item>, std::greater<Item>> heap;
    std::vector<i64> w(m, INF);
    w[0] = 0;
    heap.emplace(0, 0);
    while (!heap.empty()) {
        const auto item = heap.top();
        heap.pop();
        const i64 value = item.first;
        const int s = item.second;
        if (value != w[s]) continue;
        for (i64 g : G) {
            const int t = (s + static_cast<int>(g % m)) % m;
            const i64 candidate = value + g;
            if (candidate < w[t]) {
                w[t] = candidate;
                heap.emplace(candidate, t);
            }
        }
    }
    return w;
}

// Edge inequalities prove w is no greater than every attainable path cost.
// A strictly smaller tight predecessor for each finite nonroot proves the
// reverse inequality by descent to root 0. INF vertices are allowed, but an
// edge out of a finite vertex may not lead to INF.
inline bool certify(int m, const std::vector<i64>& G,
                    const std::vector<i64>& w, std::string* err = nullptr) {
    auto fail = [err](const std::string& message) {
        if (err) *err = message;
        return false;
    };
    try {
        validate_inputs(m, G);
    } catch (const std::exception& ex) {
        return fail(ex.what());
    }
    if (w.size() != static_cast<std::size_t>(m)) return fail("wrong table size");
    if (w[0] != 0) return fail("root distance must be zero");
    for (int s = 0; s < m; ++s) {
        if (w[s] == INF) continue;
        if (w[s] < 0 || w[s] >= INF) return fail("invalid finite distance");
        if (w[s] % m != s) return fail("distance has wrong residue");
    }
    std::vector<unsigned char> tight(m, 0);
    tight[0] = 1;
    for (int s = 0; s < m; ++s) {
        if (w[s] == INF) continue;
        for (i64 g : G) {
            const int t = (s + static_cast<int>(g % m)) % m;
            const i64 candidate = w[s] + g;
            if (w[t] == INF || w[t] > candidate)
                return fail("finite-source edge inequality fails");
            if (t != 0 && w[t] == candidate && w[s] < w[t]) tight[t] = 1;
        }
    }
    for (int s = 1; s < m; ++s)
        if (w[s] != INF && !tight[s])
            return fail("finite nonroot lacks a positive tight predecessor");
    if (err) err->clear();
    return true;
}

namespace detail {

inline void require_multiplicity(int m, const std::vector<i64>& G) {
    if (m == 1) return;
    for (i64 g : G)
        if (g <= m)
            throw std::invalid_argument("invariants/support require every G > m");
}

// A nonzero Apéry value is composite iff a tight generator edge reaches it
// from a nonzero source. This handles redundant supplied generators as well.
inline std::vector<int> primitive_residues(int m, const std::vector<i64>& G,
                                         const std::vector<i64>& w) {
    std::vector<unsigned char> composite(m, 0);
    for (int s = 1; s < m; ++s) {
        if (w[s] == INF) continue;
        for (i64 g : G) {
            const int t = (s + static_cast<int>(g % m)) % m;
            if (w[t] != INF && w[s] + g == w[t]) composite[t] = 1;
        }
    }
    std::vector<int> answer;
    for (int s = 1; s < m; ++s)
        if (w[s] != INF && !composite[s]) answer.push_back(s);
    return answer;
}

inline std::uint64_t hash_tile(const std::vector<int>& residues,
                               const std::vector<int>& words) {
    // FNV-1a on explicit little-endian uint32 entries, lengths included.
    std::uint64_t h = UINT64_C(14695981039346656037);
    auto append = [&h](std::uint32_t value) {
        for (int j = 0; j < 4; ++j) {
            h ^= static_cast<unsigned char>(value & 255U);
            h *= UINT64_C(1099511628211);
            value >>= 8;
        }
    };
    append(static_cast<std::uint32_t>(residues.size()));
    for (int x : residues) append(static_cast<std::uint32_t>(x));
    append(static_cast<std::uint32_t>(words.size()));
    for (int x : words) append(static_cast<std::uint32_t>(x));
    return h;
}

} // namespace detail

inline Basic invariants_impl(int m, const std::vector<i64>& G,
                             const std::vector<i64>& w,
                             std::vector<int>* primitive_output) {
    std::string err;
    if (!certify(m, G, w, &err)) throw std::invalid_argument("uncertified table: " + err);
    detail::require_multiplicity(m, G);
    Basic out;
    out.m = m;
    if (std::find(w.begin(), w.end(), INF) != w.end()) {
        out.e = 0;
        out.top = -1;
        out.finite = 0;
        out.c = out.g = out.W = INF;
        return out;
    }
    out.finite = 1;
    if (m == 1) {
        out.e = 1;
        return out; // N: conductor, genus and defect are all zero.
    }
    out.top = static_cast<int>(std::max_element(w.begin(), w.end()) - w.begin());
    auto primitives = detail::primitive_residues(m, G, w);
    out.e = 1 + static_cast<int>(primitives.size());
    if (primitive_output) *primitive_output = std::move(primitives);
    const i64 sum = std::accumulate(w.begin(), w.end(), i64(0));
    const i64 genus_numerator = sum - i64(m) * (m - 1) / 2;
    if (genus_numerator < 0 || genus_numerator % m != 0)
        throw std::logic_error("invalid Apéry genus numerator");
    out.g = genus_numerator / m;
    out.c = w[out.top] - m + 1;
    out.W = i64(out.e) * (out.c - out.g) - out.c;
    return out;
}

inline Basic invariants(int m, const std::vector<i64>& G,
                        const std::vector<i64>& w) {
    return invariants_impl(m, G, w, nullptr);
}

inline Support support(int m, const std::vector<i64>& G,
                       const std::vector<i64>& w, SupportTiming* timing = nullptr) {
    using SupportClock = std::chrono::steady_clock;
    auto stamp = timing ? SupportClock::now() : SupportClock::time_point{};
    if (timing) *timing = SupportTiming{};
    Support out;
    out.basic = invariants_impl(m, G, w, &out.residues);
    if (timing) {
        const auto now = SupportClock::now();
        timing->certification_ms = std::chrono::duration<double, std::milli>(now - stamp).count();
        stamp = now;
    }
    if (!out.basic.finite)
        throw std::invalid_argument("support requires a cofinite semigroup");
    out.minimal.push_back(m);
    out.gamma.assign(m, 0);
    if (m == 1) {
        out.tile_hash = detail::hash_tile(out.residues, out.words);
        return out;
    }
    // invariants_impl supplied the primitive list in increasing RESIDUE order.
    const int d = static_cast<int>(out.residues.size());
    for (int s : out.residues) out.minimal.push_back(w[s]);
    std::sort(out.minimal.begin(), out.minimal.end());
    if (d != out.basic.e - 1 || d == 0)
        throw std::logic_error("inconsistent primitive generator count");

    out.words.assign(static_cast<std::size_t>(m) * d, 0);
    std::vector<int> order(m);
    std::iota(order.begin(), order.end(), 0);
    std::sort(order.begin(), order.end(), [&w](int x, int y) { return w[x] < w[y]; });
    // Exact lex minimum, matching p39/verify_probe.py:factor_basis.
    // Positive generator values put every tight predecessor earlier in order.
    for (int s : order) {
        if (s == 0) continue;
        bool found = false;
        for (int j = 0; j < d; ++j) {
            const int r = out.residues[j];
            const int parent = (s - r + m) % m;
            if (w[parent] + w[r] != w[s]) continue;
            bool better = !found;
            if (found) {
                for (int k = 0; k < d; ++k) {
                    const int candidate = out.words[static_cast<std::size_t>(parent) * d + k] + (k == j);
                    const int old = out.words[static_cast<std::size_t>(s) * d + k];
                    if (candidate != old) { better = candidate < old; break; }
                }
            }
            if (better) {
                for (int k = 0; k < d; ++k)
                    out.words[static_cast<std::size_t>(s) * d + k] =
                        out.words[static_cast<std::size_t>(parent) * d + k] + (k == j);
                found = true;
            }
        }
        if (!found) throw std::logic_error("no primitive tight factorization");
    }

    if (timing) {
        const auto now = SupportClock::now();
        timing->canonical_ms = std::chrono::duration<double, std::milli>(now - stamp).count();
        stamp = now;
    }

    i64 gamma_sum = 0, weighted_deficit_residue = 0, weighted_height = 0;
    const int top = out.basic.top;
    const i64 M = w[top];
    for (int s = 0; s < m; ++s) {
        bool maximal = true;
        i64 axes = 0;
        for (int j = 0; j < d; ++j) {
            const int coordinate = out.words[static_cast<std::size_t>(s) * d + j];
            axes += (i64(coordinate) * out.residues[j]) % m;
            const int child = (s + out.residues[j]) % m;
            bool canonical_child = (w[s] + w[out.residues[j]] == w[child]);
            if (canonical_child) {
                for (int k = 0; k < d; ++k)
                    if (out.words[static_cast<std::size_t>(child) * d + k] !=
                        out.words[static_cast<std::size_t>(s) * d + k] + (k == j)) {
                        canonical_child = false;
                        break;
                    }
            }
            if (canonical_child) maximal = false;
            else out.gamma[s] += coordinate + 1;
        }
        out.kappa += axes / m;
        if (!maximal) out.Dep += out.gamma[s];
        gamma_sum += out.gamma[s];
        weighted_deficit_residue += i64(out.gamma[s]) * ((top - s + m) % m);
        weighted_height += i64(out.gamma[s]) * ((M - w[s]) / m);
    }
    if (gamma_sum != i64(d) * m)
        throw std::logic_error("canonical column mass identity failed");
    const i64 C = i64(d - 1) * m * (m - 1) / 2;
    const i64 phase_numerator = weighted_deficit_residue - C;
    if (phase_numerator % m != 0)
        throw std::logic_error("nonintegral phase budget");
    const i64 phase = phase_numerator / m;
    out.N = out.kappa + phase;
    out.Q = out.Dep + phase;
    out.R = weighted_height - out.Dep;
    if (out.N < 0 || out.R < 0 || out.basic.W != out.Q + out.R)
        throw std::logic_error("support identity or nonnegativity check failed");

    // Enumerate all TOP-RESIDUE phases. These are diagnostic phases, not claims
    // of realizable conductors with the fixed generators/tile.
    i64 at_zero_numerator = -C;
    for (int s = 0; s < m; ++s)
        at_zero_numerator += i64(out.gamma[s]) * ((m - s) % m);
    if (at_zero_numerator % m != 0)
        throw std::logic_error("nonintegral zero-phase budget");
    i64 q = out.Dep + at_zero_numerator / m;
    out.Qmin = q;
    out.min_phase = 0;
    if (top == 0 && q != out.Q) throw std::logic_error("actual phase mismatch");
    for (int r = 1; r < m; ++r) {
        q += d - out.gamma[r];
        if (q < out.Qmin) { out.Qmin = q; out.min_phase = r; }
        if (r == top && q != out.Q) throw std::logic_error("actual phase mismatch");
    }
    if (q + d - out.gamma[0] != out.Dep + at_zero_numerator / m)
        throw std::logic_error("phase sweep did not close");
    out.tile_hash = detail::hash_tile(out.residues, out.words);
    if (timing)
        timing->scoring_ms = std::chrono::duration<double, std::milli>(SupportClock::now() - stamp).count();
    return out;
}

} // namespace wilf
