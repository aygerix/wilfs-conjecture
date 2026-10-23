#include "gpu.hpp"
#include <cuda_runtime.h>
#include <cub/block/block_scan.cuh>
#include <cub/block/block_reduce.cuh>
#include <chrono>
#include <sstream>

namespace wilf {
namespace {
void check(cudaError_t error, const char* operation) {
    if (error != cudaSuccess)
        throw std::runtime_error(std::string(operation) + ": " + cudaGetErrorString(error));
}
struct Node { i64 value; int head; };
struct SegMin {
    __device__ Node operator()(const Node& a, const Node& b) const {
        return {b.head ? b.value : (a.value < b.value ? a.value : b.value), a.head | b.head};
    }
};
struct Aggregate { i64 maximum, genus; int primitives, unreachable, top; };
struct Merge {
    __device__ Aggregate operator()(const Aggregate& a, const Aggregate& b) const {
        const bool right = b.maximum > a.maximum ||
            (b.maximum == a.maximum && b.top > a.top);
        return {right ? b.maximum : a.maximum, a.genus + b.genus,
                a.primitives + b.primitives, a.unreachable + b.unreachable,
                right ? b.top : a.top};
    }
};
__device__ int gcd_device(int a, int b) {
    while (b) { const int next = a % b; a = b; b = next; }
    return a;
}

template<int BLOCK>
__global__ void scan_kernel(int m, int k, const i64* generators, i64* output, Basic* stats) {
    using Scan = cub::BlockScan<Node, BLOCK>;
    using Reduce = cub::BlockReduce<Aggregate, BLOCK>;
    __shared__ union Temporary {
        typename Scan::TempStorage scan;
        typename Reduce::TempStorage reduce;
    } temp;
    __shared__ i64 w[BLOCK], suffix[BLOCK];
    const int lane = threadIdx.x;
    const size_t candidate = blockIdx.x;
    const i64* G = k ? generators + candidate * k : nullptr;
    w[lane] = lane == 0 ? 0 : INF;
    __syncthreads();
    for (int stage = 0; stage < k; ++stage) {
        const i64 p = G[stage];
        const int delta = static_cast<int>(p % m);
        if (delta == 0) continue; // Uniform within the block.
        const int cycles = gcd_device(m, delta), h = m / cycles;
        const int cycle = lane / h, t = lane % h;
        int residue = 0, reverse_t = 0;
        Node forward{INF, 1}, reverse{INF, 1}, prefix, backward;
        if (lane < m) {
            residue = (cycle + t * delta) % m;
            reverse_t = h - 1 - t;
            const int reverse_residue = (cycle + reverse_t * delta) % m;
            forward = {w[residue] == INF ? INF : w[residue] - t * p, t == 0};
            reverse = {w[reverse_residue] == INF ? INF : w[reverse_residue] - reverse_t * p, t == 0};
        }
        Scan(temp.scan).InclusiveScan(forward, prefix, SegMin{});
        __syncthreads(); // CUB scan scratch is reused below.
        Scan(temp.scan).InclusiveScan(reverse, backward, SegMin{});
        if (lane < m) suffix[cycle * h + reverse_t] = backward.value;
        __syncthreads();
        i64 next = INF;
        if (lane < m) {
            i64 best = prefix.value;
            if (t + 1 < h && suffix[cycle * h + t + 1] != INF) {
                const i64 wrapped = h * p + suffix[cycle * h + t + 1];
                best = best < wrapped ? best : wrapped;
            }
            if (best != INF) next = t * p + best;
        }
        __syncthreads(); // Every old-weight read finishes before overwriting w.
        if (lane < m) w[residue] = next;
        __syncthreads();
    }
    Aggregate item{0, 0, 0, 0, -1};
    if (lane < m) {
        const i64 value = w[lane];
        output[candidate * m + lane] = value;
        if (value == INF) item.unreachable = 1;
        else {
            item.maximum = value; item.genus = value / m; item.top = lane;
            if (lane != 0) {
                bool composite = false;
                for (int j = 0; j < k; ++j) {
                    const int parent = (lane - static_cast<int>(G[j] % m) + m) % m;
                    if (parent != 0 && w[parent] != INF && w[parent] + G[j] == value)
                        composite = true;
                }
                item.primitives = !composite;
            }
        }
    }
    __syncthreads();
    const Aggregate total = Reduce(temp.reduce).Reduce(item, Merge{});
    if (lane == 0) { // BlockReduce results are valid only in lane zero.
        Basic* result = stats + candidate;
        result->m = m;
        result->finite = total.unreachable == 0;
        if (total.unreachable) {
            result->e = 0; result->top = -1;
            result->c = result->g = result->W = INF;
        } else {
            result->e = 1 + total.primitives; result->top = total.top;
            result->c = total.maximum - m + 1; result->g = total.genus;
            result->W = static_cast<i64>(result->e) * (result->c - result->g) - result->c;
        }
    }
}
}

std::string gpu_description() {
    cudaDeviceProp device{};
    check(cudaGetDeviceProperties(&device, 0), "read GPU properties");
    std::ostringstream out;
    out << device.name << "; cc=" << device.major << '.' << device.minor
        << "; global_bytes=" << device.totalGlobalMem;
    return out.str();
}

namespace {
using Clock = std::chrono::steady_clock;
double milliseconds(Clock::time_point start) {
    return std::chrono::duration<double, std::milli>(Clock::now() - start).count();
}
void finish_timing(GpuTiming& timing, Clock::time_point start) {
    timing.wall_ms = milliseconds(start);
    timing.host_ms = std::max(0.0, timing.wall_ms - timing.allocation_ms - timing.setup_ms -
        timing.upload_ms - timing.kernel_ms - timing.download_ms);
}
void validate_batch(int m, int k, int batch, int capacity,
                    const std::vector<i64>& generators) {
    if (m < 1 || m > 1024 || k < 0 || capacity <= 0 || capacity > (1 << 20) ||
        batch <= 0 || batch > capacity ||
        generators.size() != static_cast<size_t>(batch) * k)
        throw std::invalid_argument("invalid GPU batch shape or workspace capacity");
    for (i64 p : generators) {
        if (p <= m || static_cast<__int128>(8) * m * m * p >= INF)
            throw std::invalid_argument("GPU requires p>m and 8*m*m*p<INF");
    }
}
}

struct GpuWorkspace::Impl {
    int modulus = 0, generator_count = 0, batch_capacity = 0;
    i64 *input = nullptr, *output = nullptr;
    Basic* stats = nullptr;
    cudaEvent_t before = nullptr, after = nullptr;
    GpuTiming setup;
    ~Impl() noexcept {
        // Cleanup must not replace an allocation/launch exception. cudaFree
        // also waits for outstanding uses if run() failed after a launch.
        if (input) cudaFree(input);
        if (output) cudaFree(output);
        if (stats) cudaFree(stats);
        if (before) cudaEventDestroy(before);
        if (after) cudaEventDestroy(after);
    }
};

GpuWorkspace::GpuWorkspace(int m, int k, int capacity) : impl_(new Impl) {
    const auto start = Clock::now();
    if (m < 1 || m > 1024 || k < 0 || capacity <= 0 || capacity > (1 << 20))
        throw std::invalid_argument("invalid GPU workspace shape (m<=1024)");
    Impl& state = *impl_;
    state.modulus = m; state.generator_count = k; state.batch_capacity = capacity;
    const size_t input_bytes = static_cast<size_t>(capacity) * k * sizeof(i64);
    const size_t output_bytes = static_cast<size_t>(capacity) * m * sizeof(i64);
    const auto allocation_start = Clock::now();
    if (input_bytes) check(cudaMalloc(&state.input, input_bytes), "allocate workspace generators");
    check(cudaMalloc(&state.output, output_bytes), "allocate workspace Apéry arrays");
    check(cudaMalloc(&state.stats, static_cast<size_t>(capacity) * sizeof(Basic)), "allocate workspace statistics");
    state.setup.allocation_ms = milliseconds(allocation_start);
    const auto setup_start = Clock::now();
    check(cudaEventCreate(&state.before), "create workspace start event");
    check(cudaEventCreate(&state.after), "create workspace end event");
    state.setup.setup_ms = milliseconds(setup_start);
    finish_timing(state.setup, start);
}

GpuWorkspace::~GpuWorkspace() noexcept = default;
GpuWorkspace::GpuWorkspace(GpuWorkspace&&) noexcept = default;
GpuWorkspace& GpuWorkspace::operator=(GpuWorkspace&&) noexcept = default;
int GpuWorkspace::m() const noexcept { return impl_ ? impl_->modulus : 0; }
int GpuWorkspace::k() const noexcept { return impl_ ? impl_->generator_count : 0; }
int GpuWorkspace::capacity() const noexcept { return impl_ ? impl_->batch_capacity : 0; }
const GpuTiming& GpuWorkspace::setup_timing() const noexcept {
    static const GpuTiming empty;
    return impl_ ? impl_->setup : empty;
}

void GpuWorkspace::run(int batch, const std::vector<i64>& generators,
                       std::vector<i64>& weights, std::vector<Basic>& stats,
                       GpuTiming& timing) {
    const auto start = Clock::now();
    timing = GpuTiming{};
    if (!impl_) throw std::logic_error("cannot run a moved-from GPU workspace");
    Impl& state = *impl_;
    const int m = state.modulus, k = state.generator_count;
    validate_batch(m, k, batch, state.batch_capacity, generators);
    const size_t input_bytes = generators.size() * sizeof(i64);
    const size_t output_bytes = static_cast<size_t>(batch) * m * sizeof(i64);
    const auto upload_start = Clock::now();
    if (input_bytes)
        check(cudaMemcpy(state.input, generators.data(), input_bytes, cudaMemcpyHostToDevice), "upload generators");
    timing.upload_ms = milliseconds(upload_start);
    // Upload before resizing so the legacy API also tolerates using the input
    // vector as the output vector. No host input is read after this point.
    weights.resize(static_cast<size_t>(batch) * m);
    stats.resize(batch);
    check(cudaEventRecord(state.before), "record kernel start");
    if (m <= 256) scan_kernel<256><<<batch, 256>>>(m, k, state.input, state.output, state.stats);
    else if (m <= 512) scan_kernel<512><<<batch, 512>>>(m, k, state.input, state.output, state.stats);
    else scan_kernel<1024><<<batch, 1024>>>(m, k, state.input, state.output, state.stats);
    check(cudaGetLastError(), "launch cyclic scans");
    check(cudaEventRecord(state.after), "record kernel end");
    check(cudaEventSynchronize(state.after), "wait for cyclic scans");
    check(cudaEventElapsedTime(&timing.kernel_ms, state.before, state.after), "measure kernel");
    const auto download_start = Clock::now();
    check(cudaMemcpy(weights.data(), state.output, output_bytes, cudaMemcpyDeviceToHost), "download Apéry arrays");
    check(cudaMemcpy(stats.data(), state.stats, static_cast<size_t>(batch) * sizeof(Basic), cudaMemcpyDeviceToHost), "download statistics");
    timing.download_ms = milliseconds(download_start);
    finish_timing(timing, start);
}

void gpu_scan_batch(int m, int k, int batch, const std::vector<i64>& generators,
                    std::vector<i64>& weights, std::vector<Basic>& stats,
                    GpuTiming& timing) {
    const auto start = Clock::now();
    // Preserve the legacy path's rejection of malformed/range-invalid inputs
    // before any CUDA allocation or context initialization.
    validate_batch(m, k, batch, batch, generators);
    GpuTiming setup;
    {
        GpuWorkspace workspace(m, k, batch);
        setup = workspace.setup_timing();
        workspace.run(batch, generators, weights, stats, timing);
    }
    timing.allocation_ms = setup.allocation_ms;
    timing.setup_ms = setup.setup_ms;
    finish_timing(timing, start);
}
}
