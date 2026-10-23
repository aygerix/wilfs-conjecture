#pragma once
// Included after driver helpers. Repeated FULL paths on identical inputs, with
// a persistent CUDA workspace. Candidate elapsed sums are not parallel wall times.
#include <map>

struct WarmResult {
    double total = 0, reconstruction = 0, analysis = 0;
    double certification_sum = 0, canonical_sum = 0, scoring_sum = 0;
    double upload = 0, kernel = 0, download = 0, gpu_host = 0;
};
inline void warm_metric(const char* name, std::vector<double> values) {
    std::sort(values.begin(), values.end());
    std::cout << '"' << name << "\":{\"min\":" << values.front()
              << ",\"median\":" << values[values.size()/2]
              << ",\"max\":" << values.back() << '}';
}
int warmed_run(int batch, int repeats, std::uint64_t seed, int threads, int m, int k) {
    require(batch>=1 && batch<=65536 && repeats>=1 && repeats<=15 && threads>=1 && threads<=128 &&
            m>=2 && m<=1024 && k>=1 && k<=64, "invalid warm shape");
    Random rng{seed};
    std::vector<i64> flat(static_cast<size_t>(batch)*k);
    // E450 parameter ranges/seeds and two per-candidate draws, now explicitly
    // sequenced across compilers. The old expression did not specify draw order.
    for(int i=0;i<batch;++i) {
        (void)(rng.next()%k); (void)(rng.next()%k);
        for(int j=0;j<k;++j) {
            const i64 height=1+rng.next()%12;
            const int delta=rng.next()%m;
            i64 p=i64(m)*height+delta;
            if(p==m)p+=m;
            flat[static_cast<size_t>(i)*k+j]=p;
        }
    }
    std::vector<i64> reference(static_cast<size_t>(batch)*m), cpu(reference.size()), gpu;
    std::vector<Basic> reference_stats(batch), gpu_stats;
    safe_parallel(batch,threads,[&](int i) {
        const std::vector<i64> G(flat.begin()+static_cast<size_t>(i)*k,flat.begin()+static_cast<size_t>(i+1)*k);
        const auto w=scan_cpu(m,G);
        std::copy(w.begin(),w.end(),reference.begin()+static_cast<size_t>(i)*m);
        reference_stats[i]=invariants(m,G,w);
        if(i<16)require(w==dijkstra_heap(m,G),"warm reference heap differs");
    });
#ifdef WILF_CUDA
    GpuWorkspace workspace(m,k,batch);
    const auto setup=workspace.setup_timing();
#else
    throw std::runtime_error("--warm requires CUDA build for paired measurement");
#endif
    auto analysis=[&](const std::vector<i64>& weights,WarmResult& result) {
        const auto started=Clock::now();
        std::vector<SupportTiming> timers(batch);
        safe_parallel(batch,threads,[&](int i) {
            const std::vector<i64> G(flat.begin()+static_cast<size_t>(i)*k,flat.begin()+static_cast<size_t>(i+1)*k);
            const std::vector<i64> w(weights.begin()+static_cast<size_t>(i)*m,weights.begin()+static_cast<size_t>(i+1)*m);
            if(reference_stats[i].finite) {
                const auto s=support(m,G,w,&timers[i]);
                basic_equal(s.basic,reference_stats[i]);
            } else {
                const auto cert_started=Clock::now();
                basic_equal(invariants(m,G,w),reference_stats[i]);
                timers[i].certification_ms=elapsed(cert_started);
            }
        });
        result.analysis=elapsed(started);
        for(const auto& t:timers) {
            result.certification_sum+=t.certification_ms;
            result.canonical_sum+=t.canonical_ms;
            result.scoring_sum+=t.scoring_ms;
        }
    };
    auto cpu_path=[&] {
        WarmResult r;const auto start=Clock::now(), reconstruction_start=start;
        safe_parallel(batch,threads,[&](int i) {
            const std::vector<i64> G(flat.begin()+static_cast<size_t>(i)*k,flat.begin()+static_cast<size_t>(i+1)*k);
            const auto w=scan_cpu(m,G);
            std::copy(w.begin(),w.end(),cpu.begin()+static_cast<size_t>(i)*m);
        });
        r.reconstruction=elapsed(reconstruction_start);
        analysis(cpu,r);r.total=elapsed(start);
        require(cpu==reference,"warm full CPU array differs");
        return r;
    };
    auto gpu_path=[&] {
        WarmResult r;
#ifdef WILF_CUDA
        const auto start=Clock::now();GpuTiming t;
        workspace.run(batch,flat,gpu,gpu_stats,t);
        r.reconstruction=t.wall_ms;r.upload=t.upload_ms;r.kernel=t.kernel_ms;
        r.download=t.download_ms;r.gpu_host=t.host_ms;
        analysis(gpu,r);r.total=elapsed(start);
        require(gpu==reference,"warm full GPU array differs");
        for(int i=0;i<batch;++i)basic_equal(gpu_stats[i],reference_stats[i]);
#endif
        return r;
    };
    std::vector<WarmResult> cpu_runs,gpu_runs;
    for(int run=-2;run<repeats;++run) {
        WarmResult c,g;
        if(run%2==0){c=cpu_path();g=gpu_path();}else{g=gpu_path();c=cpu_path();}
        if(run>=0){cpu_runs.push_back(c);gpu_runs.push_back(g);}
    }
    std::cout<<"{\"kind\":\"warmed_benchmark\",\"m\":"<<m<<",\"supplied_k\":"<<k
             <<",\"batch\":"<<batch<<",\"seed\":"<<seed<<",\"threads\":"<<threads
             <<",\"warmups\":2,\"repetitions\":"<<repeats<<",\"all_arrays_and_stats_verified\":true"
             <<",\"candidate_sums_are_not_parallel_wall_times\":true";
    std::uint64_t input_hash=UINT64_C(14695981039346656037);
    for(i64 value:flat)for(int byte=0;byte<8;++byte){input_hash^=(static_cast<std::uint64_t>(value)>>(8*byte))&255;input_hash*=UINT64_C(1099511628211);}
    std::cout<<",\"input_hash\":\""<<input_hash<<"\",\"generation_draw_order\":\"height_then_residue\"";
#ifdef WILF_CUDA
    std::cout<<",\"gpu_context_observation_ms\":"<<gpu_context_initialization_ms
             <<",\"workspace_allocation_ms\":"<<setup.allocation_ms<<",\"workspace_setup_ms\":"<<setup.setup_ms;
#endif
    auto metric=[&](const char* name,const std::vector<WarmResult>& runs,double WarmResult::*field) {
        std::vector<double> values;for(const auto& r:runs)values.push_back(r.*field);
        std::cout<<',';warm_metric(name,values);
    };
    metric("cpu_full_batch_wall_ms",cpu_runs,&WarmResult::total);
    metric("gpu_full_batch_wall_ms",gpu_runs,&WarmResult::total);
    metric("cpu_reconstruction_wall_ms",cpu_runs,&WarmResult::reconstruction);
    metric("gpu_reconstruction_wall_ms",gpu_runs,&WarmResult::reconstruction);
    metric("cpu_analysis_wall_ms",cpu_runs,&WarmResult::analysis);
    metric("gpu_analysis_wall_ms",gpu_runs,&WarmResult::analysis);
    metric("gpu_upload_ms",gpu_runs,&WarmResult::upload);
    metric("gpu_kernel_ms",gpu_runs,&WarmResult::kernel);
    metric("gpu_download_ms",gpu_runs,&WarmResult::download);
    metric("gpu_host_residual_ms",gpu_runs,&WarmResult::gpu_host);
    metric("certification_sum_candidate_elapsed_ms",gpu_runs,&WarmResult::certification_sum);
    metric("canonical_sum_candidate_elapsed_ms",gpu_runs,&WarmResult::canonical_sum);
    metric("scoring_sum_candidate_elapsed_ms",gpu_runs,&WarmResult::scoring_sum);
    std::cout<<",\"samples\":[";
    for(int i=0;i<repeats;++i)std::cout<<(i?",":"")<<"{\"cpu_full_ms\":"<<cpu_runs[i].total
        <<",\"gpu_full_ms\":"<<gpu_runs[i].total<<",\"gpu_kernel_ms\":"<<gpu_runs[i].kernel<<'}';
    std::cout<<"]}\n"<<std::flush;
    return 0;
}
