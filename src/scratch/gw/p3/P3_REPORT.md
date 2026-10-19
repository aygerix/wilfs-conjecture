# P3 research report

Status: **P3 is proved on paper**, with exact exhaustive checks of the
counting lemmas on fejer. The proof uses residues only when `M<4m`.
The stronger local statements LP3 and TCI3 are not proved here.

## Proved theorem P3

Let `D` be a nonempty finite down-set in `N^d`, let `m=|D|` and `n in Z^d`,
and assume `n_a>m` whenever `e_a in D`. Assume `x -> x.n mod m` is a bijection from `D` onto
`Z/m`. With `v(x)=x.n`, `M=max v`, `kappa=floor(v/m)` and
`lambda=floor((M-v)/m)`, we have

`sum_D min(3,kappa) <= d sum_D min(3,lambda)`.

Inactive coordinates may be removed: their removal preserves all sums and
decreases the multiplier on the right. The case `D={0}` is immediate.
Hence the proof below assumes all `d` unit vectors belong to `D`.

## Proof overview and dependency

There are three regimes:

* `M<3m`: apply the proved depth-two theorem GW-16. Both floor functions
  are at most two, so P3 equals P2.
* `3m<=M<4m`: use the classification and weighted cubic shadow argument
  proved below. This is the only regime that uses residues.
* `M>=4m`: use coordinate column reflection and the explicit charging
  argument in the next section. It needs no residue hypothesis.

Thus these cases exhaust the exact target. GW-16 is the existing theorem
in `.research/PROOFS.md`, kernel-checked in `lean/Wilf/Window2.lean`.
For completeness, its short counting proof is also recalled at the end.

## Residue-free theorem for large maxima

**Theorem H.** Let `q>=1` be an integer, let D be any finite nonempty
down-set in `N^d`, let `n in Z^d`, and assume `n_a>q` for each active direction. No relation
between q and `|D|` is required. If `M=max_D x.n >=4q-1`, then

`sum_D min(3,floor(v/q)) <= d sum_D min(3,floor((M-v)/q))`.

In particular this proves the target for `M>=4m`, without residues.

Write `F(t)=min(3,floor(t/q))` for nonnegative integers t, and put

`B(x)=sum_a F(x_a*n_a)`.

### Lemma H1: column reflection and its exact slack

For a direction b and a base z with `z_b=0`, its nonempty column consists
of `z+j*e_b`, `0<=j<=J`. Write `delta=M-v(z)-J*n_b>=0`. Reflection of the
index `j -> J-j` gives

`sum_{j=0}^J F(M-v(z)-j*n_b)`

` = sum_{j=0}^J F(delta+j*n_b) >= sum_{j=0}^J F(j*n_b)`.

Let `s(b,z)` be the difference of these column sums, and let
`CS=sum_{(b,z)} s(b,z)`. Every column slack is nonnegative and

`d sum_D F(M-v) = sum_D B(x) + CS`.                 (H1)

Each nonempty column is counted once for its direction.

### Lemma H2: the only deficits are carried mixed quadratics

Let C be the set of cells `e_a+e_b in D`, `a!=b`, for which

`q<n_a<2q`, `q<n_b<2q`, and `n_a+n_b>=3q`.

These cells have `B(x)=2`, `F(v(x))=3`. Every other cell satisfies
`B(x)>=F(v(x))`.

Indeed degree zero and degree one give equality. An axis quadratic also
gives equality. A mixed quadratic with a summand of floor at least two
has `B>=3`, while the remaining mixed quadratics are exactly the cases
just listed or have `B=F(v)=2`. Finally, if `|x|>=3`, then

`B(x)>=sum_a min(3,x_a)>=3>=F(v(x))`,

because `n_a>q` implies `floor(x_a*n_a/q)>=x_a`.

Put `sigma(x)=max(0,B(x)-F(v(x)))`, `Sigma=sum_D sigma(x)`. Consequently

`sum_D B(x) - sum_D F(v(x)) = Sigma-|C|`.          (H2)

### Lemma H3: each carried pair has a distinct payment

For each unordered pair in C, orient its two directions as `(a,b)` with
`n_b>=n_a`; break ties by the coordinate index. Then `2n_b>=3q`.

If `y=e_a+2e_b` belongs to D, charge the pair to y. At this cubic,

`B(y)=F(n_a)+F(2n_b)=1+3=4`, `F(v(y))=3`,

so `sigma(y)=1`. Different carried pairs give different such cubics,
since the cubic's two positive coordinates recover the original pair.

Otherwise charge the pair to the b-column based at `e_a`. This column
has exactly the two cells `e_a`, `e_a+e_b`: a larger cell in the same
column would force `e_a+2e_b` into D by downward closure. Its slack is

`s(b,e_a)=F(M-n_a)+F(M-n_a-n_b)-F(0)-F(n_b)`.

Since `M>=4q-1` and the integral weight `n_a<=2q-1`, we have
`M-n_a>=2q`. Also `M-n_a-n_b>=0`, because the pair belongs to D. Thus

`s(b,e_a)>=2+0-0-1=1`.

Different carried pairs charged this way use different columns: the
direction b and base `e_a` determine the pair. The cubic charges and
column charges use separate terms of `Sigma+CS`. Therefore

`|C| <= Sigma+CS`.                                (H3)

### Conclusion of Theorem H

Combining the three exact relations,

`d sum_D F(M-v)-sum_D F(v) = CS+Sigma-|C| >=0`.

This proves Theorem H. It is a finite charging argument, with no
residues, no minimality, and no appeal to an asymptotic estimate.

The cutoff is sharp without residues: for the degree-at-most-two simplex
in two variables, `m=6`, `n=(11,11)`, the maximum is `22=4m-2` and the
two sides are 11 and 10. More generally the same six-cell down-set with
`n=(2q-1,2q-1)` has this failure for every integer `q>=2`, with maximum
`4q-2` (here q need not equal the cardinality).

## Proved subcase: M < 4m

For `M<3m`, P3 is the already proved P2, since both floor functions are at
most two. It remains to prove `3m <= M < 4m`.

Put `rho=4m-1-M`, so `0<=rho<m`, and define
`I_j=[jm-rho,(j+1)m-rho)` for integer `j`. Partition the active directions
into sets A, B, C according as `n_a` lies in `I_1`, `I_2`, `I_3`, and put
`a=|A|`, `b=|B|`, `c=|C|`, `d=a+b+c`.
Every unit belongs to one of these sets, since `m<n_a<=M`.

Classify the cells of degree at least two as follows:

* Q: degree-two cells in I2; cardinality q.
* R: degree-two cells supported in A and lying in I3; cardinality r.
* F: degree-two cells with one A direction and one B direction, in I3;
  cardinality s.
* T: degree-two cells supported in B, in I3; cardinality t.
* U: degree-three cells, all lying in I3; cardinality u.

Here a repeated direction is allowed in a degree-two cell.

### Lemma 1: the classification is exhaustive

Since each active weight exceeds m, every cell has degree at most three.
A degree-two cell involving C has value at least `m+(3m-rho)>M` and is
impossible. A degree-three cell involving B or C has value greater than
`2m+(2m-rho)>M`, and is impossible. Thus every cubic is supported in A.
A quadratic involving B has value greater than `m+(2m-rho)`, and hence
cannot lie in I2. Every quadratic has value greater than 2m, so its level
is at least two; every cubic has value greater than 3m, so its level is
three. These observations give the asserted classification and

`m=1+d+q+r+s+t+u`.

For every cubic x and every positive coordinate x_i, the divisor x-e_i
belongs to Q: it is quadratic, and
`v(x-e_i) <= M-n_i < 3m-rho`.

### Lemma 2: weighted cubic shadow bound

For any cubic monomial family U in a variables whose quadratic divisors
all belong to a family Q,

`3|U| <= (a+2)|Q|`.

Proof: count pairs `(x,i)` with weight `x_i`, for `x in U` and `x_i>0`.
Their total weight is `3|U|`. Map each pair to `(x-e_i,i)`. For a fixed
quadratic w in Q, the sum of possible incoming weights is at most
`sum_{i=1}^a (w_i+1)=a+2`. Summing proves the claim. In our setting,

`3u <= (a+2)q`.

Also, simply by counting monomials,

`q+r <= a(a+1)/2`, `s <= ab`, `t <= b(b+1)/2`.

### Lemma 3: the short interval bound

The values of cells in T are distinct integers, by residue injectivity.
Each is at least `4m-2rho` and at most `M=4m-rho-1`. This interval has
exactly rho integers. Consequently `t<=rho`.

In particular,

`rho-3t >= -b(b+1)`.

Indeed `rho>=t` implies `rho-3t>=-2t`, and
`2t<=b(b+1)`.

### Lemma 4: residue sum identity and window count

Write `g=sum_D kappa`, `ell=sum_D lambda`. If a cell has value in I_j,
then `lambda=3-j`. Hence

`ell=3+2a+b+q`.

Residue completeness gives `g+ell=M-m+1=3m-rho`.
To see this directly, write `M=3m+R`, `0<=R<m`, and `v=m*kappa+r_x`.
Then `kappa+lambda=3-[r_x>R]`; summing over a complete residue system gives
`g+ell=3m-(m-1-R)=M-m+1`.

Thus the desired P3, which here is `g<=d*ell`, is equivalent to

`W=(d+1)*ell-(3m-rho)>=0`.

### Completion of the low-maximum proof

Set

`H=2a(a+1)+(a-2)q-3(r+u)`.

By Lemma 2 and the quadratic count,

`H >= 2a(a+1)+(a-2)q-3(a(a+1)/2-q)-(a+2)q`

`   = a(a+1)/2-q >=0`.

Using the formulas for m and ell, direct expansion gives the exact
identity

`W=H + b(3a+b+1+q) - 3(s+t) + c(2a+b+q) + rho`.

Since `s<=ab` and `rho-3t>=-b(b+1)`, this implies

`W >= H + bq + c(2a+b+q) >=0`.

This proves P3 for every residue-complete down-set with `M<4m`, including
non-minimal down-sets. No Macaulay theorem is needed: the weighted cubic
divisor count suffices for this monomial formulation.

## Explicit dependence on residues

Two consequences are used, and no closure of `v(D)+mN` under addition is
assumed:

1. Residue injectivity implies distinct integer values, giving `t<=rho`.
2. Residue completeness gives `g+ell=M-m+1`.

The second consequence cannot be replaced by distinct values. For
`d=2`, `D={x:|x|<=2}`, `m=6`, `n=(9,10)`, all six values
`0,9,10,18,19,20` are distinct, but P3 has left side 11 and right side 10.

## Semigroup corollary

Let S be a numerical semigroup of multiplicity m, embedding dimension e,
and conductor c. Use its minimal factorization down-set for `Ap(S,m)`
as in GW-17. Then `d=e-1`, all active weights are greater than m, and
the values give one representative of each residue class. Apply P3.

The summand `min(3,kappa(x))` counts the gaps in that residue class below
3m. The summand `min(3,lambda(x))` counts the elements of S in that
class in `[c-3m,c)`. Hence

`#((N\S) intersect [0,3m)) <= (e-1) #(S intersect [c-3m,c))`.

If `c<=3m`, the first count is the full genus g and the second count is
`ell=#(S intersect [0,c))`. Since `g+ell=c`, this gives `e*ell>=c`,
including Eliahou's conductor-at-most-three-multiplicities theorem.
The argument above also handles non-minimal residue-complete down-sets
and the window for every conductor.

## Depth-two dependency, recalled

Here is a self-contained summary of GW-16. Put `N=NonMax(D)`, and let A
be the active directions with `n_a<2m`. Let T consist of the non-maximal
cells whose upper covers are all maximal and all use A directions. Let Y
consist of the nonzero maximal cells all of whose lower covers lie in T.

The depth-two left side is `2(m-1)-|A|`. Every non-maximal cell has
lambda at least one, and every cell of `N\T` has lambda at least two:
either it has an upper cover in a direction of weight at least 2m, or
it has a two-step extension of weight greater than 2m. Thus the right
side is at least `d(2|N|-|T|)`.

Choose a lower cover of each nonzero cell, avoiding T whenever possible.
Every lower cover is non-maximal, each cell receives at most d choices,
and only elements of Y can be forced into T. Therefore, writing
`s=d|N|-(m-1)`, we have `s>=d|T|-|Y|`.

Count pairs `(y,a)` with `y in Y`, `y_a>0`. Their images `(y-e_a,a)` lie
in `T x A`, so their number is at most `|A||T|`. Each y with support
at least two supplies two pairs. There is at most one axis-maximal y
for each direction in A, so at most `|A|` members of Y have support
one. Hence

`2|Y|<=|A||T|+|A|<=d|T|+|A|`.

It follows that `2s>=d|T|-|A|`, exactly the required comparison of the
left side with `d(2|N|-|T|)`. Residues are not used.

## What remains open

The exact requested P3 and its semigroup corollary are proved above.
The stronger LP3 and TCI3 on residue-complete down-sets remain open in
this report. No claim of a Lean formalization of the new proof is made.

## Computational verification

All program execution, compilation, exact optimization, enumeration, and
aggregation took place on **fejer**, in `~/wilf/p3/`, accessed using
`gcloud compute ssh fejer --zone us-east1-b`. No mathematical code was
run on the laptop. Jobs used `nice -n 10`, with at most four single-core
jobs at once; NumPy/SciPy exploratory jobs had BLAS/OpenMP thread limits
set to one. Software: Python 3.12.3, GCC 13.3.0.

### Exhaustive residue-complete verification of every proof identity

Script: `p3scan.c`, mode 1. All labeled down-sets with all d active
directions are covered. The C generator uses one representative per
coordinate-permutation orbit and weights it by the orbit size. For each
shape it enumerates **every** residue vector `s in {1,...,m-1}^d` giving
a bijection on D, and every lift `n=s+m*k`, `k in {1,2,3}^d`.
Inactive directions are handled by the proved reduction, not discarded
as a mathematical hypothesis.

| d | m range | Residue-complete instances | Low-regime lemma checks (`floor(M/m)=3`) | Theorem H checks (`M>=4m-1`) |
|---|---|---:|---:|---:|
| 2 | 3–24 | 109,584 | 60 | 109,534 |
| 3 | 4–18 | 4,526,766 | 2,718 | 4,525,026 |
| 4 | 5–14 | 76,929,912 | 189,240 | 76,814,856 |

Total: **81,566,262** residue-complete instances, with no P3 failure and
no failed proof assertion. The two regime check counts overlap at
`M=4m-1`; cases `M<3m` use the previously proved P2 theorem.

In the low regime the scanner asserts the complete cell classification,
all quadratic and cubic incidence bounds, `t<=rho`, the residue sum
identity, the exact expansion of W, and its claimed lower bound. In the
large regime it asserts each column's nonnegative slack, both exact
identities H1/H2, the characterization of every deficient cell, both
payments in H3, injectivity of each kind of payment, and the final bound.
The column and deficient-cell identities are also asserted outside the
large regime, where they remain valid.

### Exhaustive residue-free stress test of Theorem H

Same script, mode 0: every `n_a in [m+1,4m]`, with no residue filtering.

| d | m range | All instances | Instances satisfying `M>=4m-1` | Carried pairs paid in those instances |
|---|---|---:|---:|---:|
| 2 | 3–24 | 28,830,492 | 28,830,148 | 1,488,321 |
| 3 | 4–14 | 507,752,820 | 507,576,349 | 50,962,101 |
| 4 | 5–11 | 5,476,880,934 | 5,452,741,733 | 585,528,840 |

Total: **6,013,464,246** instances, including **5,989,148,230** instances
of Theorem H and **637,979,262** carried-pair payments. Every large-regime
assertion passed. There were 49 P3 failures without residues, all below
the cutoff, as allowed and expected: five in dimension two and 44 in
dimension three. The first such dimension-two failure has `m=6`.

### Independent verifier and agreement of counts

`verify_proof.py` independently enumerates labeled down-sets as Python
tuple sets. It uses neither the C scanner's bit encoding nor its orbit
weights. It checks each proof identity directly, including the actual
two-cell column or actual surplus cubic used for every payment.

| d | m range | Residue-complete instances independently checked |
|---|---|---:|
| 2 | 3–12 | 8,316 |
| 3 | 4–9 | 81,648 |
| 4 | 5–8 | 538,488 |

All **628,452** independent checks passed. For each dimension, the total
number of instances and both regime counts agree exactly with the C
scanner restricted to the same range. A further 1,000 exact random
checks, seed 20261019, used dimensions up to 12, down-sets of size at
most 100, and weights up to `30q` for a denominator q independent of
the cardinality; 999 of these satisfied Theorem H. All applicable checks
passed.

During discovery, `closure_test.py` used exact integer network minimum
cuts to test arbitrary order ideals inside weighted simplices. The two
recorded runs made 22,616 and 9,868 tests respectively, including
dimensions up to 16. Those finite searches are supplementary evidence;
the theorem does not depend on an optimization result or a bounded check.

The original CSVs, standard-error examples, independent verifier logs,
and aggregate counts are in `logs/`. `logs/verification_summary.json`
also records source SHA-256 hashes. `summarize.py` asserts completion of
all stated ranges and the independent count agreement before producing
that summary.

### Reproduction on fejer

Copy the four scripts in this directory to `~/wilf/p3/`, then compile:

```sh
gcloud compute ssh fejer --zone us-east1-b --command \
  'cd ~/wilf/p3 && gcc -O3 -std=c11 -Wall -Wextra p3scan.c -o p3scan'
```

The exhaustive invocations on fejer are:

```sh
nice -n 10 ./p3scan 2 3 24 1 > proof_res_d2.csv 2> proof_res_d2.err
nice -n 10 ./p3scan 3 4 18 1 > proof_res_d3.csv 2> proof_res_d3.err
nice -n 10 ./p3scan 4 5 14 1 > proof_res_d4.csv 2> proof_res_d4.err
nice -n 10 ./p3scan 2 3 24 0 > proof_nores_d2.csv 2> proof_nores_d2.err
nice -n 10 ./p3scan 3 4 14 0 > proof_nores_d3.csv 2> proof_nores_d3.err
nice -n 10 ./p3scan 4 5 11 0 > proof_nores_d4.csv 2> proof_nores_d4.err
nice -n 10 python3 verify_proof.py --d 2 --m 12 --examples > independent_d2.log 2>&1
nice -n 10 python3 verify_proof.py --d 3 --m 9 > independent_d3.log 2>&1
nice -n 10 python3 verify_proof.py --d 4 --m 8 > independent_d4.log 2>&1
nice -n 10 python3 verify_proof.py --random 1000 --seed 20261019 > independent_random.log 2>&1
```

The supplementary optimization runs and final aggregation are:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python closure_test.py --trials 3000 > closure.log 2>&1
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python closure_test.py --trials 5000 --dmax 16 --cap 5 --weightmax 2 --tops 2 --seed 20261020 > closure_highdim.log 2>&1
nice -n 10 python3 summarize.py
```

The saved CSV filenames indicate the mode and dimension. `p3scan.c`
adapts the shape-generation approach in the preexisting `gw_pscan.c`;
the Python enumeration provides the independent cross-check.

## False intermediate strengthenings and counterexamples

1. **Distinct integer values suffice for P3: false.** At `d=2`, `m=6`,
   `D={x:|x|<=2}`, `n=(9,10)`, the six values are
   `0,9,10,18,19,20`, all distinct. The left side is 11 and the right
   side is 10. The bounded scans have no smaller-cardinality P3 failure.
   Residues are `0,3,4,0,1,2`, so completeness fails.

2. **TCI3 without residues when M is large: false.** For `d=2`, `m=10`,
   `D={x:|x|<=3}`, `n=(11,19)`, `M=57`, the trapped set has size 4,
   the weighted band sum `|T^(1)|+2|T^(2)|` is 3, and `beta'_3=5`.
   Thus TCI3 asserts `12<=11`. This is at the smallest m with a TCI3
   failure in the dimension-two bounded scan. LP3 itself holds here:
   its two sides are 22 and 24.

3. **LP3 without residues when M is large: false.** Let `d=7`, let D
   contain every monomial of degree at most two and also `3e_1`, so
   `m=37`; take all seven weights equal to 56. Then `M=168` and the
   LP3 sides are 94 and 91. The local-height sum is
   `3+3+6+1=13`. This is not claimed to be globally smallest. In the
   analogous family in dimension d, with `3m/2<=n<5m/3`, the LP3 slack
   is `-(d-1)(d-6)/2`, so d=7 is the first failure in that family.

All three examples are independently evaluated by
`verify_proof.py --examples`; their exact output is saved in
`logs/independent_d2.log`. They concern dropped hypotheses or stronger
local statements and do not contradict the proved P3 theorem.

## Literature comparison and final research review

Eliahou's original conductor-at-most-three-multiplicities result is
Corollary 6.5 of [Wilf's conjecture and Macaulay's theorem](https://arxiv.org/pdf/1703.01761).
The paper's profile reduction and degree-two-to-degree-three estimates
suggest the low-regime organization above. In the present down-set
formulation, the needed cubic bound is supplied by the explicit weighted
monomial count in Lemma 2. No theorem from the paper is used as an
unproved substitute for a step here.

The initial separate strategy for K>=4 was to seek a general shape
inequality. Exact optimization supported that target, and the
coordinate-column identity then isolated its entire obstruction as
carried mixed quadratics. The two payments in Lemma H3 resolve that
obstruction, so no further enumeration or unresolved lemma is needed
for P3. The resulting proof meets the original target; future work on
LP3, TCI3, or higher windows is separate.
