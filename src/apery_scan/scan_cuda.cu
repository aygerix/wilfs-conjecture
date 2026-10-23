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

void gpu_scan_batch(int m, int k, int batch, const std::vector<i64>& generators,
                    std::vector<i64>& weights, std::vector<Basic>& stats,
                    GpuTiming& timing) {
    const auto start = std::chrono::steady_clock::now();
    if (m < 1 || m > 1024 || k < 0 || batch <= 0 || batch > (1 << 20) ||
        generators.size() != static_cast<size_t>(batch) * k)
        throw std::invalid_argument("invalid GPU batch shape (m<=1024)");
    for (i64 p : generators) {
        if (p <= m || static_cast<__int128>(8) * m * m * p >= INF)
            throw std::invalid_argument("GPU requires p>m and 8*m*m*p<INF");
    }
    i64 *input = nullptr, *output = nullptr;
    Basic* device_stats = nullptr;
    cudaEvent_t before = nullptr, after = nullptr;
    try {
        const size_t input_bytes = generators.size() * sizeof(i64);
        const size_t output_bytes = static_cast<size_t>(batch) * m * sizeof(i64);
        if (input_bytes) {
            check(cudaMalloc(&input, input_bytes), "allocate generators");
            check(cudaMemcpy(input, generators.data(), input_bytes, cudaMemcpyHostToDevice), "upload generators");
        }
        check(cudaMalloc(&output, output_bytes), "allocate Apéry arrays");
        check(cudaMalloc(&device_stats, static_cast<size_t>(batch) * sizeof(Basic)), "allocate statistics");
        check(cudaEventCreate(&before), "create start event");
        check(cudaEventCreate(&after), "create end event");
        check(cudaEventRecord(before), "record kernel start");
        if (m <= 256) scan_kernel<256><<<batch, 256>>>(m, k, input, output, device_stats);
        else if (m <= 512) scan_kernel<512><<<batch, 512>>>(m, k, input, output, device_stats);
        else scan_kernel<1024><<<batch, 1024>>>(m, k, input, output, device_stats);
        check(cudaGetLastError(), "launch cyclic scans");
        check(cudaEventRecord(after), "record kernel end");
        check(cudaEventSynchronize(after), "wait for cyclic scans");
        check(cudaEventElapsedTime(&timing.kernel_ms, before, after), "measure kernel");
        weights.resize(static_cast<size_t>(batch) * m); stats.resize(batch);
        check(cudaMemcpy(weights.data(), output, output_bytes, cudaMemcpyDeviceToHost), "download Apéry arrays");
        check(cudaMemcpy(stats.data(), device_stats, static_cast<size_t>(batch) * sizeof(Basic), cudaMemcpyDeviceToHost), "download statistics");
        check(cudaFree(input), "free generators"); input = nullptr;
        check(cudaFree(output), "free Apéry arrays"); output = nullptr;
        check(cudaFree(device_stats), "free statistics"); device_stats = nullptr;
        check(cudaEventDestroy(before), "destroy start event"); before = nullptr;
        check(cudaEventDestroy(after), "destroy end event"); after = nullptr;
    } catch (...) {
        cudaFree(input); cudaFree(output); cudaFree(device_stats);
        if (before) cudaEventDestroy(before);
        if (after) cudaEventDestroy(after);
        throw;
    }
    timing.wall_ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - start).count();
}
}
