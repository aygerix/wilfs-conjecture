#pragma once
#include "apery.hpp"
#include <memory>

namespace wilf {
struct GpuTiming {
    // wall_ms is measured on the host. kernel_ms uses CUDA events; the other
    // components use host clocks. host_ms is the residual host/driver overhead.
    double wall_ms = 0;
    float kernel_ms = 0;
    double allocation_ms = 0, setup_ms = 0, upload_ms = 0, download_ms = 0, host_ms = 0;
};

// One device allocation/event set for a fixed modulus, supplied-generator
// count, and maximum batch size. Reuse run() across generations and repeats.
// Output arrays are candidate-major. Calls are synchronous and not thread-safe.
class GpuWorkspace {
public:
    GpuWorkspace(int m, int k, int capacity);
    ~GpuWorkspace() noexcept;
    GpuWorkspace(GpuWorkspace&&) noexcept;
    GpuWorkspace& operator=(GpuWorkspace&&) noexcept;
    GpuWorkspace(const GpuWorkspace&) = delete;
    GpuWorkspace& operator=(const GpuWorkspace&) = delete;

    int m() const noexcept;
    int k() const noexcept;
    int capacity() const noexcept;
    const GpuTiming& setup_timing() const noexcept;
    // Each run reports zero allocation/setup time. One-time construction costs
    // are available through setup_timing(). batch must lie in [1,capacity].
    void run(int batch, const std::vector<i64>& generators,
             std::vector<i64>& weights, std::vector<Basic>& stats,
             GpuTiming& timing);
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};

std::string gpu_description();
// Compatibility path; constructs one temporary workspace. Repeated callers
// should retain a GpuWorkspace instead.
void gpu_scan_batch(int m, int k, int batch, const std::vector<i64>& generators,
                    std::vector<i64>& weights, std::vector<Basic>& stats,
                    GpuTiming& timing);
}
