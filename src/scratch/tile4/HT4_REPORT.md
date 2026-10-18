# HT4: four-dimensional lattice tiles

Domain: canonical distinct nonzero primitive residues, with every unit vector in D. Height/HCR ratios and certificate comparisons are exact; runtime projections are estimates.
Lattice fans include every positive-weight cone; the e=5 condition filters statistics only. Data below are finite observations.

## Certificate data

| m | e=5 tiles | min H/m | t of first minimizer | levels | missing pairs (1-based) | min HCR | min non-two-face HCR |
|---:|---:|---:|---:|:--|:--|---:|---:|
| 5 | 1 | 0 | 4 | [[0, 1], [1, 4]] | [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)] | 1 | None |
| 6 | 7 | 1/2 | 4 | [[0, 1], [1, 4], [2, 1]] | [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)] | 17/15 | None |
| 7 | 13 | 6/7 | 4 | [[0, 1], [1, 4], [2, 2]] | [(1, 2), (1, 3), (1, 4), (2, 4), (3, 4)] | 79/63 | None |
| 8 | 69 | 1/2 | 5 | [[0, 1], [1, 4], [2, 3]] | [(1, 2), (1, 3), (1, 4), (2, 4), (3, 4)] | 89/84 | None |
| 9 | 125 | 7/9 | 5 | [[0, 1], [1, 4], [2, 4]] | [(1, 2), (1, 3), (1, 4), (2, 4)] | 7/6 | None |
| 10 | 319 | 1/2 | 6 | [[0, 1], [1, 4], [2, 5]] | [(1, 2), (1, 4), (2, 4), (3, 4)] | 28/27 | None |
| 11 | 356 | 8/11 | 6 | [[0, 1], [1, 4], [2, 6]] | [(1, 2), (1, 3)] | 62/55 | None |
| 12 | 1278 | 1/2 | 7 | [[0, 1], [1, 4], [2, 7]] | [(1, 3)] | 34/33 | 413/198 |
| 13 | 1084 | 4/13 | 8 | [[0, 1], [1, 4], [2, 8]] | [(3, 4)] | 112/117 | 193/78 |
| 14 | 2551 | 4/7 | 8 | [[0, 1], [1, 4], [2, 8], [3, 1]] | [(1, 3)] | 96/91 | 37/21 |
| 15 | 3721 | 11/15 | 8 | [[0, 1], [1, 4], [2, 8], [3, 2]] | [(1, 2)] | 23/21 | 197/105 |
| 16 | 5388 | 7/8 | 8 | [[0, 1], [1, 4], [2, 7], [3, 4]] | [(1, 3), (1, 4), (2, 4)] | 409/360 | 13/9 |
| 17 | 5407 | 1 | 9 | [[0, 1], [1, 4], [2, 9], [3, 2], [4, 1]] | [(2, 4)] | 83/68 | 47/34 |
| 18 | 12980 | 5/6 | 9 | [[0, 1], [1, 4], [2, 8], [3, 5]] | [(1, 2)] | 511/459 | 229/153 |
| 19 | 10302 | 18/19 | 9 | [[0, 1], [1, 4], [2, 9], [3, 5]] | [(1, 4)] | 586/513 | 28/19 |
| 20 | 22103 | 1 | 9 | [[0, 1], [1, 4], [2, 8], [3, 7]] | [(1, 3)] | 219/190 | 257/190 |

Every minimizing tile, its maximal cells, and every corner q -> y(q) are in ht4_data_m.json.
The exact joint distribution for H/m < 2 is stored there as triples (H,t,count), and in ht4_joint.csv. The complete per-m trade-off step function is alpha_frontier, also in ht4_alpha.csv; min_H_by_t and alpha_tau_grid give supporting data.
For a finite range I, alpha_I(tau)=min{H/m: m in I, t/m <= tau}; this is a finite observed lower envelope, not an asymptotic bound.

| observed range | tau | alpha_I(tau) | witness (m,t,H) |
|:--|---:|---:|:--|
| 14–20 | 1/4 | 5/2 | (20, 5, 50) |
| 14–20 | 1/3 | 17/9 | (18, 6, 34) |
| 14–20 | 2/5 | 27/20 | (20, 8, 27) |
| 14–20 | 1/2 | 5/6 | (18, 9, 15) |
| 14–20 | 3/5 | 4/7 | (14, 8, 8) |
| 14–20 | 2/3 | 4/7 | (14, 8, 8) |
| 14–20 | 3/4 | 4/7 | (14, 8, 8) |
| 14–20 | 1 | 4/7 | (14, 8, 8) |

## Compiled enumerator validation

ht4_scan.cpp / ht4_core.hpp use uint16_t coordinates (m <= 256, explicit degree/coordinate assertions), int64 primitive homogeneous vertices and signed 128-bit intermediates.
Vertex cofactors are bounded by 6m^3. With m <= 256, clipping products, affine-rank tests and 4x4 determinants fit signed 128 bits; primary Dijkstra sums are checked before narrowing to int64.
The two primes are 2305843009213693951 and 2305843009213693921, checked by deterministic 64-bit Miller–Rabin. Positive vertex sums are smaller than both primes.
Every internal facet has an exact reciprocal neighbor with opposite normal and identical primitive vertex set. Neighbor inequalities hold on every facet vertex, and infinitesimal weights are checked strictly.
Facet closure is a rigorous completeness certificate: a generic path in the open simplex crosses only facets, so a nonempty set of full-dimensional fan cones closed under every facet neighbor is the whole fan. Modular volume sums are supplementary checks, not an unconditional probability-free volume certificate by themselves.
--exact additionally sums volumes with GMP rational arithmetic and requires exact sum 1 per lattice. Validation emits full tile sets only; normal runs retain per-m aggregates, extremizers/failures, and small per-lattice certificate metadata.

| m | lattices | tiles | e=5 tiles | complete multiset / HCR comparisons | exact volumes |
|---:|---:|---:|---:|:--|:--|
| 5 | 19 | 170 | 1 | PASS | PASS |
| 6 | 57 | 480 | 7 | PASS | PASS |
| 7 | 37 | 543 | 13 | PASS | PASS |
| 8 | 85 | 1301 | 69 | PASS | PASS |
| 9 | 84 | 1724 | 125 | PASS | PASS |
| 10 | 165 | 3300 | 319 | PASS | PASS |

Independent 4ti2/gfan cross-check (lead helper imported read-only; separate temporary files): [{'m': 5, 'r': [1, 2, 3, 4], 'tiles': 23, 'min_HCR': '1', 'status': 'PASS'}, {'m': 8, 'r': [1, 2, 3, 4], 'tiles': 22, 'min_HCR': '19/14', 'status': 'PASS'}, {'m': 13, 'r': [1, 2, 6, 9], 'tiles': 65, 'min_HCR': '112/117', 'status': 'PASS'}].

## Proved bounds and the remaining gap

**Boundary identity.** For every finite down-set D in N^4, define w(y)=sum_{a:y+e_a notin D}(y_a+1). Then sum_y w(y)=4m and H=sum_y w(y)ht(y). For maximal y, w(y)=4+|y|. Consequently H >= 4m - sum_{y maximal}(4+|y|).
Proof: each a-column has length y_a+1 at its unique top y. Summing column lengths gives m per direction and summing length times top height gives H. Every nonmaximal top has integer height at least 1.

**Cross-face bound.** For every finite down-set D with e_a+e_b absent, H >= sum_{x:x_a>0 or x_b>0}ht(x).
Proof: x_a>0 forces x_b=0 and x+e_b absent, so x is its own b-top. Likewise x_b>0 gives an a-top. The two sets of cells are disjoint. Retain only these terms in H.

**Long-axis bound.** Let L_i=1+max_{x in D}x_i. For every finite down-set D in N^4 and every i, H >= (L_i^2 sum_{b != i}1/L_b - 3L_i)/2. In particular, for every integer B>=1, if three axis lengths are <=B, then H/m >= (3/2)(m/B^7-1). Thus HT4 holds whenever m>=2B^7 in this subclass.
Proof: on the i-axis, the b-column lengths form a nonincreasing sequence of L_i positive integers with at most L_b constant blocks. A block of length s contributes at least s(s-1)/2 through its axis cells, since its top can move forward along i until the end of that block. Cauchy gives sum s^2>=L_i^2/L_b. Sum over b!=i. Finally m<=L_i B^3, L_i<=m, and sum 1/L_b>=3/B give the stated uniform bound.

**Maximal-cell contribution.** For every finite D containing the four unit vectors, R>=3t^2-7t+10 if t>=4, and R>=5t(t-1)/2 otherwise.
Proof: all maximal T values are >=6 except at most four degree-one cells with T=5. In decreasing order those exceptions occupy the last positions. Subtracting the last four indices from 6 sum_{i=0}^{t-1}i gives 3t^2-7t+10.

**Antichain bound (PROVED).** For every finite nonempty down-set E in N^k, n=|E|, every antichain has size at most C_k n^((k-1)/k), where C_1=1 and C_k=1+k C_(k-1). Thus C_2=3, C_3=10 and C_4=41.
Proof by induction. Put L=ceil(n^(1/k)). For antichain points with every coordinate >=L-1, count the L^k points of E directly below each. A fixed point of E is counted at most L^(k-1) times: the antichain points above it lie in an L-box and projection to any k-1 coordinates is injective. There are at most n/L such interior points. Every other antichain point is in a slice x_a=s with 0<=s<L-1. Ignore empty slices. In each coordinate, induction and concavity bound the sum of slice antichain sizes by C_(k-1)(L-1)^(1/(k-1))n^((k-2)/(k-1)). Multiply by k, use L-1<n^(1/k) and n/L<=n^((k-1)/k). This gives the stated recurrence. The k=1 base is immediate.

**Average-height bound (PROVED).** In the same setting, n^(-1)sum_x ht_E(x) >= n^(1/k)/(2C_k)-1/2.
Proof: each exact height level is an antichain, because x<y implies ht(x)>=ht(y)+|y-x|. Write W=C_k n^((k-1)/k); the first h height levels contain at most hW points. Hence sum ht >= sum_{h=1}^{floor(n/W)}(n-hW) >= n^2/(2W)-n/2. Writing n/W=q+r with 0<=r<1 proves the last inequality.

**All two-face down-sets have divergent H/m (PROVED).** For every finite down-set D in N^4 of size m with e_a+e_b absent,
`H/m >= min{m^(1/3)/160 - 1/2, m^(1/2)/12 - 1}.`
In particular H/m tends uniformly to infinity in this class, and HT4 holds for all such D with m>=32768000. No lattice or coherence assumption is needed.
Proof: split D into the arms U={x_a>0}, V={x_b>0}, and the face F={x_a=x_b=0}; put u=|U|, v=|V|, s=u+v, c=m-s. Shifting either arm by its unit vector gives a 3-D down-set, with the same heights as in D. If s>=m/4, the cross-face bound and the average-height bound with C_3=10 give H >= (u^(4/3)+v^(4/3))/20-s/2 >= m^(4/3)/160-m/2, by convexity.
If s<m/4, at most s cells of F have an extension into either arm. Thus at least e>=m-2s>m/2 face cells are singleton columns in both a and b. Each of their two terms is at least ht_F(x). Every height level in F has at most W=3sqrt(c) cells. The same height-level counting argument for any subset of e cells gives sum ht_F >= e^2/(2W)-e/2. Hence H >= e^2/(3sqrt(c))-e >= m^(3/2)/12-m. The two cases prove the inequality. At m>=320^3 both displayed lower bounds are at least 3/2, which implies HT4.

**Products cannot be a bounded-height counter-family (PROVED).** For every pair of nonempty finite down-sets A in N^k and B in N^l, let n=|A|, s=|B|, and define H with the appropriate number of directions in each factor. Then
`H(A x B)/(ns) = H(A)/n + H(B)/s + l*average(ht_A) + k*average(ht_B).`
Proof: heights add in a Cartesian product, and a column top changes only its own factor. Summing separately over directions in A and B gives the identity. If k,l>=1 are fixed and ns tends to infinity, max(n,s) tends to infinity; the average-height bound shows H(A x B)/(ns) tends to infinity.

**Planar sharpening (PROVED).** Every antichain of size w in a planar down-set of size n forces n>=w(w+1)/2, hence its width is at most sqrt(2n), and average height is at least sqrt(n)/(2sqrt(2))-1/2.
Proof: order the antichain by increasing first coordinate. Its i-th point dominates (i,w-1-i), using 0-based i. Thus the down-set contains the complete planar simplex of level w-1. Apply the same height-level counting argument with W=sqrt(2n).

**Practical product threshold (PROVED).** Every 2+2 product down-set satisfies H/m >= (sqrt(n)+sqrt(s))/sqrt(2)-2 >= sqrt(2)m^(1/4)-2. Therefore HT4 holds for m>=38, whether or not it is a lattice tile (38=ceil(2401/64)). A 1+3 product containing every unit vector satisfies H/m>=3(n-1)/2>=3/2, where n>=2 is the length of the one-dimensional factor, so it always satisfies HT4.
Proof: insert the planar average-height bound into the product identity, discard nonnegative factor H terms, and use AM–GM. For the 1+3 split, the one-dimensional factor has average height (n-1)/2.

**Boxes (PROVED).** For every four integers L_i>=2, let D=product_i{0,...,L_i-1} in N^4. Then H/m=(3/2)sum_i(L_i-1). These boxes are coherent cyclic lattice tiles for residues (1,L_1,L_1L_2,L_1L_2L_3) modulo m=product L_i; the residues are distinct and all unit vectors occur.
Proof: ht(x)=sum_i(L_i-1-x_i), and each residual coordinate occurs in exactly three top heights. Mixed-radix digits are residue-bijective. The minimal non-elements L_i e_i map to e_(i+1), for i<4, and L_4 e_4 maps to 0. Positive integer weights p_1=1, p_(i+1)=L_i p_i-1 satisfy all these strict inequalities. Thus box products do not give a bounded H/m family.

The general alternative H/m -> infinity versus a bounded infinite family remains unresolved for non-two-face, non-product tiles. The two-face result rules out the thin two-face minimizers as a bounded infinite family; the explicit threshold is much larger than the intended enumeration range. Neither finite minima nor the subclass bounds supply a practical global M0. A stronger inequality coupling H and R (or H and t), using the lattice restrictions, is the exact missing step.

## Reproducibility

All computation runs on fejer in ~/wilf/tile4. No lead job is stopped or modified. Build: g++ -O3 -std=c++17 -Wall -Wextra -pthread src/scratch/tile4/ht4_scan.cpp -lgmpxx -lgmp -o src/scratch/tile4/ht4_scan.
Data: /usr/bin/python3 -B src/scratch/tile4/ht4_tasks.py data 5 39. Validation: /usr/bin/python3 -B src/scratch/tile4/ht4_tasks.py validate 5 36. Use nohup with dedicated logs for long jobs.
Larger production runs are deferred until measured compiled benchmarks supply projected wall times to m=100,150,200.

## Complete Cartesian-product subclass

The exact finite check ht4_product_check.py passed 1280 ordered pairs of planar order ideals containing both unit vectors with product size <38. Minimum HT4 ratio was 10/9; details are in ht4_product_validation.json.
Coverage proof: every planar down-set is encoded uniquely by its nonincreasing positive row lengths (an integer partition). Each factor contains both unit vectors, so each has size >=3; product size <38 implies each factor has size <=12. All such partitions and all such ordered factor pairs are checked, with the product H identity additionally compared to the direct 4-D height definition.
**Conclusion (analytic proof plus exact finite check): every Cartesian-product down-set in N^4 containing all four unit vectors satisfies HT4, hence HCR>=1.** A proper coordinate split is either 1+3 or 2+2, up to swapping factors; the analytic bounds cover 1+3 and all 2+2 products with m>=38, and the finite check covers the rest.

## Finite adversarial searches

CP-SAT chooses a residue-bijective down-set inside a bounded simplex, minimizing the exact dynamic-program H. These are finite construction tests, not infinite families. A floating LP is used only to propose weights; acceptance requires a positive integer vector satisfying every strict cone inequality and exact Dijkstra reproduction.

| m | r | CP status | H/m | t | HCR | positive weight certified |
|---:|:--|:--|---:|---:|---:|:--|
| 101 | [1, 4, 16, 64] | OPTIMAL | 413/101 | 14 | 1433/505 | True |
| 50 | [1, 3, 9, 27] | OPTIMAL | 191/50 | 9 | 10051/3675 | True |
| 61 | [1, 4, 16, 3] | OPTIMAL | 293/61 | 9 | 18511/5490 | True |
| 80 | [1, 3, 9, 27] | OPTIMAL | 33/4 | 4 | 8921/1580 | True |

Full cells and exact accepted weight witnesses are stored in ht4_cp_m_b.json. An LP failure is not asserted to prove nonrealizability.
