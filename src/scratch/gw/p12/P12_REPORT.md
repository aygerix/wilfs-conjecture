# P12: REST-M3

Research date: 2026-10-19. All mathematical computations reported here run on
fejer in `~/wilf/p12/rest/`, with `nice -n 10`. Earlier reports are unchanged.
Status words distinguish PROVED, COUNTEREXAMPLE, FINITE CHECK and OPEN.

**Outcome: REST-M3 is FALSE, including for `e>=3` and `3e<m`. The weaker
target `Delta<=C2` on the same class is also FALSE.**

- `<32,39,...,45>` has `M=134>=3*39` and `REST=47>0`.
- `<87,105,...,122>` has `M=365>=3*105`, `REST=4937`,
  `con(0)=-1018`, and `Delta=3919>C2=3741`.
- Sections 3–6 prove the infinite counterexample family
  `<5k+2,6k+3,...,7k+3>`: REST is positive for every `k>=6`, and
  CHAIN fails for every `k>=17`.
- Section 7 proves a fixed-low-generator perturbation. It also refutes the
  repair `M>=4n_1`, still with `3e<m` and Apéry height exactly three.

All these semigroups satisfy Wilf; their Wilf numbers are computed explicitly.
No counterexample to Wilf or to MaxCL is asserted.

## 1. Exact target and the embedding-dimension-two exception

Write `Ap = Ap(S,m)`, `M = max Ap`, `c = M-m+1`, and let
`n_1 < ... < n_d` be the minimal generators other than `m`. Thus `e=d+1`.
For `w` in `Ap`, set

    lambda(w) = floor((M-w)/m),  s_w = (M-w) mod m,
    top_a(w) = w + k_(w,a) n_a,
    con(w) = sum_a [s_w - (M-top_a(w))],
    REST = sum_(w != 0) con(w),  Delta = REST + con(0),
    C2 = m(m-1)/2.

The target as written in the task is

    M >= 3 n_1  ==>  REST <= 0.                         (REST-M3)

**COUNTEREXAMPLE (literal statement).** Take `S=<4,5>`. Its Apéry set,
in increasing value and also in residue order, is `[0,5,10,15]`.
Here `M=15=3 n_1`, and every `5`-chain ends at `15`. Thus

| w | lambda(w) | s_w | top_5(w) | con(w) |
|---|---|---|---|---|
| 0 | 3 | 3 | 15 | 3 |
| 5 | 2 | 2 | 15 | 2 |
| 10 | 1 | 1 | 15 | 1 |
| 15 | 0 | 0 | 15 | 0 |

Consequently `REST=3>0`. Independently, `ell'=3` and `N_5=3`, whence
`REST=5*3-4*3=3`. Also `con(0)=3`, `Delta=6=C2`. This is a
counterexample to REST-M3, not to CHAIN or Wilf.

The lead's supplied `src/scratch/p19/m3_tree2.c` restricts its statistics to
`e>=3` in `visit`; hence this example is outside its reported tested domain.
We retain the written counterexample and continue the intended question
with the explicit additional hypothesis `e>=3`.

**PROVED (infinite counterexample family).** Let `S=<m,n>`, where
`m>=4`, `n>m` and `gcd(m,n)=1`. Then `Ap={j n:0<=j<m}` and
`M=(m-1)n>=3n`. All chains in the unique non-multiplicity direction
end at `M`, so `con(j n)=(M-j n) mod m`. Multiplication by `n`
permutes the residues modulo `m`; it follows that

    Delta=C2,
    con(0)=((m-1)n) mod m,
    REST=C2-(((m-1)n) mod m)>0.

The final strict inequality follows from `C2>m-1` for `m>=4`.
In particular for `n=m+1`, `REST=(m-1)(m-2)/2`.
The example `<4,5>` has the smallest possible multiplicity in this family;
for `m<=3` no two-generator semigroup satisfies `M>=3n`.

**FINITE CHECK.** `check.py 4 5` computes Apéry by Dijkstra, then computes
REST both from explicit chain tops and from an independent enumeration of
endpoint pairs `w<z` with `(z-w) mod n_a=0`. The two values are both `3`.
The full exact output is retained in `results/e2_counter.json`.

## 2. Count identity and the revised frontier

**PROVED (count identity).** If `w<w'` are in `Ap` and
`w'-w=j n_a`, every intermediate `w+i n_a` is in `Ap`: otherwise
`w+i n_a-m` in `S` would imply `w'-m` in `S`. Thus the endpoint-pair
count defining `N_a` equals `sum_(w!=0) k_(w,a)`. Directly,

    con_a(w)=k_(w,a)n_a-m lambda(w),
    REST=sum_a n_a N_a-md ell',
    ell'=sum_(w!=0) lambda(w).

For the last equality, the nonzero-residue elements below the conductor
in residue `w mod m` are `w,w+m,...<c`; their count is
`max(0,ceil((c-w)/m))=floor((M-w)/m)`, since `c=M-m+1`.

**COUNTEREXAMPLE (intended target).** REST-M3 with `e>=3` is refuted in
Section 5. The weaker sufficient target `Delta<=C2` on `M>=3n_1`
is refuted in Section 6. For `e=2` that weaker target is an equality.

The first discriminating searches are interval cores with an added small
generator, near-conductor truncations, and Kunz annealing whose accepted
states all satisfy `M>=3n_1` and `e>=3`. These test whether forcing a
length-three numerical range necessarily pays the positive REST mass of
the known short-range examples. A zero-failure search will be recorded
only as finite evidence, not as proof.

## 3. An explicit interval family: exact Apéry set

**PROVED.** For every integer `k>=1`, put

    m=5k+2,
    n_i=6k+3+i,  0<=i<=k,
    S_k=<m,n_0,...,n_k>.

In Sections 3–6 the direction index starts at zero; the task's least
generator `n_1` is the `n_0` in this displayed parametrization.

Every displayed generator other than `m` belongs to `(m,2m)`, so all are
primitive, and `e=k+2`, `d=k+1`. Consecutive generators give gcd one.
Its Apéry set is the following disjoint union of integer intervals:

    Ap_k = {0}
           union [6k+3,7k+3]
           union [12k+6,14k+6]
           union [19k+9,20k+7]
           union [20k+9,21k+8].                         (AP)

An interval with lower endpoint above its upper endpoint is empty; this
convention applies to the fourth interval when `k=1`.
Consequently

    M=21k+8=4m+k,       c=16k+7,
    q=4,               M-3n_0=3k-1>0,
    ell'=4k+3,         ell=4k+7,
    genus=12k,         W=4k^2-k+7>0.                   (INV)

The Apéry set has least-factorization height exactly three. Also
`3e<m` whenever `k>=3`.

**Proof of (AP).** The offsets of the primitive generators modulo `m`
form `[k+1,2k+1]`. Their two-fold integer sums form
`[2k+2,4k+2]`, with no wrap. Their three-fold sums form
`[3k+3,6k+3]`. On reducing the latter interval modulo `m`, its residues
not already represented by zero, a unit or a pair are exactly

    [4k+3,5k+1]  and  [1,k].

The least three-generator values at these residues are respectively
`3m+r` and `4m+r`, giving the last two intervals in (AP). For residues
already represented by a unit or a pair, the three-generator value is
larger. Thus the displayed values represent every residue exactly once:
the positive residue intervals are

    [1,k], [k+1,2k+1], [2k+2,4k+2], [4k+3,5k+1].

They are the smallest values obtained using at most three non-multiplicity
generators. Four such generators have sum at least `24k+12>M`, so
no other sum can improve a displayed representative. Adding copies of
`m` cannot improve a representative either. This proves (AP).

Every element in the last two nonempty intervals requires three
non-multiplicity generators: its value exceeds twice the largest
generator `7k+3`. Hence the least-factorization height is three.

The co-level of a unit is two, that of a pair is one, and that of
a cubic is zero. The origin has co-level four. This gives
`ell'=2(k+1)+(2k+1)=4k+3` and all remaining formulas in (INV).
Finally `3e<m` is `3k+6<5k+2`, equivalent to `k>2`. QED.

## 4. Exact chain counts for the interval family

Write `[P]` for the indicator of a predicate. Define

    H_i=[floor(k/2)<=i<k],
    L_i=max(k-2i,0),
    N_i=3k+2+i-L_i-H_i-2[i=k],  0<=i<=k.             (N)

**PROVED.** `N_i` is the number of positive-endpoint chain pairs in the
direction `n_i`: it is exactly the `N_a` in the task, with starting
point different from zero.

**Proof.** No positive starting point can take three steps in this
direction, since four primitive generators exceed `M`. The only
possibilities are unit to pair, unit to cubic in two steps, and pair
to cubic in one step.

Every unit plus `n_i` is a pair in (AP), giving `k+1` pairs.
Write the starting unit as `6k+3+j`, `0<=j<=k`.
After two steps its value is `18k+9+2i+j`. It is a cubic in (AP)
exactly when

    2i+j in [k,2k-2] union [2k,3k-1].

Of the `k+1` choices of `j`, the losses are `L_i` values below `k`,
one value with `2i+j=2k-1` precisely when `H_i=1`, and the terminal
value `3k` precisely when `i=k`. This gives
`k+1-L_i-H_i-[i=k]` two-step pairs.

Next write a starting pair as `12k+6+j`, `0<=j<=2k`. Its successor
is `18k+9+i+j`. The same two target intervals require deleting
`k-i` low values, the single hole `2k-1`, and the terminal value
`3k` when `i=k`. The count is `k+i-[i=k]`. Summing the three
counts gives (N). No other pair type is possible by the value ranges.
QED.

This proof counts endpoint pairs; the intermediate-point lemma in
Section 2 makes it identical to the literal-chain definition.

## 5. REST is positive: closed formulas and the first witness

**PROVED.** For the family `S_k`,

    REST_k = (31k^3-87k^2-382k-144)/24,  if k is even;
    REST_k = (31k^3-87k^2-499k-189)/24,  if k is odd.   (REST-POLY)

In particular `REST_k>0` for every `k>=6`.

**Symbolic verification.** Set `u=ceil(k/2)`. The base sum, before
the three correction terms in (N), satisfies

    sum_(i=0)^k (6k+3+i)(3k+2+i)
       -(5k+2)(k+1)(4k+3) = k(k+1)(17k+4)/6.

The weighted low loss and hole loss are respectively

    L=(6k+3)ku -(11k+6)u(u-1)/2 -u(u-1)(2u-1)/3,
    H=u(6k+3)+u(2k-u-1)/2.

The terminal loss is `2(7k+3)`. Therefore

    REST_k=k(k+1)(17k+4)/6-L-H-2(7k+3).

Substitution of `u=k/2` or `u=(k+1)/2` gives (REST-POLY).
For the sign, the odd polynomial is smaller than the even polynomial
by `(39k+15)/8`. Write `k=6+x`. Then the numerator of the odd
polynomial becomes

    31x^3+471x^2+1805x+381,

which is positive for every `x>=0`. For `k=1,...,5`, the exact REST
values are `-31,-42,-68,-45,-41`; thus `k=6` is the first positive
member of this family. This is a family statement, not a claim that
it is the globally smallest counterexample.

**COUNTEREXAMPLE (e>=3, sparse, q=4).** At `k=6`,

    S=<32,39,40,41,42,43,44,45>,
    Ap={0} union [39,45] union [78,90]
             union [123,127] union [129,134],
    M=134, n_1=39, ell'=27,
    (N_39,...,N_45)=(14,17,20,22,23,24,24).

Thus

    sum_a n_a N_a=6095,
    md ell'=32*7*27=6048,
    REST=47>0.

The independent explicit-chain computation gives the same value. It
also gives `con(0)=-138`, `Delta=-91`, `C2=496`, `c=103`,
`ell=31`, `W=145`. Here `M>=3n_1` and `3e=24<m=32`.
The full generator list, Apéry set in residue order, every chain top
and every `con(w)` are retained in `results/counter32.json`.

## 6. The weaker target and CHAIN also fail

**PROVED.** Set `v=ceil(k/3)`. In the interval family,

    con(0)=-(k+1)(7k+2)
            +(k-v)(13k+5+v)/2
            -[k=2 mod 3](20k+8)/3.                  (ORIGIN)

**Proof.** Every origin chain contains `n_i` and `2n_i`, and
`4n_i>M`. It contains `3n_i` exactly when

    ceil(k/3)<=i<=k-1,  and  3i != 2k-1.

The two-step baseline for `con(0)` is

    2 sum_i n_i - 4m(k+1)=-(k+1)(7k+2).

The extra third steps contribute the sum of `6k+3+i` over
`v<=i<=k-1`, which is `(k-v)(13k+5+v)/2`, except for the
missing value `i=(2k-1)/3` when `k=2 mod 3`. That value of
`n_i` is `(20k+8)/3`. This proves (ORIGIN). QED.

**PROVED.** `Delta_k>C2_k` for every `k>=17`.

Here is a complete polynomial certificate. In each row write
`k=k0+6j`, `j>=0`. Substitution of (REST-POLY), (ORIGIN), and
`C2=(5k+2)(5k+1)/2` gives the listed coefficients of
`Delta-C2`, in increasing powers of `j`:

| k0 | constant | j | j^2 | j^3 |
|---|---:|---:|---:|---:|
| 17 | 178 | 2642 | 1699 | 279 |
| 18 | 918 | 6627/2 | 3677/2 | 279 |
| 19 | 1346 | 3895 | 1978 | 279 |
| 20 | 2058 | 9159/2 | 4235/2 | 279 |
| 21 | 2965 | 5332 | 2257 | 279 |
| 22 | 3932 | 12223/2 | 4793/2 | 279 |

Every coefficient is positive, and these six progressions exhaust
`k>=17`. The identities follow by substitution into explicit formulas;
they are not inferred from finite sampling. `family.py` independently
reconstructs the coefficients using rational arithmetic and checks each
identity for `0<=j<=1000` as a computational guard.

**COUNTEREXAMPLE (smallest CHAIN failure in this family).** At `k=17`,

    S=<87,105,106,...,122>,
    Ap={0} union [105,122] union [210,244]
             union [332,347] union [349,365],
    M=365>=3*105,  c=279,  ell'=71,  ell=75,
    REST=4937, con(0)=-1018, Delta=3919>C2=3741.

The counts in directions `105,...,122` are

    (36,39,42,45,48,51,54,57,59,61,62,63,64,65,66,67,68,68).

Here `3e=57<m=87`. The chain budget is

    B_chain=18*3741-3919=63419,
    need=17*3741=63597,

so CHAIN misses by `178`, while `W=19*75-279=1146>0`.
The values `k=1,...,16` have no CHAIN failure, as follows by direct
substitution into (REST-POLY) and (ORIGIN), and was checked independently
from the generators. Full data are in `results/chain_counter.json`.

The initially reported larger witness `<102,123,...,143>` is retained in
`results/chain_counter20.json`: `REST=8559`, `con(0)=-1350`,
`Delta=7209>C2=5151`, and `W=1587`.

**Asymptotic size of the failure.** The exact formulas imply

    REST=(31/24)k^3+O(k^2),
    con(0)=-(23/9)k^2+O(k),
    B_chain/need -> 269/300 < 1.

Thus this is a leading-order failure of CHAIN, not just a bounded
exception at a small phase. Moreover `M/n_0 -> 7/2` from below,
so no replacement of `3` by a fixed constant smaller than `7/2`
repairs either conjecture, even with `q=4`, height three and `3e<m`.

## 7. Fixed low generators: failure also when M>=4n_1

The origin of the counterexamples is not restricted to the absence of
small primitive generators. The following gives explicit infinite
families with any prescribed positive number of low units.

**PROVED (LOW-PERTURB).** Let `r>=1` and `k>3r` be integers, and put

    S_(k,r)=<5k+2, 5k+3,...,5k+2+r, 6k+3,...,7k+3>.

Every displayed non-multiplicity generator lies in `(m,2m)`; thus
`e=k+r+2`, `d=k+r+1`. Starting with (AP), its Apéry set is obtained
by removing `4m+j`, `1<=j<=3r`, and inserting

    m+j       for 1<=j<=r,
    2m+j      for r<j<=2r,
    3m+j      for 2r<j<=3r.                          (LOW-AP)

In particular

    M=21k+8, c=16k+7, n_1=m+1,
    ell'=4k+3+6r, ell=4k+7+6r,
    W=4k^2+(10r-1)k+6r^2+19r+7>0.                 (LOW-INV)

The least-factorization height is exactly three. In the primary-regime
notation of the task, `a=alpha=r`.

**Proof of (LOW-AP).** Call the new generators `m+j`, `1<=j<=r`,
low, and the old generators `6k+3+i`, `0<=i<=k`, core. At most four
non-multiplicity generators can occur below `M`, since
`5(m+1)>M`. The only improvements coming from pure low sums are those
in (LOW-AP): offsets `1,...,r` occur in degree one, `r+1,...,2r`
first occur in degree two, and `2r+1,...,3r` first occur in degree
three. Four-low sums either coincide with an old representative `4m+j`
or exceed `M`.

For mixed sums of degree at most three, compare offsets:

- one low plus one core has offset in `[k+2,2k+1+r]`; the old
  representative at that residue has degree at most two;
- two lows plus one core has offset in `[k+3,2k+1+2r]`, which
  lies below `4k+3`, so the old representative has degree at most two;
- one low plus two cores has offset in `[2k+3,4k+2+r]`, below
  `m`; the old representative has degree at most three.

None improves an old representative. A mixed degree-four sum whose
offset does not wrap has offset greater than `k`, where an old
representative has degree at most three. If its offset wraps, its value
is at least `5m>M`. Thus it cannot improve a representative either.
The old core-only sums are already accounted for in (AP). This proves
the exact replacement rule. Its changes of co-level are respectively
three, two and one on `r` residues each, giving (LOW-INV).

All representatives still have factorizations of length at most three;
the unchanged high cubics exceed twice the largest generator, so the
height is exactly three. Finally `c-2m=6k+3`, so exactly the `r`
low generators lie in `(m,c-2m)`. Also
`(c-m)/2=(11k+5)/2`, and `k>3r` puts exactly these same `r`
generators below that bound. Thus `a=alpha=r`. QED.

**PROVED (uniform failures with low generators).** For every `r>=1`
and every `k>=100(r+1)`,

    REST(S_(k,r))>0,     Delta(S_(k,r))>C2,
    M>=4n_1,            3e<m.                         (LOW-FAIL)

Here is an explicit quantitative proof. Every old core direction has
`M<4n_i`; therefore an Apéry chain in that direction has at most four
elements, and any one element participates in at most three endpoint
pairs. Removing `3r` cells from (AP) deletes at most `9r` nonzero-start
pairs per old direction. Adding the new cells cannot delete pairs
between retained cells. Consequently

    N_i(new)>=N_i(old)-9r.

The new directions contribute at least `-m ell'(new)` each to REST,
because their pair counts are nonnegative. Using (LOW-INV),

    REST(new)>=REST_k-r L(k,r),

    L(k,r)=9 sum_i n_i+6m(k+1)+m(4k+3+6r)
          =(217/2)k^2+(301/2+30r)k+45+12r.           (ROBUST)

Two elementary bounds make this uniform. First, (REST-POLY) gives
`REST_k>=(5/4)k^3` for `k>=100`. For the smaller, odd polynomial,
24 times the difference from `(5/4)k^3`, on writing `k=100+x`, is

    x^3+213x^2+12101x+79911>0.

Second, if `k>=100(r+1)`, then `k>=200` and `r<=k/100`, whence

    L(k,r)<=(544/5)k^2+(7531/50)k+45 <=110k^2.

For the last inequality, 50 times the difference equals at least
`60k^2-7531k-2250`; putting `k=200+x` gives
`60x^2+16469x+891550>0`. Hence

    REST(new)>=k^2(5k/4-110r)>=(15r+125)k^2.         (PAY)

Also `lambda(0)=4`, so `con(0)>=-4md`. The simple bounds
`m<=6k` and `d<=2k` give `4md+C2<=66k^2`. Therefore

    Delta-C2 >= REST(new)-4md-C2
             >= (15r+59)k^2 > 0.

Finally `M-4n_1=k-4>=0`, and `3e<m` follows from
`2k>3r+4`. This completes the proof of (LOW-FAIL). QED.

**Consequences.** Since `M/n_1 -> 21/5` as `k` tends to infinity
with `r` fixed, the same construction refutes any fixed threshold
smaller than `21/5`, including `M>=4n_1`. It does not settle thresholds
at or above `21/5`.

For `r>=19`, these examples also meet the coarse numerical filters
`alpha>=6`, `a>=19`, `a<10*C(alpha+1,2)`, `3e<m`, `m>=211`
from P11. They have `a=alpha` and hence do not have the negative A-face
required in the sharper GW-26 remaining family. Thus they refute CHAIN
as a universal sufficient payment on those coarse filters; they do not
provide a difficult unproved Wilf instance.

**FINITE CHECK (two exact REST methods).** `perturb.py` compares the
predicted Apéry set with Dijkstra and compares literal chain sums with
residue-class endpoint counts for eight cases. Some larger outputs are:

| k | r | m | e | M | n_1 | REST | con(0) | Delta | C2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 80 | 1 | 402 | 83 | 1688 | 403 | 122192 | -18183 | 104009 | 80601 |
| 100 | 1 | 502 | 103 | 2108 | 503 | 451242 | -27381 | 423861 | 125751 |
| 200 | 1 | 1002 | 203 | 4208 | 1003 | 6987492 | -106783 | 6880709 | 501501 |
| 1000 | 6 | 5002 | 1008 | 21008 | 5003 | 810853784 | -2662114 | 808191670 | 12507501 |
| 2000 | 19 | 10002 | 2021 | 42008 | 10003 | 4287173439 | -10857562 | 4276315877 | 50015001 |

The first two cases are below the sufficient threshold in (LOW-FAIL),
and are individual exact counterexamples rather than consequences of
that threshold. The `k=100,r=1` case has `M>4n_1=2012`; full data
are in `results/counter_M4.json`.

## 8. The proposed implication is correct; its premise is false

This section checks the logical route requested in the task. It is not
a new Wilf theorem.

**PROVED (identities and sufficient criterion).** Since the values
`s_w=(M-w) mod m` are a permutation of the residues,

    B_chain=sum_(w,a)(M-top_a(w))=d*C2-Delta.

Let `P_a` count all endpoint pairs, including those starting at zero.
Writing `ell=sum_w lambda(w)` gives

    Delta=sum_a n_a P_a-dm ell.

For a factorization down-set, the sum of all column-top values is
`(d+1)sum_Ap w`: in one direction, subtracting the column values from
its length times its top gives that generator times the sum of the
column coordinates, and summing over directions gives `sum_Ap w`.
The full Apéry-chain top is at least the factorization-column top.
Therefore, with

    B=dmM-(d+1)sum_Ap w,
    need=(d-1)C2,

we have `B>=B_chain`.

This last comparison also has a tile-free proof. For each `w` choose
any factorization `w=sum_a x_a n_a`, with no copies of `m`.
If `h_a(w)` is the number of backwards steps in its full Apéry chain,
then `h_a(w)>=x_a`: every `w-j n_a`, `j<=x_a`, belongs to Apéry.
Thus `sum_a n_a h_a(w)>=w`. Summing and counting the chain pairs
from their larger endpoint gives `sum_a n_a P_a>=sum_Ap w`, exactly
`B>=B_chain`.

Finally,

    ell=(mM-sum_Ap w-C2)/m,
    mW=B-need.

This proves `Delta<=C2 ==> W>=0`.

If REST-M3 for `e>=3` were true, on `M>=3n_1` we would have

    Delta<=con(0)<=d*s_0<=d(m-1)<=C2,  if d<=m/2.

The first origin inequality uses only `M-top_a(0)>=0`; it does not
assume distinct origin tops. If `d>m/2`, then `2e=2d+2>m+2`,
which meets Sammartano's exact hypothesis `2e>=m`. The cited result
is Theorem 18 of [Numerical semigroups with large embedding dimension
satisfy Wilf's conjecture](https://arxiv.org/pdf/1111.1863), checked in
the original paper, page 9. No depth or extra gcd condition is needed
beyond being a numerical semigroup.

For `M<3n_1`, a factorization of an Apéry element cannot use `m`,
and three other generators have sum at least `3n_1>M`. Thus every
Apéry element has a factorization of length at most two, exactly the
hypothesis of the project theorem `wilf_of_apery_height_le_two` in
`lean/Wilf/MaxCL.lean`. For `e=2`, Wilf is an equality directly from
the Apéry set in Section 1: `ell=(m-1)(n-1)/2=c/2`.

Thus the implication proposed in the task has no sign or hypothesis
problem after treating `e=2` separately. Its proposed premise is what
the counterexamples refute.

**Where the chain argument loses the Wilf margin.** Define the
nonnegative column-to-chain loss

    L_chain=B-B_chain=sum_a n_a P_a-sum_Ap w.

Then exactly

    mW=C2-Delta+L_chain.

On `S_k`, `L_chain=(511/24)k^3+O(k^2)`, so it is essential.
This is an interpretation of the counterexample, not a new bound:
long Apéry chains follow several different factorizations, while a
factorization tile must choose one. The counts defining REST keep
all such chain pairs. Discarding `L_chain` is already invalid on
the explicit height-three families above.

## 9. Computational record and reproducibility

All mathematical executions were on fejer in `~/wilf/p12/rest/`,
using `nice -n 10`, at most three of our single-core jobs at once.
The software was Python 3.12.3 and GCC 13.3.0 on Ubuntu.
No pre-existing process was stopped or altered. One of our own early
formula-check processes was stopped and restarted after replacing a
linear list-membership test by a set-membership test. The final code
and final completed outputs are retained. No computation was run on
the laptop and no commit was made.

### Exact certificates and independent counterexample verification

- `check.py` computes Apéry by Dijkstra, literal full-chain tops,
  every `con(w)`, and independently enumerates all endpoint pairs.
  `counter32.json`, `chain_counter.json` and `chain_counter20.json`
  give complete data for the three principal `e>=3` witnesses.
- `independent.py` uses a forward semigroup-membership sieve, not
  Dijkstra. It reconstructs Apéry and the left elements from membership,
  then recomputes REST using literal progressions. It agrees in every
  field tested on `<4,5>`, `<32,39,...,45>`, `<87,105,...,122>`,
  and `<102,123,...,143>`. Full output is `independent_sieve.json`.
- `family.py 40` compares (AP), (N), REST, the origin contribution
  and Delta with the generator-based calculation for every `1<=k<=40`.
  It finds the first positive REST at `k=6` and first CHAIN failure
  at `k=17`. These are 40 individual exact semigroups.
- `certificate.py` implements arithmetic in the polynomial ring
  over the rational numbers using `fractions.Fraction`. It verifies
  (REST-POLY) from the three explicit loss sums for both parities,
  all six CHAIN polynomial identities, and the three sign certificates
  in Sections 5 and 7. It uses neither interpolation nor floating point.
  Its complete output is `certificate.json`.
- As an independent guard, `family.py` also reconstructs each six-row
  coefficient vector from four rational evaluations and compares it
  with the closed formula for `0<=j<=1000`. Its initial parity
  polynomial guard checks every `2<=k<=2000`; `k=1` is also checked
  directly from the semigroup. These are formula checks,
  not additional semigroup enumerations; they are not the justification
  for the universal polynomial identities.
- `sparse_check.py` independently obtains `N_a` from the sizes of
  the residue classes of Apéry modulo `n_a`: if these sizes are `h_r`,
  then `N_a=sum_r C(h_r,2)-(h_0-1)`. It compares this count with
  literal full-chain traversal and the direct sum of `con(w)`.
  This costs only linear storage in `m`, avoiding a stored matrix
  of every chain top.
- `perturb.py` checks the exact modified Apéry sets and both REST
  calculations for `(k,r)=(4,1),(10,1),(40,1),(80,1),(100,1),`
  `(200,1),(1000,6),(2000,19)`. The last three also check every
  numerical inequality in the sufficient bound (LOW-FAIL). All pass.

### Discovery searches; their scopes are finite

- `structured.c` uses the independent C implementation `rest.h`:
  Dijkstra for Apéry, primitive extraction from increasing values,
  and memoized whole-chain lengths. Mode 0 explores interval cores
  `{L*m+a,...,L*m+a+w}` plus a small generator `m+z`:
  `L=1,...,4`; `1<=a<m`; `1<=w<m-a`, keeping `w<=8` or
  `w=0 mod 3`; `1<=z<=floor(m/3)`, keeping `z<=8` or
  `z=0 mod 5`. The run requested `19<=m<=80` but stopped at its
  first positive REST, the witness at `m=32`. It completed all its
  specified inputs through `m=31` (82,856 input evaluations, 78,352
  in the class, 47,644 also satisfying `3e<m`). The tail of
  `interval.log` records the exact stopping witness. No claim is made
  about the unexecuted part `m>32`.
- Mode 1 evaluated every pair `m+1<=a<=4m`, `a<b<=6m`,
  for `7<=m<=70`, retaining actual embedding dimension three and
  `M>=3n_1`. There were 1,221,696 input pairs, 956,339 retained
  class evaluations, and 955,206 also with `3e<m`, with repetitions
  of the same semigroup possible. No positive REST was found. The
  largest ratio was `-3/7`, at `<8,9,11>`. This is not a proof
  for all three-generated semigroups. The output is `e3_box.log`.
- `anneal.c 61 24 200000 120061` made 4,800,000 single-coordinate
  Kunz proposals. It found 1,213,133 valid Kunz candidates and
  1,208,112 satisfying the hard constraints `e>=3`, `M>=3n_1`;
  6,127 mutations were accepted. Its best logged accepted state had
  `REST=-20406`. Initial seeds are initialization, not part of its
  accepted-state record. This lane was ineffective compared with the
  structured interval search and is not used for any theorem.
  The output is `anneal61.log`.
- Modes for additional random and near-truncation families were written
  in `structured.c` but were not launched after the counterexample.
  No genus-tree extension or Sidon census was run. A counterexample
  made those broader zero-failure searches unnecessary for this task.

The essential reproduction commands, after copying this directory to
`~/wilf/p12/rest/`, are:

```sh
nice -n 10 gcc -O3 -std=c11 structured.c -o structured
nice -n 10 gcc -O3 -std=c11 anneal.c -lm -o anneal
nice -n 10 ./structured 19 80 0
nice -n 10 ~/mathenv/bin/python check.py 32 39 40 41 42 43 44 45
nice -n 10 ~/mathenv/bin/python family.py 40
nice -n 10 ~/mathenv/bin/python certificate.py
nice -n 10 ~/mathenv/bin/python independent.py
nice -n 10 ~/mathenv/bin/python perturb.py
```

The structured search returns exit status 2 when it finds a counterexample;
that is a successful falsification, not an arithmetic or program failure.

## 10. Preserved failures

1. **REST-M3 as written:** smallest member of the two-generator family
   is `<4,5>`, REST `3` (Section 1).
2. **REST-M3 repaired by `e>=3`:** `<32,39,...,45>`, REST `47`.
   This is the smallest positive member of (AP), and the first found
   in our discovery run; global minimality is not claimed.
3. **REST-M3 with `3e<m`:** the same example has `24<32`.
4. **The weaker `Delta<=C2` / CHAIN under `M>=3n_1`:**
   `<87,105,...,122>`, `Delta-C2=178`, with `3e<m` and height three.
   This is the first failure in (AP), not a global minimality claim.
5. **A larger threshold `M>=4n_1` repairs the statement:** false.
   For example `<402,403,483,...,563>` (`k=80,r=1`) has
   `M=1688>=4*403`, REST `122192`, and `Delta-C2=23408`.
   This is the smallest checked perturbed CHAIN failure in our listed
   sample, not a proved first member. The full-data witness retained
   is the `k=100` example in Section 7.
6. **Failed scratch lower bound:** the even-parity formula initially
   suggested the uniform bound
   `REST_k >= (31/24)k^3-(29/8)k^2-16k-7`.
   It is false for odd `k`: already `k=1` gives `-31<-76/3`;
   on the positive branch, `k=7` gives `112<1757/12`.
   It is not used anywhere. The correct odd polynomial and the
   sign certificates are given explicitly in Sections 5 and 7.

No inequality in GW-24/GW-26 or a prior proved MaxCL theorem is
contradicted. The failure is in the proposed sufficient chain/REST
criteria. In particular, the counterexamples have explicit positive
Wilf numbers and do not contest the P11 theorems currently under the
lead's independent review.

## 11. Strategic review and exact remaining gap

**PROVED / COUNTEREXAMPLE.** P12 has a negative resolution: REST-M3,
the proposed weaker total-deficit bound, and the repair with threshold
four are false. The infinite family proof is complete; its sign
certificates are exact. The perturbation permits any fixed positive
number of low generators and retains `3e<m` and height three.

**Strategic decision.** Discontinue global REST/CHAIN searches under
the sole range hypothesis `M>=3n_1`. The counterexamples have a cubic
deficit, so enlarging a genus census or improving the isolated origin
bound cannot repair this route. The column-to-chain overlap loss must
be paid, or additional shape hypotheses must exclude the interval
families. The alternative target `con(0)<=C2` with tied tops is not
refuted here, but cannot by itself restore either failed total bound.

**OPEN.** Wilf for all numerical semigroups remains unresolved. This
report proves no new all-semigroup Wilf reduction. The existing primary
negative-A-face frontier is not settled or enlarged by these examples:
in the base family `a=alpha=0`, and in the perturbed family `a=alpha=r`,
where the earlier A-face argument already gives nonnegative payment.

The next precise discriminating target for a resumed depth-four chain
route is CHAIN restricted to the full negative-A-face frontier, including
`W_A<0`, rather than merely the coarse numerical filters
`alpha>=6`, `a>=19`, `a<10*C(alpha+1,2)`, `3e<m`.
That restricted statement is OPEN and is not asserted by this report.
