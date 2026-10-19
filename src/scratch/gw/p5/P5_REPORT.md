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

There is also a uniform criterion from H0=h-L. For alpha>=1 put

```
p=a-alpha, l=sum l_i, E0=min(p,l+r_A),
C_H=alpha+n0+c0+l+E0+C(E0+2,3)+(n0+alpha*E0)p,
Psi=delta+(a-1)+(a+3)q2+D3+(a+1)u3-5k-2C_H
    +b[a-1+q2+u3-2(alpha+E0+q2)]
    +G+(c+e)(2q2+u3)-2c(alpha+E0).                  (HLOC)
```

For a>=3, `Psi>=0` also implies W>=0. Here E0 is an exception
count, not the number e of E units. At most E0 high directions
lie below H0: each gives a present low--high I2 pair with the
lowest direction, or one of the r_A missing pairs. An all-high
intruding cubic is supported on these exceptions; a
one-low--two-high intruder uses an exception. Thus

```
J_{H0,A}<=C_H+k,
J_{H0}-J_{H0,A}<=b(alpha+E0+q2)+c(alpha+E0).
```

The terms in C_H count low units, low pairs, pure-low cubics,
low--high I2 pairs, exceptional units, exceptional cubics,
two-low--one-high candidates and one-low--two-high candidates,
respectively. All quartics are counted separately by k; there
is no subtraction of cold I3 cubics. Substitute both bounds
into `A2+(b+2)q2+k+delta-2J_{H0}`. Its lower bound is exactly
Psi. This proves HLOC and supplies a second counts-only
payment criterion for every low population.

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

Equivalently, with `Delta_a(q)=(a+2)q-3q^{<2>}`,
`D3=Delta_a(q)+3epsilon_M`. Thus the localized defect used in
packing is also a retained positive payment in the arc identity.

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

There is a further useful finite-family reduction. For alpha=3,
a>=13, an unproved case must have **c=e=0**. We may assume
r<=2, since T2.3-M handles r>=3. In the fixed payment,
`P+D3>=-(5a-15)`, and the b coefficient is nonnegative.
Also q>=Q-2 and q2>=6-r>=4. If c>=1, the C part of the
outside remainder is at least

```
c[q+q2-4]>=Q-2.
```

If e>=1, its coefficient is even larger. But

```
Q-2-(5a-15)=(a^2-9a+26)/2>0.
```

Thus either outside class pays the entire rough loss.

At a=13 the only possible zero value of
`B_f=a-7-n0+l` is n0=6,l=0. Let beta count the low pairs
with tau<ceil(h/2), as in OUT2b. The exact b coefficient can
instead be bounded by

```
12+q2+u3-6-2beta=12+u3-2beta.
```

If u3>=1 or beta<=5, this coefficient is at least 1. In
the remaining case beta=6,u3=0, all low offsets are below h/4,
so all ten pure-low cubics have tau<h and are absent. Because
n0=6, every missing pair uses a high direction, and none of
its forced cubic multiples is pure low. Therefore
`t>=t_forced+10`, so `D3>=D_r+30`. Using c0=0 instead of the
upper bound 10 in GEN-COUNT gives P>=-30. Thus P+D3>=D_r>=0,
which already proves Wilf in this remaining case. Consequently
every *unclosed* a=13 case has a valid effective b coefficient
`max(1,B_f)`.

The finite scan can therefore also include a=13, replacing
B_f by max(1,B_f) there. Both implementations agree on 1,413
pre-packing profiles and 113 surviving profiles at a=13.
Together with the 59 at a=14,15, they give the complete saved
list [three_profiles_survivors_13.json](t3/three_profiles_survivors_13.json):
172 profiles, 4,863 expanded delta tuples, identical checksum
`13171536009687149148`. The largest b is 13 and the largest
d=a+b is 26.

Since c=e=0, the number of cells is bounded by all monomials
through degree 3 on d directions plus the degree-4 A monomials:

```
m<=C(d+3,3)+C(a+3,4).
```

Taking this bound over the 172 profiles gives **m<=5474**.
All A/B unit weights are less than 3m. Thus the remaining
alpha=3, 13<=a<=15 semigroup family is genuinely finite:
c=e=0, embedding dimension at most 27, multiplicity at most
5,474, and count data in the displayed 172-profile file, in
addition to END, ASR-ALL, LC-minus, MAC-minus and GLOC. No
exhaustive search of that finite semigroup family is asserted.

## 28. Preserved failures and explicit boundary witnesses

The smallest relaxed witness to unrestricted OL is retained in
section 17. Neither OL nor even the stronger fixed-arc assertion
`P+D3>=0` extends to two lows under residue completeness. A new
actual-semigroup witness, compressed from the targeted search, is

```
S=<985,1177,1183,1382,1393,1421,1437,1441> union [3524,infinity),
m=985, c_S=3524, h=569,
A offsets=(192,198,397,408,436,452,456),
a=7, b=c=0, e=865, alpha=2,
q2=3, q3=25, u3=k=0, u4=84,
r_A=D3=0, LC=24, W_A=-32,
J_A=19, P=P+D3=-2, P_H=183,
embedding dimension=873, ell=56, W=45364.
```

The tile consists of the full A simplex through degree 3
(120 cells) and 865 E units, one at each unused residue r,
with weight `3m+h+((r-h) mod m)`. Every one of its 985 residues
is distinct. Its 19 pure-A intruders are the four pure-low
cubics and all 15 two-low--one-high cubics. The wider arc pays
them. This is a counterexample to the proposed fixed pure-A
payment, not to Wilf or any verified GW theorem.

The complete tile is [compressed_counter.json](t3/fixtures/compressed_counter.json).
The independent tuple verifier checks down-closure, residue
bijection, all classes, the floor definition of W, closure of
the Apéry array under every generator, and minimality of every
unit. Thus the displayed S and its embedding dimension are
verified directly, in addition to the tile calculation.
The saved witness was reduced to m=985 in this continuation.
`compress_counter.py` minimized m in one fixed residue-order
cone and reported m=985; no global minimality assertion is
made. The smaller relaxed witness of section 17 remains part
of the record.

A separate incorrect subtraction was caught while deriving
2L-HCOUNT: an I3 cubic with two low factors and one high factor
**can** occupy the cold part of the wider H0 arc. The smallest
multiplicity for this phenomenon is 8. An explicit
residue-complete down-set has

```
m=h=8, weights=(9,11,12,39),
D=(0,x,x^2,y,z,xz,x^2z,E),
values=(0,9,18,11,12,21,30,39),
residues=(0,1,2,3,4,5,6,7).
```

The A offsets are (1,3,4), with two lows. At H0=7 the arc is
`[1,7)`; `x^2z` has tau=6<h, so it is an I3 cubic and an
intruder. This is a down-set witness, not an Apéry tile of
the semigroup generated by the listed unit weights.
To verify minimality, any such mixed I3 cubic has
`tau>=2+ceil(h/2)`, whereas the cold arc endpoint is at most
`2h-1-m`. For h<=m<=7 the former is at least the latter;
equality at m=h=7 still misses the half-open interval. The
displayed m=8 example therefore is minimal. Its full data are
[cold_mixed_minimal.json](t3/fixtures/cold_mixed_minimal.json).
The corrected high-arc counts in sections 22 and 26 count
these cubics and all possible quartics; they do not subtract u1.

Finally, [a7_beta3.json](t3/fixtures/a7_beta3.json) deliberately
exercises the exceptional a=7,b>0 branch, which the random
semigroup runs reached infrequently. It has

```
m=16000,h=4000,a=7,b=1,c=0,e=15878,alpha=2,
q2=3,q3=25,u3=k=0,u4=80,r_A=0,D3=12,
beta=3,W_A=-16,W=901220.
```

Its A offsets are (400,600,3601,3604,3616,3664,3856), and its
B offset is 4000. The B unit, both low AB cells and all three
low-pair-times-B cubics are present. The independent verifier
checks this as an actual residue-complete down-set. It is not
asserted to be a semigroup Apéry tile.

The [C-extension fixture](t3/fixtures/a7_beta3_C.json) adds a
C unit of weight 36100 and both low AC cells before completion.
It has c=1,e=15875,J=22 and W=916985. This separately tests
the two-low AC occupant bound with an actual C direction.

## 29. Computational checks for sections 20–28

Every mathematical run in this continuation was on fejer, in
`~/wilf/p7/`, at nice level 10, with at most four single-core
jobs. The laptop was used only to read, edit and copy files.
No commits were made. The final sources, data hashes and tool
versions are recorded in [MANIFEST.json](t3/MANIFEST.json) and
[SHA256SUMS](t3/SHA256SUMS). The environment was Python 3.12.3,
NumPy 2.5.4, SciPy 1.18.1 and GCC 13.3.0. No sympy dependency
is used.

The main actual-semigroup runs were:

| seed | attempts | m range | proposed lows | tile | primary instances | a>=7, exactly two lows |
|---:|---:|---|---:|---|---:|---:|
|202610202|100000|100–3000|2|lex|99122|72255|
|202610205|100000|100–3000|3|grlex|98736|3237|
|202610206|20000|5000–16000|3|grlex|19975|121|
|202610207|10000|5000–16000|3|lex|9987|50|
|202610210|10000|5000–16000|4|grlex|9984|13|

These are 237,804 primary semigroup instances across the five
runs; no assertion of pairwise distinct semigroups is made.
The proposed A population is 7–20 in the first two runs and
13–26 in the last three. Conductor recomputation and primitive
generator extraction occur before the final classification,
so the actual number of lows can differ from the proposed one.
Every chosen normal-form tile is checked for down-closure by
deleting each factor of each represented cell. The semigroup
membership array, actual conductor, Apéry array and minimal
generators are computed directly.

`two_low.h` independently recounts all two-low types, the two
arcs, outside occupants, the rough payment, COLD2, MG2, SIDON2,
the fixed/high alternatives and the final I-LOW/HIGH payments.
The first run includes 968 two-low instances with W_A<0, of
which 361 have a missing A pair. The saved compressed witness
also checks a negative fixed payment with W_A<0. No inequality
failure occurred.

`multi_low.h` checks the general GEN-COUNT, GLOC, END, ASR-ALL,
the three-low refined bounds and the applicable finite
certificate conclusions. The large grlex run exercised
T2.3-M on 243 deficient instances; the large lex run exercised
it on 123. The final four-low run additionally checks the
uniform legal-cubic localization and WINDOW-SP. A final
1,000-attempt control run, seed 202610212 in the same large-m
box, checks the final HLOC identity and occupant bounds;
its log is [uniform_hloc_check.log](t3/logs/uniform_hloc_check.log).
The saved boundary fixtures are read again by the final C
checker and by the independent Python tuple verifier.

The deliberate residue-complete down-set runs were:

- `two_tiles`, seed 202610204: 20,000 proposals, 100<=m<=3500,
  7<=a<=20, exactly two lows, all A pairs present. There were
  13,429 successful completions and 3,829 with W_A<0. Of these
  completions, 35 have negative actual P+D3, so the wider-arc
  branch is tested on genuine residue-complete objects. No
  two-low certificate failed.
- `two_tiles`, seed 202610208: 10,000 proposals, 500<=m<=5000,
  13<=a<=26, exactly three lows, all A pairs present. There
  were 5,444 successful completions, 896 with W_A<0, and
  4,842 instances in the refined three-low branches. The
  short/wide local SP bounds and the finite-certificate
  conclusion passed. The saved [three-low fixture](t3/fixtures/three_tile_fixture.json)
  is independently verified to be a semigroup Apéry tile.

These completions are built by checking residues and every
divisor before adding a cell, reserving h-1 for the maximum,
and filling all remaining residues by E axes. In general they
are residue-complete down-sets; semigroup closure is asserted
only for individually verified saved files.

The exact algebra audits are separate from actual-instance
experiments:

```
identities.py: 21 exact polynomial identities (fractions only);
three_low_table.py: all 18 infinite-region shifted polynomials;
MG2 grid: 4,544,456 (a,q) pairs, 7<=a<=300, min slack 0;
MG6 grid: 4,542,432 pairs, 13<=a<=300, no failure;
2L-ROUGH: 35,819,980 local-count tuples, 7<=a<=300;
COLD2: 10,340 tuples, 7<=a<=100;
ALT2: 998,970 count tuples, 7<=a<=1000.
```

The finite proof has 47,379 pre-packing profiles at a=16..40,
all excluded. The default a=14..40 audit has 50,089 profiles;
the a=13 extension has 51,502. The independent C and Python
checks agree on every per-a count and on both ordered
survivor-list checksums. The logs are
[Python](t3/logs/three_profiles.log),
[C](t3/logs/three_profiles_c.log),
[Python including a=13](t3/logs/three_profiles13.log), and
[C including a=13](t3/logs/three_profiles13_c.log).
These audits certify the bounded count calculation; they
are not exhaustive searches of numerical semigroups.

The targeted search on the genuinely remaining low population
uses [frontier_adversary.c](t3/frontier_adversary.c), seed
202610209, 5,000 proposals, m=1000..5000, a=13..24, four lows.
It extends negative-W_A A faces by up to 35 B directions,
testing 24 proposed additions at each step and selecting for
residue coverage and Wilf cost. It produced 149 negative-W_A
faces and completed every optimized object. No LOW+ violation
was found. Its closest saved completion is
[frontier_best.json](t3/fixtures/frontier_best.json):

```
m=2331,h=1109,a=13,b=35,c=0,e=576,alpha=4,
q2=14,q3=77,u3=k=0,u4=414,r_A=0,D3=123,
W_A=-4,W=325648,J_A=37,X_SR=28,
eta_end=-295,Phi=304743,
old LOW+ deficit=-304839.
```

It remains far from the remaining frontier. The source checks
the old transfer bounds throughout optimization and the full
new certificates on every final optimized completion. The
independent verifier confirms the saved down-set, cardinality,
residue bijection and maximum. It is not a semigroup Apéry
tile. Expanding this same E-heavy search would not establish
the missing uniform assertion.

Principal reproduction commands, all run on fejer, are:

```sh
cd ~/wilf/p7
nice -n 10 gcc -O2 two_semigroups.c -o two_semigroups
nice -n 10 gcc -O2 two_tiles.c -o two_tiles
nice -n 10 gcc -O2 frontier_adversary.c -o frontier_adversary
nice -n 10 gcc -O2 three_profiles.c -o three_profiles
nice -n 10 gcc -O2 read_sparse.c -o read_sparse
nice -n 10 ./two_semigroups 202610202 100000 100 3000 2 0
nice -n 10 ./two_semigroups 202610205 100000 100 3000 3 1
nice -n 10 ./two_semigroups 202610206 20000 5000 16000 3 1 13
nice -n 10 ./two_semigroups 202610207 10000 5000 16000 3 0 13
nice -n 10 ./two_semigroups 202610210 10000 5000 16000 4 1 13
nice -n 10 ./two_tiles 202610204 20000 100 3500 7
nice -n 10 ./two_tiles 202610208 10000 500 5000 13 3
nice -n 10 ./frontier_adversary 202610209 5000 1000 5000 1 4
nice -n 10 ~/mathenv/bin/python identities.py
nice -n 10 ~/mathenv/bin/python symbolic_two.py
nice -n 10 ~/mathenv/bin/python three_low_table.py
nice -n 10 ~/mathenv/bin/python three_profiles.py
nice -n 10 ./three_profiles
nice -n 10 ~/mathenv/bin/python three_profiles.py 13
nice -n 10 ./three_profiles 13
nice -n 10 ~/mathenv/bin/python verify_saved.py --fixtures \
  compressed_counter.json three_tile_fixture.json frontier_best.json
```

The compression run uses one HiGHS thread and exact integer
verification of its returned candidate. Its reported optimum
in a residue-order cone is not a theorem dependency. No
counterexample to Wilf or to a step of GW-24, GW-26 or GW-26c
was found.

## 30. Current exact frontier and the next lemma

The full primary regime remains unproved. The new established
results are T2.2 (all two-low cases, analytic), T2.3 (three
lows with a>=41, analytic), and T2.3F (three lows with a>=16,
with an explicit independently audited finite certificate).
During this continuation the lead independently verified T2.2
and recorded it as GW-26d in PROOFS.md. The later three-low
claims and finite-family reduction are supplied here for the
lead's independent review; no such review is claimed for them.
The counts-only criteria GLOC and HLOC, END-ETA, ASR-ALL and
the localized WINDOW-SP bounds hold for every low population.

After combining these with the verified GW-24/26/26c results,
any remaining counterexample must satisfy a>=7, alpha>=3,
delta>0, LC-minus, LP-low and MAC-minus. With Astar and Cdef
as in section 13, it must also satisfy

```
eta_end > Astar+(b+2)q2+k;
W_A+T+H3+X_SR <0;
LC+C(p_hi+2,3)-F+5r_A+D3+T+X_SR <0;
Phi<0, Psi<0.                                      (NEW-FRONTIER)
```

All applicable WINDOW-SP and WINDOW-COUNT inequalities must
hold, with the localized defect
`epsilon_M=q^{<2>}-(u3+u4)` and
`D3=Delta_a(q)+3epsilon_M`. In particular:

- if alpha=3 and 7<=a<=12, the remaining family is the small
  A-dimension family satisfying these necessary conditions;
- if alpha=3 and 13<=a<=15, it is the explicit finite family
  with c=e=0, d<=26, m<=5474 and count data in the saved
  172-profile file;
- alpha>=4 remains an unbounded family subject to the displayed
  structural conditions. No uniform theorem for that family is
  claimed.

The next precise uniform target is the following **unproved
four-low payment lemma**: for an actual residue-complete primary
down-set with alpha=4 and a>=7,

```
max(Phi, Psi, W_A+T+H3+X_SR)>=0.                     (Q4)
```

Any of its three alternatives proves Wilf. The mechanism to
test is to convert WINDOW-SP's required epsilon_M into the
retained payment `3epsilon_M` in D3, while accounting for the
low-star links and the missing-pair vertex cover. A relaxed
count counterexample to Q4 would be useful only after checking
whether its shifted pair/cubic residues can be injected. The
fixed pure-A payment already fails on an actual semigroup, so
that stronger assertion will not be reused.

There is a separate finite target: eliminate the 172 small
three-low profiles with global A/B signed packing, using
c=e=0, d<=26 and m<=5474. The scalar window counts leave these
profiles; no actual counterexample near them was found. The
current adversarial search is dominated by outside E payment,
so enlarging its same random boxes is discontinued. The next
search should impose the finite profiles or the four-low
localized-defect constraints before attempting residue-complete
realization. This is the strategic gap after this continuation,
not an assertion that all other proof methods are exhausted.

## 31. Joint low/high packing (continuation, 2026-10-19)

Sections 1–30 are retained as the historical record. The lead has
independently reviewed the identities and certificates described
in his continuation request. The new results below supersede the
frontier in section 30. They do not prove the full primary regime.
All notation and the exact residue-complete down-set hypotheses
remain those of sections 1 and 20–27.

Put `Q_alpha=C(alpha+1,2)`, `U_alpha=C(alpha+2,3)`,
`t=U-u3-u4`, `r=r_A`, and

```
epsilon=q^{<2>}-(u3+u4),
theta=ceil(3h/2), delta=h-2L>0,
R=#{high A units with t_j<theta-2L}.
```

**JOINT-SP/COUNT (the lead's lemma, re-checked here).** For every
alpha>=1, set `s=ceil(3delta/2)` and `n=max(0,alpha+R-r)`. Then

```
3s-2 >= H(n)-lambda_n*epsilon,                       (JOINT-SP)
3s-2 >= C(alpha+R+2,3)-t.                            (JOINT-COUNT)
```

Proof. All lows and the R indicated highs lie in the single integer
interval `[L,theta-2L)`. Indeed `theta-2L>h/2`, whereas every low
has offset below h/2. The interval has exactly
`theta-3L=ceil(3delta/2)` integers. Delete an endpoint of each
missing pair on these directions, deleting the only endpoint if
it is a loop. This leaves at least alpha+R-r directions with all
pairs present. Section 27's localization gives at most epsilon
missing cubics on them; LSP proves JOINT-SP. On all alpha+R
directions there are at least `C(alpha+R+2,3)-t` present cubics.
Their distinct ordinary sums lie in an interval of 3s-2 integers.
This proves JOINT-COUNT. There is no restriction on a, r or alpha.

The new scripts are in `src/scratch/gw/p5/t4/`. `joint_profiles.py`
uses integer endpoint bounds; `joint_profiles.c` enumerates every
delta. On the section 27 FIN range 13<=a<=40 they both give
51,502 pre-packing profiles and exactly 11 JOINT survivors, with
101 expanded delta tuples and ordered checksum
`16894550478840797404`. There are none for a>=14. The 11 rows are
exactly those supplied by the lead. Thus JOINT-SP alone extends
the section 27 certificate from a>=16 to a>=14. The next two
sections eliminate a=13 as well.

## 32. Signed packing without deleting missing-pair endpoints

The following bound is useful when the legal cubic defect is
small. It does not assume pair injectivity on the absent pairs.

**Partial signed packing (PSP).** Let n distinct integers lie in
an interval of s integers. Specify at most r absent unordered
pairs, with loops allowed, and some present cubics. Suppose the
present pairs have distinct sums and the present cubics have
distinct sums. A cubic is legal when all its pair divisors are
present. Suppose at most epsilon legal cubics are absent. Then

```
3s-2 >= H(n)-4 C(r+1,2)
         -9[n C(r+1,2)+(r+1)epsilon+C(epsilon,2)].    (PSP)
```

The same conclusion, with m on the left, holds directly in Z/m
when unit residues are distinct and present pair and cubic
residues are injective.

Proof. Let E2 and E3 be the numbers of unordered collision pairs
of formal pair and triple sums, respectively, in the ambient
group. At most one formal pair per sum is present. Consequently
`E2<=C(r+1,2)`: if the fiber excesses are e_i, their sum is at
most r and `sum C(e_i+1,2)<=C(r+1,2)`.

There are `n C(n,2)` normal signed labels `(p,q;x)`, with
p,q different from x, and n unit labels. A collision between a
normal signed label and a unit comes from a collision of two
distinct pair monomials. Each such pair collision gives at most
four normal labels of this kind (choose the positive pair and
the negative member of the other pair). Hence their total loss
is at most 4E2. A collision of two distinct normal labels maps
to a collision of two distinct triple monomials by moving the
negative entries across. The triples cannot be the same formal
monomial: normality would then force the labels to be identical.
Each unordered triple collision gives at most nine unordered
normal-label collision pairs, by choosing one support member
from each triple. Thus the represented union has size at least
`H(n)-4E2-9E3`. This argument also permits intersecting triple
supports.

Partition the absent cubics into the illegal family F, of size f,
and the absent legal family E, of size at most epsilon. For each
absent pair, its n cubic multiples have distinct sums, since the
units are distinct. Therefore `f<=nr`, each sum fiber of F has
size at most r, and the number of collision pairs within F is
at most `n C(r,2)`. The last assertion follows by assigning each
illegal cubic to one of its absent pair divisors: two different
assigned pair families have at most n matches. Each F cubic has
at most one collision with a present cubic. Each E cubic has
at most r collisions with F and at most one with a present
cubic. Finally E has at most C(epsilon,2) internal collision
pairs. It follows that

```
E3 <= nr+n C(r,2)+(r+1)epsilon+C(epsilon,2).
```

This proves PSP in a group. For the interval assertion translate
the minimum to zero and take modulus 3s-2. Pair and triple
sums have spans 2s-2 and 3s-3, so equality modulo this modulus
is ordinary equality. QED.

Two refinements used only for the 11 rows are worth recording.
With one missing pair there are exactly n illegal cubics and
no internal F collisions. Thus the PSP loss is
`4+9[n+2epsilon+C(epsilon,2)]`.
With two missing pairs sharing a factor, f=2n-1. Their sums
are different. A fixed nonzero ordinary unit difference has
multiplicity at most four: C(v,2)<=2E2<=6, since each pair-sum
collision induces at most two equal-difference pairs. One match
between the two translated pair families is their common formal
cubic. Hence F has at most three nontrivial internal collisions.
The improved loss is

```
12+9[2n+2+3epsilon+C(epsilon,2)].                   (PSP-2*)
```

If the two missing pairs do not share a factor, their 2n cubic
multiples are distinct formal monomials and have at most n
internal collision pairs. With epsilon=0 the loss is at most
`12+27n`. These statements retain the pair endpoints throughout.

For the 11 JOINT rows n=a=13. For r=1, t=13 and 14 give lower
bounds 906 and 888, respectively, for `3ceil(3delta/2)-2`; their
largest allowed values are 889 and 808. For r=2,t=25 the missing
pairs must share a factor; PSP-2* gives 763, versus at most 682.
For r=2,t=26, sharing a factor gives at least 736, and disjoint
pairs give at least 664; the allowed value is at most 616. All
11 are impossible. Both new FIN implementations check these
integer comparisons.

## 33. Cold low pairs pay without spending D3

Here is a simpler independent elimination of the 11 rows, and
a useful improvement for every alpha.

Let beta be the number of present low--low pairs with
`tau<ceil(h/2)`. Let `t0=U_alpha-c0`. Every extension of such a
pair by any low unit has tau<h. Weighted shadow incidence gives

```
(alpha+2)beta <= 3(u0+t0).                         (COLD)
```

Indeed a quadratic receives total incoming weight alpha+2;
each resulting cubic receives total weight at most three. A
resulting cubic is either an I3 pure-low cubic or an absent
pure-low cubic. Absence includes illegality.

Every two-low--one-high cubic that enters the fixed arc uses
a high direction counted by R. The sharper intruder count is

```
J_A <= alpha+beta+c0+k0+n0 R-u1+sum_i C(l_i+1,2).
```

The same range proof as section 26 proves this: present low
pairs in the arc are cold; pure-low cubics contribute at most
c0; hot one-low--two-high cubics force their two low--high
divisors into I2; an I3 two-low--one-high cubic is outside the
fixed arc and can be subtracted. Quartics with a high factor
do not enter this arc.

Put `S=sum l_i(a+2-l_i)` and `P=a-1+LC+2q2+k-2J_A`. Then

```
P+D3 >= D3+a-1-2alpha-2beta-2c0+(a+3)n0+S-2n0 R
          +(a+1)u0-5k0+(a+3)u1-3k1.               (R-EXACT)
```

Suppose alpha>=3, a+1>=alpha, and

```
(alpha+2)(4a-5alpha-11)>=24.                       (COLD-SIGN)
```

The shadows give `(a+1)u0-5k0 >= A u0`, where
`A=(4a-5alpha-11)/4>=6/(alpha+2)`, and
`(a+3)u1-3k1 >=(a+1-alpha)u1>=0`. Since
`min(A,2)(u0+t0)>=2beta` by COLD, R-EXACT proves

```
P+D3 >= D3+a-1-2alpha-2U_alpha
          +(a+3)n0+S-2n0 R.                       (COLD-FIX)
```

In particular D3 is retained in full. This corrects no previous
inequality; it strengthens the earlier cold-payment lower bound,
which had already replaced c0 by U_alpha before paying cold pairs.

For the 11 rows `(alpha,a,n0,R)=(3,13,6,10)`, COLD-FIX is
`-38+S+D3`. For r=1,l=1 it is 0 or 3, and for r=2,l=0 it is
7 or 10. The fixed outside coefficients from section 27 are
nonnegative in all these rows, so I-LOW proves W>=0 directly.

**Theorem T2.3G.** Under the exact primary P4 hypotheses,
alpha=3 and a>=13 imply W>=0, for all b,c,e. Proof: section 26
covers a>=41 and excludes r>=3 and the large-star cases; the
independently implemented FIN enumeration on 13<=a<=40, with
JOINT-SP, leaves only the 11 rows. Either PSP in section 32 or
COLD-FIX eliminates them. This theorem retains the finite
certificate dependency; it is not claimed to be an all-paper
replacement for FIN.

## 34. Exact uniform R and delta bounds, with outside directions

This section gives quantified versions of the lead's heuristic.
No signs are suppressed. Let `E=min(a-alpha,l+r)` and define

```
beta_H=#{present low--low pairs with tau<h-L},
B_f=a-1+q2+u3-2alpha-2beta,
B_H=a-1+q2+u3-2(alpha+E+l+beta_H),
Omega_f=G+(c+e)(2q2+u3)-2alpha*c,
Omega_H=G+(c+e)(2q2+u3)-2(alpha+E)c,
C_H=alpha+n0+c0+l+E+C(E+2,3)+(n0+alpha E)(a-alpha).
```

The sharper outside bounds are

```
J-J_A <= b(alpha+beta)+alpha*c,
J_H-J_{H,A} <= b(alpha+E+l+beta_H)+c(alpha+E),
beta_H <= min(n0,u0+t0).                           (H-COLD)
```

For the fixed arc an AAB intruder has two low A factors and
its AA divisor is cold; its B offset is at least h. For H0=h-L,
an intruding AAB's I2 divisor has tau<H0. Its low--low choices
are counted by beta_H and its remaining choices by l. Low and
exceptional AB or AC cells account for alpha+E. Finally multiply
each pair counted by beta_H by the lowest low unit: the resulting
distinct formal pure-low cubics have tau<h, and are counted by
u0 or t0. These arguments prove all three bounds.

In a counterexample, the fixed I-LOW payment is negative. Under
COLD-SIGN, COLD-FIX therefore implies the exact necessary bound

```
2n0 R >= D3+a-2alpha-2U_alpha+(a+3)n0+S
             +b B_f+Omega_f.                       (R-LOW)
```

The extra 1 comes from the negative integer payment being at
most -1. When n0>0, divide by 2n0 and take the ceiling. Without
COLD-SIGN use R-EXACT instead, with its displayed shadow terms;
this gives a valid exact bound for every a>=3. When n0=0 the
same formula is interpreted as a direct payment test, not a
division.

The H0 payment is bounded below by

```
delta+a-1+(a+3)q2+D3+(a+1)u3-5k-2C_H
       +b B_H+Omega_H.
```

Consequently every counterexample satisfies

```
delta <= 2C_H-(a-1)-(a+3)q2-(a+1)u3+5k
                -D3-b B_H-Omega_H-1.               (DELTA-UP)
```

This version requires no shadow-sign hypothesis. If
`a+1>=5(alpha+3)/4` and `a+1>=5(alpha+2)/3`, the term
`(a+1)u3-5k` is nonnegative and can be dropped. The resulting
constant, before the `-D3-b B_H-Omega_H-1`, is exactly

```
(a-2alpha-1)n0+2c0+2alpha-a+1-(a+1)l
 +2E[1+alpha(a-alpha)]+2C(E+2,3).                    (B-EXACT)
```

When l=0, u1=k1=0, so only the first shadow-sign condition is
needed. R-LOW, DELTA-UP and JOINT-SP/COUNT are the requested
general-alpha inequalities. They explicitly exhibit two potential
escapes: a large localized cubic defect and a negative outside
B coefficient. Sections 35–38 give further control of each.

## 35. Localized low defects, cold Macaulay, and hot high cubics

Three uniform refinements make the general-alpha conditions
substantially sharper.

**LOC-LOW.** With `r_LL=Q_alpha-n0`,

```
t0 <= alpha*r_LL+epsilon,       c0<=n0^{<2>}.         (LOC-LOW)
```

Proof. Each missing low pair has alpha formal pure-low cubic
multiples. Their union has size at most alpha*r_LL. Every other
absent pure-low cubic is legal, and there are at most epsilon
absent legal A cubics in total by section 27. The second bound
is Macaulay on the pure-low face.

**COLD-MAC.** With beta as in section 33,

```
u0+t0 >= U_alpha-(Q_alpha-beta)^{<2>}.               (COLD-MAC)
```

Proof. All formal cubics extending one of the beta cold pairs
have tau<h. The complementary cubics have all pair divisors in
the other Q_alpha-beta formal low pairs. Their number is at
most `(Q_alpha-beta)^{<2>}` by Macaulay. Every extended cubic
is either counted by u0 or absent and counted by t0. This proves
the assertion. COLD-MAC is stronger than the weighted incidence
bound COLD; it uses all formal low pairs in the complement,
regardless of whether that complementary pair is present in D.

We also have the mixed weighted shadow

```
2u1 <= (alpha+1)l,   u1<=n0(a-alpha).               (LLH)
```

For the first inequality count the total low exponent two in
an I3 LLH cubic against its low--high I2 pair divisors. Such a
pair has total possible incoming low weight alpha+1. The second
follows by deleting the high factor.

**COLD-HIGH.** Suppose beta>=1. Put p=a-alpha, E=min(p,l+r),
and for 0<=j<=E put

```
n_j=p-j,
r_j=max(0,r-r_LL-max(0,j-l)).
H_cold=max(0, C(p-E+2,3)-t+t0,
                min_{0<=j<=E}[C(n_j+2,3)-n_j*r_j-epsilon]).
```

Then `H3>=H_cold`, and hence

```
W >= W_A+T+H_cold+X_SR.                            (COLD-HIGH)
```

Proof. A cold pair has tau>=2L, so beta>=1 implies L<h/4.
Every high unit at least H0=h-L is then above 3h/4, and all
cubics on such units have tau>2h. If exactly j high units
lie below H0, j<=l+r. At least max(0,j-l) of the lowest-low/high
pairs are absent, in addition to r_LL absent low pairs. Thus
at most r_j missing pairs can be entirely on the other n_j
high directions. At most n_j*r_j cubics there are illegal, and
at most epsilon legal ones are absent. This gives the minimum
term in H_cold. Independently, the t0 absent pure-low cubics
are disjoint from this high family, so at least
`C(p-E+2,3)-(t-t0)` high cubics are present. ASR-ALL supplies
the final W inequality. All estimates hold with j or n_j zero.

The large-fiber obstruction below is not an obstruction to
these three statements. In particular LOC-LOW prevents charging
all missing A cubics to the low face when most are already
forced by pairs outside that face.

## 36. A uniform small-defect theorem, including a<=2alpha+1

**Theorem U-SMALL.** Under the exact primary P4 hypotheses,
suppose alpha>=4, `r_A=0`, `l=0`, and

```
epsilon <= Q_alpha/4.
```

Then W>=0 for every a,b,c,e. Thus this is a theorem for every
low population, including the strip a<=2alpha+1; alpha is not
bounded and a does not need to exceed 13.

Proof. Assume W<0. Write Q0=Q_alpha, U0=U_alpha. The hypotheses
give n0=q2=Q0, u1=k1=0 and `t=epsilon`. LC-minus implies

```
a(a-1)>3alpha(alpha+1),   a>5alpha/3+1.              (A-LOW)
```

For the second assertion evaluate a(a-1) at 5alpha/3+1:
its difference from 3alpha(alpha+1) is
`-2alpha^2/9-4alpha/3<0`, and a(a-1) increases in this range.
COLD-SIGN holds: for alpha>=6, A-LOW gives
`4a-5alpha-11>5alpha/3-7`, whose product with alpha+2 is
at least 24. For alpha=4,5 the first inequality forces a>=9,11,
respectively, and direct substitution verifies COLD-SIGN.
In particular `(a+1)u0-5k0>=0` for the H0 payment.

LOC-LOW gives t0<=epsilon. COLD implies
`u0>=(alpha+2)beta/3-t0`. Consequently

```
B_f >= a-1-2alpha+Q0-t0+(alpha-4)beta/3
    >= Q0-epsilon-alpha/3 >= 3Q0/5.                (UF)
```

Here alpha/3<=2Q0/15 for alpha>=4, so the penultimate bound
is in fact at least 37Q0/60. Also H-COLD implies
`Q0+u0-2beta_H>=-t0`, by splitting at u0+t0=Q0. Thus

```
B_H >= a-1-2alpha-t0 >= -alpha/3-Q0/4 >= -2Q0/5.  (UH)
```

Both Omega terms in section 34 are nonnegative: E=0 and
their C coefficients are at least `2+Q+Q0-2alpha>0`; their
E coefficients are positive as well.

The negative fixed payment and COLD-FIX now force, with n=alpha+R,

```
n > a/2+2alpha/3+5/6+(a-1-2alpha)/(2Q0)
                       +3epsilon/(2Q0)+3b/10
  > nu := a/2+2alpha/3+3/4+3b/10.                  (UN)
```

Indeed `(a-1-2alpha)/(2Q0)>-1/[3(alpha+1)]>=-1/15`.
Set

```
B0=(a-2alpha-1)Q0+2U0+2alpha-a+1.
```

The H0 payment, using c0<=U0, its nonnegative u0/k0 term,
and UH, gives the necessary inequality

```
delta <= B0+(2/5)bQ0-1.                            (UD)
```

The -1 remains valid despite the rational lower coefficient:
the actual payment is a negative integer, and every real lower
bound for it is therefore at most -1.

All pairs on the joint n directions are present. JOINT-SP,
`lambda_n<=3n/2`, and epsilon<=Q0/4 give

```
2[3ceil(3delta/2)-2]
 >= f(n):=n^3-n^2+2n-(3/4)nQ0.
```

The polynomial f is increasing for n>=alpha: its derivative
is at least `(21alpha^2-19alpha+16)/8>0`. Since n>nu>alpha,
and `2[3ceil(3delta/2)-2]<=9delta-1`, UN and UD contradict

```
f(nu)-9B0-(18/5)bQ0+10 >0.                        (U-POLY)
```

Here is a complete certificate for this last inequality. Put
`x=a-5alpha/3-1>0`, `z=alpha-4>=0`. The left side of U-POLY
is identically

```
(9alpha/8)(x-7alpha/12-1/4)^2
 +(119z^3+1086z^2+2559z+2126)/128
 +(355/32)x+(11/16)x^2+x^3/8
 +b[201/160+(33/40)x+(9/40)x^2+(9/16)alpha
                         +(27/20)alpha*x+(9/80)alpha^2]
 +b^2[99/400+(27/200)x+(81/200)alpha]+(27/1000)b^3.
```

Every displayed summand is nonnegative and the second is
strictly positive. `uniform_polys.py` verifies this identity
in an exact sparse Fraction polynomial ring. This proves
U-SMALL. For alpha=4 the test specializes to r=l=0,t<=2;
it is one test of a uniform mechanism, not a four-low endpoint.

There is a useful complement that removes the small-defect
hypothesis on the low-dimensional, B-free side.

**Corollary U-B0.** Suppose alpha>=4, r=l=0 and b=0. If
`a<=2alpha+2`, then W>=0, with no restriction on epsilon,c,e.
For general a, a counterexample in this B-free full-pair family
must satisfy the explicit middle-defect restriction

```
Q_alpha/4 < epsilon
 <= [(a-2alpha-1)Q_alpha-2a+3alpha]/6.              (MID-B0)
```

Proof. For b=0 retain the u0,k0 terms in DELTA-UP. Its bound
is `delta<=B1-D3-1`, apart from a nonnegative C/E payment, with

```
B1=(a-2alpha-1)Q_alpha+2c0+2alpha-a+1
                                      -(a+1)u0+5k0.
```

Violation of LOW+ requires
`3delta>=a-1+(a+1)(Q_alpha+u0)-3k0+D3+2Q_alpha+1`,
again with nonnegative outside terms. Subtract three times
the upper bound for delta from this lower bound. The result
is exactly

```
4a-6alpha+(6alpha+6-2a)Q_alpha-6c0
                           +4(a+1)u0-18k0+4D3.
```

Using c0<=U_alpha and 4k0<=(alpha+3)u0 makes it at least

```
4a-6alpha+2(2alpha+1-a)Q_alpha+4D3.                 (LOW-H)
```

The discarded u0 coefficient is nonnegative because
`8a-9alpha-19>0` follows from A-LOW for alpha>=4. The outside
remainder is at least
`4G+4(c+e)(2Q_alpha+u0)-6alpha*c>=0`.
Since D3=3epsilon and 4a-6alpha>0, LOW-H is positive for
a<=2alpha+1. For a=2alpha+2 it is positive whenever
epsilon>Q_alpha/4; the complementary range is U-SMALL.
For general a, LOW-H must be nonpositive in a counterexample,
which gives the upper bound in MID-B0. U-SMALL gives its
strict lower bound. The identity is verified by
`uniform_identities.py`. This quantifies an actual gap in the
current uniform argument rather than hiding it in an asymptotic
statement: MID-B0 can be nonempty when a grows faster than
2alpha.

## 37. What an n-independent signed-loss assertion cannot say

The following precise proposed strengthening is false:

> There is an absolute C such that, for every pair-distinct
> n-element integer set B with triple collision excess epsilon,
> the union of B and its normal signed-label sums has at least
> H(n)-C*epsilon elements.

For every g>=2 take independent formal coordinates A_i,B_i,Z,
and the 3g vectors `A_i,B_i,Z-A_i-B_i`. All pairs are distinct.
The only triple collision is the fiber of g triples
`A_i+B_i+(Z-A_i-B_i)=Z`. To obtain explicit positive integers
after a common translation, choose `R=10^(4g)` and, for
0<=i<g, use

```
R+10^(2i), R+10^(2i+1), 2R-10^(2i)-10^(2i+1).       (HF-FAMILY)
```

Base-ten coefficient comparison is valid: a difference of two
sums of degree at most three has digit coefficients of absolute
value at most six, and its lower part has absolute value less
than R. In the free-coordinate description a relation has
equal coefficients on A_i,B_i and the i-th third vector.
Its Z coefficient then forces their sum to be zero. At degrees
at most three, the only nonzero possibilities are the difference
of two indicated squarefree triples. This also rules out
relations between different total degrees at most three.

Thus epsilon=g-1, there is a single fiber of size g, and
all its triple supports are disjoint. For each i<j its nine
choices of one member from each support give nine signed-label
collisions. Each collision fiber has size two: its common
signed sum is `4R-p-q`, and pair distinctness makes p+q unique.
There are no other signed collisions, and no signed label equals
a unit. Consequently the union has exactly

```
H(3g)-9 C(g,2),
[H(3g)-union]/epsilon=9g/2.                         (HF-LOSS)
```

This ratio is unbounded. For the particular false choice C=12,
g=3 gives n=9, epsilon=2, H(9)=333 and union size 306, smaller
than 333-24. The dimension n=9 is minimal for that value C:
the verified SP constants for n<=8 are at most 12. No minimum
diameter claim is made for the explicit base-ten witness.

This is not merely an abstract support partition. It also
occurs inside residue-complete primary tiles satisfying LC-minus.
Add the following 2g high A offsets to HF-FAMILY:

```
3R-10^(2g+j),  0<=j<2g;
a=5g, alpha=2g, h=3R+2, m=10R.
```

Take every formal A monomial of degree at most three except
g-1 of the g cubics of sum 4R. Their tau values are distinct
modulo m, even between degrees, by the same digit proof; all
are below 9R<m. The residue h-1=3R+1 is unused. For each
unoccupied residue r introduce a separate E unit of weight

```
3m+h+((r-h) mod m).
```

This defines an active residue-complete down-set of cardinality
m, and the unused residue h-1 ensures its maximum is
`4m+h-1`. It has

```
q2=3g^2+2g, r_A=0, u3=k=0, t=epsilon=g-1,
LC=(5g+1)(3g^2+2g),
W_A=-(35/6)g^3+13g^2+(41/6)g-4.
```

The unexpanded expression is
`-C(5g+1,3)+(5g+1)(3g^2+2g)+4(g-1)`.
For g=3+u the polynomial is
`-24-(218/3)u-(79/2)u^2-(35/6)u^3<0`.
Also `a(a-1)-6q2=g(7g-17)>0` for g>=3, so LC-minus holds.
There are no other triple collisions after adding the high
directions, whose reserved digit coordinates are independent.

`fiber_family.py` verifies all pair/triple fibers, cross-degree
injectivity, signed-union cardinalities and these exact counts
for g=2,...,12; the infinite claims have the digit proof above.
The fill is given by a formula, not an enumeration of 10R units.
These examples have enormous E payment and do not violate LOW+.

Crucial limitation: HF-LOSS refutes an n-independent constant
for the *standard signed-label union*. It does **not** refute
`3s-2>=H(n)-C*epsilon` for the ambient interval or
`m>=H(n)-C*epsilon` for an ambient cyclic group: the examples
have very large diameter and modulus. Neither a proof nor a
counterexample to those stronger ambient statements is claimed.
Similarly, a frontier-specific fiber bound could still use
LOW-plus violation or the outside-payment budget. A fiber-size
bound from pair distinctness, residue completeness and LC-minus
alone is false by the displayed primary tiles.

## 38. A uniform cutoff for B directions from the transfer budget

This lemma removes the unbounded-b escape in any fixed A
dimension. It also finishes the small-a certificate below.

Let Hhat be any proved nonnegative lower bound for the short
slack `rho-t3-BC-v3-w-z`; for example Hhat=H3+X_SR, or H_cold.
In a counterexample define

```
F=C(a+1,3), B0=-W_A-Hhat-1>=0.
```

**B-CUT.** For a>=7 every counterexample satisfies

```
b <= max(3, floor((B0+2)/2), floor(sqrt(2F+1))-a).    (B-CUT)
```

In particular, without computing Hhat,

```
b <= floor((F+1)/2).                               (B-UNIFORM)
```

Proof. Let B=C(b+1,2), p_AB=ab-s3 and delta_B=B-t3. Write
Dv,Dw,Dz for the last three mixed defects in GW-21's transfer
identity. The budget T+R-Hhat<=B0 holds, and these three defects
are disjoint from the short slack. Suppose

```
b>3,  2b-2>B0.
```

If 2<=t3<B, MG2, applied in b variables, implies
`Dz>=(b+2)t3-3t3^{<2>}>=2b-2>B0`. If t3 is zero or one,
`s3>=ab-B0` since T>=p_AB, and w<=a*t3 gives

```
Dw >= (b+1)(ab-B0)-2a > B0.
```

For the strict inequality substitute B0<2b-2; its remaining
positive difference is at least
`(a-2)[b(b+1)-2]>0`. Thus necessarily t3=B.

For an A direction let k_i be the number of B directions
which are not its I3 AB neighbors. Then its ABB count is at
most C(b-k_i+1,2), because every ABB divisor is an I3 AB or
I3 BB pair. Its contribution to p_AB+Dw is at least

```
k_i+B+(b+1)(b-k_i)-3C(b-k_i+1,2)
       = k_i(4b+3-3k_i)/2.
```

For 1<=k_i<=b the concave expression is at least 2b, by
checking k_i=1,b. This exceeds B0. Hence s3=ab as well.
With all these neighbors,

```
Dv=2br+4(bq2-v2)+3(bq3-v3).
```

So r=0, since 2b>B0. Also b*u3<=B0 gives u3<=1, and
Macaulay on the I3 cubic family gives k<=1. A C unit would
cost at least s3=ab>B0 in T, and an E unit at least 2b>B0;
therefore c=e=0.

All pairs in the a+b directions are now present. Let d0=a+b
and let t_all count their missing cubic monomials. The three
mixed defects are at least three times the missing mixed
cubics. Thus

```
t_all <= t+B0/3
 = [F-LC-t-1-Hhat]/3 <F/3.
```

Here `W_A=-F+LC+4t`, since r=0. The whole cardinality satisfies
`m=C(d0+3,3)-t_all+k`, k<=1. Global SP on zero and these d0
unit residues gives

```
2C(d0+1,3) <= ((3/2)(d0+1)-1)t_all+k
            <= (3d0+1)F/6+1.
```

Multiplying by three and dividing by d0 yields
`d0^2-1<=2F+3/d0`. Since d0>=11, integrality gives
`d0^2<=2F+1`. Therefore, whenever b is larger than the first
two terms of B-CUT, it is at most the third. This proves the
cutoff.

For B-UNIFORM, the exact identity
`4t-(a-3)r=(4/3)D3+(a+17)r/3>=0` and LC>=0 imply
`-W_A<=F`. Thus B0<=F-1. For a>=7, F>=56, the other two
terms in B-CUT are at most floor((F+1)/2).

A second bound, useful before the cutoff, is

```
T+R-Hhat >= b[u3+min(2r,2a-r)]                     (B-NEIGH)
```

when its bracket is nonnegative. For a B direction missing
p>=1 I3 A-neighbors, at least
`p(2a-p+1)/2-r` present A pairs are lost among its possible
AAB divisors. Its p_AB+Dv cost is at least
`p(4a+3-3p)/2-r>=2a-r`. At p=0 its Dv cost is at least 2r.
Summing, and retaining b*u3, proves B-NEIGH. Its proof uses
neither the short slack nor any C/E term, so those costs can
be retained simultaneously.

There is consequently a genuine finite-instance reduction for
each fixed a, uniform in alpha. In any remaining counterexample

```
b<=floor((F+1)/2),
c(c+1)<=F-1,        e<=floor((F-1)/(3a)),
m<=C(a+b+3,3)+c(a+b+1)+e+C(a+3,4).                 (FIXED-A-FIN)
```

The last bound counts A/B cells through degree three, C units
and their AC/BC pairs, E units, and A quartics. Every active
weight is below 5m. Thus this is a finite family of actual
integer weighted down-sets for every fixed a; it is not just
a finite collection of real LP profiles. The dimension a is
still unbounded, so FIXED-A-FIN does not finish Wilf.

There is a stronger completion test which combines the A and
B Macaulay faces rather than estimating them separately.

**MIX-GAP.** Put d0=a+b, `qg=q+s3+t3`, and
`Delta_d(x)=(d+2)x-3x^{<2>}`. Then, for every primary tile,

```
Dv+Dw+Dz >= Delta_{d0}(qg)-2(a-1)r.                (MIX-GAP)
```

Proof. Keep all present A pairs but only I3 AB and BB pairs
as a formal quadratic down-set in d0 variables. All actual
A/B cubics are legal for it. Of the t missing pure-A cubics,
at most ar are forced by missing A pairs. Thus at least t-ar
missing legal cubics remain in this global face. Macaulay gives

```
u3+u4+v2+v3+w+z <= qg^{<2>}-(t-ar).
```

This remains valid if t-ar is negative. The exact identity

```
D3+Dv+Dw+Dz
 =(d0+2)qg-3(u3+u4+v2+v3+w+z)+(bq2-v2)
```

and `D3=3t-(a+2)r` prove MIX-GAP. For r=0 all t are legal,
so their D3 cost cancels instead of being charged a second
time to the mixed budget.

If some AB or BB pair is not in I3, q<=qg<=C(d0+1,2)-r-1.
Define

```
Gamma(d0,q,r)=min_{q<=x<=C(d0+1,2)-r-1} Delta_{d0}(x)
                                                -2(a-1)r.
```

An empty minimum is +infinity. If the available mixed budget
B0 is smaller than Gamma, every AB and BB pair lies in I3.
This is an explicit uniform criterion. On each Macaulay block
`x=C(j+1,2)+z`, 0<=z<=j, Delta is the concave quadratic

```
(d0-j)C(j+1,2)+(d0+2)z-3C(z+1,2).
```

Thus Gamma is computed exactly by the two endpoints of each
block intersecting its interval. The two finite programs use
independently coded endpoint loops; no numerical optimization
is involved.

There are useful analytic bounds on the main frontier a>=13.
If the mixed quadratic face is incomplete, then

```
r=0: Dv+Dw+Dz >= 2(a+b)-2;
r=1: Dv+Dw+Dz >= 2a+4b-5;
r=2: Dv+Dw+Dz >= 2a+6b-14.                         (MIX-012)
```

For r=0 use MG2. For r=1, MG6 covers qg<=C(d0+1,2)-3,
where its bound exceeds 4d0-7; the remaining endpoint has
Delta=4d0-7. Subtract 2(a-1). For r=2 use MG6 and subtract
4(a-1). The hypotheses qg>=q>=Q-2>=6 and d0>=13 verify
every use of MG6.

Once the completion test succeeds, let

```
rem=B0-b*u3-2br,
t_all_up=t+br+floor(rem/3),
epsilon_all_up=t_all_up-[C(d0+2,3)
                               -(C(d0+1,2)-r)^{<2>}].
```

If rem or epsilon_all_up is negative, the branch is impossible.
Otherwise all mixed legal cubic omissions cost at least three:
the identity for Dv with full neighbors supplies the baseline
2br and the retained defects. Hence epsilon_all_up bounds the
global legal cubic defect on all d0 directions. Apply SP after
deleting r pair endpoints from zero and these units, and PSP
without deletion, to obtain a global lower bound for m. Its
upper bound is

```
C(d0+3,3)-r(1+b)-t+k+c(d0+1)+e,
```

with c,e bounded using rem and the full-neighbor C/E cost
`c(c+1+q+q2+u3+ab+B)+e(3a+2b+c+q+q2+u3+ab+B)`.
These are the additional completion/cardinality tests in the
final small-dimension certificate. MIX-GAP is uniform in alpha.

## 39. The small-A strip 7<=a<=13 is closed

**Computer-assisted Theorem T2-SMALL.** Under the exact primary
P4 hypotheses, a<=13 implies W>=0, for every low population
and all b,c,e. The cases a<=6 are GW-24. The cases alpha<=2
are GW-26/26c/26d. For 7<=a<=13 and alpha>=3 the following
finite count certificate has zero survivors.

The source files `t4/small_counts.py` and `t4/small_counts.c`
implement the following fully integral relaxation. The Python
version computes monotone delta endpoints; the C version tests
every delta. The latter was written separately from the Python
loop body and shares no imported implementation.

Enumerate a=7,...,13, alpha=3,...,a, r=0,...,Q, p=a-alpha,

```
max(0,Q_alpha-r)<=n0<=Q_alpha, 0<=l<=alpha*p,
q2=n0+l<=q=Q-r,
3(a+1)q2+(a+17)r<3F.
```

Let `t_f=U-q^{<2>}`. Enumerate

```
t_f<=t<=floor((F-(a+1)q2+(a-3)r-1)/4),
epsilon=t-t_f, D3=3t-(a+2)r,
0<=u0<=U_alpha,
0<=u1<=min(p*n0,floor((alpha+1)l/2),
                         U-t-u0,q2^{<2>}-u0).
```

Set

```
K0=min(u0^{<3>},floor((alpha+3)u0/4)),
K1=floor((alpha+2)u1/3), K=K0+K1, u=u0+u1,
LCbar=(a+1)(q2+u)-4K,
WAbar=-F+LCbar-(a-3)r+4t.
```

These maximize the quartic allowances and therefore lower
every payment used. The relevant enumerated states satisfy
LCbar>=(a+1)q2; both implementations assert this rather than
discarding a state on that assumption. If WAbar>=0 the state
is excluded. Enumerate

```
max(u0,U_alpha-t,U_alpha-alpha(Q_alpha-n0)-epsilon)
 <= c0 <= min(n0^{<2>},U-t-u1).
```

Let t0=U_alpha-c0. Use COLD-MAC to compute the largest possible
beta in [0,n0]. Treat beta=0 separately, and for beta>=1 use
this maximum. This is a valid domination: increasing beta
decreases both the fixed constant and its B coefficient; the
COLD-HIGH lower bound only requires beta>=1 and is independent
of its size. Set beta_H=min(n0,u0+t0), E=min(p,l+r), and use
Hhat=0 for beta=0 or H_cold for the positive branch. If
WAbar+Hhat>=0 the branch is excluded.

For the star sum use its exact minimum with 0<=l_i<=p and
sum l_i=l. If l=kp+z, 0<=z<p, it is
`S_min=kp(a+2-p)+z(a+2-z)`; at p=0 it is zero. This follows
by repeatedly transferring mass to an endpoint in the concave
function x(a+2-x).

Use R-EXACT with beta,K0,K1 and S_min to obtain a lower fixed
payment `f_R+b B_f`, and DELTA-UP with these same quartic
allowances to obtain `delta<=B-D3-b B_H-1`. Enumerate
R=0,...,p and b from zero through the smaller of B-CUT and
B-NEIGH's bound, using WAbar and Hhat in the budget. If B_f>0
also impose `b<=floor((-f_R-1)/B_f)`. Keep only
`f_R+b B_f<=-1`. Every C/E remainder in both arc payments is
nonnegative in these ranges: the code checks
`q+q2+2>=2(alpha+E)` on every base state. Thus outside C/E
directions need not be enumerated in the arc constraints.

They are nevertheless included in the cardinality comparison.
Put `bc=u+min(2r,2a-r)` and
`budget=-WAbar-Hhat-b*bc-1`. For each integer cc>=0 with
`cc(cc+1+q+q2+u)<=budget`, let

```
ee=floor((budget-cc(cc+1+q+q2+u)) /
                            (3a+2b+cc+q+q2+u)).
m_up=max_cc [C(a+b+3,3)-r(1+b)-t+K+cc(a+b+1)+ee].
```

This follows from the retained C/E terms in T and the capacity
bound v2+v3<=bq. Each missing A pair removes itself and its b
AAB multiples, accounting for r(1+b). It is an upper bound
even when the independent quartic allowances are incompatible.

For the lower cardinality bound apply global SP after deleting
at most r pair endpoints from zero and the a A directions,
and also apply PSP to all a+1 directions:

```
n_g=max(0,a+1-r), er=C(r+1,2),
m_low=max(ceil(H(n_g)-lambda_{n_g}epsilon),
 H(a+1)-4er-9[(a+1)er+(r+1)epsilon+C(epsilon,2)]).
```

Zero-padded legal pair and unit triples are already present,
so the same localized epsilon is valid in these global bounds.
If m_low>m_up discard the branch. Also impose delta<=m_up-2,
because h=delta+2L<=m and L>=1. Finally impose all section 27
WINDOW-SP/COUNT and PSID bounds, JOINT-SP/COUNT, PSP on the
alpha+R joint directions, and violation of LOW+:

```
3delta >= (a-1)(b+1)+(a+1)(q2+u)+D3
                         +(b+2)q2+b*u-3K+1.        (LOW-FIN)
```

Also apply the MIX-GAP completion test and resulting global
cardinality comparison in section 38. LOW-FIN is I-LOW with
eta=3delta, after dropping nonnegative C/E
costs; `LC+k=(a+1)(q2+u3)-3k`. Every step enlarges the possible
counterexample set. The bounded loops and these explicit tests
therefore give a complete finite certificate.

Both implementations give the following table. A base state is
(a,alpha,r,n0,l) admitting some t. The u-column counts
(t,u0,u1) states with WAbar<0 before c0 is enumerated. Packing
profiles are branches (including R,b and the dominating beta
choice) reaching the final packing/cardinality tests.

| a | Base states | u states | Packing profiles | Surviving delta tuples |
|---:|---:|---:|---:|---:|
| 7 | 1 | 3 | 5 | 0 |
| 8 | 7 | 92 | 25 | 0 |
| 9 | 25 | 813 | 92 | 0 |
| 10 | 103 | 5,252 | 272 | 0 |
| 11 | 303 | 24,219 | 953 | 0 |
| 12 | 735 | 105,982 | 2,724 | 0 |
| 13 | 1,580 | 386,234 | 8,823 | 0 |
| Total | 2,754 | 522,595 | 12,894 | 0 |

For an additional transparent endpoint check, before using the
Hhat budget in B-CUT there were exactly three survivors:
`a=12,alpha=4,r=0,n0=10,l=3,t=20,u0=u1=k=c0=0`,
beta=10,R=8,b=17,18,19. All have WAbar=-37 and H_cold=35.
The residual budget is one. B-CUT then gives b<=11, eliminating
all three. One can alternatively see the contradiction directly:
this budget forces all AB and BB pairs into I3, all mixed cubics
present, and c=e=0. The resulting nearly full cubic simplex
violates global SP. These were relaxed count profiles, not
actual residue-complete examples.

**Semigroup consequences.** In the range 3m<c_S<=4m, a is the
number of nonmultiplicity minimal generators below
`c_S-2m`. The new small theorem proves Wilf whenever this number
is at most 13. Combined with T2.3G, Wilf also holds for every
such semigroup having at most three nonmultiplicity minimal generators with
`2n_j<c_S-m`. For U-SMALL, r and l are measured in the chosen
residue-complete factorization tile; no tile-free translation
of those two additional hypotheses is asserted.

## 40. Checks, preserved failures, and reproduction for sections 31–39

All computations in this continuation ran on fejer in
`~/wilf/p8/`, with nice level 10 and single-core programs.
No more than four owned computation jobs ran concurrently;
the main verification stages used one or two. The laptop was
used for reading, editing and copying files. No commits were
made. The new sources and outputs are under `t4/`; earlier T1
and T2 sources and the text of sections 1–30 are retained.
Recorded versions are Python 3.12.3, NumPy 2.5.4, SciPy 1.18.1
and GCC 13.3.0. Symbolic verification uses exact Fractions,
without sympy.

The principal exact checks are:

- JOINT-FIN: two implementations, a=13,...,40; 51,502
  pre-packing profiles; 11 JOINT survivors and 101 expanded
  delta tuples; all 11 excluded by the independently proved
  PSP bounds. This agrees with the lead's supplied table.
- T2-SMALL: Python endpoint calculations and independent C
  direct-delta calculations agree on every row of the section
  39 table: 2,754 base states, 522,595 u states, 12,894 packing
  profiles, no unbounded b branches, zero survivors.
- `uniform_identities.py`: 29 exact Fraction polynomial
  identities, including R-EXACT, B-EXACT, the B-neighbor
  polynomial, the B-free LOW/H0 identity, both heavy-fiber
  W_A expansions, and the exact MIX-GAP identity.
- `uniform_polys.py`: exact verification of U-POLY's displayed
  positive certificate. Its preliminary polynomial expansions
  are diagnostics; the final identity and coefficient signs
  prove the infinite parameter range, not a numerical grid.
- `fiber_family.py`: g=2,...,12; pair distinctness, the unique
  nontrivial triple fiber, signed-union sizes, cross-degree
  injectivity after adding the high units, the unused top
  residue, and the exact low counts. The large E fill is
  implicit and justified by the formula in section 37.

Actual-semigroup checks used the sparse lex/grlex generator
from section 29, with the updated `t4/multi_low.h`. Each accepted
tile is checked for residue bijection and down-set closure by
the generator and checker. In addition to the old checks the
new header verifies JOINT-SP/COUNT, COLD and COLD-MAC, LOC-LOW,
LLH, H-COLD, both refined outside counts, R-EXACT, COLD-FIX
when its signs apply, COLD-HIGH, B-NEIGH, and PSP. The final
control runs were:

| Seed | Proposals | Proposed lows | Factorization | m range | Proposed A range | Primary instances |
|---:|---:|---:|:---|:---|:---|---:|
| 202610193 | 15,000 | 4 | lex | 200–6,000 | 7–20 | 14,890 |
| 202610195 | 10,000 | 6 | grlex | 500–8,000 | 7–20 | 9,937 |
| 202610196 | 2,000 | 4 | grlex | 500–5,000 | 13–26 | 1,983 |

Total: 26,810 primary instances (not asserted to be distinct).
There were 26,625 applications of the new joint bounds and
18,483 applications of COLD-FIX's sign condition. MIX-GAP was
added for the last run and passed on its 1,983 primary instances.
The last two controls did not reach a negative W_A multi-low
frontier; the first had minimum W_A=-120. None reached violation
of the old LOW+ test. These facts limit the adversarial claim:
the controls verify inequalities on actual instances, but do
not certify that random sampling approaches an actual remaining
counterexample. The finite certificates and symbolic proofs
are separate from this sampling evidence.

A distinct adversarial experiment tested the **unproved ambient
SP12 assertion** discussed below. `ambient_adversary.c` uses
pair-distinct sets with n=9,12,...,30, interval bounds
`floor((H(n)+2)r/300)` for r=40,60,80,95, two greedy starts
per bound when initialization succeeds, and 2,000 mutations
per successful start. It minimizes ordinary triple collision
excess while retaining pair distinctness, with fixed seed
202610194. It evaluated 116,000 mutations, 8,439 of which
were pair-distinct; repetitions are included. No SP12 failure
was found. The largest observed necessary constant
`[H(n)-(3span-2)]/epsilon` was 650/137. The log records the
full best set for each initialized interval. This is a bounded
stochastic falsification test, not a packing theorem.

Preserved failures and distinctions:

1. The proposed absolute constant for the standard signed-label
   union is false, by HF-FAMILY. For C=12 the smallest dimension
   admitting the exhibited violation is n=9, with complete
   explicit integer data in `fiber_family.json`. The same
   construction supplies unbounded fibers even in primary,
   residue-complete tiles with LC-minus.
2. The implication from that pointwise failure to failure of an
   ambient-modulus or ambient-interval estimate is invalid.
   The explicit examples have large unused ambient space. No
   counterexample to the ambient estimate is claimed.
3. A draft expansion of the heavy-fiber W_A with coefficients
   `-35g^3/6+51g^2/2+31g/3-4` was an arithmetic error. At the
   smallest g in the recorded family, g=2, it gives 72 rather
   than the exact 15. Section 37 gives the corrected polynomial
   and its independently checked shift at g=3.
4. A draft evaluation used S=15 for a=13,l=1, whereas
   `S=l(a+2-l)=14`. The corresponding COLD-FIX bounds for
   t=13,14 are 0,3, rather than 1,4. The first affected row
   is `(a,r,l,n0,t,R)=(13,1,1,6,13,10)`. The corrected
   nonnegative bound suffices, and both JOINT programs now
   check it on every survivor.
5. Before retaining H_cold in B-CUT, the small-A relaxation
   left three a=12 profiles. Their full count data and direct
   exclusion are recorded in section 39. Before MIX-GAP, the
   a=13 relaxation left 126 profiles, all alpha=4: 10 with r=0,
   109 with r=1, and 7 with r=2. MIX-GAP and the resulting
   global packing comparison exclude them. No such profile
   was asserted to have a residue-complete realization.

The reproducibility inventory is `t4/MANIFEST.json`, with file
digests in `t4/SHA256SUMS`. It checks rowwise totals between the
finite implementations, all saved empty-survivor results, the
11 JOINT rows and their PSP exclusions, and the symbolic logs.
Principal commands, run on fejer, are:

```sh
cd ~/wilf/p8
nice -n 10 ~/mathenv/bin/python joint_profiles.py 13
nice -n 10 gcc -O2 joint_profiles.c -o joint_profiles
nice -n 10 ./joint_profiles 13
nice -n 10 ~/mathenv/bin/python small_counts.py 7 13
nice -n 10 gcc -O2 small_counts.c -o small_counts
nice -n 10 ./small_counts
nice -n 10 ~/mathenv/bin/python uniform_identities.py
nice -n 10 ~/mathenv/bin/python uniform_polys.py
nice -n 10 ~/mathenv/bin/python fiber_family.py
nice -n 10 gcc -O2 uniform_semigroups.c -o uniform_semigroups
nice -n 10 ./uniform_semigroups 202610193 15000 200 6000 4 0 7
nice -n 10 ./uniform_semigroups 202610195 10000 500 8000 6 1 7
nice -n 10 ./uniform_semigroups 202610196 2000 500 5000 4 1 13
nice -n 10 gcc -O2 ambient_adversary.c -o ambient_adversary
nice -n 10 ./ambient_adversary
nice -n 10 ~/mathenv/bin/python audit_p8.py
```

For `audit_p8.py`, redirect outputs to the log names in its
source and copy the final report to `~/wilf/p8/P5_REPORT.md`.
No counterexample to Wilf or a verified step of GW-24/26/26c
was found.

## 41. Final frontier and the next precise packing question

The full primary regime, and therefore Wilf for every semigroup
with 3m<c_S<=4m, remains unproved. The new established results
are T2.3G (all three-low cases with a>=13), T2-SMALL (all a<=13),
U-SMALL and U-B0 (uniform in alpha), and the general JOINT,
cold-defect, R/delta, B-CUT and MIX-GAP lemmas. The first two
retain explicit finite-certificate dependencies; the latter
statements have paper proofs above.

Any remaining counterexample must now have

```
a>=14, alpha>=4, delta>0,
W_A<0, LC-minus, LP-low, MAC-minus,
violation of LOW+, I-LOW+ and the exact END-ETA test,
Phi<0, Psi<0,
W_A+T+H3+X_SR<0,
LC+C(p_hi+2,3)-F+5r+D3+T+X_SR<0.                   (FRONTIER-41)
```

It must satisfy all WINDOW and JOINT packing/count inequalities,
PSP, LOC-LOW, COLD-MAC, COLD-HIGH, the exact section 34 R and
delta bounds, B-CUT and FIXED-A-FIN. When MIX-GAP completes
the mixed quadratic face, its global-cardinality test must
also pass. These are necessary conditions, not assertions
that every such count vector has a tile realization.

There are two more explicit exclusions:

- If r=l=0, then epsilon>Q_alpha/4.
- If also b=0, then a>=2alpha+3 and MID-B0 holds. Thus the
  B-free low-dimensional strip a<=2alpha+2 is closed throughout
  the r=l=0 branch, including arbitrary localized cubic defect.

In semigroup language any remaining counterexample has at
least 14 nonmultiplicity minimal generators below c_S-2m,
and at least four with 2n_j<c_S-m. The count a remains the
only unbounded dimension in FIXED-A-FIN; for each a it gives
explicit bounds on b,c,e,m and on every active weight.

The precise unresolved packing candidate is:

> **Ambient SP12 (unproved).** Let B be an n-element integer
> set in an interval of s integers, with all unordered pair
> sums distinct, and let epsilon be the excess of the number
> of unordered triples over the number of their ordinary sums.
> Then `3s-2>=H(n)-12epsilon`.

It is true from SP for n<=8, and follows from LSP at epsilon=0.
HF-FAMILY refutes the analogous signed-union statement but not
this ambient statement. The coefficient 12 is chosen because
the retained payment `3epsilon` in DELTA-UP buys 13.5epsilon
in the joint ambient capacity `3ceil(3delta/2)-2`; thus a loss
of 12epsilon would leave a positive linear payment. For r>0
the pair endpoint loss must still be included, or replaced by
PSP/MIX-GAP. No claim is made that Ambient SP12 alone already
proves all of FRONTIER-41.

The strategic decision after the cold-payment and global-mixed
attempts is therefore to discontinue an n-independent bound
on the standard signed union or on fiber size under LC-minus
alone. Both are disproved. The productive next lemma must use
ambient interval space, or impose the full FRONTIER-41 payment
budget on heavy fibers. MID-B0 identifies exactly the middle
localized-defect interval still left by the present uniform
argument in its simplest branch. Enlarging the earlier E-heavy
random boxes would not address that interval. The completed
small-dimension exclusions and the explicit heavy-fiber family
are retained as constraints on the next proof, not presented
as a proof of the full conductor range.

## 42. P5e: the conditional packing question, without a hidden reduction

This continuation is dated 2026-10-19. Sections 1--41 are retained
unchanged. The lead has verified sections 24--33 and recorded GW-26e;
sections 34--39 remain under independent review. Results below that
use those sections retain that dependency. In particular no assertion
here upgrades the lead's review status of T2-SMALL or U-SMALL.

Write P(C) for the following ambient statement, with no modulus:

> For every n-element integer set X in an interval of s integers,
> if its unordered pair sums, including loops, are distinct, and
> epsilon_X=C(n+2,3)-|3X|, then
> `3s-2 >= H(n)-C*epsilon_X`, where H(n)=n(C(n,2)+1).

The loss is the ordinary unordered triple excess, including repeated
summands. There is no unspecified O(n^2) term. A larger C is a weaker
statement. P(12) is the lead's candidate; it is not proved here.

There is **not yet a proof that P(12) empties the entire FRONTIER-41**.
The new conditional theorem in section 45 closes the entire
`r=l=b=0` branch with the substantially weaker P(47). It includes
all localized cubic defects and all C/E directions, and hence includes
MID-B0. Sections 43--44 give an exact repair-and-defect treatment of
r>0, including its lower-order terms. Links and B units remain in
the exact R-EXACT/DELTA-UP coefficients of section 34. Neither is
silently set to zero in the general reduction.

Here is the precise general conditional test supplied by P(C).
Let k be the minimum number of A units meeting every absent A pair.
Put

```
zeta_A=t-a*r+C(r,2),
e_k=min(epsilon_M,zeta_A-C(k,2)),
n_j=max(0,alpha+R-k), s_j=ceil(3delta/2),
n_w=max(0,R-k),
n_s=max(0,R-l-r-k), s_s=ceil(delta/2).
```

Then P(C), if true, gives all three inequalities

```
3s_j-2 >= H(n_j)-C*e_k,
3delta-2 >= H(n_w)-C*e_k,
3s_s-2 >= H(n_s)-C*e_k.                         (P-REPAIR)
```

The allowed k and the nonnegative e_k are bounded exactly in section
43. The global cyclic SP/PSP inequalities of that section are also
required, but P(C) cannot be applied to a cyclic set by calling its
modulus an interval length. The B-direction test in section 44 is
an additional, independent global cyclic test. A conditional proof
for the full primary regime still has to exclude all count profiles
satisfying these tests and R-EXACT, DELTA-UP, LOW-FIN, HIGH, COLD-HIGH
and the retained outside budgets, including E-REPAIR in section 50.
Such an exclusion is not presently
established uniformly in alpha. Thus there is no justified global
"weakest C" yet. Section 45 specifies the sufficient constant and
its optimization for the branch actually reduced to ambient P.

## 43. Missing-pair defect, vertex covers, and linked packing

The following lemma applies to arbitrary loop graphs and does not
assume residue completeness.

**PAIR-COVER.** Let G be a family of r distinct quadratic monomials
on d variables, including possible squares. Let F_G be the number
of cubic monomials divisible by a member of G, and let tau(G) be
the smallest number of variables meeting all monomials in G. Put

```
D_G=#{unordered pairs of members of G with disjoint supports},
T_G=#{three distinct variables whose three edges belong to G}.
```

Then

```
F_G=d*r-C(r,2)+D_G+T_G,
D_G+T_G >= C(tau(G),2).                         (PAIR-COVER)
```

The second inequality is sharp: r disjoint loops have tau=r and
D_G=C(r,2), T_G=0. A triangle has tau=2, D_G=0, T_G=1.

Proof of the identity. Every absent quadratic has d distinct cubic
multiples. Two distinct quadratics have a common cubic multiple
exactly when their supports intersect; that multiple is unique.
Three distinct quadratics have a common cubic multiple exactly
when they are the three edges of a triangle on distinct variables.
A cubic has at most three distinct quadratic divisors. Inclusion
and exclusion therefore stops after the triangle term and proves
the identity, including loops.

Proof of the cover inequality, by induction on r. Give a vertex
degree equal to the number of members of G containing it; a loop
counts once. If some vertex v has degree Delta>=3, remove its star
and call the remaining graph G'. Each edge of G' intersects at most
two of the Delta star edges. Hence the new disjoint pairs number
at least `(Delta-2)|G'|>=|G'|`. Also
`tau(G')>=tau(G)-1` and `|G'|>=tau(G)-1`, since v together with one
endpoint from each edge of G' is a cover of G. The induction
hypothesis gives

```
D_G+T_G >= C(tau(G)-1,2)+tau(G)-1=C(tau(G),2).
```

If tau(G)=1 the conclusion is simply nonnegativity; use that
case directly, without interpreting C(-1,2).

It remains to consider maximum degree at most two. Let
`J=sum_v C(deg(v),2)`. Each intersecting pair has exactly one common
vertex, so `D_G=C(r,2)-J`, and J<=r. If G has no intersecting pair,
tau=r and the result is equality. If J<=r-1 and there is an
intersecting pair, tau<=r-1 and
`D_G>=C(r,2)-(r-1)=C(r-1,2)`. If J=r, equality in the degree sum
forces no loops and every nonisolated vertex to have degree two.
Thus G is a disjoint union of simple cycles. If a triangle occurs,
T_G>=1 and again `D_G+T_G>=C(r-1,2)`. If no triangle occurs,
tau<=r-2, while `D_G=C(r,2)-r>=C(r-2,2)` for r>=4. This proves
all remaining cases. The empty graph has tau=0.

Here is the exact connection to the tile defect. Suppose all
present cubic monomials on these d directions have present pairs.
If t cubics are missing, let v be the number of legal missing
cubics, whose pair divisors are all present. Then

```
zeta:=t-d*r+C(r,2)=D_G+T_G+v.                    (PAIR-ID)
```

Consequently the actual minimum cover k satisfies

```
C(k,2)<=zeta-v_lower,
v<=min(epsilon_M,zeta-C(k,2)),
epsilon_M=q^{<2>}-(C(d+2,3)-t), q=C(d+1,2)-r.    (LINKED-DEF)
```

Here v_lower is any established lower bound for v. The inequality
v<=epsilon_M follows because the number of legal cubic monomials
is at most q^{<2>}. If r<=d, the near-full Macaulay formula is
`C(d+2,3)-q^{<2>}=d*r-C(r,2)`, so zeta is exactly epsilon_M.
For larger r, PAIR-ID is still valid; zeta must not be replaced
by epsilon_M.

An explicit cover upper bound used in the scripts is as follows.
For z>=0 define gamma(0,z)=0. For r>0 start with

```
gamma=min(r,floor((1+sqrt(1+8z))/2)).
```

Let `D0=1+ceil((C(r,2)-z)/r)`. If D0>=3, also take the minimum
with `1+floor(z/(D0-2))`. The first bound is PAIR-COVER. For the
second, `sum C(deg(v),2)>=C(r,2)-z` and
`sum C(deg(v),2)<=r(Delta-1)` force Delta>=D0. A star of maximum
degree leaves at most z/(Delta-2) edges outside it. Its center
and one endpoint of each remaining edge cover G. Clamp gamma
to d if necessary. At z=0 and r>0 this gives gamma=1: all missing
pairs have a common endpoint. This also follows directly since a
pairwise intersecting family of edges is a star or a triangle,
and the triangle has T_G=1.

For the A face one may take

```
v_lower=max(0,t0-alpha*r_LL), r_LL=Q_alpha-n0,
z=zeta_A-v_lower.
```

Indeed at most alpha*r_LL pure-low cubics are forced absent by
low pairs; every other missing pure-low cubic is a legal omission.
This spends the low defect before repairing the missing-pair graph.

**Linked residue packing.** Let N=d+1 denote zero together with
the d units. For the actual cover k, remove its k unit residues.
All remaining pairs, including those with zero, are present and
injective. Cubics involving zero are already present lower-degree
cells. The missing cubics on this set number at most

```
e_k=min(epsilon_M,zeta-C(k,2)).
```

Thus the existing cyclic SP lemma gives

```
2m >= 2H(N-k)-L2(N-k)*e_k, L2(n)=2lambda_n.      (LINK-SP)
```

PSP on all N directions gives the additional bound

```
m >= H(N)-4E_r
       -9[N*E_r+(r+1)e_k+C(e_k,2)],
E_r=C(r+1,2).                                   (LINK-PSP)
```

The same argument on a selected interval proves P-REPAIR if P(C)
is assumed, or the unconditional version with C=lambda_n. One
must use the same k and e_k in the global A packing and the
three interval tests. Taking the largest possible k and simultaneously
allowing the entire epsilon_M loses this coupling. In a relaxed
certificate enumerate `k=0` if r=0 or
`1<=k<=min(d,gamma(r,z))` otherwise; for each k use e_k.
Exclusion of every such k excludes the original tile.

For a repaired, pair-injective set there is also the older
quadratic collision bound

```
m>=H(N-k)-9C(e_k+1,2).                           (LINK-Q)
```

Indeed a triple fiber of size g contributes at most 9C(g,2)
colliding normal-label pairs. Summing and using
`sum(g-1)<=e_k` bounds this by 9C(e_k+1,2). Normal labels avoid
the unit residues by pair injectivity. This is the P4 signed-union
argument before its linear support optimization. The final scripts
use the maximum of LINK-Q and LINK-SP, and their interval analogues.

## 44. MIX-PACK: a partial mixed face is sufficient

The mixed face need not be completely quadratic before using
global residue packing. The following version retains its exact
shadow defect. Write d0=a+b, U_d0=C(d0+2,3), and

```
q_g=q+s3+t3, r_g=C(d0+1,2)-q_g,
u_g=(u3+u4)+(v2+v3)+w+z,
epsilon_g=q_g^{<2>}-u_g,
Delta_g=(d0+2)q_g-3q_g^{<2>}.
```

Every actual A/B cubic has legal quadratic divisors, where legal
means all AA pairs and the I3 AB/BB pairs. Therefore epsilon_g>=0.
The exact identity in section 38 is

```
D3+D_mix=Delta_g+3epsilon_g+(b*q2-v2).            (MIX-ID)
```

In particular if D_mix<=M, then

```
epsilon_g<=floor((D3+M-Delta_g)/3).              (MIX-EP)
```

This upper bound uses an already paid shadow budget; it is not
an independent arbitrary allowance for missing mixed cubics.

Here is a finite necessary test for each profile in section 39,
valid without completing the mixed face. Use quartic upper
allowances K and WAbar as there, a lower bound Hhat on the
short-residue slack, and u=u3. Set

```
M=-WAbar-Hhat-1-b*u,
s_min=max(0,ab-M),
t_min=max(0,ceil((b*s_min+ab-M)/(2a))).
```

A counterexample requires M>=0. Since T pays `ab-s3+b*u`,
`s3>=s_min`. Also w<=a*t3 and
`D_w=a*t3+(b+1)s3-3w>=(b+1)s3-2a*t3`.
The budget `D_w+(ab-s3)<=M` implies t_min. Thus enumerate only

```
q+s_min+t_min <= q_g <= C(d0+1,2)-r.
```

Retain only q_g satisfying

```
Delta_g<=M+2(a-1)r,
Delta_g<=D3+M.                                  (MIX-RANGE)
```

The first is MIX-GAP with b*u already paid; the second is MIX-ID.
Put E_g=floor((D3+M-Delta_g)/3), and

```
Z_g=U_d0-q_g^{<2>}+E_g-d0*r_g+C(r_g,2),
V_A=max(0,t-a*r).
```

At least V_A pure-A omissions are legal in this global graph,
because at most a*r are forced by absent AA pairs. Therefore
the actual cover k_g obeys

```
1<=k_g<=min(d0,gamma(r_g,Z_g-V_A))  if r_g>0,
k_g=0                                             if r_g=0.
```

Negative Z_g-V_A excludes q_g. For each remaining k_g use

```
e_g=min(E_g,Z_g-C(k_g,2)), N=d0+1.
```

The maximum of LINK-SP and LINK-PSP is a lower bound on m for
that choice. The unknown actual epsilon_g and actual missing
cubic count were bounded above to obtain Z_g and e_g; every
replacement enlarges the feasible set.

For the upper bound put co=q_g+q2+u. The retained C/E transfer
costs are at least

```
c(c+1+co)+e(3a+2b+c+co).
```

All A/B cubics number at most q_g^{<2>}, and each missing AA pair
also excludes its b AAB multiples. Hence

```
Bcard=min(C(d0+3,3)-r(1+b)-t+K,
          1+d0+C(d0+1,2)-r+q_g^{<2>}+K),
m <= Bcard+c(d0+1)+e.                            (MIX-CARD)
```

For every integer c>=0 with c(c+1+co)<=M maximize this bound by
setting `e=floor((M-c(c+1+co))/(3a+2b+c+co))`. Call the resulting
maximum U_g. If every q_g and every k_g has its packing lower
bound greater than U_g, the profile cannot come from a tile.
This is MIX-PACK. No ambient packing conjecture is used here.

## 45. An exact conditional theorem covering MID-B0

**Theorem P47-B0.** Under the primary hypotheses, alpha>=4 and
`r=l=b=0`, assume P(47). Then W>=0 for every c,e, with no
restriction on epsilon_M. The same follows from P(C) with C<=47.

Proof. Assume W<0. Put A=alpha, Q0=C(A+1,2), U0=C(A+2,3),
epsilon=epsilon_M=t. The A-LOW, U-SMALL and U-B0 arguments in
section 36 give a>5A/3+1, a>=2A+3 and MID-B0. In particular

```
x:=a-2A-1-6epsilon/Q0 >= (2a-3A)/Q0 >0.
```

Let y=epsilon/Q0. COLD-FIX and R-LOW, retaining D3=3epsilon,
give, for n=A+R,

```
n >= a/2+2A/3+5/6+(a-2A)/(2Q0)+3y/2
  > nu:=a/2+2A/3+5/6+3y/2.
```

All joint pairs are present. DELTA-UP, dropping its nonnegative
low-cubic term and using c0<=U0, gives

```
delta<=B0-3epsilon-1,
B0=(a-2A-1)Q0+2U0+2A-a+1.
```

All C/E terms discarded in these two bounds are nonnegative by
the calculation in section 36; MID-B0 also retains that fact.
The integer capacity satisfies
`2(3ceil(3delta/2)-2)<=9delta-1`. P(47), monotonicity of
n^3-n^2+2n for n>=1, and n>nu would therefore require

```
F:=nu^3-nu^2+2nu-9B0-67epsilon+10 <0.            (P47-NEC)
```

Here is a complete positive certificate. Set

```
T=9y/(2A)>=0, V=x/(2A)>=0, w=T+V,
g(w)=w^3+5w^2-(46/9)w+44/27,
j(w)=3w^2-(31/9)w-2/3.
```

Direct expansion gives the exact identity

```
F=A^2[(A-4)g(w)+4g(w)+j(w)]
  +(40/9)(A^3+A^2)V
  +A[16/9+(50/3)T+(68/3)V]+358/27.              (P47-ID)
```

The two needed polynomials have explicit certificates

```
g(w)=w^3+5(w-23/45)^2+131/405,
4g(w)+j(w)=4w(w-1/2)^2
                +27(w-112/243)^2+254/2187.
```

Both are strictly positive for w>=0, so F>0, a contradiction.
All constants and lower-order terms are displayed.
`t5/p5e_identities.py` verifies the identities over exact Fractions.

There is a modest optimization. For general C replace L=46/9
by `(2C-48)/9` in g, and replace 31/9 in j by `L-5/3`.
The identity has coefficient `(2C-54)/9` on `(A^3+A^2)V`,
which is nonnegative for C>=27. Define

```
C_dagger=min_{w>0} [51/2+(18/5)w^2+(207/10)w+79/(15w)].
```

The minimizer is the unique positive root of
`216w^3+621w^2-158=0`. One has 47<C_dagger<48: the lower bound
is the strict certificate above; evaluate at w=1/2 for the upper
bound. For C<=C_dagger, `4g+j>=0`. Also g>0 for C<=48, since
`g>=w^3+5(w-8/15)^2+28/135`. Thus the same proof works at
C=C_dagger. This is the largest C allowed by this two-polynomial
core certificate. It is **not asserted to be the sharp constant
for the original integer branch or for FRONTIER-41**.

Two unconditional consequences are useful. First, if the actual
joint set has n<=32, existing SP gives lambda_n<=47, so P47-B0
requires no conjecture. In particular it closes the entire
`r=l=b=0, a<=32` branch. Second, that branch is also closed when
a>=2Q0+38. Indeed MID-B0 gives epsilon<aQ0/6, R-LOW gives
n>a/2, and the derivative of
`f(n)=n^3-n^2+(2-3epsilon)n` is positive for n>=a/2 if a>=2Q0.
Unconditional JOINT-SP and DELTA-UP would require

```
0 > f(a/2)-9B0+10
  >= a[a^2/8-a(Q0/4+1/4)-9Q0+1]+10.
```

Here B0<=aQ0. The bracket equals

```
172+[a-(2Q0+38)](a/8+9/2),
```

which is positive when a>=2Q0+38. This is an analytic bound for
every fixed A, not a finite-grid extrapolation. Section 47 records
a bounded computation between these two analytic ends.

## 46. Uniform large-a closure, with arbitrary missing pairs and links

**Theorem LARGE-A.** Under the primary hypotheses let alpha>=4
and put R0=C(alpha+1,2). If

```
a>=16R0^2,
```

then W>=0 for every b,c,e. There are no restrictions on
r,l,epsilon or the number of high exceptions. Thus every fixed
alpha has an explicit upper bound on a in a counterexample.

Proof. Assume W<0. Write A=alpha, R0=C(A+1,2), K=R0-1 and
U0=C(A+2,3). We use GLOC, Macaulay and cyclic SP, plus elementary
counts; no ambient P is assumed. Since R0>=10, all inequalities
below follow from a>=16R0^2.

First q>=C(R0+1,2). Otherwise Macaulay gives
`u3+u4<=C(R0+2,3)<=R0^3`, while the original expression
`W_A=3a(a+1)+(a-3)q-4(u3+u4)+LC` is positive: LC>=0 and
3a(a+1)>4R0^3. This contradicts W_A<0.

The two low-cubic terms of GLOC are nonnegative:

```
(a+1)u0-5k0 >= [a+1-5(A+3)/4]u0>=0,
(a+3)u1-3k1 >=(a+1-A)u1>=0.
```

Its C/E remainder is nonnegative: its c coefficient is at
least q+1-2A>0 and its e coefficient is positive. Its b
coefficient is at least `a-1-2A-R0>=a/2`. As a>=2A+1,
n0<=R0 and c0<=U0, the remaining pure term is at least

```
D3-M_A(a)+S,
M_A(a)=(R0-1)a+2A+1-R0(4A-1)/3 <K*a.
```

The strict inequality follows from R0>=A and (4A-1)/3>=5.
The negative counterexample payment Phi therefore forces

```
D3<K*a,                   b<2K.                 (LA-BUDGET)
```

We next prove r<R0. Write q=C(j+1,2)+z with 0<=z<=j and
Delta=(a+2)q-3q^{<2>}. Then j>=R0 and

```
Delta=(a-j)C(j+1,2)+(a+2)z-3C(z+1,2).
```

If j<=a/2, its z term is nonnegative and
`Delta>=a R0(R0+1)/4>K*a`. If a/2<j<=a-2, concavity in z
reduces to the endpoints. At z=0 the bound exceeds a^2/4.
At z=j use the exact identity

```
Delta=(a-j-1)C(j+2,2)+3j+1-a>a^2/8>K*a.
```

Both cases contradict Delta<=D3<K*a. The full q=C(a+1,2)
case has r=0. In the remaining last block j=a-1,

```
Delta=r(4a-3r-1)/2, 1<=r<=a.
```

If r>=R0, concavity in r reduces to R0 and a. At R0 the
bound is `2R0*a-(3R0^2+R0)/2>=K*a`; at a it is
`a(a-1)/2>=K*a`. Again this is impossible. Hence r<=K.
Also epsilon_M=(D3-Delta)/3<K*a/3.

Delete at most r pair endpoints from zero and the a A units.
The remaining pair-injective cyclic set has
`n=a+1-r>=(15/16)a`, and n<=a+1. Cyclic SP gives

```
2m >= n^3-n^2+2n-3n*epsilon_M
    > n[n^2-n+2-K*a]
    >= (15a/16)[(209/256)a^2+1].
```

For the last inequality use n^2>=225a^2/256 and
`(K+1)a<=a^2/16`. In particular

```
m>(3135/8192)a^3>a^3/3.                          (LA-LOWER)
```

There is an incompatible upper bound. Put d0=a+b. From b<2K
we have d0+3<(17/16)a, because a/16>=R0^2>2R0+1. Thus

```
C(d0+3,3)<(4913/24576)a^3<a^3/5.
```

Transfer and -W_A<=F imply
`c(c+1)<=F-1`, `e<a^2/18`, and hence `c<a^(3/2)/2`.
Since a>=256 and d0+1<(17/16)a,

```
c(d0+1)<(17/512)a^3<a^3/30.
```

Every quartic has at most one high factor. Its pure-low part
satisfies `k0<=(A+3)U0/4<=R0^4<=a^2/256`; its remaining
part satisfies
`k1<=(A+2)u1/3<=(A+2)R0*a/3<=R0^2*a<=a^2/16`.
Thus k<a^2/8 and

```
k+e<(13/72)a^2<a^3/60.
```

All A/B cells except quartics number at most C(d0+3,3).
A C unit contributes at most itself and its d0 A/B pairs;
an E unit contributes only itself. Consequently

```
m<=C(d0+3,3)+k+c(d0+1)+e
 <a^3(1/5+1/30+1/60)=a^3/4,                     (LA-UPPER)
```

contradicting LA-LOWER. This proves LARGE-A. The large constant
is deliberate: it supplies an explicit analytic closure for every
fixed alpha, with all outside directions retained. No optimization
of 16 is claimed.

## 47. Finite continuation: a<=16, and four matching profiles at a=17

The finite certificate of section 39 extends through a=16 after
adding LINKED-DEF and MIX-PACK. This is a computer-assisted result;
it retains the section 39 dependencies, whose independent review
by the lead is not yet complete.

**Theorem T2-SMALL16 (finite certificate).** Under the primary
hypotheses, a<=16 implies W>=0, for every alpha,b,c,e.

For a<=13 use section 39. For a=14,15,16 the two programs
`t5/frontier_counts.py` and `t5/frontier_counts.c` enumerate the
same section 39 domain. The Python implementation uses monotone
delta endpoints; the C implementation tests every integer delta.
The new steps, after the old section 39 tests, are:

1. Compute zeta_A=t-a*r+C(r,2) and
   `v_lower=max(0,t0-alpha*(Q_alpha-n0))`.
2. Enumerate the possible actual minimum covers
   `k=0` if r=0 or `1<=k<=min(a,gamma(r,zeta_A-v_lower))`.
   Use e_k=min(epsilon_M,zeta_A-C(k,2)).
3. Require one and the same k to satisfy the global A cyclic
   packing bounds and the short, wide and joint interval bounds.
   Use LINK-SP, LINK-Q and LINK-PSP. The initial linear-only
   version already gives zero survivors through a=16; LINK-Q
   subsequently strengthens the certificate.
4. Apply MIX-PACK with the linked cover/defect test to every
   possible q_g. Keep a profile only if some q_g and k_g survive.

Every replacement in sections 43--44 is a necessary condition.
Quartic counts are still replaced by upper allowances exactly as
in section 39. The C/E remainders have nonnegative coefficients
on every enumerated base state; both programs check that assertion
instead of discarding failures. Thus the finite tests enlarge the
set of possible counterexamples and zero survivors proves the result.

| a | Base states | u states | Packing profiles | Surviving delta tuples |
|---:|---:|---:|---:|---:|
| 14 | 3,100 | 1,301,946 | 26,159 | 0 |
| 15 | 5,624 | 3,879,965 | 83,071 | 0 |
| 16 | 9,813 | 11,135,603 | 320,665 | 0 |

A base state and packing profile have exactly the meanings in
section 39. The independently written Python endpoint calculation
and C direct-delta calculation are compared in the audit. The
completed Python a=14,15 slices used the weaker linear-only LINK-SP.
The cached a=16 replay and the C final run also use LINK-Q.
The unstrengthened comparisons have the same
three base/u/packing columns, which are determined before the
new linked tests.

For a=17, the final C relaxation, with LINK-Q, gives
16,337 base states, 29,039,496 u states, 1,119,332 packing
profiles, and exactly the following four surviving profiles:

```
alpha=7, n0=q2=28, l=u0=u1=k0=k1=beta=b=0, R=10.

r   t    epsilon_M   c0   delta_min  delta_max  m      WA
4   80   18          84   247        665        1056   -48
5   85   10          84   246        841        1050   -42
5   86   11          83   247        836        1049   -38
5   86   11          84   247        838        1049   -38
```

The four intervals contain 2,197 delta tuples. These are relaxed
counts, not realizable tiles. Their outside budgets force c=e=0:
for example even the first C cost c(c+1+q+q2) already exceeds
-WA-1 in every row. Thus m=C(20,3)-r-t is exact, and
W=WA+rho. A counterexample in the respective rows needs

```
0<=rho<=47,  0<=rho<=41,  0<=rho<=37,  0<=rho<=37.
```

There is further exact structure, not just a list of counts.
All these rows require the actual absent-pair graph to be a
matching, with loops allowed. If its minimum cover were at
most r-1, LINK-SP at the worst remaining cover would give:

```
(r,t,m)=(4,80,1056): k=3, e_k<=15, m>=ceil(1590-22.5*15)=1253;
(r,t,m)=(5,85,1050): k=4, e_k<=4,  m>=1288-19.5*4=1210;
(r,t,m)=(5,86,1049): k=4, e_k<=5,  m>=ceil(1288-19.5*5)=1191.
```

Smaller k give still larger lower bounds (direct substitution
in the finite set k=1,...,r-1). Hence tau(G)=r. Any intersecting
pair of edges would have a common-endpoint cover and reduce
this to r-1, so G is a matching. PAIR-ID now says there are
exactly 12, 0, 1 and 1 legal cubic omissions respectively.
No absent pair is low--low, since n0=Q_7.

For the r=4 row the data

```
a=17, alpha=7, r=4, q2=28, t=80, c0=84,
R=10, b=c=e=0, delta=247, m=1056,
WA=-48, D3=164, k_cover=4, e_k=12
```

survive the pre-E-REPAIR necessary count tests even after replacing
all three interval inequalities in P-REPAIR by
`capacity>=H(n)` (zero defect loss). The joint set has n=13,
H(n)=1027 and capacity 1111. The global cyclic A lower bound
is 1054, just below m=1056. The short and wide interval tests
also pass, as does the MIX-PACK relaxation.
`t5/profile_witness.py` replays these numbers exactly.

This refutes the *proposed count-certificate shortcut* of simply
substituting P(12) into the existing scalar tests and declaring
all profiles excluded. It does not refute P(12), or the possibility
that further geometric uses of P(12), HIGH or the band ranges
close this row. In particular it is not an actual residue-complete
counterexample to anything proved.

The linear-only C exploration was also extended to a=18. It gave
26,725 base states, 71,891,624 u states and 4,008,931 packing
profiles, with 175,177 surviving delta tuples. This is a bounded
exploration, not an exclusion. The final quadratic refinement
was not swept over all a=18 profiles; no such claim is made.

There is a separate small certificate for the B-free, full-pair,
link-free branch. The two analytic ends in section 45 reduce it
to 33<=a<2Q_alpha+38 and a>=2alpha+3. For fixed alpha,a,n, use

```
e_min=floor(Q_alpha/4)+1,
e_max=min(floor(((a-2alpha-1)Q_alpha-2a+3alpha)/6),
          floor((B0-2)/3),
          floor((2Q_alpha(n-alpha)-a+2alpha+2U_alpha
                                      -(a+3)Q_alpha)/3)).
```

When e_min<=e_max, JOINT-SP and DELTA-UP require

```
2H(n)-9B0+10+[27-L2(n)]epsilon<=0.
```

This is linear in epsilon, so check the two endpoints.
`t5/b0_strip.c` selects the adverse endpoint;
`t5/b0_verify.py` checks both endpoints independently.
For 4<=alpha<=14 every interval fails. Combined with the two
analytic ends this proves W>=0 for **every a** when
`4<=alpha<=14, r=l=b=0`, for all c,e. At alpha=15 the weaker
scalar test first leaves `(a,n,epsilon)=(44,36,248)`; this is
not a tile and does not assert that the full other tests pass.

## 48. Checks, preserved failures, and limits of the new computations

All computation in this continuation was run on fejer, in
`~/wilf/p9/`, with nice 10 and at most four owned single-core jobs.
The laptop was used only to read/edit/copy files. No commits were
made, no foreign process was changed, and the lead's exhaustive
ambient runs were not duplicated.

The experiment predicates were fixed before each computation:

- The count continuation tests the necessary domain of section 39,
  adding only the proved linked and mixed packing conditions.
  A survivor is a count vector, not evidence of a tile. Zero
  survivors in a fully enumerated a slice give an exclusion.
- `cover_graphs.c` tests PAIR-ID by explicitly enumerating cubic
  divisors and computes the exact minimum cover from every vertex
  subset. It covers every loop graph on n<=6 vertices. A single
  failure would refute PAIR-COVER or its implementation.
- `multi_low.h` in t5 adds actual-instance checks of MIX-ID,
  MIX-EP's underlying nonnegative defect, the BB shadow lower
  bound, MIX-CARD, the improved repaired SP and linked global
  packing. It retains the earlier actual checks from t4. Actual
  runs are controls and inequality checks, not exhaustive bounds
  on the primary regime.
- `p5e_identities.py` verifies seven new rational polynomial identities
  in addition to the 29 imported earlier identities; the numerical
  constants in LARGE-A are exact Fraction comparisons.
- `b0_strip.c` checks the explicit B-free middle strip through
  alpha=40. Its independent Python replay covers alpha=4,...,14
  and checks both endpoints of 49,289 nonempty epsilon intervals.
  The alpha=15,...,40 survivors are deliberately retained.

The graph check gives:

| n | All loop graphs | Equality in C(tau,2)<=D+T | D+T=0 |
|---:|---:|---:|---:|
| 1 | 2 | 2 | 2 |
| 2 | 8 | 8 | 6 |
| 3 | 64 | 36 | 19 |
| 4 | 1,024 | 133 | 55 |
| 5 | 32,768 | 412 | 146 |
| 6 | 2,097,152 | 1,176 | 364 |

The exact formulas and paper proof in section 43 apply to every
n; this table is an independent implementation check, not an
induction base for an otherwise unproved extension.

Actual primary-instance control runs used the following seeds:

```
2026101951: 12,000 proposals, proposed 4 lows, lex, m=200..6000;
2026101952: 12,000 proposals, proposed 6 lows, grlex, m=400..8000;
2026101953:  8,000 proposals, proposed 4 lows, grlex, m=300..7000;
2026101954:  6,000 proposals, proposed 5 lows, grlex, m=300..8000.
```

Proposed A counts were 7..20; actual counts are recomputed after
finding the conductor and primitive generators. The first run
checks the initial repair and mixed identities. The second adds
linked repair, the third includes LINK-Q, and the fourth checks
HOT-WINDOW as well. None is claimed to
sample uniformly or exhaust the matching profiles of section 47.
All found zero failures on 37,743 accepted primary instances:
11,923, 11,929, 7,948 and 5,943 respectively. These counts include
repeated semigroups/tiles and are not uniqueness counts. The last
three runs exhibited strictly improved cover
bounds on 244, 251 and 144 actual instances respectively.

The small structured adversarial test `matching_moduli.py`
examines the r=5,t=85 matching profile with five disjoint off-diagonal
absent pairs sharing one sum modulo p. For p=2,3,5 it enumerates
all residue counts of the 17 units compatible with at least five
such disjoint pairs and tests the tile's residue counts modulo p.
This is an exact finite necessary test for that structured
subfamily; it does not construct a tile. Balanced residue-count
profiles survive: 2, 3 and 10 respectively, out of 26, 333 and
15,225 tested profiles. They are saved, not reported as a closure.
The test shows that individual small-modulus projections do not
exclude even this narrower matching construction. Section 50
subsequently excludes it by E-DELTA. General absent
pairs need not share a residue, and are not covered by that test.

The literature check was restricted to the particular proposed
Fourier tool. Green, *The number of squares and B_h[g] sets*,
Acta Arith. 100 (2001), Theorem 17, proves the asymptotic B3 bound
with leading constant (7/2)^(1/3); its hypothesis has zero triple
excess. The proof's pointwise convolution bound in Lemma 16 uses
that hypothesis. No robust constant-excess version needed here
was found in or deduced from that statement. The primary source is
[Green's paper](https://www.impan.pl/shop/en/publication/transaction/download/product/82571).
This continuation does not cite its asymptotic bound as an exact
finite P(C), and does not claim an impossibility result about
adapting the method.

The lead's Ambient SP12 n=9 log was read after completion. It
reports 220,523,125 DFS nodes, 170,153 complete unpruned leaves,
minimum slack 115 at
`{0,1,4,14,46,65,76,85,93}`, s=94 and excess 14, with no failure.
Its n=10 log was still empty at the last check. These are the
lead's results, not reruns by this agent; neither supplies an
induction step for all n.

Preserved failures and cautions:

1. Extending the old count-code assertion `bc>=0` past its verified
   a<=13 domain is false for the raw enumerated domain. The first
   a found is 17: alpha=3,r=35,q=118,n0=l=q2=u0=u1=0,t=318,
   epsilon=0, WA=-34 gives min(2r,2a-r)=-1. All slices through
   a=16 passed that guard. This is a relaxed Macaulay count profile,
   not a semigroup and not a failure of B-NEIGH. The valid repair
   is `bc=u+max(0,min(2r,2a-r))`, since transfer also pays b*u
   separately. Both final enumerators use that bound. The interrupted
   preliminary a=17 log is retained.
2. Independent worst-case endpoint deletion and cubic excess are
   weaker than their linked treatment. Before keeping the C(k,2)
   cost, the a=15 relaxation retained 2,511 delta tuples and a=16
   retained 2,966. These are not counterexamples to either version;
   they document the lost correlation. The linked version excludes
   both slices.
3. Merely adding Ambient SP12 to the earlier scalar certificate is
   not a proved reduction of the entire frontier. Section 47 gives
   an explicit survivor even with zero interval defect loss. This
   is a failure of that certificate shortcut; no actual tile is
   asserted. The sharp ambient constant itself remains unknown.
4. The earlier signed-union constant counterfamily remains a
   counterexample only to its signed-union assertion. Nothing in
   this continuation changes it into a counterexample to ambient P.

No actual residue-complete counterexample to Wilf or a verified
step of GW-24/26/26c was found. No proof of ambient P(C), for a
constant independent of n in the unresolved range, is claimed.

## 49. HOT-WINDOW and a 129-tuple refinement at a=17

There is a further paper reduction of the four matching rows,
using the actual high offset window rather than a stronger ambient
packing conjecture.

**HOT-WINDOW.** Fix an actual minimum cover k of the absent A-pair
graph, with r>0. The degree of each vertex of that graph is at
most r-k+1: taking that vertex and one endpoint of every edge
outside its star gives a cover of size at most r-deg(v)+1.
Consequently the number j of high units below H0=h-L satisfies

```
j<=E_k:=min(a-alpha,l+r-k+1).
```

Indeed each such high unit has an I2 pair with the minimum low
unit. At most l such pairs are present; every other one is an
absent edge incident to that low unit. For r=0 use E_0=min(p,l).

Put p=a-alpha. For each j between 0 and E_k, write n=p-j and

```
r_h=max(0,r-r_LL-max(0,j-l)),
K_k=max(0,min_{0<=j<=E_k}[C(n+2,3)-n*r_h-e_k]).
```

Here e_k is the legal cubic budget of section 43. The actual
nonexceptional high core has at least K_k present cubic cells:
at most n*r_h cubes are forced by its absent pairs, and at most
e_k legal cubes are missing. All core offsets are at least h-L.
Its nonhot cubes have tau in `[3(h-L),2h)`, an interval with
max(0,3L-h) integers. Residue injectivity implies distinct ordinary
values for these cubes. Thus

```
H3>=K_k-max(0,3L-h),
K_k<=rho+max(0,3L-h).                            (HOT-WINDOW)
```

The first inequality can be replaced by its maximum with zero;
the second follows from the joint short-residue lemma rho>=H3.
The actual-instance checker separately verifies the underlying
interval-occupancy inequality on the actual nonexceptional core.
The graph checker also verifies deg(v)<=r-tau(G)+1 for every
loop graph on at most six vertices.

For each a=17 row, the matching condition gives k=r, l=r_LL=0,
and hence j<=1. The legal cubic budgets v are exactly 12,0,1,1.
The resulting lower core-cubic counts are respectively 126,129,
128,128, since

```
K=min(C(12,3)-10*r-v, C(11,3)-9*(r-1)-v).
```

Because b=c=e=0, a counterexample has W=WA+rho<0, so
`h>=h_min:=m+WA+1`. The function
`m-h+max(0,(h-3delta)/2)` decreases with h. HOT-WINDOW therefore
requires

```
2K<=2m-2h_min+max(0,h_min-3delta).                (HOT-FIN)
```

In all four rows K>m-h_min. It follows that

```
delta<=floor((2m-h_min-2K)/3).
```

This gives the sharper necessary table

| r | t | c0 | m | h_min | K | delta interval |
|---:|---:|---:|---:|---:|---:|:---|
| 4 | 80 | 84 | 1056 | 1009 | 126 | 247..283 |
| 5 | 85 | 84 | 1050 | 1009 | 129 | 246..277 |
| 5 | 86 | 83 | 1049 | 1012 | 128 | 247..276 |
| 5 | 86 | 84 | 1049 | 1012 | 128 | 247..276 |

There are 37+32+30+30=129 delta tuples. Parity of h and delta,
additional offset restrictions, and the full residue-injective
weight problem have not been enumerated, so 129 is an upper
bound on a structured family, not a realization count. The example
at delta=247 in section 47 remains within this refined family.
`t5/profile_witness.py` checks the four HOT-FIN endpoint calculations.

## 50. E-REPAIR closes the matching families

The four families in section 49 are excluded by a stronger use of
the same degree observation. That section's 129-tuple reduction is
retained as an intermediate result; none of those tuples remains
after the following step.

**E-REPAIR.** For the actual minimum cover k of the absent A-pair
graph, replace the previous exception bound min(p,l+r) by

```
E_k=min(p,l+min(r-r_LL,r-k+1)) if r>0,
E_0=min(p,l) if r=0.
```

Every occurrence of E in the section 34 H0 accounting can use
this bound. The reason is that E enters there only as an upper
bound on the number of high units below h-L. Section 49 proved
the degree bound directly. Also at most r-r_LL absent pairs can
be low--high, giving the other term in the minimum. C_H is
increasing in E; the bounds on
outside intruders use alpha+E in the same direction. Therefore
each counterexample, with the same k used in LINKED-DEF, requires

```
delta<=2C_H(E_k)-(a-1)-(a+3)q2-(a+1)u3+5k_quartic
                       -D3-b B_H(E_k)-Omega_H(E_k)-1.   (E-DELTA)
```

Here k_quartic denotes the old quartic count; it is not the
minimum cover k. Both final count programs keep this distinction.
Dropping a nonnegative Omega_H gives the necessary version used
in the small certificate. Its nonnegativity is checked at the
larger old E bound, so it remains valid after reducing E.

All four a=17 families have minimum cover k=r, l=b=c=e=0,
u3=k_quartic=0 and n0=q2=28. Hence E_k=1. Their new constants
and necessary delta upper bounds are

| r | t | c0 | C_H(1) | D3 | E-DELTA upper | LOW-FIN lower |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 80 | 84 | 471 | 164 | 201 | 247 |
| 5 | 85 | 84 | 471 | 160 | 205 | 246 |
| 5 | 86 | 83 | 470 | 163 | 200 | 247 |
| 5 | 86 | 84 | 471 | 163 | 202 | 247 |

Each interval is empty. This is a paper exclusion of all four
rows, using the finite count reduction only to obtain their list.
In particular the pre-E-REPAIR witness in section 47 is now excluded;
it remains a useful counterexample to the earlier count shortcut.

**Theorem T2-SMALL17 (finite certificate).** Under the primary
hypotheses, a<=17 implies W>=0 for every alpha,b,c,e. For a<=16
use section 47. At a=17 the exhaustive necessary count relaxation
leaves precisely the four rows, each excluded by E-DELTA above.
The final C version also includes E-DELTA directly and gives zero
survivors, providing a redundant check of the row argument.

There is a uniform analytic consequence beyond these four rows.
Suppose alpha=A>=4, all low pairs are present, and
`l=b=c=e=0`. A counterexample has q2=Q_A, u1=k1=0. A-LOW gives
a>5A/3+1. Combining LOW-FIN and E-DELTA, and using
c0<=U_A, 4k0<=(A+3)u0, yields the necessary inequality

```
4a-6A+2(2A+1-a)Q_A+4D3
        -6E_k[1+A(a-A)]-6C(E_k+2,3)<=0.           (LOW-H(E))
```

For completeness the exact pre-shadow difference of the lower
bound for 3delta and three times its upper bound is

```
4a-6A+(6A+6-2a)Q_A-6c0
 +4(a+1)u0-18k0+4D3
 -6E_k[1+A(a-A)]-6C(E_k+2,3).
```

Replacing c0 by U_A gives the displayed Q_A term. The remaining
u0 coefficient is nonnegative because 8a-9A-19>0 follows from
A-LOW for A>=4, as in section 36. Thus LOW-H(E) is a uniform
necessary condition, not a finite-grid observation. At r=0 it
recovers LOW-H. If the missing pairs form a matching, E_k=1 and
PAIR-ID gives D3=2(a-1)r+3v, with v the legal missing-cubic
count. In that case a counterexample requires

```
8(a-1)r+12v+4a-6A-12
       +2(2A+1-a)Q_A-6A(a-A)<=0.                 (MATCH-LOW)
```

The four row exclusions are also immediate from this inequality.
The exact difference identity is included in the Fraction audit.

The following local cover refinement is stronger than the simple
E_k bound, and is the final version used in the replay certificate.
Let j be the number of low vertices in an actual minimum cover k,
and put f(j)=alpha*j-C(j,2). Necessarily

```
max(0,k-p)<=j<=min(alpha,k),
r<=a*k-C(k,2),        r_LL<=f(j).                (LOCAL-COVER)
```

Indeed a cover of j low vertices meets at most f(j) low pairs;
all other low pairs must be present. Equivalently
`n0>=C(alpha-j+1,2)`. The total-pair bound is the same argument
on all a vertices. This rejects a proposed k when no such j exists.

Distinguish whether the minimum low unit belongs to the chosen
cover. If it does not, every absent pair from it to a high unit
ends at a covered high vertex. Therefore its missing high-neighbor
count is at most

```
min(k-j,r-r_LL,r-k+1)                 if j<alpha.  (E0)
```

If it belongs to the cover, the other j-1 low vertices can cover
at most f(j-1) absent low pairs. Its own missing low degree is
therefore at least d_L=max(0,r_LL-f(j-1)). Since its total missing
degree is at most r-k+1, its missing high degree is at most

```
min(r-r_LL,r-k+1-d_L)                  if j>=1.   (E1)
```

A negative latter bound makes this membership case impossible.
Take the maximum of all feasible E0/E1 bounds over feasible j,
add l, and cap at p. Denote this result by Ehat_k. If there is no
feasible case, discard k. For r=0, Ehat_0=min(p,l). Each actual
minimum cover supplies one of these cases, so its actual exception
count is at most Ehat_k. Moreover Ehat_k<=E_k. Substitution of
Ehat_k for E_k in E-DELTA is therefore valid. These are elementary
cover counts, not a conjectural Sidon or Fourier estimate.

**Theorem T2-SMALL18 (two-stage finite certificate).** Under the
primary hypotheses, a<=18 implies W>=0 for all alpha,b,c,e.
For a<=17 use the preceding theorem. For a=18 the C enumeration
with the simpler degree-only E-REPAIR (E=min(p,l+r-k+1)) has

```
26,725 base states; 71,891,624 u states;
4,008,931 packing profiles;
151,063 surviving delta tuples in 90 profile hulls.
```

`t5/replay_profiles.py` independently reads all 90 exported hulls.
For each hull and each allowed k it computes e_k, tests LOCAL-COVER,
computes Ehat_k and the new E-DELTA upper bound, and checks the
linked global A and short/wide/joint packing inequalities. It
finds zero surviving hulls. This is a complete bounded certificate:
the initial enumeration is exhaustive on the section 39 necessary
domain, and its first/last-delta hulls enlarge its survivor set.
For a fixed k all the interval packing tests increase in delta;
thus it suffices to test them at the smaller of the hull's upper
endpoint and E-DELTA's upper bound, provided it is at least the
hull's lower endpoint. Global packing is independent of delta.
No interval containing an actual candidate is lost by this replay.
No ambient packing conjecture is used.

The same independent replay also excludes the five earlier a=16
profile hulls and the four a=17 hulls. This replay does not claim
to be a second full-domain enumeration at a=18. The completed
full Python domain slices are a=14,15,16; the bounded-loop a=16
replay agrees exactly on all three count columns with C. Two
slower redundant a=16 sweeps and an optional GLOC-pruned a=17
continuation were stopped. No completed full Python a=17 or 18
sweep is claimed. The C full-domain enumeration and the independent
bounded replay, with the stated analytic pruning, are the actual
dependencies of the small theorem. The source and every exported
hull used by the replay are retained.

For example the a=18 raw hulls include alpha=7,r=18,n0=14,
epsilon_M<=7. The generic cover upper bound forces k=1 there,
but r_LL=28-14=14 exceeds f(1)=7. LOCAL-COVER immediately excludes
that apparent star. This illustrates the missing consistency
condition between global pair repair and the low face; it was
not an actual residue-complete counterexample.

## 51. P5e status and exact remaining work

The full primary regime, and Wilf for every numerical semigroup
with 3m<c_S<=4m, remain open in this report. The new mathematical
results of this continuation are PAIR-COVER and its linked defect
packing, MIX-PACK, E-REPAIR/LOCAL-COVER, the conditional P47-B0
certificate (optimized to C_dagger), HOT-WINDOW, and the analytic
LARGE-A theorem.
The new finite certificates extend T2-SMALL through a=18 and
close `r=l=b=0` for 4<=alpha<=14 for every a. The lead has not
independently reviewed these new statements; their proof and
finite-verification dependencies are stated above.

Subject to those explicit finite certificates, every remaining
counterexample must satisfy all FRONTIER-41 conditions and

```
alpha>=4,
19<=a<16*C(alpha+1,2)^2,
LINKED-DEF, LINK-SP/Q/PSP, HOT-WINDOW, LOCAL-COVER,
E-DELTA with Ehat_k, and MIX-PACK.
```

This is a uniform explicit bound on a for every fixed alpha.
It is not an absolute finite bound on alpha: the low population
is still unbounded. Each fixed alpha now has a finite search,
since section 38 also bounds b,c,e,m and every active weight.
The four intermediate a=17 matching families and all 90 a=18
profile hulls are excluded in section 50.

In the branch r=l=b=0 a counterexample further needs

```
alpha>=15, a>=2alpha+3,
33<=a<2*C(alpha+1,2)+38,
epsilon_M>Q_alpha/4 and MID-B0,
alpha+R>=33.
```

P(C_dagger), with exactly zero lower-order error, would remove
this entire branch. Even after assuming that P, the branches
r+l+b>0 still require a uniform geometric/payment argument;
no claim that they have already been reduced to P is made.

The next precise uniform packing target is P(C_dagger) on
pair-distinct integer sets with n>=33, retaining the ordinary
unordered triple excess. The next precise finite target is the
a=19 necessary domain with LOCAL-COVER and Ehat_k included from
the start; no a=19 exclusion is claimed. A successful uniform
argument must also use the r/l/B budget beyond the present
P-REPAIR count substitution. Section 47 identifies a historical
profile which E-REPAIR now excludes. For the general branch the
remaining task is to close the coupled k/Ehat_k/legal-defect
inequalities uniformly, retaining their coupling.

For a numerical semigroup the translation is
`h=c_S-3m`, `a=#{minimal n>m : n<c_S-2m}` and
`alpha=#{minimal n>m : 2n<c_S-m}`. Thus T2-SMALL18 proves Wilf
in this conductor range when a<=18, and LARGE-A proves it when
`a>=16*C(alpha+1,2)^2`. Together with the earlier zero-, one-,
two- and three-low results, any remaining semigroup has the
explicit parameters just displayed. These are partial extensions,
not a proof for every c_S<=4m.

Since a is at most the embedding dimension minus one, the finite
certificate also covers every semigroup of embedding dimension
at most 19 in this conductor range.

The reproducible P5e artifacts are in `src/scratch/gw/p5/t5/`.
The audit compares the independent count outputs, graph enumeration,
B-free endpoints, polynomial identities and actual-instance logs;
`AUDIT.json` records totals and `SHA256SUMS` records the remote
source/report/log inventory. Failed preliminary logs are retained.
