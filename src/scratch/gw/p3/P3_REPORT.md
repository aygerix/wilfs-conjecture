# P3 research report

Status: a complete proof of the subcase `M < 4m` has been derived below. The
general depth-three window inequality is **not yet proved** in this report.
Computational sections will be completed from the fejer logs.

## Exact target

Let `D` be a nonempty finite down-set in `N^d`, `m=|D|`, and assume `n_a>m`
whenever `e_a in D`. Assume `x -> x.n mod m` is a bijection from `D` onto
`Z/m`. With `v(x)=x.n`, `M=max v`, `kappa=floor(v/m)` and
`lambda=floor((M-v)/m)`, the requested conclusion is

`sum_D min(3,kappa) <= d sum_D min(3,lambda)`.

Inactive coordinates may be removed: their removal preserves all sums and
decreases the multiplier on the right. The case `D={0}` is immediate.
Hence the proof below assumes all `d` unit vectors belong to `D`.

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

## Current strategic decision

The K<=3 regime is now resolved by an exact argument; the remaining target
is K>=4. A candidate sufficient lemma is that P3 holds in this regime
without any residue hypothesis. This is stronger than needed and is being
tested with two independent approaches: exhaustive fixed-cardinality
enumeration and integer minimum cuts over all order ideals of a bounded
weighted simplex. These are tests, not a proof. A proof or a counterexample
to that lemma is the next discriminating step. TCI3 is not being used in
this route because it can fail without residues even at K>=4.
