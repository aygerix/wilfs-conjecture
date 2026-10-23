#!/usr/bin/env bash
# Run on fejer from ~/wilf/p39. Reconstructs the selected exact certificates;
# does not repeat the larger sampler/enumeration records in data/.
set -euo pipefail
GUROBI_ROOT=${GUROBI_ROOT:-/home/jmercedes/gurobi1303/linux64}
export LD_LIBRARY_PATH="$GUROBI_ROOT/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
gcc -O2 certprobe.c -I"$GUROBI_ROOT/include" -L"$GUROBI_ROOT/lib" -lgurobi130 -lm -o certprobe
gcc -O3 upper_scan.c -o repair_scan
for name in probe structural_probe residual_probe stress_probe; do
  python3 verify_probe.py "data/$name.jsonl.gz" "/tmp/wilf-p39-$name-summary.json"
done
python3 verify_matching.py data/matching_residual.jsonl data/residual_probe.jsonl.gz
python3 verify_matching.py data/matching_boundary.jsonl data/structural_probe.jsonl.gz
python3 verify_matching.py data/matching_stress.jsonl data/stress_probe.jsonl.gz
python3 base_deflation.py
