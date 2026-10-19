# P5: the upper-unit primary regime

Status: **T1 and T1s are proved on paper, uniformly in all parameters.**
The B-heavy part uses the degree-two condensed Macaulay inequality and
an explicit positive-coefficient polynomial. There is no finite
certificate dependency in the proof. T2 is not proved in full; section
9 gives a new adaptive arc and a uniform quantitative reduction using
LC. All computation described here was executed on fejer, in
`~/wilf/p5`, with `nice`, using at most four concurrent single-core
jobs. No commits were made.

## 1. Exact theorem and conventions

Use the P4 multiplicity hypotheses: `D` is a finite down-set in
`N^d`, every direction is active, `m=|D|`, all active integer weights
`n_j>m`, and the map `x -> x.n mod m` is bijective on `D`. Write
`M=max_D x.n`, and suppose `4m<=M<5m`. Put

```
rho=5m-1-M, h=m-rho,
I_j=[jm-rho,(j+1)m-rho),
g=sum_D floor(x.n/m), ell=sum_D floor((M-x.n)/m), W=d ell-g.
```

The unit classes A,B,C,E have sizes `a,b,c,e`; `c` in the algebra
below counts C directions, rather than denoting a conductor. For a
cell of total degree j, write its value as `jm+tau` and put
`t_j=n_j-m`. The unit tau ranges are

```
A: [1,h), B: [h,h+m), C: [h+m,h+2m), E: [h+2m,h+3m).
```

**Theorem P5.** Suppose every A direction satisfies `2t_j>=h`.
If `a>=1`, then

```
W >= (a-1)(b+1)
     + c(c+e+1) + e(3a+2b-1)
     + (c+e)(q3+s3+t3).                                  (P5)
```

If `a=0`, then

```
W >= c(c+1)+e(2b+c)+(c+e)t3 >= 0.                         (P5.0)
```

In particular, P4 holds under the upper-unit hypothesis for every
`a,b,c,e`. The proof below also gives a larger C coefficient in the
region covered by the arc-only certificate.

Dependencies checked against the project record: GW-21's band
identity, weighted shadows, and joint short-residue lemma; GW-24's LC
only for the stretch result; and the degree-two condensed Macaulay
theorem. The proof of P5 does not use GW-24's finite certificates or
any packing lemma.

## 2. Arc verification, including endpoints

Under the upper-unit hypothesis, `q2=u3=k=v2=0`. Indeed the tau of
an AA cell is at least h; that of an AAA cell is at least `3h/2>h-1`;
and that of a quartic is at least `2h>h-1`, whereas every quartic in
D has tau at most `h-1`.

Put `theta=ceil(3h/2)` and take integer residues in

```
Y=[h,min(theta,m)) union [1,theta-m).
```

An empty interval contributes nothing. If `theta<=m`, its cardinality
is `theta-h`. If `theta>m`, its cardinality is `theta-h-1`, including
the case `theta=m+1`, where the second interval is empty. Consequently
`|Y|>=h/2-1`. The low interval and high interval are disjoint, and
neither contains zero.

Here is a full exclusion check. Every cubic has
`theta<=tau<=m+h-1<2m`. Before reduction modulo m it misses the high
arc; after wrapping it misses the low arc, because its tau is at least
theta. Its wrapped residue is below h and therefore misses the high
arc as well. An A unit misses the high interval since `t<h`; it misses
the low interval since `theta-m<=ceil(h/2)<=t`. An AC or BC cell has

```
m+theta <= tau <= 2m+h-1.
```

After either one or two wraps this interval misses Y: one-wrap
residues are at least theta, and two-wrap residues are below h and,
when the low arc exists, at least `theta-m`. There are no other
quadratic types except AA,AB,BB, and there are no quartics.

An AB or BB cell has `tau>=theta`. To occupy the high part of Y it
must have `m+h<=tau<m+theta`; to occupy the low part it must have
`2m+1<=tau<m+theta`. Both imply `tau>=m+h`, so these cells are in I4.
AA cells are all in I3. Thus every residue of Y is occupied by an
I3 AA cell, a B/C/E unit, an I4 AB cell, or an I4 BB cell. Bijectivity
gives

```
h <= 2(q3+b+c+e+s4+t4)+2.                                (ARC)
```

This verifies the refined arc lemma for arbitrary residue-complete
down-sets, not just semigroup tiles. GW-25a's conductor-interval
argument and GW-25's pure-A proof also check out; the argument above
is the refined form needed here.

## 3. A single exact identity that pays for C and E

Abbreviate

```
q=q3, u=u4, s=s3, S=s4, t=t3, T=t4,
H=number of AC cells, I=number of BC cells,
v=v3, w=w, z=z,
Q=a(a+1)/2, B=b(b+1)/2, Z=b(b+1)(b+2)/6,
A0=a(a+1)(a-1)/6, r=c+e.
```

All these counts are nonnegative. The bounds used are exactly

```
q<=Q, 3u<=(a+2)q,
s+S<=ab, t+T<=B, H<=ac, I<=bc,
v<=bq, 2v<=(a+1)s,
w<=at, 2w<=(b+1)s, 3z<=(b+2)t,
rho>=t+I+v+w+z.                                         (SR)
```

Define two nonnegative residue slacks

```
SRslack=rho-t-I-v-w-z,
ARCslack=rho-[a-b-c-e-1-q+u+s-S+H+t-T+I+v+w+z].
```

The second is ARC after using `m=1+d+N`. For `0<=lambda<=1` set

```
C_lambda=3a(a+1)+ab+lambda(a-b-1-ab-B),
k_lambda=b-(a+17)/3+lambda(a-1)/3,
j_lambda=a+b+1+2lambda,
l_lambda=a+b+2+lambda,
G_lambda=c[1+r+lambda(a-1)]+e[3a+2b-lambda]+r(q+s+t).
```

Direct expansion of GW-21 identity (1) gives the following exact
identity, which is also a compact symbolic verification of the
reduction:

```
W = C_lambda+k_lambda q+j_lambda s+l_lambda t-3(v+w+z)+G_lambda
  + (4-lambda)/3 [(a+2)q-3u]
  + (4+lambda)[ab-s-S+B-t-T]
  + (4-lambda)(ac-H)+3(bc-I)
  + (1-lambda)SRslack+lambda ARCslack.                    (ID)
```

For `a>=1` all terms after the first line are nonnegative, and

```
G_lambda >= G := c(c+e+1)+e(3a+2b-1)+r(q+s+t).             (G)
```

Indeed `G_lambda-G=lambda c(a-1)+(1-lambda)e>=0`.
Thus every A/B certificate below automatically extends to all C/E
counts, with exactly the claimed explicit positive terms.

## 4. Region I: a linear arc certificate

Assume `a>=2` and

```
b<=a^2-a-1,
b(2a+b+1)<=6a(a+1).                                    (R1)
```

In particular these hold for `a>=3, 0<=b<=a+1`, and for
`a=2, b=0,1`.

Use lambda=1 in ID, and put

```
mu=(a^2-a-b-1)/(a(a+1)), nu=(3-mu)/2,
mu'=(a+1)/a, nu'=(2a-1)/(2a),
kappa=b(2a+b+1)/(a(a+1))-6.
```

All `mu,nu,mu',nu',-kappa` are nonnegative in R1. The following
identities verify every variable coefficient symbolically:

```
mu+2nu=3, mu'+2nu'=3,
nu(a+1)+nu'(b+1)=a+b+3,
mu'a+(b+2)=a+b+3,
b-6-mu b=kappa,
C_1+kappa Q=(a-1)(b+1).                                (LIN)
```

Consequently the first line of ID, with G_1 removed, is exactly

```
(a-1)(b+1)
 + (-kappa)(Q-q)
 + mu(bq-v)+nu((a+1)s-2v)
 + mu'(at-w)+nu'((b+1)s-2w)
 + ((b+2)t-3z).
```

Together with the remaining slacks in ID this is the requested
explicit dual certificate. In the original list of constraints its
multipliers are 5 on both mixed quadratic capacities, 1 on the AAA
and BBB weighted shadows, the four displayed multipliers on the
mixed cubic shadows, `-kappa` on `q<=Q`, 3 on the AC and BC
capacities, and 1 on ARC. It proves the stronger bound

```
W >= (a-1)(b+1)+G_1.
```

For completeness, R1's signs follow without finite checking. Its
first inequality gives mu>=0; mu<=1, hence nu>=1. The second gives
kappa<=0. If `a>=3,b<=a+1`, then
`a+1<=a^2-a-1` and `(a+1)(3a+2)<=6a(a+1)`.

## 5. The B-face curvature inequality

The B units, I3 BB cells, and BBB cells form a multicomplex: every
BB divisor of a BBB cell lies in I3, by the same divisor-band
calculation used in GW-21. Its degree-two and degree-three counts
are t and z.

The precise external theorem used is condensed Macaulay: if a finite
multicomplex has degree-two count `t=binom(x+1,2)`, with real `x>=0`,
then its degree-three count is at most `binom(x+2,3)`. This is
[Eliahou, Theorem 5.10](https://ems.press/content/serial-article-files/32312),
applied at degree two to the monomial quotient with this standard
monomial set. The case t=0 gives z=0 directly. Thus

```
z <= F(t):= t(sqrt(8t+1)+3)/6.
```

Since `0<=t<=B` and `sqrt(8B+1)=2b+1`, rationalizing gives

```
3[Zt/B-F(t)]
 = 4t(B-t)/(2b+1+sqrt(8t+1))
 >= 2t(B-t)/(2b+1).                                    (MC)
```

Equivalently,

```
3z <= (b+2)t-2t(B-t)/(2b+1).
```

This rational quadratic inequality is the only consequence of
Macaulay needed below. It captures a curvature term lost by the
linear shadow `3z<=(b+2)t`.

## 6. Region II: endpoint certificates and an analytic bridge

This region consists of

```
a>=2, b>=a+2,
and the two additional points (a,b)=(2,2),(2,3).          (R2)
```

For lambda=0 and lambda=1 separately define

```
alpha_lambda=max(-k_lambda,0),
mu_lambda=max(k_lambda,0)/b,
nu_lambda=(3-mu_lambda)/2,
eta_lambda=[j_lambda-nu_lambda(a+1)]/(b+1),
chi_lambda=3-2eta_lambda,
C'_lambda=C_lambda-alpha_lambda Q,
K_lambda=l_lambda-a chi_lambda.
```

These are explicit rational dual certificates for every fixed t;
they use MC for z. Their nonzero multipliers beyond ID are alpha
on `q<=Q`, mu on `v<=bq`, nu on `2v<=(a+1)s`, chi on `w<=at`, and
eta on `2w<=(b+1)s`. The symbolic coefficient checks are

```
k_lambda=mu_lambda b-alpha_lambda,
mu_lambda+2nu_lambda=3,
chi_lambda+2eta_lambda=3,
nu_lambda(a+1)+eta_lambda(b+1)=j_lambda.
```

Hence ID implies

```
W >= C'_lambda+K_lambda t-3z+G_lambda.                    (END)
```

All multipliers are nonnegative. On `b>=a+2`, one has
`0<=mu_lambda<=1`, `1<=nu_lambda<=3/2`, and

```
0 < b-(a+1)/2 <= j_lambda-nu_lambda(a+1) <= b+2.
```

Since `b>=4` here, the upper bound gives eta<=3/2 and chi>=0.
At `(2,2),(2,3)` these signs follow directly from the displayed
formulas (mu=0 at both endpoints). No division by zero occurs in R2.

Write `w0=(a-1)(b+1)`. Direct substitution gives the two endpoint
identities

```
C'_0+K_0 B-3Z=-A0,
C'_1+K_1 B-3Z=w0.                                      (EP)
```

These can also be verified by substituting the full counts
`q=Q,u=binom(a+2,3),s=ab,t=B,v=bQ,w=aB,z=Z`: every shadow used
in END is an equality, the SR evaluation is `-A0` by the transfer
identity, and the ARC evaluation is `w0` by LIN. This is an algebraic
evaluation, with no assumption that the full count vector is an
actual tile.

Put `x=t/B` and `D0=2B^2/(2b+1)`. END, EP, and MC give

```
W-G >= f0(x):=C'_0(1-x)-A0 x+D0 x(1-x),
W-G >= f1(x):=C'_1(1-x)+w0 x+D0 x(1-x).                  (BR)
```

It remains to check a parameter inequality, not an optimization over
integer t:

```
C'_0>w0,
D0(C'_0-w0) >= (w0-C'_1)(C'_0+A0).                      (S)
```

Here is the analytic bridge. If `C'_1>=w0`, f1>=w0 throughout
`[0,1]`. Otherwise put `x0=(w0-C'_1)/D0`. Inequality S implies

```
0<x0 <= (C'_0-w0)/(C'_0+A0) < 1.
```

For `x>=x0`,
`f1(x)-w0=(1-x)[C'_1-w0+D0 x]>=0`. For `x<=x0`, discard the
nonnegative curvature in f0 and obtain
`f0(x)-w0>=C'_0-w0-(C'_0+A0)x>=0`.
This proves `max(f0,f1)>=w0` for every real x in `[0,1]`.

### 6.1. Symbolic verification of S in the infinite region

When both k_0 and k_1 are nonnegative, the primed constants are

```
C0=3a(a+1)+ab,
C1=3a^2+4a-1-(b^2+3b)/2,
C0-w0=3a^2+2a+b+1>0,
H0:=w0-C1=B+ab-3a(a+1).
```

Let

```
P(a,b)=12{2B^2(C0-w0)-(2b+1)H0(C0+A0)}.
```

With `X=a-1>=0` and `Y=b-a-2>=0`, exact expansion gives

```
P = 5508+13974X+16650X^2+10407X^3+3342X^4+495X^5+24X^6
  + Y(5634+9606X+8497X^2+4079X^3+920X^4+70X^5)
  + Y^2(3150+3856X+2431X^2+797X^3+98X^4)
  + Y^3(936+854X+390X^2+70X^3)
  + Y^4(126+66X+18X^2)+6Y^5.                             (POLY)
```

Every coefficient is positive. This proves S for the entire
infinite region, since its denominator `12(2b+1)` is positive.
`certificate.py` represents and `verify_certificates.py` checks this
expansion against the explicitly listed coefficients using exact
`fractions.Fraction` arithmetic;
the expression has 26 monomials.

### 6.2. The complete finite list where a k endpoint is negative

In `a>=2,b>=a+2`, `k_0<0` can occur only for
`a=2,b=4,5,6; a=3,b=5,6; a=4,b=6; a=5,b=7`.
Indeed `3b<a+17` and `b>=a+2` imply a<=5. The set where k_1<0
is contained in that list. Include the extra points `(2,2),(2,3)`.
Here are the exact primed constants and the left side minus right
side of S:

| a | b | C'_0 | C'_1 | S margin |
|---:|---:|---:|---:|---:|
| 2 | 2 | 9 | 2 | 58/5 |
| 2 | 3 | 14 | 1 | 405/7 |
| 2 | 4 | 19 | -1 | 1720/9 |
| 2 | 5 | 24 | -4 | 5350/11 |
| 2 | 6 | 29 | -8 | 13554/13 |
| 3 | 5 | 41 | 12 | 13050/11 |
| 3 | 6 | 50 | 11 | 29646/13 |
| 4 | 6 | 74 | 36 | 63126/13 |
| 5 | 7 | 120 | 59 | 194684/15 |

All have C'_0>w0. This table is merely evaluation of the displayed
rational formulas at nine small points, so it is checkable by hand;
it is not an enumeration-based mathematical dependency.

## 7. Completion of T1

If a=0, GW-21's exact transfer identity has W_A=0 and gives P5.0.
If a=1, the upper-unit shadow bounds give `q<=1,u<=q`, hence
`W_A=6-2q-4u>=0`. The transfer bound then gives

```
W >= ab-s+c(c+1)+e(3+2b+c)+r(q+s+t) >= G,
```

which is P5 since w0=0.

For a=2, Region I covers b=0,1 and Region II covers b>=2. For
every a>=3, Region I covers b<=a+1 and Region II covers b>=a+2.
Sections 4 and 6 therefore prove P5 for all parameters.

This is a complete analytic proof. The roles of computation are to
verify algebra and test the inequalities on actual instances; the
unbounded quantifiers follow from LIN, the multiplier signs, POLY,
and the nine displayed evaluations.

## 8. Exact semigroup translation: T1s

Let S be a numerical semigroup of multiplicity m, conductor C_S,
embedding dimension E_S, and smallest minimal generator n_1 other
than m. Suppose

```
3m<C_S<=4m, 2n_1>=C_S-m.
```

Choose the lexicographic factorization down-set for Ap(S,m) on the
minimal generators other than m. It is downward closed: replacing a
divisor by a preferred factorization would replace the original
factorization by a preferred one. It has m elements and distinct
residues, all directions are active, and its maximum value is
`M=C_S+m-1`. Thus

```
d=E_S-1, rho=4m-C_S, h=C_S-3m,
A: m<n<C_S-2m,
B: C_S-2m<=n<C_S-m,
C: C_S-m<=n<C_S,
E: C_S<=n<C_S+m.
```

For an A generator, `2(n-m)>=h` is exactly `2n>=C_S-m`.
Generators outside A satisfy this inequality automatically, since
`C_S>3m`. Thus the hypothesis on n_1 is exactly the upper-unit
hypothesis. Selmer's formula gives `g=genus(S)` and
`ell=C_S-g=|S intersect [0,C_S)|`. Consequently

```
W=d ell-g=E_S ell-C_S=W(S).
```

P5/P5.0 prove **Wilf for every S with
`3m<C_S<=4m` and `2n_1>=C_S-m`**, with the stronger quantitative
bound in P5 when a>=1.

## 9. Stretch result: an adaptive arc and an LC reduction

Drop the upper-unit hypothesis and assume a>=1. Let

```
L=min_{A} t_j, delta=max(0,h-2L),
K=q3+b+c+e+s4+t4.
```

**Adaptive arc lemma.** In the full primary regime,

```
h <= 2K+2+3delta.                                      (AARC)
```

If delta=0 this is section 2. If `3L<=h`, it follows immediately
from `3delta=3h-6L>=h`. In the remaining case
`h/3<L<h/2`, use

```
Y_L=[h,min(3L,m)) union [1,3L-m).
```

Its size is at least `3L-h-1`. Cubics have tau at least 3L;
quartics cannot occur since `4L>h-1`; and cubic tau is at most
`m+h-1`. A units miss the low arc since `3L-m<=L`, using `2L<m`.
AC and BC have tau at least `m+h+L>=m+3L`. An I2 AA cell has
tau<h and at least 2L, and therefore misses both arcs. The same
range argument as in section 2 shows that only q3, B/C/E units,
s4 and t4 occupy Y_L. Thus `K>=3L-h-1`, which rearranges to AARC.
This proof applies to every down-set in the original P4 setting.

**Theorem P5-low (uniform quantitative reduction).** Let a>=3,
retain all P4 hypotheses, and put

```
G=c(c+e+1)+e(3a+2b-1)+(c+e)(q3+s3+t3),
Lmin=min((a+1)q2, binom(a+1,3)),
J=(b+2)q2+k-3delta.
```

Then

```
W >= (a-1)(b+1)+G+Lmin+b u3+(c+e)(2q2+u3)
     - max(0,3delta-(b+2)q2-k).                         (LOW)
```

Here is the full algebraic extension of the previous proof.
Replace ARCslack by

```
rho-[ARC_rhs_from_section_3+q2+u3+k+v2-3delta],
```

which is nonnegative by AARC. Replace the AAA shadow defect in ID
by `(a+2)(q2+q3)-3(u3+u4)`. Before the mixed v shadow and q capacity
are used, the additional low terms in ID are exactly

```
[2(a+b)-2+lambda-(4-lambda)(a+2)/3]q2
+(a+b+1)u3-(4-lambda)(k+v2)-3lambda delta
+(c+e)(2q2+u3).
```

For the endpoint certificates, use
`2(v2+v3)<=(a+1)s3` in place of the v-only shadow. Its contribution
adds `2nu_lambda v2`. The remaining v2 coefficient is
`-(1-lambda+mu_lambda)`, which is nonpositive; pay it with
`v2<=bq2`. Use `q2+q3<=Q` in place of `q3<=Q`.
Substitution of k_lambda then leaves exactly

```
(a+1)q2+(a+b+1)u3-4k+lambda[(b+2)q2+k-3delta]
+(c+e)(2q2+u3)
= [(a+1)(q2+u3)-4k] + b u3 + lambda J
+(c+e)(2q2+u3).                                       (LOW-ID)
```

The signs of all certificate multipliers remain as before. In
Region I the same computation uses its lambda=1 certificate, the
total q capacity, and its mu; it gives exactly LOW-ID with lambda=1.
The B multicomplex and MC remain valid without the upper-unit
hypothesis. GW-24's LC says the square bracket is at least Lmin.
In Region II, add LOW-ID to each of the two lower bounds in BR;
the bridge gives `max(f0,f1)>=w0`, and
`lambda J>=min(0,J)`. Region I gives at least that same weaker
conclusion. This proves LOW.

In particular Wilf follows whenever

```
3delta <= (a-1)(b+1)+G+Lmin+(b+2)q2+b u3+k
          +(c+e)(2q2+u3).                              (LOW+)
```

For semigroups, `delta=max(0,C_S-m-2n_1)`. For example, without
any assumption on q2, the primary regime with a>=3 is proved if
`3delta<=(a-1)(b+1)`.

Combining LOW with GW-24 gives a precise remaining frontier: a
counterexample in the full primary regime must have a>=7, delta>0,
violate LOW+, and satisfy GW-24's necessary LC-minus conditions

```
q2<a(a-1)/6,
3(a+1)q2+(a+17)r_A < 3 binom(a+1,3),
r_A=Q-q2-q3.
```

No claim is made that these remaining conditions are inconsistent.
The low-unit problem is still open in this report.

## 10. Computational verification and provenance

All executions used fejer, Python 3.12.3 (`~/mathenv/bin/python`),
and GCC; exact certificate work used `fractions`, with no sympy.
Scripts and logs are in this directory; reproducible commands use
`gcloud compute ssh fejer --zone us-east1-b --command 'cd ~/wilf/p5 ...'`.

`verify_certificates.py` checks the endpoint identities, multiplier
signs, and bridge inequality exactly on
`2<=a<=250, a+2<=b<=1000`, plus `(2,2),(2,3)`:
**217,379 parameter pairs**, no failures. It verifies LIN exactly on
**126,245 pairs**, `2<=a<=500, 0<=b<=a+1`, omitting a=2,b=2,3.
The positive-coefficient POLY identity is checked exactly as a
polynomial, including all 26 coefficients, rather than sampled.

The shared `p5_check.h` independently reclassifies each cell, checks
the band counts and GW-21 transfer identity, every capacity and
weighted shadow used here, SR, exact discrete Macaulay
`z<=t^{<2>}`, the rational MC inequality, ARC under U, AARC in
general, LC, P5, and LOW. The exact discrete Macaulay calculation
uses `t=binom(k,2)+r`, `0<=r<k`, and
`t^{<2>}=binom(k+1,3)+binom(r+1,2)`. MC is tested after clearing
denominators, entirely with integer arithmetic.

The exhaustive scanners are adaptations of the P4 scanners. They
enumerate down-sets with every direction active, one shape per
coordinate-permutation orbit, all residue assignments, and lifts
1 through 4. The semigroup tree enumerates by deleting effective
minimal generators and constructs a lexicographic Apéry tile;
downward closure is independently asserted for every chosen
factorization. `p5_random.c` adapts the supplied arc generator,
constructs actual semigroups by Dijkstra, recovers minimal generators,
constructs their tiles, and independently checks downward closure.

Final runs, with zero assertion failures, gave the following counts.
Counts for upper instances
include a=0, where U is vacuous; the `linear`/`curvature` fields only
count a>=2. The exhaustive scanner's primary/upper fields are
cumulative within each invocation.

| Check | Domain / attempts | Primary instances | Upper-unit instances |
|---|---:|---:|---:|
| Arbitrary down-sets, d=2 | m=3..22; 72,224 weight assignments | 94 | 52 |
| Arbitrary down-sets, d=3 | m=4..13; 347,776 weight assignments | 2,989 | 1,156 |
| Arbitrary down-sets, d=4 | m=5..10; 992,768 weight assignments | 42,237 | 19,316 |
| Exhaustive semigroup tree | genus<=28; 5,311,726 nodes including N | 642,239 | 580,615 |
| Random semigroups | seed=20261019; 250,000 attempts; 10<=m<=120 | 14,444 | 5,885 |

The tree checked AARC on 189,141 instances with A nonempty, and
LC/LOW on 8,894 instances with a>=3, including 6,258 below U. The
random run checked AARC on 11,611 instances and LC/LOW on 6,635,
including 5,674 below U. Upper-unit random examples reached a=11
and b=13. The smallest slack in P5 among a>=1 was 1 in the
exhaustive checks and 11 in the random run; no optimality claim is
based on these samples.

In addition to parameter sampling, `symbolic.py` proves LIN and EP
as exact identities in the rational-function field Q(a,b), treating
both signs of k independently. It also verifies the corrected
LOW-ID coefficient symbolically. Its output is

```
All endpoint branches, LIN identities, and LOW-ID verified in Q(a,b).
```

`lp_counterexample.py` checks every row and the objective of the
fractional witness in section 11 using exact fractions, and verifies
that MC excludes that vector.

The [logs](logs/) include the complete runs, the exploration outputs,
and `SHA256SUMS` for the executed sources. The final commands run on
fejer, within `~/wilf/p5`, were:

```sh
nice -n 10 ~/mathenv/bin/python verify_certificates.py > verify_certificates.log
nice -n 10 ~/mathenv/bin/python symbolic.py > symbolic.log
nice -n 10 ~/mathenv/bin/python lp_counterexample.py > lp_counterexample.log
gcc -O2 p5_scan.c -o p5_scan
gcc -O2 p5_tree.c -o p5_tree
gcc -O2 p5_random.c -o p5_random
nice -n 10 ./p5_scan 2 3 22 > scan2.log
nice -n 10 ./p5_scan 3 4 13 > scan3.log
nice -n 10 ./p5_scan 4 5 10 > scan4.log
nice -n 10 ./p5_tree 28 > tree28.log
nice -n 10 ./p5_random 20261019 250000 10 120 > random.log
nice -n 10 ~/mathenv/bin/python summarize.py > summary.log
```

These can be run serially. During this task at most four single-core
jobs ran at once. Exploratory scipy LP calls used
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`. Compiler:
`gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`.

## 11. Failed claims, corrections, and strategic review

**False LP claim in the input evidence:** the linear LP without
Macaulay does not always have minimum `(a-1)(b+1)`, even for small
positive a,b. The smallest positive-a,b counterexample in
lexicographic order is `(a,b)=(2,2)`, c=e=0, with objective
`29/11<3` and the feasible count vector

```
q=3, u=4,
s=28/11, S=16/11, t=21/11, T=12/11,
v=w=42/11, z=28/11, rho=133/11, H=I=0.
```

All constraints in `arc_lp2.py` hold. For a=1 the transfer/shadow
bound proves W>=0 and the full count vector attains 0; for a=2,
b=0,1 LIN proves and attains the stated bound. Thus the above is
indeed the smallest positive-a,b failure. This is a fractional LP
vector, not an actual tile or a Wilf counterexample. The lead's
B-heavy negative LP witness `(20,160)` is consistent with this
phenomenon. Section 5 supplies the missing nonlinear information.

**Discarded intermediate algebra:** in extending the endpoint
certificates to low AA cells, the lambda=0 v2 coefficient must be
`-(1+mu_0)`, whereas the lambda=1 coefficient is `-mu_1`.
Omitting that extra 1 would incorrectly place `b q2` outside the
lambda-dependent term. LOW-ID displays the corrected exact
calculation; the claimed theorem is LOW. The first exact checker
also exposed a Python int-to-float division at negative k endpoints;
the verifier was changed to force Fraction arithmetic before its
reported successful run. Neither issue is used as a mathematical
assertion.

**Strategic review.** The linear dual is sufficient in an overlapping
A-heavy region. Its failure in the B-heavy region reflects the loss
of curvature in the BBB shadow. The endpoint bridge pays this loss
uniformly and completes the actual upper-unit target. It is therefore
unnecessary to pursue the packing alternatives for T1. After that
completion, moving the arc to `3L` produces the explicit low-unit
loss and the LC reduction in section 9. The remaining task for a
full c<=4m theorem is to control that loss in the stated LC-minus
frontier; bounded LP searches do not settle it.
