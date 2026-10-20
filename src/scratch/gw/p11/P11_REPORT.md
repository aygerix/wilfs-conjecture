# P11: uniform payments for the primary regime

2026-10-19. **Partial result. The full assertion for $3m<c\le4m$ remains open.**

The new results are analytic inequalities on infinite classes, not an extension of the per-
\(\alpha\) enumeration. They use ordinary integer packing, with its entire quadratic error.
No ambient $P(C)$ conjecture is assumed. Earlier reports are unchanged; no commits were made.
The remote working directory is `~/wilf/p11/primary/`; the pre-existing contents of
`~/wilf/p11/` were preserved.

## 1. Results and their precise scope

Use a residue-complete primary factorization down-set \(D\), with

\[
 |D|=m,\qquad M=4m+h-1,\quad 1\le h\le m,\qquad n_i=m+t_i>m.
\]

All directions are active, \(v(x)=\sum_i x_i n_i\), \(M=\max_Dv\), and
\(x\mapsto v(x)\bmod m\) is bijective. Put

\[
 d=\#\{i\},\quad \ell=\sum_D\left\lfloor\frac{M-v(x)}m\right\rfloor,
 \quad g=\sum_D\left\lfloor\frac{v(x)}m\right\rfloor,\quad W=d\ell-g.
\]

For an Apéry tile, \(g\) is the genus, \(\ell=c-g\), and this is
\(W=(d+1)\ell-c\), the usual Wilf number.

The A directions have \(1\le t_i<h\), and their number is \(a\). There are
\(\alpha\) low A directions, those with \(2t_i<h\). The B directions have
\(h\le t_i<h+m\), and their number is \(b\). C and E have the ranges in GW-21.
For a semigroup, \(h=c-3m\), so these are exactly the \(a,\alpha\) in the task.

Here are the additional, explicitly computable parameters. All pairs include loops.

* \(n_0\) is the number of present low--low pairs, and
  \(Q=\binom{\alpha+1}{2}\), \(r_{LL}=Q-n_0\).
* \(l\) is the number of low--high A pairs in I2. Let \(L=\min_A t_i\), and let
  \(j_L\) count the high A directions whose pair with this lowest direction is absent.
* Choose a vertex cover \(C\) of **all** absent A pairs; a missing loop forces its vertex
  into the cover. Put \(\kappa=|C|\). A cover obtained by deleting one endpoint of each
  missing pair always exists.
* Set \(\theta=\lceil3h/2\rceil\), and let \(R\) count the high A directions with
  \(t_i<\theta-2L\). Form the ordinary integer set
  \[
  X=\{t_i:i\notin C,\ i\text{ is low or }t_i<\theta-2L\}.
  \]
  Let \(g_{11}\) be the number of integers that have at least eleven representations
  as a sum of **three distinct members** of \(X\). An upper bound obtained by using
  all A offsets outside \(C\) instead of \(X\) is also permissible.
* Define the localized cost
  \[
  d_0=\max\left\{l+j_L,\ b,
               \left\lceil\frac{\kappa+r_{LL}+b}{2}\right\rceil\right\}. \tag{1}
  \]

The scalar \(d_0\) is not the dimension of the tile. Write \(G\) for any nonnegative integer
upper bound on \(g_{11}\).

**Theorem A [PROVED, analytic].** Suppose \(\alpha\ge6\), \(n_0\ge Q/2\), and

\[
                a\ge13(\alpha+d_0+G+22).                 \tag{2}
\]

Then \(W\ge0\), for arbitrary C/E directions and all the other face counts.
In particular, the previously quadratic cutoff in \(\alpha\) becomes linear on
this stated geometric class. There is no restriction on the number of absent legal A
cubics, or on the sizes of the \(G\) exceptional squarefree sum fibres.

**Corollary A1 [PROVED, using LARGE-A′].** The condition \(n_0\ge Q/2\) can be omitted if
(2) is supplemented by \(a\ge20r_{LL}\). Indeed, if \(n_0<Q/2\), then

\[
 a\ge20r_{LL}>10Q,
\]

and the already proved LARGE-A′ applies. A simpler, weaker sufficient condition is

\[
 a\ge20(\alpha+r_A+l+b+G+22),                          \tag{3}
\]

where \(r_A\) is the total number of absent A pairs. To check (3), use
\(\kappa,r_{LL},j_L\le r_A\) in (1), hence \(d_0\le r_A+l+b\).

**Theorem B [PROVED, analytic].** With the same definition (1), suppose

\[
 \alpha\ge1280(d_0+G+1),\qquad a\ge3\alpha.             \tag{4}
\]

Then \(W\ge0\). The half-low-face condition is automatic here, since
\(r_{LL}\le2d_0\le\alpha/640<Q/2\).

**Theorem C [PROVED, analytic].** Suppose \(r_A=l=b=0\). Then

\[
                    \alpha\ge1140+9G                  \tag{5}
\]

implies \(W\ge0\), with no restriction on \(a\) or on C/E directions.
Here no cover is needed. This improves P5g's BFREE-LIGHT cutoff \(1910\) to \(1140\),
and improves its asymptotic necessary heavy-fibre count from \(\alpha/32\) to
approximately \(\alpha/9\). It is an improvement and extension of the existing
packing mechanism, not a first proof of that B-free light-fibre branch.

These are statements about actual tiles. They are not assertions that every remaining
semigroup has small \(d_0\) or small \(g_{11}\). For numerical semigroups the hypotheses
are imposed on some Apéry factorization down-set, such as a lex or grlex tile, and
the conclusion is Wilf's conjecture for that semigroup.

## 2. Elementary face budgets; no new Macaulay input

Write \(q=q_2+q_3\) for all present A pairs, \(u=u_3+u_4\) for all present A cubics,
and \(k_4\) for A quartics. Put

\[
 D_3=(a+2)q-3u,\qquad
 LC=(a+1)(q_2+u_3)-4k_4.
\]

The weighted shadows give

\[
3u\le(a+2)q,\quad 3u_3\le(a+2)q_2,\quad
4k_4\le(a+3)u_3.
\]

Thus \(LC\ge(a-1)q_2/3\ge0\). Re-expanding the GW-21 pure-A expression gives

\[
 W_A=3a(a+1)+(a-3)q-4u+LC
 \ge3a(a+1)-\frac{a+17}{3}q.                            \tag{6}
\]

Since GW-21's transfer has \(W\ge W_A\), any counterexample with \(a\ge4\) satisfies

\[
 q>\frac{9a(a+1)}{a+17}>2a.                            \tag{7}
\]

Let \(\varepsilon\) count absent **legal** A cubics: a formal cubic is legal if all
its pair divisors are present. If \(u_{\rm legal}\) is the number of all legal cubics,
weighted pair-to-cubic incidence gives \(3u_{\rm legal}\le(a+2)q\). Consequently

\[
                  D_3\ge3\varepsilon.                 \tag{8}
\]

This is the actual legal defect; it need not be replaced by the larger Macaulay defect.
After deleting \(C\), all pairs on the remaining directions are present. Therefore
every formal cubic on \(X\) is legal, and its ordinary triple excess satisfies

\[
 \operatorname{ex}(X)=\binom{|X|+2}{3}-|3X|
                \le\varepsilon.                       \tag{9}
\]

Indeed each sum fibre contains at most one present cubic, by residue injectivity;
its excess is at most its number of absent cubics. Sum over the fibres.

## 3. Re-derived two-arc necessary bounds

This section spells out the consequences of the proved I-LOW payment used below.
They apply to every hypothetical \(W<0\), with \(\alpha\ge3\), \(a\ge3\alpha\).
The special full-pair branch in section 7 only needs its weaker A-LOW lower bound.
No layer-sign conjecture or RC assertion is used.

Put \(A=\alpha\), \(Q=\binom{A+1}{2}\), \(U=\binom{A+2}{3}\),
\(\delta=h-2L>0\). Let \(c_0\) count present pure-low cubics, \(u_0\) their I3
subfamily, \(u_1\) the I3 two-low--one-high cubics, and \(k_0,k_1\) the quartics
with respectively zero and one high factor. There are no quartics with two high
factors. Thus \(u_3=u_0+u_1\), \(k_4=k_0+k_1\), and \(q_2=n_0+l\).

Let \(l_i\) be the I2 degree of low direction \(i\) into the high directions and

\[
 S_l=\sum_i l_i(a+2-l_i)\ge0.
\]

Let \(\beta\) count present low--low pairs with \(\tau<\lceil h/2\rceil\), and
\(\beta_H\) those with \(\tau<h-L\). Define

\[
\begin{split}
 B_f&=a-1+q_2+u_3-2A-2\beta,\\
 B_H&=a-1+q_2+u_3-2(A+E+l+\beta_H),\\
 C_H&=A+n_0+c_0+l+E+\binom{E+2}{3}
                    +(n_0+AE)(a-A),                  \tag{10}
\end{split}
\]

where \(E=\min(a-A,l+j_L)\). This is an upper bound for the number of high units
below \(h-L\): their pairs with the lowest unit either are present I2 pairs or are
one of the \(j_L\) missing pairs. This localizes the former bound \(E\le l+r_A\).

For clarity about the outside signs, let \(C_\#,E_\#\) denote the C/E unit counts,
and put, as in LOW-ID,

\[
\begin{split}
\mathcal G={}&C_\#(C_\#+E_\#+1)+E_\#(3a+2b-1)
              +(C_\#+E_\#)(q_3+s_3+t_3),\\
\Omega_f={}&\mathcal G+(C_\#+E_\#)(2q_2+u_3)-2AC_\#,\\
\Omega_H={}&\mathcal G+(C_\#+E_\#)(2q_2+u_3)-2(A+E)C_\#.
\end{split}
\]

Both Omega quantities are nonnegative in a counterexample: (7), \(A+E\le a\),
and \(\mathcal G\ge(C_\#+E_\#)q_3\) prove every required sign. This use of (7)
is essential; the unrestricted sign assertion without \(W_A<0\) is not assumed.

Here is the intruder calculation, retaining the terms that will be spent. For the
fixed arc \(Y\) of GW-26, its pure-A intruders satisfy

\[
 J_A\le A+\beta+c_0+k_0+n_0R-u_1+\sum_i\binom{l_i+1}{2}.
\]

The types counted are low units, cold pairs, pure-low cubics, pure-low quartics,
two-low--one-high cubics on the \(R\) directions, and the one-low--two-high cubics
whose two low--high divisors are I2. The I3 mixed cubics counted by \(u_1\) miss
the fixed arc. The outside intruders number at most \(b(A+\beta)+AC_\#\).

For \(H_0=h-L\), the pure-A intruders are at most \(C_H+k_4\). The terms in
\(C_H\) count low units, low pairs, pure-low cubics, low--high I2 pairs, exceptional
high units, all-high exceptional cubics, and the two mixed cubic types. The outside
bound is \(b(A+E+l+\beta_H)+C_\#(A+E)\).

The cold shadow is

\[
 (A+2)\beta\le3(u_0+U-c_0),\quad
 4k_0\le(A+3)u_0,\quad 3k_1\le(A+2)u_1.               \tag{11}
\]

For the first inequality, every cold pair's low extensions have \(\tau<h\);
they are present I3 pure-low cubics or absent pure-low cubics. Count weighted
incidences. In the fixed I-LOW payment, substitution of the displayed intruder
count gives coefficients \((4a-5A-11)/4\) on \(u_0\), \(2\) on \(U-c_0\), and a
nonnegative coefficient on \(u_1\). Since

\[
 (A+2)(4a-5A-11)\ge24,
\]

(11) pays the \(2\beta\) term in full. This condition holds for \(A\ge3,a\ge3A\).
The fixed payment is an integer and must be at most \(-1\) in a counterexample.
It therefore gives

\[
 2n_0R\ge D_3+a-2A-2U+(a+3)n_0+S_l+bB_f+\Omega_f.    \tag{12}
\]

The \(H_0\) payment, with the same integer strictness, gives

\[
 \delta\le2C_H-(a-1)-(a+3)q_2-(a+1)u_3+5k_4
                         -D_3-bB_H-\Omega_H-1.        \tag{13}
\]

These are exactly substitutions in I-LOW, using respectively \(2J\) and
\(-\delta+2J_{H_0}\) for its arc loss; they do not assert a sign for either
individual layer or any individual generator. Equations (10)--(13) also re-derive
the relevant R-LOW/DELTA-UP specialization without a Macaulay substitution.

## 4. Coarsening with a localized repair cost

Suppose \(n_0\ge Q/2\), \(A\ge6\), \(a\ge3A\). Let \(d_0\) be (1), abbreviated
to \(D_0\) below. Thus

\[
 E,l,b\le D_0,\qquad \kappa+r_{LL}+b\le2D_0.
\]

By \(\beta\le n_0\le Q\), \(\beta_H\le n_0\), and \(q_2=n_0+l\),

\[
 B_f\ge-Q,\qquad B_H\ge-Q-2E-l.                       \tag{14}
\]

Discard \(S_l,\Omega_f\) in (12), use (8), and separate its positive numerator
from \(-2U-bQ\). Since \(n_0\le Q\), \(a-2A>0\), this proves

\[
 A+R-\kappa\ge\nu-\kappa-r_{LL}-b\ge\nu-2D_0,
 \quad \nu=\frac a2+\frac{2A}{3}+\frac56+\frac{3\varepsilon}{2Q}. \tag{15}
\]

The two estimates for the loss are explicitly

\[
\frac{U}{n_0}-\frac UQ=\frac{Ur_{LL}}{Qn_0}\le r_{LL},
\qquad \frac{bQ}{2n_0}\le b.
\]

The first follows from \(n_0\ge Q/2\) and \(2(A+2)/(3Q)\le1\) for \(A\ge2\).
In particular \(n=|X|\ge\nu-2D_0\).

In (13) the pure and mixed quartic shadows make
\((a+1)u_3-5k_4\ge0\), since \(a\ge3A\). Put

\[
 B_0=(a-2A-1)Q+2U+2A-a+1.
\]

Expanding \(C_H\), replacing \(n_0\le Q,c_0\le U\), discarding
\(-(a+1)l\), and using (14) gives

\[
 \delta\le B_0-3\varepsilon-1+T,
\quad T=2E[1+A(a-A)]+2\binom{E+2}{3}+b(Q+2E+l).       \tag{16}
\]

The following bound is valid even when \(D_0>A\):

\[
 T\le T_0:=3D_0Aa+\frac{D_0^3}{3}+4D_0^2+\frac{8D_0}{3}. \tag{17}
\]

Indeed \(E,b,l\le D_0\) first give

\[
T\le2D_0Aa+D_0Q+\frac{D_0^3}{3}+4D_0^2+\frac{8D_0}{3},
\]

and \(Q\le Aa\). When \(D_0\le A\), \(a\ge3A\), there is also the stronger

\[
                         T\le3D_0Aa.                  \tag{18}
\]

For (18), the leftover bracket is at most
\(2+Q+3A+(A+1)(A+2)/3\le Aa\). At \(a=3A\) the difference is

\[
 \frac{13(A-3)^2+51(A-3)+20}{6}>0 \quad(A\ge3).
\]

The terms cubic in \(D_0\) in (17) must be retained for Theorem A. Dropping
them without \(D_0\le A\) would be an unjustified stronger bound.
In fact that stronger **algebraic** claim is false. In the count family
\(A=6\), \(a=13(A+D_0+22)\), \(E=D_0\), \(b=l=0\), the first failure as
\(D_0\) increases is \(D_0=258\):

\[
 a=3718,\qquad T=17284108>3D_0Aa=17266392.
\]

`poly.py` checks every \(1\le D_0<258\) in this specified family. These are
count data refuting a proposed coarsening, not a residue-complete instance or
a Wilf counterexample. The proof above keeps the missing cubic error.

## 5. The integer packing input, with its error re-derived

Let \(Z\) be a pair-distinct \(n\)-set of integers in an interval of \(s\) integers.
Let \(G\) bound the number of squarefree triple-sum fibres of size at least eleven,
and let \(\varepsilon_Z\) be its ordinary unordered triple excess. Then

\[
3s-2\ge H(n)-45\varepsilon_Z-(63+G/2)n^2+3n,
\quad H(n)=\frac{n^3-n^2+2n}{2}.                       \tag{19}
\]

This is the strict SF-M bound of P5g, and the following is its proof. A nonzero
ordinary difference has at most one ordered representation in a pair-distinct set:
two representations would give two equal, formally distinct pairs. If \(r_z\) is
the number of repeated cubics at sum \(z\), choosing their two repeated centres gives

\[
 \sum_z\binom{r_z}{2}\le\binom n2.
\]

Use proper signed labels \(x+y-z\) with \(x<y\), \(z\notin\{x,y\}\). A collision
corresponds to two distinct equal-sum cubics. A fixed pair of cubics contributes at
most the product of their support sizes: choose the two negative entries, which
then determine the two labels. If \(f_z\) counts squarefree cubics, the proper-label
collision-pair count is therefore at most

\[
 9\sum_z\binom{f_z}{2}+6\sum_zf_zr_z+4\sum_z\binom{r_z}{2}.
\]

Discarding loop-positive signed labels costs \(n(n-1)\) formal labels. Proper
signed labels cannot equal a unit label, by pair injectivity. A proper-label fibre
of size \(v\) loses at most \(\binom v2\) values. For the fibres with \(f_z\le10\),

\[
 9\binom{f_z}{2}\le45(f_z-1)_+,\qquad
 6\sum_{f_z\le10}f_zr_z\le60n^2.
\]

In any single ordinary triple fibre all distinct cubic supports are disjoint:
a common member would cancel to an equality of two pairs. Its **whole** signed
collision potential is consequently at most \(n^2/2\). Charge this once for each
of the at most \(G\) heavy squarefree fibres. Counting repeated/repeated collisions
again is harmless. Combining the losses gives

\[
 H(n)-|N(Z)|\le45\varepsilon_Z+(63+G/2)n^2-3n.
\]

Finally all signed labels lie in an integer interval of length \(3s-2\), proving
(19). This is an integer argument. No cyclic version of DIFF2, nor a reduction of
an arbitrary cyclic set to an interval, is used.

For \(X\) in section 1, every offset lies in
\([L,\theta-2L)\), an interval of exactly \(s=\lceil3\delta/2\rceil\) integers.
Apply (19), (9), and

\[
2(3\lceil3\delta/2\rceil-2)\le9\delta-1.
\]

Together with (16)--(17) they imply the following **necessary** inequality for a
counterexample, where \(c_*=127+G\):

\[
 F(n):=n^3-c_*n^2+8n-9B_0-63\varepsilon+10-9T_0\le0. \tag{20}
\]

It is (20), rather than a conjectured zero-error \(P(C)\), that is spent below.

## 6. Proof of Theorem A: the linear threshold

Write \(D_0=d_0\), \(S_0=A+D_0+G+22\), \(C_*=c_*+6D_0\), and suppose
\(a\ge13S_0\). Then \(a\ge3A\), so sections 2--5 apply. The polynomial
\(n^3-c_*n^2+8n\) increases for \(n\ge\nu-2D_0\): this lower endpoint is at least
\(a/2-2S_0\ge9a/26>2c_*/3\), since \(c_*\le6S_0\).

Substitute \(n\ge\nu-2D_0\) in (20). Expansion, discarding the nonnegative
\((12D_0^2+4c_*D_0)\nu\) term, gives

\[
\begin{split}
F(n)\ge{}&h(\nu)+(12a+40A)Q-27D_0Aa\\
 &+32Q-18A+9a+1+8\nu-E_0,\\
h(z)={}&z^3-C_*z^2-42Qz,\\
E_0={}&11D_0^3+(4c_*+36)D_0^2+40D_0.                 \tag{21}
\end{split}
\]

The elimination of \(\varepsilon\) is exact: use
\(63\varepsilon=42Q(\nu-a/2-2A/3-5/6)\) and the definition of \(B_0\).
The constants \(36D_0^2+24D_0+3D_0^3\) in (21) are the retained cost from (17).

For \(z\ge a/2\), \(h\) is increasing. Indeed

\[
C_*\le6S_0\le6a/13,\quad 42Q\le21S_0^2\le21a^2/169,
\]

so \(h'(a/2)\ge111a^2/676>0\), and \(h'\) increases thereafter. Since
\(\nu\ge a/2\), discard the other nonnegative terms in (21) to obtain

\[
F(n)\ge\frac{a^3}{8}-\frac{C_*a^2}{4}-9aQ-27D_0Aa-E_0. \tag{22}
\]

Use the exact identity

\[
C_*=6S_0-6A-5G-5,
\]

and \(D_0\le S_0-A\), \(S_0\le a/13\). The part of (22) before \(-E_0\) is at
least

\[
\begin{split}
&\frac{a^3}{104}-\frac{15}{26}Aa^2+\frac{45}{2}A^2a
          -\frac92Aa+\frac54(G+1)a^2\\
={}&\frac{a^3}{169}+\frac{45}{2}a(A-a/78)^2
          -\frac92Aa+\frac54(G+1)a^2\\
\ge{}&\frac{a^3}{169}+\frac{47}{52}a^2.               \tag{23}
\end{split}
\]

For the error, \(c_*\le6(S_0-D_0)\), hence

\[
 E_0\le24S_0D_0^2-13D_0^3+36D_0^2+40D_0
       \le11S_0^3+36S_0^2+40S_0.                       \tag{24}
\]

The last cubic comparison has a nonnegative certificate:

\[
11S_0^3-24S_0D_0^2+13D_0^3
=(S_0-D_0)^2(11S_0+13D_0)+9S_0D_0(S_0-D_0).
\]

Equations (22)--(24) finally prove

\[
 F(n)\ge\frac{2a^3}{2197}+\frac{467a^2}{676}-\frac{40a}{13}>0,
\]

because \(a\ge13(6+22)>5\). This contradicts (20) and proves Theorem A.
All lower-order terms and their signs have been retained.

## 7. Two improvements in the middle ratio range

### 7.1. Proof of Theorem B

Assume (4). It implies \(D_0\le A\), \(r_{LL}\le2D_0<Q/2\), and \(a\ge3A\).
Use the stronger (18) instead of (17). Thus (21) has

\[
 E_0'=8D_0^3+4c_*D_0^2+16D_0
\]

instead of \(E_0\), with the other terms unchanged. Now

\[
 C_*\le127(D_0+G+1)<A/10,\quad
 42Q<(21+1/60)A^2,\quad E_0'\le A^3/512.
\]

For the last bound use \(D_0\le A/1280\), \(c_*\le A/10\), \(A\ge1280\);
each of its three terms is at most \(A^3/2048\).
The coefficient of \(a\) in \((12a+40A)Q-27D_0Aa\) is positive, so \(a\ge3A\) gives

\[
 (12a+40A)Q-27D_0Aa\ge(38-81/1280)A^3.
\]

Since \(81/1280+1/512<1/15\), (21) would require a nonpositive value of

\[
 P(z)=z^3-z^2/10-(21+1/60)z+38-1/15,\quad z=\nu/A\ge0.
\]

Here is a complete elementary certificate:

\[
 P(z)=(z-27/10)^2(z+53/10)+(47/150)z-2111/3000.
\]

For \(z\ge9/4\), the last two terms are at least \(1/750\). For
\(0\le z\le9/4\), the square term is at least
\((9/20)^2(53/10)\), and its difference from \(2111/3000\) is \(887/2400>0\).
This proves Theorem B.

### 7.2. Proof of Theorem C, including the A-LOW and LOW-H signs

Now \(r_A=l=b=0\), \(n_0=q_2=Q\), \(u_3=u_0\), \(k_4=k_0\), and
\(D_3=3\varepsilon\) exactly. Put \(F_a=\binom{a+1}{3}\). Directly,

\[
 W_A=-F_a+LC+4\varepsilon.
\]

At \(a=A,A+1\), the shadow yields
\(LC\ge(a+1)Q-2U\), and
\(-F_a+(a+1)Q-2U=0\) at both endpoints. Thus a counterexample has \(a\ge A+2\).
Then \(LC\ge(a+1)Q\), so \(W_A<0\) forces

\[
 a(a-1)>3A(A+1),\qquad a>5A/3+1.                      \tag{25}
\]

In particular the cold sign and the quartic-shadow sign used in (12)--(13) hold
for \(A\ge1140\).

The LOW+ payment from I-LOW, keeping its \(3\delta\) arc, and the full \(H_0\)
payment imply, on subtracting three times the upper bound for \(\delta\),

\[
0\ge4a-6A+(6A+6-2a)Q-6c_0
                   +4(a+1)u_0-18k_0+4D_3.
\]

Replace \(c_0\le U\), \(4k_0\le(A+3)u_0\). The remaining \(u_0\) coefficient
is \((8a-9A-19)/2>0\), by (25). The C/E remainder is nonnegative by (7).
Hence

\[
 4a-6A+2(2A+1-a)Q+12\varepsilon\le0.                  \tag{26}
\]

Since \(4a-6A>0\), this forces \(a\ge2A+2\), and

\[
 x:=a-2A-1-6\varepsilon/Q\ge(2a-3A)/Q>0.             \tag{27}
\]

Thus no small-defect theorem or finite certificate is needed to justify the
substitution below. Equations (12)--(13) give

\[
 n>\nu=a/2+2A/3+5/6+3\varepsilon/(2Q),\quad
 \delta\le B_0-3\varepsilon-1.                         \tag{28}
\]

Let \(y=\varepsilon/Q\), \(T=9y/(2A)\), \(V=x/(2A)\), \(w=T+V\). Both \(T,V\)
are nonnegative. Define

\[
\begin{split}
g(w)&=w^3+5w^2-14w/3+44/27,\\
j(w)&=3w^2-3w-2/3,\\
F_{45}&=\nu^3-\nu^2+2\nu-9B_0-63\varepsilon+10.
\end{split}
\]

The exact identity is

\[
\begin{split}
F_{45}={}&A^2[(A-4)g(w)+4g(w)+j(w)]
 +4(A^3+A^2)V\\
 &+A[16/9+(50/3)T+(68/3)V]+358/27,\\
\nu={}&A(w+5/3)+4/3.                                  \tag{29}
\end{split}
\]

The positive certificates needed are

\[
\begin{split}
g(w)&=w^3+\frac{44}{9}(w-17/33)^2
                   +\frac19(w+5/3)^2+\frac7{297},\\
4g(w)+j(w)&=4w(w-1/2)^2+27(w-34/81)^2+266/243.
\end{split}
\]

Put \(K=126+G\), \(Y=A(w+5/3)\). The integer packing bound (19) and (28) would
require

\[
 F_{45}-K\nu^2+6\nu\le0.
\]

Substitution of \(n>\nu\) is valid: its cubic polynomial increases for
\(n\ge\nu>5A/3\). But \(A\ge1140+9G=9K+6\), and (29) gives

\[
\begin{split}
F_{45}-K\nu^2+6\nu
&>\frac{A-4}{9}Y^2-K(Y+4/3)^2\\
&\ge\frac29Y^2-\frac{8K}{3}Y-\frac{16K}{9}>0.
\end{split}
\]

The last polynomial increases for \(Y\ge6K\), whereas \(Y\ge5A/3>15K\).
At \(Y=15K\) it is \(10K^2-16K/9>0\). This contradiction proves Theorem C.

### 7.3. A genuinely finite reduction on the light, B-free full-pair class

Take \(r_A=l=b=0\), \(g_{11}=0\). Here \(d_0=0\). Theorems A and C reduce any
counterexample in this particular class to

\[
6\le\alpha\le1139,\qquad
19\le a\le15092,\qquad a<13\alpha+286.                 \tag{30}
\]

Existing P47-B0 additionally closes \(a\le32\) and \(a\ge2Q+38\).
This is **not** a finite reduction of the whole primary regime: \(g_{11}\) and
the localized repair cost are unrestricted in the whole problem.

For completeness the negative-W part of (30) even has a crude finite multiplicity
bound. The transfer contains \((C_\#+E_\#)q\); here \(q=\binom{a+1}{2}\) and
\(-W_A\le F_a\), so \(C_\#+E_\#<(a-1)/3\). Since \(l=0\) forbids the mixed
quartics, cardinality gives

\[
m\le\binom{a+3}{3}+\binom{\alpha+3}{4}+(a^2-1)/3
 \le643714076491.                                     \tag{31}
\]

This large finite box has **not** been enumerated, and no claim is made that such
an enumeration would be practical. It makes the limited finite reduction precise.

## 8. The chain route: exact reduction, successful falsification, and what is open

The chain route was tested first, as requested. Let \(\lambda(w)=\lfloor(M-w)/m\rfloor\)
and let \(k_{w,n}\) be the number of forward \(n\)-steps from \(w\) in its Apéry
chain. Define

\[
 \operatorname{con}(w)=\sum_n(k_{w,n}n-m\lambda(w)),\quad
 \Delta=\sum_w\operatorname{con}(w).
\]

Residue completeness gives \(\sum_w((M-w)\bmod m)=C_2\), hence directly

\[
B_{\rm chain}=dC_2-\Delta,
\quad \Delta=\sum_n nP_n-dm\ell,
\quad \ell=\sum_w\lambda(w).
\]

An Apéry chain is consecutive: if two endpoints are Apéry elements and an
intermediate point minus \(m\) were in \(S\), adding the remaining generator
multiples would contradict the upper endpoint. Thus tile columns lie in these
chains; CH′ yields \(B\ge B_{\rm chain}\ge R\).

At depth four, the co-level-0 cells have zero contribution. Indeed \(w\ge c\)
implies \(w+n-m\ge c\), so \(w+n\) is not in Apéry. Co-level four consists only of
zero, since every other Apéry element is at least \(m+1\). Therefore

\[
\Delta=\operatorname{con}(0)+\mathrm{Bulk},\qquad
\mathrm{Bulk}=\sum_{\lambda=1,2,3}\operatorname{con}(w).
\]

W0 follows again from \(k_{0,n}n\le M=4m+h-1\):
\(\operatorname{con}(0)\le d(h-1)\). Hence

> **BULK0 [OPEN]:** \(\mathrm{Bulk}\le0\) for every depth-four semigroup, or just
> for those in the exact residual.

would close the sparse case, because \(3e<m\) gives
\(\Delta\le d(m-1)<2C_2/3<C_2\). The proof of BULK0 is not obtained here.
Neither its extensive zero-failure census nor its equivalence to an explicit
count budget is presented as a theorem.

### Preserved failed strengthenings

`scan.c` enumerates all semigroups through genus 33 and tests the following six
candidates. “Smallest” in this table means smallest genus in that exhaustive
domain; no tie-minimal multiplicity claim is made.

| Candidate | All depth-four failures | Sparse failures | Smallest witness |
|---|---:|---:|---|
| Bulk \(\le0\) | 0 | 0 | OPEN |
| Every \(n\ge2m\) has \(R_n\ge C_2\) | 20,538 | 0 | \(\langle3,11,13\rangle\), genus 7 |
| Every \(n\ge c-2m\) has \(R_n\ge C_2\) | 801,601 | 119 | same; sparse \(\langle13,15,18,19\rangle\), genus 26 |
| \(\sum_{w\ne0}\operatorname{con}(w)_+\le C_2-\operatorname{con}(0)\) | 0 | 0 | OPEN |
| Every nonprimitive nonzero \(w\) has \(\operatorname{con}(w)\le0\) | 650 | 69 | \(\langle8,10,13,15\rangle\), genus 15; sparse \(\langle11,12,15\rangle\), genus 25 |
| Co-level 1 + co-level 2 total \(\le0\) | 5 | 0 | \(\langle7,9,11\rangle\), genus 15 |

The last witness has layer totals \((0,3,0,-31,-14)\), ordered by co-level
0 through 4. Thus its positive middle sum is cancelled by layer 3.
`audit.json` contains the complete generators, Apéry tables, individual chain and
RC terms and all layer totals for every smallest-genus witness.

There is also an infinite failure of a direction-by-direction BULK0 proof.
Take \(m=4k+1\), \(S=\langle m,m+1,\ldots,m+k\rangle\), \(k\ge2\). Then

\[
w_r=\lceil r/k\rceil m+r\quad(1\le r\le4k),\quad
c=4m,\quad\ell=4+6k.
\]

In direction \(n=m+k\), the origin chain has five cells and the other \(k-1\)
chains have four. Thus \(P_n=6k+4\), \(k_{0,n}=4\), and

\[
\sum_{w\ne0}(k_{w,n}n-m\lambda(w))=6k^2>0.
\]

For \(k\ge3\) this is sparse: \(3e<m\). The whole-semigroup Bulk is nonpositive
on these examples; only the proposed separate-direction payment fails. This
family is NO-WRAP and is not claimed to be part of the exact residual.

### Co-Kunz formula audit [CORRECTION]

For \(s=(M-w)\bmod m\), let \(\lambda(s)=(M-w-s)/m\), and write \(n=m+b\).
The exact expression is

\[
 R_n-C_2=n\sum_{s=0}^{m-1}
       \left\lceil\frac{\lambda(s)b-s}{n}\right\rceil-b\ell. \tag{32}
\]

It follows by reducing \(M-w=m\lambda+s\) modulo \(n\), and summing.
The ceiling is nonnegative, but can exceed one. The expression with just
\(\#\{s:s<\lambda(s)b\}\) is a lower bound, not a general equality.
For \(\langle5,9,12\rangle\), \(n=9\), the actual term is \(-1\), while the
indicator expression is \(-10\). For \(\langle4,9,10\rangle\), \(n=9\), they are
\(-4\) and \(-13\). These are independently recomputed in `audit.py`.
No proof in sections 2--7 uses the indicator equality.

## 9. Computational checks and their limits

**FINITE CHECK.** `scan.c 33`: 63,754,402 total semigroups (all genera 0--33),
7,096,029 depth-four semigroups with \(e\ge3\), of which only 425 have \(3e<m\).
The candidate table above is its exact output. This genus range contains no
semigroups meeting the new large-
parameter theorems' hypotheses; its role is falsification of the chain candidates.

**FINITE CHECK.** `audit.py` independently uses Dijkstra from the generators,
recomputes every smallest-genus witness, and checks the explicit interval family
for \(2\le k\le50\). The family is proved for all \(k\) above; the checks are not
its proof.

**FINITE CHECK.** `kunz.c` mutates exact depth-four Kunz coordinates, checking all
affected Kunz inequalities. Generator minimality and chain/RC quantities are
recomputed. Its final witnesses are exact; the acceptance objective is floating
point and is used only for search. The initial version lost depth four before
reaching a valid sparse start, and produced **zero evaluated states**. Those
unsuccessful initializations are preserved and are not counted as evidence.
The corrected initialization uses shortest-path semigroups, conductor truncation,
and a depth-preserving descent fallback.

| run | valid starts | evaluated valid mutations | domain | Bulk failures | high-RC failures |
|---|---:|---:|---|---:|---:|
| seed 21, \(m=85\) | 8 | 42,198 | \(3e<m\) | 0 | 0 |
| seed 22, \(m=257\) | 1 | 0 | numeric residual plus YZ exclusion | 0 | 0 |
| seed 23, \(m=503\) | 8 | 18,587 | same | 0 | 0 |
| seed 31, \(m=320\) | 7 | 17,472 | same; objective targets high-RC | 0 | 0 |

“Evaluated mutations” need not be distinct semigroups. The \(m=257\) seed supplies
one exact starting example but no successful mutation census.
The final \(m=503\) example has \(c=1699,e=28,\alpha=9,a=20\),
\(\mathrm{Bulk}=-2473194\), \(C_2=126253\). No observed negative Wilf number or
failure of GW-24/26 was found.

**FINITE CHECK.** `instances.py 71 2500` rebuilds grlex Apéry down-sets independently
from shortest paths, and adds named examples, the interval family, and the saved
Kunz states. It checks 1,836 actual depth-four tiles, 968 sparse, 526 with
\(\alpha\ge6\), and 137 in the numeric residual. Of the 1,500 tiles with at least
one low A unit, it checks the legal-defect shadow, LC, the localized exception
bound, the \(H_0\) intruder count, the cover and joint-size bounds, and the
localized triple excess. It checks the cold payment in 505 applicable instances,
the coarse B/H coefficients and delta error in 277, and the SF-M joint bound in
1,480 nonempty joint sets. All pass. Only one has \(W_A<0\); these are not
claimed as a strong adversarial census of the negative-face frontier. None meets
the numerical hypotheses of Theorems A--C, so this check validates the ingredients,
not an observed population newly settled by those theorems.

A second run, `instances.py 72 0 60 targeted`, adds sixty conductor-truncated
Sidon-offset constructions at \(8000\le m\le40000\), with three to eight low
directions and highs in \([h-L,h)\). Including the named and saved-state controls,
it checks 163 tiles and has 54 negative pure-A faces. Its 95 applicable cold
payments and 156 nonempty joint packing tests all pass. The controls overlap the
first run, so the two tile totals are not added as distinct semigroups. The
truncated constructions usually have many E generators; this supplements the
negative-face ingredient checks rather than claiming a sparse-residual census.

**EXACT ALGEBRA CHECK.** `poly.py` implements a sparse polynomial ring over
`fractions.Fraction`, without sympy. It verifies (29), its two positive square
certificates, epsilon elimination, the two middle-range cubic certificates, the
linear-threshold square, the cubic error bound, and the final positive remainder
by coefficient equality: twelve identities in total. It also checks 336,128
scalar rows (\(0\le G\le100\), \(0\le r\le12\), \(0\le l,b\le7\), four choices
of \(a\)), 15,435 linear-threshold rows (\(6\le A\le40\), \(0\le D_0,G\le20\)),
and 10,201 middle-threshold rows (\(0\le D_0,G\le100\)), all over exact rationals.
The first grid also retains a weaker intermediate sufficient cutoff; it is not
the source of the optimized constants in the theorems. The output is in `results/poly.log`.
The all-parameter proof consists of the inequalities in sections 2--7; it is not
inferred from those grids.

**FINITE CHECK.** `packing.py` independently enumerates the ordinary signed
support, repeated-cubic collisions, and SF-M remainder on thirteen pair-distinct
sets. These include the P5g planted 11- and 16-triple heavy fibres (\(n=33,48\)),
the lead's \(n=9\) extremizer, and ten fresh Sidon sets of sizes
\(3,5,10,15,20,30,40,50,64,80\). All pass. The planted inputs are copied as data
from P5g and explicitly identified as such; their construction is not new work here.

Only project-proved lemmas are used: GW-21's transfer, the proved GW-26 I-LOW
payment, and (for Corollary A1 only) LARGE-A′. The new proof uses no external
Freiman, Kneser, Nathanson or Macaulay theorem with additional unchecked hypotheses.
The collision argument (19) has been re-proved above in its required integer scope.

## 10. Strategic review and exact remaining gap

The combined nonzero chain layers remain the shortest possible route to the whole
task: BULK0 would close it using W0. Separate-direction and separate-layer payments
are explicitly false, and more zero-failure random searches do not prove BULK0.
That is why the proof effort shifted to the two-arc packing budget rather than
continuing its census.

The geometric results close a new repaired-pair, B-perturbed infinite class and
strengthen the already known B-free light-fibre class. They do **not** establish
the unrestricted \(c\le4m\) frontier theorem. The original possible counterexample
still has

\[
 \alpha\ge6,\quad19\le a<10\binom{\alpha+1}{2},\quad
 3e<m,\quad m\ge211,
\]

and all the previously proved GW-26 necessary conditions. In addition it must
fail the new tests for every chosen absent-pair cover:

\[
\begin{split}
& n_0<Q/2\quad\text{or}\quad a<13(\alpha+d_0+g_{11}+22),\\
& a<3\alpha\quad\text{or}\quad\alpha<1280(d_0+g_{11}+1),\\
& r_A+l+b>0\quad\text{or}\quad\alpha<1140+9g_{11}.
\end{split}                                             \tag{33}
\]

If using an upper bound for \(g_{11}\), use that same bound in these tests.
No finite certificate covering all of (33) is claimed. Even the fully light,
B-free finite box (30)--(31) is not enumerated in this turn.

The next precise chain lemma is **BULK0 restricted to the original sparse residual**.
On the packing route, the missing statement is a primary-specific payment for the
heavy joint squarefree fibres, with the localized repair cost retained. The bound

\[
 g_{11}\le a/13-\alpha-d_0-22
\]

would suffice in the half-low-face, large-ratio branch; the difficult central strip
has \(a<13\alpha+O(d_0+g_{11})\), and needs the LOW-H information as well. No such
heavy-fibre bound is assumed here. The exact gap is geometric, rather than an
unperformed sweep over successive values of \(a\).
