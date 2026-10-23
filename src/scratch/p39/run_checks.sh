#!/usr/bin/env bash
# Run on fejer from ~/wilf/p39. Reconstructs the selected exact certificates;
# does not repeat the larger sampler/enumeration records in data/.
set -euo pipefail
GUROBI_ROOT=${GUROBI_ROOT:-/home/jmercedes/gurobi1303/linux64}
export LD_LIBRARY_PATH="$GUROBI_ROOT/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
gcc -O2 certprobe.c -I"$GUROBI_ROOT/include" -L"$GUROBI_ROOT/lib" -lgurobi130 -lm -o certprobe
gcc -O3 upper_scan.c -o repair_scan
python3 verify_probe.py --completion-cut-check data/completion_cut_probe.jsonl.gz /tmp/wilf-p39-completion-cut.json
python3 verify_probe.py --completion-structure-check data/completion_cut_probe.jsonl.gz /tmp/wilf-p39-completion-structure.json
python3 verify_probe.py --completion-pool-check data/completion_pool_probe.jsonl.gz /tmp/wilf-p39-completion-pool.json
python3 verify_probe.py --partial-support-check data/partial_support_probe.jsonl.gz /tmp/wilf-p39-partial-support.json
python3 verify_probe.py --residue-check data/residue_descent_audit.jsonl.gz /tmp/wilf-p39-residue-summary.json
python3 verify_probe.py --tangent-check data/primitive_tangent.jsonl.gz /tmp/wilf-p39-tangent-summary.json
python3 verify_probe.py --support-audit data/axis_transport_zero.jsonl.gz /tmp/wilf-p39-support-anchors.json ./repair_scan
python3 verify_probe.py --support-audit data/support_weighted_endpoint.jsonl /tmp/wilf-p39-support-weighted.json ./repair_scan
python3 verify_probe.py --support-audit data/support_cycle_endpoint.jsonl /tmp/wilf-p39-support-cycle.json ./repair_scan
python3 verify_probe.py --lo-only-check data/support_lo_witnesses.jsonl.gz
for name in probe structural_probe residual_probe stress_probe climb_probe margin_probe; do
  python3 verify_probe.py "data/$name.jsonl.gz" "/tmp/wilf-p39-$name-summary.json"
done
for name in cone_survey capped_core_probe coupling_probe combined_probe joint_face_probe primitive_face_probe allowance_source_probe; do
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
python3 verify_matching.py --standalone data/joint_witness_matching.jsonl
python3 verify_matching.py --standalone data/interior_unit_candidate.jsonl
python3 verify_probe.py --axis-transport data/axis_transport.jsonl.gz /tmp/wilf-p39-axis-summary.json
python3 verify_probe.py --axis-transport data/axis_transport_zero.jsonl.gz /tmp/wilf-p39-axis-zero-summary.json
python3 verify_probe.py --axis-transport data/axis_backwards.jsonl.gz /tmp/wilf-p39-axis-climb-summary.json
python3 verify_probe.py --axis-face data/axis_face_probe.jsonl.gz /tmp/wilf-p39-axis-face-summary.json
python3 - <<'PY'
import json
full={tuple(sorted(R['generators'])):R['face']['optimum'] for R in json.load(open('/tmp/wilf-p39-joint_face_probe-summary.json'))}
reduced=json.load(open('/tmp/wilf-p39-primitive_face_probe-summary.json'))
assert all(full[tuple(sorted(R['generators']))]==R['face']['optimum'] for R in reduced)
print('MATCHED',len(reduced),'full/primitive joint-face optima exactly')
diagnostics=json.load(open('/tmp/wilf-p39-allowance_source_probe-summary.json'))
integer=[R['cone'] for R in diagnostics if sorted(R['generators'])==[104,420,453,509] and R.get('cone',{}).get('integer_witness')]
assert len(integer)==1 and integer[0]['fully_extendible'] and integer[0]['unique_apery_factorizations'] and integer[0]['integer_optimum']=='2' and integer[0]['real_upper_bound']=='7/3'
trade=[R['face']['primitive_projection'] for R in diagnostics if sorted(R['generators'])==[11,12,18] and 'face' in R]
assert len(trade)==1 and trade[0]['zero_gap_injected_sources']>=1
print('CERTIFIED fully extendible coordinate: real maximum7/3, integer maximum2; injected relations can be zero-gap trades')
ordinary={tuple(sorted(R['generators'])):R for R in json.load(open('/tmp/wilf-p39-axis-summary.json'))}
zero={tuple(sorted(R['generators'])):R for R in json.load(open('/tmp/wilf-p39-axis-zero-summary.json'))}
assert len(ordinary)==8 and len(zero)==36
assert ordinary[60,67,71,121]['baseline_bound']==-13
assert ordinary[60,61,67,71]['baseline_bound']==-10
assert ordinary[146,147,155,185]['baseline_bound']==-33
assert zero[60,67,71,121]['baseline_bound']==144
assert zero[104,420,453,509]['baseline_bound']==3107
assert zero[13,17]['mixed_cells']==zero[13,17]['transport_cost']==0
assert zero[13,17,27,29]['mixed_cells']==0 and zero[13,17,27,29]['known_zero']==12
for R in list(ordinary.values())+list(zero.values()):
    assert all(C['surplus']>0 for P in R['primitive_cycles'] for C in P['cycles'])
weighted=zero[153,166,170,317,325,474,617,766,921,925,1080]
orbit=[C for P in weighted['primitive_cycles'] if P['primitive']==170 for C in P['cycles'] if C['orbit']==4]
assert len(orbit)==1 and orbit[0]['column_weighted_strict_excess']==7 and orbit[0]['column_weighted_active_allowance']==42
print('CERTIFIED44 integer transport flows and primitive orbit allocations, including optimal negative original baselines and zero-demand controls; no universal sign assertion')
joint=json.load(open('/tmp/wilf-p39-joint_face_probe-summary.json'))
assert sum(R['face']['actual_dual_transfer']['certified_optimum'] is not None for R in joint)==20
profiles=json.load(open('/tmp/wilf-p39-axis-face-summary.json'))
complete={tuple(sorted(R['generators'])):R['minimum'] for R in profiles if R['epsilon']=='0'}
assert len(profiles)==6 and complete=={(60,67,71,121):'100',(146,155,184,535):'300',(146,147,155,185):'312'}
climbs=json.load(open('/tmp/wilf-p39-axis-climb-summary.json'))
assert len(climbs)==3 and any(sorted(R['generators'])==[60,67,131,181] and R['baseline_bound']==199 for R in climbs)
print('CERTIFIED20 actual minima by dual transfer,6 fixed-column regional LP minima,3 bounded descent endpoints; no universal sign assertion')
PY
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
./repair_scan --axis-seed 60 67 131 181 > /tmp/wilf-p39-fresh-axis-seed.jsonl
python3 verify_probe.py /tmp/wilf-p39-fresh-axis-seed.jsonl /tmp/wilf-p39-fresh-axis-seed-summary.json
