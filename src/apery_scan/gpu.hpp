#pragma once
#include "apery.hpp"

namespace wilf {
struct GpuTiming { double wall_ms = 0; float kernel_ms = 0; };
std::string gpu_description();
void gpu_scan_batch(int m, int k, int batch, const std::vector<i64>& generators,
                    std::vector<i64>& weights, std::vector<Basic>& stats,
                    GpuTiming& timing);
}
