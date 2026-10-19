# P6c: height-three MaxCL, exact window payments and incomplete rows

2026-10-19. Status: proved partial results, an explicit obstruction to the
proposed face-free slack argument, and computational checks. This report
does not prove height-three MaxCL in full. P6_REPORT.md and P6B_REPORT.md
are unchanged. No commits were made. All calculations ran on fejer, in
`~/wilf/p6c`, with nice 10 and single-core processes.

## 1. Scope and notation

Use the accepted spike reduction. A core C has k non-maximal units, q
pairs, p non-maximal pairs N2, and t cubics T. Its maximal pairs are A2,
with a=q-p. There are s=m-|C| spikes, d=k+s, and

```
|C|=1+k+q+t,       m=1+k+s+q+t,
Q_k=binom(k+1,2),  e=Q_k-q.
```

Throughout the height-three statements, C is a down-set and its linear
labels are injective modulo m. Missing residues are filled by spikes.
At a phase sigma put r(x)=(phi(x)-sigma) mod m, rho0=r(0),
rho_i=r(e_i), nu=m-rho0, and

```
ell(x)=sum_i x_i rho_i-(|x|-1)rho0,
K(x)=(ell(x)-r(x))/m,
psi(z)=sum_{i:z+e_i in T}(z_i+1),
deg_Q(i)=sum_{z in Q} z_i,
delta_i=k+1-deg_Q(i) >=0.
```

The accepted nonnegative expression is

```
Lplus=sum_i (s+delta_i)rho_i
      +sum_{z in N2}(d+2-psi(z))r(z).
```

MaxCL is S>=0, where

```
S=(d+1)(rho0+sum_i rho_i+sum_N2 r)-sum_A2 r-2sum_T r.
```

Let W=[nu,m), Pminus and Pplus be the numbers of N2 pairs of carry
-1 and +1, respectively, and

```
OW=rho0-#{z in A2:K(z)=-1}.
```

Thus OW counts the cells of W other than maximal pairs of carry -1.
The lead's exact identity, used here with all spikes counted, is

```
S=HCprime+m #{z in A2:K(z)=1},
HCprime=Lplus+m(OW+B),
B=2sum_T K-sum_N2 (psi-1)K.                    (HC)
```

Accepted input: height <=2; all k<=4 and all d<=5; DENSE075;
the full-pair few-cubic theorems; CR, FLAT-CR, and MIN-PHASE. In
particular the lead's H3-CORE4 is used as proved, not rerun.

## 2. Exact payment of all but one unit per cubic

For each cubic y define, with one term per distinct divisor and the
indicated multiplicity,

```
kappa_y=2K(y)-sum_{i:y_i>0} y_i K(y-e_i).
```

**Lemma WINDOW-ID (proved).** Put

```
v_y=1_{r(y) in W},        b_y=kappa_y+v_y,
beta=#{y in T:b_y=-1},    gain=sum_y max(0,b_y),
Orest=OW-Pminus-sum_T v_y.
```

Then Orest>=0, every b_y>=-1, and exactly

```
HCprime=Lplus+m(Orest+Pplus+gain-beta).          (WINDOW-ID)
```

Consequently, at every phase and with no face or dimension hypothesis,

```
HCprime >= Lplus-m beta >= Lplus-m t.           (WINDOW-LOSS)
```

Proof. CUBIC-LIFT gives

```
2ell(y)+rho0=sum_i y_i ell(y-e_i),
m kappa_y=sum_i y_i r(y-e_i)-2r(y)-rho0.
```

The right side is greater than -3m, so kappa_y>=-2. If r(y)<nu,
then 2r(y)+rho0<2m, so kappa_y>=-1. Thus b_y>=-1. Each N2
pair of carry -1 lies in W; those pairs and the cubics in W are
distinct cells counted by OW. This proves Orest>=0. Finally

```
sum_y kappa_y=2sum_T K-sum_N2 psi K,
B=sum_y kappa_y+sum_N2 K
 =sum_y kappa_y+Pplus-Pminus.
```

Insert this in (HC) and separate the negative and positive b_y. QED.

This is an exact reduction of HCprime>=0 to a packing/payment problem
with cost one per bad cubic. It does not assert that beta is zero.
In particular the earlier false lower bound kappa>=-1 has not been
reintroduced: kappa=-2 is explicitly allowed and paid once by its own
window cell.

**Shape-only consequence WINDOW-RANK (proved).** Sort the k+p
nonnegative coefficients

```
{s+delta_i}_i union {d+2-psi(z)}_{z in N2}
```

in descending order w_0,...,w_{k+p-1}. Put Lambda=sum_j j w_j.
If Lambda>=mt, then HCprime>=0 at every phase. More generally a
proved bound beta<=b permits Lambda>=mb instead.

Indeed the k+p residues supporting Lplus are distinct nonnegative
integers. Rearrangement gives Lplus>=Lambda; apply WINDOW-LOSS.
This is an additional sufficient condition, not an equivalence or a
replacement for CR.

## 3. Common cubic factor at its zero phase

**Theorem CONE-PHASE (proved).** Suppose every cubic contains x_i.
At sigma=phi(e_i),

```
OW+B>=0,        HCprime>=Lplus>=0.               (CONE)
```

There is no restriction on k, q, t, or the number of spikes.

Proof. Here rho_i=0. A non-maximal pair not containing i has only
one possible cubic cover, namely z+e_i, so psi(z)=1. Every pair
containing i has K in {-1,0}. Let Z be those N2 pairs containing
i with K=-1. Define

```
w_y=sum_{c:y-e_c in Z} y_c.
```

Then

```
B=2sum_y K(y)+sum_y w_y-|Z|.
```

For every cubic containing i,

```
-2K(y) <= w_y+1_{K(y)<0,r(y) in W}
                  +1_{y_i=1,K(y)=-2}.          (LOCAL-CONE)
```

Here is the complete local verification. For K>=0 the assertion is
immediate. If rho0=0 there is no negative cubic. Otherwise:

* y_i=3: w_y=3. A carry -2 cubic is in W; carry -1 costs only 2.
* y_i=2, with remaining unit residue u: w_y=1+2[u<rho0].
  Carry -2 forces u<rho0 and r(y) in W. For carry -1, either
  u<rho0 and w_y=3, or u>=rho0 and r(y) in W, giving 1+1=2.
* y_i=1, with remaining residues u,v, allowing u=v:
  w_y=[u<rho0]+[v<rho0], with multiplicity. Carry -1 forces
  u+v<2rho0. If both are below rho0 the weight is 2. Otherwise
  the weight is 1 and u+v>=rho0 makes r(y) in W. Carry -2 forces
  u+v<2rho0-m<rho0: the weight is 2, the cubic is in W, and
  the last indicator supplies the fourth unit.

Each last indicator has its own additional N2 pair z=y-e_i, not
containing i. Its lift is u+v-rho0<0 and its residue is nu+u+v,
which lies in W. These pairs are distinct for distinct y. They are
disjoint from Z and from all cubics. Thus OW pays |Z|, all the cubic
window indicators, and all the last indicators in LOCAL-CONE, each
once. Summation proves OW+B>=0. QED.

The distinctness of the last group of pairs is essential. Reusing the
origin once for every negative cubic would not prove this theorem.

For reference a conservative defect version follows. At the zero phase
of x_i let u be the number of cubics not containing i, and pnew the
number of pairs covered by these cubics but by none containing i.
Then

```
HCprime >= Lplus-m(7u-pnew).                    (CONE-DEFECT)
```

To see this, first retain only the cubics containing i. The previous
window payment holds. Adding the other cubics changes their own carry
term by at least -4u. Their weighted pair incidences total 3u;
the subtraction of psi-1 costs at most 3u-pnew, since K(pair)<=1.
The newly non-maximal negative pairs increase OW, which helps. This
proves the displayed bound. It is not needed for the one-cubic theorem.

## 4. One cubic: an unconditional family in every dimension

**Lemma ONE-PAIR-PHASE (proved).** If t=1 and a non-maximal pair has
residue zero, then HCprime>=Lplus.

Proof. Write y for the cubic and p for its number of distinct pair
divisors. A zero-residue divisor z0 has K(z0) in {0,1}. Hence
ell(y)=mK(z0)+rho_c-rho0>-m and K(y)>=-1. If K(y)=-1, all its
pair lifts are <rho0<m, so all pair carries are <=0 and

```
2K(y)-sum_N2(psi-1)K >=-2.
```

For K(y)=0 the same expression is >=-(3-p)>=-2; for K(y)>=1
it is nonnegative. Since no unit has residue zero, all core-unit
residues are >=1. Negative maximal pairs have residues >=nu+2.
Thus OW>=min(2,rho0), paying the possible loss if rho0>=2.
If rho0<=1, all unit residues are >=rho0; then K(y)>=0 and
K(y-e_c)<=K(y). Since sum(psi-1)=3-p, the expression is at least
(p-1)K(y)>=0. QED.

The window observation used here is useful independently:

```
L=min_i rho_i  ==>  OW>=min(rho0,2L).            (WINDOW-MIN)
```

It follows because a maximal pair of carry -1 has residue
nu+rho_i+rho_j>=nu+2L. Spikes are included in OW.

**Lemma ONE-DEFICIT (proved, sharp).** For t=1, OW+B<0 occurs
exactly in the following situation:

```
K(y)=-1, r(y) in W, every N2 pair has K=0, OW=1.
```

Its value is then -1. Such a phase necessarily has core units of
residues 0 and 1, both outside the cubic; rho0<m/2; and every N2
pair has residue >=2. In particular m>=17.

Proof of the classification. Write p=|N2|, so sum(psi-1)=3-p.
If K(y)>=1 then B>=2-(3-p)>=0. If K(y)=0, a weighted pair
of carry +1 is impossible: its deleted direction occurs at least
twice in y, hence also in the pair, and both units of a +1 pair
have residues >rho0. Adding the deleted unit would give K(y)>=1.
Thus B>=0. If K(y)=-2 all pair divisors have carry -1; B=-p-1
and OW>=p+1 pays it. If K(y)=-1 and r(y) outside W, all pairs
again have carry -1; B=1-p and OW>=p. Finally if K(y)=-1 in W,
all pair carries are <=0, B>=-2 and OW>=1. Equality OW+B=-1
forces OW=1, all weighted pair carries zero, and no unweighted
negative pair, since that would be a second OW cell. This proves
the displayed characterization.

Let b=r(y)-nu. The pair residues are b-rho_c for the deleted
unit c. They are nonnegative. If b=0, all factors have residue
zero, contradicting sum y_c rho_c=rho0+b with rho0>0. So b>0.
The window's first position nu is not the cubic and must be a
negative maximal pair; its unit sum is zero, so a zero unit is
present. Pair residues cannot be zero, hence b=1 would force all
cubic factors to be zero, again a contradiction. Thus b>=2.
The next window position nu+1 must also be a negative maximal pair,
forcing a unit of residue 1. Both units are non-maximal because
these pairs are present. Every pair residue avoids the unit residues
0 and 1, so is >=2. Thus every cubic factor has residue <=b-2<rho0.
If a cubic factor had residue <=1, a divisor pair containing it
would require its other factor to have residue >rho0, a
contradiction. Both units are therefore outside the cubic. Also

```
6<=sum_c y_c r(y-e_c)=2b-rho0<=rho0-2.
```

It follows that rho0>=8. The origin is a second OW cell if it is
in W, so rho0<nu and m>=2rho0+1>=17. QED.

**Theorem ONE-COVERED (proved analytically).** Suppose t=1, k>=2,
every unit touches a missing pair (a missing loop counts), and

```
s(Q_k-1)+e>=4.                                  (COVER-BUDGET)
```

Then HCprime>=0 at every phase. In particular the conclusion holds
for every k>=7 under the stated missing-pair coverage hypothesis.

Proof. Coverage says delta_i>=1 for every i. If some N2 pair is at
zero, use ONE-PAIR-PHASE. Otherwise select one N2 pair: its residue
is positive and its coefficient in Lplus is >=d-1. The k unit
coefficients are >=s+1, their residues are distinct, and they avoid
that pair. As d-1>=s+1, rearrangement, with the pair forbidden from
zero, gives

```
Lplus >=(d-1)+(s+1)(Q_k-1)=(s+1)Q_k+k-2,
Lplus-m >=s(Q_k-1)+e-4>=0.
```

WINDOW-LOSS with t=1 completes the proof. For k>=7, coverage implies
2e=sum delta_i>=k and e>=4. QED.

**Theorem ONE-PARTIAL-COVER (proved analytically).** Let t=1 and
let g be the number of units with delta_i=0, v=k-g>=2. Then
HCprime>=0 at every phase provided

```
s[binom(v+1,2)-1]+e+k-6 >= g(2k-g+1)/2.         (PARTIAL-COVER)
```

Only a ONE-DEFICIT phase needs proof. Retain the v defective-unit
coefficients, each >=s+1, and one N2 coefficient >=d-1. Its residue
is >=2. Since d-1>=s+1, rearrangement allowing this pair residue
2 and the unit residues 0,1,3,...,v gives

```
Lplus>=2(d-1)+(s+1)[binom(v+1,2)-2].
```

Its difference from m is exactly the left side of PARTIAL-COVER
minus its right side. Apply WINDOW-LOSS. QED.

In particular for g=0 the sufficient condition is
s(Q_k-1)+e+k>=6, which is automatic for k>=4 under coverage
(2e>=k). For g=1 it is s[binom(k,2)-1]+e>=6, automatic
at k>=12 because 2e>=k-1. Thus the one-cubic HCprime theorem
also includes at most one complete quadratic row when k>=12.

**Corollary ONE-COVERED-ALL (proved analytically plus accepted k<=3).**
MaxCL holds at every phase
for every one-cubic tile whose missing-pair graph covers all its core
units, for every k and any spike count.

For k<=3 use the accepted core theorems; for k>=4 use
ONE-PARTIAL-COVER with g=0. These small-core uses assert MaxCL,
not the stronger HCprime statement. The latter is analytic for k>=4.

An auxiliary finite check was made for the only k=6 case left by
the weaker COVER-BUDGET argument: s=0,e=3. Coverage then forces
three disjoint ordinary missing pairs, q=18 and m=26. There is no
injective labeling even of its origin, units and present pairs.
The full enumeration `c/matching6.c` checks all
177100 six-element subsets of {1,...,25}, all 15 perfect matchings
on each set (2656500 cases), and finds zero pair bases. This is a
finite nonexistence statement. The strengthened analytic theorem
does not need this enumeration.

**Further one-cubic reductions (proved).** At the origin-zero phase,
HCprime>=Lplus: K(y)>=0 and K(y-e_i)<=K(y), so the same
(p-1)K(y) argument applies. At a unit in supp(y), CONE applies.
Thus by MIN-PHASE a one-cubic MaxCL counterexample would have its
minimum at a unit outside supp(y). ONE-COVERED-ALL says its missing
graph must have an isolated vertex: a complete quadratic row.
The full-pair case is already the accepted ONE-CUBIC theorem.

For k>=15, FLAT-CR also closes every one-cubic tile with s>=4.
Indeed its worst value at s=4,p=1,q=Q_k is

```
4 binom(k,2)-3(k+Q_k+5)=(k-15)(k+2)/2>=0,
```

and the s coefficient binom(k,2)-3 is positive. Therefore the new
one-cubic remaining family at k>=15 has s<=3, some missing pairs,
some complete quadratic rows, and a zero unit outside the cubic.
If there are g complete rows, PAIR-PACK on those g directions further
forces

```
g^2+g <= k+q+4                                  (if s<=3).
```

These are necessary conditions, not existence assertions.

## 5. A stronger flat bound from missing quadratic degrees

**Lemma DEFECT-FLAT (proved).** Sort delta_i in descending order and
put F_G=sum_{j=0}^{k-1} j delta_(j). If c=k+1,
2e=cf+r with 0<=r<c, set

```
F_e=c f(f-1)/2+fr >= 2e^2/(k+1)-e.
```

Then F_G>=F_e, and at every phase

```
S>= s binom(k,2)+F_G+(d+2)binom(p,2)
       -3t(m-1)+t(t-1).                         (DEFECT-FLAT)
```

Proof. The k unit residues are distinct, so
sum_i delta_i rho_i>=F_G. Each delta_i<=k+1 and sum delta_i=2e;
putting this mass on the smallest ranks, up to capacity k+1 per
rank, gives F_e. Its difference from 2e^2/(k+1)-e is
r(c-r)/(2c)>=0. Insert the improvement of U into the accepted
HYBRID-ID proof of FLAT-CR. All other steps are identical. QED.

For example this proves, without any complete-face hypothesis,

```
t=1, k>=36, e^2>=k^3  ==> MaxCL at every phase.  (ONE-LARGE-DEFECT)
```

Indeed the s coefficient is >=binom(k,2)-3>0. At s=0 it suffices
to have F_e>=3(k+Q_k+1). F_e is increasing with e in the indicated
range, and at e=k sqrt(k) it is at least
2k^3/(k+1)-k sqrt(k). For k>=36, sqrt(k)<=k/6 and
2k^3/(k+1)>=2k^2-2k. The required difference is at least
k^2/3-13k/2-3>0. These are real endpoint comparisons; integral e
only improves them. This is a uniform sufficient condition, not an
enumeration in k.

**Theorem CUBIC-DEGREE (proved, with unbounded t and k).** If

```
2<=t<=k/2,          delta_i>=t for every core unit i,
```

then HCprime>=0 at every phase, with any number of spikes. Thus
MaxCL holds for this family of incomplete quadratic faces.

Proof. For a fixed pair z, each cubic successor contributes 1,
with at most two extra units of multiplicity (a loop's pure cube
contributes 3, or an ordinary pair has two successors contributing
2). Therefore psi(z)<=t+2, and its Lplus coefficient is at least
c=d-t. Unit coefficients are at least w=s+t. The hypothesis
k>=2t gives c>=w. Also t>=2 forces at least two distinct N2
pairs: a single pair can support only its one pure cube. Retain
two pair coefficients c and the k unit coefficients w. Distinctness
and rearrangement, allowing the pairs the two smallest residues,
give

```
Lplus>=c+w sum_{j=2}^{k+1}j
      =(d-t)+(s+t)(Q_k+k).
```

The difference of this bound from mt is exactly

```
s(Q_k+k+1-t)+k+te-t^2-2t.
```

Since 2e=sum delta_i>=kt and k>=2t, it is at least

```
s(Q_k+k+1-t)+k(1+t^2/2)-t^2-2t
 >=s(Q_k+k+1-t)+t^2(t-1)>=0.
```

Apply WINDOW-LOSS. QED. Unlike a t=1,2,3 finite table, this
closes a family in which both the number of cubics and the core
dimension are unbounded. The condition is on missing quadratic
incidences; it is not assumed automatically for arbitrary cores.

## 6. Quantile arc at an upper semicircle

**Theorem UPPER-ARC (proved).** At a phase define

```
G={i:2rho_i>=m+rho0}, g=|G|, eta=(m+rho0) mod 2.
```

Let a_j count maximal pairs with j factors from G, and t_j count
cubics with j factors from G, with multiplicity. Put

```
cost=a_1+2a_0+4t_2+6t_1+8t_0.
```

Then

```
S>=Lplus+m(2g-d-1+eta-cost).                     (UPPER-ARC)
```

If g>=2, a further bound is

```
S>=m(2g-k-1+eta-cost)
       +s(g ceil((m+rho0)/2)-m).                 (UPPER-PAY)
```

In particular cost<=2g-k-1+eta implies MaxCL. If all core units
belong to G and k>=2, this gives the explicit positive bound

```
S>=m(k-1+eta)+s(k ceil((m+rho0)/2)-m)>=0.
```

Proof. A pair with 2,1,0 high factors has K>=1,0,-1. A cubic
with j high factors has K>=j-2, for j=0,1,2,3. High cubics have
carry 1 or 2. Write t32 for the number with carry 2 and
LT=t_2+2t_1+3t_0. Since sum_N2(psi-1)=3t-p and K(pair)<=1,

```
Br0:=sum_A2 K+2sum_T K-sum_N2(psi-1)K
 >=q-t-a_1-2a_0-2LT+2t32.
```

Every high cubic of carry 1 has residue >=ceil(nu/2). The g high
units also lie in Y=[ceil(nu/2),m). They are distinct, so

```
t32>=t_3-|Y|+g,       2|Y|=m+rho0-eta.
```

Substitution gives rho0+Br0>=2g-d-1+eta-cost. The accepted unit
identity S=Lplus+m(rho0+Br0) proves the first bound. In Lplus
retain only the s part of the g high-unit coefficients; this proves
UPPER-PAY. Its last term is nonnegative for g>=2. QED.

This theorem uses residue injectivity in the arc, not a full quadratic
face. It proves a range of individual phases; it does not imply that
every minimizing phase belongs to that range.

## 7. The proposed face-free positive spike bound is false

Take three groups of r variables, r>=1. C consists of the monomials
choosing at most one variable from each group. Put b=r+1 and give
the groups labels

```
1,...,r;       b,2b,...,rb;       b^2,2b^2,...,rb^2
```

modulo m=b^3. The cells are exactly the base-b digit strings; hence
the labeling is bijective, C is a down-set, every unit is non-maximal,
and

```
k=3r, q=p=3r^2, t=r^3, s=0.
```

Thus no inequality s>=c t^2/k^4 with c>0 holds for arbitrary
height-three cores. Nor can an error of lower order than k^2 repair
it, since t^2/k^4=r^2/81. This is not a counterexample to MaxCL.

It also refutes an eventual assertion that CR alone, or CR plus a
positive spike bound, closes every large k. Here

```
2R(0)=-2r^6+15r^5+51r^4+52r^3+21r^2+3r.
```

It is negative for every r>=11. Explicitly, with r=11+x,

```
-2R(0)/r=28080+46872x+13995x^2+1709x^3+95x^4+2x^5.
```

For r=1,...,10 the expression R(0) is positive. At r=11 the
complete data are k=33,m=1728,p=q=363,t=1331,s=0,
R(0)=-154440. The next section proves its exact minimum S=5595480.
The example has t/U_k tending to 2/9, so it lies in a fixed-density
middle regime. Its exact CR spike threshold is -R(0)/(J-2t),
asymptotic to 2r^2/9. The threshold depends on the quadratic shadow;
substituting the full-pair value p=Q_k would give a different constant.

Even in the new k>=5 frontier, a small zero-spike example is the
unequal three-group product (r1,r2,r3)=(1,1,3), with k=5,m=16,
q=p=7,t=3. This is a counterexample to the positive-slack assertion,
not to the accepted k=4 or d=5 theorems.

A smaller zero-spike witness in the precise remaining dimension
range k>=5,d>=6 is

```
k=d=6, m=12, P=(3,1,4,7,2,8),
Q={00,12,23,45}, T={000}                         (zero-based indices).
```

Its residues are the origin 0, units 3,1,4,7,2,8, pairs 6,5,11,10,
and cubic 9. It has s=0. This is the least possible modulus for a
zero-spike genuine height-three core in this dimension range:
s=0 forces k=d>=6, and a cubic with u distinct factors has u pair
divisors; covering the other units requires at least
ceil((k-u)/2) more pairs. Thus q>=ceil((k+1)/2)>=4 and
m>=1+6+4+1=12. The balanced infinite family, rather than this
small example, refutes the proposed leading-order middle bound.

## 8. Mixed-radix products: all phases, all heights, all spike lifts

**Theorem DIGITAL-STAR (proved).** Let H>=2, r_j>=1, b_j=r_j+1,
M_j=product_{i<j}b_i, and

```
m0=product_j b_j,     k=sum_j r_j,     t=product_j r_j.
```

Use H groups of variables with labels a M_j, 1<=a<=r_j, and let
C consist of the cells choosing at most one variable from each group.
For any m=m0+s>=m0, keep these labels modulo m and add one isolated
unit on every missing residue. This tile satisfies MaxCL at every
phase. Its height is H and its core dimension k is unbounded.

If S0 is its unspiked slack at phase zero and n=m0-t, then

```
S_m(sigma)>=S0+s binom(n,2)>=0.                  (DIGITAL-LIFT)
```

Proof, including the prefix and spike steps. The integer cell labels
are exactly 0,...,m0-1. The maximal-cell labels T0 are the digit
strings all of whose digits are nonzero; all maxima have height H.
For 0<=u<=m0 let F(u)=#(T0 intersect [0,u)). Then

```
m0 F(u)<=t u.                                   (PREFIX)
```

An elementary coupling proves this. For each j take independent
uniform real U_j in [0,1), and compare floor(b_j U_j) with
1+floor(r_j U_j). The latter is always at least the former. The
weighted sums are respectively uniform on all digit strings and on
T0. Their prefix probabilities give PREFIX. A finite proof uses a
uniform integer from 0,...,r_j(r_j+1)-1 and the floors of its
quotients by r_j and r_j+1; the same inequality and uniform
marginals hold. This avoids a measure-theoretic input in Lean.

Put A=sum_{v in T0}v. At modulus m0 the maximal residue sum is

```
A(u)=A-tu+m0F(u)<=A.
```

The no-wrap column-top lemma gives
S0=(k+1)binom(m0,2)-(k+H)A>=0. Since all maxima have the same
height, S_{m0}(u)>=S0 at every phase. Also

```
(k+H)t<=k m0,                                   (DENSITY)
```

either by counting maximal column lengths or directly: each term
(r_j+1)t/m0=r_j product_{i!=j} r_i/(r_i+1) is <=r_j.

For the spike lift, write x=m-m0 and first take 0<=u<m0. Let
N(u) be the base sum of non-maximal residues and FN(u)=u-F(u).
The exact first-form slack satisfies

```
S_m(u)=S_{m0}(u)
       +x[N(u)+(k+1)FN(u)-(H-1)F(u)]+x^2 FN(u).
```

PREFIX and DENSITY give
(k+1)FN(u)-(H-1)F(u)=(k+1)u-(k+H)F(u)>=0.
The n non-maximal residues are distinct, so N(u)>=binom(n,2).
This proves DIGITAL-LIFT on this phase range. For m0<=u<m,
put y=m-u. All core residues are the original integer labels plus y,
and

```
S_m(u)=S0+x N(0)+y[(k+x+1)n-(H-1)t].
```

The bracket is nonnegative by DENSITY, and N(0)>=binom(n,2).
This proves the other range. QED.

For H=3 all maximal pairs are absent, so HCprime=S. Thus the theorem
also proves HCprime>=0 on these families, with any spike count.

For the balanced three-block family,

```
sum_T phi=r^2(r+1)(m0-1)/2,
min_sigma S=(r+1)^2(4r+1)(m0-1)/2.
```

The minimum is at zero by PREFIX. At r=11 it is 5595480, as stated.

## 9. Partial rows and their height-H extension

**Lemma RECTANGLE-PACK (proved, every height).** Let D be any
injectively labeled finite down-set modulo m, J a nonempty set of h
unit directions, and

```
F_J={z in D:z+e_i in D for every i in J}.
```

Then all the reduced labels

```
phi(z), and phi(z)-phi(e_c) for c in J\supp(z),  z in F_J
```

are distinct. Consequently

```
m>=sum_{z in F_J}(h+1-|supp(z) intersect J|).    (RECTANGLE)
```

Proof. Write c=0 for the unreduced positive label, with e_0=0.
An equality gives phi(z+e_{c'})=phi(z'+e_c). Both cells are
present by definition of F_J. Injectivity makes the formal vectors
equal. Their reduced signed forms, with the negative direction
outside the positive support, are unique. Thus z=z',c=c'. QED.

No complete pair face is assumed. This is the common-denominator
case of the lead's partial-row question. It includes rows from
different degrees. It does not assert injectivity for all partial
rows without the cross-cover condition.

**Binomial-moment corollary (proved).** Let I(z) be the set of
present successor directions, i_z=|I(z)| and j_z=|supp(z) intersect
I(z)|. Averaging RECTANGLE over every h-subset J of k directions,

```
m binom(k,h) >=
 sum_{z:i_z>=h}[(h+1)binom(i_z,h)-j_z binom(i_z-1,h-1)].  (ROW-MOMENT)
```

Each row occurs binom(i_z,h) times, and each of its relevant support
directions occurs binom(i_z-1,h-1) times. This proves the formula.
For fixed density i_z/k<1 and bounded h, its leading contribution
from pair rows is only O(k^2); it does not provide the missing
O(k^3) middle-regime estimate. Maximizing over J can be stronger
than this average, but no uniform improvement is claimed.

Here is the more general exact partial-row constraint. Make a graph
on reduced signed labels (z,c). Join (z,c) and (z',c') whenever
z+e_{c'} and z'+e_c are both present. An actual residue fiber is an
independent set. Thus any proper-coloring lower bound for this graph
is a lower bound for m. Present cells can be included as c=0 vertices;
all such vertices form a clique. This statement uses neither a
complete face nor a torsion assumption. The passage from this graph
to a uniform chromatic bound sufficient for MaxCL remains open.

**Full-face B_H packing (proved).** Suppose all cells of degree <=H-1
on h directions are present, and F is a family of degree H-1 rows
whose every successor on those directions is present. Add these rows
to the full set of rows of degrees 0,...,H-2 in RECTANGLE. If the
whole height-H simplex is present, the result is

```
m>=B_H(h):=binom(h+H-1,H-1)+h binom(h+H-2,H-1).
```

For H=2 this is h^2+h+1; for H=3 it is the accepted H(h+1)
count. It follows by summing
(h+1)binom(h+j-1,j)-h binom(h+j-2,j-1)
over j=0,...,H-1. The h=1 case is the chain bound H+1 directly.
Missing top cells spoil only their immediate predecessor rows.
More precisely, starting from B_H, subtract for each absent y

```
sum_{c in supp(y)}(h+1-|supp(y-e_c)|).
```

Union bounding spoiled rows is valid even when it overcounts. If
l=|supp(y)| and n1 counts singleton exponents, this cost is
l(h+1-l)+n1. The height-three costs are h,2h-1,3(h-1), recovering
ROW-DEF. This proves the generalization with explicit constants.

## 10. Other statements that extend to every height

**CR_H (proved).** Sort the positive maximal weights |y|-1 as
w_1>=...>=w_b>0 and let n=|N|. Then

```
S>=(d+1)binom(n,2)-sum_{j=1}^b w_j(m-j).
```

This is rearrangement and distinctness. With a fixed core and spikes
its right side is linear in m, of slope binom(n,2)-sum w_j. No
general positivity of that slope is asserted here.

**FLAT-WINDOW-H (proved identity).** Keep the maximal pairs A2,
let Nbig be the non-maximal cells of degree >=2, and Abig the
maximal cells of degree >=3. With adeg_i=sum_A2 z_i, the exact
identity is

```
S = sum_i(d+1-adeg_i)rho_i +(d+1)sum_Nbig r
    -sum_{y in Abig}(|y|-1)r(y)
    -( |Nbig|+|Abig| )rho0 +m OW
    +m #{z in A2:K(z)=1}.
```

Apply the flat pair identity only to A2, and use
m=1+d+|A2|+|Nbig|+|Abig|. The negative maximal-pair carries
occupy W exactly as before. This proves the identity at arbitrary
height. It does not prove the higher-height HC expression nonnegative.

The particularly strong one-unit-per-cubic loss in WINDOW-LOSS uses
CUBIC-LIFT and degree three. The report does not silently apply it
to quartics. DIGITAL-STAR and RECTANGLE/B_H do apply to height four
and to every H.

## 11. Preserved failed claims and explicit witnesses

1. **Positive face-free packing slack.** Section 7 gives an infinite
   counterexample family, including CR-failing members at every
   r>=11. The assertion remains false after adding an error o(k^2).
   The small three-block example (1,1,3) is k=5,m=16. No claim of
   global minimality among all shapes is needed or made.

2. **Dropping the whole HC carry term even for one cubic.** The
   stronger proposed inequality OW+B>=0 is false. There is an
   infinite sharp family for WINDOW-LOSS with t=1. Take integers
   r>=2,u>=2r+1, rho=2u-r, m=2rho+1, and v*=u+r. At the chosen
   phase the core-unit residues are

   ```
   U={0,...,rho-1}\{r,v*},       rho0=rho.
   ```

   Give these units original labels P_v=(v-rho) mod m. Include the
   maximal pair (0,v) for every v in U, the maximal pair (1,r-1),
   the non-maximal loop (u,u), and the cubic (u,u,u). Add the one
   spike with rotated residue v*. Here 0 in a pair denotes the
   zero-residue UNIT, not the origin. The negative maximal-pair
   sums cover every integer 0,...,rho-1 except v*: for the missing
   unit r use 1+(r-1). The origin, units and non-maximal pair fill
   residues 0,...,rho. Hence this is an actual residue-complete
   tile with k=rho-2,s=1,q=rho,t=p=1. Its cubic carry is -1,
   its N2 pair carry is 0, and OW=1, so OW+B=-1 exactly.

   The smallest member of this constructed family is r=2,u=5:

   ```
   m=17, k=6, s=1, d=7, sigma=9, rho0=8,
   P=(9,10,12,13,14,15),
   Q={00,01,11,02,03,04,05,44}, T={444},
   spike label=16.
   ```

   Indices in Q are zero-based. This gives a checkable counterexample
   to OW+B>=0: Lplus=133 and S=HCprime=116. ONE-DEFICIT proves
   that m=17 is the smallest possible modulus for this failure.
   The statement attempted and
   retained as proved is WINDOW-LOSS, which is sharp on this family.

3. **Omitting spikes from the top-form objective.** An intermediate
   formula incorrectly used (d+1)binom(m,2)-(d+H)sum_T r for a
   spiked pure core. The maximal spikes contribute (d+1)r in that
   top form. The smallest height-three example is the chain
   {0,x,x^2,x^3}, label x=1, lifted from m0=4 to m=5 with one
   spike at label 4. It has d=2 and true minimum S=3, whereas
   the erroneous formula gives 10. No smaller modulus can contain
   a height-three core and a spike. The three binary stars at m0=8,
   lifted to m=9,
   have true minimum S=91, whereas the erroneous formula gives 124.
   This is the smallest three-block example with a spike. The proof
   of DIGITAL-LIFT uses the exact first-form identity and includes
   this case. No accepted prior result is changed.

## 12. Computations and reproducibility

All scripts, outputs, and seeds are in `src/scratch/gw/p6/c/`.
They use integer arithmetic for every identity and final tile check.
None of the random or MILP searches substitutes for a uniform proof.

* `stress.py`: HCprime identity at all phases of F3 and HYBRID_UNPAID;
  balanced digital stars r=1,...,60 by an independent phase recurrence.
  F3 min HCprime=min S=78 at sigma=0. HYBRID_UNPAID min HCprime=
  min S=473 at sigma=30. The first negative digital CR value is
  r=11, -154440, while the exact all-phase minimum S is 5595480.
* `checks.py`, seed 2026101941, 1400 random proposals, named stress
  cases, five members of the sharp one-cubic-loss family, and larger
  one-cubic examples at k=36,40,48. 1384 actual height-three tiles,
  175625 phase checks. WINDOW-ID/LOSS, WINDOW-MIN, DEFECT-FLAT and
  UPPER-ARC: zero failures. 1666 CONE phases, minimum carry slack 0;
  60494 one-cubic phases, minimum slack in OW+B+1 equal to 0;
  1202 one-pair-zero phases; 38799 qualifying ONE-COVERED phases;
  38718 strong-covered and 59990 PARTIAL-COVER phases; five sharp
  deficits with the complete ONE-DEFICIT classification checked;
  14510 CONE-DEFECT phases;
  992 ONE-LARGE-DEFECT phases. 243 UPPER-PAY qualifications.
  Literal RECTANGLE labels: 10524 sets. ROW-MOMENT was independently
  checked against the sum over every J in 2856 (tile,h) cases.
* `digital.py`, seed 2026101951: 577 digital/spike tiles, 83524 phase
  checks, at heights 2,...,7. All ordered triples r_j=1,...,5 with
  spike counts 0,1,2,7; further heights and the r=11 stress case.
  It checks PREFIX, DENSITY, exact lifting identities, and every
  slack. The shifted polynomial for negative CR was reconstructed
  exactly, and the family identity was checked at r=1,...,400.
  The final audit also checks the minimal m=5 failed top-form
  example and the m=12 minimal zero-spike witness explicitly.
* `matching6.c`: exhaustive sorted unit sets and perfect matchings
  for the only k=6 uncovered analytic budget case. 177100 sets,
  2656500 matching cases, zero injective pair bases. Thus no cubic
  or phase test is needed there.
  `matching6_independent.py` fixes the missing matching, assigns
  coordinates incrementally, and prunes on every newly available
  pair. It reduces only by the matching automorphisms, rather than
  looping over unit sets. Depth counts are 1,24,240,1852,2928,222,0
  at depths 0,...,6. It independently finds no pair base.
* `milp_hc.py`, seed 2026101933: fixed labels, modulus, phase and
  dimension; optimize the pair/cubic shape with downward closure,
  residue injection and exact cell count. 174 solver calls: 66
  optimal, 90 infeasible, 18 time-limited with incumbents. All 84
  returned tiles were checked at every phase with exact integers:
  4350 phases, no MaxCL or HCprime failure. Some optima are flat;
  the file does not count them as new height-three evidence. A
  time-limited incumbent is not a proof of optimality. HiGHS was
  restricted to one thread, as were BLAS/OpenMP. This was an
  adversarial search, not an enumeration of all unit labelings.
* `degree_check.py`, seed 2026101961: 450 proposals, 404 qualifying
  actual tiles, t=2,...,10, 58203 phase checks of CUBIC-DEGREE.
  Every lower bound Lplus>=c+w(Q_k+k)>=mt and HCprime>=Lplus-mt
  is checked exactly. Minimum HCprime is 266; no failure.

Example commands, run from `~/wilf/p6c` through gcloud ssh:

```
nice -n 10 ~/mathenv/bin/python stress.py > stress.log
nice -n 10 ~/mathenv/bin/python checks.py 1400 > checks.log
nice -n 10 ~/mathenv/bin/python digital.py > digital.log
nice -n 10 cc -O3 -o matching6 matching6.c
nice -n 10 ./matching6 > matching6.log
nice -n 10 ~/mathenv/bin/python milp_hc.py 180 > milp_hc.log
nice -n 10 ~/mathenv/bin/python degree_check.py > degree_check.log
nice -n 10 ~/mathenv/bin/python matching6_independent.py > matching6_independent.log
nice -n 10 ~/mathenv/bin/python audit.py > audit.log
```

## 13. Exact remaining gap and next lemma

The original goal, all k>=K0 for an explicit universal K0, is not
proved here. The geometric reduction cannot be replaced by an
unconditional positive spike-slack bound: DIGITAL-STAR has s=0,
unbounded k, and negative CR. That lane is discontinued in its
face-free form. Its useful replacement is a residue-moment payment,
as the prefix proof and WINDOW-ID show.

The remaining general family is still k>=5,d>=6, with CR,
FLAT-CR and the accepted dense/few-cubic criteria unpaid. Add these
new necessary conditions to a hypothetical counterexample:

* DEFECT-FLAT<0 and Lambda<mt;
* CUBIC-DEGREE does not apply: either t>k/2 or some delta_i<t
  (for t>=2);
* at its minimizing phase, UPPER-PAY does not apply and the
  CONE-PHASE condition does not hold;
* it is outside DIGITAL-STAR and its spike lifts;
* in WINDOW-ID, beta>Orest+Pplus+gain+Lplus/m is necessary even
  for HCprime<0. A MaxCL failure needs the stronger excess after
  adding the positive maximal-pair carries in (HC).

For t=1 there is a more structured frontier. The missing-pair graph
has both missing edges and at least one isolated vertex (complete
quadratic row), because the full-pair and covered-missing-graph
cases are proved. Its minimizing zero cell is a unit outside the
cubic; in fact any negative phase has core-unit residues 0 and 1
outside the cubic, rho0>=8, 2rho0<m, and all N2 residues >=2.
At k>=12 there are at least two complete rows, by
ONE-PARTIAL-COVER, and its general PARTIAL-COVER inequality fails.
At k>=15 it has s<=3. It fails DEFECT-FLAT; at k>=36 it
also has e^2<k^3. If g counts complete rows then
g^2+g<=k+q+4. These conditions are uniform, not a finite certificate
in unbounded k.

A precise next local lemma is **ONE-RELAY**: in that one-cubic
frontier, at a zero unit outside the cubic, if OW+B=-1, prove
Lplus>=m (or the weaker Lplus+m P_A^+>=m needed for S).
The zero-unit quadratic row and the complete rows provide the
shifted pair residues that are not used by the present proofs.
Proving ONE-RELAY would close all one-cubic tiles; it would not by
itself close multiple cubics. The corresponding general task is to
charge the beta bad cubics in WINDOW-ID to Orest, Pplus, gain and
the residue-weighted Lplus, with injectivity preventing repeated
use of a relay. CONE supplies one exact, arbitrary-size instance
of this charging.

Formalization needs only finite sums, integer floors/remainders,
injections of the explicitly listed cells, and rearrangement for
the new carry and row lemmas. DIGITAL-STAR additionally uses the
finite digit coupling and the already Lean-checked column-top
lemma. No new literature theorem, unproved ambient packing input,
or assumption about P4 was used.
