# P10: embedding dimension five, by the support of an Apéry tile

Date: 2026-10-19. Status: **partial result; the full embedding-dimension-five problem remains open.**

All computations below were run on fejer, in `~/wilf/p10/e5/`, with `nice -n 10` and one core per process. The pre-existing contents of `~/wilf/p10/` were left alone. No commits were made. Earlier reports are unchanged.

## 1. New conclusions and their scope

Let $S=\langle m,n_1,n_2,n_3,n_4\rangle$, with the five generators minimal and $m<n_1<\cdots<n_4$. Let $D\subset\mathbb N^4$ be an Apéry factorization down-set: $|D|=m$ and $x\mapsto x\cdot n$ is a bijection from $D$ to $\operatorname{Ap}(S,m)$. Write $\operatorname{supp}(x)=\{a:x_a>0\}$. Minimality forces all four unit cells to belong to $D$.

**Theorem B4 [PROVED, analytic].** Suppose $(1,1,1,1)\notin D$, equivalently every cell of $D$ uses at most three distinct directions. If $m\ge22^3=10,648$, then $S$ satisfies Wilf. In fact $W=5\ell-c\ge3$.

**Theorem B2 [PROVED, with an exact finite certificate].** Suppose every cell of $D$ uses at most two distinct directions. If $m\ge60$, then $S$ satisfies Wilf, strictly: $W\ge1$. The proof is analytic for $m\ge144$, an exact count-profile certificate for $64\le m\le143$, and a stronger exact face-profile certificate for $60\le m\le63$. These are certificates over all down-sets with the stated support restriction; no lattice-realizability or residue-labeling filter is used.

Combining B2 with the lead's already verified $m\le39$ result proves the same tile class for $m\le39$ or $m\ge60$. The interval $40\le m\le59$ is **not** claimed here.

**Intrinsic corollaries [PROVED].**

1. If $m\ge10,648$ and $n_1+n_2+n_3+n_4\ge c+m$, then Wilf holds.
2. If $m\ge60$ and $n_1+n_2+n_3\ge c+m$, then Wilf holds.

Indeed $\max\operatorname{Ap}=c+m-1$. The first inequality excludes every factorization using all four directions; the second excludes every factorization using three distinct directions. Both statements concern distinct directions, not factorization length. They allow arbitrarily large tile height.

The intrinsic B4 range is separate from VOL-MINK, and even from the data-dependent VOL-CORNER criterion: putting $N=\sum n_i$ and $\Lambda=\max\operatorname{Ap}+N$, it has $\Lambda<2N$. Since VOL-CORNER's $g\le1/4$, that criterion would require $\Lambda\ge6(N+m-1)$, which is impossible here. No part of the lead's very-deep argument is used below.

## 2. The height criterion, re-derived

The combinatorial lemmas below apply to finite down-sets containing all four unit cells. In this section the Apéry bijection converts their height bounds into Wilf inequalities.

Let $A=\max D$, and define

\[
 h(x)=\max\{|y|-|x|:y\in D, y\ge x\},\qquad
 H_x=\sum_{a=1}^4h(\operatorname{top}_a x),\qquad H=\sum_D H_x.
\]

For $y\in A$, put $w_y=4+|y|$. If $w_0\ge\cdots\ge w_{t-1}$ is this multiset in decreasing order, set

\[
 R=\sum_{i=0}^{t-1}iw_i.
\]

For a semigroup tile, $M=\max\operatorname{Ap}=c+m-1$ and

\[
 mW+\frac32m(m-1)=\sum_{x\in D}\sum_{a=1}^4(M-v(\operatorname{top}_a x)). \tag{CH}
\]

For completeness, in a column of length $L$,

\[
 L v(\operatorname{top})-\sum_Cv=n_a\binom L2.
\]

Summing in direction $a$ gives $\sum_xv(\operatorname{top}_a x)=\sum_Dv+n_a\sum_Dx_a$; summing all directions gives $5\sum_Dv$. Also $\sum_Dv=mg+m(m-1)/2$, by counting the gaps in each residue class, and $W=4c-5g$. These give (CH).

A non-maximal top $z$ satisfies $M-v(z)\ge(m+1)h(z)$: take an upper cell attaining $h(z)$, and use $n_a\ge m+1$. A maximal cell $y$ is a top with multiplicity $4+|y|$. Its deficit $M-v(y)$ is a nonnegative integer, and the maximal-cell deficits are distinct. Rearrangement therefore gives

\[
 mW\ge(m+1)H+R-\frac32m(m-1). \tag{HC}
\]

In particular $H\ge3m/2\Rightarrow W\ge3$. All finite certificates below verify the right side of (HC) directly.

Two elementary properties of the rank term will be useful. For any nonnegative weights,

\[
 R(w)=\sum_{i<j}\min(w_i,w_j). \tag{R-MIN}
\]

Consequently $R$ is coordinatewise nondecreasing and concave as a function of the individually indexed weights. Both statements follow directly from the pairwise-minimum expression.

## 3. Missing directions pay small local height

Let $t_s=\#\{y\in A:|\operatorname{supp}y|=s\}$, and $N_s=\#\{x\in D:|\operatorname{supp}x|=s\}$. Thus $N_0=1$, $N_1\ge4$, and $t_1\le4$. The scripts use `n1`, `n2`, `n3` for these support counts, not for generator values.

**Lemma BH2 [PROVED].** If $N_4=0$, then

\[
 H\ge2m-\frac52t_1-\frac{10}{3}t_2-6t_3. \tag{BH2}
\]

**Proof.** Bound $\sum_x(2-H_x)_+$; negative contributions to $2m-H$ can be discarded. Maximal cells contribute $2(t_1+t_2+t_3)$.

Consider a non-maximal $x$ with support size $r\le2$. Among its $4-r$ missing directions, let $M_x$ be the number whose column top is maximal. Every other missing-direction top contributes at least one to $H_x$, so $M_x\ge4-r-H_x$. For $H_x<2$,

\[
 2-H_x\le\frac{2}{4-r}M_x.
\]

Each incidence counted by $M_x$ ends at a maximal cell of support $r+1$. For a fixed maximal cell and a fixed positive coordinate, its projection with that coordinate zero is unique. Thus these incidences number at most $(r+1)t_{r+1}$. Their costs are at most $t_1/2, 4t_2/3, 3t_3$, for $r=0,1,2$, respectively.

Finally let $x$ be non-maximal of support three with $H_x<2$. Its missing-direction column consists of $x$, since $N_4=0$. Hence $h(x)=H_x=1$. Each of its three present-direction tops must be maximal. Since $h(x)=1$, these tops are the three distinct upper covers $x+e_a$. Count the resulting incidences: each such $x$ gives three, while a support-three maximal cell has at most three support-three lower covers. There are at most $t_3$ such $x$, each of cost one. Adding the costs proves (BH2). ∎

**Lemma BH3 [PROVED].** If $N_3=N_4=0$, then

\[
 H\ge3m-\frac{15}{4}t_1-6t_2. \tag{BH3}
\]

**Proof.** Use $3-H_x$. Maximal cells cost $3(t_1+t_2)$. For non-maximal cells of support $r=0,1$, the preceding missing-direction argument gives

\[
 (3-H_x)_+\le\frac3{4-r}M_x,
\]

with total costs at most $3t_1/4$ and $2t_2$. A non-maximal support-two cell has two missing directions, both with top $x$. If $H_x<3$, necessarily $h(x)=1, H_x=2$, and its two present directions lead to distinct maximal upper covers. Counting these two incidences bounds their number by $t_2$. Total cost is $15t_1/4+6t_2$. ∎

These arguments do not assume a bound on the degrees of maximal cells. They also give useful all-multiplicity conclusions: for a boundary tile, $3m\ge15t_1+20t_2+36t_3$ implies $H\ge3m/2$ and Wilf. In particular $m\ge12|A|$ suffices. For a support-two tile, $2m\ge5t_1+8t_2$ suffices. These criteria are valid below the uniform thresholds as well.

## 4. Antichain bounds with a self-contained proof

For a finite down-set $C\subset\mathbb N^r$, let $a=|\max C|$, $n=|C|$. More generally the same bounds below hold for a subset of its maximal cells.

The column census gives

\[
 \sum_{y\in\max C}(r+|y|)\le rn. \tag{GAUSS}
\]

Indeed each coordinate column contributes its length to the sum of $T(x)=\sum_{b:x\text{ a }b\text{-top}}(x_b+1)$, so $\sum_CT=rn$; for a maximal $y$, $T(y)=r+|y|$.

Here is the antichain inequality needed, including its proof, rather than an appeal to Macaulay or an external packing theorem:

\[
 \sum_{y\in A}\binom{|y|+r-1}{r-1}^{-1}\le1 \quad(A\text{ an antichain in }\mathbb N^r). \tag{LYM}
\]

Start a chain at zero; from $x$ of degree $j$, increment coordinate $b$ with probability $(x_b+1)/(j+r)$. Induction shows the degree-$j$ location is uniform on the $\binom{j+r-1}{r-1}$ compositions: for a target $y$ of degree $j+1$, the predecessor probabilities add to $(j+1)/(j+r)$ times the common degree-$j$ probability. A chain meets an antichain at most once, proving (LYM). One can truncate the chain at the largest degree in $A$; no infinite probability argument is required.

For $r=2$, Jensen applied to $1/(h+1)$, followed by (GAUSS), gives

\[
 n\ge\frac{a(a+1)}2. \tag{TYPE2}
\]

For $r=3$, put $z=h+3/2$. The function $2/(z^2-1/4)$ is convex and decreasing for $z\ge3/2$, with second derivative $(12z^2+1)/(z^2-1/4)^3>0$. Equations (LYM) and (GAUSS) give

\[
 6n\ge a(\sqrt{8a+1}+3). \tag{TYPE3}
\]

For every positive support face $I$, shift its cells by $\mathbf1_I$. They form a down-set in $\mathbb N^{|I|}$. Maximal cells of $D$ on that face shift to a subset of its maximal cells. The six positive two-faces and four positive three-faces have disjoint interiors. Summing (TYPE2), and using convexity in (TYPE3), gives

\[
 12N_2\ge t_2^2+6t_2,\qquad
 6N_3\ge t_3(\sqrt{2t_3+1}+3). \tag{FACE-TYPE}
\]

For the latter Jensen step, $a\mapsto a\sqrt{8a+1}$ has second derivative $8(6a+1)/(8a+1)^{3/2}>0$. In particular

\[
 t_2\le\sqrt{12N_2},\qquad t_3^3\le18N_3^2. \tag{TYPE-WEAK}
\]

## 5. Degree mass inside a face

**Lemma DEG-HEIGHT [PROVED].** If $C\subset\mathbb N^r$ is a finite down-set, then

\[
 r\sum_Ch_C(x)\ge\sum_C|x|. \tag{DH}
\]

For each direction, the sum of the upward distances to the column tops equals the sum of that coordinate, by reversing each column. Pointwise each upward distance is at most $h_C(x)$. Summing proves (DH).

Define $D_r(n;f)$ as the smallest sum of degrees of $n$ distinct cells in $f$ disjoint copies of $\mathbb N^r$. This is entirely explicit: fill degrees $j=0,1,\ldots$, each of capacity $f\binom{j+r-1}{r-1}$.

When $N_4=0$, a support-three cell has its missing-direction top equal to itself, and its height is its height inside its positive three-face. Consequently

\[
 3H\ge D_3(N_3;4). \tag{G3}
\]

The following smooth lower bound is useful:

\[
 H\ge\frac{N_3}{4}\left(\frac{3N_3}{2}\right)^{1/3}-\frac{N_3}{2}. \tag{G3-CONT}
\]

To verify it, replace the cells of the four shifted faces by disjoint unit cubes. Their total volume is $N_3$, and the integral of the coordinate sum is $\sum|x|+3N_3/2$. Among sets of volume $N_3$ in four positive octants, this integral is minimized by four equal initial simplices. Their radius is $\mathcal R=(3N_3/2)^{1/3}$, and their mean coordinate sum is $3\mathcal R/4$. This minimizing assertion follows directly by subtracting the filled simplices: the removed part has coordinate sum at most $\mathcal R$, the added part at least $\mathcal R$, and their volumes agree. Apply (DH) and divide by three to obtain (G3-CONT). No Brunn–Minkowski, Minkowski, or external isoperimetric theorem is used.

## 6. Proof of Theorem B4

Assume $m\ge22^3$.

If $N_3\ge3m/8$, then $\mathcal R=(3N_3/2)^{1/3}\ge(9m/16)^{1/3}>18$. For the last inequality it suffices to note

\[
 (9/16)^{1/3}>9/11,\qquad 22(9/11)=18;
\]

the cubed inequality is $1331>1296$. Equation (G3-CONT) now gives $H>4N_3\ge3m/2$.

If $N_3<3m/8$, (BH2), $t_1\le4$, and (TYPE-WEAK) give

\[
 H\ge2m-10-\frac{35}{3}\sqrt m-\frac{33}{4}m^{2/3}. \tag{B4-LOW}
\]

Here $\sqrt{12}<7/2$, and

\[
 6\sqrt[3]{18}(3/8)^{2/3}
 =6(81/32)^{1/3}<33/4,
\]

since $1296<1331$ after cubing. As $m\ge22^3>10,000$, the loss in (B4-LOW), divided by $m$, is strictly less than

\[
 \frac1{1000}+\frac7{60}+\frac38=\frac{739}{1500}<\frac12.
\]

Thus $H>3m/2$ in both cases. Equation (HC) proves $W\ge3$. ∎

This proves an infinite class. It does not assert that B4 holds for every smaller multiplicity.

## 7. Support-two tiles: the axis and face payment

In the rest of the proof assume $N_3=N_4=0$. For an unordered pair $ab$, let $C_{ab}$ be the shifted positive two-face, $v_{ab}=|C_{ab}|$, and $a_{ab}=|\max C_{ab}|$. Here every maximal cell of $C_{ab}$ is maximal in $D$. Put $f=\#\{ab:v_{ab}>0\}$, so $f\le6$, and $t=t_2=\sum a_{ab}$.

If $a_{ab}=a>0$, then

\[
 v_{ab}\ge\binom{a+1}{2},\qquad |y|\ge a+1\quad(y\text{ a maximal positive }ab\text{-cell}). \tag{FACE-A}
\]

The size bound is (TYPE2). For the degree bound order the $a$ positive incomparable points by first coordinate. At position $i=1,\ldots,a$, its coordinates are at least $i$ and $a+1-i$. Each maximal-cell weight on this face is therefore at least $a+5$.

Let $L_a=\max\{i:ie_a\in D\}$, so $N_1=\sum_aL_a$. Let $A_{ab}=\max\{i\ge1:ie_a+e_b\in D\}$, or zero for an empty face. For $i>A_{ab}$, the $b$-top of $ie_a$ is $ie_a$, whose height is at least $L_a-i$. Therefore the axis cells contribute at least

\[
 \sum_{a\ne b}\binom{L_a-A_{ab}}2.
\]

The first positive row and column in $C_{ab}$ give $A_{ab}+A_{ba}\le v_{ab}+1$ when it is nonempty. Hence $\sum_{a\ne b} A_{ab}\le N_2+f$. There are twelve nonnegative integers $L_a-A_{ab}$, with sum at least $3N_1-N_2-f$.

For $q\ge1$, define, with $S\ge0$ and $S=qu+r, 0\le r<q$,

\[
 J_q(S)=q\binom u2+ru,
\]

and set $J_q(S)=0$ for $S<0$. Convexity of the integer sequence $\binom j2$ shows this is the minimum of $\sum_{i=1}^q\binom{z_i}2$ at fixed sum $S$; it is nondecreasing in $S$.

A positive two-face cell has two missing-direction tops equal to itself. Equation (DH) with $r=2$ shows their contribution is at least the sum of degrees in the shifted face. These contributions are disjoint from the axis contributions. Thus

\[
 H\ge D_2(N_2;f)+J_{12}(3N_1-N_2-f). \tag{AXIS-FACE}
\]

The weaker version with $f=6$ is valid even for fewer faces, by adding empty copies and increasing the loss in $J_{12}$.

## 8. Analytic support-two theorem for $m\ge144$

From (BH3), $t_1\le4$, and the pair weights being at least six,

\[
 H\ge3m-15-6t,\qquad R\ge3t(t-1).
\]

Also $N_1\ge4$, and (FACE-TYPE) gives

\[
 t^2+6t\le12(m-5),\quad t\le\sqrt{12m}-3.
\]

The lower bound on the right side of (HC) is

\[
 F_m(t)=\tfrac32m^2-\tfrac{21}{2}m-15+3t^2-(6m+9)t.
\]

For $m\ge144$ it is decreasing throughout $0\le t\le\sqrt{12m}-3$. Evaluating at that endpoint gives

\[
 F_m(t)\ge\tfrac32m^2+\tfrac{87}{2}m+39-(6m+27)\sqrt{12m}. \tag{A144}
\]

Set $x=\sqrt m=12+u$, $u\ge0$, and use $\sqrt{12}<52/15$. The right side of (A144) is strictly larger than

\[
 \frac{1707}{5}+\frac{11664}{5}u+\frac{5907}{10}u^2+\frac{256}{5}u^3+\frac32u^4>0. \tag{A144-POLY}
\]

This is an exact polynomial identity after the rational replacement. It proves strict Wilf for all $m\ge144$.

## 9. Finite certificate for $64\le m\le143$

This certificate is over necessary count profiles, not sampled semigroups.

Enumerate $N_2=0,\ldots,m-5$, put $N_1=m-1-N_2$, and enumerate $t_1=0,\ldots,4$. Enumerate the six nonnegative face-antichain sizes, in nondecreasing order $a_1\le\cdots\le a_6$, with

\[
 \sum_i a_i=t,\qquad \sum_i\binom{a_i+1}{2}\le N_2.
\]

The ordering loses nothing: at this stage only the multiset of face sizes is used. Each face supplies $a_i$ weights of size at least $a_i+5$. Let $R_{\rm pair}(a_1,\ldots,a_6)$ be the rank term of that multiset. Define $R_*(t,N_2)$ to be the minimum of these finitely many rank terms over the displayed constraints. The actual partition of a tile is among them. Axis maximal cells have weight at least five, so (R-MIN) gives

\[
 R\ge R_*(t,N_2)+5\left(tt_1+\binom{t_1}{2}\right). \tag{RF}
\]

For each profile set

\[
 H_* =\max\left(0,
 \left\lceil3m-\frac{15}{4}t_1-6t\right\rceil,
 D_2(N_2;6)+J_{12}(3N_1-N_2-6)\right). \tag{HF}
\]

Equations (BH3) and (AXIS-FACE) give $H\ge H_*$. The final exact check is

\[
 (m+1)H_*+R_*(t,N_2)+5\left(tt_1+\binom{t_1}{2}\right)
 -\frac32m(m-1)>0. \tag{FIN64}
\]

**FINITE CHECK.** `two_refined.py` checks (FIN64) in integer arithmetic. It enumerates 7,439 face-size partitions and 839,610 count profiles. There are zero failures. The minimum is **9**, at

\[
 (m,N_1,N_2,t_1,t,H_*,R_{\rm lower})=(64,21,42,4,18,69,1572).
\]

`two_verify.c`, written separately, computes the rank term by pairwise minima instead of sorted ranks, and enumerates the partition envelope in another order. It gives exactly the same partition count, profile count, minimum, and minimizing tuple. This provides two exact implementations of the finite step. The source files and logs are included.

## 10. Finite face-profile certificate for $60\le m\le63$

Retain the placement of the six face sizes on the edges of $K_4$. Let $J\subseteq[4]$ be the axes whose final axis cell $L_be_b$ is maximal in $D$. Thus $|J|=t_1$. Set

\[
 b_i=\max_{j\ne i}a_{ij},\qquad
 \ell_i=\begin{cases}b_i+[i\in J],&b_i>0,\\1,&b_i=0.\end{cases}
\]

Every isolated vertex $(b_i=0)$ belongs to $J$. Every actual axis length satisfies $L_i\ge\ell_i$: a positive face with $a$ maximal cells has extent at least $a$ in both coordinates; if the axis top itself is maximal, its length must be strictly larger than that face extent. Therefore

\[
 N_1\ge\sum_i\ell_i. \tag{AXIS-MIN}
\]

Start with the weights consisting of $a_{ij}$ copies of $a_{ij}+5$ per face and one weight $4+\ell_i$ for each $i\in J$. Their rank term is a lower bound on $R$.

There is one further improvement if $J=[4]$, because all four axis lengths occur in the weight list and $\sum_iL_i=N_1$. Put $E=N_1-\sum_i\ell_i$. By the concavity in (R-MIN), the minimum rank term on the simplex $L_i\ge\ell_i, \sum_i L_i=N_1$ is attained at a vertex. Thus it suffices to try the four weight lists obtained by adding all $E$ to one axis weight. The minimum of these four rank terms is still a valid lower bound on $R$. For $J\ne[4]$ the unallocated length may all lie on non-maximal axes, and the base weight list is used.

For each profile use the maximum of (BH3) and (AXIS-FACE), rounded up where necessary, and this rank lower bound in (HC).

**FINITE CHECK.** `support2_fin.c` enumerates every ordered edge tuple with $\sum_{ij}\binom{a_{ij}+1}{2}\le58$, every maximal-axis subset, every $N_2$ above that minimum, and $N_1=m-1-N_2\ge\sum\ell_i$. The cap 58 is complete because $m\le63, N_1\ge4$. There are 134,382 edge tuples before the other filters. The certified rows are:

| $m$ | Expanded profiles | Minimum right side of (HC) |
|---:|---:|---:|
|60|8,733,115|36|
|61|9,429,611|40|
|62|10,168,171|99|
|63|10,950,744|154|

Every minimum is positive. This completes B2, together with §§8–9. The code also enumerated $40\le m\le59$; it does **not** certify that interval (see §13).

## 11. An unbounded carried family in the intrinsic B2 class

This section proves non-vacuity at unbounded multiplicity and unbounded height. It is not used to prove B2.

For $N\ge2$, put

\[
 m=N(N+2),\quad a=2m-N-1,\quad b=2m-1,
 \quad g_A=(4N-4)m+1,\quad g_B=g_A+N.
\]

Then

\[
 S_N=\langle m,a,b,g_A,g_B\rangle
\]

has embedding dimension five. An Apéry factorization tile consists of

\[
 \{(x,y,0,0):0\le x,y\le N\}
 \setminus\{(N,N,0,0),(N,N-1,0,0),(N-1,N,0,0)\}
 \quad\cup\{e_3,e_4\}. \tag{L-TILE}
\]

Here are complete checks of this assertion. First take $T=\langle m,a,b\rangle$. The reductions

\[
 (N+1)a=b+(2N-1)m,\qquad (N+1)b=a+2Nm,\qquad N(a+b)=(4N-1)m
\]

strictly lower the represented value by a positive multiple of $m$. They reduce every factorization in $a,b$ to the rectangle $0\le x,y\le N$ with its corner $(N,N)$ deleted. That rectangle has exactly $m$ cells, and the two relation vectors $(N,N)$ and $(-1,N+1)$ generate a sublattice of determinant $N(N+2)=m$. The reductions give a representative in each residue (also $\gcd(m,b)=1$); with exactly $m$ cells, the labels are distinct. The reductions therefore prove these representatives are the Apéry minima.

Its maximal cells are $A=(N,N-1)$ and $B=(N-1,N)$, with

\[
 v(A)=(4N-3)m+1,\qquad v(B)=(4N-3)m+N+1.
\]

Their predecessors $v(A)-m=g_A, v(B)-m=g_B$ are precisely the two pseudo-Frobenius gaps: adding each of $m,a,b$ to either lands in $T$. This follows from maximality in the displayed tile, or directly from the three reductions. Their difference is $N<m$, hence is not in $T$, and $2g_A>g_B=F(T)$. Consequently adjoining both adds exactly those two gaps, neither new generator decomposes, and the three old generators remain minimal. Replacing the two Apéry maxima by the two new units gives (L-TILE).

The largest new Apéry value is $g_B$: every old non-maximal Apéry cell is at least $a>m$ below one of the old maxima. Thus

\[
 c(S_N)=(4N-5)m+N+2,\quad q=4N-4,\quad
 \ell(S_N)=(2N-4)m+3N+3,
\]

and

\[
 W(S_N)=(6N-15)m+14N+13>0\quad(N\ge3).
\]

For the formula for $\ell$, the old tile has $\sum x=\sum y=N(m-1)/2$, so $g(T)=(2N-1)(m-1)$. Adjoining the two gaps lowers the genus by two. These formulas can also be checked directly from (L-TILE).

The height is $2N-2$, and $a+b+g_A>g_B=c+m-1$, giving the intrinsic B2 hypothesis. This family has genuine carries: the Apéry element $2a$ has the unique factorization $2e_1$, since $g_A>2a$, every three-generator sum is at least $3a>2a$, and the other two-factor sums in $a,b$ are larger. Its canonical offset sum is $2(a-m)>m$. Thus NO-WRAP fails. For $N\ge7$, $m\ge63, q\ge24$, the height exceeds three, $3e<m$, and $e(\eta+2)=20<2m$, with $\eta=2$. The LK+YZ first-band lower bound is exactly $8(N-1)^2$; it does not prove Wilf for $N\ge7$, since

\[
 c-5\cdot8(N-1)^2=(N-1)(4N^2-33N+38)>0.
\]

This is a scope check, not a claim that no other sufficient criterion in the literature could recognize this particular family. The new theorems concern general e=5 semigroups; they do not close e=5 intersected with P18. In fact the intrinsic B4 condition has no P18 member at its large-multiplicity threshold: P18 gives $\sum n_i<8m$, hence $c<7m$ under that condition, tile degree at most seven, and $m\le\binom{11}{4}=330$.

## 12. Verification record

All numerical claims in this section are **FINITE CHECK / OBSERVED**, and are not substituted for the proofs above.

### 12.1 Full E153 shape census

`shape_scan.c` reads `certificate_all_m.jsonl.gz` on fejer for every $5\le m\le39$, restricting to distinct nonzero residues and tiles containing all four units. It computes heights and tops independently from the certificate cells. It checks (BH2), (BH3), (FACE-TYPE), (G3), (G3-CONT), (AXIS-FACE), the per-face degree/volume assertions, the placed-face rank and axis bounds of §10, and TYPE4, whenever their hypotheses hold.

- Total applicable e=5 tile occurrences: **4,568,871**.
- Boundary occurrences $N_4=0$: **4,473,923**.
- Support-at-most-two occurrences: **1,755,418**.
- Failures of the new applicable inequalities: **0**.
- Minimum scaled BH2 and BH3 slack: zero.

These are occurrences in the supplied certificates, not claimed distinct shapes or all possible weight vectors. The checks are shape-only: multiplying a residue vector by a unit does not change any tested quantity, so no unit-orbit expansion is needed for these statements. No labeling-dependent theorem is inferred from one representative per orbit.

The exploratory universal inequality $H+7|A|\ge2m$ had minimum slack 16 in this census; the maximum observed ratio $(2m-H)/|A|$ was $22/8$. It is **not proved** here.

### 12.2 Random shapes and actual semigroups

`boundary.py` builds arbitrary boundary down-sets, including nearly rank-flat growth, long columns, and both support restrictions, and checks the displayed integer inequalities. It also computes lex/grlex Apéry tiles by Dijkstra, verifies that all five generators are primitive, and checks the applicable inequalities.

| Seed | Boundary shapes | Primitive semigroup tiles | Boundary semigroup tiles | Support-two tiles |
|---:|---:|---:|---:|---:|
|1019|1,212|1,956|972|314|
|1020|1,612|2,514|1,226|407|

The 12 rank-flat boundary families in each shape count are intentional stress cases. Semigroup sampling includes P18, near progressions with an outlier, a high primitive direction, and projected two-dimensional cones. Multiplicities are 40–1000. There were no failures. The second run includes the axis-height inequality.

`stress.py` performs 24 annealing runs at multiplicities 40–500, restricting evaluated primitive semigroups to $q\ge5$ and tile height at least four. It evaluated **3,866** such tiles, **911** boundary tiles. There were no failures of the proved applicable inequalities and no negative Wilf value. Its minimum HCR was (1629/820), at

\[
 \langle41,85,135,184,206\rangle,\quad q=17,\quad \operatorname{ht}=5,
 \quad H=108,quad(t_1,t_2,t_3)=(0,6,4),\quad R=351,\quad W=879.
\]

This is evidence only; it is not an exhaustion of the P10 frontier.

### 12.3 Explicit families and symbolic constants

`families.py` checks the polynomial coefficients in (A144-POLY) with exact `Fraction` arithmetic, and the rational cube comparisons in §6. It uses Dijkstra independently of the reductions to check the balanced L-family for $3\le N\le40$. It also checks a different two-face family for $3\le N\le40$, and a three-dimensional box core with one Frobenius spike for $N=4,8,12,24$. The latter includes $m=13,824$, above B4's threshold, and has height 68 and nonzero carries. Every expected tile agrees with the independently computed Apéry tile.

Reproduction commands and output files are collected in `checks/`. All scripts use only the Python standard library or C plus zlib. The fejer versions were Python 3.12.3 and GCC 13.3.0 (Ubuntu 24.04).

## 13. Preserved failures and limitations

1. **Count-relaxation failure, not a semigroup counterexample.** The simpler certificate (FIN64) does not close all $m\ge40$. The abstract profile $(m,N_1,N_2,t_1,t)=(63,20,42,4,18)$ gives $H_*=66, R_{\rm lower}=1572$, and slack $-63$. The stronger placed-face certificate eliminates that row. No actual tile realizing the negative relaxation is asserted.

2. **Placed-face relaxation still leaves a finite interval.** `support2_fin.c` leaves 389,942 expanded profiles in $40\le m\le59$, including symmetry repetitions. Its smallest multiplicity is 40; its largest is 59. The last multiplicity has 828 profiles and minimum relaxed slack $-17$. These are necessary-parameter profiles, not constructed lattice tiles or Wilf counterexamples. The report does not call B2 an all-multiplicity theorem.

3. **The boundary hypothesis in BH2 cannot simply be deleted.** On the full four-dimensional degree-five simplex, $m=126, H=0, (t_1,t_2,t_3,t_4)=(4,24,24,4)$. The right side of (BH2), if incorrectly applied without $N_4=0$, is $18>0$. This is the first failure among the full simplices of degrees one through eight tested by `obstructions.py`. It is a down-set counterexample to that extension, not a lattice-tile counterexample.

4. **The support-two face payment does not extend unchanged to three-support cells.** The degree-three simplex $D=\{x:|x|\le3\}$ is already a boundary down-set, with $m=35, H=0, N_2=18$, while $D_2(N_2;6)=12$. This is the first failure in the tested rank-flat family. The next boundary member, $D=\{x:|x|\le4, |\operatorname{supp}x|\le3\}$, has $m=69, H=4, N_2=36$ and $D_2(N_2;6)=48$. Thus the pair-degree payment alone is invalid once positive three-faces can extend its missing-direction columns. The exact hypotheses in §7 are essential.

5. **Cylinder structure alone is insufficient for a small universal loss constant.** The degree-three simplex in $\mathbb N^4$ has $m=35, H=0, |A|=20$, hence $H+3|A|<2m$. Its cylinder determined by the coordinate projections consists of that simplex plus the single cell $(1,1,1,1)$, so it even has the one-cone cylinder form after deleting that cell. It cannot be an injectively labeled lattice tile: if $B=\{0,p_1,\ldots,p_4\}$ had all three-fold sums distinct, the signed labels $b$ (5 choices), $2b-b'$ with $b\ne b'$ (20 choices), and $b+b'-b''$ with three distinct entries and unordered positive pair (30 choices) would all be distinct. Any collision cross-multiplies to an equality of two three-fold sums, forcing the same formal signed label. This requires $m\ge55$, contradicting $m=35$. This prevents a proof of the stronger $H+3|A|\ge2m$ from the cylinder form alone. It does not refute that inequality for actual tiles.

6. **Implementation correction, preserved.** Scanner v1 accidentally allowed the missing-unit flag of one tile in a record to suppress later tiles in that record. It was caught before any census claim. v1 counted only 156,857 occurrences. All counts quoted here are from corrected v5, which counts 4,568,871. v2–v5 agree on this total; v4 adds the face/axis checks, and v5 adds the continuous face bound, the placed-face rank/axis bounds, and TYPE4. v1 is archived on fejer and is not used in a proof.

No Wilf counterexample or contradiction to an accepted project theorem was found. The new proofs use HCR, and do not claim a new all-height MaxCL theorem.

## 14. Exact residual family and the next lemma

After adding these results to the user's pre-existing exclusions, a remaining e=5 case has $m\ge40, q\ge5$, and tile height at least four, and must avoid all the pre-existing criteria. Relative to the chosen factorization tile, it lies in one of:

1. **Full support:** $(1,1,1,1)\in D$.
2. **Boundary with a positive three-face:** $N_4=0, N_3>0, 40\le m\le10,647$, and the direct lower bounds (BH2), (G3), (HC) do not certify it.
3. **Two-support finite multiplicities:** $N_3=N_4=0, 40\le m\le59$, with a placed-face count profile surviving §10 and avoiding the earlier criteria.

This is not a reduction of the *whole* e=5 problem to a finite computation: family 1 still has unbounded multiplicity. In particular no universal $M_0$ for all e=5 semigroups is claimed.

The global strategy review was: discontinue an unsupported promotion of the small-tile $H+7|A|\ge2m$ observation; prove the missing-direction payment in the class where it is valid; use finite enumeration only after an analytic tail exists. The resulting B2/B4 theorems are infinite-class statements, not larger zero-failure censuses.

A precise next target is a **lattice** extension of the payment, for example

\[
 H(D)+7|\max D|\ge2|D| \quad\text{for four-dimensional lattice down-set tiles}. \tag{FULL-INTERIOR, OPEN}
\]

The new proof handles the boundary contribution with constant six; it does not control support-four cells, or the three-support column tops that move into the interior. Residue injectivity, beyond the bare cylinder form in failure 5, must enter that step.

For scale, (FULL-INTERIOR) would give a genuine all-large-multiplicity theorem. The same self-contained antichain argument in dimension four yields

\[
 |\max D|^4\le\frac{32}{3}|D|^3. \tag{TYPE4}
\]

To see this, use $z=|y|+2$ in (LYM). The function $6/(z^3-z)$ is convex and decreasing for $z\ge2$; its second derivative is $6(12z^4-6z^2+2)/(z^3-z)^3>0$. If $\zeta^3-\zeta=6t$, (LYM) gives mean $z\ge\zeta>(6t)^{1/3}$, and (GAUSS) gives $4m\ge t(\zeta+2)>6^{1/3}t^{4/3}$. Thus a proved $H\ge2m-Ct$ would imply Wilf whenever $m\ge(512/3)C^4$; for $C=7$, $m\ge409,771$ suffices. This implication is **conditional**, and the finite interval below it is not certified here.

**Status.** B4 is an analytic theorem; B2 is an analytic theorem plus two fully specified finite certificates. The intrinsic sum-of-generators corollaries follow without choosing a special term order. Full e=5 Wilf, and the support-four height payment, remain open.
