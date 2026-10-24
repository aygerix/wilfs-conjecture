// E472: ONE fixed complete-2-basis construction and its flat-profile comparison.
// No search, parameter sweep, dense m*d word table, or universal Wilf claim.
// Build: c++ -O3 -std=c++17 -Wall -Wextra -Werror cover_cubic.cpp -o cover_cubic
// Run only under the separately approved fixed-input execution scope.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
using i64 = long long;
using Wide = __int128;
constexpr int m = 95250;
constexpr int d = 507;
constexpr int distinguished_raw = 127;

void require(bool ok, const std::string& message) {
    if (!ok) throw std::runtime_error(message);
}
i64 narrow(Wide x) {
    require(x >= std::numeric_limits<i64>::min() && x <= std::numeric_limits<i64>::max(),
            "signed64 result overflow");
    return static_cast<i64>(x);
}
struct Word {
    std::array<int,3> index{{-1,-1,-1}};
    int length = -1;
};
Word word(std::initializer_list<int> indices) {
    require(indices.size() <= 3, "sparse word degree exceeds3");
    Word result; result.length=static_cast<int>(indices.size());
    std::copy(indices.begin(),indices.end(),result.index.begin());
    // A tiny bounded insertion sort avoids GCC13's spurious array-bounds
    // diagnostic from std::sort's 16-element internal insertion threshold.
    for(int i=1;i<result.length;++i)
        for(int j=i;j>0 && result.index[j]<result.index[j-1];--j)
            std::swap(result.index[j],result.index[j-1]);
    return result;
}
bool equal(const Word& a,const Word& b) {
    if(a.length!=b.length)return false;
    for(int i=0;i<a.length;++i)if(a.index[i]!=b.index[i])return false;
    return true;
}
// Lexicographic order of EXPONENT VECTORS, not of sparse index lists.
bool lex_less(const Word& a,const Word& b) {
    int i=0,j=0;
    while(i<a.length || j<b.length) {
        const int ai=i<a.length?a.index[i]:std::numeric_limits<int>::max();
        const int bj=j<b.length?b.index[j]:std::numeric_limits<int>::max();
        const int coordinate=std::min(ai,bj);
        int ca=0,cb=0;
        while(i<a.length && a.index[i]==coordinate){++ca;++i;}
        while(j<b.length && b.index[j]==coordinate){++cb;++j;}
        if(ca!=cb)return ca<cb;
    }
    return false;
}
int count(const Word& a,int coordinate) {
    int result=0;
    for(int i=0;i<a.length;++i)result+=a.index[i]==coordinate;
    return result;
}
Word subtract(const Word& a,int coordinate) {
    Word result;result.length=0;bool removed=false;
    for(int i=0;i<a.length;++i) {
        if(!removed && a.index[i]==coordinate){removed=true;continue;}
        result.index[result.length++]=a.index[i];
    }
    require(removed,"subtracting absent sparse coordinate");
    return result;
}
bool extends(const Word& parent,const Word& child,int coordinate) {
    if(parent.length<0 || child.length!=parent.length+1)return false;
    bool removed=false;int k=0;
    for(int i=0;i<child.length;++i) {
        if(!removed && child.index[i]==coordinate){removed=true;continue;}
        if(k>=parent.length || child.index[i]!=parent.index[k++])return false;
    }
    return removed && k==parent.length;
}
i64 cost(const Word& a,const std::vector<i64>& P) {
    Wide result=0;
    for(int i=0;i<a.length;++i)result+=P[a.index[i]];
    return narrow(result);
}
int residue(const Word& a,const std::vector<int>& delta) {
    int result=0;
    for(int i=0;i<a.length;++i)result=(result+delta[a.index[i]])%m;
    return result;
}
int support_size(const Word& a) {
    int result=0;
    for(int i=0;i<a.length;++i)result+=i==0 || a.index[i]!=a.index[i-1];
    return result;
}
i64 carry(const Word& a,const std::vector<int>& delta) {
    i64 total=0;
    for(int i=0;i<a.length;) {
        const int j=a.index[i];int multiplicity=0;
        while(i<a.length && a.index[i]==j){++multiplicity;++i;}
        const int axis=static_cast<int>(i64(multiplicity)*delta[j]%m);
        require(axis!=0,"selected word contains a nonempty zero-residue axis block");
        total+=axis;
    }
    return total/m;
}

std::vector<int> fixed_basis() {
    std::vector<int> A;std::vector<bool> seen(m,false);
    auto append=[&](int x) {
        require(x>=0 && x<m && !seen[x],"fixed basis components overlap or leave modulus");
        seen[x]=true;A.push_back(x);
    };
    for(int h=0;h<=128;++h)append(6*h);
    for(int h=0;h<=126;++h)append(500+750*h);
    for(int h=0;h<=124;++h)append(127+762*h);
    for(int h=0;h<=126;++h)append(static_cast<int>((31750LL+48012LL*h)%m));
    require(A.size()==508 && seen[0] && seen[127] && !seen[254] && !seen[381],
            "fixed basis cardinality/distinguished exclusions failed");
    std::vector<bool> covered(m,false);
    for(int x:A)for(int y:A)covered[(x+y)%m]=true;
    require(std::all_of(covered.begin(),covered.end(),[](bool x){return x;}),
            "fixed input is not a complete cyclic2basis");
    A.erase(std::find(A.begin(),A.end(),0));
    std::sort(A.begin(),A.end(),std::greater<int>());
    require(A.size()==d,"fixed nonzero basis size failed");
    return A;
}
std::vector<Word> canonical_pairs(const std::vector<int>& delta,
                                  const std::vector<i64>& ranking_cost) {
    std::vector<Word> result(m);
    std::vector<i64> best(m,std::numeric_limits<i64>::max());
    auto consider=[&](const Word& w) {
        const int r=residue(w,delta);const i64 value=cost(w,ranking_cost);
        if(value<best[r] || (value==best[r] && lex_less(w,result[r]))) {
            result[r]=w;best[r]=value;
        }
    };
    consider(word({}));
    for(int j=0;j<d;++j)consider(word({j}));
    for(int j=0;j<d;++j)for(int k=j;k<d;++k)consider(word({j,k}));
    for(const auto& w:result)require(w.length>=0,"unit/pair coverage missing a residue");
    return result;
}
void check_pair_order(const std::vector<Word>& selected,const std::vector<int>& delta,
                      const std::vector<i64>& P) {
    auto check=[&](const Word& candidate) {
        const auto& chosen=selected[residue(candidate,delta)];
        const i64 a=cost(candidate,P),b=cost(chosen,P);
        require(b<a || (b==a && !lex_less(candidate,chosen)),
                "raw canonical pair rule was not preserved by actual reflected costs");
    };
    check(word({}));
    for(int j=0;j<d;++j)check(word({j}));
    for(int j=0;j<d;++j)for(int k=j;k<d;++k)check(word({j,k}));
}
std::vector<i64> deletion_cofactors(const std::vector<i64>& P) {
    std::vector<i64> generators{m};generators.insert(generators.end(),P.begin(),P.end());
    std::vector<i64> prefix(generators.size()+1,0),suffix(prefix.size(),0),result(generators.size());
    for(std::size_t i=0;i<generators.size();++i)prefix[i+1]=std::gcd(prefix[i],generators[i]);
    for(std::size_t i=generators.size();i>0;--i)suffix[i-1]=std::gcd(suffix[i],generators[i-1]);
    for(std::size_t i=0;i<generators.size();++i)result[i]=std::gcd(prefix[i],suffix[i+1]);
    return result;
}
struct Profile {
    std::vector<Word> words;
    std::vector<i64> P,w,cofactors;
    std::vector<int> gamma;
    std::vector<bool> nonmax;
    i64 M=0,c=0,g=0,ell=0,W=0,Dep=0,kappa=0,raw_kappa=0,N=0,Q=0,R=0,F=0;
    i64 mixed_count=0,T=0,columns=0,nontrivial_columns=0,canonical_edges=0,edge_checks=0;
    int r=-1,height=0;
    std::array<i64,4> degree_counts{{0,0,0,0}};
};
Profile analyze(std::vector<Word> words,const std::vector<i64>& P,
                const std::vector<int>& delta,const std::vector<int>& raw_delta,
                bool check_all_generator_edges) {
    Profile result;result.words=std::move(words);result.P=P;
    result.w.resize(m);result.gamma.assign(m,d);result.nonmax.assign(m,false);
    require(result.words[0].length==0,"origin is not empty");
    Wide genus=0;
    for(int s=0;s<m;++s) {
        const auto& w=result.words[s];
        require(w.length>=0 && w.length<=3 && residue(w,delta)==s,"invalid sparse residue word");
        for(int i=0;i<w.length;++i)
            require(w.index[i]>=0 && w.index[i]<d && (i==0 || w.index[i-1]<=w.index[i]),
                    "sparse coordinates invalid or not sorted");
        result.w[s]=cost(w,P);
        require(result.w[s]>=0 && result.w[s]%m==s,"actual weight has wrong residue");
        if(result.w[s]>result.M){result.M=result.w[s];result.r=s;}
        genus+=result.w[s]/m;
        result.height=std::max(result.height,w.length);++result.degree_counts[w.length];
        const int support=support_size(w);
        result.T+=std::max(0,support-1);result.mixed_count+=support>=2;
        const i64 raw=carry(w,raw_delta),mirrored=carry(w,delta);
        if(w.length)require(raw+mirrored==support-1,"wordwise mirror carry identity failed");
        result.raw_kappa+=raw;result.kappa+=mirrored;
        for(int i=0;i<w.length;) {
            const int j=w.index[i];
            while(i<w.length && w.index[i]==j)++i;
            const int parent=(s-delta[j]+m)%m;
            require(equal(result.words[parent],subtract(w,j)),"sparse tile is not a downset");
            ++result.canonical_edges;
        }
    }
    require(result.r>0,"proper source has no positive maximum");
    for(int j=0;j<d;++j)require(equal(result.words[delta[j]],word({j})),"source unit missing");
    result.g=narrow(genus);result.c=result.M-m+1;result.ell=result.c-result.g;
    result.W=narrow(Wide(d+1)*result.ell-result.c);
    const int rho=m-1-result.r;
    std::vector<int> label(m);
    for(int s=0;s<m;++s)label[s]=(s+rho)%m;

    // Initially regard every cell in every direction as a singleton column.
    // A genuine nonsingleton column is found exactly once: its first child has
    // exponent1 in that direction. Replacing its singleton contributions costs
    // O(column length), at most4, and never constructs a dense coordinate row.
    i64 walked_edges=0;
    for(int first=1;first<m;++first) {
        const auto& w=result.words[first];
        for(int i=0;i<w.length;) {
            const int j=w.index[i];int multiplicity=0;
            while(i<w.length && w.index[i]==j){++multiplicity;++i;}
            if(multiplicity!=1)continue;
            const int base=(first-delta[j]+m)%m;
            require(count(result.words[base],j)==0,"nontrivial column start not at exponent0");
            std::array<int,4> members{{-1,-1,-1,-1}};
            int length=0,current=base;
            while(true) {
                require(length<4,"column exceeds sparse degree bound");
                members[length++]=current;
                const int child=(current+delta[j])%m;
                if(!extends(result.words[current],result.words[child],j))break;
                current=child;
            }
            require(length>=2 && members[1]==first,"incorrect nontrivial column enumeration");
            ++result.nontrivial_columns;walked_edges+=length-1;
            const int top=members[length-1];
            for(int k=0;k<length-1;++k) {
                --result.gamma[members[k]];result.nonmax[members[k]]=true;
                result.N+=label[members[k]]>label[top];
            }
            result.gamma[top]+=length-1;
        }
    }
    require(walked_edges==result.canonical_edges,"sparse columns missed or duplicated an edge");
    result.columns=i64(d)*m-walked_edges;
    Wide gamma_mass=0,weighted_height=0,weighted_residue=0;
    for(int s=0;s<m;++s) {
        require(result.gamma[s]>=0,"negative sparse column mass");
        gamma_mass+=result.gamma[s];
        if(result.nonmax[s])result.Dep+=result.gamma[s];
        weighted_height+=Wide(result.gamma[s])*((result.M-result.w[s])/m);
        weighted_residue+=Wide(result.gamma[s])*((result.r-s+m)%m);
    }
    require(gamma_mass==Wide(d)*m,"total column mass failed");
    const Wide C=Wide(d-1)*m*(m-1)/2;
    require((weighted_residue-C)%m==0,"nonintegral phase budget");
    result.Q=result.Dep+result.N-result.kappa;
    require(result.Q==result.Dep+narrow((weighted_residue-C)/m),"direct columns/phase Q disagree");
    result.R=narrow(weighted_height-result.Dep);result.F=result.kappa-result.Dep;
    require(result.R>=0 && result.W==result.Q+result.R,"full support identity failed");
    require(result.kappa+result.raw_kappa==result.T,"full mirror carry identity failed");
    result.cofactors=deletion_cofactors(P);
    require(std::all_of(result.cofactors.begin(),result.cofactors.end(),[](i64 x){return x==1;}),
            "a deletion cofactor is not1");

    if(check_all_generator_edges) {
        for(int s=0;s<m;++s)for(int j=0;j<d;++j) {
            const int target=(s+delta[j])%m;
            require(Wide(result.w[s])+P[j]>=result.w[target],"source generator-edge certificate failed");
            ++result.edge_checks;
        }
        // Every exported nonzero word has a canonical strictly smaller prefix.
        for(int s=1;s<m;++s) {
            const int j=result.words[s].index[0],parent=(s-delta[j]+m)%m;
            require(result.w[parent]<result.w[s] && result.w[parent]+P[j]==result.w[s],
                    "source attaining predecessor failed");
        }
    }
    return result;
}

template<class T> void array(std::ostream& out,const std::vector<T>& values) {
    out<<'[';for(std::size_t i=0;i<values.size();++i)out<<(i?",":"")<<values[i];out<<']';
}
void words_json(std::ostream& out,const std::vector<Word>& words) {
    out<<'[';
    for(std::size_t s=0;s<words.size();++s) {
        if(s)out<<',';
        out<<'[';for(int i=0;i<words[s].length;++i)out<<(i?",":"")<<words[s].index[i];out<<']';
    }
    out<<']';
}
std::string escaped(const std::string& input) {
    const char* hex="0123456789abcdef";std::string out;
    for(unsigned char c:input) {
        if(c=='"' || c=='\\'){out+='\\';out+=static_cast<char>(c);}
        else if(c<32){out+="\\u00";out+=hex[c>>4];out+=hex[c&15];}
        else out+=static_cast<char>(c);
    }
    return out;
}
void summary_json(std::ostream& out,const Profile& p) {
    out<<"{\"e\":"<<d+1<<",\"M\":"<<p.M<<",\"r\":"<<p.r
       <<",\"c\":"<<p.c<<",\"g\":"<<p.g<<",\"ell\":"<<p.ell<<",\"W\":"<<p.W
       <<",\"Dep\":"<<p.Dep<<",\"kappa\":"<<p.kappa<<",\"raw_kappa\":"<<p.raw_kappa
       <<",\"N\":"<<p.N<<",\"Q\":"<<p.Q<<",\"R\":"<<p.R<<",\"F\":"<<p.F
       <<",\"height\":"<<p.height<<",\"mixed_count\":"<<p.mixed_count<<",\"T\":"<<p.T
       <<",\"columns\":"<<p.columns<<",\"nontrivial_columns\":"<<p.nontrivial_columns
       <<",\"canonical_edges\":"<<p.canonical_edges<<",\"gamma_mass\":"<<i64(d)*m
       <<",\"generator_edges_checked\":"<<p.edge_checks<<",\"cofactor1\":true,\"deletion_cofactors\":";
    array(out,p.cofactors);
    out<<",\"degree_counts\":[";
    for(int i=0;i<4;++i)out<<(i?",":"")<<p.degree_counts[i];
    out<<"]}";
}
void profile_json(std::ostream& out,const Profile& p,bool include_P) {
    out<<'{';
    if(include_P){out<<"\"P\":";array(out,p.P);out<<',';}
    out<<"\"w\":";array(out,p.w);
    out<<",\"words\":";words_json(out,p.words);
    out<<",\"summary\":";summary_json(out,p);
    out<<",\"gamma\":";array(out,p.gamma);out<<'}';
}
} // namespace

int main(int argc,char** argv) {
    try {
        if(argc==2 && std::string(argv[1])=="--help") {
            std::cout<<"usage: cover_cubic --output PATH\nFixed E472 input only; no search options.\n";return 0;
        }
        require(argc==3 && std::string(argv[1])=="--output" && std::string(argv[2]).size()>0,
                "usage: cover_cubic --output PATH");
        const auto started=std::chrono::steady_clock::now();
        const std::string output_path=argv[2];
        const auto raw_delta=fixed_basis();
        std::vector<int> delta(d);
        std::vector<i64> P(d),flat_P(d),raw_flat_P(d);
        int distinguished=-1;
        for(int j=0;j<d;++j) {
            if(raw_delta[j]==distinguished_raw)distinguished=j;
            delta[j]=m-raw_delta[j];
            const int h=raw_delta[j]==distinguished_raw?12:20;
            const int flat_h=raw_delta[j]==distinguished_raw?16:20;
            P[j]=narrow(Wide(h)*m*m+m+Wide(m-1)*raw_delta[j]);
            flat_P[j]=narrow(Wide(flat_h)*m*m+m+Wide(m-1)*raw_delta[j]);
            raw_flat_P[j]=i64(flat_h)*m+raw_delta[j];
            require(P[j]>m && P[j]%m==delta[j],"actual generator lift failed");
        }
        require(distinguished>=0 && std::is_sorted(delta.begin(),delta.end()),"coordinate order failed");
        auto flat_words=canonical_pairs(delta,raw_flat_P);
        check_pair_order(flat_words,delta,flat_P);
        check_pair_order(flat_words,delta,P);
        const int cubic_residue=(3*delta[distinguished])%m;
        require(cubic_residue==m-381,"cubic residue alignment failed");
        const Word removed=flat_words[cubic_residue];
        require(removed.length==2,"removed representative is not quadratic");
        std::vector<int> removed_raw={raw_delta[removed.index[0]],raw_delta[removed.index[1]]};
        std::sort(removed_raw.begin(),removed_raw.end(),std::greater<int>());
        require(removed_raw==std::vector<int>({63500,32131}),"unexpected canonical removed pair");
        require(count(removed,distinguished)==0,"removed pair contains distinguished atom");
        const auto cubic=word({distinguished,distinguished,distinguished});
        auto source_words=flat_words;source_words[cubic_residue]=cubic;
        int changed=0;
        for(int s=0;s<m;++s)changed+=!equal(source_words[s],flat_words[s]);
        require(changed==1,"construction changed more than one word");
        const int square_residue=(2*delta[distinguished])%m;
        require(equal(source_words[square_residue],word({distinguished,distinguished})),
                "distinguished square was not retained");

        const i64 maximum=*std::max_element(P.begin(),P.end());
        i64 other_min=std::numeric_limits<i64>::max();
        for(int j=0;j<d;++j)if(j!=distinguished)other_min=std::min(other_min,P[j]);
        require(P[distinguished]<other_min && 2*Wide(P[distinguished])>maximum,
                "actual primitive/unit cost separation failed");
        require(3*Wide(flat_P[distinguished])>2*Wide(*std::max_element(flat_P.begin(),flat_P.end())),
                "flat triples are not excluded");
        require(2*Wide(P[distinguished])+other_min>2*Wide(maximum) &&
                4*Wide(P[distinguished])>2*Wide(maximum),"nonpure triples/higher words not excluded");
        require(cost(cubic,P)<cost(removed,P) && 3*Wide(P[distinguished])<2*Wide(other_min) &&
                3*Wide(P[distinguished])>Wide(P[distinguished])+maximum,
                "cubic ordering failed");

        const auto flat=analyze(std::move(flat_words),flat_P,delta,raw_delta,false);
        const auto source=analyze(std::move(source_words),P,delta,raw_delta,true);
        require(flat.height==2 && source.height==3 && source.degree_counts[3]==1,
                "flat/nonflat height assertion failed");
        require(3*(d+1)<m && source.c>4LL*m,"source leaves sparse/deep remaining domain");
        int newly_maximal=0;std::vector<int> newly_maximal_coordinates;
        for(int j=0;j<d;++j)if(flat.nonmax[delta[j]] && !source.nonmax[delta[j]]) {
            ++newly_maximal;newly_maximal_coordinates.push_back(j);
            require(count(removed,j)>0,"unrelated source unit became maximal");
        }
        const i64 removed_kappa=carry(removed,delta);
        require(newly_maximal<=2 && source.Dep-flat.Dep==i64(d+1)*(1-newly_maximal) &&
                source.kappa-flat.kappa==-removed_kappa,"one-cell Dep/carry jump failed");
        require(source.F==flat.F-i64(d+1)*(1-newly_maximal)-removed_kappa,
                "one-cell F identity failed");
        require(removed_kappa==0 && carry(removed,raw_delta)==1,"removed pair mirror carry failed");
        require(flat.raw_kappa<=25130 && flat.T>=94235 && flat.Dep<=68072 && flat.F>=1033,
                "flat paper bounds failed: raw_kappa="+std::to_string(flat.raw_kappa)+
                " T="+std::to_string(flat.T)+" Dep="+std::to_string(flat.Dep)+" F="+std::to_string(flat.F));
        require(source.F>=525,"nonflat paper bound F>=525 failed");

        std::ofstream output(output_path,std::ios::binary|std::ios::trunc);
        require(output.good(),"cannot open output path");
        output<<"{\"kind\":\"cover_cubic_fixed_E472\",\"m\":"<<m<<",\"d\":"<<d
              <<",\"raw_delta\":";array(output,raw_delta);
        output<<",\"P\":";array(output,P);
        output<<",\"distinguished_raw\":127,\"distinguished_coordinate\":"<<distinguished
              <<",\"coordinate_order\":\"decreasing_raw_delta_increasing_actual_residue\""
              <<",\"word_format\":\"sorted_zero_based_coordinate_indices_with_repetition_by_actual_residue\""
              <<",\"basis_cardinality\":508,\"pair_cover_verified\":true,\"source_count\":1"
              <<",\"flat_is_comparison_profile\":true,\"source\":";
        profile_json(output,source,false);
        output<<",\"flat_profile\":";profile_json(output,flat,true);
        output<<",\"replacement\":{\"actual_residue\":"<<cubic_residue
              <<",\"raw_residue\":381,\"removed_raw\":[63500,32131],\"removed_word\":";
        words_json(output,std::vector<Word>{removed});
        output<<",\"inserted_word\":";words_json(output,std::vector<Word>{cubic});
        output<<",\"changed_word_count\":1,\"removed_mirrored_kappa\":"<<removed_kappa
              <<",\"newly_maximal_parent_units\":"<<newly_maximal<<",\"newly_maximal_coordinates\":";
        array(output,newly_maximal_coordinates);
        output<<"},\"paper_bounds\":{\"flat_raw_kappa_upper\":25130,\"flat_T_lower\":94235"
              <<",\"flat_Dep_upper\":68072,\"flat_F_lower\":1033,\"source_F_lower\":525,\"verified\":true}"
              <<",\"universal_sign_claim\":false}\n";
        output.close();require(output.good(),"failed writing complete witness");
        const double wall_ms=std::chrono::duration<double,std::milli>(
            std::chrono::steady_clock::now()-started).count();
        std::cout<<"{\"kind\":\"cover_cubic_complete\",\"m\":"<<m<<",\"e\":"<<d+1
                 <<",\"F\":"<<source.F<<",\"Q\":"<<source.Q<<",\"W\":"<<source.W
                 <<",\"generator_edges_checked\":"<<source.edge_checks
                 <<",\"output\":\""<<escaped(output_path)<<"\",\"wall_ms\":"<<wall_ms<<"}\n";
        return source.W<0?4:source.Q<0?3:0;
    } catch(const std::exception& error) {
        std::cerr<<"cover_cubic: "<<error.what()<<'\n';return 2;
    }
}
