# GW-SCAN: independent falsification search

No counterexample was found. All computations in this report ran on the GCP VM `fejer` (`us-east1-b`), using at most four single-threaded search/check processes at a time, at nice level 15. No existing project job was stopped or modified. The laptop was used for source/report edits, file transfer, and git inspection.

The completed exhaustive search covered **138,091,734,792 labeled instances**, **593,481,672 residue-complete labeled pairs**, and **67,389,859 labeled down-sets** (3,900,804 coordinate-permutation orbits), over the finite ranges below. The final structured/random run tested **92,810,240 candidate instances**, including repeated states, through **m = 100**, with **zero failures**. Its smallest E/c under c ≥ m and more than d maximal cells was **1/9**; the smallest saved non-minimal example had E/c = **21/79**. These are bounded computational results; they do not establish GW in general.

**Exact target and arithmetic.** D is any finite down-set in N^d of size m containing every unit vector. Positive n must give every residue modulo m once. For v(x)=x·n, M=max v, g=Σ floor(v/m), c=M−m+1, the failure predicate is E=d c−(d+1)g < 0. The search allows arbitrary residue-complete down-sets. The proved d≤2 and at-most-d-corner cases are recorded in [PROOFS.md](../../../../.research/PROOFS.md), “Down-set Wilf (GW)” and “GW: corner reflection and dimension two”. No additional theorem is used by the scanner.

**Independent exhaustive implementation.** [gw_scan.c](gw_scan.c) was written from the statement without importing or copying the lead’s Python. A cell is encoded in five bits per coordinate. The code bounds are d≤6 and m≤31; the reported runs use d≤5 and m≤30. All arithmetic for values, floors, g, c, and E is signed 64-bit integer arithmetic. Counts are unsigned 64-bit integers.

Generation appends addable cells in increasing encoded lexicographic order. Every componentwise predecessor has smaller encoding; therefore each down-set has exactly one such ordered construction. A branch is discarded if a missing unit vector has already been passed. At each final shape, all d! coordinate permutations are compared, and only the lexicographically least shape is scanned. If its coordinate stabilizer has size a, every count is weighted by d!/a. Thus canonical-downset counts are orbit counts, while labeled-downset, pair, instance, and hard-instance counts refer to all labeled coordinates. Every s in [1,m−1]^d that is residue-complete on the representative is tested; equal s coordinates are rejected because the unit vectors would collide. Partial coordinate assignments reject collisions only among cells whose support is already assigned.

For each valid (D,s), all k in {0,1,2}^d are tested. The exact identity g(D,s+mk)=g(D,s)+Σ_a k_a Σ_D x_a is used. M is computed from all maximal cells using positive n. Minimum E values are unweighted minima. The “hard” columns restrict only to t(D)>d, without imposing c≥m. In particular c=0 is included in the exhaustive search. Every equality instance is checked for Apéry minimality by shortest paths on residues.

**Completed exhaustive totals and runtimes.** Wall times below are elapsed time inside each m row; CPU times are process CPU time. Scans in different dimensions ran concurrently. Timings exclude SSH, copying, compilation, and the separate verifications.

| d | m range | Canonical shapes | Labeled shapes | Residue-complete pairs | Instances | Wall sum (s) | CPU sum (s) |
|---:|:---|---:|---:|---:|---:|---:|---:|
| 3 | 4–30 | 2,753,874 | 16,469,528 | 2,767,680 | 74,727,360 | 201.933193 | 181.061969 |
| 4 | 5–22 | 856,859 | 20,026,203 | 34,114,152 | 2,763,246,312 | 136.607845 | 121.102654 |
| 5 | 6–19 | 290,071 | 30,894,128 | 556,599,840 | 135,253,761,120 | 229.559204 | 205.913423 |
| Total | | 3,900,804 | 67,389,859 | 593,481,672 | 138,091,734,792 | 568.100242 | 508.078046 |

| d | m | Canonical D | Labeled D | Residue pairs | Instances | t>d instances | Failures | min E | min E, t>d | Wall s | CPU s |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 1 | 1 | 6 | 162 | 0 | 0 | 0 | NA | 0.000027 | 0.000025 |
| 3 | 5 | 2 | 6 | 48 | 1296 | 0 | 0 | 0 | NA | 0.000022 | 0.000020 |
| 3 | 6 | 5 | 18 | 126 | 3402 | 0 | 0 | 0 | NA | 0.000047 | 0.000046 |
| 3 | 7 | 11 | 44 | 444 | 11988 | 972 | 0 | 0 | 0 | 0.000127 | 0.000126 |
| 3 | 8 | 21 | 97 | 744 | 20088 | 2268 | 0 | 0 | 0 | 0.000306 | 0.000295 |
| 3 | 9 | 39 | 195 | 1656 | 44712 | 6804 | 0 | 0 | 0 | 0.000517 | 0.000516 |
| 3 | 10 | 73 | 377 | 2232 | 60264 | 10044 | 0 | 0 | 0 | 0.000972 | 0.000970 |
| 3 | 11 | 129 | 694 | 5520 | 149040 | 37260 | 0 | 0 | 0 | 0.016714 | 0.014840 |
| 3 | 12 | 227 | 1251 | 5136 | 138672 | 29160 | 0 | 0 | 0 | 0.003198 | 0.003196 |
| 3 | 13 | 390 | 2185 | 12984 | 350568 | 110808 | 0 | 0 | 0 | 0.007514 | 0.007512 |
| 3 | 14 | 662 | 3765 | 12210 | 329670 | 91044 | 0 | 0 | 0 | 0.011527 | 0.011525 |
| 3 | 15 | 1103 | 6354 | 19416 | 524232 | 173016 | 0 | 0 | 0 | 0.023412 | 0.021958 |
| 3 | 16 | 1829 | 10607 | 24408 | 659016 | 216432 | 0 | 0 | 0 | 0.040345 | 0.038607 |
| 3 | 17 | 2986 | 17446 | 48096 | 1298592 | 526176 | 0 | 0 | 0 | 0.084517 | 0.081466 |
| 3 | 18 | 4844 | 28449 | 34632 | 935064 | 310554 | 0 | 0 | 0 | 0.112275 | 0.112273 |
| 3 | 19 | 7778 | 45863 | 81468 | 2199636 | 976860 | 0 | 0 | 0 | 0.254457 | 0.254299 |
| 3 | 20 | 12409 | 73400 | 61464 | 1659528 | 639576 | 0 | 0 | 0 | 0.353108 | 0.353090 |
| 3 | 21 | 19624 | 116421 | 95076 | 2567052 | 1126548 | 0 | 0 | 0 | 0.668086 | 0.659931 |
| 3 | 22 | 30868 | 183472 | 103590 | 2796930 | 1155060 | 0 | 0 | 0 | 1.137266 | 1.122656 |
| 3 | 23 | 48203 | 287021 | 196284 | 5299668 | 2637360 | 0 | 0 | 0 | 2.653286 | 2.331187 |
| 3 | 24 | 74880 | 446472 | 123744 | 3341088 | 1396440 | 0 | 0 | 0 | 2.899616 | 2.844669 |
| 3 | 25 | 115621 | 690162 | 255720 | 6904440 | 3538080 | 0 | 0 | 0 | 6.483870 | 6.424932 |
| 3 | 26 | 177665 | 1061440 | 222000 | 5994000 | 2773116 | 0 | 0 | 0 | 9.833427 | 9.398809 |
| 3 | 27 | 271549 | 1623631 | 317412 | 8570124 | 4426488 | 0 | 0 | 0 | 19.968472 | 17.462593 |
| 3 | 28 | 413219 | 2472083 | 283896 | 7665192 | 3670272 | 0 | 0 | 0 | 27.885386 | 24.668348 |
| 3 | 29 | 625824 | 3745920 | 556752 | 15032304 | 8391600 | 0 | 0 | 0 | 62.020147 | 55.461103 |
| 3 | 30 | 943912 | 5652154 | 302616 | 8170632 | 3799224 | 0 | 0 | 0 | 67.474552 | 59.786977 |
| 4 | 5 | 1 | 1 | 24 | 1944 | 0 | 0 | 0 | NA | 0.000082 | 0.000080 |
| 4 | 6 | 2 | 10 | 288 | 23328 | 0 | 0 | 0 | NA | 0.000144 | 0.000143 |
| 4 | 7 | 6 | 49 | 1584 | 128304 | 0 | 0 | 0 | NA | 0.000469 | 0.000468 |
| 4 | 8 | 16 | 172 | 4752 | 384912 | 11664 | 0 | 0 | 0 | 0.001274 | 0.001273 |
| 4 | 9 | 38 | 512 | 14928 | 1209168 | 209952 | 0 | 0 | 0 | 0.003551 | 0.003550 |
| 4 | 10 | 86 | 1370 | 29664 | 2402784 | 466560 | 0 | 0 | 0 | 0.140582 | 0.061512 |
| 4 | 11 | 193 | 3396 | 86280 | 6988680 | 1963440 | 0 | 0 | 0 | 0.027758 | 0.018751 |
| 4 | 12 | 420 | 7968 | 109392 | 8860752 | 2865456 | 0 | 0 | 0 | 0.044304 | 0.032295 |
| 4 | 13 | 890 | 17910 | 316152 | 25608312 | 10375128 | 0 | 0 | 0 | 0.100321 | 0.088309 |
| 4 | 14 | 1860 | 38942 | 386688 | 31321728 | 12857616 | 0 | 0 | 0 | 0.162442 | 0.156832 |
| 4 | 15 | 3810 | 82338 | 735456 | 59571936 | 31415040 | 0 | 0 | 0 | 0.372757 | 0.365644 |
| 4 | 16 | 7697 | 170265 | 1026144 | 83117664 | 42021504 | 0 | 0 | 0 | 0.733804 | 0.733570 |
| 4 | 17 | 15325 | 345291 | 2287392 | 185278752 | 109112832 | 0 | 0 | 0 | 2.021464 | 1.829700 |
| 4 | 18 | 30169 | 689026 | 2057232 | 166635792 | 93280896 | 0 | 0 | 0 | 3.080628 | 3.065598 |
| 4 | 19 | 58695 | 1355253 | 5071032 | 410753592 | 267898752 | 0 | 0 | 0 | 8.816266 | 8.204589 |
| 4 | 20 | 113114 | 2632975 | 4488000 | 363528000 | 231398208 | 0 | 0 | 0 | 16.301297 | 14.258289 |
| 4 | 21 | 215890 | 5058305 | 7952184 | 644126904 | 450560880 | 0 | 0 | 0 | 35.892300 | 31.739049 |
| 4 | 22 | 408647 | 9622420 | 9546960 | 773303760 | 518814720 | 0 | 0 | 0 | 68.908402 | 60.543002 |
| 5 | 6 | 1 | 1 | 120 | 29160 | 0 | 0 | 0 | NA | 0.000913 | 0.000904 |
| 5 | 7 | 2 | 15 | 2160 | 524880 | 0 | 0 | 0 | NA | 0.024981 | 0.001949 |
| 5 | 8 | 6 | 110 | 15480 | 3761640 | 0 | 0 | 0 | NA | 0.005410 | 0.005409 |
| 5 | 9 | 18 | 550 | 78240 | 19012320 | 524880 | 0 | 0 | 0 | 0.142301 | 0.019277 |
| 5 | 10 | 51 | 2195 | 249120 | 60536160 | 3965760 | 0 | 0 | 0 | 0.061978 | 0.046954 |
| 5 | 11 | 135 | 7603 | 911280 | 221441040 | 47822400 | 0 | 0 | 0 | 0.162211 | 0.141188 |
| 5 | 12 | 352 | 23860 | 1766760 | 429322680 | 130549320 | 0 | 0 | 0 | 0.274925 | 0.265909 |
| 5 | 13 | 894 | 69580 | 5873760 | 1427323680 | 545875200 | 0 | 0 | 0 | 0.815830 | 0.815812 |
| 5 | 14 | 2229 | 191795 | 9375480 | 2278241640 | 929999880 | 0 | 0 | 0 | 1.521838 | 1.501977 |
| 5 | 15 | 5446 | 505640 | 22904880 | 5565885840 | 3019226400 | 0 | 0 | 0 | 4.959623 | 4.004200 |
| 5 | 16 | 13083 | 1285754 | 36193920 | 8795122560 | 4851057600 | 0 | 0 | 0 | 9.583533 | 8.407087 |
| 5 | 17 | 30892 | 3173220 | 93740160 | 22778858880 | 14820744960 | 0 | 0 | 0 | 26.425999 | 23.276757 |
| 5 | 18 | 71909 | 7637795 | 103822320 | 25228823760 | 16290525600 | 0 | 0 | 0 | 48.661845 | 42.641447 |
| 5 | 19 | 165053 | 17996010 | 281666160 | 68444876880 | 50401602000 | 0 | 0 | 0 | 136.917817 | 124.784553 |

Raw CSVs preserve the exact printed timings and all extra columns: [scan_d3.csv](results/scan_d3.csv), [scan_d3_extend.csv](results/scan_d3_extend.csv), [scan_d4.csv](results/scan_d4.csv), [scan_d4_extend.csv](results/scan_d4_extend.csv), [scan_d5.csv](results/scan_d5.csv), [scan_d5_extend.csv](results/scan_d5_extend.csv).

**Validation.** The supplied comparisons matched exactly:

| d | m | Minimal instances | Non-minimal instances | Total |
|---:|---:|---:|---:|---:|
| 3 | 11 | 20,286 | 128,754 | 149,040 |
| 4 | 10 | 214,056 | 2,188,728 | 2,402,784 |

For these two rows, minimality was classified for every instance by Dijkstra shortest paths in the residue graph with edges of weight n_a. Minimality means v(D) equals Ap(⟨m,n_1,…,n_d⟩,m); it does not assert that m is the multiplicity or that all listed generators are minimal. On every row in the whole exhaustive range, every E=0 instance was minimal (`equality_nonminimal=0`). The search made no minimality assumption.

The separate [verify.py](verify.py) builds labeled ideals by set-union growth from the star and deduplicates frozensets, without the C prefix/orbit algorithm. Its down-set counts agree through (d,m)=(3,11),(4,10),(5,11). It also literally enumerates all s and k, evaluates every floor pointwise, and matches the full C counts, hard counts, and minima at (3,7),(4,7),(5,7). AddressSanitizer and UndefinedBehaviorSanitizer found no issue on the exhaustive d=5, m=6…11 run. The 20 saved ranked records were checked by both Python and the independent pointwise C checker [gw_verify.c](gw_verify.c). These check the domain, all residues, all values/floors, corners, and mE=B−τ. Python independently checks all lower boxes and recomputes Apéry minimality using a heap-based shortest-path algorithm. See [verify.log](results/verify.log), [sanitizer.csv](results/sanitizer.csv), and their empty stderr files.

**Structured and random search.** The report uses the final reproducible run of [gw_adversary.c](gw_adversary.c), scale 16, xorshift64* seed 816341962711. An earlier scale-1 development run is excluded from all report totals and rankings. The final run took 67.211780 wall seconds and 57.924354 CPU seconds on fejer. The log is [adversary.log](results/adversary.log). Candidate counts include repeats and are not counts of distinct (D,n). No coordinate-orbit weights are applied in this phase. The ranked records are deduplicated under simultaneous coordinate permutations of D and n.

Near-stars consist of 0, all units, and selected degree-two cells. The code chooses distinct nonzero residues, then, for each uncovered residue, chooses a degree-two cell having that residue; attempts without such a cell are rejected. The construction attempts dimensions 3…12 and m from d+2 to min(100,d+1+d(d+1)/2); successful tested pairs reached m=49. This is a randomized subset of near-stars, not an enumeration of them.

Arms have two or three randomly lengthened coordinate axes plus the other unit vectors, and up to four attempted mixed degree-two additions. Dimensions are 3…5, with requested target size 20…100; duplicate mixed additions can reduce the actual size to 17. For each shape, randomized-order residue backtracking is capped at 12,000 recursive nodes and eight valid s. It is not exhaustive in shapes or weights.

Boxes use dimension 3…5, first three side lengths in 2…6, all further side lengths 2, and volume at most 100. All 189 such side-length tuples are used (including coordinate-equivalent ones). Residue backtracking is capped at 6,000 nodes and eight valid s per box. For each box and coordinate, a one-cell-flipped shape removes the unique maximal corner and adds L_a e_a. All 673 such attempts are used, with a 4,000-node/two-s cap. The old box is not required to be residue-complete for the same s.

Products take a separately generated 3-D Gröbner tile of size 7…25 times an interval of length 2…4, retaining volume at most 100. They use a 16,000-node/eight-s residue cap. The base tile is obtained by shortest paths with weights m+s_a, resolving equal weights by an additive lexicographic monomial order. Such positive weights ensure the unit vectors occur. Every successful structured pair is explicitly checked for the down-set and residue-bijection conditions.

The walk phase uses 1,024 independently seeded Gröbner tiles in dimensions 3…6 and m=20…100, each with 9,000 proposals. The first 3,000 proposals accept the available random flips without objective selection; if no flip is available, they change a lift coordinate. For a flip, all addable z are considered; the old cell y with matching residue must be maximal, must not be a unit, and must not be an immediate predecessor needed by z. The remaining 6,000 proposals use E/c with c≥m and t>d, a decreasing Metropolis temperature 0.03(1−step/9000)+0.001, lift-coordinate changes, and occasional multiplication of s by a random unit modulo m. There were 9,216,000 proposals, 5,030,906 accepted proposals, 2,608,114 accepted cell flips, and 353 seeds with no initial flip. Walks can revisit states; no distinct-shape count or connected-component coverage is claimed.

All successful structured pairs, all walk seeds, and every 1,000th walk state test every lift k in [0,3]^d when d≤6. Near-stars with d≥7 test 512 independent random lifts with replacement instead. Individual walk proposals test their current lift, which always remains in [0,3]^d. All candidate E values are checked, including those outside the ranking constraints. Integer cross-products compare saved E/c values exactly; floating point is used only for heuristic move acceptance.

| family | shape_attempts | residue_pairs | node_visits |
|---|---|---|---|
| nearstar | 192000 | 73496 | 0 |
| arms | 3200 | 2648 | 253349 |
| boxes | 189 | 1472 | 56458 |
| box_one_flip | 673 | 666 | 1408284 |
| product | 2326 | 18560 | 1448614 |

| family | tests | eligible | d_min | d_max | m_min | m_max | best_E | best_c |
|---|---|---|---|---|---|---|---|---|
| nearstar | 62045824 | 24273288 | 3 | 12 | 5 | 49 | 2 | 18 |
| arms | 1252352 | 51200 | 3 | 5 | 17 | 100 | 159 | 116 |
| boxes | 320000 | 0 | 3 | 5 | 8 | 100 | 0 | 0 |
| box_one_flip | 142464 | 142303 | 3 | 5 | 8 | 100 | 4 | 16 |
| product | 4751360 | 773921 | 4 | 4 | 14 | 100 | 14 | 36 |
| walk_seed | 1508224 | 1477725 | 3 | 6 | 20 | 100 | 10 | 30 |
| random_flip | 3072000 | 2663709 | 3 | 6 | 20 | 100 | 124 | 304 |
| local_search | 6144000 | 5352519 | 3 | 6 | 20 | 100 | 328 | 924 |
| walk_lifts | 13574016 | 13275478 | 3 | 6 | 20 | 100 | 10 | 30 |

The family size ranges in the second table refer to candidates actually tested, not rejected construction attempts. “eligible” requires c≥m and t>d. best_E/best_c is the exact minimum eligible ratio for that family; 0/0 for boxes means no eligible instance was tested. All 92,810,240 candidates had E≥0. The accepted walks and lift sweeps constitute a sample of arbitrary residue-complete down-sets; no exhaustive claim is made beyond the C scanner ranges.

**Ten smallest saved E/c values, up to coordinate permutations.** All have c≥m and t>d. Values and κ use the listed cell order. Full machine-readable records: [top10.jsonl](results/top10.jsonl).

| Rank | d | m | n | t | E | c | g | E/c | Apéry-minimal |
|---:|---:|---:|:---|---:|---:|---:|---:|:---|:---|
| 1 | 3 | 7 | [12, 11, 20] | 4 | 2 | 18 | 13 | 1/9 | True |
| 2 | 3 | 9 | [10, 12, 13] | 5 | 2 | 18 | 13 | 1/9 | True |
| 3 | 3 | 9 | [19, 21, 22] | 5 | 4 | 36 | 26 | 1/9 | True |
| 4 | 3 | 9 | [28, 30, 31] | 5 | 6 | 54 | 39 | 1/9 | True |
| 5 | 3 | 9 | [33, 34, 31] | 5 | 8 | 60 | 43 | 2/15 | True |
| 6 | 3 | 7 | [8, 19, 10] | 4 | 2 | 14 | 10 | 1/7 | True |
| 7 | 3 | 9 | [32, 29, 30] | 5 | 8 | 56 | 40 | 1/7 | True |
| 8 | 3 | 7 | [10, 15, 9] | 4 | 2 | 14 | 10 | 1/7 | True |
| 9 | 3 | 9 | [24, 25, 22] | 5 | 6 | 42 | 30 | 1/7 | True |
| 10 | 3 | 9 | [29, 30, 26] | 5 | 8 | 52 | 37 | 2/13 | True |

top10 rank 1: m=7, n=[12, 11, 20], M=24, c=18, g=13, E=3·18−4·13=2.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[0,2,0],[1,1,0],[2,0,0]],"v":[0,12,11,20,22,23,24],"kappa":[0,1,1,2,3,3,3]}
```

top10 rank 2: m=9, n=[10, 12, 13], M=26, c=18, g=13, E=3·18−4·13=2.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[2,0,0],[1,0,1],[0,2,0],[0,1,1],[0,0,2]],"v":[0,10,12,13,20,23,24,25,26],"kappa":[0,1,1,1,2,2,2,2,2]}
```

top10 rank 3: m=9, n=[19, 21, 22], M=44, c=36, g=26, E=3·36−4·26=4.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[2,0,0],[1,0,1],[0,2,0],[0,1,1],[0,0,2]],"v":[0,19,21,22,38,41,42,43,44],"kappa":[0,2,2,2,4,4,4,4,4]}
```

top10 rank 4: m=9, n=[28, 30, 31], M=62, c=54, g=39, E=3·54−4·39=6.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[2,0,0],[1,0,1],[0,2,0],[0,1,1],[0,0,2]],"v":[0,28,30,31,56,59,60,61,62],"kappa":[0,3,3,3,6,6,6,6,6]}
```

top10 rank 5: m=9, n=[33, 34, 31], M=68, c=60, g=43, E=3·60−4·43=8.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,0,1],[0,1,1],[2,0,0],[0,2,0],[0,0,2]],"v":[0,33,34,31,64,65,66,68,62],"kappa":[0,3,3,3,7,7,7,7,6]}
```

top10 rank 6: m=7, n=[8, 19, 10], M=20, c=14, g=10, E=3·14−4·10=2.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[2,0,0],[1,0,1],[0,0,2]],"v":[0,8,19,10,16,18,20],"kappa":[0,1,2,1,2,2,2]}
```

top10 rank 7: m=9, n=[32, 29, 30], M=64, c=56, g=40, E=3·56−4·40=8.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[2,0,0],[0,2,0],[0,0,2],[1,1,0],[1,0,1]],"v":[0,32,29,30,64,58,60,61,62],"kappa":[0,3,3,3,7,6,6,6,6]}
```

top10 rank 8: m=7, n=[10, 15, 9], M=20, c=14, g=10, E=3·14−4·10=2.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[0,0,2],[1,0,1],[2,0,0]],"v":[0,10,15,9,18,19,20],"kappa":[0,1,2,1,2,2,2]}
```

top10 rank 9: m=9, n=[24, 25, 22], M=50, c=42, g=30, E=3·42−4·30=6.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,0,1],[0,1,1],[2,0,0],[0,2,0],[0,0,2]],"v":[0,24,25,22,46,47,48,50,44],"kappa":[0,2,2,2,5,5,5,5,4]}
```

top10 rank 10: m=9, n=[29, 30, 26], M=60, c=52, g=37, E=3·52−4·37=8.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,0,1],[2,0,0],[1,1,0],[0,2,0],[0,0,2]],"v":[0,29,30,26,55,58,59,60,52],"kappa":[0,3,3,2,6,6,6,6,5]}
```

**Additional ten smallest saved non-minimal E/c values.** All have c≥m and t>d. Values and κ use the listed cell order. Full machine-readable records: [top10_nonminimal.jsonl](results/top10_nonminimal.jsonl).

| Rank | d | m | n | t | E | c | g | E/c | Apéry-minimal |
|---:|---:|---:|:---|---:|---:|---:|---:|:---|:---|
| 1 | 4 | 12 | [43, 46, 44, 37] | 7 | 21 | 79 | 59 | 21/79 | False |
| 2 | 4 | 12 | [38, 40, 35, 41] | 7 | 19 | 71 | 53 | 19/71 | False |
| 3 | 4 | 12 | [31, 34, 32, 25] | 7 | 15 | 55 | 41 | 3/11 | False |
| 4 | 3 | 8 | [26, 23, 27] | 4 | 13 | 47 | 32 | 13/47 | False |
| 5 | 4 | 12 | [26, 28, 23, 29] | 7 | 13 | 47 | 35 | 13/47 | False |
| 6 | 3 | 8 | [29, 30, 25] | 4 | 15 | 53 | 36 | 15/53 | False |
| 7 | 3 | 8 | [18, 15, 19] | 4 | 9 | 31 | 21 | 9/31 | False |
| 8 | 4 | 12 | [19, 22, 20, 13] | 7 | 9 | 31 | 23 | 9/31 | False |
| 9 | 5 | 17 | [54, 49, 58, 60, 55] | 11 | 30 | 102 | 80 | 5/17 | False |
| 10 | 3 | 8 | [21, 22, 17] | 4 | 11 | 37 | 25 | 11/37 | False |

top10_nonminimal rank 1: m=12, n=[43, 46, 44, 37], M=90, c=79, g=59, E=4·79−5·59=21.

```json
{"D":[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[2,0,0,0],[1,0,1,0],[0,0,2,0],[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,1,0,1]],"v":[0,43,46,44,37,86,87,88,89,90,81,83],"kappa":[0,3,3,3,3,7,7,7,7,7,6,6]}
```

top10_nonminimal rank 2: m=12, n=[38, 40, 35, 41], M=82, c=71, g=53, E=4·71−5·53=19.

```json
{"D":[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,1,0],[0,1,1,0],[1,1,0,0],[1,0,0,1],[0,2,0,0],[0,1,0,1],[0,0,0,2]],"v":[0,38,40,35,41,73,75,78,79,80,81,82],"kappa":[0,3,3,2,3,6,6,6,6,6,6,6]}
```

top10_nonminimal rank 3: m=12, n=[31, 34, 32, 25], M=66, c=55, g=41, E=4·55−5·41=15.

```json
{"D":[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[2,0,0,0],[1,0,1,0],[0,0,2,0],[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,1,0,1]],"v":[0,31,34,32,25,62,63,64,65,66,57,59],"kappa":[0,2,2,2,2,5,5,5,5,5,4,4]}
```

top10_nonminimal rank 4: m=8, n=[26, 23, 27], M=54, c=47, g=32, E=3·47−4·32=13.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,0],[2,0,0],[1,0,1],[0,0,2]],"v":[0,26,23,27,49,52,53,54],"kappa":[0,3,2,3,6,6,6,6]}
```

top10_nonminimal rank 5: m=12, n=[26, 28, 23, 29], M=58, c=47, g=35, E=4·47−5·35=13.

```json
{"D":[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,1,0],[0,1,1,0],[1,1,0,0],[1,0,0,1],[0,2,0,0],[0,1,0,1],[0,0,0,2]],"v":[0,26,28,23,29,49,51,54,55,56,57,58],"kappa":[0,2,2,1,2,4,4,4,4,4,4,4]}
```

top10_nonminimal rank 6: m=8, n=[29, 30, 25], M=60, c=53, g=36, E=3·53−4·36=15.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[2,0,0],[1,1,0],[0,2,0],[0,1,1]],"v":[0,29,30,25,58,59,60,55],"kappa":[0,3,3,3,7,7,7,6]}
```

top10_nonminimal rank 7: m=8, n=[18, 15, 19], M=38, c=31, g=21, E=3·31−4·21=9.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[1,1,0],[2,0,0],[1,0,1],[0,0,2]],"v":[0,18,15,19,33,36,37,38],"kappa":[0,2,1,2,4,4,4,4]}
```

top10_nonminimal rank 8: m=12, n=[19, 22, 20, 13], M=42, c=31, g=23, E=4·31−5·23=9.

```json
{"D":[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[2,0,0,0],[1,0,1,0],[0,0,2,0],[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,1,0,1]],"v":[0,19,22,20,13,38,39,40,41,42,33,35],"kappa":[0,1,1,1,1,3,3,3,3,3,2,2]}
```

top10_nonminimal rank 9: m=17, n=[54, 49, 58, 60, 55], M=118, c=102, g=80, E=5·102−6·80=30.

```json
{"D":[[0,0,0,0,0],[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[1,1,0,0,0],[0,1,0,0,1],[0,1,1,0,0],[2,0,0,0,0],[0,0,0,0,2],[1,0,1,0,0],[0,0,1,0,1],[1,0,0,1,0],[0,0,0,1,1],[0,0,2,0,0],[0,0,1,1,0]],"v":[0,54,49,58,60,55,103,104,107,108,110,112,113,114,115,116,118],"kappa":[0,3,2,3,3,3,6,6,6,6,6,6,6,6,6,6,6]}
```

top10_nonminimal rank 10: m=8, n=[21, 22, 17], M=44, c=37, g=25, E=3·37−4·25=11.

```json
{"D":[[0,0,0],[1,0,0],[0,1,0],[0,0,1],[2,0,0],[1,1,0],[0,2,0],[0,1,1]],"v":[0,21,22,17,42,43,44,39],"kappa":[0,2,2,2,5,5,5,4]}
```

**Reproduction.** Source files are in `src/scratch/gw/scan/`. Copy them to `~/wilf/gwscan/` on fejer with `gcloud compute scp --zone us-east1-b`, and run all following commands through `gcloud compute ssh fejer --zone us-east1-b --command "..."`. Never run the computation on the laptop. GCC was 13.3.0 and Python was 3.12.3. Use the commands below in the VM directory. Start at most four single-threaded computational commands concurrently; finish the first three scans before launching the three extensions. Each nohup line is a separate SSH command. The adversary can be the fourth concurrent job; run the two verification jobs after a slot is free.

Source hashes are saved in [source_sha256.txt](results/source_sha256.txt); raw result hashes are in [results_sha256.txt](results/results_sha256.txt). The final report/results were collected on 2026-10-19 UTC (2026-10-18 America/New_York).

```sh
cd ~/wilf/gwscan
gcc -O3 -std=c11 -Wall -Wextra gw_scan.c -o gw_scan
gcc -O3 -std=c11 -Wall -Wextra gw_adversary.c -lm -o gw_adversary_v2
gcc -O2 -std=c11 gw_verify.c -o gw_verify
nohup nice -n 15 ./gw_scan 3 4 22 11 > scan_d3.csv 2> scan_d3.err < /dev/null &
nohup nice -n 15 ./gw_scan 4 5 16 10 > scan_d4.csv 2> scan_d4.err < /dev/null &
nohup nice -n 15 ./gw_scan 5 6 14 > scan_d5.csv 2> scan_d5.err < /dev/null &
nohup nice -n 15 ./gw_scan 3 23 30 > scan_d3_extend.csv 2> scan_d3_extend.err < /dev/null &
nohup nice -n 15 ./gw_scan 4 17 22 > scan_d4_extend.csv 2> scan_d4_extend.err < /dev/null &
nohup nice -n 15 ./gw_scan 5 15 19 > scan_d5_extend.csv 2> scan_d5_extend.err < /dev/null &
mkdir -p adversary_r2
cd ~/wilf/gwscan/adversary_r2
nohup nice -n 15 ../gw_adversary_v2 16 816341962711 > adversary.log 2> adversary.err < /dev/null &
cd ~/wilf/gwscan
nohup nice -n 15 python3 -u verify.py --records adversary_r2/top10.jsonl adversary_r2/top10_nonminimal.jsonl --csv scan_d3.csv scan_d3_extend.csv scan_d4.csv scan_d4_extend.csv scan_d5.csv scan_d5_extend.csv > verify.log 2> verify.err < /dev/null &
gcc -O1 -g -std=c11 -fsanitize=address,undefined -fno-omit-frame-pointer gw_scan.c -o gw_scan_san
nohup nice -n 15 ./gw_scan_san 5 6 11 > sanitizer.csv 2> sanitizer.err < /dev/null &
# After the jobs above have finished:
nice -n 15 python3 make_report.py
```

**Coverage limits.** Exhaustiveness is limited to the three displayed dimension/size ranges and lifts k∈{0,1,2}^d. The larger families use the explicitly stated finite constructions, residue-search caps, PRNG seed, and lift sampling. No assertion is made about unvisited shapes, other residue vectors/lifts, d≥6 outside the structured sample, or m>100. The search stops on the first negative E and writes its data for independent verification; no such stop occurred. The top lists contain the smallest saved values from the final adversarial run, with ties retaining the first coordinate-inequivalent record encountered. They are not global optima for their m or dimension.
