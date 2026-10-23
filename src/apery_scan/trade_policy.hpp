#pragma once
// E459: one bounded source-trade policy, not a complete augmentation algorithm.
// Include after apery.hpp, driver helpers and adaptive.hpp. No GPU dependency.
#include <set>
#include <map>
#include <tuple>

namespace trade_policy_detail {
using Word=std::vector<int>;
using Tile=std::set<Word>;
struct Step { std::string kind; Word x,y; i64 sigma=0,copies=0,credit=0; };
struct Result {
    int m=0,a=0; Basic basic; std::vector<i64> G,actual,w,P,beta,U;
    Tile initial,final; std::vector<Step> steps;
    i64 M=0,initial_L=0,final_L=0,total_credit=0;
    int corner_steps=0,terminal_positive_corners=-1;
    bool evaluated=false,accepted=false,cofactor1=false;
    std::string status="not_evaluated",reason;
};
inline i64 checked(__int128 value) {
    require(value>=std::numeric_limits<i64>::min() && value<=std::numeric_limits<i64>::max(),"trade integer overflow");
    return static_cast<i64>(value);
}
inline i64 cost(const Word& z,const std::vector<i64>& P) {
    __int128 result=0;for(std::size_t j=0;j<P.size();++j)result+=static_cast<__int128>(z[j])*P[j];return checked(result);
}
inline Word unit(int d,int j){Word z(d,0);z[j]=1;return z;}
inline bool below(const Word& x,const Word& z){for(std::size_t j=0;j<x.size();++j)if(x[j]>z[j])return false;return true;}
inline std::vector<Word> audit(const Tile& D,int a,const std::vector<i64>& P,bool all_units=false) {
    const int d=static_cast<int>(P.size());require(D.size()==static_cast<std::size_t>(a),"trade tile size changed");
    std::vector<Word> by_residue(a);std::vector<int> seen(a,0);
    for(const auto& z:D) {
        require(z.size()==P.size(),"trade word dimension changed");
        for(int j=0;j<d;++j){require(z[j]>=0,"negative trade exponent");if(z[j]){auto p=z;--p[j];require(D.count(p),"trade update broke downward closure");}}
        const int r=cost(z,P)%a;require(!seen[r],"trade update duplicated residue");seen[r]=1;by_residue[r]=z;
    }
    require(D.count(Word(d,0)),"trade tile lost zero");
    if(all_units)for(int j=0;j<d;++j)require(D.count(unit(d,j)),"trade tile lost a source unit");
    return by_residue;
}
inline i64 potential(const Tile& D,int a,const std::vector<i64>& P,i64 M,int e) {
    __int128 sum=0;for(const auto& z:D)sum+=cost(z,P);
    const __int128 numerator=static_cast<__int128>(2)*a*(e-1)*M-static_cast<__int128>(2)*e*sum-
        static_cast<__int128>(a)*(e-2)*(a-1);
    require(numerator%(2*a)==0,"nonintegral constructed Wilf bound");return checked(numerator/(2*a));
}
inline i64 copies(const Word& z,const Word& x) {
    i64 q=std::numeric_limits<i64>::max();for(std::size_t j=0;j<x.size();++j)if(x[j])q=std::min(q,i64(z[j]/x[j]));
    require(q!=std::numeric_limits<i64>::max(),"zero source-trade input");return q;
}
inline std::vector<Step> corners(const Tile& D,int a,const std::vector<i64>& P) {
    const int d=P.size();const auto residues=audit(D,a,P,true);
    std::set<Word> maximal,border;
    for(const auto& z:D) {
        bool top=true;
        for(int j=0;j<d;++j) {
            auto y=z;++y[j];if(D.count(y)){top=false;continue;}
            bool minimal=true;
            for(int k=0;k<d && minimal;++k)if(y[k]){auto pred=y;--pred[k];minimal=D.count(pred);}
            if(minimal)border.insert(std::move(y));
        }
        if(top)maximal.insert(z);
    }
    std::vector<Step> options;
    for(const auto& y:border) {
        const auto& x=residues[cost(y,P)%a];if(!maximal.count(x))continue;
        const i64 difference=checked(static_cast<__int128>(cost(x,P))-cost(y,P));
        if(difference<=0)continue;
        require(difference%a==0,"corner residue/cost mismatch");
        options.push_back({"corner",x,y,difference/a,1,difference/a});
    }
    std::sort(options.begin(),options.end(),[](const Step& x,const Step& y){
        if(x.sigma!=y.sigma)return x.sigma>y.sigma;
        return x.x!=y.x?x.x<y.x:x.y<y.y;
    });
    return options;
}
inline Result evaluate(int m,const std::vector<i64>& G,bool filter) {
    Result r;r.m=m;r.G=G;r.evaluated=true;
    r.w=scan_cpu(m,G);std::vector<int> primitives;
    r.basic=invariants_impl(m,G,r.w,&primitives);
    if(!r.basic.finite){r.status="rejected";r.reason="noncofinite";return r;}
    r.actual.push_back(m);for(int s:primitives)r.actual.push_back(r.w[s]);std::sort(r.actual.begin(),r.actual.end());
    i64 pivot=0;for(i64 p:r.actual)if(p%2){pivot=p;break;}
    r.cofactor1=true;
    for(std::size_t j=0;j<r.actual.size();++j){i64 g=0;for(std::size_t k=0;k<r.actual.size();++k)if(k!=j)g=std::gcd(g,r.actual[k]);r.cofactor1&=g==1;}
    if(pivot<=0 || pivot>256){r.status=r.basic.W<0?"negative_W":"rejected";r.reason="least_odd_pivot_cap";return r;}
    r.a=static_cast<int>(pivot);
    if(filter && r.basic.W>=0 && (r.basic.e<4 || 3*r.basic.e>=m || r.basic.c<=4LL*m || !r.cofactor1)) {
        r.status="rejected";
        r.reason=r.basic.e<4?"embedding_dimension":3*r.basic.e>=m?"density_complement":
            r.basic.c<=4LL*m?"conductor_complement":"cofactor";
        return r;
    }
    r.accepted=true;r.M=r.basic.c+r.a-1;
    for(i64 p:r.actual)if(p!=r.a){r.P.push_back(p);r.beta.push_back((p-(p%2?r.a:0))/2);}
    const int d=r.P.size();require(d==r.basic.e-1,"source primitive count changed");
    r.U=scan_cpu(r.a,r.beta);require(std::find(r.U.begin(),r.U.end(),INF)==r.U.end(),"closure residue table not finite");
    std::string error;require(certify(r.a,r.beta,r.U,&error),"closure certificate: "+error);
    std::vector<Word> words(r.a,Word(d,0));std::vector<i64> chi(r.a,INF);chi[0]=0;
    std::vector<int> order(r.a);std::iota(order.begin(),order.end(),0);
    std::sort(order.begin(),order.end(),[&](int x,int y){return r.U[x]<r.U[y];});
    for(int s:order)if(s) {
        bool found=false;
        for(int j=0;j<d;++j) {
            const int p=(s-static_cast<int>(r.beta[j]%r.a)+r.a)%r.a;
            if(r.U[p]+r.beta[j]!=r.U[s])continue;
            auto candidate=words[p];++candidate[j];const i64 n=chi[p]+(r.P[j]%2);
            if(!found || n<chi[s] || (n==chi[s] && candidate<words[s])) {words[s]=std::move(candidate);chi[s]=n;found=true;}
        }
        require(found,"closure word has no tight source predecessor");
    }
    r.final=Tile(words.begin(),words.end());audit(r.final,r.a,r.P);r.initial=r.final;
    r.initial_L=r.final_L=potential(r.final,r.a,r.P,r.M,r.basic.e);
    require(r.final_L<=r.basic.W,"initial constructed bound exceeds actual Wilf defect");
    if(r.basic.W<0){r.status="negative_W";return r;}
    // Complete every missing unit, even if the bound becomes positive early.
    for(int pass=0;pass<d;++pass) {
        const auto residues=audit(r.final,r.a,r.P);int selected=-1;Step best;
        for(int j=0;j<d;++j)if(!r.final.count(unit(d,j))) {
            const Word x=residues[r.P[j]%r.a];const i64 diff=checked(static_cast<__int128>(cost(x,r.P))-r.P[j]);
            require(diff>0 && diff%r.a==0,"missing primitive lacks positive source trade");
            Step candidate{"unit",x,unit(d,j),diff/r.a,0,0};
            for(const auto& z:r.final)candidate.copies=checked(static_cast<__int128>(candidate.copies)+copies(z,x));
            candidate.credit=checked(static_cast<__int128>(candidate.sigma)*candidate.copies);
            if(selected<0 || candidate.credit>best.credit){selected=j;best=std::move(candidate);}
        }
        if(selected<0)break;
        Tile next;
        for(const auto& z:r.final) {
            const auto q=copies(z,best.x);auto y=z;
            for(int j=0;j<d;++j)y[j]-=static_cast<int>(q*best.x[j]);
            y[selected]+=static_cast<int>(q);require(next.insert(std::move(y)).second,"unit shadow map not injective");
        }
        for(int j=0;j<d;++j)if(r.final.count(unit(d,j)))require(next.count(unit(d,j)),"unit restoration lost a prior unit");
        const i64 old=r.final_L;r.final=std::move(next);audit(r.final,r.a,r.P);
        r.final_L=potential(r.final,r.a,r.P,r.M,r.basic.e);
        require(static_cast<__int128>(r.final_L)-old==static_cast<__int128>(r.basic.e)*best.credit,"unit shadow credit mismatch");
        require(r.final_L<=r.basic.W,"unit bound exceeds actual Wilf defect");
        r.total_credit=checked(static_cast<__int128>(r.total_credit)+best.credit);r.steps.push_back(std::move(best));
    }
    audit(r.final,r.a,r.P,true);
    while(r.final_L<0) {
        if(r.corner_steps>=1000){r.status="step_cap_unresolved";return r;}
        auto options=corners(r.final,r.a,r.P);
        if(options.empty()){r.terminal_positive_corners=0;r.status="negative_L_corner_stall";return r;}
        const Step step=options.front();const i64 old=r.final_L;
        require(r.final.erase(step.x)==1 && r.final.insert(step.y).second,"corner replacement failed");
        audit(r.final,r.a,r.P,true);r.final_L=potential(r.final,r.a,r.P,r.M,r.basic.e);
        require(static_cast<__int128>(r.final_L)-old==static_cast<__int128>(r.basic.e)*step.credit,"corner credit mismatch");
        require(r.final_L<=r.basic.W,"corner bound exceeds actual Wilf defect");
        r.total_credit=checked(static_cast<__int128>(r.total_credit)+step.credit);r.steps.push_back(step);++r.corner_steps;
    }
    r.status="nonnegative_L";return r;
}
inline void print_words(const Tile& D) {
    std::cout<<'[';bool first=true;for(const auto& z:D){if(!first)std::cout<<',';first=false;print_array(z);}std::cout<<']';
}
inline void emit(const Result& r) {
    if(r.basic.finite)emit_case("trade_source",r.m,r.G,r.w,support(r.m,r.G,r.w));
    std::cout<<"{\"kind\":\"trade_policy_trace\",\"m\":"<<r.m<<",\"a\":"<<r.a
        <<",\"actual_generators\":";print_array(r.actual);
    std::cout<<",\"P\":";print_array(r.P);std::cout<<",\"beta\":";print_array(r.beta);
    std::cout<<",\"closure_apery\":";print_array(r.U);std::cout<<",\"initial_words\":";print_words(r.initial);
    std::cout<<",\"final_words\":";print_words(r.final);
    std::cout<<",\"M_actual\":"<<r.M<<",\"initial_L\":"<<r.initial_L<<",\"final_L\":"<<r.final_L
        <<",\"total_credit\":"<<r.total_credit<<",\"corner_steps\":"<<r.corner_steps
        <<",\"terminal_positive_corners\":"<<r.terminal_positive_corners<<",\"status\":\""<<r.status
        <<"\",\"accepted\":"<<(r.accepted?"true":"false")<<",\"cofactor1\":"<<(r.cofactor1?"true":"false")
        <<",\"step_cap\":1000,\"credit_is_pivot_mass_not_W_increment\":true,\"steps\":[";
    for(std::size_t i=0;i<r.steps.size();++i){const auto& s=r.steps[i];if(i)std::cout<<',';
        std::cout<<"{\"kind\":\""<<s.kind<<"\",\"x\":";print_array(s.x);std::cout<<",\"y\":";print_array(s.y);
        std::cout<<",\"sigma\":"<<s.sigma<<",\"copies\":"<<s.copies<<",\"credit\":"<<s.credit<<'}';}
    std::cout<<"],\"universal_sign_claim\":false}\n"<<std::flush;
}
inline bool promoted(const Result& r){return r.evaluated && (r.basic.W<0 || r.status=="negative_L_corner_stall");}
inline auto structure(const Result& r) {
    std::vector<int> words;for(const auto& z:r.initial)words.insert(words.end(),z.begin(),z.end());
    std::vector<i64> residues;for(i64 p:r.P)residues.push_back(p%r.a);
    return std::make_tuple(r.m,r.a,r.basic.e,residues,words);
}
inline bool better(const Result& x,const Result& y) {
    if(x.final_L!=y.final_L)return x.final_L<y.final_L;
    if(x.initial_L!=y.initial_L)return x.initial_L<y.initial_L;
    const __int128 left=static_cast<__int128>(x.basic.W)*y.basic.c,right=static_cast<__int128>(y.basic.W)*x.basic.c;
    return left!=right?left<right:std::make_pair(x.m,x.G)<std::make_pair(y.m,y.G);
}
} // namespace trade_policy_detail

inline int trade_policy_case(int m,const std::vector<i64>& G) {
    auto r=trade_policy_detail::evaluate(m,G,false);trade_policy_detail::emit(r);
    return r.basic.W<0?4:r.status=="negative_L_corner_stall"?6:0;
}

inline int trade_policy_search(int threads) {
    using namespace trade_policy_detail;
    require(threads==7,"E459 finite policy search specifies seven CPU threads");
    struct Proposal {int m;std::vector<i64> G;};
    const std::vector<Proposal> anchors={
        {31,{33,101,103}},{39,{41,113,115}},{51,{53,149,151}},
        {63,{239,282,295,318,333,379,386,390,400,405,407}}};
    Random rng{4590};std::vector<Result> archive;Result best;bool have_best=false;
    std::set<std::pair<int,std::vector<i64>>> distinct;
    std::set<std::vector<i64>> distinct_sources;
    int total_proposed=0,total_evaluated=0,total_accepted=0,total_feedback=0,total_elites=0,total_caps=0;
    const auto started=Clock::now();
    std::cout<<"{\"kind\":\"trade_policy_search_setup\",\"seed\":4590,\"generations\":4,\"batch\":128,\"budget\":512"
        <<",\"threads\":"<<threads<<",\"m_min\":25,\"m_max\":96,\"raw_generator_count_min\":3,\"raw_generator_count_max\":11"
        <<",\"height_min\":1,\"height_max\":12,\"least_odd_pivot_cap\":256,\"actual_e_min\":4"
        <<",\"requires_3e_lt_m\":true,\"requires_c_gt_4m\":true,\"requires_cofactor1\":true"
        <<",\"state_cap\":32,\"representatives_per_structure_cap\":4,\"corner_step_cap\":1000"
        <<",\"unit_tie\":\"coordinate\",\"corner_tie\":\"input_then_output_lex\",\"universal_sign_claim\":false}\n"<<std::flush;
    for(int generation=0;generation<4;++generation) {
        std::vector<Proposal> proposals(128);int feedback=0,migrants=0,elites=0;
        for(int i=0;i<128;++i) {
            if(generation==0 && i<4){proposals[i]=anchors[i];continue;}
            if(generation>0 && i<std::min(8,static_cast<int>(archive.size()))) {
                proposals[i]={archive[i].m,archive[i].G};++elites;continue;
            }
            if(generation==0 || i%8==7 || archive.empty()) {
                const int m=25+rng.next()%72,k=3+rng.next()%9;
                proposals[i]={m,adaptive_migrant(rng,m,k)};++migrants;continue;
            }
            const auto x=rng.next()%archive.size(),y=rng.next()%archive.size();
            const auto& parent=archive[std::min(x,y)];Proposal p{parent.m,parent.G};++feedback;
            const int mode=rng.next()%100;
            if(mode<15) {
                const int next_m=25+rng.next()%72;
                for(auto& value:p.G)value=adaptive_value(next_m,value/p.m,(value%p.m)%next_m);
                p.m=next_m;
            } else if(mode<30) {
                const bool add=p.G.size()==3 || (p.G.size()<11 && rng.next()%2);
                if(add){const i64 h=1+rng.next()%12;const int residue=rng.next()%p.m;p.G.push_back(adaptive_value(p.m,h,residue));}
                else p.G.erase(p.G.begin()+rng.next()%p.G.size());
            } else {int operation=0;p.G=adaptive_mutate(rng,p.m,p.G,operation);}
            proposals[i]=std::move(p);
        }
        total_proposed+=128;total_feedback+=feedback;total_elites+=elites;
        std::vector<Result> results(128);std::atomic<int> first_promotion{-1};
        safe_parallel(128,threads,[&](int i){
            if(first_promotion.load()>=0)return;
            results[i]=evaluate(proposals[i].m,proposals[i].G,true);
            if(promoted(results[i])){int empty=-1;first_promotion.compare_exchange_strong(empty,i);}
        });
        int evaluated=0,accepted=0,caps=0;std::vector<Result> pool=archive;
        std::map<std::string,int> rejection_reasons;
        for(int i=0;i<128;++i)if(results[i].evaluated) {
            ++evaluated;auto signature=proposals[i].G;std::sort(signature.begin(),signature.end());distinct.insert({proposals[i].m,std::move(signature)});
            if(results[i].basic.finite)distinct_sources.insert(results[i].actual);
            if(!results[i].accepted)++rejection_reasons[results[i].reason];
            if(results[i].accepted){++accepted;caps+=results[i].status=="step_cap_unresolved";
                if(!have_best || better(results[i],best)){best=results[i];have_best=true;}pool.push_back(results[i]);}
        }
        total_evaluated+=evaluated;total_accepted+=accepted;total_caps+=caps;
        std::sort(pool.begin(),pool.end(),better);archive.clear();
        using Key=decltype(structure(best));std::map<Key,int> per_structure;
        std::set<std::pair<Key,std::vector<i64>>> states;
        for(auto& r:pool) {
            const auto key=structure(r);std::vector<i64> heights;for(i64 p:r.P)heights.push_back(p/r.a);
            if(per_structure[key]>=4 || !states.insert({key,heights}).second)continue;
            ++per_structure[key];archive.push_back(std::move(r));if(archive.size()==32)break;
        }
        std::cout<<"{\"kind\":\"trade_policy_generation\",\"generation\":"<<generation<<",\"seed\":4590"
            <<",\"proposed\":128,\"evaluated\":"<<evaluated<<",\"accepted\":"<<accepted
            <<",\"parent_dependent_proposals\":"<<feedback<<",\"elites\":"<<elites<<",\"migrants\":"<<migrants
            <<",\"archive_states\":"<<archive.size()<<",\"archive_structures\":"<<per_structure.size()
            <<",\"unresolved_caps\":"<<caps<<",\"total_proposed\":"<<total_proposed<<",\"total_evaluated\":"<<total_evaluated
            <<",\"distinct_supplied_states\":"<<distinct.size()<<",\"best_terminal_L\":";
        if(have_best)std::cout<<best.final_L;else std::cout<<"null";
        std::cout<<",\"rejection_reasons\":{";bool first_reason=true;
        for(const auto& reason:rejection_reasons){if(!first_reason)std::cout<<',';first_reason=false;std::cout<<'"'<<reason.first<<"\":"<<reason.second;}
        std::cout<<"},\"distinct_actual_semigroups\":"<<distinct_sources.size()
            <<",\"counts_include_elites_and_repeats\":true,\"state_cap\":32,\"representatives_per_structure_cap\":4"
            <<",\"universal_sign_claim\":false}\n"<<std::flush;
        int promotion=first_promotion.load();
        // A negative-W result from any already-running worker has priority over
        // the first corner stall. Pending candidates still stop at the flag.
        for(int i=0;i<128;++i)if(results[i].evaluated && results[i].basic.finite && results[i].basic.W<0){promotion=i;break;}
        if(promotion>=0) {
            const auto& r=results[promotion];require(r.w==dijkstra_heap(r.m,r.G),"promoted trade source heap mismatch");emit(r);
            std::cout<<"{\"kind\":\"trade_policy_stop\",\"reason\":\""<<r.status<<"\",\"total_evaluated\":"<<total_evaluated
                <<",\"total_proposed\":"<<total_proposed<<",\"total_accepted\":"<<total_accepted
                <<",\"distinct_actual_semigroups\":"<<distinct_sources.size()
                <<",\"bounded_budget\":512,\"independent_membership_replay_required\":true}\n"<<std::flush;
            return r.basic.W<0?4:6;
        }
    }
    if(have_best){require(best.w==dijkstra_heap(best.m,best.G),"best trade source heap mismatch");emit(best);}
    std::cout<<"{\"kind\":\"trade_policy_complete\",\"seed\":4590,\"generations\":4,\"total_proposed\":"<<total_proposed
        <<",\"total_evaluated\":"<<total_evaluated<<",\"total_accepted\":"<<total_accepted
        <<",\"distinct_supplied_states\":"<<distinct.size()<<",\"total_parent_dependent_proposals\":"<<total_feedback
        <<",\"distinct_actual_semigroups\":"<<distinct_sources.size()<<",\"counts_include_elites_and_repeats\":true"
        <<",\"total_elites\":"<<total_elites<<",\"unresolved_caps\":"<<total_caps
        <<",\"wall_ms\":"<<elapsed(started)<<",\"universal_sign_claim\":false}\n"<<std::flush;
    return 0;
}
