#pragma once
// Exact two-atom coverage diagnostic; mathematical criterion is valid for all m.
// This bitset implementation supports m<=64 and is not a global Wilf verifier.
#include <set>

inline std::uint64_t exchange_mask(int m) {
    return m==64?~UINT64_C(0):(UINT64_C(1)<<m)-1;
}
inline std::uint64_t exchange_rotate(std::uint64_t bits,int shift,int m) {
    shift%=m;
    if(!shift)return bits;
    return ((bits<<shift)|(bits>>(m-shift)))&exchange_mask(m);
}
inline std::uint64_t exchange_bits(const std::vector<int>& A) {
    std::uint64_t bits=0;for(int a:A)bits|=UINT64_C(1)<<a;return bits;
}
inline std::uint64_t exchange_sums(const std::vector<int>& A,int m) {
    const auto bits=exchange_bits(A);std::uint64_t out=0;
    for(int a:A)out|=exchange_rotate(bits,a,m);
    return out;
}
inline int exchange_count(std::uint64_t bits) {return __builtin_popcountll(bits);}

int exchange_audit(int threads,int m,const std::vector<i64>& anchor) {
    require(m>=3 && m<=64 && threads>=1 && threads<=128,"invalid exchange shape");
    const auto oldw=scan_cpu(m,anchor);const auto old=support(m,anchor,oldw);
    std::vector<int>A{0};A.insert(A.end(),old.residues.begin(),old.residues.end());
    const int k=static_cast<int>(A.size()),d=k-1;
    require(k>=3 && 3*k<m,"exchange requires sparse generator domain");
    require(exchange_sums(A,m)==exchange_mask(m),"anchor must be a full pair cover");
    std::vector<int> outside;
    for(int s=0;s<m;++s)if(!std::binary_search(A.begin(),A.end(),s))outside.push_back(s);
    const std::uint64_t expected=static_cast<std::uint64_t>(d)*(d-1)/2*outside.size()*(outside.size()-1)/2;
    require(expected<=2000000,"exact exchange proposal cap exceeded");
    std::set<std::vector<int>> orbit;
    for(int unit=1;unit<m;++unit)if(std::gcd(unit,m)==1)for(int pivot:A) {
        std::vector<int> image;for(int a:A)image.push_back((unit*((a-pivot+m)%m))%m);
        std::sort(image.begin(),image.end());orbit.insert(image);
    }
    const auto started=Clock::now();
    std::vector<std::uint64_t> histogram(m+1,0);
    std::vector<std::vector<int>> full,onehole;
    std::uint64_t proposals=0,full_in_orbit=0;
    for(int i=1;i<k;++i)for(int j=i+1;j<k;++j) {
        std::vector<int>B;for(int a:A)if(a!=A[i] && a!=A[j])B.push_back(a);
        const auto bits=exchange_bits(B),pair=exchange_sums(B,m);
        for(size_t c=0;c<outside.size();++c)for(size_t e=c+1;e<outside.size();++e) {
            const int x=outside[c],y=outside[e];
            const auto coverage=pair|exchange_rotate(bits,x,m)|exchange_rotate(bits,y,m)|
                (UINT64_C(1)<<((2*x)%m))|(UINT64_C(1)<<((x+y)%m))|(UINT64_C(1)<<((2*y)%m));
            const int count=exchange_count(coverage);++histogram[count];++proposals;
            if(count<m-1)continue;
            auto next=B;next.push_back(x);next.push_back(y);std::sort(next.begin(),next.end());
            require(exchange_sums(next,m)==coverage,"two-atom hole criterion disagrees with direct sums");
            if(count==m){full_in_orbit+=orbit.count(next);full.push_back(std::move(next));}
            else {
                // A one-hole pair basis is automatically a full triple basis.
                std::uint64_t triple=0;for(int a:next)triple|=exchange_rotate(coverage,a,m);
                require(triple==exchange_mask(m),"one-hole triple repair failed");
                onehole.push_back(std::move(next));
            }
        }
    }
    require(proposals==expected,"two-atom enumeration coverage mismatch");
    std::sort(full.begin(),full.end());std::sort(onehole.begin(),onehole.end());
    require(std::adjacent_find(onehole.begin(),onehole.end())==onehole.end(),"duplicate two-atom result");
    const double coverage_ms=elapsed(started);
    std::cout<<"{\"kind\":\"two_atom_coverage\",\"m\":"<<m<<",\"old_atoms\":";print_array(A);
    std::cout<<",\"exact_distance\":2,\"proposals\":"<<proposals<<",\"coverage_histogram\":";print_array(histogram);
    std::cout<<",\"affine_orbit_size\":"<<orbit.size()<<",\"full_covers\":"<<full.size()
             <<",\"full_covers_in_old_affine_orbit\":"<<full_in_orbit<<",\"one_hole_covers\":"<<onehole.size()
             <<",\"coverage_wall_ms\":"<<coverage_ms<<",\"full_cover_sets\":[";
    for(size_t i=0;i<full.size();++i){if(i)std::cout<<',';print_array(full[i]);}
    std::cout<<"],\"one_hole_sets\":[";
    for(size_t i=0;i<onehole.size();++i){if(i)std::cout<<',';print_array(onehole[i]);}
    std::cout<<"]}\n"<<std::flush;
    struct Result {Support score;std::vector<i64> G,w;int height=0,type=0;bool checked=false;};
    std::vector<Result> results(onehole.size());std::atomic<bool> discovery{false};
    const auto scoring_started=Clock::now();
    safe_parallel(static_cast<int>(onehole.size()),threads,[&](int i) {
        if(discovery.load())return;
        auto& r=results[i];for(int atom:onehole[i])if(atom)r.G.push_back(3LL*m+atom);
        r.w=scan_cpu(m,r.G);r.score=support(m,r.G,r.w);r.checked=true;
        require(r.score.basic.e==k && r.score.basic.c>4LL*m,"one-hole uniform realization changed e/depth");
        int cubics=0;
        for(int s=0;s<m;++s) {
            int degree=0,nonzero=0;
            for(int t=0;t<d;++t){const int value=r.score.words[static_cast<size_t>(s)*d+t];degree+=value;nonzero+=value>0;}
            r.height=std::max(r.height,degree);if(degree==3){++cubics;r.type=nonzero;}
        }
        require(r.height==3 && cubics==1,"one-hole construction did not give exactly one cubic");
        if(r.score.basic.W<0 || r.score.Q<0 || r.score.kappa>r.score.Dep)discovery=true;
    });
    int checked=0,best=-1,promoted=-1,code=0;std::vector<int>types(4,0);
    i64 maximum=std::numeric_limits<i64>::min();
    for(int i=0;i<static_cast<int>(results.size());++i) {
        const auto& r=results[i];if(!r.checked)continue;++checked;++types[r.type];
        const i64 F=r.score.kappa-r.score.Dep;
        if(F>maximum){maximum=F;best=i;}
        const int next=r.score.basic.W<0?4:r.score.Q<0?3:F>0?5:0;
        auto priority=[](int c){return c==4?3:c==3?2:c==5?1:0;};
        if(priority(next)>priority(code)){code=next;promoted=i;}
    }
    std::cout<<"{\"kind\":\"one_hole_realizations\",\"m\":"<<m<<",\"uniform_height\":3,\"available\":"<<onehole.size()
             <<",\"evaluated\":"<<checked<<",\"cubic_support_histogram\":";print_array(types);
    std::cout<<",\"maximum_F\":";if(checked)std::cout<<maximum;else std::cout<<"null";
    std::cout<<",\"scoring_wall_ms\":"<<elapsed(scoring_started)<<",\"promoted_exit\":"<<code
             <<",\"universal_sign_claim\":false}\n"<<std::flush;
    const int selected=promoted>=0?promoted:best;
    if(selected>=0) {
        const auto& r=results[selected];require(r.w==dijkstra_heap(m,r.G),"exchange selected heap audit failed");
        emit_case(code==4?"negative_W_candidate":code==3?"negative_Q_candidate":code==5?"support_resistant_candidate":"exchange_best",m,r.G,r.w,r.score);
    }
    return code;
}
