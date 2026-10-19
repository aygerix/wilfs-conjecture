"""Generate the factual GW scan report on fejer after all jobs finish."""
import csv
from fractions import Fraction
import json
from pathlib import Path
import re


root = Path('.')
files = [f'scan_d{d}{suffix}.csv' for d in (3, 4, 5) for suffix in ('', '_extend')]
rows = []
for name in files:
    rows.extend(csv.DictReader((root/name).open()))
rows.sort(key=lambda r: (int(r['d']), int(r['m'])))
expected = {3: (4, 30), 4: (5, 22), 5: (6, 19)}
for d, (lo, hi) in expected.items():
    assert [int(r['m']) for r in rows if int(r['d']) == d] == list(range(lo, hi+1))
for r in rows:
    assert int(r['failures']) == 0
    assert int(r['instances']) == int(r['residue_pairs'])*3**int(r['d'])
    assert int(r['hard_instances']) <= int(r['instances'])
    assert int(r['equality_nonminimal']) == 0
log = (root/'adversary_r2/adversary.log').read_text()
assert not (root/'adversary_r2/adversary.err').read_text()
assert not (root/'verify.err').read_text()
assert not (root/'sanitizer.err').read_text()
assert 'checked_records=20' in (root/'verify.log').read_text()
assert all(not (root/name.replace('.csv', '.err')).read_text() for name in files)
total = sum(int(r['instances']) for r in rows)
ideals = sum(int(r['labeled_downsets']) for r in rows)
pairs = sum(int(r['residue_pairs']) for r in rows)
canonical = sum(int(r['canonical_downsets']) for r in rows)
cpu = sum(float(r['cpu_seconds']) for r in rows)
wall = sum(float(r['wall_seconds']) for r in rows)
out = []


def add(s=''):
    out.append(s)


add('# GW-SCAN: independent falsification search')
add()
add('No counterexample was found. All computations in this report ran on the GCP VM '
    '`fejer` (`us-east1-b`), using at most four single-threaded search/check processes '
    'at a time, at nice level 15. No existing project job was stopped or modified. '
    'The laptop was used for source/report edits, file transfer, and git inspection.')
add()
add(f'The completed exhaustive search covered **{total:,} labeled instances**, '
    f'**{pairs:,} residue-complete labeled pairs**, and **{ideals:,} labeled down-sets** '
    f'({canonical:,} coordinate-permutation orbits), over the finite ranges below. '
    'The final structured/random run tested **92,810,240 candidate instances**, '
    'including repeated states, through **m = 100**, with **zero failures**. '
    'Its smallest E/c under c ≥ m and more than d maximal cells was **1/9**; '
    'the smallest saved non-minimal example had E/c = **21/79**. '
    'These are bounded computational results; they do not establish GW in general.')
add()
add('**Exact target and arithmetic.** D is any finite down-set in N^d of size m '
    'containing every unit vector. Positive n must give every residue modulo m once. '
    'For v(x)=x·n, M=max v, g=Σ floor(v/m), c=M−m+1, the failure predicate is '
    'E=d c−(d+1)g < 0. The search allows arbitrary residue-complete down-sets. '
    'The proved d≤2 and at-most-d-corner cases are recorded in '
    '[PROOFS.md](../../../../.research/PROOFS.md), “Down-set Wilf (GW)” and '
    '“GW: corner reflection and dimension two”. No additional theorem is used by the scanner.')
add()
add('**Independent exhaustive implementation.** [gw_scan.c](gw_scan.c) was written '
    'from the statement without importing or copying the lead’s Python. A cell is '
    'encoded in five bits per coordinate. The code bounds are d≤6 and m≤31; '
    'the reported runs use d≤5 and m≤30. All arithmetic for values, floors, g, c, '
    'and E is signed 64-bit integer arithmetic. Counts are unsigned 64-bit integers.')
add()
add('Generation appends addable cells in increasing encoded lexicographic order. '
    'Every componentwise predecessor has smaller encoding; therefore each down-set '
    'has exactly one such ordered construction. A branch is discarded if a missing '
    'unit vector has already been passed. At each final shape, all d! coordinate '
    'permutations are compared, and only the lexicographically least shape is '
    'scanned. If its coordinate stabilizer has size a, every count is weighted '
    'by d!/a. Thus canonical-downset counts are orbit counts, while labeled-downset, '
    'pair, instance, and hard-instance counts refer to all labeled coordinates. '
    'Every s in [1,m−1]^d that is residue-complete on the representative is tested; '
    'equal s coordinates are rejected because the unit vectors would collide. '
    'Partial coordinate assignments reject collisions only among cells whose '
    'support is already assigned.')
add()
add('For each valid (D,s), all k in {0,1,2}^d are tested. The exact identity '
    'g(D,s+mk)=g(D,s)+Σ_a k_a Σ_D x_a is used. M is computed from all maximal '
    'cells using positive n. Minimum E values are unweighted minima. '
    'The “hard” columns restrict only to t(D)>d, without imposing c≥m. '
    'In particular c=0 is included in the exhaustive search. Every equality '
    'instance is checked for Apéry minimality by shortest paths on residues.')
add()
add('**Completed exhaustive totals and runtimes.** Wall times below are elapsed '
    'time inside each m row; CPU times are process CPU time. Scans in different '
    'dimensions ran concurrently. Timings exclude SSH, copying, compilation, '
    'and the separate verifications.')
add()
add('| d | m range | Canonical shapes | Labeled shapes | Residue-complete pairs | Instances | Wall sum (s) | CPU sum (s) |')
add('|---:|:---|---:|---:|---:|---:|---:|---:|')
for d in expected:
    rr = [r for r in rows if int(r['d']) == d]
    sums = [sum(int(r[k]) for r in rr) for k in ('canonical_downsets', 'labeled_downsets', 'residue_pairs', 'instances')]
    add(f'| {d} | {expected[d][0]}–{expected[d][1]} | ' + ' | '.join(f'{a:,}' for a in sums)
        + f' | {sum(float(r["wall_seconds"]) for r in rr):.6f} | {sum(float(r["cpu_seconds"]) for r in rr):.6f} |')
add(f'| Total | | {canonical:,} | {ideals:,} | {pairs:,} | {total:,} | {wall:.6f} | {cpu:.6f} |')
add()
add('| d | m | Canonical D | Labeled D | Residue pairs | Instances | t>d instances | Failures | min E | min E, t>d | Wall s | CPU s |')
add('|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
keys = ('d','m','canonical_downsets','labeled_downsets','residue_pairs','instances','hard_instances','failures','min_E','min_E_more_than_d_corners','wall_seconds','cpu_seconds')
for r in rows:
    add('| ' + ' | '.join(r[k] for k in keys) + ' |')
add()
add('Raw CSVs preserve the exact printed timings and all extra columns: '
    + ', '.join(f'[{name}](results/{name})' for name in files) + '.')
add()
add('**Validation.** The supplied comparisons matched exactly:')
add()
add('| d | m | Minimal instances | Non-minimal instances | Total |')
add('|---:|---:|---:|---:|---:|')
for d,m,mi,nm in [(3,11,20286,128754),(4,10,214056,2188728)]:
    r = next(r for r in rows if int(r['d']) == d and int(r['m']) == m)
    assert int(r['minimal']) == mi and int(r['nonminimal']) == nm
    add(f'| {d} | {m} | {mi:,} | {nm:,} | {int(r["instances"]):,} |')
add()
add('For these two rows, minimality was classified for every instance by Dijkstra '
    'shortest paths in the residue graph with edges of weight n_a. Minimality means '
    'v(D) equals Ap(⟨m,n_1,…,n_d⟩,m); it does not assert that m is the multiplicity '
    'or that all listed generators are minimal. On every row in the whole exhaustive '
    'range, every E=0 instance was minimal (`equality_nonminimal=0`). '
    'The search made no minimality assumption.')
add()
add('The separate [verify.py](verify.py) builds labeled ideals by set-union growth '
    'from the star and deduplicates frozensets, without the C prefix/orbit algorithm. '
    'Its down-set counts agree through (d,m)=(3,11),(4,10),(5,11). It also literally '
    'enumerates all s and k, evaluates every floor pointwise, and matches the full '
    'C counts, hard counts, and minima at (3,7),(4,7),(5,7). '
    'AddressSanitizer and UndefinedBehaviorSanitizer found no issue on the exhaustive '
    'd=5, m=6…11 run. The 20 saved ranked records were checked by both Python '
    'and the independent pointwise C checker [gw_verify.c](gw_verify.c). '
    'These check the domain, all residues, all values/floors, corners, '
    'and mE=B−τ. Python independently checks all lower boxes and recomputes '
    'Apéry minimality using a heap-based shortest-path algorithm. '
    'See [verify.log](results/verify.log), [sanitizer.csv](results/sanitizer.csv), '
    'and their empty stderr files.')
add()
add('**Structured and random search.** The report uses the final reproducible run '
    'of [gw_adversary.c](gw_adversary.c), scale 16, xorshift64* seed 816341962711. '
    'An earlier scale-1 development run is excluded from all report totals and rankings. '
    'The final run took 67.211780 wall seconds and 57.924354 CPU seconds on fejer. '
    'The log is [adversary.log](results/adversary.log). Candidate counts include repeats '
    'and are not counts of distinct (D,n). No coordinate-orbit weights are applied '
    'in this phase. The ranked records are deduplicated under simultaneous '
    'coordinate permutations of D and n.')
add()
add('Near-stars consist of 0, all units, and selected degree-two cells. The code '
    'chooses distinct nonzero residues, then, for each uncovered residue, chooses '
    'a degree-two cell having that residue; attempts without such a cell are rejected. '
    'The construction attempts dimensions 3…12 and m from d+2 to '
    'min(100,d+1+d(d+1)/2); successful tested pairs reached m=49. '
    'This is a randomized subset of near-stars, not an enumeration of them.')
add()
add('Arms have two or three randomly lengthened coordinate axes plus the other '
    'unit vectors, and up to four attempted mixed degree-two additions. '
    'Dimensions are 3…5, with requested target size 20…100; duplicate mixed '
    'additions can reduce the actual size to 17. For each shape, randomized-order '
    'residue backtracking is capped at 12,000 recursive nodes and eight valid s. '
    'It is not exhaustive in shapes or weights.')
add()
add('Boxes use dimension 3…5, first three side lengths in 2…6, all further side '
    'lengths 2, and volume at most 100. All 189 such side-length tuples are used '
    '(including coordinate-equivalent ones). Residue backtracking is capped at '
    '6,000 nodes and eight valid s per box. For each box and coordinate, '
    'a one-cell-flipped shape removes the unique maximal corner and adds '
    'L_a e_a. All 673 such attempts are used, with a 4,000-node/two-s cap. '
    'The old box is not required to be residue-complete for the same s.')
add()
add('Products take a separately generated 3-D Gröbner tile of size 7…25 '
    'times an interval of length 2…4, retaining volume at most 100. '
    'They use a 16,000-node/eight-s residue cap. The base tile is obtained '
    'by shortest paths with weights m+s_a, resolving equal weights by an '
    'additive lexicographic monomial order. Such positive weights ensure '
    'the unit vectors occur. Every successful structured pair is explicitly '
    'checked for the down-set and residue-bijection conditions.')
add()
add('The walk phase uses 1,024 independently seeded Gröbner tiles in dimensions '
    '3…6 and m=20…100, each with 9,000 proposals. The first 3,000 proposals '
    'accept the available random flips without objective selection; if no flip '
    'is available, they change a lift coordinate. For a flip, all addable z are '
    'considered; the old cell y with matching residue must be maximal, must '
    'not be a unit, and must not be an immediate predecessor needed by z. '
    'The remaining 6,000 proposals use E/c with c≥m and t>d, a decreasing '
    'Metropolis temperature 0.03(1−step/9000)+0.001, lift-coordinate changes, '
    'and occasional multiplication of s by a random unit modulo m. '
    'There were 9,216,000 proposals, 5,030,906 accepted proposals, '
    '2,608,114 accepted cell flips, and 353 seeds with no initial flip. '
    'Walks can revisit states; no distinct-shape count or connected-component '
    'coverage is claimed.')
add()
add('All successful structured pairs, all walk seeds, and every 1,000th walk '
    'state test every lift k in [0,3]^d when d≤6. Near-stars with d≥7 test '
    '512 independent random lifts with replacement instead. Individual walk '
    'proposals test their current lift, which always remains in [0,3]^d. '
    'All candidate E values are checked, including those outside the ranking '
    'constraints. Integer cross-products compare saved E/c values exactly; '
    'floating point is used only for heuristic move acceptance.')
add()
lines = log.splitlines()
for header, cols in [('family,shape_attempts,residue_pairs,node_visits', 4),
                     ('family,tests,eligible,d_min,d_max,m_min,m_max,best_E,best_c', 9)]:
    start = lines.index(header)+1
    add('| ' + ' | '.join(header.split(',')) + ' |')
    add('|' + '|'.join(['---']*cols) + '|')
    for line in lines[start:]:
        if len(line.split(',')) != cols:
            break
        add('| ' + ' | '.join(line.split(',')) + ' |')
    add()
add('The family size ranges in the second table refer to candidates actually '
    'tested, not rejected construction attempts. “eligible” requires c≥m '
    'and t>d. best_E/best_c is the exact minimum eligible ratio for that family; '
    '0/0 for boxes means no eligible instance was tested. All 92,810,240 '
    'candidates had E≥0. The accepted walks and lift sweeps constitute a '
    'sample of arbitrary residue-complete down-sets; no exhaustive claim '
    'is made beyond the C scanner ranges.')
add()


def ranked(name, title):
    rr = [json.loads(line) for line in (root/'verified'/f'{name}.jsonl').read_text().splitlines()]
    add(f'**{title}.** All have c≥m and t>d. Values and κ use the listed cell order. '
        f'Full machine-readable records: [{name}.jsonl](results/{name}.jsonl).')
    add()
    add('| Rank | d | m | n | t | E | c | g | E/c | Apéry-minimal |')
    add('|---:|---:|---:|:---|---:|---:|---:|---:|:---|:---|')
    for i,r in enumerate(rr,1):
        add(f'| {i} | {r["d"]} | {r["m"]} | {r["n"]} | {r["corners"]} | '
            f'{r["E"]} | {r["c"]} | {r["g"]} | {r["ratio"]} | {r["minimal"]} |')
    add()
    for i,r in enumerate(rr,1):
        add(f'{name} rank {i}: m={r["m"]}, n={r["n"]}, '
            f'M={r["M"]}, c={r["c"]}, g={r["g"]}, '
            f'E={r["d"]}·{r["c"]}−{r["d"]+1}·{r["g"]}={r["E"]}.')
        add()
        add('```json')
        add(json.dumps({'D':r['D'], 'v':r['values'], 'kappa':r['kappa']},separators=(',',':')))
        add('```')
        add()


ranked('top10', 'Ten smallest saved E/c values, up to coordinate permutations')
ranked('top10_nonminimal', 'Additional ten smallest saved non-minimal E/c values')
add('**Reproduction.** Source files are in `src/scratch/gw/scan/`. '
    'Copy them to `~/wilf/gwscan/` on fejer with `gcloud compute scp --zone '
    'us-east1-b`, and run all following commands through '
    '`gcloud compute ssh fejer --zone us-east1-b --command "..."`. '
    'Never run the computation on the laptop. GCC was 13.3.0 and Python was '
    '3.12.3. Use the commands below in the VM directory. Start at most '
    'four single-threaded computational commands concurrently; finish the '
    'first three scans before launching the three extensions. Each '
    'nohup line is a separate SSH command. The adversary can be the fourth '
    'concurrent job; run the two verification jobs after a slot is free.')
add()
add('Source hashes are saved in [source_sha256.txt](results/source_sha256.txt); '
    'raw result hashes are in [results_sha256.txt](results/results_sha256.txt). '
    'The final report/results were collected on 2026-10-19 UTC '
    '(2026-10-18 America/New_York).')
add()
add('```sh')
add('cd ~/wilf/gwscan')
add('gcc -O3 -std=c11 -Wall -Wextra gw_scan.c -o gw_scan')
add('gcc -O3 -std=c11 -Wall -Wextra gw_adversary.c -lm -o gw_adversary_v2')
add('gcc -O2 -std=c11 gw_verify.c -o gw_verify')
for d, lo, hi, check in [(3,4,22,11),(4,5,16,10),(5,6,14,None),(3,23,30,None),(4,17,22,None),(5,15,19,None)]:
    ext = '_extend' if (d,lo) in [(3,23),(4,17),(5,15)] else ''
    extra = '' if check is None else f' {check}'
    add(f'nohup nice -n 15 ./gw_scan {d} {lo} {hi}{extra} > scan_d{d}{ext}.csv 2> scan_d{d}{ext}.err < /dev/null &')
add('mkdir -p adversary_r2')
add('cd ~/wilf/gwscan/adversary_r2')
add('nohup nice -n 15 ../gw_adversary_v2 16 816341962711 > adversary.log 2> adversary.err < /dev/null &')
add('cd ~/wilf/gwscan')
add('nohup nice -n 15 python3 -u verify.py --records adversary_r2/top10.jsonl adversary_r2/top10_nonminimal.jsonl --csv scan_d3.csv scan_d3_extend.csv scan_d4.csv scan_d4_extend.csv scan_d5.csv scan_d5_extend.csv > verify.log 2> verify.err < /dev/null &')
add('gcc -O1 -g -std=c11 -fsanitize=address,undefined -fno-omit-frame-pointer gw_scan.c -o gw_scan_san')
add('nohup nice -n 15 ./gw_scan_san 5 6 11 > sanitizer.csv 2> sanitizer.err < /dev/null &')
add('# After the jobs above have finished:')
add('nice -n 15 python3 make_report.py')
add('```')
add()
add('**Coverage limits.** Exhaustiveness is limited to the three displayed '
    'dimension/size ranges and lifts k∈{0,1,2}^d. The larger families use '
    'the explicitly stated finite constructions, residue-search caps, '
    'PRNG seed, and lift sampling. No assertion is made about unvisited '
    'shapes, other residue vectors/lifts, d≥6 outside the structured sample, '
    'or m>100. The search stops on the first negative E and writes its '
    'data for independent verification; no such stop occurred. '
    'The top lists contain the smallest saved values from the final '
    'adversarial run, with ties retaining the first coordinate-inequivalent '
    'record encountered. They are not global optima for their m or dimension.')
(root/'GW_SCAN_REPORT.md').write_text('\n'.join(out)+'\n')
print(f'REPORT: {len(rows)} rows; {total:,} exhaustive instances; {ideals:,} downsets; {pairs:,} residue pairs')
