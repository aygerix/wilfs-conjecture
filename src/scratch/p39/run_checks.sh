#!/usr/bin/env bash
# Run on fejer from ~/wilf/p39. Reconstructs the selected exact certificates;
# does not repeat the larger sampler/enumeration records in data/.
set -euo pipefail
GUROBI_ROOT=${GUROBI_ROOT:-/home/jmercedes/gurobi1303/linux64}
export LD_LIBRARY_PATH="$GUROBI_ROOT/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
gcc -O2 certprobe.c -I"$GUROBI_ROOT/include" -L"$GUROBI_ROOT/lib" -lgurobi130 -lm -o certprobe
gcc -O3 upper_scan.c -o repair_scan
for name in probe structural_probe residual_probe stress_probe climb_probe margin_probe; do
  python3 verify_probe.py "data/$name.jsonl.gz" "/tmp/wilf-p39-$name-summary.json"
done
for name in cone_survey capped_core_probe coupling_probe combined_probe; do
  python3 verify_probe.py "data/$name.jsonl.gz" "/tmp/wilf-p39-$name-summary.json"
done
./certprobe 20 21 22 > /tmp/wilf-p39-fresh-probe.jsonl
python3 verify_probe.py /tmp/wilf-p39-fresh-probe.jsonl /tmp/wilf-p39-fresh-summary.json
python3 verify_matching.py data/matching_residual.jsonl data/residual_probe.jsonl.gz
python3 verify_matching.py data/matching_boundary.jsonl data/structural_probe.jsonl.gz
python3 verify_matching.py data/matching_stress.jsonl data/stress_probe.jsonl.gz
python3 verify_matching.py --standalone data/matching_loss.jsonl data/climb_matching.jsonl data/lattice_matching.jsonl.gz data/lattice_cover_large.jsonl.gz data/capacity_audit.jsonl data/dichotomy_matching.jsonl data/low_wilf_matching.jsonl
python3 verify_matching.py --standalone data/individual_selected.jsonl data/top_primitive.jsonl data/top_primitive_transport.jsonl
python3 verify_matching.py --standalone data/weighted_matching.jsonl data/integer_weighted_matching.jsonl data/weighted_search_selected.jsonl
python3 verify_matching.py --standalone data/combined_selected.jsonl data/equality_selected.jsonl
python3 verify_matching.py data/transport_all.jsonl data/probe.jsonl.gz data/structural_probe.jsonl.gz data/residual_probe.jsonl.gz data/stress_probe.jsonl.gz data/climb_probe.jsonl.gz data/margin_probe.jsonl.gz
./repair_scan --position-audit 128
./repair_scan --capacity-audit 66 67 71 72 98 103 128 > /tmp/wilf-p39-capacity.jsonl
python3 verify_matching.py --standalone /tmp/wilf-p39-capacity.jsonl
./repair_scan --cover 64 67 69 77 129 > /tmp/wilf-p39-cover.jsonl
python3 verify_matching.py --standalone /tmp/wilf-p39-cover.jsonl
python3 upper_dp.py --propagate data/climb_probe.jsonl.gz > /tmp/wilf-p39-propagate.log
python3 upper_dp.py --rigid data/climb_probe.jsonl.gz > rigid_closure.log
python3 upper_dp.py --rigid data/residual_probe.jsonl.gz >> rigid_closure.log
python3 upper_dp.py --rigid data/margin_probe.jsonl.gz >> rigid_closure.log
cat rigid_closure.log
python3 upper_dp.py --chain-budget data/probe.jsonl.gz data/integer_weighted_matching.jsonl
python3 upper_dp.py --chain-budget data/stress_probe.jsonl.gz data/integer_weighted_matching.jsonl
python3 base_deflation.py
