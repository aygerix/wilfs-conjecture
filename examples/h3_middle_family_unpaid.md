# Height-3 cores outside every proved class (k ≥ 5, d ≥ 6, CR < 0, FLAT-CR < 0)

Found by the lead's adversarial annealer src/scratch/h3/anneal_h3.c (mode 1; fejer ~/wilf/h3/unpaid_sweep.log,
2026-10-19). Every state is an injective height-3 core: unit labels P mod m, and the listed cells of degree ≥ 2.
The core also contains 0 and every unit. The remaining residues are spikes, and units without a pair are maximal
(they are spikes too).

`f` is the exact MaxCL slack min_σ S, at the phase `sigma`. `ratio` is f / mean_σ S. CR and FLAT-CR are as in
P6B_REPORT §1, §7. Re-evaluate any row with

    anneal_h3 K m 0 0 0 2 P_1 ... P_K cell cell ...     (mode 2)

or with src/scratch/h3/hc_core_eval.py (also gives HC′).

None of these is a MaxCL counterexample. At most σ they are not close to tight: in the unpaid region the minimum ratio
found is 0.146 (t = 1), rising to ≥ 0.224 once t ≥ 3.

| K | m | k | q | p | t | s | d | CR | FLAT | f (σ) | P | cells of degree ≥ 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 20 | 5 | 11 | 1 | 1 | 2 | 7 | −5 | −37 | 61 (12) | 12,13,17,1,15 | 20000 11000 10100 10001 02000 01001 00200 00110 00020 00011 00002 00300 |
| 7 | 28 | 7 | 19 | 1 | 1 | 0 | 7 | −81 | −81 | 135 (26) | 8,2,27,11,9,3,12 | 2000000 1100000 1010000 1001000 1000100 1000001 0200000 0110000 0101000 0100010 0100001 0020000 0002000 0001001 0000200 0000101 0000020 0000011 0000002 0030000 |
| 6 | 22 | 6 | 14 | 1 | 1 | 0 | 6 | −28 | −63 | 84 (20) | 6,2,9,4,21,8 | 200000 101000 100010 100001 011000 010010 010001 002000 001100 001001 000110 000020 000011 000002 000030 |
| 5 | 22 | 5 | 13 | 2 | 2 | 1 | 6 | −40 | −106 | 82 (20) | 3,21,8,5,9 | 20000 11000 10100 10001 02000 01100 01010 00200 00110 00101 00020 00011 00002 12000 03000 |
| 6 | 26 | 6 | 16 | 2 | 2 | 1 | 7 | −41 | −124 | 145 (24) | 25,5,10,7,11,3 | 200000 110000 101000 100100 100001 011000 010100 010010 010001 002000 001100 001010 001001 000110 000020 000011 300000 200001 |
| 6 | 26 | 6 | 14 | 3 | 4 | 1 | 7 | −4 | −246 | 171 (0) | 3,6,17,14,7,1 | 110000 101000 100010 100001 020000 011000 010010 002000 001100 001010 001001 000200 000110 000101 003000 002100 001200 000300 |
| 7 | 38 | 7 | 22 | 3 | 4 | 4 | 11 | −80 | −309 | 451 (10) | 11,25,28,16,17,13,10 | 2000000 1100000 1010000 1001000 1000010 1000001 0200000 0110000 0100100 0100001 0020000 0011000 0010100 0010010 0002000 0001100 0001010 0000200 0000110 0000020 0000011 0000002 0300000 0210000 0120000 0030000 |
| 6 | 30 | 6 | 15 | 5 | 7 | 1 | 7 | −11 | −462 | 267 (20) | 29,26,7,6,25,4 | 200000 100100 100010 100001 020000 010100 010010 002000 001100 001001 000200 000110 000101 000020 000002 300000 200010 100020 030000 020010 010020 000030 |

Structure: the tightest unpaid states are near-flat (q close to C(k+1,2), p ≤ 3, t ≤ 2). Their pair faces are
defective, which is why ONE-CUBIC and THREE-CUBICS (complete faces) do not apply, and s is small. The t ≥ 4 rows
are binary or ternary cubic faces on 2–3 units ("columns of cubes") over a near-complete quadratic face.
