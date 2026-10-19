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

## 12. T2 continuation: status and exact new results (2026-10-19)

The lead has independently verified sections 1–9 and recorded them
as GW-26 and GW-26b. This continuation leaves those sections intact.
**The full primary regime is not closed here.** The following are
new proved results, uniform in a:

1. A stronger arc reduction using the actual intruders, the actual
   low-face cost, and retained shadow/capacity defects (section 13).
2. **Wilf whenever at most one A unit is low**, with arbitrary B/C/E
   directions (section 14). Combined with GW-24, this covers every a.
   In semigroup notation it suffices that `2n_2>=C_S-m`, where n_2 is
   the second minimal generator other than m; n_1 may be arbitrarily
   small.
3. An augmented joint short-residue lemma and a high-core certificate
   (section 15).
4. A corrected low-pair count and an exact total-Macaulay restriction
   on any remaining deficient A face (section 16).

The remaining structured family is specified in section 17. Its
nonemptiness as an actual residue-complete family is not established.
The adversarial searches in section 18 did not reach the old LOW+
frontier; this is explicitly a limitation of the searches, not a
proof that the frontier is empty.

Notation remains that of sections 1–9. In this continuation put

```
Q=binom(a+1,2), U=binom(a+2,3), F=binom(a+1,3),
q=q2+q3, u=u3+u4,
r_A=Q-q, t_A=U-u,
D3=(a+2)q-3u=3t_A-(a+2)r_A,
LC_actual=(a+1)(q2+u3)-4k.
```

All are exact counts or nonnegative defects, except that LC_actual
needs LC (a>=3) for its nonnegativity. Two useful identities are

```
WA=3a(a+1)+(a-3)q-4u+LC_actual
  =-F+LC_actual-(a-3)r_A+4t_A.                         (A-ID)
```

The term T is exactly the nonnegative transfer term in GW-21 / P4
section 3; G is as in section 9 above.

## 13. The actual-intruder reduction, retaining defects

Take the same fixed arc as in GW-26:

```
theta=ceil(3h/2),
Y=[h,min(theta,m)) union [1,theta-m).
```

Let J be the number of cells whose residues are in Y and which are
not of any of these allowed types:

```
q3; B/C/E units; s4; t4.
```

Let J_A be the number of these intruders supported entirely in A.
These definitions apply without U. In particular, J counts cells,
not formal factorizations that are absent from D.

Since `|Y|>=h/2-1`, residue injectivity gives the unconditional
inequality

```
h<=2(q3+b+c+e+s4+t4)+2+2J.                            (IARC)
```

This is also immediate by partitioning the actual occupants of Y
into allowed cells and intruders. There is no assumption about the
number or location of low directions in IARC.

Define

```
Mq=(ab-s3-s4)+(B-t3-t4),
Cdef=D3+4Mq+3(ac-H)+3(bc-I),
Astar=(a-1)(b+1)+G+LC_actual+b u3
      +(c+e)(2q2+u3)+Cdef,
eta=min(3delta,2J), delta=max(0,h-2L).
```

Here H and I count AC and BC cells. Every term in Cdef is
nonnegative. **For a>=3,**

```
W>=Astar-max(0, eta-(b+2)q2-k).                        (I-LOW)
```

In particular Wilf follows if

```
eta <= Astar+(b+2)q2+k.                              (I-LOW+)
```

Proof. Both AARC and IARC imply
`h<=2K+2+eta`, with K from section 9. Repeat LOW-ID with the
arc loss `3delta` replaced by eta, and retain the low-face cost as
LC_actual. The low terms are exactly

```
LC_actual+b u3+(c+e)(2q2+u3)
   +lambda[(b+2)q2+k-eta].
```

The total AAA shadow defect is D3. Its multiplier in ID is
`(4-lambda)/3>=1`; those of Mq and the AC/BC capacity defects are
at least 4,3,3. They therefore contribute at least Cdef at both
endpoints. The endpoint bridge and Region I certificate remain
unchanged, and `lambda J0>=min(0,J0)` for
`J0=(b+2)q2+k-eta`. This proves I-LOW. All its terms apart from
the final loss are nonnegative. I-LOW+ follows.

This strengthens GW-26b in three independent ways: eta can be
smaller than 3delta, LC_actual can exceed its minimum, and Cdef was
previously discarded. Its proof uses the already verified symbolic
LOW-ID rather than a new numerical optimization.

There is a useful **high-relative family of arcs**. Choose a threshold
H with `ceil(h/2)<=H<h`, and call the A directions with t>=H its
upper core. Put

```
Theta_H=h+H,
Y_H=[h,min(Theta_H,m)) union [1,Theta_H-m),
J_H=# occupants of Y_H not of an allowed type.
```

Then `|Y_H|>=H-1` and

```
H<=K+J_H+1,
h<=2K+2+[h-2H+2J_H].                                (HARC)
```

Moreover, every intruder in J_H contains an A direction outside
the upper core. An all-core cubic has tau>=3H>=h+H; an all-core
quartic cannot fit. A core unit misses the low interval since
`Theta_H-m<=H`. AB and BB using only core A directions have tau
at least h+H; AC and BC have tau at least m+h+H. Their possible
wraps miss Y_H exactly as in the fixed-arc proof. Core AA cells
are allowed q3 cells.

It follows that I-LOW remains valid with the stronger choice

```
eta=min(3delta,2J, h-2H+2J_H for chosen upper-core thresholds H).
                                                               (ETA)
```

The last quantity can be negative; the endpoint proof only requires
the displayed valid arc inequalities and still gives the same
maximum-with-zero formula. For the explicit remaining family below,
take every H which occurs as an offset of an upper A unit. There
are at most a such tests.

This repairs an endpoint problem in the proposed `Theta=3H` arc.
Without additional hypotheses its low interval can contain high
units: in the semigroup from section 16, m=h=6, L=2, H=4, the
proposed `[1,3H-m)=[1,6)` contains the high unit with offset 4.
It therefore cannot be treated as an arc with only low-supported
intruders under the stated general hypotheses. The choice h+H
above avoids this issue, including when H>m/2.

## 14. A complete proof with exactly one low A direction

**Theorem T2.1.** In the full primary regime, if a>=6 and at most one
A direction satisfies `2t_j<h`, then W>=0, for every b,c,e.
The case of no low directions is GW-26. Combining the new case
with the paper part of GW-24 (a<=5) proves the assertion for every a;
the a=6 finite certificates are not needed for this corollary.

We first prove a down-set inequality which does not need residue
injectivity or the cardinality relation. Its inputs need only obey
the P4 value bound and unit ranges at the fixed scale m,h.

**One-low arc payment lemma.** Suppose a>=6, the only low A unit is
x with offset L<h/2, and every other A offset is at least ceil(h/2).
Then

```
2J_A <= (a-1)+LC_actual+2q2+k.                         (OL)
```

Proof. Write `p=a-1`. A cold residue means an integer in
`[1,theta-m)`; its upper endpoint is at most ceil(h/2).
A hot pure-A cubic has tau in `[h,theta)`.

Every pure-A intruder is of one of these types:

* a cold cell `x`, `x^2`, `x^3`, or `x^4`;
* a hot cubic `x^3`, `x^2 y`, or `x y z`, where y,z are high A
  directions, and y=z is allowed.

Indeed a cell containing a high direction cannot be cold; all-high
cubics have tau at least theta. High AA cells are allowed q3 cells.
Any quartic with at least two high factors has tau greater than h-1
and cannot lie in D. A quartic with one high factor can be in D,
but cannot be cold and therefore is not an intruder. The list is
an upper bound; a zero residue or an endpoint omitted from Y only
reduces J_A.

Let l count the present low pairs `xy` with `L+t_y<h`. A hot
`xyz` intruder forces both xy and xz to be such pairs: otherwise
its tau is at least `h+ceil(h/2)=theta`. Thus there are at most
`binom(l+1,2)` such intruders, with `0<=l<=a-1`.

If x^2 is absent, q2=l and u3=k=0. Only the cold unit x and the
above xyz cubics can intrude. Therefore the right side minus left
side of OL is at least

```
(a-1)+(a+3)l-l(l+1)-2
 =a-3+l(a+2-l)>=0.
```

Suppose x^2 is present. Let

```
epsilon3=1 if x^3 is present and 3L<h, otherwise 0,
epsilon4=1 if x^4 is present, otherwise 0,
u0=# {x^2 y in D: 2L+t_y<h},
v0=# {x^3 y in D}.
```

Then

```
q2=1+l, u3=epsilon3+u0, k=epsilon4+v0,
0<=v0<=u0, epsilon4<=epsilon3.
```

The last two facts follow by deleting x from a quartic. There are
at most `p-u0` hot x^2 y intruders, since those with tau<h and
those with tau>=h are disjoint. Subtracting the upper bounds on
these and the xyz intruders from the proposed payment leaves at
least

```
4+l(a+2-l)+(a+1)epsilon3-3epsilon4+a u0,                (OL-res)
```

before the cold cells and a possible hot x^3 are paid. This is
exactly the following calculation:

```
(a-1)+(a+3)(1+l)+(a+1)(epsilon3+u0)-3(epsilon4+v0)
 -l(l+1)-2(a-1-u0)
 =4+l(a+2-l)+(a+1)epsilon3-3epsilon4
   +(a+3)u0-3v0
 >=OL-res.
```

If `3L>=h`, then epsilon3=epsilon4=u0=0; there can be one hot
x^3 and one cold x, but x^2 is not cold since
`2L>=2h/3>=ceil(h/2)`. These cost at most 4, paid by OL-res.

If `3L<h`, there is no hot x^3. The cold cells cost at most
`2(2+epsilon3+epsilon4)`. Subtracting this from OL-res leaves

```
l(a+2-l)+a u0+(a-1)epsilon3-5epsilon4>=0,
```

because a>=6 and epsilon4<=epsilon3. This proves OL.

To finish the theorem, every non-pure-A intruder must contain x.
The only possibilities are an I3 cell xB, an AC cell xC, and an
AAB cell x^2 B. There are at most b,c,b of them respectively, and
the last family requires x^2 in D. Thus, writing epsilon2 for the
presence of x^2,

```
J-J_A <= b(1+epsilon2)+c.                              (OL-out)
```

The range exclusions are explicit: a cubic x y B with high y has
tau at least `L+ceil(h/2)+h>theta`; ABB and BBB have tau>theta;
BC has tau at least m+2h and misses Y. A high AC or high AB cell
cannot be an intruder by the original GW-26 range argument.

Use I-LOW with eta replaced by 2J. Its total proposed payment
for that loss is at least

```
(a-1)(b+1)+G+LC_actual+b u3+(b+2)q2+k.
```

After using OL and OL-out, the remaining payment is at least

```
b[a-1+q2+u3-2(1+epsilon2)]+G-2c>=0.
```

For epsilon2=0 the bracket is at least a-3; for epsilon2=1,
q2>=1 makes it at least a-4. Also
`G>=c(c+e+1)>=2c` whenever c>0, with the c=0 case immediate.
All omitted terms in I-LOW are nonnegative. This proves W>=0.

**Semigroup corollary.** Let `m<n_1<n_2<...` be the minimal
generators other than m. Wilf holds for

```
3m<C_S<=4m, 2n_2>=C_S-m.
```

If there is only one generator other than m, Wilf already holds.
The condition says exactly that at most one A direction is low,
since every generator outside A automatically satisfies the
upper-unit inequality. No restriction on n_1 is imposed.

## 15. An augmented short-residue lemma and the high core

Let H3 count the present AAA cells whose tau is at least 2h.
Then

```
rho >= t3+I+v3+w+z+H3.                               (ASR)
```

Proof. The five old families have residues in the cyclic interval
obtained by reducing `[2h,m+h)` modulo m. This interval has rho
integer residues. Every additional AAA cell in H3 has
`2h<=tau<=m+h-1` and therefore lies in that same interval. The
families are disjoint and all residues are distinct. This proves ASR.

Consequently the exact transfer identity gives

```
W>=WA+T+H3.                                          (HOT)
```

Define

```
p=# {A units j: 3t_j>=2h}.
```

Every present cubic on these p directions is counted by H3. At
most t_A of the `binom(p+2,3)` formal cubics can be absent, so
`H3>=binom(p+2,3)-t_A`. Substituting A-ID and
`3t_A=(a+2)r_A+D3` into HOT proves the uniform certificate

```
W >= LC_actual+binom(p+2,3)-F+5r_A+D3+T.               (HIGH)
```

In particular it proves Wilf whenever the right side is nonnegative.
For p>=a-1 this gives W>=LC_actual+5r_A+D3+T>=0. This special
case is contained in Theorem T2.1, but HIGH also applies to families
with several low units. It is an independent certificate whose
positive D3 term makes missing cubic cells pay for the deficit.

One can augment ASR further with any other known occupants of that
same cyclic interval. For example, if h<=m/2, zero, all A units,
all q2 and u3 cells, and all quartics have residues in it, and hence

```
rho>=t3+I+v3+w+z+H3+1+a+q2+u3+k.                    (ASR-small)
```

This follows because the interval is then
`[2h,m) union [0,h)` in ordinary residues. This optional bonus
was not used in the proof of T2.1.

## 16. Correcting the low-pair premise; total Macaulay

Let alpha count the low A units, those with 2t<h. Every formal
pair of low units has tau<h. If that monomial is present it is q2;
if absent it is one of the r_A missing AA monomials. The correct
unconditional count is

```
binom(alpha+1,2)<=q2+r_A,                             (LP-low)
```

not `binom(alpha+1,2)<=q2`. The latter premise in the lead's
structural observations needs a completeness hypothesis on AA.

A smallest-multiplicity actual semigroup counterexample is

```
S=<6,8,10,25,27,29>, C_S=24,
Ap(S,6)=(0,25,8,27,10,29) by residue,
a=2, h=6, L=2, alpha=1, q2=0, r_A=3.
```

In particular `2*8=10+6` is not in Ap, so the low unit has no
loop in D. Its conductor is 24 because 23 is a gap and 24 through
29 are in S. The other missing AA cells are 8+10=18 and
10+10=20, also not in Ap. All six displayed generators are
minimal. The genus-28 tree found no smaller-multiplicity example;
that tree covers every primary semigroup with m<6, since C_S<=20
there implies genus<=16. Thus the minimal-multiplicity statement
here is an exact finite verification, not a random-search claim.
No conclusion `alpha<a/sqrt(3)` is inferred without accounting for
r_A.

There is also a useful stronger total-Macaulay restriction on a
deficient A face. Let `q^{<2>}` be the exact Macaulay growth at
degree two. Since the A face is a multicomplex,
`u3+u4<=q^{<2>}`. A-ID gives

```
WA<0 => 4q^{<2>}>3a(a+1)+(a-3)q+LC_actual.             (MAC-)
```

LC-minus already implies `LC_actual>=(a+1)q2` in this situation.
Therefore every possible deficient profile must satisfy

```
4q^{<2>}>3a(a+1)+(a-3)q+(a+1)q2.                     (MAC-simple)
```

These are exact integer conditions. For each fixed a they give a
finite explicit list of possible q and q2 counts, which can then be
combined with LP-low. No asymptotic estimate is substituted for the
exact growth operation. The script `t2/count_frontier.py` evaluates
these finite necessary count lists for the a values in its log.

For example, the number of surviving total-q values and the largest
alpha permitted by these *necessary count tests* are:

| a | total-q values | alpha upper bound |
|---:|---:|---:|
| 7 | 3 | 3 |
| 8 | 4 | 3 |
| 12 | 15 | 6 |
| 20 | 53 | 10 |
| 50 | 428 | 29 |
| 100 | 1,917 | 61 |

These are not claims that actual residue-complete examples attain
the bounds. After T2.1 the remaining alpha range starts at 2.

## 17. The remaining structured family and the failure of a simpler route

Combining the new results with GW-24, GW-26, and GW-26b, any
counterexample in the primary regime must satisfy all of:

```
a>=7, alpha>=2, delta>0;
LC-minus, LP-low, and MAC-minus;
eta>Astar+(b+2)q2+k;                                  (F1)
WA+T+H3<0;                                           (F2)
LC_actual+binom(p+2,3)-F+5r_A+D3+T<0.                 (F3)
```

Here all terms are explicit counts or thresholds of the A offsets;
eta, Astar, H3 and p are defined in sections 13 and 15. In particular
F1 implies both a large adaptive-arc deficit and enough actual
intruders to overwhelm the retained low-face and capacity costs.
F3 restricts the population of units at or above 2h/3. These are
uniform restrictions with no bound on a,b,c,e. This report does not
prove that this remaining structured family is empty.

The promising but false unrestricted analogue of OL would assert

```
2J_A <= (a-1)+LC_actual+2q2+k
```

for any number of low directions using only the down-set and
value-band hypotheses. A small counterexample within the main
range a>=7 is the full degree-three simplex in seven variables,
at scale `m=h=5`, with offsets `(2,2,3,3,3,3,3)`.
Its actual maximum is `24=4m+h-1`, and

```
q2=3, u3=k=0, J_A=21, LC_actual=24,
(a-1)+LC_actual+2q2+k-2J_A=-6.
```

J_A comprises two low units, four low-only cubics, and fifteen
low-low-high cubics. This is a counterexample to the proposed
scale/cardinality-free payment, not to Wilf: its down-set has 120
cells, not m=5, and has many repeated residues. It is the smallest
a in the stipulated a>=7 domain, and m=5 is the smallest scale
in the full-cubic two-level exact-maximum family at a=7, checked
in `validate.py`.
The experimental scripts retain the full failing inputs and label
their relaxed hypotheses.

A second relaxation explains why the fixed arc and the high-cubic
certificate alone do not prove the full result. Take the full cubic
simplex with

```
a=12, m=455, h=317,
four offsets 106 and eight offsets 257.
```

Now `|D|=m` and its actual maximum is
`2136=4m+h-1`. Its counts are

```
q2=10, q3=68, u3=k=0, u4=364,
LC_actual=130, WA=-156, p=8, H3=120,
J_A=100, delta=105, D3=r_A=0.
```

The formal band expression would be WA+rho=-18; the actual P4
slack, computed directly from the floors, is -104. They differ
because the band identity uses residue completeness. This relaxed
example has only a handful of distinct residues, and is not a
numerical-semigroup or residue-complete example. Even taking all
twelve weights distinct, with offsets 106..109 and 250..257,
leaves the same band counts and direct P4 slack -104.

HARC does exclude this profile: at H=257 one has J_H=104 and
K=q3=68, so it would require `257<=68+104+1=173`. This failure
is a reason for retaining the high-relative arcs in ETA. The
example is not claimed to survive the complete F1–F3 reduction.

Signed B3 packing immediately excludes either full cubic simplex
as a residue-injective tile: it would require
`m>=H_12=13(78+1)=1027`, rather than 455. Thus this is evidence
for retaining residue packing in any further attack, not evidence
for a Wilf counterexample. The naive intruder-only payment has been
discontinued; OL is used only with its proved one-low hypothesis.

There is an explicit packing supplement in the full-AA family.
If r_A=0, write X for the number of cells involving outside
directions, and retain k quartics. Cardinality gives
`m=binom(a+3,3)-t_A+k+X`. Applying GW-24 LP to the A face gives

```
(3a+1)t_A>=4F-2k-2X.                                (PACK-A)
```

Indeed `2m>=2H_a-3(a+1)t_A` and
`H_a=binom(a+3,3)+2F`. For a pure-A, no-quartic a=12 profile,
PACK-A forces t_A>=31. If q2=10, u3=0 and J_A<=100 remain as
in the displayed two-level phase, I-LOW receives at least 93
through D3, more than its possible 39-unit intruder-payment
deficit. This excludes that near-full scalar phase. PACK-A does not
uniformly control the entire remaining family when a is unbounded
and many cubic cells are missing.

## 18. Continuation computations and adversarial searches

All computation in this continuation ran on fejer in `~/wilf/p6`,
with `nice`, no more than four single-core processes at once. Local
work was reading, editing and copying. No commits were made.
The code and archived outputs are under `t2/`.

`p6_check.h` independently counts the arc intruders and high AAA
cells on actual residue-complete inputs, and checks LP-low, HOT,
HIGH, I-LOW, and OL whenever its one-low hypothesis applies. The
old P5 checker runs as well. The semigroup tree independently
constructs and checks its lexicographic factorization down-set.
The final runs had zero assertion failures:

| Check | Domain | Verified instances / tests |
|---|---|---:|
| Semigroup tree | genus<=28, 5,311,726 nodes including N | 642,239 primary semigroups |
| General intruder/defect bound on that tree | a>=3 | 8,894 |
| High-relative arcs on that tree | all upper A thresholds, a>=3 | 20,546 |
| Exhaustive arbitrary down-sets | d=4, m=5..10, lifts 1..4 | 992,768 residue-bijective weight assignments; 42,237 primary |
| General bound on those down-sets | a>=3 | 3,155 |
| High-relative arcs on those down-sets | all upper A thresholds, a>=3 | 4,826 |
| Targeted random semigroups | seed=202610194; 100,000 attempts; 120<=m<=3000 | 97,340 primary; 89,443 with a>=7 |
| OL on the random semigroups | a>=6, exactly one low A unit | 11,046 |

The random run found 302 low-unit instances with a>=7 and WA<0,
with minimum WA=-126. None violated LOW+. All HOT/HIGH assertions
and the general bound retaining D3 passed. The genus tree has only
three one-low instances with a>=6, all at a=6; the random run is
therefore useful evidence beyond the small-genus range.

The min-closure experiment in `arc_minclosure.py` is a different
kind of test: at fixed weights and scale it minimizes the proposed
pure-A payment over **all** eligible down-sets by a maximum-flow
reduction. Cells with negative coefficients have source edges,
positive coefficients have sink edges, and every cell has an
infinite-capacity edge to every immediate divisor; units are forced
present. The residual source side recovers a minimizing down-set.
It omits residue constraints deliberately to test the combinatorial
payment lemma. On 2,987 one-low inputs with 6<=a<=19, seed
202610192 and 3<=h<=m<=1000, it found no negative payment; the
smallest value was 2. This verifies examples of OL and is not its
proof. The unrestricted run found a negative payment after 22
inputs; the smaller explicit construction in section 17 replaces
that large random witness for review.

`adversary.c` constructs actual semigroups
`<m,base> union [3m+h,infinity)`, then computes their actual
conductor rather than assuming that the forced endpoint is sharp.
It recovers minimal generators, a lexicographic Apéry tile, and all
counts used in the new inequalities. The generator flavors place
low offsets below h/2 and high offsets near h-L, above h/2, near
h/3..2h/3, or above 2h/3; up to forty B candidates are added. The
search records negative WA faces and tests whether they violate
LOW+. It is biased toward the proposed mechanisms, but does not
guarantee a frontier instance.

`tile_adversary.c` searches arbitrary residue-complete down-sets,
which gives more freedom than semigroup closure. It builds an A
face from present quadratic and I4 cubic cells, adds B directions
and their eligible descendants while preserving all divisor and
residue constraints, then fills unused residues with E units. The
maximum residue h-1 is reserved for the E unit at `4m+h-1`, so
the claimed primary regime is exact. The greedy mode optimizes the
LOW deficit; the coverage mode allows adverse intermediate steps
and prioritizes covering unused residues. The two-low mode forces
at least two low A units. It saves the closest completed down-set
as `tile_best.json` rather than only recording a count vector.

`validate.py` reconstructs that saved complete down-set in ordinary
coordinate tuples, checks downward closure and residue bijectivity
without the C code, recomputes every floor in W, and checks the new
certificates. It also independently checks the explicit relaxed
counterexamples in section 17. `count_frontier.py` uses exact
Macaulay integer growth, not condensed or floating approximations.

The final multi-low completion run used seed 202610198, 10,000
attempts, 100<=m<=1800, coverage mode, and at least two low units.
It produced 41 initial negative-WA faces which were extended with
B directions and completed. None violated LOW+. Its closest saved
completion, [tile_best.json](t2/tile_best.json), has

```
m=717, h=278, a=7, b=35, c=0, e=35, alpha=2,
q2=3, q3=25, u3=k=0, u4=81,
WA=-20, W=18475, delta=74,
J=17, J_A=7, H3=49, D3=9, T=9406.
```

Its LOW+ right side exceeds 3delta by 9,334: it is still far from
the old frontier, despite the targeted construction. The independent
validator gives HIGH lower bound 9,403 and I-LOW lower bound 11,802.
Its five upper-unit thresholds give

```
(H,J_H,h-2H+2J_H)=
(185,32,-28), (213,46,-56), (220,50,-62),
(266,84,-86), (270,86,-90).
```

Thus ETA is -90 for this actual example. The saved file includes
682 core cells including zero; the validator supplies 35 E units
to give all 717 cells. All these cells are checked independently
in ordinary coordinate tuples.

The [continuation logs](t2/logs/) include final checks, explicit
relaxation witnesses, earlier probe outputs, and SHA256SUMS of the
executed sources. The principal final commands on fejer were:

```sh
cd ~/wilf/p6
cp ../p5/p5_check.h .
gcc -O2 p6_tree.c -o p6_tree
gcc -O2 p6_scan.c -o p6_scan
gcc -O2 adversary.c -o adversary
gcc -O2 tile_adversary.c -o tile_adversary
nice -n 10 ./p6_tree 28 > tree28_final.log
nice -n 10 ./p6_scan 4 5 10 > scan4_final.log
nice -n 10 ./adversary 202610194 100000 120 3000 > adversary_b40_final.log
nice -n 10 ./tile_adversary 202610198 10000 100 1800 1 2 > tile_two_low.log
nice -n 10 ~/mathenv/bin/python validate.py > validate_final.log
nice -n 10 ~/mathenv/bin/python count_frontier.py > count_frontier.log
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python \
  arc_minclosure.py --one-low --amin 6 --trials 3000 > one_low_ge6.log
```

The source `p5_check.h` is copied unchanged from the T1 directory.
The final tree and exhaustive run also assert the corrected
high-arc support exclusions and MAC-minus on every deficient face.

A final discriminating test, `full_relaxation.py`, varied the
near-full two-level obstruction rather than expanding the actual
semigroup boxes. It generated 10,000 full-cubic cardinality-correct
profiles, 7<=a<=40, seed 202610199, with exact primary maximum,
at least two low units in `[ceil(h/3),ceil(h/2))`, and upper units
in `[ceil(h/2),Hmax]`. Of these, 4,519 had negative formal band
slack. **None satisfied all the high-relative arc coverage tests.**
This supports retaining the full high-arc family; it does not prove
that those arcs suffice on arbitrary down-sets. The profiles in
this experiment were explicitly relaxed and were not claimed to
have distinct residues. The command was

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 \
  ~/mathenv/bin/python full_relaxation.py > full_relaxation.log
```

## 19. Strategic review and exact open task after this continuation

Two distinct mechanisms advanced the task: local payment for arc
intruders proved the one-low theorem, while short-residue
augmentation supplied HIGH for general low populations. The
proposed universal intruder payment failed and was replaced by a
proved restricted lemma, rather than promoted from random checks.

The full-primary claim remains unproved. The fixed arc and the
high-cubic scalar certificate allow the relaxed full simplex in
section 17; the high-relative arc then excludes it. Thus that
example diagnoses a weakness of the fixed-arc route, rather than
refuting the complete new arc family. A uniform payment for all
multiple-low populations has not been proved. The tested actual
examples have substantial outside-direction or shadow payment and
did not reach LOW+'s remaining frontier. Expanding those same
random boxes would not establish the missing assertion.

The next discriminating mathematical task is a uniform choice of
upper-core threshold H paying for its multiple-low intruders in
F1, or a proof that such a failure is paid by HIGH. The last
experiment favors this quantile-arc route over simply enlarging the
fixed-arc LP. A packing supplement using shifted pair residues is
still available: PACK-A succeeds in the near-full pure-A phase,
but its current coefficient loses a factor of a as the missing
cubic family grows. No assertion is made that all packing
approaches or all proof routes have been exhausted.

## 20. Multi-low continuation: the two-low theorem (2026-10-19)

Sections 1–19 are retained. The lead has independently verified the
one-low theorem and recorded it as GW-26c. The new theorem of this
continuation is the following; its proof uses residue injectivity in
addition to arc occupancy.

**Theorem T2.2 (two low directions).** In the exact P4 primary setting,
if at most two A directions satisfy `2t<h`, then `W>=0`.
There is no restriction on b,c,e. In particular, if

```
S=<m,n1,n2,n3,...>,  m<n1<n2<n3<...,
3m<c_S<=4m,  2n3>=c_S-m,
```

then Wilf's conjecture holds. If fewer than three non-m minimal
generators exist, the condition is vacuous and GW-24 applies.

The cases with no low direction, one low direction, or a<=6 were
already proved. It remains to prove the theorem for a>=7 and exactly
two low directions. The proof below is analytic for every a and all
outside-direction counts. No finite-instance check is used as a
proof step.

Write x,y for the two low directions, with offsets L<=L_y, and put

```
p=a-2, theta=ceil(3h/2), delta=h-2L>0,
q=q2+q3, r_A=Q-q, D3=(a+2)q-3(u3+u4),
LC=(a+1)(q2+u3)-4k,
P=(a-1)+LC+2q2+k-2J_A.
```

Here J_A uses the fixed arc of section 13. Further local counts are:

```
n0 = number of present pairs on x,y;              0<=n0<=3;
l_x,l_y = numbers of I2 low--high A pairs;
l=l_x+l_y, so q2=n0+l and 0<=l_x,l_y<=p;
u0 = number of I3 cubics supported on x,y;
u1 = number of I3 cubics with two low factors and one high factor;
k0 = number of quartics supported on x,y;
k1 = number of quartics with three low factors and one high factor.
```

All quartics have tau<h, so no quartic contains two high factors.
Likewise no I3 cubic contains two high factors. Consequently
`u3=u0+u1` and `k=k0+k1`.

## 21. The local two-low payment and the Macaulay gap

The two-variable shadow inequalities are

```
4k0<=5u0,             3k1<=4u1.                       (2L-SH)
```

For the second, fix the high direction and apply the degree-two to
degree-three shadow inequality to its link on x,y, then sum. These
are ordinary shadows of present cells and require no full-face
assumption.

A pure-A intruder is one of the following:

- a low unit, a low--low pair, a pure-low cubic, or a pure-low quartic;
- a cubic with two low factors and one high factor;
- a cubic with one low factor and two high factors.

High units miss the low part of the fixed arc. A quartic containing
a high factor also misses it, since the upper endpoint of the low
part is at most ceil(h/2). Pure-high cubics miss both parts.

There are at most 2 low units, n0 low pairs, 4 pure-low cubics and k0
pure-low quartics. Of the at most `p*n0` two-low--one-high cubics,
the u1 I3 cubics miss the arc. For a one-low--two-high cubic to
intrude, both its low--high pair divisors must be in I2: its raw tau
is below theta, whereas each high offset is at least ceil(h/2).
The number of these cubics is therefore at most
`C(l_x+1,2)+C(l_y+1,2)`. Thus

```
J_A <= 6+(p+1)n0+k0-u1
       +C(l_x+1,2)+C(l_y+1,2).                        (2L-COUNT)
```

On substituting into P and using (2L-SH), for a>=7 we obtain

```
P >= a-13+(5-a)n0
     +l_x(a+2-l_x)+l_y(a+2-l_y) >= 2-2a.             (2L-ROUGH)
```

Indeed the discarded terms are
`(a+1)u0-5k0 >= (a-21/4)u0` and
`(a+3)u1-3k1 >= (a-1)u1`. The minimum in n0 is at n0=3.
Also, if l>=2, the two star terms sum to at least 2a: if one star
has size at least 2, use
`s(a+2-s)>=2a` for `2<=s<=a-2`; otherwise both have size 1.
Consequently

```
l>=2  ==>  P>=2.                                    (2L-STARS)
```

The following gap is the reason a missing A pair pays the entire
rough loss.

**Macaulay gap.** If a>=4 and `2<=q<Q=C(a+1,2)`, then

```
(a+2)q-3q^{<2>} >= 2a-2.                            (MG2)
```

Proof. Write `q=C(j+1,2)+s`, `0<=s<=j`, `1<=j<=a-1`.
On this block, the left side is the concave quadratic

```
f_j(s)=(a-j)C(j+1,2)+(a+2)s-3s(s+1)/2.
```

It is enough to check its endpoints. The endpoint s=j is verified
by the exact factorization

```
f_j(j)-(2a-2)=(j-1)(a-1-j)(j+4)/2 >=0.
```

At s=0, j=1 is excluded because q>=2. For j=2 use
`3(a-2)>=2a-2`. For j>=3 use `j(a-j)>=a-1` and j+1>=4.
This proves MG2. By Macaulay, `u3+u4<=q^{<2>}`, hence

```
r_A>0, q>=2  ==> D3>=2a-2, P+D3>=0.                 (2L-MISS)
```

If q<=1, then u3+u4<=1, and
`W_A=3a(a+1)+(a-3)q-4(u3+u4)+LC>=0` for a>=7.
Here LC>=0 by the existing LC lemma. We may therefore assume
q>=2 whenever we assume W_A<0.

## 22. The full-quadratic case: two complementary arcs and Sidon packing

It remains to consider r_A=0 and l<=1. Now n0=3 and `D3=3t_A`.
Set

```
H0=h-L,       R=#{high A directions with t<theta-2L}.
```

We will prove the two independent bounds

```
P+D3 >= 4a-4+(a+1)l-6R;                             (2L-FIX)
P_H >= delta-(2a-2)-(3a-5)l,                         (2L-HIGHARC)
P_H=(a-1)+LC+2q2+k+delta-2J_{H0,A}.
```

The arc for H0 is the corrected arc `Y_H` in section 13, with
endpoint h+H0. Since `h-2H0=-delta`, P_H is exactly its pure-A
payment expression.

For 2L-FIX, let q_c be the number of the three low pairs in the
low part of the fixed arc, c0 the number of present pure-low
cubics, and t0=4-c0. A cold pair has tau<ceil(h/2); each of its
extensions by x or y has tau<h. The union of these extensions
contains at least q_c+1 distinct cubics if q_c>0. Therefore

```
u0+t0>=q_c+1   (q_c>0).
```

For u0=0,1,2,3,4, the largest possible k0 is respectively
0,1,2,3,5. At a=7 the corresponding lower bounds for
`(a+1)u0-5k0` are 0,3,6,9,7; they increase with a. The preceding
extension inequality, or this five-entry table directly, proves

```
(a+1)u0-5k0+3t0 >= 2q_c.                            (COLD2)
```

Every intruding two-low--one-high cubic uses a high direction
counted by R. The u1 I3 cubics also use such directions and miss
the arc. As l<=1, there are at most l one-low--two-high intruders.
Thus the more precise count is

```
J_A<=2+q_c+4+k0+3R-u1+l.
```

Substitute this count into P, use COLD2 with `D3>=3t0`, and
discard `(a+3)u1-3k1>=0`. This is 2L-FIX.

For 2L-HIGHARC, call a high A direction exceptional if t<H0.
Since every A pair is present, such a direction makes an I2 pair
with x. Hence there are at most l exceptional high directions.
An intruder with one low and two nonexceptional high factors is
impossible, because `L+H0=h`. A cubic supported only on high
directions and containing a nonexceptional direction is also
impossible: the other two high offsets sum to at least h.
There are at most 2p one-low--two-high candidates if l=1, and at
most one pure-high cubic. There are at most l exceptional high
units and l low--high I2 pairs. Counting all quartics, whether or
not they intrude, gives

```
J_{H0,A} <= 9+3p+(2p+3)l+k.                          (2L-HCOUNT)
```

Here the 9 counts 2 low units, 3 low pairs and 4 pure-low
cubics. Substitution yields 2L-HIGHARC after discarding
`(a+1)u0-5k0>=0` and `(a+1)u1-5k1>=0` by 2L-SH.
Notice that I3 mixed cubics can be cold in this wider arc; they
were **not** subtracted in 2L-HCOUNT.

We now use residue injectivity beyond arc occupancy. Apart from
at most l exceptions, the R high offsets lie in the integer window

```
[h-L,theta-2L),  of length w=ceil(delta/2).
```

Let n=max(0,R-l). All the pairs on these n directions are present.
Their residues are distinct. In particular their ordinary pair
sums are distinct. Therefore their C(n,2) positive differences are
distinct integers in `[1,w-1]`: equality of two distinct positive
differences would give two equal pair sums, including the possible
diagonal-pair case. Consequently

```
n(n-1)<=2w-2<=delta-1.                               (SIDON2)
```

**Arc alternative.** For a>=7, r_A=0 and l<=1,

```
P+D3>=0  or  P_H>=0.                                (ALT2)
```

For l=0, failure of both would give
`R>2(a-1)/3` and `delta<2a-2`. But

```
[2(a-1)/3][2(a-1)/3-1]-(2a-3)
 =(4a^2-32a+37)/9
 =(4(a-7)^2+24(a-7)+9)/9 >0.
```

This contradicts SIDON2. For l=1 and a=7,8,9, 2L-FIX is at least
9-a since R<=a-2. For a=10, its failure forces R=8; SIDON2 then
gives delta>=43, exactly the high-arc threshold 5a-7. Finally, if
a>=11 and both fail, `n=R-1>(5a-9)/6`. Hence

```
n(n-1)>[(5a-9)(5a-15)]/36 >=5a-8,
```

where the last difference, times 36, is

```
25a^2-300a+423
 =25(a-11)^2+250(a-11)+148 >0.
```

Again this contradicts `n(n-1)<=delta-1<5a-8`.
This proves ALT2 with symbolic verification of every unbounded
parameter range and explicit checks of a=7,8,9,10.

## 23. Paying for B,C,E and completing T2.2

The only nonpure intruders in the fixed arc are a low A times B,
a low A times C, and a low--low pair times B. Thus

```
J-J_A <= b(2+n0)+2c.                                (OUT2)
```

Let beta be the number of present low pairs with
`tau<theta-h=ceil(h/2)`. An intruding AAB cell must use one of
these pairs, giving the useful refinement

```
J-J_A <= b(2+beta)+2c.                              (OUT2b)
```

For r_A=0, l<=1, the H0 arc has the bounds

```
J_H-J_{H,A} <= b(2+l+q2)+c(2+l).                    (HOUT2)
```

Indeed AB and AC intruders must use a low or exceptional A
direction. An AAB intruder has AA tau<H0<h, hence uses an I2
pair; there are at most bq2 such cells. ABB and the remaining
mixed types miss the arc by their tau lower bounds.

For clarity use the weaker, valid version of I-LOW that retains
only D3 from Cdef. Define

```
A2=(a-1)(b+1)+G+LC+b u3+(c+e)(2q2+u3)+D3.
```

It is sufficient that, for one of our arcs,

```
A2+(b+2)q2+k-eta>=0.                               (PAY2)
```

With the fixed arc eta=2J, OUT2 makes its left side at least

```
P+D3 + b[a-1+q2+u3-2(2+n0)]
     +G+(c+e)(2q2+u3)-4c.                          (PAY2-F)
```

The C/E part is nonnegative whenever q>=2. For c>0 its c
contribution is at least `c[2+q+q2+u3]>=4c`; the e part is
nonnegative. If a>=8, the b coefficient is at least a-8>=0.
Thus 2L-MISS or 2L-STARS completes every case with r_A>0 or l>=2.

Suppose r_A=0,l=0. The same outside bound holds for the H0 arc,
because q2=3 and HOUT2 is 5b+2c, equal to OUT2. Its pure payment
is P_H, with the extra nonnegative D3 available. ALT2 therefore
completes this case for a>=8.

Suppose r_A=0,l=1. If b>=1, the fixed-arc bound is enough even
without ALT2: 2L-FIX is at least 9-a and the b coefficient in
PAY2-F is at least a-7. Their sum is at least 2 for a>=7. If b=0,
use ALT2. For the wider arc HOUT2 costs 6c, whereas the C part
of `G+(c+e)(2q2+u3)` is at least 10c since q2=4. This pays
the wider-arc outside cost. This completes all a>=8 cases and
also all a=7 cases except a small boundary considered next.

At a=7 the b coefficient of PAY2-F can be negative only when

```
n0=q2=3,  l=u3=0.                                   (B7)
```

Then k=0 and LC=24. Assuming W_A<0, Macaulay forces r_A<=1.
To see this, `q^{<2>}-q` is nondecreasing (each successive
Macaulay-growth increment is at least 1), and at q=26 it is
`71-26=45`. If q<=26, then

```
W_A=192+4q-4(u3+u4)>=192-4*45=12,
```

a contradiction.

If beta=3, then `4L_y<h`. Any high A direction with `3t<2h`
therefore makes a formal I2 pair with x. Because l=0, that pair
is absent. There are at most r_A such high directions. HIGH from
section 15 thus has p>=5-r_A. At r_A=0 its lower bound is at
least `24+C(7,3)-C(8,3)=3`. At r_A=1 use MG2, D3>=12;
the lower bound is at least
`24+C(6,3)-C(8,3)+5+12=5`. The nonnegative T is available
in both cases. Thus beta=3 is complete, for every b,c,e.

If beta<=2, OUT2b makes the b contribution at least b. At
r_A=1 the fixed pure payment is nonnegative by 2L-MISS. At
r_A=0, 2L-FIX is `P+D3>=24-6R`. If R<=4 it is
nonnegative. If R=5, SIDON2 gives delta>=21, so
`P_H>=delta-12>=9`. For b>=6, use the fixed arc and its lower
bound `-6+b>=0`. For b<=5, use the wider arc; its b cost in
B7 is at worst -b, leaving at least `9-b>=4`.
The C/E payments already proved apply. This completes B7 and
therefore the proof of T2.2.

For the semigroup translation, h=c_S-3m and t_i=n_i-m. A
direction is low precisely when `2n_i<c_S-m`. B,C,E directions
cannot be low. Thus at most two low directions is exactly
`2n3>=c_S-m`, with the convention in section 20.

## 24. General low population: a local-payment criterion and a three-low theorem

The counting part extends to any alpha. This is useful even though
the final two-low Sidon alternative has not yet been extended to
all alpha.

Let p=a-alpha, n0 be the number of present low--low pairs, and l_i
the number of I2 pairs between low direction i and the high
directions. Let c0 count all present pure-low cubics, u0 their I3
subfamily, and u1 the I3 cubics with two low and one high factor.
Let k0,k1 count quartics with respectively zero and one high
factor. Then

```
q2=n0+sum_i l_i,  u3=u0+u1,  k=k0+k1.
```

The same range proof as in section 21 gives, without any full-face
assumption,

```
J_A <= alpha+n0+c0+k0+p*n0-u1+sum_i C(l_i+1,2),
J-J_A <= b(alpha+n0)+alpha*c.                        (GEN-COUNT)
```

Every I3 mixed pure-A cubic has two low factors and one high
factor, so the u1 subtraction is valid for the fixed arc. A
quartic containing a high direction misses the fixed arc. A hot
one-low--two-high cubic forces both low--high pair divisors into
I2, as before.

**General local criterion (GLOC).** Put

```
Phi = D3+(a-1)-2alpha-2c0+(2alpha+1-a)n0
      +sum_i l_i(a+2-l_i)
      +(a+1)u0-5k0+(a+3)u1-3k1
      +b[a-1+q2+u3-2alpha-2n0]
      +G+(c+e)(2q2+u3)-2alpha*c.
```

For a>=3 in the P4 primary setting, `Phi>=0` implies `W>=0`.
This assertion is uniform in a,alpha,b,c,e. Proof: substitute
GEN-COUNT into the sufficient I-LOW payment
`A2+(b+2)q2+k-2J>=0`. Its lower bound is exactly Phi, by
coefficient comparison. No further bound on the low face is used.

For a simpler scalar version, let
`Q_alpha=C(alpha+1,2)` and `U_alpha=C(alpha+2,3)`. The shadows are

```
4k0<=(alpha+3)u0,      3k1<=(alpha+2)u1.
```

If `a>=2alpha+1` and alpha>=3, their terms in Phi are
nonnegative. Discarding the star terms, using n0<=Q_alpha and
c0<=U_alpha gives

```
P >= -M_alpha,
M_alpha=(a-2alpha-1)Q_alpha+2alpha+2U_alpha-a+1
       =(Q_alpha-1)a+2alpha+1
         -alpha(alpha+1)(4alpha-1)/6.                 (GEN-ROUGH)
```

Here `P=(a-1)+LC+2q2+k-2J_A` as in section 20. For example
`M_2=2a-2`, `M_3=5a-15`, `M_4=9a-41`. The alpha=2 statement
holds for a>=7 by its separately checked shadow signs.
The exact Phi, rather than this scalar relaxation, is retained
in the final frontier.

There is an unconditional additional exclusion for three lows.

**Theorem T2.3-M (three lows with at least three missing A pairs).**
In the primary setting, suppose alpha=3, a>=13 and r_A>=3.
Then `W>=0`, with no restrictions on b,c,e.

We need the following explicit Macaulay gap:

```
a>=13, 6<=q<=Q-3
  ==> (a+2)q-3q^{<2>} >=6a-18.                       (MG6)
```

To prove it, use the same concave blocks f_j(s) as in MG2. The
lower endpoints `(a-j)j(j+1)/2` for 3<=j<=a-1 have their minimum
at an endpoint: their derivative is a quadratic with negative
leading coefficient and one positive root, so the cubic first
increases and then decreases on j>=0. The two endpoint values
are `6a-18` and `a(a-1)/2`; the latter differs from 6a-18 by
`(a-4)(a-9)/2>=0`.

The upper endpoints f_j(j), for 3<=j<=a-2, have the same
increase-then-decrease property: their derivative is
`[-3j^2+2(a-4)j+3a+1]/2`, again with exactly one positive root.
Their endpoint values are

```
f_3(3)=9a-30,
f_{a-2}(a-2)=(a^2+3a-10)/2.
```

These exceed 6a-18 by respectively `3a-12` and
`[(a-4)(a-5)+6]/2`. In the last, truncated block j=a-1,
the top endpoint s=a-3 corresponds to q=Q-3 and equals
`6a-15`. Concavity now proves MG6 on every block.

For T2.3-M assume W_A<0, since otherwise transfer finishes.
Then q>=6: for q<=5, Macaulay gives u3+u4<=7, and
`W_A>=3a(a+1)-28>=0`. Thus MG6 applies and D3>=6a-18.
GEN-ROUGH with alpha=3 gives `P>=15-5a`, hence

```
P+D3>=a-3.
```

The fixed-arc b payment has coefficient
`a-1+q2+u3-6-2n0>=a-7-n0>=a-13>=0`.
The C part of `G+(c+e)(2q2+u3)` is at least
`c[2+q+q2+u3]>=8c`, paying the outside cost 6c; the E part is
nonnegative. Therefore the fixed-arc I-LOW payment is
nonnegative, proving T2.3-M.

## 25. The strongest exact HARC and a short-residue supplement for all h

**End-arc lemma (END).** For a residue-injective D, the exact loss

```
eta_H=h-2H+2J_H
```

is nonincreasing as integer H runs from ceil(h/2) to h-1.
Indeed `Y_{H+1}\Y_H` contains at most one residue. Thus
`J_{H+1}-J_H` is either 0 or 1, and
`eta_{H+1}-eta_H=-2+2(J_{H+1}-J_H)<=0`. The possible omitted
zero residue only makes the difference smaller.

Consequently, when h>=2, the exact best upper-core arc is always
H=h-1, and I-LOW is valid with

```
eta_end=min(3delta, 2-h+2J_{h-1}).                    (END-ETA)
```

This dominates the fixed arc and all actual-unit thresholds in
section 13. The smaller threshold H0=h-L remains useful for
*analytic upper bounds* on intruders, as in T2.2; END concerns
their exact counts. In particular, the cardinality-correct full
simplex relaxations of section 17, which are not residue
injective, cannot be used to invalidate END.

There is also a uniform version of ASR-small. Put

```
sigma=max(0,2h-m),
X_SR=#{cells among 0, A units, q2, u3, k with tau>=sigma}.
```

All the named cells have tau<h. The short-residue interval
`[2h,m+h) mod m` contains, among residues in `[0,h)`, exactly
`[sigma,h)`. This is immediate by separating h<=m/2 from
h>m/2. The new cells have disjoint types from SR's five families
and from H3. Residue injectivity therefore gives

```
rho >= t3+I+v3+w+z+H3+X_SR.                         (ASR-ALL)
W >= W_A+T+H3+X_SR;                                 (HOT-ALL)
W >= LC+C(p_hi+2,3)-F+5r_A+D3+T+X_SR.               (HIGH-ALL)
```

Here `p_hi=#{A directions with 3t>=2h}`, to distinguish it from
the high population p=a-alpha used in sections 20–24. HOT-ALL
follows by retaining these extra occupants in the short-residue
slack in the transfer identity. The proof of HIGH in section 15
then gives HIGH-ALL without further loss. When h<=m/2,
`X_SR=1+a+q2+u3+k`; this recovers ASR-small exactly. When
h>m/2, it is the requested analogue, counting the actual A-face
cells above the cutoff 2h-m. No X_SR term is asserted for I-LOW,
whose arc endpoint can have zero short-residue multiplier.

## 26. Three lows: a near-full-face certificate and bounded a

The two-low packing argument has a quantitative extension when
only a few A pairs are missing. We first record the exact loss
in the Sidon estimate.

**Partial Sidon lemma.** Suppose n distinct integer offsets lie
in an interval of length w. Among their formal unordered pairs,
including loops, suppose at most r are absent, and the present
pairs have distinct residues modulo m. Then

```
n(n-1) <= 2w-2+2r(r+1).                             (PSID)
```

Proof. In any group of equal *ordinary* pair sums, at most one
pair is present. With at most r absent pairs, the total number
of unordered collisions of pair sums is at most C(r+1,2).
This follows by writing the group excesses as g_i-1: their sum
is at most r, and `sum C(g_i,2)<=C(r+1,2)`.
Each equality of two distinct positive differences induces a
collision of pair sums. A pair-sum collision induces at most two
unordered equal-difference pairs; it induces only one if one of
the pair monomials is a loop. Thus the number of unordered
collisions among positive differences is at most r(r+1).
The excess number of differences above the number of distinct
differences is no larger than that collision count. Since the
distinct differences lie in `[1,w-1]`, we obtain
`C(n,2)<=w-1+r(r+1)`, proving PSID.

Now assume alpha=3, a>=13. Retain the notation of section 24,
and write r=r_A and l=sum l_i. If l>=6, the star sum pays the
entire scalar loss M_3=5a-15. In fact, if some l_i>=6,

```
l_i(a+2-l_i)>=min(6a-24,5a-15)>=5a-15,
```

using l_i<=a-3. Otherwise each l_i<=5 and their sum is at least
6, so the star sum is at least `6(a-3)>=5a-15`. Outside
payments are nonnegative just as in T2.3-M. Therefore

```
alpha=3, a>=13, l>=6  ==> W>=0.                     (3L-STARS)
```

By T2.3-M the only further case requiring analysis has

```
r in {0,1,2},  l in {0,1,2,3,4,5}.
```

Put H0=h-L, delta=h-2L, and let
`R=#{high A directions with t<theta-2L}` as before.
The following bounds hold:

```
P+D3 >= A_{r,l}(a)-12R,
A_{r,l}(a)=(7+l-2r)a-9+2l-l^2-5r;                  (3L-FIX)

P_H >= delta-B_{r,l}(a),
B_{r,l}(a)=(5+5l+7r)a-15-17l-13r
            +2 C(l+r+2,3).                         (3L-HIGHARC)
```

Here P and P_H have exactly the definitions of section 22,
with J_A and J_{H0,A} now for three low directions.

To prove 3L-FIX, let q_c count cold low--low pairs and let
t0=10-c0 count missing pure-low cubics. Each cold pair has three
extensions by low directions, all with tau<h. Each cubic has at
most three distinct pair divisors, so their union has at least
q_c cubics. Hence u0+t0>=q_c. The low-face shadow gives

```
(a+1)u0-5k0 >= (a-13/2)u0 >=3u0,
```

and consequently `(a+1)u0-5k0+3t0>=2q_c`.
Now use the sharper fixed-arc count

```
J_A<=3+q_c+10+k0+n0 R-u1+sum C(l_i+1,2).
```

Use `D3=3t_A-(a+2)r` to pay the cold pairs. The remaining bound
is

```
a-27+(a+3)n0+sum l_i(a+2-l_i)-2n0 R-(a+2)r.
```

Since `6-r<=n0<=6` and `sum l_i(a+2-l_i)>=l(a+2-l)`, it is
at least 3L-FIX. The discarded mixed shadow term is
`(a+3)u1-3k1>=0`, because `3k1<=5u1`.

For 3L-HIGHARC, there are at most l+r exceptional high
directions below H0. Every such direction makes a formal I2
pair with the lowest low direction, which is either present
and counted by l or absent and counted by r. Set e0=l+r.
Pure-high intruding cubics must be supported on these exceptions;
there are at most C(e0+2,3). One-low--two-high intruders must
use an exception; there are at most `3e0(a-3)` candidates.
There are at most l low--high I2 pairs, e0 exceptional units,
and at most `6(a-3)` two-low--one-high cubic candidates. Thus

```
J_{H0,A}<=19+l+e0+C(e0+2,3)
          +(6+3e0)(a-3)+k.
```

Substitution, using q2>=6-r+l, gives 3L-HIGHARC after
discarding `(a+1)u0-5k0` and `(a+1)u1-5k1`, both nonnegative
for a>=13. This derivation also counts all possible cold mixed
cubics and quartics.

At least n=max(0,R-l-r) of the R offsets lie in
`[h-L,theta-2L)`, of length ceil(delta/2). Applying PSID with
at most r missing A pairs gives

```
n(n-1)<=delta-1+2r(r+1).                            (3L-PACK)
```

It is essential to retain the Macaulay gap in the near-full
case. For r=1,2 the exact degree-two growth at q=Q-r gives

```
D3>=D_r(a)=r(4a-3r-1)/2.                            (NEAR-GAP)
```

There is also a sharper star exclusion. For r=0,1,2 put
`s0=5-2r`. If l>=s0, then the star sum is at least
`s0(a+2-s0)`. Indeed, if one star has size at least s0,
minimize its concave quadratic on `[s0,a-3]`; otherwise all
stars have size at most s0-1 and use their total size. The
two possible endpoint values are at least the asserted bound
for a>=13. The resulting lower bounds for P+D3 are respectively
0,10,9. The fixed-arc outside payments are nonnegative. Thus

```
alpha=3, a>=13, r<=2, l>=5-2r ==> W>=0.             (3L-GAP-STARS)
```

For r>=1, instead of charging the cold pairs to `3t_A`, simply
use q_c<=6 and retain D3. The sharper fixed payment is

```
P+D3 >= Ahat_{r,l}(a)-12R,
Ahat_{r,l}(a)=(7+r+l)a-21+2l-l^2-r(3r+7)/2.          (3L-SHARP)
```

Indeed the intermediate bound is
`a-39+(a+3)n0+sum l_i(a+2-l_i)-2n0 R+D3`; use
n0>=6-r, n0<=6, and NEAR-GAP. For r=0 retain the better
earlier bound, so set `Ahat_{0,l}=A_{0,l}`.
For all r=0,1,2 set D_0=0 and

```
Bhat_{r,l}=B_{r,l}-D_r,
P_H+D3>=delta-Bhat_{r,l}.                            (3L-HSHARP)
```

Here are explicit infinite-region certificates. For each row
and column of the next table, Wilf holds if a is at least the
displayed A. The table applies to alpha=3, r=r_A<=2,
l=sum l_i<=5 and arbitrary b,c,e.

| r \ l | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 16 | 26 | 33 | 37 | 41 | 43 |
| 1 | 32 | 37 | 40 | 43 | 45 | 47 |
| 2 | 39 | 42 | 44 | 46 | 47 | 49 |

For complete symbolic verification set

```
C(a)=Ahat_{r,l}(a)-12(l+r),
G_{r,l}(a)=C(a)[C(a)-12]
           -144[Bhat_{r,l}(a)-1+2r(r+1)].           (3L-POLY)
```

Explicitly, for r=0,
`C(a)=(7+l)a-9-10l-l^2`. For r=1,2,
`C(a)=(7+l+r)a-21-10l-l^2-r(3r+31)/2`.

Failure of both payments gives
`R>Ahat_{r,l}(a)/12` and `delta<Bhat_{r,l}(a)`. Hence
`n>C(a)/12`. In every displayed region C(a)>12; if G>=0,

```
n(n-1)>C(a)[C(a)-12]/144
       >=Bhat_{r,l}(a)-1+2r(r+1),
```

contrary to 3L-PACK. The following table gives **all three
coefficients** of `G_{r,l}(A+t)=g2*t^2+g1*t+g0` for t>=0.
They are nonnegative, verifying every infinite a-region.

| r | l | A | g2 | g1 | g0 |
|---:|---:|---:|---:|---:|---:|
|0|0|16|49|638|157|
|0|1|26|64|1472|112|
|0|2|33|81|2484|1296|
|0|3|37|100|3440|28|
|0|4|41|121|4760|3100|
|0|5|43|144|5904|144|
|1|0|32|64|1952|1852|
|1|1|37|81|2844|1936|
|1|2|40|100|3760|316|
|1|3|43|121|4980|2160|
|1|4|45|144|6240|2188|
|1|5|47|169|7752|4572|
|2|0|39|81|3006|253|
|2|1|42|100|4020|909|
|2|2|44|121|5112|828|
|2|3|46|144|6456|3421|
|2|4|47|169|7726|1141|
|2|5|49|196|9556|8293|

For example C(A)>12 follows at the smallest entry (r,l)=(0,0)
from C(16)=103 and is checked by direct substitution at the
other 17 listed endpoints; C increases with a since its slope
is at least 7.
These direct substitutions are also included in
`t3/three_low_table.py`.

Finally pay the outside directions. In the wider arc,

```
J_H-J_{H,A}<=b(3+l+r+q2)+c(3+l+r).
```

The b coefficient after pure payment is at least
`a-13-3l-2r`, nonnegative at every A in the table. The C part
of `G+(c+e)(2q2+u3)` is at least
`c[2+2(6-r+l)]`, which pays `2c(3+l+r)` since r<=2.
For the fixed arc the b coefficient is at least a-13, and
the C/E payment was already checked in T2.3-M. This completes
all 18 certificates.

**Theorem T2.3 (large-a three-low regime).** If alpha<=3 and
a>=41 in the primary setting, then W>=0. More precisely, for
alpha=3 and a>=13, the only possible remaining cases have
`r_A in {0,1,2}`, `0<=l<=4-2r_A`, and a strictly below the
corresponding table entry. The largest relevant entry is 41:
it is (r,l)=(0,4); the relevant maxima for r=1 and r=2 are
40 and 39. Entries for the other columns remain valid but
are superseded by 3L-GAP-STARS.
This is a bounded set of A-count parameters, not a claim that
the remaining semigroups themselves form a finite set.

## 27. Local signed packing and a finite three-low certificate

The bound a>=41 can be reduced by applying the **existing P4
signed packing lemma inside the high-unit window**, and by
removing the cubic defect already forced by missing pairs.
This gives a computer-assisted refinement with two independent
integer implementations. The two-low theorem remains entirely
analytic.

Write `H(n)=n(C(n,2)+1)`. Let lambda_n be the SP constant from
P4 section 17:

```
lambda_0=lambda_1=0,
lambda_2=1, lambda_3=2, lambda_4=4,
lambda_n=3n/2          if n>=5 and 3 divides n,
lambda_n=3(n-1)/2      if n>=5 and 3 does not divide n.
```

**Local SP lemma.** Suppose n selected A offsets lie in an
integer interval of length s, every pair on them is present,
and at most epsilon cubic monomials on them are missing. Then

```
3s-2 >= H(n)-lambda_n*epsilon.                       (LSP)
```

Translate their minimum to zero and use modulus `m'=3s-2`.
Pair sums lie in `[0,2s-2]`, and triple sums in `[0,3s-3]`.
Present pairs and triples have distinct ordinary sums because
their original residues are distinct. Thus the pair residues
are injective modulo m', and the full triple collision excess
is at most epsilon. Apply P4's SP lemma with its n-element
set B0. This proves LSP. The n=0,1 cases are immediate.

**Localization of the missing-cubic budget (uniform in alpha
and r_A).** Put

```
epsilon_M=q^{<2>}-(u3+u4)>=0.
```

The legal cubics are the formal A cubics all of whose pair
divisors are present. Together with zero, the A units and the
present A pairs, they form a down-set, so their number is at
most q^{<2>}. Every actual A cubic is legal. A selected set of
directions with all pairs present has no illegal cubic, and
its missing cubics are therefore among the absent legal
cubics. It has at most epsilon_M missing cubics. This proves
the localization assertion without any restriction on r_A or
the number of low directions.

For r=r_A in {0,1,2}, the exact Macaulay formula specializes to

```
t=t_A, t_forced=0,a,2a-1 respectively,
epsilon=t-t_forced>=0.                              (LOC-DEF)
```

Every cubic divisible by an absent pair is absent. There are a
distinct cubic multiples of a single missing pair; two missing
pairs have at least 2a-1 distinct cubic multiples, since their
two sets of multiples intersect in at most their one degree-3
least common multiple. None of these forced missing cubics
lies on a set of directions whose pairs are all present.
Consequently epsilon, rather than t, is a valid upper bound
for the missing cubics on **any** such selected set. This is
the important improvement over charging the entire global
defect to each window.

For alpha=3 and the notation of section 26, all R high offsets
lie in the window

```
[ceil(h/2),theta-2L),   length delta.
```

At least `max(0,R-l-r)` lie in the shorter window of length
`w=ceil(delta/2)`. Deleting one endpoint from each missing
pair loses at most r further directions and leaves every pair
present. Therefore LSP and LOC-DEF give

```
n_s=max(0,R-l-2r), n_w=max(0,R-r),
3w-2     >= H(n_s)-lambda_{n_s}*epsilon,
3delta-2 >= H(n_w)-lambda_{n_w}*epsilon.             (WINDOW-SP)
```

In fact WINDOW-SP is valid for any alpha>=1 and r_A, using
epsilon=epsilon_M: the exception and deletion counts use only
l and r_A, and the two window lengths do not depend on alpha.
The closed form LOC-DEF is needed only for the finite
three-low certificate below.

Two elementary counts, which do not require all the pairs to
be present, are also retained:

```
n_c=max(0,R-l-r),
C(n_c+2,3)-t <=3w-2,
C(R+2,3)-t   <=3delta-2,
R(R-1)<=2delta-2+2r(r+1).                           (WINDOW-COUNT)
```

The cubic inequalities count present cubics in the ordinary
sum interval; the last inequality is PSID in the wider window.

**Theorem T2.3F (bounded certificate).** In the primary setting,
if alpha<=3 and a>=16, then W>=0, for arbitrary b,c,e.
For a>=41 this is the analytic theorem of section 26. For
16<=a<=40 the following is a complete bounded certificate.

Assume W<0. Previous results give

```
r in {0,1,2}, 0<=l<=4-2r, 6-r<=n0<=6,
q2=n0+l, t>=t_forced,
4t<=F-(a+1)q2+(a-3)r-1,
D3=3t-(a+2)r, S_l=l(a+2-l), 0<=R<=a-3.
```

Here we used `LC_actual>=(a+1)q2`, which is a consequence
of W_A<0 in LC-minus, already verified by the lead. Define

```
F_rough=15-5a+S_l+D3,
F_cold =a-27+(a+3)n0+S_l-2n0 R-(a+2)r,
F_raw  =a-39+(a+3)n0+S_l-2n0 R+D3,
K=max(F_rough,F_cold,F_raw),
B_f=a-7-n0+l >=1,
B_h=a-7-n0-3l-2r,
e0=l+r,
B=2[13+n0+l+e0+C(e0+2,3)+(n0+3e0)(a-3)]
  -(a-1)-(a+3)(n0+l).
```

The fixed-arc full payment is at least `K+b B_f`. F_rough is
GEN-ROUGH retaining stars and D3. F_cold is the cold-pair
payment retaining n0 instead of replacing it by its extreme
values. F_raw uses the same count with `q_c<=6`, pays at most
12 for cold pairs, and retains D3. The H0-arc full payment is
at least `delta-B+D3+b B_h`, by the exact-n0 high-arc count.
The C/E terms in both payments are nonnegative, as proved in
section 26. Thus W<0 requires

```
K+b B_f<=-1,
1<=delta<=B-D3-b B_h-1.                             (FIN)
```

This is a finite parameter problem. Explicit complete bounds
are

```
0<=b<=5a-16,
t_forced<=t<=min(
 floor([F-(a+1)(n0+l)+(a-3)r-1]/4),
 floor([5a-16-S_l+(a+2)r]/3)).
```

The b bound follows from K>=F_rough>=15-5a and B_f>=1.
The second t bound follows from F_rough<0. For each tuple
(a,r,l,n0,t,R,b), test FIN, PSID, WINDOW-SP and WINDOW-COUNT.
No tuple survives for 16<=a<=40.

The independent programs [three_profiles.py](t3/three_profiles.py)
and [three_profiles.c](t3/three_profiles.c) implement the
certificate differently. Python solves the monotone packing
inequalities for a lower endpoint of delta. C enumerates every
integer delta up to FIN's upper endpoint and tests each original
inequality directly. They agree on the following complete
pre-packing profile counts:

```
a=14..40:
1573,1137,1018,992,1019,1054,1100,1166,1228,1304,1382,
1477,1569,1665,1761,1873,1989,2100,2217,2341,2464,2598,
2723,2864,3017,3160,3298.
```

The corresponding surviving profile counts are 46 at a=14,
13 at a=15, and zero at every a=16..40. Expanding the delta
intervals gives 1,302 surviving tuples below a=16. The two
implementations give the identical 64-bit rolling checksum
`2605186666962456684` for their ordered 59-profile list,
including both delta endpoints. That full list is saved as
[three_profiles_survivors.json](t3/three_profiles_survivors.json).
These are relaxed count profiles, not actual down-sets.

This completes T2.3F. Its finite computation is a stated proof
dependency. The analytic T2.3 and T2.2 do not depend on it.
For three lows, the remaining unbounded parameters have now
been restricted to a<=15; at a=14,15 their count data must lie
in the explicit 59-profile list in addition to the general
frontier inequalities below.
