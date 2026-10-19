# P6e: origin phases, the two bad types, and sparse upper layers

2026-10-19. All statements marked **proved** below have analytic proofs.
Computation audits the statements and supplies the explicitly marked finite
tables; it is not used to promote a sampled assertion to a theorem.

The main new conclusions are:

* **ORIGIN-EDGE:** MaxCL at the origin, for every cubic count and every spike
  count, if at most one core unit is at most `m/2`. This includes the all-high
  origin requested in P6e(i). Also, HC' holds at the origin if at most one
  core unit is above `m/2`.
* **BAD-TWO:** at an arbitrary phase there are exactly two possible bad-cubic
  types. Their factor-unit supports are disjoint, on the two sides of `rho`.
  No bad cubic has a negative face carry or a mixture of zero and positive
  face carries. This gives explicit positive-face and zero-unit gain relays.
* **GENERAL-FEW40:** HC' at every phase for every height-three tile with
  `k >= 40t+8`, t>=2. An exact integer cutoff is given below. The proof uses
  the new height-independent linked-moment bound
  `A >= (4v^4-16v^2-12v-1)/(8(5v+4))` on the missing-pair support of size v.
* Further origin results: HC' for at most three bad cubics; the all-high
  HC' regimes HIGH-FEW, HIGH-FIVE and HIGH-MAX; a graph condition for the
  one-low-factor family; and an explicit cubic bound on the number of low
  units in a separated two-band origin configuration.

**The full height-three theorem is not proved here.** In particular,
HIGH-ORIGIN as originally formulated asks for HC', whereas ORIGIN-EDGE proves
MaxCL using the maximal-pair credits. The stronger HC' statement remains
open outside the specific regimes stated below. This distinction is
essential. There is no counterexample to HC' or MaxCL in the checks.

The earlier P6 reports are unchanged. Code and results are in `e/`.
All execution was on fejer in `~/wilf/p6e/e`, nice 10, with one thread per
job and at most three simultaneous owned computation jobs. No commits.

## 1. Exact setting and accepted input

Remove maximal-unit spikes. The core has k non-maximal units, q pairs Q,
p non-maximal pairs N2, and t cubics T. Put

```
Qk=binom(k+1,2), e=Qk-q, s=m-(1+k+q+t), d=k+s,
delta_i=k+1-sum_{z in Q}z_i, A=sum_i delta_i u_i.
```

Here `u_i=r(e_i)`, `rho=r(0)`, `nu=m-rho`,
`ell(x)=sum_i x_i u_i-(|x|-1)rho`, and `K=(ell-r)/m`.
All residues of core cells are distinct; the s missing residues are spikes.
Missing pairs have ordinary weight `u_i+u_j`, with repetitions for loops,
and A is exactly the sum of their weights. Let `a=q-p`.

We use the accepted identities

```
L = A+s sum_i u_i+sum_{z in N2}(d+2-psi(z))r(z) >=0,
HC' = L+m(Orest+Pplus+gain-beta),
S = HC'+m PAplus.                                      (W)
```

`Pplus` counts positive-carry N2 pairs, `PAplus` positive-carry maximal
pairs, and `beta` bad cubics. For a cubic y,

```
kappa_y=2K(y)-sum_i y_i K(y-e_i),
b_y=kappa_y+[r(y)>=nu],  beta=#{y:b_y=-1},
gain=sum_y max(b_y,0).
```

The cubic lift is `2ell(y)+rho=sum_i y_i ell(y-e_i)`. Pair coefficients
in L are nonnegative. We also use the accepted any-height rectangle bound:
if the missing-pair graph has support of size v, then

```
m >= k(k-v+1)+1.                                      (RECT)
```

Every criterion for S is a criterion for MaxCL at the specified phase.
An all-phase criterion gives the usual Tile-TOP''/Wilf consequence.
An origin-only criterion gives that consequence when the required phase is
the origin, for example when the conductor is divisible by m. We do not
claim an all-phase semigroup theorem from an origin-only result.

## 2. BAD-TWO: the arbitrary-phase classification

**Lemma BAD-TWO (proved).** A cubic is bad if and only if it has one of
the following two types, counting its three faces with multiplicity:

| Type | Cubic carry | Window | Face carries | Factor-unit residues |
|---|---:|---|---|---|
| A, positive | +1 | outside W | +1,+1,+1 | all strictly above rho |
| D, deep | -1 | inside W | 0,0,0 | all strictly below rho |

In particular no bad cubic mixes units from the two sides of rho.

Proof. Write the three factor copies as u,v,w in `[0,m)` and
`T=u+v+w`. A negative pair carry means, say, `u+v<rho`.
A positive pair sharing either of its factors is then impossible:
`u+w<rho+m`. Any two faces of a cubic share a factor copy. Thus positive
and negative face carries cannot coexist.

If `K(y)=-2`, then `T<2rho-m<rho`, so all three face carries are -1;
also `r(y)>=2nu>nu`, giving `b_y=-4+3+1=0`.
If `K(y)=-1`, a positive face is impossible, since
`T<2rho<rho+m`. If the cubic is outside W then `T<rho`, all faces are
negative, and `b_y=1`. Inside W, `b_y=-1` is equivalent to the face-carry
sum being zero; since all face carries are nonpositive, all are zero.
This is type D.

Suppose `K(y)=0`. A bad cubic outside W would need one positive face.
But `T<rho+m`, contradicting that face's ordinary sum being at least
`rho+m`. A bad cubic inside W would need two positive faces. Adding their
ordinary-sum inequalities gives `T+u_i>=2(rho+m)` for the shared factor.
Since `u_i<m`, this implies `T>m+2rho`, contradicting `K(y)=0`.
The only other possibility is `K(y)=1`, outside W, with all three face
carries positive. `K(y)=2` cannot be bad. These conditions also directly
give `b_y=-1`, so the classification is exact.

In type A, each factor exceeds rho because it belongs to a pair of sum
at least `m+rho` and the other factor is below m. In type D, every pair
sum is at least rho whereas `T<2rho`; subtracting the pair opposite a
factor gives that factor strictly below rho. QED.

**Corollary BAD-ARCS (proved).** With `beta_A,beta_D` the two counts,

```
r(A) in [ceil(nu/2),nu),       beta_A <= floor(nu/2),
r(D) in [m-floor(rho/2),m),    beta_D <= floor(rho/2).       (BA)
```

For A the lift says `2r=nu+sum_faces r`; for D write
`r=nu+b`, giving `sum_faces r=2b-rho>=0`.
The bounds follow by residue injectivity in the two integer arcs.
At the origin, every face residue of a bad cubic is positive (residue 0
belongs to the origin), so `r(y)>m/2`, strictly.

**Corollary DEEP-HOLES (proved).** For a deep cubic, let r be its least
face residue. Then

```
rho >= 3r+2,
2r+1 <= u_i <= rho-r-1 for every factor copy,
beta_D <= floor((rho-3r_*)/2),                            (DH)
```

where the last inequality uses any common lower bound `r_*` for all
deep-face residues. Indeed `r(y)=nu+b`, `b<=rho-1`, and
`sum_faces r=2b-rho>=3r`. Also `u_i=b-r(opposite face)<=rho-r-1`;
adding the two face-sum inequalities containing `u_i` gives
`u_i>=rho+2r-b>=2r+1`. Counting the allowed distinct b's gives the last
bound. Unlike the original ONE-DEFICIT use, this lemma does not assume
one cubic or one bad cubic.

## 3. Positive-face relays, at every phase

For the type-A family form the bipartite incidence graph to its distinct
quadratic faces. Every such face belongs to N2 and has carry +1.

**Lemma POSITIVE-RELAY (proved).** If these cubics admit an injective
choice of a face, then `Pplus>=beta_A`, and

```
HC' >= L+m(Orest+gain-beta_D).                          (PR)
```

Thus HC' holds if there is no deep cubic. Two sufficient conditions for
the injective choice, with no bound on the other cubics, are:

* at most three type-A cubics;
* all type-A cubics share a fixed factor direction i: choose `y-e_i`.

For the first assertion, any family of at most three distinct cubics has
at least as many distinct quadratic faces. With one available pair only
a pure cube can occur. With two available pairs there are at most two
cubes: a mixed cube needs a loop and an incident ordinary pair; the
remaining possibilities are pure cubes. This argument applies to every
subfamily of size at most three. The finite marriage argument gives an
injective choice: if an augmenting path fails, its reachable cubics have
fewer neighboring pairs, contrary to these inequalities. QED.

At the origin there are no deep cubics. In particular:

**ORIGIN-THREE (proved):** `beta<=3` implies HC', regardless of t.

There is a useful graph version that addresses the one-low-factor
family. At an arbitrary phase put units at least `(m+rho)/2` in the
upper part. A type-A cubic has at least two factor copies in that part:
its smallest two factors have sum at least m+rho. More generally one
may choose ANY partition for which every positive bad cubic has zero
or one factor copy in the lower part. At the origin the strict upper
part `u>m/2` has this property, since a zero-residue pair is forbidden.

For each lower direction l, form the graph F_l whose edges, including
loops, are the pairs of upper directions in bad cubics `x_l x_i x_j`.
Assume every connected component of F_l has at most as many edges as
vertices. Assign its edges injectively to incident vertices: remove
leaves inward in a tree, orient a remaining cycle consistently, and
assign a loop to its own vertex. Match `x_l x_i x_j` to the positive
face `x_l x_v` for its assigned vertex v. Different lower directions
use different faces. The all-upper bad cubics can separately be
matched to upper-upper faces.

**LOW-LINK-RELAY (proved).** If every F_l has this pseudoforest property
and the all-upper positive bad family has an injective face choice,
then POSITIVE-RELAY applies. This is a uniform sufficient condition,
not a claim that all such graphs are pseudoforests.

If all origin bad cubics have one copy of the SAME low direction,
there is an even simpler injection: remove that low copy and use the
upper-upper face. This proves HC' in that case without the pseudoforest
condition. Removing the varying low copy is not injective in general;
the minimum counterexample is recorded in section 11.

At the origin with exactly one high unit h, every bad cubic is `h^3`
or `h^2 l`. Match these respectively to `h^2` and `hl`.
Consequently **ORIGIN-ONE-HIGH (proved): HC' for every t whenever at
most one core unit exceeds m/2.**

## 4. HALF-ID: an origin identity with no bad-cubic term

This section concerns rho=0. Let

```
H=#{units u>m/2}, l=k-H, h=floor((m-1)/2), pi=m-1-2h,
q0=#{pairs K=0}, q0L=#{pairs K=0, r<=m/2},
qpH=#{pairs K=1, r>m/2}, sH=#{spikes r>m/2}.
```

Here all pairs, maximal or not, are counted. Thus pi is 1 for even m,
0 for odd m. For cubics let `nL,nH` be the neutral (`b=0`) counts below
or at m/2 and strictly above m/2; let `gL,gH` count positive-b cubics
in the two parts; and let

```
E=sum_{b_y>0}(b_y-1) >=0.
```

**Lemma HALF-ID (proved).** Exactly,

```
S/m = L/m +pi+H-l+q0-s-nL
      +2sH-2q0L+2qpH+nH+2gH+E.                        (HI)
```

Proof. Every bad cubic is strictly above m/2. The upper and lower
nonzero residue counts are

```
h = H+qH+beta+nH+gH+sH,
m-1-h = l+qL+nL+gL+sL.
```

Subtract them, use `gain=gL+gH+E`, and use
`qplus+qH-qL=q0-2q0L+2qpH`. Substitute in
`S/m=L/m+qplus+gain-beta`. This gives (HI). QED.

The lower neutral cubics are exactly these two kinds:

1. `K=0`, all faces zero, with ordinary factor sum at most m/2;
   all factors are low.
2. `K=1`, with two positive face incidences and one zero face incidence,
   with factor sum at most 3m/2. There is exactly one high factor copy
   and two low copies; both low-high faces are positive.

For kind 2, two high copies would, together with a positive cross face,
make the factor sum exceed 3m/2. No high copies would give no positive
pair, since a zero-residue pair is forbidden at the origin. This proves
the asserted classification, including the repeated-factor case.

The exact origin obstruction has therefore moved from bad cubics to
LOWER NEUTRAL cubics. A useful additional criterion, for any accepted
shape lower bound M<=L, is

```
nL <= floor(M/m)+pi+H-l+q0-s-2q0L  ==>  S>=0.           (HN)
```

The terms omitted from (HI) are nonnegative. They may be retained for
a sharper criterion. The no-wrap theorem is still needed when an
entire large lower neutral face occurs; (HN) is not asserted to pay
every such face by itself.

## 5. All-high origin: MaxCL is completely paid

**Theorem HIGH-ORIGIN-S (proved).** If every core unit exceeds m/2,
then MaxCL holds at the origin for every t. For k>=2,

```
S >= m [e+k+pi+(k-2)s/2] >0.                           (HS)
HC' >= m [e+k-a+pi+(k-2)s/2].                          (HM)
```

Proof. Every present pair has carry +1. A cubic is bad with carry 1
or has `b=1` with carry 2. There are no neutral cubics. In HALF-ID,
`l=q0=q0L=nL=nH=E=0`. Each missing pair has ordinary weight greater
than m, and `sum_units u>km/2`, so

```
L >= m(e+ks/2).
```

Dropping `2sH+2qpH+2gH` in (HI) gives (HS); subtract `m a` for (HM).
For k=1, ORIGIN-ONE-HIGH proves the stronger HC'. The flat or empty
core is covered by the accepted flat theorem. QED.

In particular **HIGH-MAX (proved)** gives HC' whenever

```
a <= e+k+pi+(k-2)s/2.                                 (HMAX)
```

This includes every all-high core without maximal pairs. It does not
establish the stronger HIGH-ORIGIN conjecture for every a.

Here are two further unconditional HC' regimes within the all-high origin.

**HIGH-FEW (proved).** HC' holds if `k>=2t`.

Proof. If it failed then, with `g=t-beta`,
`beta>p+g+e+ks/2`. For t<=1 use ORIGIN-THREE. For t>=2 a positive
s would give `ks/2>=t>=beta`, impossible. Hence s=0 and
`e<=t-p-1<=t-2`. COARSE-PACK and cardinality give

```
binom(k,2) <= 2e^2+e+t <= 2t^2-6t+6.
```

But `k>=2t` gives `binom(k,2)>=2t^2-t`; their difference is
`5t-6>0`. QED.

**HIGH-FIVE (proved).** HC' holds if `beta<=5`, for any t.

Counts up to three were covered above. First let beta=4; its positive
shadow has p>=3. If p>=4
or g>=1 the assertion is immediate. Otherwise p=3,g=0,t=4; the four
bad cubics form a full binary cubic simplex. An absent pair gives
`L>m`, as does s>=1 (k>=2). For e=s=0 COARSE-PACK forces
`binom(k,2)<=4`, so k<=3. At k=2, m=10 and the interval `(m/2,2m/3)`
has only one possible binary factor label. At k=3, m=14, the two
binary labels must be 8,9. The third all-high label w is 10,11,12 or
13. Respectively there is a collision of `8+w` with `9+9`, `2w` with
unit 8, `2w` with cubic `8+8+8`, or `9+w` with unit 8.
All are modulo 14. No case is injective.

For beta=5 the shadow has p>=4. If p>=5 or g>=1 it is paid directly;
otherwise p=4,g=0,t=5. As before, e>=1 or s>=1 pays the deficit of
one m. With e=s=0 COARSE-PACK gives `binom(k,2)<=5`, so k<=3;
k=2 has fewer than four pairs, leaving k=3,m=15. Five cubics on
four pairs contain a full binary quartet: with zero or one loop
there are at most four cubes; with at least two loops, five cubes
require their joining edge and all four binary cubes. (The possible
five-cube supports are two loops plus the joining edge and an
incident extra edge, or three loops plus a joining edge.) At m=15
the binary bad factors must be 8,9, whose cube `8^3` has the same
residue as unit 9. Thus beta=5 is excluded too. QED.

The elementary shadow fact used here is: four cubics on three pair
faces must be the full binary simplex. A triangle without loops
supports only its squarefree cubic; three loops support three pure
cubes; one loop and two ordinary edges support at most three cubes;
two loops and their joining edge give the binary simplex.

## 6. One low unit at the origin, with arbitrary covers and gains

**Theorem ORIGIN-ONE-LOW (proved).** MaxCL holds at the origin whenever
at most one core unit is at most m/2. No bound is placed on t, q, s,
or the placement of the larger units. Together with ORIGIN-ONE-HIGH,
this proves ORIGIN-EDGE.

Proof. The all-high case was proved above. Let the sole low unit be v,
and let H=k-1 be the number of high directions. If H<=1, use
ORIGIN-ONE-HIGH. Assume H>=2, and put

```
J={high u:u+v>m}, j=|J|.
```

First suppose `v>m/4`. All zero-carry pairs are strictly above m/2,
so q0L=0. A lower neutral cubic cannot be `v^3`; the only possibilities
are `v^2 u` with u in J, hence nL<=j<=H. If nL>0 the pair `v^2` is
present, so q0>=1. The right side of (HI), after dropping other
nonnegative terms, is at least

```
s(sum_units u/m-1)+H-1+q0-nL >=0.
```

Here `sum_units u/m>H/2+v/m>1`; and the last three terms are at least
H-nL when nL>0, or H-1 when nL=0.

Now suppose `v<=m/4`. Each u in J is strictly above 3m/4. For every
formal pair in Sym^2 J, a present pair contributes 2 to `2qpH`, while
an absent pair contributes more than 3/2 to A/m. For each high unit
outside J, the formal pair `{u,v}` either is present and contributes
1 to q0 (its residue is above m/2), or is absent and contributes more
than 1/2 to A/m. These are disjoint sets of formal pairs. The only
possible negative zero-pair contribution is `v^2`, worth at worst -1.
Consequently

```
A/m+q0-2q0L+2qpH >= (H-j)/2+(3/2)binom(j+1,2)-1.
```

There are at most j lower neutral cubics `v^2 u`, plus possibly `v^3`.
Thus `nL<=j+1`. Using (HI), the nonnegative N2 mass in L, and
`sum_units u/m>H/2>=1`, gives

```
S/m >= s(sum_units u/m-1)
       +(3H/2)-3+(3/4)j(j-1) >=0.
```

This includes the H=2 boundary exactly. QED.

This proof uses maximal-pair credits and proves S. It does not claim
HC' for all one-low origin configurations.

## 7. A two-band origin theorem with many low directions

**Theorem SMALL-LOW-BAND (proved).** Suppose every core unit is in
`(0,m/4]` or `(m/2,m)`. Let l be the number in the first band and H
the number in the second. Cases H<=1 are already HC'. If H>=2 and
l>=1, put

```
j=#{high u:u+max(low units)>m},
Ql=binom(l+1,2), Ul=binom(l+2,3), D=2l^2+4l-3,
P_l(H,j)=((l+2)/2)H-l-Ql-Ul+(3j^2-Dj)/4.
```

Then `S>=m P_l(H,j)`. In particular MaxCL holds whenever

```
H >= ceil(l^3/6+2l^2/3+5l/6+1-13/(8(l+2))).             (SB)
```

Proof. The j indicated high units exceed 3m/4. Their mutual pairs
give at least `(3/2)binom(j+1,2)` to A/m+2qpH, by the same
present-or-absent argument as above. The l(H-j) cross pairs with
the remaining high units are zero-carry pairs of residue above m/2
when present, and have ordinary weight above m/2 when absent.
They give at least `l(H-j)/2`. All present low-low pairs contribute
at worst `-Ql` to q0-2q0L. Lower neutral cubics number at most
`Ul+j Ql`. Finally `s(sum_units u/m-1)>=0` since H>=2.
Substitution in (HI) gives P_l exactly.

Completing the square gives `3j^2-Dj>=-D^2/12`. Therefore a sufficient
condition is

```
H >= [2/(l+2)](l+Ql+Ul+D^2/48)
  = l^3/6+2l^2/3+5l/6+1-13/(8(l+2)).
```

This proves (SB). No cubic or pair face is assumed complete. QED.

For l=2,3,4,5,6 the sufficient H are respectively 7,14,26,43,66.
For l=1 use the sharper H>=2 theorem of section 6. The exact integer-j
criterion P_l>=0 is stronger than the displayed real-square bound.

## 8. A height-independent cubic lower bound on missing-pair mass

Let v be the number of directions touched by an absent pair. There
are no absent pairs outside Sym^2 of those v directions, so the
number qD of present pairs within them is `binom(v+1,2)-e`.

**Lemma DEFECT-CUBIC (proved, any height and any phase).**

```
18A >= v(v+1)(v-3).                                    (DC)
```

Proof. The localized missing degrees have sum 2e and cap v+1.
Putting the largest weights at the smallest possible distinct
nonnegative unit residues gives

```
A >= 2e^2/(v+1)-e.                                     (8.1)
```

For completeness, if `2e=(v+1)f+r`, `0<=r<v+1`, the exact rank
bound is `(v+1)binom(f,2)+fr`. Its difference from (8.1) is
`r(v+1-r)/(2(v+1))>=0`.

All qD ordinary sums of present pairs are distinct nonnegative
integers. Their sum is `(v+1)sum_D u-A`, and `sum_D u<=A`
since every localized missing degree is at least 1. Hence

```
A >= binom(qD,2)/v.                                    (8.2)
```

For v<=3 the asserted lower bound is nonpositive or zero. For v>=4,
split at `e0=v(v+1)/6`. If e>=e0, (8.1) is increasing and gives
`A>=v(v+1)(v-3)/18`. If e<e0, then `qD>v(v+1)/3`; (8.2) gives

```
A >= (v+1)(v(v+1)-3)/18
  = v(v+1)(v-3)/18+(v+1)(4v-3)/18.
```

This is stronger. The proof uses only pair-residue injectivity and
distinct unit residues, and so is independent of the height. QED.

### 8.1. LINKED-CUBIC: retaining the degree-minus-one mass

The two separate lower bounds above lose information. Retaining their
link gives the following stronger result, also height-independent.

**Lemma LINKED-CUBIC (proved).** For v>=1 put

```
R(v)=(4v^4-16v^2-12v-1)/(8(5v+4)).
```

Then A>=R(v), and in particular

```
10A >= v(v+1)(v-3).                                    (LC10)
```

Proof. Write `W=sum_D u`, `X=2e-v>=0`, and `E=A-W`.
The nonnegative weights `delta_i-1` have sum X and cap v, hence
`E>=X^2/(2v)-X/2` by the same rank argument. The distinct present
pair sums give

```
vA >= binom(qD,2)+(v+1)E,
qD=v(v+1)/2-e.
```

Completing the resulting quadratic in e gives exactly

```
[binom(qD,2)+(v+1)(X^2/(2v)-X/2)]/v
 = R(v)+(5v+4)/(2v^2)
          [e-v(v^2+7v+5)/(2(5v+4))]^2.                  (LC)
```

This proves the bound. For v>=1, the difference between R(v) and
`v(v+1)(v-3)/10` has numerator
`48v^3+24v^2-24v-10>0` over `80(5v+4)`; for v=0 use A>=0.
This gives (LC10). Also R is increasing on positive integers:
the numerator of `R(v+1)-R(v)`, over `8(5v+4)(5v+9)`, is

```
60v^4+184v^3+96v^2-124v-91
 =60x^4+424x^3+1008x^2+860x+125,   x=v-1>=0.
```

These explicit identities make the rounding and monotonicity steps
below mechanical. QED.

## 9. Sparse upper layers, all phases; exact moment cutoffs

The final threshold is GENERAL-FEW40 in section 9.1. The coarser
80t and 72t+10 certificates are retained as independent checks using
the simpler unlinked moment (DC).

**Theorem GENERAL-FEW80 (proved).** Every height-three tile with
`t>=2` and `k>=80t` satisfies HC' at every phase.

Proof. Suppose HC'<0. WINDOW-ID gives `L<mt`. The unit spike part
gives `L>=s binom(k,2)`. Put `C=binom(k,2)` and
`M0=binom(k+2,2)=1+k+Qk`. Cardinality gives

```
m=M0-e+t+s <=M0+t+s,
s(C-t)<t(M0+t).                                       (9.1)
```

Since `k>=80t>=160`, `M0+t<2(C-t)`, hence s<2t. Thus

```
m<M0+3t <= k^2/2+(123/80)k+1 <=(51/100)k^2.             (9.2)
```

The last inequality follows, at `k=160+x`, from

```
k^2/100-(123/80)k-1 =9+(133/80)x+x^2/100 >0.
```

By RECT and the first bound in (9.2),

```
v >= k+1-(m-1)/k > k/2-43/80,
```

so the integer v is at least floor(k/2). DEFECT-CUBIC now gives

```
A >= (k^2-1)(k-7)/144 >= (19/2880)k^3.
```

For the last comparison, for k>=160 use
`k^2-1>=(159/160)k^2` and `k-7>=(153/160)k`;
their product factor `24327/25600` exceeds `19/20`.
But (9.2) and t<=k/80 give

```
mt <(51/8000)k^3 <(19/2880)k^3,
19/2880-51/8000=1/4500.
```

This contradicts `A<=L<mt`. QED.

This first bound is a uniform theorem for defective Q, rather than the
earlier full-Q few-cubic theorem. The following refinement reaches the
limiting coefficient of this particular moment argument.

Here is the stronger exact form, useful without rounding to 80.
If C>t define

```
smax=floor((t(M0+t)-1)/(C-t)),
mmax=M0+t+smax,
vmin=max(0,k+1-floor((mmax-1)/k)).
```

**EXACT-FEW (proved).** HC' holds if

```
vmin>=3,  vmin(vmin+1)(vmin-3)>=18 mmax t.               (EF)
```

Indeed (9.1) forces s<=smax, hence m<=mmax and v>=vmin.
The cubic in (DC) is increasing for v>=3, giving a contradiction
to L<mt. This proves the formula with no finite-domain assumption.

**Theorem GENERAL-FEW72 (proved).** For every t>=2, HC' holds at every
phase whenever `k>=72t+10`. Criterion (EF) closes all these k and
fails at `k=72t+9` for every t>=2. The latter is a statement about
the numerical criterion, not the existence of a tile.

Proof. Suppose HC'<0 and write `k=72t+10+y`, y>=0. Then

```
C-2kt-2t^2-2t
 =2446t^2+662t+45+(140t+19)y/2+y^2/2 >0.
```

It follows from (9.1) that s<=t: if s>=t+1, then
`s(C-t)>= (t+1)(C-t)>t(M0+t)`. In fact the exact smax in (EF)
equals t, since `t(2k+1+2t)>=1` also gives smax>=t.
Consequently `m<=M0+2t`. Writing `n=floor(k/2)` and using k>4t
in RECT gives `v>=n`. For the even case the relevant floor is
`floor((mmax-1)/k)<=n+1`, and for the odd case it is at most n+2.
Also `n>=36t+5` and

```
m <= (n+1)(2n+3)+2t.
```

The cubic moment gives `18A>=n(n+1)(n-3)`. Set `x=n-36t-5>=0`.
The difference between this last lower bound and 18t times the
upper bound for m is exactly

```
612t^2+468t+60 +(1296t^2+486t+52)x
                    +(72t+13)x^2+x^3 >0.              (FP72)
```

This contradicts A<=L<mt. This proves the all-k assertion and also
that (EF) closes it. At `k=72t+9`, smax=t, vmin=36t+4, and the
same exact difference is `-684t^2+54t+20<0`. Thus (EF) fails there.
QED.

For t=2,3,4,5,6 the sufficient thresholds are 154,226,298,370,442.
The finite t=2..20 table in the code first suggested the formula;
(FP72) proves it for every t. The constant 72 is specific to the
two lower bounds optimized in DEFECT-CUBIC and is not claimed optimal
for actual tiles.

### 9.1. GENERAL-FEW40 from the linked moment

In the same integer definitions smax,mmax,vmin, replace the last
inequality of (EF) by

```
vmin>=1,
4vmin^4-16vmin^2-12vmin-1
      >=8(5vmin+4)mmax t.                              (EF-L)
```

This **EXACT-FEW-LINKED** criterion proves HC' by (LC) and the integer
monotonicity of R, exactly as (EF) did with the weaker moment.

**Theorem GENERAL-FEW40 (proved).** For every t>=2, every phase of
every height-three tile with `k>=40t+8` satisfies HC'. Criterion
(EF-L) closes all these k and fails at `k=40t+7` for every t>=2.

Proof. If HC'<0, (9.1) still holds. Write k=40t+8+y, y>=0. Then

```
C-2kt-2t^2-2t
 =718t^2+282t+28+(76t+15)y/2+y^2/2 >0.
```

As before this forces s<=t and in fact smax=t. Set `n=floor(k/2)`.
The parity calculation using k>4t gives v>=n, n>=20t+4, and
`m<=M0+2t<=(n+1)(2n+3)+2t`. Thus A>=R(n). Put x=n-20t-4>=0.
The numerator of

```
R(n)-t[(n+1)(2n+3)+2t]
```

over its positive denominator `8(5n+4)` is exactly

```
20800t^3+22176t^2+7120t+719
 +(32000t^3+27760t^2+8488t+884)x
 +(4800t^2+2616t+368)x^2+(240t+64)x^3+4x^4 >0.            (FP40)
```

This contradicts A<=L<mt and proves HC'. At k=40t+7, smax=t,
vmin=20t+3, and the exact numerator is

```
-11200t^3-784t^2+1008t+143 <0.
```

The last inequality already holds for t>=1. This proves the failure
of this numerical criterion at that endpoint; it asserts no actual
counterexample there. QED.

The sufficient all-k thresholds are now 88,128,168,208,248 for
t=2,3,4,5,6. The asymptotic constant 40 comes from keeping the
linked degree-minus-one mass: `R(v)~v^3/10`, with v about k/2.
It is a constant of this relaxation, not a proposed sharp threshold
for actual tiles.

## 10. Zero-unit relays and the exact general-phase gap

At a phase with unit direction a of residue zero, no bad cubic uses a:
type A factors exceed rho, and type D factors are at least 1 by (DH).

**Lemma ZERO-EXTENSION (proved).** Let z be a face of a deep bad cubic.
If `z+e_a` is present, it has `b=1`. Distinct z give distinct gain cubics.
For a face z of a positive bad cubic, the present extension has

```
b(z+e_a) = [r(z)>=rho].                                (ZE)
```

Proof. For a deep face, its two factors are below rho and `K(z)=0`,
`r(z)<rho`. The other two faces of `z+e_a` have carry -1, its cubic
carry is -1, and its residue is `nu+r(z)` in W. Thus kappa=0 and b=1.
For a positive face its factors exceed rho; the other faces have
carry zero. The extension has carry 0 or 1 according as r(z)<rho
or r(z)>=rho. In the first case it lies in W and has b=0;
in the second it is outside W and has b=1. QED.

Thus there is an actual injective relay for every positive bad family
with a face matching and every deep bad family matchable to faces
whose zero extensions are present. The positive family uses Pplus;
the deep family uses the distinct b=1 cubics just constructed. The
resources are disjoint. Under these two matching hypotheses HC'>=L.
The usual common-factor condition suffices for each face matching.

There is also a weighted version. Suppose the positive family has
been paid by a face matching, and choose an injective face f(y) for
the deep family. Let F consist of the chosen faces with absent zero
extension. Each z in F has coefficient `d+2-psi(z)>=s+1>=1` in L.
Set `L_F=L-sum_{z in F}r(z)>=0`. Then

```
HC' >= L_F +m Orest-sum_{z in F}(m-r(z)).                 (ZW)
```

Present zero extensions pay the other deep cubes by (ZE); subtract
one coefficient from each distinct absent-extension face in L to get
the formula. Any rank lower bound for the remaining nonnegative
coefficients may replace L_F. Concretely, sort the unit coefficients
`s+delta_i` and the N2 coefficients after these decrements in decreasing
order w_j; then `L_F>=sum_{j>=0}j w_j`. This makes (ZW) a checkable
criterion with a fractional cost `m-r(z)` per remaining relay.

These are sufficient conditions; they do not assert face matchings
for dense cubic families. The first obstruction is already the four
binary cubics on three faces. The remaining deep problem is to pay
both the cost of absent zero extensions in (ZW) and genuine shadow
excess by L and Orest after the available gains have been used.
Positive families with shadow excess can also remain, outside the
origin regimes proved above. A full face matching alone is not being
claimed sufficient for HC'; its absent-extension mass must still
pass the displayed criterion.

By MIN-PHASE, for an all-phase MaxCL proof it suffices to consider a
zero residue at the origin, a non-maximal unit, or an N2 pair. The
unit-zero phases have the relays above; pair-zero phases, unpaid
absent extensions, and shadow-excess families remain. This is an exact further reduction,
not a claim that all minimum phases are unit-zero.

## 11. Rejected claims and minimum counterexamples

All examples below are actual injectively labelled down-sets, completed
by spikes. Tuple notation names factor directions, starting at 0.
The minimum statements refer to the stated claims/shapes, with the
small-modulus exhaustive searches in `algebra.py`; forced collisions
cannot be repaired by adding optional cells.

**F1: beta<=Pplus at the origin.** False. The minimum binary example
is m=14, U=(8,9), all three pairs and all four binary cubics. It has
beta=4, Pplus=3, s=4, L=104, S=HC'=90. For m<10 the forced core
has too many cells; at m=10,12 there is only one possible binary
factor in `(m/2,2m/3)`, and at m=11,13 the two possible factors have
a cubic/unit collision. This is also the smallest counterexample
to the general inequality: p<=2 cannot fail; with p=3 one needs
the binary quartet; with p=4 and m<=13 one needs five cubics on four
pairs, which contains the binary quartet; p>=5 requires at least
15 core cells. This preserves the need for fractional L mass.

**F2: removing the low factor always gives an injective bad-cube relay.**
False. Minimum m=12, U=(8,5,6),

```
Q={00,01,02}, T={001,002}.
```

Both bad cubes remove to 00. Their pair labels are 4,1,2 and their
cubic labels 9,10. With a non-loop common high-high face, two distinct
low directions force at least 12 cells. With a loop, the search
exhausts every high label and pair of low labels at m<12.
Both low factors can be strictly below m/2 at the same minimum m:
take U=(9,4,5) with the same Q,T; the pairs have residues 6,1,2 and
the cubics 10,11.

**F3: every low-link graph is a pseudoforest.** False. Minimum m=14,
U=(8,10,7),

```
Q={00,01,11,02,12}, T={002,012,112}.
```

The single low link has the two loops and their joining edge: three
edges on two vertices. If the low factor is required STRICTLY below
m/2, the minimum in this forced shape is m=16, U=(10,12,7), with
the same Q,T. A denser link on at least three vertices already
requires at least 16 cells. Neither example violates HC'; the
upper-upper faces supply additional relay capacity.

**F4: a zero-unit extension of any bad face is a gain.** False;
the correct distinction is (ZE). Minimum m=7, rho=2, U=(0,5),

```
Q={01,11}, T={011,111}.
```

The pure cube 111 is positive bad, its face 11 has residue 1<rho,
and 011 has b=0, not a gain. Core residues are all seven residues:
origin 2, units 0,5, pairs 3,1, cubics 6,4. Here L=6, HC'=S=13.
The forced origin, two units, two pairs and two cubics require m>=7.

The stronger count-only all-high proposal
`2(e+p+gain-beta)+ks>=0` and the stronger payment that discards
all gains were tested but not refuted in the origin sample. They
remain **unproved observations**, and are not inputs to any theorem.
The still stronger sampled predicate `L/m+p>=2beta` was likewise
not refuted; the source preserves it as a diagnostic only.

**F5: six cubes on five faces must contain a binary quartet.** False.
This tempting continuation of HIGH-FIVE stops here. The minimum
shadow parameters are three directions and five pairs:

```
Q={00,11,22,01,02},
T={111,222,001,011,002,022}.
```

The cube 000 is absent, so neither binary quartet is complete.
This is realizable with all six cubics bad: the minimum modulus
for this forced all-high/all-bad shape is m=23, U=(14,13,15).
Pair residues are 5,3,7,4,6 and cubic residues, in the listed order,
are 16,22,18,17,20,21. Exhaustive label search below 23 is in
`algebra.py`. The smallest monomial parameters follow because
two directions have at most four cubes and four pairs have at most
five. This is a counterexample to the containment claim, not to HC'.

**F6: residue 1 can never be a factor of a deep bad cubic.** False
without ONE-DEFICIT's additional hypotheses. Minimum m=4, rho=2,
U=(1), Q={00}, T={000}. The cell residues are 2,1,0,3, in degree
order. The cubic is deep, its least face residue is 0, and
L=HC'=S=0; it is paid by Orest=1. This is the tile of <4,7> at
sigma=2. Four cells are necessary for height three. DEEP-HOLES
correctly allows a factor 1 when r=0; it excludes only residue 0.

## 12. Computational checks and reproducibility

All exact arithmetic used Python 3.12.3 and its standard library.
The scripts import the accepted `d/core.py` evaluator but compute
the new quantities independently of the report formulas they assert.
Every generated core is checked for down-closure, active core
directions, distinct cell residues, and nonnegative spike count.

1. `origin_probe.py`, seed 2026101972, 12,000 proposals, m=12..500,
   at most 18 candidate unit directions. Pools alternate narrow-high,
   all-high, unrestricted and middle-band; pairs are greedily selected
   with residue injectivity, and half the runs prioritize bad cubics.
   There are 11,629 actual cores, 11,517 with t>=2, 6,099 all-high
   origins, and 365,714 bad cubics. No target failure; minimum sampled
   HC'=87. This is sampling, not an exhaustive theorem.
2. `verify.py`, seed 2026101973, 3,500 proposals plus the eight mandatory
   stress cores and E47/E51. It checks every phase of every retained
   core. Pools target all-high, one-low, two-band, one-high and arbitrary
   units. It asserts BAD-TWO, BAD-ARCS, DEEP-HOLES, HALF-ID, the lower
   neutral classification, the quantitative one-low proof bounds,
   SMALL-LOW-BAND, DEFECT-CUBIC, LINKED-CUBIC and the applicable payment implications.
   Full final counts are in `e/results/verify.json`.
   There are 3,207 retained cores and 237,948 phases; 1,574 origins
   have at most one low unit (606 all-high and 968 exactly one-low),
   and 875 have at most one high unit. There are 386,428 deep-bad
   and 214,487 positive-bad cubic occurrences. The zero-extension
   identities are checked on 6,584 deep faces and 6,841 positive
   faces with present extensions. No failure; minimum HC'=S=26.
3. `algebra.py` checks all local cubic triples, including repeated
   factor copies and non-injective local configurations, for m=2..36,
   every rho and every unordered triple of unit residues. Exactly
   2,385,278 cases: 61,971 type A, 54,390 type D, and no other bad type.
   It verifies the rational identities in DEFECT-CUBIC, the 80t margin,
   the two-band polynomial, the exact t=2..20 cutoffs, the positive
   coefficient identities (FP72), and the minimum
   forced-shape counterexamples above. These finite algebra audits
   supplement the symbolic derivations; they do not replace them.
   The (FP72) integer identities and both cutoff endpoints are
   additionally checked for every t=2..400 and x=0..25.
   The linked completion of the square is checked for every v=1..80
   and every admissible e. The (FP40) identities and both endpoints
   are checked for t=2..400 and x=0..25; the finite linked-cutoff
   table covers t=2..20 as an additional audit.
4. `few_actual.py`, seed 2026101974, constructs qualifying large-k
   examples with t=2..5 and k=40t+8,72t+10,80t. At the prescribed
   phase all t cubics are pure deep bad. For the fixed units and forced
   faces it includes one maximal pair of greatest ordinary sum per
   available residue, minimizing L among such pair choices. It checks
   twelve phases per tile, including the prescribed phase. Full data
   and exact slacks are in `e/results/few_actual.json`. These stress
   the several-deep-bad theorem but do not certify every labeling.
5. `relay_check.py`, seed 2026101975, 1,200 proposals plus the eight
   stress cores, explicitly constructs maximum face matchings at
   every unit-zero phase. It checks both disjoint relay resources,
   the coefficient reservation in (ZW), and its rank lower bound.
   Full counts and actual deep shadow-excess stress examples are in
   `e/results/relay_check.json`.
   It checks 7,649 unit-zero phases. Complete disjoint relays occur
   6,107 times, including 747 with deep bad cubics. Both full face
   matchings exist in 7,546 cases, and all 7,546 pass the weighted
   rank criterion. The latter is an observation, not a theorem that
   a face matching always suffices. A stress obstruction is the
   sixth mandatory core at sigma=1: m=26, beta_D=4 on three deep
   faces, no present zero extension, HC'=S=318. It demonstrates a
   genuine matching defect; its numerical slack is positive and it
   is not a remaining numerical counterexample.

The eight mandatory stress minima remain, in file order,

```
61,135,84,82,145,171,451,267.
```

Every phase of both E47/E51 is included; no strong MaxCL or HC'
violation was found. These stress tests are not assertions that a
single new criterion closes their shape for all labelings.

Reproduce on fejer, from `~/wilf/p6e/e`, after copying `d/core.py` to
the sibling `d/` directory:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python origin_probe.py --trials 12000 --output results/origin_probe.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python verify.py --trials 3500 --output results/verify.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python algebra.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python few_actual.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python relay_check.py
```

All sources and output logs are retained. There is no new exhaustive
enumeration of all tiles at any unbounded parameter.

## 13. Height H, in brief

DIFF-CENSUS, COARSE-PACK, WP/WP2, RECT and both defect moments are literally
height-independent: they use only units and quadratic residue
injectivity. Under WINDOW-H put
`B=sum_{j>=3}(j-2)|C_j|` and `T=sum_{j>=3}|C_j|<=B`.
Then `HC_H>=L_H-mB`, `L_H>=A+s binom(k,2)`, and
`m=M0-e+T+s<=M0-e+B+s`. The entire section 9 proof applies with B in
place of t. Thus **H-FEW40 (proved): k>=40B+8, B>=2, implies HC_H
at every phase** (B=0 is flat and B=1 is ONE-CUBIC).
By contrast BAD-TWO, HALF-ID and the origin one-low argument use the
height-three carry classification. BAD-NARROW's empty arcs can be
occupied by higher cells, and its negative-cell count must be replaced
by the weighted `(j-2)` loss. We do not claim its unchanged higher-height
version. The accepted WINDOW-H identities, including the quartic lift
`3ell+rho`, remain the exact starting point.

## 14. Status, exact residual family, and next lemma

**Proved:** the analytic results above, including all-high and one-low
origin MaxCL for arbitrary t, the two bad types with disjoint unit
supports, and an all-phase/all-height sparse-upper-layer theorem.
**Finite audits:** the explicitly bounded exact cutoff and local-case
tables; the final cutoff formula has the analytic proof (FP40).
**Observed:** the stronger count-only all-high
payments and sampled HC' positivity. No conditional packing assertion
is used.

The remaining possible height-three MaxCL counterexample must have
`k>=5`, `d>=6`, `t>=2`, fail the accepted earlier criteria, fail
EXACT-FEW-LINKED (in particular k<40t+8), and at a minimum phase have

```
beta_A+beta_D > Orest+Pplus+gain+PAplus+floor(M_shape/m).
```

Here M_shape may be enlarged by
`ceil(max(0,R(v)))+s binom(k,2)+Gamma` (set R(0)=0), where Gamma is
the pair-coefficient rank bound. At rho=0 it further
requires at least two high and at least two low core units, beta>=4,
and failure of (HN). In the two-band case it must also have
`P_l(H,j)<0`; in particular H is below (SB). At positive rho the only
bad cells are exactly A and D above. The positive-face and zero-gain
matching criteria close the stated subfamilies. The precise unit-zero
residual consists of positive face-matching defects, genuine deep
face-matching defects, or absent zero extensions failing the weighted
rank criterion (ZW). Pair-zero minimum phases remain separately.
The origin branch with one low FACTOR per bad cube but several
possible low DIRECTIONS is closed only in the common-low and
LOW-LINK subfamilies proved above. It is not being identified with
ORIGIN-ONE-LOW, which has only one low unit direction in the entire core.

The original HC' HIGH-ORIGIN frontier is separately delimited:
`a>e+k+pi+(k-2)s/2`, `k<2t`, `beta>=6`, and failure of the other
accepted HC' criteria. Its MaxCL assertion is already proved here.

**Next precise lemma, ABSENT-ZERO (conjectured, not an input):** at a
unit-zero minimum phase suppose both bad families have full face
matchings, with the positive one using positive faces. For some
injective face choice f of the deep family, let F and Lambda_F be
the absent-extension faces and the residual rank bound in section 10.
Prove

```
Lambda_F+m Orest >= sum_{z in F}(m-r(z)).
```

It is precise, purely checkable, and passed every qualifying phase
in the relay audit, but it is not proved universally. A counterexample
would refute this rank lemma without necessarily refuting HC'. After
that, genuine deep shadow excess (already four binary cubics on three
faces) requires residue packing beyond a face injection. Positive
shadow excess at non-origin phases and pair-zero minimum phases are
the other explicit gaps. These are not removed by the origin theorem
or by the sparse-layer theorem.

The strategic decision is to retain the linked moment as the sparse-layer
certificate and stop refining its lower-order cutoff. It does not reach
the middle regime t of cubic order in k. The next work should test or
prove ABSENT-ZERO, then spend residue packing on actual matching excess;
enumerating one more dimension would not address those two mechanisms.
