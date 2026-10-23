#pragma once
// Finite two-step audit: exact same-tile neutral representatives, then all
// single-input exits in the stated box. This is not the full neutral component.
struct NeutralState {std::vector<i64> G,w;Support score;};
inline bool neutral_same_tile(const Support& a,const Support& b) {
    return a.basic.e==b.basic.e && a.residues==b.residues && a.words==b.words && a.gamma==b.gamma;
}
inline int neutral_height(const Support& s,int m) {
    const int d=s.basic.e-1;int height=0;
    for(int r=0;r<m;++r){int degree=0;for(int j=0;j<d;++j)degree+=s.words[static_cast<size_t>(r)*d+j];height=std::max(height,degree);}
    return height;
}
int neutral_audit(int threads,int m,const std::vector<i64>& anchor) {
    require(m>=3 && m<=1024 && threads>=1 && threads<=128 && !anchor.empty() && anchor.size()<=64,
            "invalid neutral audit shape");
    for(i64 p:anchor)require(p>m && p<13LL*m,"neutral anchor out of height range");
    NeutralState origin;origin.G=anchor;origin.w=scan_cpu(m,anchor);origin.score=support(m,anchor,origin.w);
    require(origin.w==dijkstra_heap(m,anchor),"neutral origin heap mismatch");
    const i64 baseF=origin.score.kappa-origin.score.Dep;
    require(origin.score.basic.e>=4 && 3*origin.score.basic.e<m && origin.score.basic.c>4LL*m &&
            neutral_height(origin.score,m)>=3,"neutral origin outside intended domain");
    std::vector<std::pair<int,i64>> moves;
    for(int j=0;j<static_cast<int>(anchor.size());++j)for(i64 value=m+1;value<13LL*m;++value)
        if(value!=anchor[j])moves.emplace_back(j,value);
    require(moves.size()<=10000,"neutral outgoing move budget exceeded");
    std::vector<NeutralState> tied(moves.size());
    std::vector<int> retained(moves.size()),neutralF(moves.size());
    std::vector<int> first_evaluated(moves.size()),first_codes(moves.size());std::atomic<bool> first_negative{false};
    const auto started=Clock::now();
    safe_parallel(static_cast<int>(moves.size()),threads,[&](int i) {
        if(first_negative.load())return;
        first_evaluated[i]=1;
        auto G=anchor;G[moves[i].first]=moves[i].second;
        const auto w=scan_cpu(m,G);if(std::find(w.begin(),w.end(),INF)!=w.end())return;
        const auto score=support(m,G,w);
        const bool domain=score.basic.e>=4 && 3*score.basic.e<m && score.basic.c>4LL*m;
        if(score.basic.W<0 || (domain && score.Q<0)) {
            tied[i]={G,w,score};first_codes[i]=score.basic.W<0?4:3;first_negative=true;return;
        }
        if(score.basic.e<4 || 3*score.basic.e>=m || score.basic.c<=4LL*m || neutral_height(score,m)<3)return;
        if(score.kappa-score.Dep!=baseF)return;
        neutralF[i]=1;
        if(!neutral_same_tile(origin.score,score))return;
        tied[i]={std::move(G),w,score};retained[i]=1;
    });
    for(size_t i=0;i<moves.size();++i)if(first_codes[i]) {
        const auto& candidate=tied[i];require(candidate.w==dijkstra_heap(m,candidate.G),"neutral first-step negative heap mismatch");
        emit_case(first_codes[i]==4?"negative_W_candidate":"negative_Q_candidate",m,candidate.G,candidate.w,candidate.score);
        return first_codes[i];
    }
    std::vector<NeutralState> representatives;
    std::set<std::vector<i64>> distinct_heights;
    for(size_t i=0;i<moves.size();++i)if(retained[i]) {
        std::vector<i64> values;for(int residue:tied[i].score.residues)values.push_back(tied[i].w[residue]);
        if(distinct_heights.insert(values).second)representatives.push_back(std::move(tied[i]));
    }
    require(representatives.size()<=19,"neutral representative budget exceeded; do not enlarge silently");
    std::cout<<"{\"kind\":\"neutral_seed_audit\",\"m\":"<<m<<",\"base_F\":"<<baseF
             <<",\"first_step_replacements\":"<<moves.size()<<",\"F_neutral_neighbors\":"
             <<std::accumulate(neutralF.begin(),neutralF.end(),0)<<",\"same_exact_tile_representatives\":"<<representatives.size()
             <<",\"full_arrays_compared\":true,\"first_step_wall_ms\":"<<elapsed(started)<<"}\n"<<std::flush;
    emit_case("neutral_origin",m,origin.G,origin.w,origin.score);
    std::uint64_t total_evaluated=std::accumulate(first_evaluated.begin(),first_evaluated.end(),0);
    bool escaped=false,negative_candidate=false;int return_code=0;
    for(size_t seed=0;seed<representatives.size();++seed) {
        const auto& rep=representatives[seed];
        require(rep.w==dijkstra_heap(m,rep.G),"neutral representative heap mismatch");
        const std::string name="neutral_seed_"+std::to_string(seed);
        emit_case(name.c_str(),m,rep.G,rep.w,rep.score);
        std::vector<std::pair<int,i64>> exits;
        for(int j=0;j<static_cast<int>(rep.G.size());++j)for(i64 value=m+1;value<13LL*m;++value)
            if(value!=rep.G[j])exits.emplace_back(j,value);
        std::vector<i64> F(exits.size(),std::numeric_limits<i64>::min());
        std::vector<int> eligible(exits.size()),evaluated(exits.size()),changed_residue(exits.size()),codes(exits.size());
        std::atomic<bool> found{false};const auto exit_started=Clock::now();
        safe_parallel(static_cast<int>(exits.size()),threads,[&](int i) {
            if(found.load())return;
            evaluated[i]=1;
            auto G=rep.G;G[exits[i].first]=exits[i].second;
            const auto w=scan_cpu(m,G);if(std::find(w.begin(),w.end(),INF)!=w.end())return;
            const auto s=support(m,G,w);const auto& b=s.basic;
            if(b.W<0){codes[i]=4;found=true;}
            if(b.e<4 || 3*b.e>=m || b.c<=4LL*m)return;
            if(s.Q<0 && codes[i]!=4){codes[i]=3;found=true;}
            if(neutral_height(s,m)<3)return;
            eligible[i]=1;F[i]=s.kappa-s.Dep;
            changed_residue[i]=exits[i].second%m!=rep.G[exits[i].first]%m;
            if(F[i]>baseF){if(!codes[i] && F[i]>0)codes[i]=5;found=true;}
        });
        const int done=std::accumulate(evaluated.begin(),evaluated.end(),0);total_evaluated+=done;
        int best=-1,promotion=-1,pcode=0; i64 bestF=std::numeric_limits<i64>::min(),residueF=bestF;
        auto priority=[](int c){return c==4?3:c==3?2:c==5?1:0;};
        for(size_t i=0;i<exits.size();++i) {
            if(priority(codes[i])>priority(pcode)){promotion=static_cast<int>(i);pcode=codes[i];}
            if(!eligible[i])continue;
            if(F[i]>bestF){bestF=F[i];best=static_cast<int>(i);}
            if(changed_residue[i])residueF=std::max(residueF,F[i]);
        }
        if(promotion>=0)best=promotion;
        std::cout<<"{\"kind\":\"neutral_outgoing_audit\",\"seed_index\":"<<seed<<",\"planned\":"<<exits.size()
                 <<",\"evaluated\":"<<done<<",\"eligible_nonflat\":"<<std::accumulate(eligible.begin(),eligible.end(),0)
                 <<",\"maximum_F\":";
        if(bestF==std::numeric_limits<i64>::min())std::cout<<"null";else std::cout<<bestF;
        std::cout<<",\"changed_residue_maximum_F\":";
        if(residueF==std::numeric_limits<i64>::min())std::cout<<"null";else std::cout<<residueF;
        std::cout<<",\"representative_W\":"<<rep.score.basic.W<<",\"representative_R\":"<<rep.score.R
                 <<",\"representative_top\":"<<rep.score.basic.top<<",\"wall_ms\":"<<elapsed(exit_started)<<"}\n"<<std::flush;
        if(best>=0) {
            auto G=rep.G;G[exits[best].first]=exits[best].second;
            const auto w=scan_cpu(m,G);require(w==dijkstra_heap(m,G),"neutral exit best heap mismatch");
            const auto s=support(m,G,w);
            const bool improved=s.kappa-s.Dep>baseF;
            const std::string label="neutral_neighbor_best_"+std::to_string(seed);
            emit_case(label.c_str(),m,G,w,s);
            if(improved || pcode) {
                std::cout<<"{\"kind\":\"neutral_escape\",\"seed_index\":"<<seed<<",\"old_F\":"<<baseF
                         <<",\"new_F\":"<<s.kappa-s.Dep<<",\"promotion_code\":"<<pcode
                         <<",\"same_tile_neutral_first_step\":true,\"finite_two_step_path\":true}\n";
                emit_case("neutral_path_origin",m,origin.G,origin.w,origin.score);
                emit_case("neutral_path_middle",m,rep.G,rep.w,rep.score);
                emit_case("neutral_path_exit",m,G,w,s);escaped=improved;negative_candidate=pcode==3 || pcode==4;return_code=pcode;break;
            }
        }
    }
    std::cout<<"{\"kind\":\"neutral_audit_complete\",\"representatives\":"<<representatives.size()
             <<",\"total_evaluated\":"<<total_evaluated<<",\"improving_exit_found\":"<<(escaped?"true":"false")
             <<",\"negative_candidate_found\":"<<(negative_candidate?"true":"false")
             <<",\"wall_ms\":"<<elapsed(started)<<",\"exhausts_full_neutral_component\":false}\n"<<std::flush;
    return return_code;
}
