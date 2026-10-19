# P8: symmetric row packing and residue-mass payments at height three

2026-10-19. All computations ran on fejer, with nice 10 and at most four
single-core jobs. Work was placed in `~/wilf/p8/h3/`: `~/wilf/p8/` already
contained earlier P5 work, which was left intact. Earlier reports are
unchanged. No commits were made.

**PROVED, analytic:** the cyclic, height-independent SYMMETRIC-RECTANGLE
inequality; GENERAL-FEW21+240 (`k>=21t+240`, every phase, every cubic
shadow); its all-height weighted version; and the shadow-density theorems
in section 8.

**PROVED, with finite exact convex certificates:** HC' at every phase if
`p>=9t/4` and `k>=255`; and HC' in every dimension if `p=3t`. The latter
condition says exactly that the cubics are squarefree and no two have a
common quadratic divisor. These are infinite classes.

**COUNTEREXAMPLE:** the stronger shortcut `Lplus>=mt` for arbitrary
height-three cores fails at `m=20,k=5,t=4`: `Lplus=79`, `mt=80`, while
`HC'=S=99`. Window credits remain necessary.

**OPEN:** general height-three MaxCL. No MaxCL violation was found.
The remaining possible family and the distinction between actual tiles
and negative relaxed count profiles are stated in section 12.

## 1. Exact setting and the accepted window identity

Remove maximal-unit spikes. The remaining core has k non-maximal units,
q pairs Q, p covered pairs N2, and t cubics T. All cubics are maximal.
Set

```
Qk=binom(k+1,2), Uk=binom(k+2,3), e=Qk-q,
s=m-(1+k+q+t), d=k+s, epsilon=Uk-t,
a=q-p, w=3t-p.
```

Thus epsilon denotes missing cubics, while e denotes missing pairs.
The new shadow parameter w is the excess of weighted cubic-face
incidences over distinct covered pairs. In particular w>=0. Exactly
`d+1=m-q-t`.

At a phase sigma, let `rho=r(0)`, `u_i=r(e_i)`, and

```
ell(x)=sum_i x_i u_i-(|x|-1)rho,
K(x)=floor(ell(x)/m), r(x)=ell(x)-mK(x),
psi(z)=sum_{i:z+e_i in T}(z_i+1),
delta_i=k+1-sum_{z in Q}z_i,
A=sum_i delta_i u_i.
```

There are `v=#{i:delta_i>0}` defective directions. All missing pairs
lie on these v directions, their number is e, and

```
sum delta_i=2e, 0<=delta_i<=v+1 on the defective directions,
ceil(v/2)<=e<=binom(v+1,2) when v>0.
```

Let `U=sum_i u_i` and `R=sum_N2 r`. The exact MaxCL slack, including
all spikes, is

```
S=(d+1)(rho+U+R)-sum_A2 r-2sum_T r.                  (1.1)
L=A+sU+sum_N2(d+2-psi(z))r(z).
```

We use the accepted HC'/WINDOW-ID, but recall its derivation. Put

```
kappa_y=2K(y)-sum_i y_i K(y-e_i),
b_y=kappa_y+1_{r(y)>=m-rho}.
```

The lift gives

```
2ell(y)+rho=sum_i y_i ell(y-e_i),
m kappa_y=sum_i y_i r(y-e_i)-2r(y)-rho.
```

It implies `b_y>=-1`: outside the window the right side is greater
than -2m; inside it is greater than -3m before the window credit.
Let beta count the b=-1 cubics, gain sum the positive b's, Pplus
count positive-carry N2 pairs, and Orest count the window cells
left after deleting negative-carry pairs and cubic window cells.
Residue completeness gives Orest>=0. Expanding maximal pairs by
the flat identity and summing the cubic lift gives exactly

```
HC'=L+m(Orest+Pplus+gain-beta),
S=HC'+m PAplus,                                     (1.2)
```

where PAplus counts positive-carry maximal pairs. The carry term
before window separation is `2sum_T K-sum_N2(psi-1)K`;
`sum_y sum_i y_i K(y-e_i)=sum_N2 psi K` verifies its coefficient.
Every pair has `psi<=k+2`, so L has nonnegative coefficients. Thus

```
HC'>=L-m beta>=L-mt.                                (WL)
```

We do not assume unrestricted `L>=mt`; section 11 refutes it.

## 2. A new height-independent cyclic packing inequality

**PROVED: SYMMETRIC-RECTANGLE.** Suppose the origin, k units and a
quadratic down-set have injective labels modulo m. Residue completeness
and any upper-layer hypothesis are unnecessary. Then

```
m>=k(k+1)+1-v(v-1)-4e.                              (SR)
```

Proof. Work in Z/m. Pad with zero, and let V contain zero and the
k unit labels. Let G consist of zero and the good units, those
untouched by missing pairs; `h=|G|=k-v+1`. All formal pairs with
at least one endpoint in G are present. Their sums are distinct.
Padded pairs are interpreted as the origin or units.

Consider `D1={g-b:g in G,b in V,g!=b}`. The rectangle argument
gives `|D1|=hk`: a collision compares two present formal sums,
forcing equality of the ordered differences. The h(h-1)
good-good differences lie in `D1 intersect (-D1)`.

Any other element of that intersection has representations
`g-b=b'-g'`, with g,g' good and b,b' bad. An endpoint b' in G
would compare two present sums and be impossible. Now
`b+b'=g+g'`. The bad-bad pair must be missing, since the good-good
pair is present and formally different. A fixed missing pair has
at most one good-good pair with the same sum. Those two unordered
pairs give at most four intersection labels; loops decrease this
number. Hence

```
|D1 intersect (-D1)|<=h(h-1)+4e,
m-1>=|D1 union (-D1)|>=2hk-h(h-1)-4e.
```

Substitute `h=k-v+1`. This permits even m, 2-torsion and 3-torsion;
no integer DIFF2 statement is used. QED.

Retain also the one-sided rectangle bound

```
m>=k(k-v+1)+1.                                     (R)
```

With `C=binom(k,2)`, `M0=binom(k+2,2)`, the two bounds give

```
s>=max(0,C-kv+e-t,C-v(v-1)-3e-t).                   (SR-s)
```

The second nonzero term is new. Both terms enter the finite
certificate in section 9.

## 3. The linked missing-pair moment, with e retained

This re-derives the accepted LINKED-CUBIC input before minimizing e.

**PROVED: RETAINED-MOMENT.** For v>0 put

```
qD=v(v+1)/2-e, X=2e-v,
F(v,e)=[binom(qD,2)+(v+1)(X^2/(2v)-X/2)]/v.
```

Then `A>=F(v,e)` at every phase. Indeed let W be the sum of the
defective unit residues and `E=A-W`. The nonnegative weights
delta_i-1 have sum X and cap v. For distinct nonnegative integer
residues their weighted rank bound is at least `X^2/(2v)-X/2`.
For `X=vf+r`, the exact minimum is `v binom(f,2)+fr`; the
difference is `r(v-r)/(2v)>=0`.

The ordinary sums of the qD present pairs on defective directions
are distinct nonnegative integers. Their sum is
`(v+1)W-A=vA-(v+1)E>=binom(qD,2)`. Combining proves the claim.
All these facts are height-independent. The full expansion is

```
F(v,e)=v^3/8-ve/2+5e^2/(2v)
       +v^2/4+7v/8+3/4-7e/2-5e/(2v)+2e^2/v^2.      (3.1)
```

`certify.py` verifies this identity coefficientwise over fractions.

## 4. Paying the pair mass after rearrangement

**PROVED: SHADOW-RANK.** At every height-three phase,

```
sum_N2(d+2-psi)r >= (d+1)binom(p,2)-w(p-1),
HC'>=A+sC+(d+1)binom(p,2)-w(p-1)-mt.                (M)
```

Proof. Set `a_z=psi(z)-1`. These nonnegative integers sum to w,
and `d+1-a_z>=0`. Sort the latter coefficients decreasingly.
For distinct nonnegative residues their weighted sum is at least
the rank sum on 0,...,p-1, which is
`(d+1)binom(p,2)-sum_j j a_j >= (d+1)binom(p,2)-w(p-1)`.
Also U>=C. Insert in (WL). QED.

The p-1 factor matters. Subtracting excess incidences from arbitrary
residues before rearranging would lose w(m-1).

For real `h in [13/6,3]` with p>=ht, the function p(3t-p) decreases
on this range. Therefore

```
HC'>=A+sC+(d+1)(h^2 t^2-ht)/2-h(3-h)t^2-mt.         (Mh)
```

A phase-free sufficient criterion follows. Put
`FZ=ceil(max(0,F(v,e)))`, with FZ=0 at v=0. Then HC' holds at
every phase if

```
FZ+sC+(k+s+1)binom(p,2)-(3t-p)(p-1)>=mt.             (MC)
```

The uniform infinite-family theorems below are stronger deliverables
than this criterion alone.

## 5. Normalized moments: complete polynomial certificates

Define `f(x,y)=x^3/8-xy/2+5y^2/(2x)` and `z=1/2-y`.

**PROVED: NORMALIZED-MOMENT.** On the real domain

```
0<x<=2, 0<=y<=1, x>=1/2+y, x^2+3y>=1/2,             (D)
```

one has

```
f(x,y)>=z/21+1/50000,                              (NL)
```

and these three quadratic inequalities:

| h | gamma=1/(2h^2) | mu | bound |
|---|---|---|---|
| 9/4 | 8/81 | 1/1000 | f >= gamma z^2+mu |
| 11/5 | 25/242 | 1/2000 | f >= gamma z^2+mu |
| 13/6 | 18/169 | 1/50000 | f >= gamma z^2+mu |

Proof. Domain (D) forces x>=14/25: otherwise
`x^2+3y<=x^2+3x-3/2<1/2`; the endpoint gives 0.4936.
Put `a=14/25`, `b=31/50`, `y0=(1/2-x^2)/3`.

For a<=x<=b, (D) gives y>=y0. The derivative of
`f-gamma z^2` in y is `-x/2+gamma+(5/x-2gamma)y`. Its lower
bound `-b/2+gamma+(5/b-2gamma)(1/2-b^2)/3` is positive in
each row. For (NL) the derivative is `-x/2+5y/x+1/21`,
with positive lower bound 3149/65100. Thus minimization in this
range reduces to y=y0.

For a quadratic row form the degree-five polynomial

```
P(x)=x^4-4x^2 y0+20y0^2-8gamma x(1/2-y0)^2-8mu x.
```

For (NL) use the degree-four polynomial

```
P_L(x)=x^4-4x^2 y0+20y0^2-(8/21)x(1/2-y0)-8x/50000.
```

The exact Bernstein certificates are below. On [l,r], a vector
`(c_0,...,c_n)/D` means

```
P(l+(r-l)u)=sum_j (c_j/D)binom(n,j)u^j(1-u)^(n-j).
```

Every numerator is positive, proving positivity on the entire
interval including endpoints.

| row | interval | D | numerator vector, in order |
|---|---|---:|---|
| h=9/4 | [14/25,31/50] | 113906250000 | (945712624,481534168,231969676,221016532,473944549,1017288193) |
| h=11/5 | [14/25,59/100] | 181500000000 | (1205644800,825360224,530230672,325025712,214641299,204099370) |
| h=11/5 | [59/100,31/50] | 181500000000 | (204099370,193557441,282857996,477022972,781200288,1200663440) |
| h=13/6 | [14/25,59/100] | 3802500000000 | (22974001664,14875365536,8555777264,4115011136,1655484389,1282248461) |
| h=13/6 | [59/100,31/50] | 3802500000000 | (1282248461,909012533,2622067424,6526464572,12729889616,21342653648) |
| NL | [14/25,59/100] | 2100000000 | (8641024,4198696,1479264,625576,1788229) |
| NL | [59/100,31/50] | 2100000000 | (1788229,2950882,6129876,11475808,19147024) |

For x>=b use the exact square

```
f=x^3/10+(5/(2x))(y-x^2/10)^2.                      (5.1)
```

For (NL), z<=1/2 gives
`f-z/21-1/50000>=b^3/10-1/42-1/50000=43/13125000>0`.

For a quadratic row put `alpha=5/(2x)-gamma>0`. Its minimum
as a quadratic in y is nonnegative if

```
Q(x)=x^3-gamma*x^4/2+gamma*x^2+4gamma*mu*x
      -(5gamma/2+10mu)>=0.
```

This is the discriminant test multiplied by x. On [b,2],
`Q'=x^2(3-2gamma*x)+2gamma*x+4gamma*mu>0`. The Q(b) values are

```
1040161/84375000, 879667/121000000, 5211591/1056250000,
```

respectively. Thus every branch is proved. `symmetric.py` verifies
the identities and coefficients over fractions. QED.

## 6. What a negative phase would force

The next caps are conditional on HC'<0, not bounds on every tile.

**PROVED: NEGATIVE-CAPS.** Suppose k>=150, t>=2, and either
p>=13t/6 or t<k/4 is already known. In the former case, HC'<0
first forces t<k/4. In both cases it forces

```
s<k/2,
m<k^2/2+9k/4+1-e,                                  (6.1)
v>=k/2-5/4+e/k,
(v+2)^2+3e>=k^2/2.                                 (6.2)
```

Proof of the t cap. By (Mh), after dropping A and sC and
putting `m=M0-e+t+s`, a negative value requires

```
[h^2(k+s+1)-2h(3-h)-2]t<h(k+s+1)+2(M0-e+s).
```

If t>=k/4, e>=0 gives the opposite inequality. At h=13/6,
k=150+X, its difference at s=0 is

```
(25/144)X^2+(747/16)X+74225/24>0.
```

Its s coefficient is `h^2 k/4-h-2>0`. The difference increases
with h: its derivative is
`(k+s+1)(hk/2-1)+(4h-6)k/4>0`. This proves the cap for
h in [13/6,3].

For spikes, (WL) gives `sC<mt`, hence `s(C-t)<t(M0+t)`.
With t<k/4, s>=k/2 contradicts `2C>=M0+3k/4`, true at
k=150 and increasing thereafter. This proves s<k/2 and (6.1).
Combining (6.1) with (R) gives the first bound in (6.2).
Combining it with (SR) gives `v^2-v+3e>k^2/2-5k/4`.
Adding 5v+4 and using the first bound in (6.2) proves the last
assertion. QED.

Put `x=(v+2)/k`, `y=e/k^2`, `z=1/2-y`. Under these caps
v>0 and all of (D) hold. The upper bounds follow from v<=k,
e<=Qk and k>=150. Expansion (3.1), e<=v(v+1)/2 and

```
d/dv [v^3/8-ve/2+5e^2/(2v)]<=3v^2/8
```

give

```
A>=k^3 f((v+2)/k,e/k^2)-(5k^2/2+6k+17/4)
 >=k^3 f(x,y)-11k^2/4.                             (6.3)
```

In detail the shift by 2 costs at most `3(v+2)^2/4`; the
discarded negative terms cost at most
`7v(v+1)/4+5(v+1)/4`. Their sum is `5v^2/2+6v+17/4`,
at most 11k^2/4 for k>=150. Unit residue zero is allowed in
every rank bound used here.

## 7. An improved all-shadow theorem, including all heights

**PROVED: GENERAL-FEW21+240.** Every height-three tile with t>=2 and

```
k>=21t+240                                          (GF21)
```

satisfies HC'>=0, hence MaxCL, at every phase.

Proof. Suppose HC'<0. Here k>=282 and t<k/4, so section 6
applies. By (NL) and (6.3),

```
A>=z k^3/21+k^3/50000-11k^2/4.                      (7.1)
```

If z>=1/4, cardinality gives m>=z k^2 while (6.1) gives
`m<z k^2+9k/4+1`. Since 21t<=k-240,

```
A-mt >= A-m(k-240)/21
 >=k^3/50000-(11/4+9/84)k^2-k/21+(240/21)m
 >=k^3/50000-k/21>0.
```

The k^2 terms cancel: `11/4+9/84=240/84`. The last inequality
holds for k>=282. This contradicts A<=L<mt.

If z<1/4, then e>k^2/4. The missing-degree rank bound gives

```
A>=2e^2/(k+1)-e>=k^4/(8(k+1))-k^2/4
 >=k^3/9-k^2/4,                                   (7.2)
```

because the quadratic increases above k^2/4 and the last
comparison holds for k>=8. Also
`mt<(k/21)(k^2/4+9k/4+1)`. Hence

```
A-mt>(25/252)k^3-(5/14)k^2-k/21>0
```

for k>=8, again a contradiction. QED.

The earlier GENERAL-FEW40 is preferable at small t. The new
threshold is smaller exactly for t>=13; together they give
`min(40t+8,21t+240)`. This closes an unbounded part of P8's
complement with no cubic-shadow restriction.

**PROVED: H-FEW21+240.** At arbitrary height, put
`B=sum_{j>=3}(j-2)|C_j|`. If B>=2 and k>=21B+240, then
HC_H>=0 and MaxCL hold at every phase. C_j includes every
degree-j cell, maximal or not.

Indeed the accepted WINDOW-H, obtained from
`(j-1)ell(y)+rho=sum_i y_i ell(y-e_i)`, gives
`HC_H>=L_H-mB`, `L_H>=A+sU`. Its other coefficients are
nonnegative because psi_j<=d+j. Write
`T=sum_{j>=3}|C_j|<=B`. Then
`m=M0-e+T+s<=M0-e+B+s`, while `m>=M0-e>=z k^2`.
The spike cap, packing comparisons, (6.3), and the preceding
proof apply with B replacing t. No cubic-specific shadow-rank
or carry classification is needed for this corollary.

## 8. A broad many-cubic shadow regime

**PROVED, analytic: SHADOW-DENSE.** For each row, if t>=2,
p>=ht and k is at least the threshold, HC'>=0 at every phase.

| h | analytic threshold for k |
|---|---:|
| 9/4 | 3250 |
| 11/5 | 6500 |
| 13/6 | 162500 |

Proof. Suppose HC'<0 and apply section 6. Since h>=2, (Mh),
after discarding the spike term and replacing d by k, implies

```
HC'>=A+(h^2 k/2)t^2-[m+h(k+1)/2]t
 >=A-[m+h(k+1)/2]^2/(2h^2 k).                       (8.1)
```

The discarded extra quadratic coefficient is 3h(h-2)>=0.
By (6.1), for k>=150,

```
0<m+h(k+1)/2<z k^2+4k,
[m+h(k+1)/2]^2/(2h^2 k)
 <=gamma z^2 k^3+[2/h^2+8/(kh^2)]k^2
 <=gamma z^2 k^3+k^2/2,                            (8.2)
```

where gamma=1/(2h^2). The cross term uses only z<=1/2; the
bound remains valid if z is slightly negative, since the two
quantities before squaring are positive. NORMALIZED-MOMENT and
(6.3) now give `HC'>=mu k^3-13k^2/4`, nonnegative at the
tabulated thresholds, a contradiction. These are estimates at a
proposed negative phase, not unconditional lower bounds of this
size for every tile's slack. QED.

### 8.1. Exact convex improvement: k>=255 when p>=9t/4

**PROVED WITH FINITE CERTIFICATE: SHADOW-225.** The h=9/4 theorem
holds already for k>=255.

Only 255<=k<3250 needs a finite certificate. At a proposed
negative phase, section 6 forces these integer ranges:

```
ceil(k/2-5/4)<=v<=k,
lo=ceil(max(v/2,[k^2/2-5k/4-v(v-1)]/3)) <= e,
e<=hi=floor(min(v(v+1)/2,kv-k^2/2+5k/4)).             (8.3)
```

Put h=9/4 and

```
a_h=h^2(k+1)-2h(3-h)>0,
Z0=k^2/2+9k/4+1+h(k+1)/2,
G(k,v,e)=F(v,e)-(Z0-e)^2/(2a_h).                    (G)
```

Keeping the extra quadratic coefficient before (8.1) proves
HC'>=G at a proposed negative phase. For fixed k,v, G is a
strictly convex quadratic in e, with coefficients

```
alpha=(5v+4)/(2v^2)-1/(2a_h),
beta=-v/2-7/2-5/(2v)+Z0/a_h,
gamma0=v^3/8+v^2/4+7v/8+3/4-Z0^2/(2a_h).
```

Its minimum on [lo,hi] occurs at
`min(hi,max(lo,-beta/(2alpha)))`. This covers all e, rather
than a sampled grid. Alpha>0 follows from a_h>=h^2 k>4k and
v<=k.

`finite_shadow.py --symmetric --h 9/4 --end 3249` checks these
quadratics over fractions. Over 150<=k<=3249 it visits 2,314,825
nonempty intervals. Negative minima occur only for k<=254.
On the entire required range 255<=k<=3249 the least minimum is

```
3278015777/25852500>0 at (k,v,e)=(255,150,3282).
```

Together with the analytic tail this proves SHADOW-225. The
complete per-k minima, including the failed smaller-k relaxation,
are in `results/finite_shadow_sym_9_4.json`. This is a finite
exact certificate in count parameters, not an enumeration of
actual labelings.

## 9. All squarefree, pair-disjoint cubic families

**PROVED WITH FINITE CERTIFICATE: DISJOINT-CUBICS.** Suppose a
height-three tile has squarefree cubics and no two share a
quadratic divisor. If t>=2, HC'>=0 at every phase, with no
restriction on dimension, t, or spikes.

Equivalently p=3t: `w=sum_N2(psi-1)=0` forces psi=1,
excludes repeated-factor cubic types, and excludes a shared
face. For t>=2 it forces k>=5: two three-element subsets of
four vertices share a pair.

For k>=255 this follows from SHADOW-225. The remaining range
is 5<=k<=254; its finite certificate is as follows. Put

```
p=3t, C=binom(k,2), M0=binom(k+2,2),
Gs=C+binom(3t,2)-t>0,
C0=(k+1)binom(3t,2)-t(M0+t).
```

If `(9k+7)t>=k^2+6k+5`, then C0>=0 and (M) proves HC'
without a defect moment. Only

```
2<=t<=min(floor(C/3),floor((k^2+6k+4)/(9k+7)))        (9.1)
```

needs checking. The first bound counts three distinct ordinary
pair faces per cubic. For each k,t take 0<=v<=k and

```
ceil(v/2)<=e<=min(binom(v+1,2),Qk-3t).               (9.2)
```

By (M), (F) and (SR-s), a lower bound for HC' is

```
F(v,e)+te+C0
 +Gs max(0,C-kv+e-t,C-v(v-1)-3e-t).                 (J)
```

At v=0, e=0 and A>=0 replace F. Otherwise this is a convex
quadratic plus the maximum of three affine functions. Their
slopes and offsets are

```
(0,0), (1,C-kv-t), (-3,C-v(v-1)-t).
```

On each interval where one is largest, add its slope and offset,
multiplied by Gs, to the quadratic coefficients of F+te+C0.
Intersect with (9.2) and minimize at the clamped quadratic vertex.
This is exactly `small_disjoint.py --symmetric --end 254`.

All 585,036 nonempty (k,t,v) domains have nonnegative minimum.
In fact the least is

```
15355/507>0 at (k,t,v,e)=(23,2,13,95/3).
```

The real e=95/3 is permitted in this certificate: minimizing
over the real interval relaxes integer e and strengthens the
exclusion. There are no unchecked e or s. The s coefficient
is Gs>0, so its minimum is the maximum in (SR-s). This proves
the finite part and the infinite theorem. QED.

**Semigroup corollary.** Wilf holds whenever a factorization tile
has height at most three and its cubic factorizations are
squarefree with pairwise disjoint quadratic-divisor sets. The
t=0 and t=1 cases use the accepted flat and one-cubic theorems.
SHADOW-225 and (GF21) also give Wilf under their respective
factorization-tile hypotheses, through the accepted
MaxCL => Tile-TOP'' => Wilf reduction.

## 10. Computational checks, scope and reproduction

All scripts are in this directory; outputs are in `results/`.
Python was the supplied fejer environment, Python 3.12.3. Fractions,
integer arithmetic and elementary polynomials suffice; no sympy.

**FINITE CHECK: symbolic certificates.** `symmetric.py` expands
every Bernstein polynomial over fractions, verifies the branch
derivative and discriminant tests, and the cap and error polynomials.
`certify.py` separately implements polynomial arithmetic and checks
the retained F expansion and square identities. Its earlier
near-maximal-shadow calculation and 26,160 exact moment checks are
retained in `results/certify.json`; those thresholds are superseded
by the symmetric-packing results here.

`review.py` independently reconstructs each Bernstein polynomial
from its coefficient vector and compares with the direct moment
formula at n+1 rational points for degree n. These equalities prove
the polynomial identity. All nine retained interval certificates
pass 50 exact comparisons, including the unused but true 1/22 row.
The reviewer also checks coverage and positivity of the asserted
finite-table ranges; this table review does not replace the scan.

**FINITE CERTIFICATES used in the theorems.**

| source | range | domains | conclusion used |
|---|---|---:|---|
| `small_disjoint.py --symmetric --end 254` | k=5..254 | 585,036 convex domains | all minima positive; DISJOINT-CUBICS below 255 |
| `finite_shadow.py --symmetric --h 9/4 --end 3249` | k=150..3249 | 2,314,825 e intervals | all k=255..3249 positive; SHADOW-225 below 3250 |

The analytic proofs cover the unbounded tails. Negative relaxed
minima below 255 in the second run are preserved.

**FINITE EXHAUSTIVE MODULAR AUDIT:** `pack_check.py` examines every
unit set with 3<=m<=16, 2<=k<=5 and every maximal choice of one
permitted quadratic monomial per available residue. There are
14,756 unit sets and 91,182 maximal quadratic selections, with
no failure of (SR), including its difference-intersection bound.
Minimum packing slack is 0 at m=7, unit labels {1,3}.
Any partial selection extends to a maximal one. Deleting a pair
increases e and cannot decrease v, hence decreases the right side
of (SR); these selections therefore audit every partial selection
on the same unit sets. This is a check of the proved lemma.

**FINITE ACTUAL-TILE AUDIT:** `audit.py`, seed 2026101981, uses 700
proposals and produces 690 actual cores including named cases,
testing 53,925 phases. Of these, 53,577 are in P8's many-cubic
complement, 20,002 have p>=2.9t, and 12,029 have p=3t. The script
independently computes S, HC', L, carries and the window census,
checking (F), (R), (SR), SHADOW-RANK and (M). No claimed inequality
fails. These small cores are not asserted to test the large
analytic cutoffs.

Every phase of E47 and E51 and the eight mandatory stress cores
is included. The stress minimum S values remain, in file order,

```
61,135,84,82,145,171,451,267.
```

As a further named stress calculation, insert the verified P7
Sidon counts k=127,s=111106,t=72676,p=8126,m=192038 into (M),
with A=0. This gives `HC'>=3657269855418>0` at every phase.
Thus retained mass pays the H1' counterexample as expected.
P8 is not claimed to be the first criterion paying that family.

The audit found the omitted-excess pair-bound failure in section
11. No MaxCL or HC' violation appeared. Sampled nonviolations are
not used as a uniform hypothesis.

**COUNTEREXAMPLE SEARCH:** `search_mass.c` includes the lead's
`src/scratch/h3/anneal_h3.c` shape/label mutation machinery but
uses a new objective: the exact minimum of L-mt over all phases,
computed by a cyclic coefficient sum. K is restricted to 10 to
respect that source's array bounds. Runs (K,m,seed) were
(7,35,1981), (5,20,1982), (8,50,1983), (10,80,1984), with
233,454 / 109,430 / 397,210 / 301,550 evaluations respectively.
The second stopped at the mass counterexample. The others
finished. The original MaxCL slack was separately tested at
each state; no violation appeared.

`verify_witness.py` checks the mass witness twice: by the sparse
carry evaluator and by enumerating all 20 cells and their upper
covers in the original MaxCL formula. Both give S=99.

Reproduce in `~/wilf/p8/h3`, after copying the code, stress file
and lead source:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python symmetric.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python finite_shadow.py --symmetric --h 9/4 --end 3249 --output results/finite_shadow_sym_9_4.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python small_disjoint.py --symmetric --end 254 --output results/small_disjoint_sym254.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python pack_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python audit.py --stress-source stress.md --output results/audit_sym.json
nice -n 10 ~/mathenv/bin/python verify_witness.py
nice -n 10 ~/mathenv/bin/python review.py
nice -n 10 cc -O2 -DP8_REMOTE search_mass.c -lm -o search_mass
nice -n 10 ./search_mass 5 20 1982 200000 12
```

For the remote C build copy the lead source as `lead_anneal_h3.c`;
the repository-relative include is used without P8_REMOTE. Copy
`examples/h3_middle_family_unpaid.md` as `stress.md`. Run at most
four commands concurrently.

## 11. Preserved failures and rejected stronger constants

**COUNTEREXAMPLE: global L>=mt.** Take

```
m=20, P=(12,3,5,9,19), sigma=18, rho=2,
Q={00,01,02,03,04,11,12,14,23,33},
T={000,003,033,333}.
```

Together with the origin and five units these are exactly 20
cells, using every residue. Thus s=0,d=k=5,q=10,p=3,t=4.
At the stated phase,

```
u=(14,5,7,11,1), delta=(0,1,3,2,4), A=52,
covered-pair residues (00,03,33)=(6,3,0),
psi=(4,4,4), pair mass=27, L=79<80=mt.
```

Cubic residues are (18,15,12,9); three cubics are bad and
the fourth uses its window credit. Pplus=3, Orest=1 and
gain=PAplus=0. Hence `HC'=79+20(1+3-3)=99=S`.
Independently the maximal-pair residues sum to 87, the cubic
residues sum to 54, and the original formula gives
`6*20*19/2-7*87-8*54=99`. Minimum S over all phases is also
99. This is the smallest mass witness found in this P8 search,
not a claim of global minimum modulus.

**COUNTEREXAMPLE: omitting w in the pair bound.** A minimum-modulus
witness is m=6, P=(2,3), Q={00,01}, T={001}, rho=2 (sigma=4).
The covered-pair residues are (0,1), with coefficients (3,2),
and mass 2 below the false bound `(d+1)binom(p,2)=3`.
A failure needs p>=2, hence two units, two pairs and a cubic;
thus m>=6, proving minimality.

Within t>=2 the minimum is m=7, P=(5,3), Q={01,11},
T={011,111}, rho=6 (sigma=1). Pair residues (0,5) have
coefficients (2,0), giving mass 0<3. Cell count forces m>=7.
Both cases are exactly checked by `verify_witness.py`.

The audit initially found the larger witness m=14, P=(5,6),
all binary pairs and cubics, sigma=10 (rho=4), with
s=4,d=6,p=3,psi=(4,4,4). Pair residues (0,1,2) have mass
12<21. SHADOW-RANK correctly subtracts w(p-1)=18, giving
3<=12. This initially discovered case is retained too.

**COUNTEREXAMPLE to a larger normalized margin.** For
`h=13/6,gamma=18/169`, mu=1/10000 is false even on (D).
At `x=59/100`, `y=(1/2-x^2)/3=1519/30000`, P from section
5 is `-908731/22500000000`. This refutes that algebraic
margin, not a claim about actual tiles. The proved row uses
mu=1/50000 and its own positive certificate.

**Negative count relaxations retained.** Before (SR), the
small disjoint-cubic relaxation left 472 negative (k,t,v)
domains at k=18..149, t=2..8. The worst minimum was -52168/81
at (106,6,54,165). They remain in
`results/small_disjoint.json`. Adding (SR) kills all of them,
and the extended run is positive through k=254. These profiles
were never asserted to be residue-complete tiles.

**A limit of the present moment relaxation.** The normalized point

```
x=29/50, y=409/7500, z=3341/7500
```

satisfies both leading packing constraints, the symmetric one
with equality. Exactly

```
f(x,y)=5583521/261000000,
f(x,y)-z/20=-229819/261000000<0.                     (11.1)
```

Thus the implication f>=z/20 from (D) is false. In leading count
scaling take v~xk, e~yk^2, t~k/20, s=0, m~zk^2, with a
concentrated shadow p=O(k^(2/3)). The pair rank term is then
o(k^3); retained moment minus mt is negative to leading order.
A full cubic face on O(k^(1/3)) good directions supplies those
shadow orders. None of this constructs residue labels or a
MaxCL violation. It explains why the new moment inequalities
do not close the whole regime.

## 12. Exact remaining gap and the next geometric lemma

**PROVED status:** GENERAL-FEW21+240, SHADOW-225, its analytic
broader-shadow extensions, and DISJOINT-CUBICS are new all-phase
infinite classes. SYMMETRIC-RECTANGLE and H-FEW21+240 are
additional results. Finite certificates and sampled checks are
separately identified. No unproved packing assertion is used.

**OPEN residual.** Besides failing all accepted P6 criteria, a
possible height-three MaxCL counterexample must satisfy

```
k>=5, d=k+s>=6, t>=2, t=Uk-epsilon,
k<min(40t+8,21t+240), p<3t,
if k>=255:    p<9t/4,
if k>=6500:   p<11t/5,
if k>=162500: p<13t/6.
```

Its integer counts obey m=M0-e+t+s, p<=q=Qk-e, the localized
defect conditions on v,e and (SR-s). It must fail (MC), the
accepted CR, FLAT-CR, WINDOW-RANK, dense-face and retained-face
packing criteria, and all applicable origin and relay theorems
from P6e. For a fixed core CR still bounds s from above. There
is no new global finite bound on k or t.

More precisely take the shape lower bound Mshape for L to be
the maximum of the accepted combined coefficient rank and

```
Mnew=ceil(max(0,F(v,e)))+sC+(k+s+1)binom(p,2)
     -(3t-p)(p-1),
```

with F=0 at v=0. At a minimum phase a counterexample must have

```
beta>Orest+Pplus+gain+PAplus+floor(Mshape/m).
```

MIN-PHASE restricts attention to zero residue at the origin,
a non-maximal unit or a covered pair. The accepted P6e origin
restrictions, two bad types, absent zero extensions and matching
defects still apply. Covered-pair-zero phases and shadow excess
have not been discarded.

**Next precise candidate, OPEN: MAXMATCH-RESIDUAL.** At a unit-zero
minimum phase suppose the positive bad family is paid by distinct
positive faces. Choose a maximum matching of deep bad cubics to
their quadratic faces, of size nu, and put b=beta_D-nu. Let F
be the matched faces with absent zero extension. Let Lambda_F
be the rank sum of L's coefficients after subtracting one from
each F face. The absent zero extension gives psi<=k+1, so those
face coefficients were at least s+1 and all residual coefficients
are nonnegative. Seek a maximum
matching for which

```
Lambda_F+m Orest>=sum_{z in F}(m-r(z))+m b.           (MMR)
```

At b=0 this is the existing ABSENT-ZERO proposal. If (MMR)
holds, present zero extensions pay their matched cubes and
residual mass pays absent extensions and unmatched deep cubes,
giving HC'>=0. This is an open rank/geometry inequality, not
a conclusion of the present audit. Positive families without
a face matching and covered-pair-zero phases would still need
an argument. The concentrated-shadow obstruction (11.1) points
to such a local payment or a stronger geometric moment.

The strategic decision is to retain the new packing and mass
theorems, stop the false global L>=mt shortcut, and direct the
next height-three work to overlap/window payments in this
explicitly smaller residual family.
