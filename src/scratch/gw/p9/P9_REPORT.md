# P9: pair growth and a change of modulus for Problem 1.8

Date: 2026-10-19. Status: **PROVED partial results; Problem 1.8 remains OPEN.**

All computation was performed on fejer in `~/wilf/p9/p18/`, with nice single-core
processes and at most four concurrent jobs. The parent directory `~/wilf/p9/`
contained older P5 work and was preserved. Earlier reports were not changed.

## 1. Results and scope

Write

\[
 S=\langle m,m+b:b\in A^*\rangle,\quad B=\{0\}\cup A^*,\quad
 e=|B|=k+1,\quad \beta=\max B<m,
\]

and assume `gcd(m,B)=1`. Set

\[
 g=\gcd(A^*),\qquad a=\beta/g,\qquad
 s_2=|2B\cap[0,m)|,\quad s_j^*=|jB|.
\]

Sumsets in this report are **integer** sumsets unless a cyclic group is specified.
The generators displayed above are minimal, so the embedding dimension is exactly
`e`. Let `c=qm-rho`, `0<=rho<m`, `ell=|S cap [0,c)|`, and `W=e ell-c`.

The following are the main **PROVED** conclusions.

1. **PAIR-SPAN12.** If `12a <= e s_2`, then Wilf holds. In fact, when `q>=4`
   and `k>=2`,

   \[
                         W\ge kq+\rho.                 \tag{PS12}
   \]

2. **SUMSET-MODULUS.** For any integer `j>=2`, put `T_j=e(s_j^*-1)`. If

   \[
    m>(2j-1)\beta,\qquad
    T_j\{m(m-1)-ja(m+\beta)\}\ge 2ja(m+\beta)^2,         \tag{SM-Q}
   \]

   then Wilf holds. A conductor-free sufficient condition is

   \[
    T_j>2ja,\qquad
    m\ge \left\lceil
       \frac{2j\beta(T_j+3a)}{T_j-2ja}\right\rceil.       \tag{SM-L}
   \]

   Thus sufficiently fast integer-sumset growth gives an explicit threshold
   **linear in the offset span**. No assertion about a Macaulay ratio of the
   original bands is used.

3. **Explicit carried Sidon class.** For every odd prime `p>=17`, define

   \[
    B_p=\{2pi+(i^2\bmod p):0\le i<p\},\qquad
    \beta_p=2p(p-1)+1.
   \]

   Every semigroup

   \[
    S_{m,p}=\langle m,m+b:b\in B_p\setminus\{0\}\rangle
   \]

   satisfies Wilf for every `m>=31 beta_p`. For `p>=47`, the stronger range
   `m>2 beta_p` follows from PS12. These statements are uniform in `p` and `m`.
   Their proof is in §7, including the primality and gcd hypotheses.

4. The subfamily `m=100 beta_p+1`, `p>=17`, has carries and is outside **every
   parameter criterion listed in the task**. This is proved, rather than inferred
   from a sample: `100<=q<=161`, NO-WRAP fails, and even the prime-strength
   LK+YZ numerical bound fails. These multiplicities are also below
   `beta_p^2`, the previously known general shifted-family threshold.

The third and fourth points should not be read as a claim that no other
known, data-dependent Wilf test can recognize these semigroups. In particular,
Yang--Zhang's higher-layer `(Q,t)` tests recognize all the explicit Sidon examples
computed here. The new uniform assertions use only integer sumsets of `B`, their
span, and `m`; they do not require computing the conductor or Kunz layers.
No priority claim is made for every possible consequence of the published
multi-layer formulas. The general statements PS12 and SM-Q/SM-L, with proofs,
are the deliverable.

The depth-four problem in its full generality is **not** settled. At depth four,
the simplest second-layer sufficient conditions are already consequences of
Yang--Zhang. I do not count those restatements as a new depth-four theorem.

## 2. External inputs and what was checked

Problem 1.8 and its scope were checked directly in Delgado--Kumar--Marion,
[arXiv 2501.04417v3](https://arxiv.org/pdf/2501.04417v3).

The only external addition theorem used in the new proofs is the following
precise finite-set form of **Kneser's theorem**. If `X,Y` are finite nonempty
subsets of an abelian group and `K=Stab(X+Y)`, then

\[
 |X+Y|\ge |X+K|+|Y+K|-|K|.                            \tag{K}
\]

The statement and proof were checked in Matt DeVos,
[A short proof of Kneser's addition theorem for abelian groups, Theorem 1](https://www.sfu.ca/~mdevos/papers/kneser.pdf).
All applications below are in a finite cyclic group. `X` is a nonempty last-gap
set, `Y=-C` is nonempty, and `X-C` avoids zero. Thus its stabilizer is proper.
Generation and the condition `0 in C` are checked in each application; they
are not inferred from cardinalities.

The exact multiplicity-band count used in §4 is Yang--Zhang Prop. 5.2,
[Wilf's Conjecture from the First Kunz Layer](https://www.preprints.org/manuscript/202604.0551),
also already re-derived and verified in the project's LK+YZ theorem. It is
re-derived here. Their Theorems 5.3, 5.6 and 5.8 were read to avoid counting a
direct second-layer specialization as a new result.

The comparison with shifted semigroups uses O'Neill--Pelayo,
[Apéry sets of shifted numerical monoids, Corollary 4.6](https://arxiv.org/pdf/1708.09527):
for `n>r_k^2`, `n>r_k`, and `gcd(n,gcd(r_1,...,r_k))=1`, their shifted monoid
satisfies Wilf. These hypotheses are automatic for the particular `B_p` once
the gcd computation in §7 is made, except that our example multiplicities
are below their square threshold. Their theorem is not an input to PS12
or SUMSET-MODULUS.

No Freiman, Lev, Macaulay, or Nathanson theorem is used.
For `q<=3` the already-established Eliahou theorem is used only to include
that known range in the wording of PS12. All new quantitative proofs concern
`q>=4` or prove Wilf directly from SM-Q.

## 3. A conductor lower bound, including the offset gcd

**Lemma SPAN-CONDUCTOR (PROVED).** In P18,

\[
 c\ge m\left\lceil\frac{m-1}{a}\right\rceil
                +(g-1)(m-1).                          \tag{C1}
\]

Consequently

\[
 c\ge m(m-1)/a,\qquad m\le qa+1,                    \tag{C2}
\]

and if `rho>0`, then

\[
                         m\le(q-1)a+1.                 \tag{C3}
\]

Proof. `g<m` and `gcd(g,m)=1`. Take the Apéry element in residue `m-g`.
A factorization of an Apéry element uses no copy of `m`. Its offset sum has
the form `g u`. Its residue gives `u=-1 mod m`; hence `u>=m-1`.
If its factorization length is `l`, then

\[
 l\beta\ge g(m-1),\qquad l\ge\lceil(m-1)/a\rceil.
\]

The Apéry element is therefore at least
`m ceil((m-1)/a)+g(m-1)`. Subtract `m-1` to obtain C1.
C2 follows from `c<=qm`; if `rho>0`, C1 and `c<qm` force
`ceil((m-1)/a)<=q-1`, proving C3. QED.

This is why the normalized span `a=beta/g`, rather than just `beta`, can
be used in both theorems. Setting `g=1` is always a valid weakening.

## 4. Transport of gaps and the first new theorem

### 4.1 Arbitrary-modulus transport

Let `n in S` be positive; it need not be the multiplicity. Define

\[
 R_H^{(n)}=\{0\le r<n:Hn+r\in S\},\quad
 G_H^{(n)}=\mathbb Z/n\setminus R_H^{(n)}.
\]

These populations are monotone in `H`, and every `R_H` contains zero.

**Lemma TRANSPORT (PROVED).** If `C subset R_{j-1}^{(n)}`, then

\[
                   G_{H+j}^{(n)}-C\subset G_H^{(n)}.     \tag{TR}
\]

Proof. If `r in G_{H+j}`, `c in C`, and `r-c mod n in R_H`, add the two
semigroup elements `Hn+(r-c mod n)` and `(j-1)n+c`. The result is either
`(H+j-1)n+r` or `(H+j)n+r`. Adding a copy of `n` in the first case contradicts
the choice of `r` in both cases. QED.

**Lemma GENERATING-GAIN (PROVED).** Suppose additionally `0 in C`,
`|C|=s>=2`, and `C` generates `Z/n`. Whenever `G_{H+j}` is nonempty,

\[
 |R_{H+j}^{(n)}|-|R_H^{(n)}|\ge \lceil s/2\rceil.      \tag{GG}
\]

If `n` is prime the gain can be replaced by `s-1`.

Proof. Apply K to `X=G_{H+j}`, `Y=-C`. Since `X-C subset G_H` and
`0 notin G_H`, the stabilizer `K` is proper. If it is trivial, K gives gain
`s-1`, which is at least `ceil(s/2)`. Otherwise `C` meets `r>=2` cosets of
`K`: containment in one coset, together with `0 in C`, would put `C` in a
proper subgroup. If `|K|=h`, K gives gain at least
`(r-1)h >= rh/2 >= s/2`. Integrality gives GG. The prime case has only a
trivial proper stabilizer. QED.

This proves exactly the Kneser hypotheses needed below. In particular, no
gcd assumption is silently dropped when a different modulus is used.

### 4.2 Pair blocks in the multiplicity bands

In P18,

\[
 R_1^{(m)}=B,\qquad R_2^{(m)}=2B\cap[0,m).            \tag{R2}
\]

For the second equality, an element below `3m` uses at most two generators;
pad a one-generator factorization with the zero offset. Three positive
generators cannot occur below `3m`.

Take `C=R_2`, `s=s_2`. It contains `B`, so it generates `Z/m`. TR and GG give

\[
 \Theta_{H+3}\ge\Theta_H+\lceil s/2\rceil
                      \quad(H+3\le q-1).               \tag{P3}
\]

Starting at `Theta_2=s-1` and using monotonicity,

\[
 \Theta_t\ge s-1+\lceil s/2\rceil
                          \left\lfloor\frac{t-2}{3}\right\rfloor
                              \quad(2\le t\le q-1).    \tag{P4}
\]

This is the new amplified growth input. The original LK bound starts with
`B`; P4 starts with all distinct low pair sums, and its gain can be quadratic
in `k`.

For completeness, let `x_i` be the Kunz coordinate in residue `i`. Its left
elements contribute `q-x_i` when `i<m-rho`, and `q-1-x_i` otherwise, with
negative counts replaced by zero. Summing the indicators `x_i<=t` proves

\[
 \ell=q+\sum_{t=1}^{q-2}\Theta_t+\Theta_{q-1,\rho},
 \qquad \Theta_{q-1,\rho}=\Theta_{q-1}-\rho.             \tag{BC}
\]

The last equality holds because all `rho` residues in `[m-rho,m)` already
belong to band `q-1`. In particular `Theta_{q-1,rho}>=0`.

**Lemma PAIR-QUADRATIC (PROVED).** If `q>=4` and `k>=2`, then

\[
 \begin{array}{ll}
 \ell\ge q+s\,q(q-1)/12,&\rho>0,\\[2mm]
 \ell\ge q+s\,q^2/12,&\rho=0.
 \end{array}                                           \tag{PQ}
\]

Here is a symbolic verification for every parameter, not a finite fit.
Put

\[
 F_3(n)=\sum_{i=0}^{n-1}\lfloor i/3\rfloor,\qquad
 A(n)=n+F_3(n)/2.
\]

Using `ceil(s/2)>=s/2`, BC and P4 give

\[
 \ell\ge k+3+s A(q-3)\quad(\rho>0),\qquad
 \ell\ge k+2+s A(q-2)\quad(\rho=0).                    \tag{PQ0}
\]

For `n=3u+b`, `b=0,1,2`,

\[
 F_3(n)=3u(u-1)/2+ub.
\]

In the first branch,

\[
 A(q-3)-q(q-1)/12=
 \begin{cases}u-1/2&b=0,\\u&b=1,\\u+1/3&b=2.\end{cases}
\]

The first case has `u>=1`. The differences between PQ0 and the desired PQ
bound are respectively

\[
 k+(s-3)u-s/2,\quad k-1+(s-3)u,\quad
 k-2+s/3+(s-3)u.
\]

They are nonnegative for `k>=2`, `s>=k+1>=3` (in the first case minimize at
`u=1`, then use `k+s/2-3>=1/2`).

In the second branch,

\[
 A(q-2)-q^2/12=
 \begin{cases}5u/4-1/3&b=0,\\5u/4+1/4&b=1,\\5u/4+2/3&b=2.\end{cases}
\]

For `b=0,1`, `u>=1`; for `b=2`, `u>=0`. Each expression is positive, so the
minimum of `k-n+s(A-target)` is obtained at `k=2,s=3`. Its three values are
`1+3u/4`, `7/4+3u/4`, and `2+3u/4`, respectively. This proves PQ. QED.

**Theorem PAIR-SPAN12 (PROVED).** If `12a<=e s_2`, then Wilf holds. For
`q>=4,k>=2`, PS12 holds.

Proof. If `rho>0`, combine PQ with C3:

\[
 \begin{split}
 W&\ge eq+e s_2q(q-1)/12-qm+\rho\\
  &\ge eq+a q(q-1)-q\{(q-1)a+1\}+\rho=kq+\rho.
 \end{split}
\]

If `rho=0`, use C2 and the second PQ inequality to obtain `W>=kq`.
The already-known cases `q<=3` and `e<=2` complete the assertion as worded.
QED.

## 5. Short arcs remove the periodic loss

**Lemma SHORT-ARC (PROVED).** Let `C subset Z/n`, `0 in C`, and let `C`
generate `Z/n`. Suppose a translate of `C` has integer representatives in an
interval of width strictly less than `n/2`. If `X` is nonempty and `X-C` is
proper, then

\[
                         |X-C|\ge|X|+|C|-1.             \tag{SA}
\]

Proof. Put `K=Stab(X-C)` and `h=|K|`. Every coset of `K` has equally spaced
representatives, at distance `n/h`. An interval of width `<n/2` contains at
most `ceil(h/2)` of them. If `C` meets `r` cosets, then
`|C|<=r ceil(h/2)` and `r>=2`, because `K` is proper and `C` generates.
The elementary inequality

\[
 (r-1)h\ge r\lceil h/2\rceil-1
\]

holds for every `r>=2,h>=1`: for even `h=2u` the difference of the two sides
is `(r-2)u+1`; for odd `h=2u+1` it is `(r-2)u`.
Kneser now gives

\[
 |X-C|\ge|X|+|C+K|-|K|
        =|X|+(r-1)h\ge|X|+|C|-1.
\]

This also includes the trivial stabilizer `h=1`. QED.

The width hypothesis is used here. Mere generation does not imply SA; see §9.

## 6. The largest generator as modulus: all integer sumsets

Put

\[
 N=m+\beta\in S,\qquad D=\lceil c/N\rceil,
 \qquad T_j=e(|jB|-1),\quad j\ge2.
\]

We use bands of length `N` only in this section. The original depth remains
`q=ceil(c/m)`; it is not identified with `D`.

**Lemma MAXGEN-BLOCK (PROVED).** Suppose `m>(2j-1)beta`. Let `C_j` be the
cyclic set of sums of exactly `j` displayed generators modulo `N`. Then

\[
 |C_j|=s_j^*=|jB|,\qquad C_j\subset R_{j-1}^{(N)},       \tag{MB1}
\]

`C_j` contains zero and generates `Z/N`, and lies in a cyclic arc of width
`j beta<N/2`. Moreover `|R_0^{(N)}|=e` and

\[
 |R_H^{(N)}|\ge s_j^*+(s_j^*-1)
             \left\lfloor\frac{H-j+1}{j}\right\rfloor
                  \quad(j-1\le H\le D-1).              \tag{MB2}
\]

Proof. Sums of `j` generators have the form `jm+tau`, `tau in jB`, and lie in
`[jm,jN]`. Our hypothesis gives `jm>(j-1)N` and `j beta<N/2`. Distinct integer
`tau` are distinct modulo `N`. All sums except `jN` lie in band `j-1`; its
zero residue is represented by `(j-1)N`. Thus MB1 holds.

Taking `j-1` copies of `N` and one copy of any generator shows that `C_j`
contains every generator residue modulo `N`. Those residues generate because
the gcd of all generators is one. Taking `j` copies of `N` gives zero.
The sums are in an arc of width `j beta`, as asserted.

Every positive element below `N` is a single displayed generator, since
`N<2m`. Hence `R_0` consists of zero and the `e-1` generators below `N`.
TR with `n=N`, followed by SA, gives a gain of `s_j^*-1` every `j` bands
while the terminal band has a gap. Chain from `j-1` and use monotonicity to
obtain MB2. QED.

**Lemma INTEGRATED-BLOCK (PROVED).** Under the same hypothesis, put
`n=D-j` and let `b` be the remainder of `n` modulo `j`. Then `n>=0` and

\[
 \ell\ge e+n+(s_j^*-1)
       \left\{\frac{D(D-j)}{2j}+\frac{b(j-b)}{2j}\right\}.
                                                               \tag{IB}
\]

Proof. C1 gives `D>=j` (indeed `D>=2j-1`). Count the complete `N`-bands
`0` and `j-1,...,D-2`, discarding only nonnegative populations in any skipped
bands and in the partial last band. There are `n=D-j` bands in the second
list. MB2 gives

\[
 \ell\ge e+n s_j^*+(s_j^*-1)\sum_{i=0}^{n-1}\lfloor i/j\rfloor.
\]

For `n=ju+b`,

\[
 \sum_{i=0}^{n-1}\lfloor i/j\rfloor=ju(u-1)/2+ub,
\]

so the exact identity

\[
 n+\sum_{i=0}^{n-1}\lfloor i/j\rfloor
       =\frac{n(n+j)+b(j-b)}{2j}
\]

proves IB. QED.

For `j=2` the stronger integer version is particularly simple:

\[
 \ell\ge e+D-2+(|2B|-1)
                      \left\lfloor\frac{(D-1)^2}{4}\right\rfloor.
                                                               \tag{IB2}
\]

**Theorem SUMSET-MODULUS (PROVED).** The conditions SM-Q, or the sufficient
conditions SM-L, imply Wilf. In the notation above the quantitative conclusion
under SM-Q is

\[
                           W\ge e(e+D-j).               \tag{SM-W}
\]

Proof of SM-Q. By C2,

\[
 D-j\ge\frac{m(m-1)-jaN}{aN}.
\]

SM-Q therefore implies `T_j(D-j)>=2jN`. Discard the nonnegative parity
term in IB and use `c<=DN`:

\[
 W\ge e(e+D-j)+\frac{T_jD(D-j)}{2j}-DN
       \ge e(e+D-j).
\]

Proof of SM-L. Set `A=T_j/(2ja)>1`, `x=m/beta`. The threshold in SM-L is

\[
                   x\ge \frac{2jA+3}{A-1}>2j.           \tag{X}
\]

In particular `m>(2j-1)beta`. After division by `2ja beta^2`, the second
condition of SM-Q becomes

\[
 A\{x^2-x/\beta-(ja/\beta)(x+1)\}\ge(x+1)^2.
\]

Since `beta>=1` and `a<=beta`, it suffices that

\[
 (A-1)x^2-\{(j+1)A+2\}x-(jA+1)\ge0.                \tag{XQ}
\]

By X the left side is at least
`{(j-1)A+1}x-(jA+1)`. Since `x>2`, this is greater than
`(j-2)A+1>0`. This proves SM-Q and the theorem. QED.

Thus the leading threshold of this proved block method is
`e(|jB|-1)>2ja`. For pairs it is `e(|2B|-1)>4a`, with a completely explicit
finite threshold, rather than an unspecified sufficiently-large-m assertion.
The constant `2j` describes this lower envelope; it is not claimed to be
optimal for Wilf. If `T_j<2ja`, its quadratic coefficient in SM-Q is negative,
so this particular comparison cannot close arbitrarily large `m`.

Useful pair-only corollaries, all **PROVED**, are

| Hypothesis on `T_2/a` | Sufficient multiplicity |
|---|---:|
| `>=8` | `m>=9 beta` |
| `>=6` | `m>=14 beta` |
| `>=5` | `m>=24 beta` |
| `>=128/27` | `m>=31 beta` |

To verify them use XQ with `j=2`. At the first three endpoints the respective
polynomials `(A-1)x^2-(3A+2)x-(2A+1)` have values `4`, `3`, and `5/2`, and
positive derivatives thereafter. For the last row, with `x=31+z`, the
polynomial is `(5z^2+160z+64)/27`. Increasing `A` increases XQ for these
`x`, so endpoint verification proves every entry.

In the terminology of the task, this includes the following **PROVED
fast-doubling subclass**, with no Sidon assumption: if

\[
 |2B|\ge\lambda k^2,\qquad
 (k+1)(\lambda k^2-1)\ge8a,\qquad m\ge9\beta,
\]

then Wilf holds. Indeed these hypotheses give `T_2>=8a`, so the first row
applies. The exact SM-Q criterion and SM-L usually give a wider range than
this convenient three-inequality specialization.

## 7. A uniform Sidon family, with all hypotheses verified

Let `p` be an odd prime and

\[
 b_i=2pi+r_i,\quad r_i=i^2\bmod p\in[0,p-1],
                   \quad 0\le i<p.
\]

The sequence is strictly increasing and `b_0=0`,
`b_{p-1}=beta=2p(p-1)+1`. Also

\[
 b_1=2p+1,\quad b_2=4p+4,\quad
                    \gcd(b_1,b_2)=1.                  \tag{ET-GCD}
\]

Consequently `gcd(B_p)=1` and every `m>beta` gives a numerical P18 semigroup.

**Lemma ET-SIDON (PROVED).** All unordered pair sums from `B_p`, with
repetitions allowed, are distinct as integers. Hence

\[
                s=|2B_p|=p(p+1)/2,\qquad e=p.          \tag{ET2}
\]

Proof. An equality `b_i+b_j=b_u+b_v` gives
`2p(i+j-u-v)=r_u+r_v-r_i-r_j`. The right side has absolute value `<2p`, so
`i+j=u+v`. Modulo `p`, the square sums are also equal, so `ij=uv mod p`.
Since two is invertible in the field, the two unordered pairs are the roots
of the same quadratic. The indices lie in `[0,p)`, so the unordered pairs
are identical. QED.

**Theorem ET-31 (PROVED).** For every prime `p>=17`, Wilf holds for every
`S_{m,p}` with `m>=31 beta`.

Proof. Here `a=beta`, `T_2=p(s-1)`. A direct identity is

\[
 27T_2-128\beta
   =\tfrac12\{27p^3-485p^2+458p-256\}.
\]

Writing `p=17+u`, the polynomial in braces is

\[
                    27u^3+892u^2+7377u+16>0.           \tag{ET17}
\]

Thus `T_2/beta>=128/27`; apply the last row of the preceding table. QED.

**Theorem ET-2 (PROVED).** For every prime `p>=47`, Wilf holds for every
`S_{m,p}` with `m>2 beta`.

Proof. All pair sums lie below `m`, so `s_2=s`. Also

\[
 2\{ps-12\beta\}=p^3-47p^2+48p-24.
\]

At `p=47+u` this is

\[
                         u^3+94u^2+2257u+2232>0.        \tag{ET47}
\]

Apply PS12. QED.

For reference, the same table gives `m>=24 beta` for primes `p>=19`,
`m>=14 beta` for `p>=23`, and `m>=9 beta` for `p>=31`. To check these
without a numerical monotonicity assertion, for `r=5,6,8` use

\[
 2(T_2-r\beta)=p^3-(4r-1)p^2+(4r-2)p-2r.
\]

At `p=4r-1+u`, every coefficient is positive. This proves the three
additional uniform ranges.

## 8. An infinite carried subfamily outside the listed criteria

Fix any prime `p>=17` and set `m=100 beta+1`. ET-31 proves Wilf.
The following statements are all **PROVED**, not computational observations.

First, NO-WRAP fails: `min(B_p\setminus{0})=2p+1>1`. An unwrapped
factorization in residue one would have offset sum exactly one, which is
impossible. This argument applies to any complete factorization tile.

Second,

\[
                              100\le q\le161.            \tag{ET-DEPTH}
\]

Here are details of the upper bound, to avoid assuming an unproved additive
basis property of the Sidon set. Let `C=2B_p mod beta`. In `[0,2 beta]`,
nonzero residue classes modulo `beta` have at most two representatives, and
zero has at most three. Therefore

\[
 |C|\ge(s-1)/2\ge\beta/8,
\]

where the last inequality follows from `4(s-1)-beta=4p-5>0`.
`C` contains `B_p mod beta`, so ET-GCD makes it generating. Applying Kneser's
generating gain repeatedly to `tC` shows `15C=Z/beta`: if not, its size
would be at least `|C|+14 ceil(|C|/2)>=8|C|>=beta`, a contradiction.

Every residue modulo `beta` consequently has a representative in `30B_p`,
of value at most `30 beta`. Given any residue modulo `m`, choose its
representative `tau` in the integer interval `[30 beta,30 beta+m)`.
Choose `u in 30B_p` with `u=tau mod beta`. Then `tau=u+j beta`, `j>=0`,
and `j<=130`, because `tau<=130 beta`. Thus `tau` is an offset sum of
at most `160` generators. The corresponding semigroup value is at most
`160m+130 beta`. Hence

\[
 c\le159m+130\beta+1<161m.
\]

This proves the upper bound in ET-DEPTH. C1 gives `c>=100m`, proving the lower
bound.

Third, even the strongest prime-version LK+YZ bound does not prove Wilf
on this family. Let `L_old` denote the right side of LK+YZ at the actual
`q,rho`. Since `delta<=k` and `k_rho<=k`,

\[
 L_{\rm old}\le q+k(q^2+1)/4.                           \tag{OLD-UP}
\]

For `p>=17`, `100<=q<=161`,

\[
 pL_{\rm old}
 \le pq+p(p-1)(q^2+1)/4
 <41p(p-1)(q-1).
\]

For a symbolic verification of the strict inequality, replace `1/(p-1)`
by `1/16`. After multiplication by 16 the required polynomial is
`4q^2-655q+660<0`; its endpoint values on `[100,161]` are `-24840` and
`-1111`. Convexity proves the whole interval. But

\[
 c>(q-1)m>200p(p-1)(q-1),
\]

so `p L_old<c` by a wide explicit margin.

The other listed exclusions are immediate but recorded explicitly:
`q>=100>4`, `e=p>4`, `m>3p`, `m>18`, and
`2m>p(p+1)=e(k+2)`. The DKM square-root criterion also fails, since
`m>200p(p-1)>(p-1)^2`. Finally `m=100 beta+1<beta^2` since `beta>=545`;
these are below O'Neill--Pelayo's square threshold.

Thus the task's known parameter regimes do not subsume this infinite family.
This is not an assertion of nonrecognition by every possible data-dependent
criterion. The actual Yang--Zhang `(Q,t)` criterion does recognize every
computed member; that overlap is recorded, not suppressed.

## 9. Failed candidates, smallest checked witnesses, and open strengthenings

**COUNTEREXAMPLE 1: removing the periodic correction.** The candidate
`Theta_{H+3}>=Theta_H+s_2-1` for arbitrary composite multiplicity is false.
The smallest witness found by the exhaustive search of **all** P18 offset
sets for `m<=18` is

\[
 m=14,\quad A^*=\{3,7,10\},\quad S=\langle14,17,21,24\rangle.
\]

Its exact data are

```
c=96, q=7, rho=2, ell=47, W=92,
Theta=[0,3,5,6,8,9,11,13],
C=2B cap [0,14)={0,3,6,7,10,13}, s_2=6.
```

At `H=2` the gain is `Theta_5-Theta_2=4<5=s_2-1`.
`C` is a union of three cosets of `{0,7}`. This is exactly the periodic
obstruction accounted for by GG. No Wilf inequality fails.

**COUNTEREXAMPLE 2: an overstrong quadratic payment.** The candidate
`ell>=q+s_2 q(q-1)/4` is false. With at least two non-m generators, the
smallest witness in the same exhaustive domain is

```
S=<6,8,9>, A*={2,3}, s_2=5,
c=20, q=4, rho=4, ell=10, W=10,
Theta=[0,2,4,4,5].
```

The candidate right side is 19. If one non-m generator is allowed, the
earlier smaller witness is `S=<4,7>`, `c=18,q=5,rho=2,ell=9,s_2=2`; its
candidate right side is 15. Neither is a counterexample to PQ, whose
denominator is 12.

**COUNTEREXAMPLE 3: short-arc expansion without the short arc.** In `Z/6`,
take `C={0,1,3,4}` and `X={0,3}`. Then `C` generates the group and
`X-C={0,2,3,5}`, so `|X-C|-|X|=2<3=|C|-1`. This is an explicit witness, not a
claimed global minimum. The width hypothesis of SA cannot be discarded in
the abstract addition lemma.

**OPEN strengthening, not used.** The actual largest-generator bands passed
the stronger pair gain `|R_{H+2}^{(N)}|-|R_H^{(N)}|>=|2B|-1` even in the
tested cases with `m<=3 beta`, where the short-arc proof does not apply.
This has not been proved. It is not being substituted for GG or SA.
For stress testing, the structured family
`m=2L-1, B={0,1,L,L+1}, N=3L` has periodic `2B mod N`; it also passed for
`3<=L<=50`. Periodicity alone therefore does not decide this proposed
semigroup-specific strengthening.

The two false Macaulay ratios listed in the task were not reintroduced.
Nor was generation of a cyclic group inferred without a gcd check.

## 10. Computational checks (FINITE CHECK)

These checks support, but are not substitutes for, the proofs above.
Scripts are in this directory. Remote location: `~/wilf/p9/p18/`.

`audit.py --maxm 18 --trials 15000 --seed 910` checked:

| Check | Number |
|---|---:|
| Actual P18 semigroups | 275,518 |
| Exhaustive actual semigroups, all nonempty offset subsets, `2<=m<=18` | 261,565 |
| Independent membership-DP cross-checks of conductor and `ell` | 261,565 |
| Actual semigroups with `q>=4` | 53,097 |
| P3 step inequalities | 190,964 |
| PQ inequalities (`k>=2`) | 53,000 |
| PS12 applicable | 5,098 |
| PS12 applicable at depth four | 2,749 |
| PS12 applicable with `min A*>1,e>4,3e<m,e(k+2)<2m` and LK+YZ failing | 766 |
| Independent Apéry calculations at the largest-generator modulus | 30,190 |
| Largest-modulus step inequalities | 96,554 |
| Higher-sumset short-arc step inequalities, `j=2,3,4` | 125,919 |
| Higher integrated-block inequalities | 4,756 |
| SM-Q applicable, over the tested `j` | 3,556 |
| SM-L applicable, over the tested `j` | 2,442 |

The count 766 does not exclude the project's depth-four theorem at `k<=18`,
nor does it exclude the higher-layer Yang--Zhang tests. The infinite-family
noncoverage assertion in §8 is separate and proved analytically.

There were **zero failures of every asserted inequality**. The preserved
false candidates above failed as expected. The largest-modulus cross-check
is exhaustive for `m<=14` and was made on every valid random instance.
The random portion uses arbitrary subsets, short spans, APs with an outlier,
projected two-dimensional grids, and upper clusters. Both prime and composite
moduli occur. The normalized-gcd conductor bound C1 is checked as well.

`hill.py --seed 911 --chains 100 --steps 120` made 10,538 additional exact
mutation checks, including 10,495 with depth at least four. Mutations minimize
`W/c`, with simulated-annealing escape, starting from random sets, short spans,
APs with an outlier and projected grids. All intermediate valid candidates
are checked, including rejected mutations. It checked 51,087 P3 inequalities,
28,305 largest-modulus inequalities and 5,966 higher-block step inequalities.
There were zero failures of the proved statements. Its smallest observed
`W/c` with `min A*>1,q>=4` was the exact instance

```
m=673, A*={69,73,210,435}, c=9429, q=15, rho=666,
ell=3425, W=7696.
```

It is not claimed to be covered by the new theorem; the adversary tests
both covered and uncovered inputs.

`algebra.py` checked the exact block-sum identity on 99,099 `(j,n)` pairs,
`2<=j<=100,0<=n<=1000`, and the PQ endpoint comparison on 199,994 cases,
`4<=q<=100000`, both rho branches. The positivity certificates ET17, ET47
and the `x=31` shift were checked against their original polynomials.
It also exhaustively checked SA on 223 generating short-arc sets in groups
of orders `3..14`, against 1,629,593 nonempty `X`; 758,850 had proper sumset.
Zero failures.

`families.py` checked 42 carried Sidon semigroups, at primes
`17,19,23,31,47,67,97` and multiplicities
`floor(r beta)+1`, `r in {1,6/5,3/2,2,31,100}`. The largest multiplicity was
1,862,501. All had depth at least five. It checked 974 P3 steps, 937
largest-modulus steps, and 2,673 higher-block steps, with zero failures.
The 14 instances at ratios 31 and 100 satisfy the pair SM-Q criterion;
13 further applications of PS12 (including overlapping ones) are recorded.
Every one of these 42 actual semigroups satisfies the published higher-layer
Yang--Zhang `(Q,t)` sufficient criterion. The exact-output manifest is in
`CHECKS.json`. Earlier `probe.py` and
`sidon_examples.py` outputs are preserved as preliminary checks, rather than
merged into the final census counts.

Typical commands (all computation is remote):

```sh
gcloud compute scp --zone us-east1-b src/scratch/gw/p9/*.py fejer:~/wilf/p9/p18/
gcloud compute ssh fejer --zone us-east1-b --command \
 'cd ~/wilf/p9/p18 && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/mathenv/bin/python audit.py --maxm 18 --trials 15000 --seed 910'
```

## 11. What remains open, and the next precise lemma

**PROVED:** PS12, SUMSET-MODULUS for every `j>=2`, its explicit linear-span
threshold, and the uniform carried Sidon classes of §§7--8.

**OPEN:** Problem 1.8, including the full depth-four case. No counterexample
to Wilf was found. No claim is made that every P18 offset set satisfies
one of the new growth hypotheses.

The exact family left by the new sufficient conditions is described without
an asymptotic qualifier as follows. First remove the previously covered
regimes in the task. On what remains, a possible counterexample must satisfy

\[
 12a>e|2B\cap[0,m)|,                                   \tag{P9-R1}
\]

and, for every integer `j>=2` with `m>(2j-1)beta`,

\[
 e(|jB|-1)\{m(m-1)-ja(m+\beta)\}
                       <2ja(m+\beta)^2.                 \tag{P9-R2}
\]

Only finitely many `j` occur for a specified `(m,B)`: namely
`2<=j<(m/beta+1)/2`. R1--R2 are necessary conditions for a counterexample,
not a finite reduction of the entire open problem. In particular they leave
the sparse shallow families with `m` comparable to a high power of `k`.

The next precise lemma is the semigroup-specific strengthening noted in §9:

> For P18, with `N=m+beta`, does
> `|R_{H+2}^{(N)}|-|R_H^{(N)}| >= |2B|-1`
> hold whenever `G_{H+2}^{(N)}` is nonempty, even if `m<=3 beta`?

An abstract Kneser or boundary-only proof cannot establish this: the abstract
short-arc extension is false, and periodic pair sets occur. A proof would
have to use the actual earlier semigroup bands and their forbidden residues.
It would remove the present semicircle restriction, but would still need a
separate shallow-band argument to settle depth four. This is the stated
remaining gap, not an assumed final step.

## 12. Research review and decision

The original depth-four route through a single low pair layer did not produce
a new theorem beyond the published multi-layer count, and was not promoted
as such. The amplified gap route supplied PS12, with a uniform analytic
constant and an explicit composite obstruction to its stronger variant.
Changing to the largest generator then supplied a different mechanism:
the generator sums lie in a short cyclic arc, allowing the full Kneser gain
and yielding SUMSET-MODULUS for every integer sumset order. This is the
substantive infinite-class result of the turn.

The remaining obstruction is geometric, but differs from the paused
height-three tile problem: when `m` is comparable to `beta`, the sumsets
used here do not lie in a semicircle. The observed stronger largest-modulus
gain needs actual semigroup restrictions to repair periodic fibers. I have
not spent additional runs increasing a bounded multiplicity census, nor
treated the absence of a numerical failure as that missing proof.

Decision: deliver the proved sumset criteria and explicit linear-span
subclasses, retain the stated strengthening as OPEN, and leave the full
Problem 1.8 and its depth-four frontier unresolved.
