# P6d: one cubic is paid; weighted cyclic packing and higher windows

2026-10-19. **Proved:** HC'>=0, hence MaxCL, at every phase for every
height-three tile with exactly one cubic. The proof is analytic in every
dimension. It does not need a new or previously accepted finite small-core
certificate.

Also proved: HC' at the origin when all core units lie in
`(m/2,2m/3)`, without a complete-face hypothesis; an additional shape
criterion when there is at most one bad cubic; a weighted cyclic packing
reduction; and an exact window identity at every height. The general
height-three theorem with several bad cubics remains open.

P6_REPORT.md, P6B_REPORT.md and P6C_REPORT.md are unchanged. No commits.
All computation ran on fejer in `~/wilf/p6d`, with nice 10, one thread per
job, and at most four owned jobs. Python was 3.12.3; the Python scripts
use its standard library. Code is in `d/` beside this report.

## 1. Notation and accepted input

Delete the maximal-unit spikes. The core has k non-maximal units, q
pairs Q, p non-maximal pairs N2, and t cubics T. Write

```
Qk=binom(k+1,2), e=Qk-q, s=m-(1+k+q+t), d=k+s,
delta_i=k+1-sum_{z in Q} z_i,
A=sum_i delta_i rho_i.
```

Thus e counts missing quadratic monomials, a missing loop contributes
twice to its vertex degree, and A is exactly the sum of the ordinary
unit-residue sums of all missing pairs. All rho_i are in `[0,m)`.
At phase sigma, `rho=r(0)`, `nu=m-rho`, and `W=[nu,m)`.

Use the accepted quantities

```
Lplus=A+s sum_i rho_i+sum_{z in N2}(d+2-psi(z))r(z),
PAplus=#{z in A2:K(z)=1},
HCprime=Lplus+m(OW+B),     S=HCprime+m PAplus.
```

The accepted WINDOW-ID says, with beta the number of bad cubics,

```
S=Lplus+m(C-beta),
C=Orest+Pplus+gain+PAplus >=0.                         (1)
```

Every summand in C is an integer. Here Pplus refers to N2 pairs.
For t=1 the accepted ONE-DEFICIT classification says that `OW+B<0`
forces

```
OW+B=-1;  K(y)=-1;  r(y) in W;
all N2 pairs have K=0 and residue >=2;
OW=1;  8<=rho<m/2;
unit residues 0 and 1 occur, outside supp(y).
```

In particular the origin, all units and all N2 pairs lie outside W.
In W the cubic is the sole cell other than maximal pairs of carry -1.

The accepted small-core MaxCL theorems are available, but the proof below
does not need them to cover its small cases. Their HC' counterparts are
proved here explicitly for the one-cubic shapes.

## 2. Cyclic difference census with missing pairs

Let V be n distinct elements of `Z/m`, represented by distinct integers
in `[0,m)`. A formal pair is an unordered multiset of two elements of V;
loops are included. Declare some formal pairs present and the others
missing, and assume present formal pairs have distinct sums modulo m.
For a cyclic sum fibre F write

```
g_F=|F|, j_F=#missing pairs in F, ell_F=#loops in F.
```

Then `g_F-j_F<=1`, and `ell_F<=2`. Let E_D be the number of unordered
collisions among the `n(n-1)` ordered off-diagonal differences from V.

**Lemma DIFF-CENSUS (proved, cyclic).**

```
E_D <= sum_F [4 binom(g_F,2)-2 ell_F(g_F-1)+binom(ell_F,2)].   (2)
m-1 >= n(n-1)-E_D.                                           (3)
```

Proof. A collision `a-b=c-d` between different off-diagonal formal
differences gives two different formal pairs `{a,d}` and `{c,b}` with
the same cyclic sum. Distinct pairs in a sum fibre have disjoint
supports: sharing an element would force equality of the other element.
For two ordinary pairs there are at most four corresponding unordered
collisions of ordered differences. For a loop and an ordinary pair
there are at most two; for two loops there is at most one. Thus the
bound is

```
4 binom(g-ell,2)+2 ell(g-ell)+binom(ell,2),
```

which is the expression in (2). Nonzero difference residues number at
most m-1. In a difference fibre of size h, at most `binom(h,2)` mergers
are needed to identify all h labels, since `h-1<=binom(h,2)`. This gives
(3). No assertion about three points pairwise at cyclic distance d is
used. In particular the argument is valid at composite m, including
2- and 3-torsion. QED.

If e formal pairs are missing, convexity and `g_F<=j_F+1` immediately
give the useful coarse consequence

```
m >= n(n-1)+1-2e(e+1).                         (COARSE-PACK)
```

Indeed `sum_F binom(j_F+1,2)<=binom(e+1,2)`, and dropping the loop
corrections in (2) only increases its right side.

There is also a localized version used in the diagnostic scripts.
Let v be the number of vertices touched by missing pairs. If m is
odd put `u=ceil(v/2)`; if m is even put `u=floor(v/2)+1`. Write
`e=fu+r`, `0<=r<u`. Then

```
m >= n(n-1)+1-4[f binom(u+1,2)+binom(r+1,2)].   (LOCAL-PAIR-PACK)
```

The missing pairs in any one cyclic sum fibre have disjoint supports
and at most gcd(2,m) loops, so their number is at most u. Convexity
maximizes `sum binom(j_F+1,2)` by filling fibres to that capacity,
giving the displayed formula. For e=0 use COARSE-PACK directly.
This and DIFF-CENSUS require no height bound.

## 3. Weighted packing for unwrapped defect fibres

For a missing pair `{a,b}` give it its ordinary nonnegative weight
`a+b`, using the fixed integer representatives. Let A be the sum of
these weights. Call the missing-pair fibres **unwrapped** when every
cyclic sum fibre containing a missing pair consists entirely of pairs
having one and the same ordinary integer sum.

**Lemma WEIGHTED-PACK (proved).** If the missing-pair fibres are
unwrapped, then

```
E_D<=A+e,
A>=n(n-1)-m+1-e.                              (WP)
```

If, in addition, `2 notin V`, then the stronger conclusion is

```
E_D<=A,
A>=n(n-1)-m+1.                                (WP2)
```

Proof. Work in a fibre of ordinary sum w containing j missing pairs,
g total pairs, and at most one present pair. Thus `j>=g-1`. The fibre
contributes `jw` to A.

For an unwrapped fibre there is at most one loop. If there is a loop,
g disjoint nonnegative-integer pairs require `w>=2(g-1)`. Its
contribution in (2) is at most `2(g-1)^2<=jw`. If there is no loop,
`w>=2g-1`, and the contribution is at most
`2g(g-1)<=j(w+1)`. Summing proves WP, followed by (3).

For WP2, at every w>=2 the pair `{2,w-2}` is unavailable. Among all
nonnegative-integer unordered pairs of sum w, there are
`floor(w/2)+1` possibilities; deleting this pair shows
`g<=floor(w/2)`, hence `w>=2g`. The contribution in (2) is at most
`2g(g-1)<=jw`. For w=0 or 1 there is at most one pair and no difference
collision. Summing proves WP2. QED.

WP2 is the local relay in the final pure-power case. It uses the hole at
the *integer value* 2 after unwrapping; it is not a claimed cyclic
DIFF2 theorem.

## 4. Why a proposed one-cubic violation unwraps

**Lemma ONE-UNWRAP (proved).** At a ONE-DEFICIT phase, suppose

```
PAplus=0,     A<m.
```

Apply the preceding lemmas to the integer set

```
V={rho,rho_1,...,rho_k},   n=k+1.
```

Declare the padded origin and units and all present pairs to be the
present formal pairs; precisely the e absent quadratic monomials are
missing. Then the missing-pair fibres are unwrapped, and their total
weight is the same A as in section 1.

Proof. These padded formal sums label exactly the origin, units and
present pairs, up to the common translation `2rho` in `Z/m`. Thus their
present labels are distinct. All elements of V are distinct nonnegative
integers. Since each missing-pair weight is at most A<m, two missing
pairs in one cyclic fibre have the same ordinary sum w<m.

A present pair in that fibre could have ordinary sum only w or w+m.
The second possibility is excluded as follows.

* A padded origin sum is `2rho<m`. A padded unit sum is
  `rho+rho_i<m`, because `rho_i<nu`. Neither can be w+m.
* For an actual present quadratic pair with ordinary sum w+m, if
  `w<rho` its carry is 0 and its residue is `nu+w` in W. This contradicts
  ONE-DEFICIT: W contains only the cubic and negative-carry maximal
  pairs. If `w>=rho`, its carry is +1; N2 carries are 0 and PAplus=0.

There is at most one present formal pair in the fibre. All its members
therefore have the same ordinary sum w. QED.

There is a stronger payment that permits positive maximal-pair carries.

**Lemma ONE-WEIGHTED (proved).** At any ONE-DEFICIT phase with A<m,
whether or not PAplus is zero, the conclusions (WP) hold for V in
section 4. If the least N2 pair residue is 2, the conclusions (WP2)
hold as well. The fibres themselves need not all be unwrapped.

Proof. Let r be the least N2 pair residue, and write `r(y)=nu+b`.
The cubic lift gives

```
sum_i y_i r(y-e_i)=2b-rho,
3r<=2b-rho<=rho-2,    hence rho>=3r+2.          (HOLES)
```

Both r and rho are unavailable as endpoints of missing pairs: r is
the residue of a present N2 pair, hence is not in V at all, while rho
belongs to the origin, not to a unit direction. As before all missing
weights in a given cyclic fibre are one ordinary w<m. A wrapped
present pair in that fibre must have sum w+m. The first three
exclusions in ONE-UNWRAP still apply without PAplus=0, so this can
only be an actual maximal pair of carry +1, with w>=rho.

There are j missing ordinary pairs of sum w and this one wrapped
present pair. If `w=rho+r`, the wrapped present pair has residue r
and collides with the N2 pair attaining r. This is impossible.
Otherwise the two nonnegative-integer pairs

```
{rho,w-rho},    {r,w-r}
```

are distinct and unavailable to the missing pairs. They are well
defined since `w>=rho>r`. Out of `floor(w/2)+1` possible ordinary
pairs, at most `floor(w/2)-1` can therefore be missing:

```
j<=floor(w/2)-1,    g=j+1<=floor(w/2).
```

DIFF-CENSUS bounds this entire wrapped fibre's contribution by
`4 binom(g,2)<=jw`, its missing-pair weight. All unwrapped fibres
satisfy WP. If r=2 they instead satisfy WP2, since `2 notin V`.
Adding the already-paid wrapped fibres proves both assertions. QED.

## 5. ONE-RELAY and all one-cubic tiles

**Theorem ONE-RELAY (proved, strong form).** For t=1, at every
ONE-DEFICIT phase,

```
Lplus >= m.                                   (ONE-RELAY)
```

Consequently HC'>=0 and MaxCL hold at every phase of every
height-three tile with exactly one cubic, with no restriction on its
core dimension or number of spikes.

Proof for s>=1. Retain one N2 pair, whose residue is at least 2 and whose
coefficient is at least d-1. Its residue and the k unit residues are
distinct. Since `d-1>=s`, rearrangement with the pair forbidden from
residues 0 and 1 gives

```
Lplus >= A+2(d-1)+s(Qk-2),
Lplus-m >= A+(s-1)Qk+e+k-s-4.                  (4)
```

For k>=5 the right side at s=1 is `A+e+k-5>=0`, and its increment
when s increases by one is `Qk-1>=0`. This proves the stronger claim.

Now let s=0 and k>=6. Suppose for contradiction that `Lplus<m`.
Then A<m, so ONE-WEIGHTED applies. Here

```
m=1+k+q+1=k+Qk+2-e,
A>=binom(k,2)-1                               (5)
```

by its WP conclusion. Let r>=2 be the least residue of an N2 pair. If the cubic is
pure, its pair coefficient is k-1. For multiplicity type 21 the two
pair coefficients are k+1 and k, so their contribution is at least
`(k+1)r+k(r+1)>=(5k+2)`. For a squarefree cubic its three coefficients
are k+1 and its contribution is at least `9(k+1)`. Therefore (5) gives

```
Lplus-m >= e+3k-1                 for type 21,
Lplus-m >= e+7k+6                 for type 111,
Lplus-m >= e-5+(k-1)(r-2)         for type 3.    (6)
```

The first two are positive. The third is nonnegative when r>=3, since
`k>=6` and e>=0. Only a pure cube with r=2 remains.

In this last case the integer 2 is the residue of the present N2 pair.
It is neither a unit residue nor rho, by injectivity. ONE-WEIGHTED's
WP2 conclusion improves (5) to

```
A>=binom(k,2)+e-1,
Lplus-m>=2e-5.                                (7)
```

If e>=3 this is positive. If e<=2, COARSE-PACK applied to the same
padded pair system gives

```
m >= k(k+1)+1-2e(e+1).
```

Its right side minus the exact `m=k+Qk+2-e` is

```
binom(k,2)-1-2e^2-e >= binom(k,2)-11 >0
```

for k>=6 and 0<=e<=2. There is no such injective tile. This proves
ONE-RELAY for k>=6,s=0, and finishes its non-small part.

Here are the remaining small cases, without any finite certificate.
ONE-DEFICIT needs the distinct units at 0 and 1 outside the cubic's
support, so k>=3.

* If k=3, `m<=11+s` and m>=17 imply s>=6. The right side of (4)
  is `A+5s+e-7>=0`.
* If k=4, `m<=16+s` implies s>=1. At s=1 the right side of (4)
  is A+e-1; it suffices unless e=0. That case would have m=17 and
  complete quadratic pairs, contradicting COARSE-PACK's m>=21.
  At s>=2 the right side is `A+9s+e-10>=0`.
* If k=5 and s>=1, (4) already applies. Let k=5,s=0. Then
  `m=22-e`, and COARSE-PACK excludes e=0,1. The mixed and squarefree
  estimates (6) still apply. For a pure cube with r>=3, (6) gives
  at least e-1>=1; with r=2, (7) suffices for e>=3.

The only remaining possibility is k=5,s=0,e=2,m=20, a pure cube
with pair residue 2, and `Lplus<m`. If u is its unit residue, then
`rho=2u-2`, rho>=8 and rho<m/2 force u=5,rho=8. All unit residues
are less than nu=12, so actual pair sums are at most 22, below
`m+rho=28`. There are no positive-carry pairs; ONE-UNWRAP applies.
Here `Lplus=A+8<20`, hence A<=11.

The six-element V has 30 ordered off-diagonal differences. By (3)
their collisions number at least `30-19=11`. If its two missing
pairs belong to different sum fibres, (2) gives at most 4+4=8
collisions, a contradiction. They must belong to one fibre, which
must contain three formal pairs to produce at least 11 collisions.
That fibre is unwrapped. Since `2 notin V`, three ordinary pairs
of its sum w require w>=6, by the counting step of WP2. The two
missing pairs then have total weight `A=2w>=12`, the final
contradiction.

All ONE-DEFICIT phases therefore satisfy Lplus>=m. Every other phase
has `OW+B>=0`, so `HCprime>=Lplus>=0`. This proves all phases and
all dimensions. QED.

**Semigroup consequence.** The accepted Lean-checked implications
MaxCL => Tile-TOP'' => Wilf apply, in particular at sigma=c mod m.
Hence Wilf holds for every numerical semigroup admitting an Apéry tile
of height at most three with at most one cubic cell. The case of no
cubic is the accepted height-two theorem. This does not assert the
full height-three semigroup theorem.

## 6. The origin bad-cubic classification

At rho=0 all pair carries are 0 or 1, and cubic carries are 0, 1 or 2.
A bad cubic is exactly a cubic with carry 1 all of whose three face
incidences have pair carry 1. A carry-0 cubic has no positive pair
face; a carry-2 cubic has kappa>=1. For carry 1,
`kappa=2-#positive face incidences`, proving the classification.

There must be at least two factor copies above m/2. Indeed two at most
m/2 would have a pair sum at most m; equality would make their present
pair collide with the origin. It is false that all three factors must
be above m/2.

Smallest-modulus counterexample to that latter statement:

```
m=8, core unit labels (3,6), Q={x_1 x_2,x_2^2}, T={x_1 x_2^2}.
core residues: 0,3,6,1,4,7; spikes: 2,5.
rho=0, beta=1, Pplus=2, gain=0,
Lplus=48, HCprime=S=56.
```

The factor 3 is below m/2. This is not a failure of HC' or MaxCL.
`algebra.py` exhausts all injective principal cubic cores with at most
three directions for m<8 and finds none with this property. Restricting
any proposed example to the principal core of its bad cubic justifies
this minimality check; the first witness appears at m=8.

## 7. BAD-NARROW: a complete cluster payment with arbitrary faces

**Theorem BAD-NARROW (proved).** At rho=0, suppose every core unit
label lies in `(m/2,2m/3)`. Then

```
Pplus+gain+Lplus/m >= beta,
HCprime>=0.                                    (BAD-NARROW)
```

There is no restriction on q, t, the missing-pair graph, or k.

Proof. Put `a=min rho_i`, `b=max rho_i`. Every present pair has carry
1 and residue in `[2a-m,2b-m]`. Every cubic has carry 1, residue in
`[3a-m,3b-m]`, and three positive face carries. Thus

```
beta=t, gain=0, Pplus=p,
HCprime=Lplus+m(p-t),
Lplus/m >= ks/2+e.                             (8)
```

The open integer interval `(2b-m,a)` contains no core cell: pairs are
below it, units at or above a, cubics strictly above a, and the origin
is 0. Every residue in this interval is a spike. Hence

```
s >= m+a-2b-1 > m/6-1.                         (9)
```

All units and cubics lie strictly above m/2, so injectivity gives
`k+t<=floor((m-1)/2)<=m/2`, or `t<=m/2-k`.
For k>=6, (9) implies

```
ks/2-t > m(k-6)/12+k/2 >=0.
```

This proves (8) pays every cubic.

For k=3,4,5 use `m=1+k+q+t+s` in (9), obtaining
`5s>k+q+t-5`. Also `3t=sum psi<=(k+2)p`, while `p<=q<=Qk`.
It follows that

```
ks/2+e+p-t
 > k(k-5)/10+Qk+(k/10-1)(q+t)+p
 >= k(k^2+3k-10)/20 + (k^2-8k+10)p/30.
```

The last expression, minimized with p<=Qk, is respectively

| k | lower bound |
|---:|---:|
| 3 | 1/5 |
| 4 | 8/5 |
| 5 | 5 |

For k=1, t<=p and Pplus alone pays. For k=2 the only possible case
with t>p is all four binary cubics, p=q=3. Then e=0,
`m=10+s`, and (9) gives `5s>4`, hence s>=1. Now
`ks/2+e+p-t=s-1>=0`. This proves all cases. QED.

This theorem is restricted to the core units. Spikes may lie anywhere.
It does not apply merely because the factors of some of the bad
cubics lie in the indicated cluster while other core units lie outside.

## 8. Explicit shape payments for more cubics

Here the shape is arbitrary of height three. Let D be the support of
the missing-pair graph, v=|D|, and h=binom(v+1,2)-e, the number of
present pairs supported on D. All missing pairs are supported on D.
Put `W_D=sum_{i in D}rho_i`.

**Lemma DEGREE-MOMENT (proved).** For v>0 put

```
X=2e-v=fv+r, 0<=r<v,
E0=v binom(f,2)+fr.
```

Then

```
A>=ceil([binom(h,2)+(v+1)E0]/v).               (DM)
```

Proof. The ordinary sums of the h present D-pairs are distinct
nonnegative integers, so

```
binom(h,2)<=(v+1)W_D-A.
```

On D, `1<=delta_i<=v+1`. Thus `A-W_D=sum(delta_i-1)rho_i` has
nonnegative coefficients at most v with total X. Distinct nonnegative
unit residues give `A-W_D>=E0` by filling the lowest v slots first.
Substitute `W_D<=A-E0` in the preceding inequality. QED.

Other explicit lower bounds for A, useful with DM, are

```
Fdelta=sum_j j delta_[j]  (delta sorted decreasing),
Mcover(v,e)=max_{c=0,...,v-1} [binom(v-c,2)+M_e({min(i,c)+min(j,c):0<=i<=j<v})].
```

Here M_e denotes the sum of the e smallest entries, with multiplicity.
The second bound follows by writing every unit residue as
`min(rho_i,c)+(rho_i-c)_+`, using delta_i>=1 on D, and minimizing
the costs of e missing pairs. Actual sorted D-residues dominate
`0,...,v-1`. Take A0 as the maximum of these bounds and DM (A0=0
if v=0).

Let the N2 coefficients `d+2-psi(z)` sorted decreasingly be c_j, and
put `Gamma=sum_j j c_j`. Let Lambda be the accepted WINDOW-RANK
joint rearrangement bound using the unit coefficients s+delta_i
and the N2 coefficients. Define the explicit shape integer

```
Mshape=max(Lambda, A0+s binom(k,2)+Gamma).
```

**Corollary GENERAL-SHAPE (proved).** At every phase,

```
HCprime >= Mshape+m(Orest+Pplus+gain-beta).
```

In particular `beta<=floor(Mshape/m)` proves HC'>=0 without counting
any other credit. The sharper phase test includes the displayed
Orest, Pplus and gain. This is a uniform sufficient condition, not a
claim that every residual shape satisfies it.

## 9. A single bad cubic among arbitrarily many cubics

ONE-CUBIC and ONE-BAD are different assertions: t may be large while
beta=1. Here is an additional rigorous payment in that situation.

**Theorem ONE-BAD-SHAPE (proved).** With Gamma as above, put

```
Xi=s[binom(k,2)-2]+Gamma+e-2k-2t-1.
```

At every phase where beta<=1 and Xi>=0, MaxCL holds.

Proof. Suppose S<0. By (1), beta=1 and every credit in C is zero;
also Lplus<m, hence A<m. Orest=0 forces the origin and all units
outside W, so rho<m/2 and rho_i<nu. A nonnegative-carry pair in W
would also be counted by Orest. Pplus=PAplus=0 excludes all present
positive-carry pairs. Therefore exactly the proof of ONE-UNWRAP
applies, without requiring there to be only one cubic: WP gives

```
A>=k(k+1)-m+1-e=binom(k,2)-s-t.
```

On the other hand `Lplus>=A+s binom(k,2)+Gamma`. Subtracting
`m=1+k+s+Qk-e+t` yields `S=Lplus-m>=Xi>=0`, a contradiction. QED.

One count-only version replaces Gamma by
`max(0,d-t)binom(p,2)`, using the accepted `psi<=t+2`.
This loses information but requires only k,s,e,p,t.

**Corollary ONE-BAD-LOWPAIR (proved, HC' form).** Suppose beta<=1,
N2 is nonempty, and its least residue r satisfies r<rho. Put

```
Gamma_r=sum_j (j+r)c_j,
Xi_r=s[binom(k,2)-2]+Gamma_r+e-2k-2t-1.
```

Then Xi_r>=0 proves HC'>=0. If r=2, the weaker condition
`Xi_r+e>=0` already suffices.

Proof. A hypothetical HC'<0 forces beta=1,
`Orest=Pplus=gain=0`, and Lplus<m. Thus A<m, the origin and
all units lie outside W, and no nonnegative-carry pair lies in W.
The proof of ONE-WEIGHTED now applies with this least N2 residue r:
it uses r<rho, the fact that r is not a unit/origin residue, and
the collision at `w=rho+r`. The cubic-specific HOLES identity is
not needed once r<rho is assumed. Every N2 coefficient is bounded
using the distinct residues r,r+1,..., giving Gamma_r.
WP proves `HCprime>=Xi_r`; if r=2, WP2 increases this lower bound
by e. Both contradict the stated hypotheses. QED.

This corollary permits positive maximal-pair carries. The preceding
ONE-BAD-SHAPE theorem requires no low-pair assumption and gives S>=0.

## 10. Exact localization of the additional wrap obstruction

The weighted bound also has a phasewise defect form with no
unwrapping hypothesis. For each cyclic padded-pair fibre define

```
D_F=4 binom(g_F,2)-2 ell_F(g_F-1)+binom(ell_F,2),
A_F=sum of ordinary weights of its missing pairs,
omega_F=max(0,D_F-A_F-j_F),   Omega=sum_F omega_F.
```

DIFF-CENSUS gives, at every phase,

```
A>=k(k+1)-m+1-e-Omega,
HCprime >= (s+1)binom(k,2)-s-t+Gamma-Omega
           +m(Orest+Pplus+gain-beta).          (WRAP-REDUCTION)
```

Every unwrapped fibre has omega_F=0 by WP. Thus Omega is supported
on fibres with an ordinary wrap; it is not an unspecified loss in
the cubic relaxation. The one-cubic and ONE-BAD arguments above
exclude all these fibres in the branch where their payment is needed.

For beta>=2, A may reach m and missing pairs can themselves wrap.
Nonzero window and pair credits also permit wrapped present pairs.
Neither this report nor the numerical tests establish a uniform
bound that charges all those fibres against the available credits.
This is the precise gap in extending the weighted relay to all t.

## 11. The window identity at every height

For any height H, let C_j be the degree-j cells and N_j their
non-maximal members. For z in N_j put

```
psi_j(z)=sum_{i:z+e_i in C}(z_i+1) <= d+j.
```

Retain the same maximal-pair correction
`HC_H=S-m PAplus`. Define

```
L_H=sum_i(s+delta_i)rho_i
    +sum_{j=2}^{H-1}sum_{z in N_j}(d+j-psi_j(z))r(z) >=0,
kappa_y=(j-1)K(y)-sum_i y_i K(y-e_i),  y in C_j,
v_y=1_{r(y) in W},  b_y=kappa_y+v_y.
```

**Theorem WINDOW-H (proved).** The correct lift, at every j>=2, is

```
(j-1)ell(y)+rho=sum_i y_i ell(y-e_i),
m kappa_y=sum_i y_i r(y-e_i)-(j-1)r(y)-rho.     (H-LIFT)
```

Set

```
O_H=rho-#{all pairs with K=-1}
         -sum_{j>=3}#{y in C_j:r(y) in W} >=0.
```

Then exactly

```
HC_H=L_H+m[O_H+Pplus+sum_{j>=3}sum_{y in C_j} b_y],
b_y>=-(j-2).                                  (WINDOW-H)
```

Thus a safe uniform loss is `(j-2)m` per degree-j cell, with all
intermediate cells of degree at least three included. The cubic loss
is m, and the quartic loss is 2m.

Proof. The affine definition of ell gives H-LIFT: the constant
coefficient is `(j-1)^2-j(j-2)=1`, not j-2. In the MaxCL expression,
write the degree-j contribution, j>=3, as

```
(d+j)sum_{N_j}r-(j-1)sum_{C_j}r.
```

After the flat maximal-pair expansion, the unit pair-incidences
contribute `(d+2)sum_{N2}r` and `m sum_{N2}K`. Replacing each
negative term `(j-1)r(y)` by H-LIFT subtracts psi_j from the next
lower non-maximal coefficient and contributes one rho per cell.
These rho terms cancel the original one-rho-per-cell terms exactly.
The resulting carry expression is

```
HC_H=L_H+m[OW+sum_{N2}K+sum_{j>=3}sum_{C_j}kappa_y].
```

Subtract the distinct negative pairs and all higher window cells
from OW. This gives O_H and WINDOW-H. Nonnegativity of L_H follows
from `psi_j<=d+j`.

Finally H-LIFT gives `kappa_y>=-(j-1)`, because
`(j-1)r(y)+rho<jm`. If y is outside W, the stronger
`(j-1)r(y)+rho<(j-1)m` gives `kappa_y>=-(j-2)`.
If y is in W, its one window credit gives the same bound on b_y.
QED.

For mechanical verification, the complete expression immediately before
using H-LIFT is

```
HC_H=sum_i(s+delta_i)rho_i+(d+2)sum_{N2}r
     +sum_{j>=3}(d+j)sum_{N_j}r
     -sum_{j>=3}(j-1)sum_{C_j}r
     -rho sum_{j>=3}|C_j|+m(OW+sum_{N2}K).
```

Substitution of H-LIFT in its third and fourth sums produces WINDOW-H
without an omitted base or boundary term.

The proposed quartic expression `3ell(y)+2rho` is false; it must be
`3ell(y)+rho`. At m=5, label P=1, the column `{0,x,x^2,x^3,x^4}`,
and sigma=1, one has rho=4, ell(x^4)=-12 and ell(x^3)=-8:
the proposed left side is -28 while `4ell(x^3)=-32`.
This is minimal modulus for an injective quartic down-set.

A one-m local loss per quartic is also false. A smallest-modulus
example is the full column at m=5, P=4, sigma=2:

```
rho=3; (r(x),r(x^2),r(x^3),r(x^4))=(2,1,0,4);
K(x^3)=0, K(x^4)=-1;
kappa_(x^4)=-3, v_(x^4)=1, b_(x^4)=-2;
L_H=0, O_H=2, HC_H=S=0.
```

The two window credits are the origin and the unit. Since any
quartic down-set has at least five cells, this is minimal over all
phases. It is not a MaxCL counterexample.

At the origin there is a smallest witness at m=7, P=5: the same
column has `K(x^3)=K(x^4)=2`,
`kappa_(x^4)=3*2-4*2=-2`, and an empty window. Here k=1,s=2,d=3,
`L_H=18`; the cubic gives one gain and N2 one positive carry,
so `HC_H=S=18`. The origin-phase minimum is checked over every
admissible column label at m=5,6 before reaching m=7.

**Preserved minimization failure.** An earlier draft called m=7
minimal without restricting to the origin phase. The m=5 example
above corrects that claim; it is the smallest counterexample to it.

## 12. Computation and preserved intermediate failure

The main ONE-RELAY proof in sections 2--5, including the wrapped-fibre
payment and all small cases, is analytic. The following
are exact audits and exploratory reductions; sampled checks are not
being used as uniform hypotheses.

* `stress.py`: all phases of the lead's eight unpaid examples,
  212 phases total. Their minimum S and HC' agree, respectively,
  with 61,135,84,82,145,171,451,267. It also checks the m=17 sharp
  ONE-DEFICIT and the m=8 low-factor example.
* `target_one.py`: seed 260619, 200,000 proposals, m=17..150, k=5..18.
  After the parity filter there are 108,477 proposals. Each is tested
  with and without permitting positive maximal-pair carries. There
  are 13,015 successful deficit evaluations (the two modes may give
  the same tile), 4,238 with zero spikes. No S or HC' failure. The
  minimum observed Lplus-m is 30 at m=17,k=5,rho=8,U=(0,1,3,5,7).
* `window_h.py`: seed 2026101964, 4,000 proposals, m=10..150,
  proposed k=2..12, height caps 3,4,5. One third of proposals choose
  all unit labels in the narrow interval. Non-maximal core directions
  are retained after construction. Together with the named cases,
  3,900 actual cores and 314,412 phases are checked: 33,320 height-2,
  216,282 height-3, 48,983 height-4 and 15,827 height-5 phases.
  WINDOW-H and its loss bounds have zero failures. BAD-NARROW has
  1,307 qualifying core-origin checks, zero failures. Both mandatory
  E47/E51 full binary cores at m=14 are included at all phases.
* `algebra.py` checks the exact rational small-k BAD-NARROW table,
  the diagnostic moment-polynomial identities, and all 68 injective
  principal cubic cores through the first m=8 low-factor witness.
* `quartic_audit.py` checks every phase of every injective quartic
  column label at m=5..7, and all five WINDOW-H phases of the sharp
  m=5,P=4 column. It distinguishes the all-phase minimum m=5 from
  the origin-phase minimum m=7; neither is a MaxCL violation.
* `one_small.c` was written before the hole-2 improvement in WP2.
  It checks the six coarse-packing bases left by the earlier proof
  that used WP without WP2 and excluded positive maximal-pair carries.
  A partial unit set is pruned if it already forces more than e absent
  pairs, or its minimum missing-pair weight exceeds
  `m-1-2(k-1)`. The exact node counts are below. No complete leaf
  survives. This finite check is redundant after section 5.
* `one_small_check.py` independently enumerates the same six bases
  without using the missing-weight pruning. Its node counts are
  266,2,294,316,2,951,25,224,179,427 in the table order. Every branch
  dies at the missing-count test; there is no complete leaf. Thus the
  finite audit also excludes positive-slack complete cores in these
  six restricted bases, although that stronger exclusion is not needed.
* `weighted_pack_check.py` exhausts all 63,003 integer sets containing
  0, with 2<=n<=8 and largest element at most 18. The exact ordered
  difference-collision census and WP hold with minimum slack 0.
  The 41,225 sets omitting 2 also satisfy WP2, with zero failures.
* `wpack_actual.py` uses seed 2026101971 and 2,500 proposals with
  m=10..100, proposed k=2..10, on actual injectively labeled
  height-three cores. It checks DIFF-CENSUS, the phasewise Omega
  reduction, WP/WP2 on unwrapped fibres, ONE-BAD-SHAPE and
  ONE-BAD-LOWPAIR. There are 2,444 random cores plus one named phase,
  136,577 phases in total; 52,033 have unwrapped missing-pair fibres.
  There are 103,646 qualifying ONE-BAD-SHAPE checks and 79,607
  qualifying ONE-BAD-LOWPAIR checks, all clean. Final counts are in
  `d/results/wpack_actual.log`. A named k=4,s=3,m=17
  deficit with A=14<m exercises ONE-WEIGHTED explicitly.

| k | e | m | unit-value cases | DFS nodes | count prunes | weight prunes |
|---:|---:|---:|---:|---:|---:|---:|
| 6 | 3 | 26 | 3 | 110 | 55 | 38 |
| 7 | 3 | 34 | 5 | 639 | 262 | 298 |
| 6 | 4 | 25 | 3 | 81 | 19 | 48 |
| 7 | 4 | 33 | 5 | 549 | 117 | 363 |
| 8 | 4 | 42 | 7 | 3,688 | 1,108 | 2,216 |
| 9 | 4 | 52 | 9 | 23,224 | 8,607 | 12,830 |

The early `one_moment.py`, `moment_cover.py`, `one_reserve.py`,
`one_anchor.py` and `local_pairpack.py` runs retain exact necessary
count profiles only, not realizable cores. Their final pre-WP lists
are preserved. On `5<=k<=100,d>=6,0<=s<=3`, after the stated
PARTIAL-COVER and clean-row filters, the successive diagnostic lists
have 1,252 raw profiles, 802 reserve profiles (725 pure,77 mixed),
659 anchored profiles (605 pure,54 mixed), and 230 profiles after
the localized cyclic count, all pure with k=6..33. These are not
remaining MaxCL cases after ONE-RELAY. The scripts and JSON retain
the superseded route to make that distinction reproducible.

**Preserved failure: separate unit rank bound.** An early argument
incorrectly used `sum_unit rho_i>=Qk` at a phase where a unit can have
residue zero. Its resulting claim

```
Lplus>=A+s Qk+2(d-1)
```

is false even in ONE-DEFICIT. In the smallest possible deficit modulus,
m=17, the accepted sharp witness has

```
rho=8, U=(0,1,3,4,5,6), k=6,s=1,d=7,
Q={00,01,11,02,03,04,05,44}, T={444},
A=102, Lplus=133, HCprime=S=116.
```

The false bound gives 135. The correct joint rearrangement (4) gives
133 exactly. ONE-DEFICIT proves no deficit can occur at m<17, so this
is a smallest-modulus counterexample in the domain where it was used.

The all-high equivalence and the two quartic failures are preserved
in sections 6 and 11. No counterexample to MaxCL, Wilf, or an accepted
project theorem was found.

**Preserved failed candidate: ONE-DEFICIT requires a spike.** It does
not. At the minimum possible modulus m=17, take rho=8,

```
U=(0,1,3,5,7),
Q={00,01,02,03,11,12,13,33,34,44}, T={333}.
```

These are index notation on U. The core itself occupies all 17
residues, so s=0. It has OW=1,B=-2, A=39,Lplus=47 and
S=HCprime=30. Thus unwrapping and weighted packing, rather than
the existence of a spike, are necessary for the last branch.

## 13. Exact remaining gap and next lemma

The one-cubic HC' frontier is closed. In the previously accepted remaining
height-three family k>=5,d>=6, a counterexample must now have t>=2.
At a violating phase it must satisfy

```
C=Orest+Pplus+gain+PAplus < beta,
Lplus < m(beta-C),
beta > Orest+Pplus+gain+floor(Mshape/m).
```

It also fails the accepted CR, FLAT-CR, dense/few-cubic, cone and other
previous sufficient criteria. If beta=1 it must have Xi<0; in that
branch, where the least N2 residue r<rho, it must also fail
ONE-BAD-LOWPAIR: Xi_r<0, and Xi_r+e<0 if r=2. At the origin it cannot have all
core units in `(m/2,2m/3)`.

For a general multi-bad phase, the unwrapped-defect condition may fail:
missing pairs of ordinary weight at least m and wrapped present pairs
are the additional degree-two objects. WRAP-REDUCTION records their
exact fibre loss. No uniform charging map for them is proved here.

A precise next geometric lemma is the following **HIGH-ORIGIN**:
if rho=0 and all core unit residues are strictly above m/2, prove

```
Lplus/m+p+t >= 2 beta.                         (HIGH-ORIGIN, open)
```

Here all pairs have carry +1; every cubic is either bad with carry 1
or a gain with carry 2. Thus `gain=t-beta` and the displayed assertion
is exactly the required HC' payment in this entire high-unit regime.
BAD-NARROW proves it when the units are also below 2m/3. The extension
must account for the high units at or above 2m/3, whose cubic covers
generate gains. After that, the origin case with one low factor per
bad cubic is a separate remaining branch. General phases still need
the corresponding window accounting.

Status: **all one-cubic HC' and MaxCL are proved; the general height-three
MaxCL and Wilf theorem remain open.** The new geometric tools are
WP/WP2, the exact BAD-NARROW payment, ONE-BAD-SHAPE and WINDOW-H.

## 14. Formalization boundary

No new Lean code is claimed. The central proof can be split into finite
lemmas with the following interfaces:

1. A finite subtype V of `ZMod m`, its integer representatives, `Sym2 V`,
   an injective present-pair subset, and the difference-fibre cardinalities:
   DIFF-CENSUS and COARSE-PACK.
2. Add the equality of ordinary sums in each missing-pair fibre:
   WP; add the omitted representative 2: WP2. These use only finite
   pair counts and the ordering of nonnegative integers.
3. Instantiate with the origin and unit residues. ONE-DEFICIT gives
   ONE-UNWRAP. The two unavailable endpoint values rho and r give
   ONE-WEIGHTED for the remaining wrapped fibres.
4. Combine (4)--(7) and the explicit k=3,4,5 inequalities to obtain
   `HCprime>=0`; no unverified finite base is an input.
5. WINDOW-H is a finite-sum identity using H-LIFT and the incidence
   double count defining psi_j. Its loss estimate uses only the floor
   inequalities stated in section 11.

The target is stronger than needed at sigma=c mod m: the one-cubic
HC' inequality holds for every phase, so the existing Lean MaxCL
implications can use it without a phase-selection argument.
