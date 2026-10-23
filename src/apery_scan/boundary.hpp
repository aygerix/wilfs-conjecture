#pragma once

// E468: finitely many exact ray exits from ONE cached canonical tile. Include
// after apery.hpp and the driver helpers require/print_array/emit_case/
// safe_parallel/Clock/elapsed. This is not an enumeration of fan adjacency.
// A nonidentity row has RHS m if its first coefficient is negative OR its
// target is an old primitive and source!=0; otherwise RHS 0. The primitive
// guard is essential: lex-minimal words alone need not preserve actual e.
#include <map>
#include <set>

namespace boundary_detail {
using I = __int128;

inline i64 checked(I x) {
    require(x >= std::numeric_limits<i64>::min() && x <= std::numeric_limits<i64>::max(),
            "boundary exact-integer overflow");
    return static_cast<i64>(x);
}
struct Bound {
    bool finite = false;
    i64 value = 0;
};
inline void print_bound(Bound b) {
    if (b.finite) std::cout << b.value; else std::cout << "null";
}
inline bool update(Bound& b, i64 value) {
    require(value >= 1, "boundary first failure must be positive");
    if (!b.finite || value < b.value) { b = {true, value}; return true; }
    return false;
}
inline I dot(const std::vector<int>& row, const std::vector<i64>& P) {
    I result = 0;
    for (std::size_t j = 0; j < row.size(); ++j) result += I(row[j]) * P[j];
    return result;
}
inline i64 slope(const std::vector<int>& row, const std::vector<int>& v) {
    I result = 0;
    for (std::size_t j = 0; j < row.size(); ++j) result += I(row[j]) * v[j];
    return checked(result);
}
inline int height(const Support& s, int m) {
    const int d = s.basic.e - 1;
    int result = 0;
    for (int r = 0; r < m; ++r) {
        int degree = 0;
        for (int j = 0; j < d; ++j) degree += s.words[static_cast<std::size_t>(r)*d+j];
        result = std::max(result, degree);
    }
    return result;
}
inline bool cofactor_one(const Support& s) {
    for (std::size_t omitted = 0; omitted < s.minimal.size(); ++omitted) {
        i64 g = 0;
        for (std::size_t j = 0; j < s.minimal.size(); ++j)
            if (j != omitted) g = std::gcd(g, s.minimal[j]);
        if (g != 1) return false;
    }
    return true;
}
struct Row {
    std::vector<int> coefficients;
    int source = -1, generator = -1, target = -1;
    int rhs_units = 0; // actual primitive-value RHS is m*rhs_units
    i64 margin = 0;   // (row.P)/m-rhs_units
    bool primitive_guard = false;
};
struct Target {
    std::string reason;
    i64 t = 0;
    bool positive = false, range = false;
    int point = -1;
};
struct Direction {
    std::vector<int> v;
    Bound tile, top, positivity, range_max;
    int tile_row = -1, top_target = -1, positivity_coordinate = -1;
    i64 tile_slope = 0, top_slope = 0, top_margin = 0;
    std::vector<Target> targets;
};
struct Reference { int direction = -1; i64 t = 0; std::string reason; };
struct Point {
    std::vector<i64> P, w;
    std::vector<Reference> references;
    Support score;
    bool evaluated = false, finite = false, domain = false, cofactor1 = false, eligible = false;
    bool same_tile = false;
    int height = 0, code = 0;
};
inline void print_reference(const Reference& r) {
    std::cout << "{\"direction_id\":" << r.direction << ",\"t\":" << r.t
              << ",\"reason\":\"" << r.reason << "\"}";
}
inline void print_row(const Row& row, i64 row_slope, int m) {
    std::cout << "{\"source\":" << row.source << ",\"generator_index\":" << row.generator
              << ",\"target\":" << row.target << ",\"row\":";
    print_array(row.coefficients);
    std::cout << ",\"threshold\":" << m*row.rhs_units << ",\"margin_units\":" << row.margin
              << ",\"slope_units\":" << row_slope << ",\"primitive_guard\":"
              << (row.primitive_guard ? "true" : "false") << '}';
}
} // namespace boundary_detail

inline int boundary_probe(int threads, int m, const std::vector<i64>& input) {
    using namespace boundary_detail;
    require(threads >= 1 && threads <= 128 && m == 63,
            "E468 is restricted to the single cached m63 endpoint");
    const auto started = Clock::now();
    const auto origin_w = scan_cpu(m, input);
    require(origin_w == dijkstra_heap(m, input), "boundary origin heap mismatch");
    const auto origin = support(m, input, origin_w);
    std::vector<i64> P;
    for (int r : origin.residues) P.push_back(origin_w[r]);
    auto sorted_P = P;
    std::sort(sorted_P.begin(), sorted_P.end());
    const std::vector<i64> cached = {307,438,440,454,461,474,475,477,482,486,492};
    require(sorted_P == cached, "E468 supplied source is not the approved cached endpoint");
    const int d = static_cast<int>(P.size());
    require(d == 11 && origin.basic.e >= 4 && 3*origin.basic.e < m && origin.basic.c > 4LL*m &&
            cofactor_one(origin) && height(origin,m) >= 3,
            "boundary origin fails the scoped domain gates");
    require(scan_cpu(m,P) == origin_w, "actual primitive extraction changed origin");

    std::vector<Row> rows;
    std::vector<bool> primitive(m, false);
    for (int r : origin.residues) primitive[r] = true;
    int primitive_guard_rows = 0;
    for (int s = 0; s < m; ++s) for (int j = 0; j < d; ++j) {
        Row row;
        row.source = s; row.generator = j; row.target = (s+origin.residues[j])%m;
        row.coefficients.resize(d);
        int first = 0;
        for (int k = 0; k < d; ++k) {
            const int coefficient = origin.words[static_cast<std::size_t>(s)*d+k] + (k==j)
                                  - origin.words[static_cast<std::size_t>(row.target)*d+k];
            row.coefficients[k] = coefficient;
            if (!first && coefficient) first = coefficient;
        }
        if (!first) continue; // canonical addition: an identity row
        row.primitive_guard = s != 0 && primitive[row.target];
        row.rhs_units = first < 0 || row.primitive_guard;
        primitive_guard_rows += row.primitive_guard;
        const I value = dot(row.coefficients,P);
        require(value % m == 0, "boundary row has nonzero residue");
        row.margin = checked(value/m-row.rhs_units);
        require(row.margin >= 0, "origin violates an E455 row");
        rows.push_back(std::move(row));
    }

    std::vector<Direction> directions;
    for (int j = 0; j < d; ++j) for (int sign : {-1,1}) {
        Direction dir; dir.v.assign(d,0); dir.v[j]=sign; directions.push_back(std::move(dir));
    }
    for (int j = 0; j < d; ++j) for (int k = j+1; k < d; ++k)
        for (int a : {-1,1}) for (int b : {-1,1}) {
            Direction dir; dir.v.assign(d,0); dir.v[j]=a; dir.v[k]=b;
            directions.push_back(std::move(dir));
        }
    require(directions.size() == static_cast<std::size_t>(2*d*d) && directions.size() == 242,
            "boundary direction budget mismatch");
    const i64 safe_max = checked((I(INF)-1)/(I(8)*m*m));
    std::vector<Point> points;
    std::map<std::vector<i64>,int> seen;
    int target_count = 0, positive_count = 0, range_count = 0, duplicate_count = 0;
    for (int id = 0; id < static_cast<int>(directions.size()); ++id) {
        auto& dir = directions[id];
        for (int ri = 0; ri < static_cast<int>(rows.size()); ++ri) {
            const i64 a = slope(rows[ri].coefficients,dir.v);
            if (a < 0 && update(dir.tile,checked(I(rows[ri].margin)/(-I(a))+1))) {
                dir.tile_row=ri; dir.tile_slope=a;
            }
        }
        for (int s = 0; s < m; ++s) if (s != origin.basic.top) {
            std::vector<int> row(d);
            for (int j = 0; j < d; ++j)
                row[j] = origin.words[static_cast<std::size_t>(origin.basic.top)*d+j]
                         - origin.words[static_cast<std::size_t>(s)*d+j];
            const int distance = (origin.basic.top-s+m)%m;
            const I value = dot(row,P)-distance;
            require(value >= 0 && value%m == 0, "origin actual-top margin is invalid");
            const i64 margin=checked(value/m), a=slope(row,dir.v);
            if (a < 0 && update(dir.top,checked(I(margin)/(-I(a))+1))) {
                dir.top_target=s; dir.top_slope=a; dir.top_margin=margin;
            }
        }
        for (int j = 0; j < d; ++j) {
            if (dir.v[j] < 0) {
                const i64 first=checked((I(P[j])-m-1)/(-I(m)*dir.v[j])+1);
                if (update(dir.positivity,first)) dir.positivity_coordinate=j;
            } else if (dir.v[j] > 0) {
                const i64 maximum=checked((I(safe_max)-P[j])/(I(m)*dir.v[j]));
                require(maximum >= 0, "origin exceeds boundary numeric range");
                if (!dir.range_max.finite || maximum < dir.range_max.value)
                    dir.range_max={true,maximum};
            }
        }
        auto add_target = [&](const std::string& reason, i64 t) {
            if (t <= 0) return;
            ++target_count;
            Target target; target.reason=reason; target.t=t;
            target.positive=!dir.positivity.finite || t<dir.positivity.value;
            target.range=!dir.range_max.finite || t<=dir.range_max.value;
            positive_count+=target.positive;
            range_count+=target.positive && target.range;
            if (target.positive && target.range) {
                std::vector<i64> next(d);
                for (int j = 0; j < d; ++j) {
                    next[j]=checked(I(P[j])+I(m)*t*dir.v[j]);
                    require(next[j]>m && next[j]<=safe_max, "boundary candidate range error");
                }
                const auto inserted=seen.emplace(next,static_cast<int>(points.size()));
                target.point=inserted.first->second;
                if (inserted.second) { Point point; point.P=std::move(next); points.push_back(std::move(point)); }
                else ++duplicate_count;
                points[target.point].references.push_back({id,t,reason});
            }
            dir.targets.push_back(std::move(target));
        };
        if (dir.tile.finite) {
            add_target("tile_before",dir.tile.value-1);
            add_target("tile_exit",dir.tile.value);
        }
        if (dir.top.finite && (!dir.tile.finite || dir.top.value<dir.tile.value))
            add_target("top_exit",dir.top.value);
    }
    require(target_count <= 726 && points.size() <= 726, "boundary proposal budget exceeded");

    emit_case("boundary_origin",m,P,origin_w,origin);
    std::cout << "{\"kind\":\"boundary_setup\",\"m\":" << m << ",\"d\":" << d
              << ",\"provided_input\":"; print_array(input);
    std::cout << ",\"origin_P\":"; print_array(P);
    std::cout << ",\"origin_residues\":"; print_array(origin.residues);
    std::cout << ",\"origin_top\":" << origin.basic.top << ",\"origin_height\":" << height(origin,m)
              << ",\"origin_F\":" << origin.kappa-origin.Dep << ",\"canonical_row_count\":" << rows.size()
              << ",\"primitive_guard_rows\":" << primitive_guard_rows
              << ",\"primitive_guard_in_t_D\":true,\"t_D_tracks\":\"canonical_tile_and_actual_e\""
              << ",\"direction_count\":" << directions.size()
              << ",\"target_count\":" << target_count << ",\"positive_targets\":" << positive_count
              << ",\"range_valid_targets\":" << range_count << ",\"duplicate_targets\":" << duplicate_count
              << ",\"unique_points\":" << points.size() << ",\"proposal_cap\":726,\"cpu_threads\":" << threads
              << ",\"t_T_interpretation\":\"original_tile_top_row_failure; actual only before t_D and positivity exit\""
              << ",\"stop_policy\":\"ordered_batches_W_then_Q_then_F\",\"universal_sign_claim\":false}\n";
    for (int id=0; id<static_cast<int>(directions.size()); ++id) {
        const auto& dir=directions[id];
        std::cout << "{\"kind\":\"boundary_direction\",\"direction_id\":" << id << ",\"v\":";
        print_array(dir.v);
        std::cout << ",\"t_D\":"; print_bound(dir.tile);
        std::cout << ",\"t_T\":"; print_bound(dir.top);
        std::cout << ",\"top_exit_before_tile\":"
                  << (dir.top.finite && (!dir.tile.finite || dir.top.value<dir.tile.value)?"true":"false");
        std::cout << ",\"first_nonpositive_generator_t\":"; print_bound(dir.positivity);
        std::cout << ",\"positivity_coordinate\":" << dir.positivity_coordinate
                  << ",\"maximum_range_t\":"; print_bound(dir.range_max);
        std::cout << ",\"exit_witness_type\":\""
                  << (dir.tile_row<0?"none":rows[dir.tile_row].primitive_guard?"primitive_redundancy":"canonical_word")
                  << "\",\"tile_witness\":";
        if (dir.tile_row>=0) print_row(rows[dir.tile_row],dir.tile_slope,m); else std::cout << "null";
        std::cout << ",\"top_witness\":";
        if (dir.top_target>=0)
            std::cout << "{\"target\":" << dir.top_target << ",\"distance\":"
                      << (origin.basic.top-dir.top_target+m)%m << ",\"margin_units\":" << dir.top_margin
                      << ",\"slope_units\":" << dir.top_slope << '}';
        else std::cout << "null";
        std::cout << ",\"targets\":[";
        for (std::size_t j=0;j<dir.targets.size();++j) {
            const auto& target=dir.targets[j];
            std::cout << (j?",":"") << "{\"reason\":\"" << target.reason << "\",\"t\":" << target.t
                      << ",\"within_positive\":" << (target.positive?"true":"false")
                      << ",\"within_range\":" << (target.range?"true":"false") << ",\"point_id\":";
            if (target.point>=0) std::cout << target.point; else std::cout << "null";
            std::cout << '}';
        }
        std::cout << "]}\n";
    }
    std::cout << std::flush;

    int evaluated=0, promoted=-1, promotion_code=0;
    int stop_batch_begin=-1, stop_batch_size=0, first_discovery=-1;
    auto priority=[](int code){return code==4?3:code==3?2:code==5?1:0;};
    for (int begin=0;begin<static_cast<int>(points.size());begin+=threads) {
        const int count=std::min(threads,static_cast<int>(points.size())-begin);
        safe_parallel(count,threads,[&](int offset) {
            auto& point=points[begin+offset];
            point.w=scan_cpu(m,point.P);
            point.evaluated=true;
            point.finite=std::find(point.w.begin(),point.w.end(),INF)==point.w.end();
            if (!point.finite) return;
            point.score=support(m,point.P,point.w);
            const auto& b=point.score.basic;
            point.height=height(point.score,m);
            point.cofactor1=cofactor_one(point.score);
            point.domain=b.e>=4 && 3*b.e<m && b.c>4LL*m;
            point.eligible=point.domain && point.cofactor1 && point.height>=3;
            point.same_tile=point.score.residues==origin.residues && point.score.words==origin.words;
            if (b.W<0) point.code=4;
            else if (point.eligible && point.score.Q<0) point.code=3;
            else if (point.eligible && point.score.kappa-point.score.Dep>0) point.code=5;
        });
        evaluated+=count;
        for (int i=begin;i<begin+count;++i)
            if (priority(points[i].code)>priority(promotion_code)) {promoted=i;promotion_code=points[i].code;}
        if (promotion_code) {
            stop_batch_begin=begin; stop_batch_size=count;
            for(int i=begin;i<begin+count;++i)if(points[i].code){first_discovery=i;break;}
            break;
        }
    }
    int finite=0, eligible=0, best_F=-1, min_Q=-1, min_ratio=-1;
    for (int id=0;id<static_cast<int>(points.size());++id) {
        const auto& point=points[id];
        if (point.evaluated) {finite+=point.finite; eligible+=point.eligible;}
        if (point.eligible) {
            const auto& s=point.score;
            if (best_F<0 || s.kappa-s.Dep>points[best_F].score.kappa-points[best_F].score.Dep) best_F=id;
            if (min_Q<0 || s.Q<points[min_Q].score.Q) min_Q=id;
            if (min_ratio<0 || I(s.basic.W)*points[min_ratio].score.basic.c<
                               I(points[min_ratio].score.basic.W)*s.basic.c) min_ratio=id;
        }
        std::cout << "{\"kind\":\"boundary_point\",\"point_id\":" << id << ",\"P\":";
        print_array(point.P);
        const auto& reference=point.references.front();
        std::cout << ",\"v\":"; print_array(directions[reference.direction].v);
        std::cout << ",\"t\":" << reference.t << ",\"references\":[";
        for (std::size_t j=0;j<point.references.size();++j) {
            if(j)std::cout<<',';
            print_reference(point.references[j]);
        }
        std::cout << "],\"evaluated\":" << (point.evaluated?"true":"false") << ",\"finite\":";
        if(point.evaluated)std::cout<<(point.finite?"true":"false");else std::cout<<"null";
        if (point.finite) {
            const auto& s=point.score;
            std::cout << ",\"e\":" << s.basic.e << ",\"c\":" << s.basic.c << ",\"g\":" << s.basic.g
                      << ",\"W\":" << s.basic.W << ",\"Dep\":" << s.Dep << ",\"kappa\":" << s.kappa
                      << ",\"N\":" << s.N << ",\"Q\":" << s.Q << ",\"R\":" << s.R
                      << ",\"F\":" << s.kappa-s.Dep << ",\"top\":" << s.basic.top
                      << ",\"height\":" << point.height << ",\"actual_generators\":";
            print_array(s.minimal);
            std::cout << ",\"primitive_residues\":";print_array(s.residues);
            std::cout << ",\"embedding_gate\":" << (s.basic.e>=4?"true":"false")
                      << ",\"sparse_gate\":" << (3*s.basic.e<m?"true":"false")
                      << ",\"deep_gate\":" << (s.basic.c>4LL*m?"true":"false")
                      << ",\"height_gate\":" << (point.height>=3?"true":"false")
                      << ",\"domain_gate\":" << (point.domain?"true":"false")
                      << ",\"cofactor1\":" << (point.cofactor1?"true":"false")
                      << ",\"eligible\":" << (point.eligible?"true":"false")
                      << ",\"same_tile\":" << (point.same_tile?"true":"false")
                      << ",\"same_top_residue\":" << (s.basic.top==origin.basic.top?"true":"false")
                      << ",\"tile_hash\":\"" << s.tile_hash << '\"';
        }
        std::cout << ",\"promotion_code\":" << point.code << "}\n";
    }
    auto emit_point=[&](const char* kind,int id) {
        if(id<0)return;
        const auto& point=points[id];
        require(point.w==dijkstra_heap(m,point.P),"boundary selected point heap mismatch");
        emit_case(kind,m,point.P,point.w,point.score);
    };
    emit_point("boundary_best_F",best_F);
    emit_point("boundary_min_Q",min_Q);
    emit_point("boundary_min_W_ratio",min_ratio);
    if(promoted>=0)emit_point(promotion_code==4?"negative_W_candidate":promotion_code==3?
                            "negative_Q_candidate":"support_resistant_candidate",promoted);
    std::cout << "{\"kind\":\"boundary_complete\",\"directions\":" << directions.size()
              << ",\"target_count\":" << target_count << ",\"unique_points\":" << points.size()
              << ",\"evaluated\":" << evaluated << ",\"cofinite\":" << finite
              << ",\"eligible\":" << eligible << ",\"unevaluated\":" << points.size()-evaluated
              << ",\"positivity_skipped_targets\":" << target_count-positive_count
              << ",\"range_skipped_targets\":" << positive_count-range_count
              << ",\"complete\":" << (evaluated==static_cast<int>(points.size())?"true":"false")
              << ",\"status\":\"" << (promotion_code?"discovery_stop":"complete") << "\",\"cap_status\":\""
              << (range_count==positive_count?"no_numeric_truncation":"numeric_range_skips")
              << "\",\"best_F_point\":" << best_F << ",\"min_Q_point\":" << min_Q
              << ",\"min_W_ratio_point\":" << min_ratio << ",\"promoted_point\":" << promoted
              << ",\"promotion_code\":" << promotion_code << ",\"stop_batch_begin\":" << stop_batch_begin
              << ",\"stop_batch_size\":" << stop_batch_size << ",\"first_discovery_point\":" << first_discovery
              << ",\"evaluated_after_first_discovery\":"
              << (first_discovery<0?0:stop_batch_begin+stop_batch_size-first_discovery-1)
              << ",\"wall_ms\":" << elapsed(started)
              << ",\"full_fan_adjacency_claim\":false,\"universal_sign_claim\":false}\n" << std::flush;
    return promotion_code;
}
