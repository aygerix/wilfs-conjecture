# PROOFS.md — precise statements, proofs, dependency graph, status

Status legend: PROVED (on paper, here) | CHECKED (exact computation, stated range) | CONJ | FALSE | LEAN (kernel-checked)

Notation. S ≠ ℕ numerical semigroup, multiplicity m ≥ 2, conductor c, F = c−1, genus g, n = ell = c − g,
P minimal generators, e = |P|, P' = P∖{m} = {p_1,…,p_d}, d = e − 1 ≥ 1.
Ap = Ap(S,m) = {w_0 = 0, …}, M = max Ap = F + m = c + m − 1 (Brauer–Shockley). W(S) = e·n − c.
For w ∈ Ap and a ∈ [d]: ν_a(w) = max{k ≥ 0 : w − k p_a ∈ S}.
Facts used (standard, elementary): (i) g = Σ_{w∈Ap} (w − (w mod m))/m = (Σ_{w∈Ap} w)/m − (m−1)/2 (Selmer);
(ii) M = F + m; (iii) if w ∈ Ap and w = x + y with x, y ∈ S then x, y ∈ Ap (summand closure);
(iv) every w ∈ Ap∖{0} is a sum of elements of P' (m cannot appear in a factorization of an Apéry element).

---------------------------------------------------------------------------------------------------
## Identity CH (chain identity) — PROVED 2026-10-17; CHECKED genus ≤ 18 (src/chains.py)

For a ∈ [d], call a maximal arithmetic progression with difference p_a contained in Ap a *p_a-chain*.
The p_a-chains partition Ap. Let Def_a = Σ_{C p_a-chain} |C|·(M − top(C)) and
E = Σ_{w∈Ap} E(w), E(w) = Σ_a p_a ν_a(w) − w. Then

    m·W(S) = Σ_{a=1}^{d} Def_a + E − (d−1)·m(m−1)/2,   with Def_a ≥ 0 and E ≥ 0.

Proof. (1) For a chain C = {b, b+p_a, …, b+(L−1)p_a}: b − p_a ∉ S (else b − p_a ∈ Ap by (iii) and C not
maximal), so ν_a(b + k p_a) = k by (iii). Hence Σ_{w∈C}(w + p_a ν_a(w)) = Σ_k (b + 2k p_a) = L(b+(L−1)p_a)
= |C|·top(C). Summing over chains: Σ_{w∈Ap} w + p_a Σ_w ν_a(w) = Σ_C |C| top(C), so
Def_a = mM − Σ_w w − p_a Σ_w ν_a(w) ≥ 0 since top(C) ≤ M.
(2) Σ_a Def_a + E = d mM − dΣw − Σ_w Σ_a p_aν_a(w) + Σ_wΣ_a p_aν_a(w) − Σw = d mM − (d+1)Σ_w w.
(3) By (i),(ii): W = e(c−g) − c = d c − (d+1) g, and c = M − m + 1, g = Σw/m − (m−1)/2, so
m W = d m(M − m + 1) − (d+1)Σw + (d+1)m(m−1)/2 = d mM − (d+1)Σw − (d−1)m(m−1)/2.
(4) E(w) ≥ 0: take any factorization w = Σ n_a p_a (by (iv)); then w − n_a p_a ∈ S so ν_a(w) ≥ n_a and
Σ p_a ν_a(w) ≥ w. ∎

### Corollary H (homogeneous / "continuous" Wilf) — PROVED
(d+1)·Σ_{w∈Ap} w ≤ d·m·M, i.e. mean(Ap) ≤ (d/(d+1))·max(Ap). Equivalently m·W ≥ −(d−1)m(m−1)/2,
i.e. Wilf holds up to the additive error (d−1)(m−1)/2:  e·n ≥ c − (e−2)(m−1)/2.
(Immediate from CH. This is a discrete divergence-theorem argument on the Apéry down-set; it shows
Wilf is exactly "homogeneous Chebyshev inequality + a discrete correction of size (d−1)m(m−1)/2".)
Novelty: NOT checked against literature yet (literature agent did not report it). Treat as possibly known.

---------------------------------------------------------------------------------------------------
## Lemma A (top-layer reduction) — PROVED 2026-10-17

Let X_q = Ap ∩ [c, c+m) (top layer), π(u) = u − c + 1 ∈ [1, m] for u ∈ X_q, and
ℓ(u) = min{|n| : u = Σ n_a p_a, n ∈ ℕ^d} (shortest factorization over P'). Then

    m·W(S) ≥ m((d+1)m + d − 1)/2 − Σ_{u∈X_q} π(u)(d + ℓ(u))  +  Σ_{w∈Ap∖X_q} E(w).

Proof. Every u ∈ X_q is a chain top in every direction a (u + p_a ≥ c + m > M), and the p_a-chain
with top u has length ν_a(u) + 1. Every other chain top t lies in Ap∖X_q, so t < c and M − t ≥ m.
The chains of direction a have total length m. Hence, with Λ(u) = Σ_a (ν_a(u)+1) and
M − u = m − π(u):
  Σ_a Def_a ≥ Σ_{u∈X_q} Λ(u)(m − π(u)) + m(dm − Σ_{u∈X_q}Λ(u)) = dm² − Σ_{u∈X_q} π(u)Λ(u).
For u ∈ X_q fix a shortest factorization n (|n| = ℓ(u)); ν_a(u) ≥ n_a and π(u) ≤ m < p_a give
  π(u)Λ(u) − E(u) = d π(u) + Σ_a ν_a(u)(π(u) − p_a) + u ≤ d π(u) + Σ_a n_a(π(u) − p_a) + u = π(u)(d + ℓ(u)).
Insert in CH and use dm² − (d−1)m(m−1)/2 = m((d+1)m + d − 1)/2. ∎

### Conjecture TOP'' (top-layer inequality) — CONJ; CHECKED genus ≤ 18 (all 33,281 S ≠ ℕ),
### tight exactly on the 79 semigroups with W = 0 in that range; extended runs in EXPERIMENTS.md

    Σ_{u∈X_q} π(u)·(d + ℓ(u)) ≤ m((d+1)m + d − 1)/2.

Equivalent form: with Π = π(X_q) ⊆ [1,m] and Π^c = [1,m]∖Π (positions j with c−1+j−m ∈ S, i.e. the
left elements of the last level [c−m, c)):

    Σ_{u∈X_q} π(u)·ℓ(u) ≤ m(m−1)/2 + d·Σ_{j∈Π^c} j.

TOP'' ⇒ Wilf (Lemma A). Equality cases: e = 2 (X_q = {M}, ℓ(M) = m−1, Π^c = [1,m−1]) and
S = T_{m,q} = mℕ ∪ [qm,∞) (X_q = right primitives, ℓ = 1, Π^c = {1}).

---------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------
## Factorization down-set D and the column identity CH' — PROVED 2026-10-17
Fix a monomial order ≺ on ℕ^d. For w ∈ Ap let n(w) be the ≺-least factorization of w over P' (exists by (iv)).
D := {n(w) : w ∈ Ap}. Then (a) |D| = m and φ(n) := ⟨n,p⟩ mod m is a bijection D → ℤ/m;
(b) D is a down-set: if n = n(w), n' ≤ n then w' = ⟨n',p⟩ ∈ Ap by (iii), and n' = n(w') (else n'' ≺ n' with
⟨n'',p⟩ = w' gives n''+(n−n') ≺ n, a smaller factorization of w); (c) e_a ∈ D for all a (p_a minimal generator).
For direction a, the *a-columns* are the maximal sets {b, b+e_a, …, b+(L−1)e_a} ⊆ D (b_a = 0); top = b+(L−1)e_a.
Column identity: with w(n) = ⟨n,p⟩ (integers), Σ_{x∈C}(w(x) + p_a x_a) = |C|·w(top C) (sum of an AP), hence
    Σ_a Σ_{a-columns C} |C|·w(top C) = (d+1)·Σ_{w∈Ap} w,
    Σ_a Σ_C |C|·(M − w(top C)) = d m M − (d+1)ΣAp = m·W + (d−1)·m(m−1)/2.            (CH')
(Same algebra as CH step (3).)  Every term M − w(top C) ≥ 0.

## Conjecture CL (Carry Lemma) — **FALSE** (2026-10-17, E47: S = ⟨14,22,23,57,61,62,63⟩, LHS 441 < 455;
## examples/CL_counterexample.md). Previously CHECKED genus ≤ 24 (E13). CL ⇒ Wilf is PROVED (premise false).
## Surviving restricted form (CONJ): CL for S with 3e < m and c > 3m (0/1664 failures, E48); with LITERATURE #13, #21
## it would imply Wilf.
For S as above (any monomial order):
    Σ_a Σ_{a-columns C} |C|·((M − w(top C)) mod m)  ≥  (d−1)·m(m−1)/2.                  (CL)
Proof of CL ⇒ W(S) ≥ 0: x ≥ (x mod m) for x ≥ 0, so by CH' m·W + (d−1)m(m−1)/2 ≥ LHS(CL) ≥ (d−1)m(m−1)/2. ∎
Exact relation: m·W = m·Σ_aΣ_C|C|·⌊(M − w(top C))/m⌋ + [LHS(CL) − (d−1)m(m−1)/2]  (depth part + CL slack).
CL ⇒ TOP'' (slack(TOP'') = m·W − Σ_{low D-column tops}|C|(F − t), verified numerically; see NOTEBOOK).

### Tile-CL (the depth-free general form) — **FALSE** (E47: tile of the CL counterexample, slack −1 at s = 13; upper
### bound also fails, E47/E51). Previously CHECKED exhaustively for small tiles (E15: d=2 m≤15, d=3 m≤11, d=4 m≤8).
### Still OPEN for d = 2 (L-shapes); PROVED for boxes in every d (below).
Data: d ≥ 1; D ⊆ ℕ^d a down-set with |D| = m; p ∈ (ℤ/m)^d with φ(n) = Σ n_a p_a mod m bijective on D
(equivalently D is a fundamental domain of the lattice Λ = ker φ). T(y) := Σ_{a : y+e_a ∉ D} (y_a + 1)
(= Σ over the columns topped by y of their lengths). Claim: for every s ∈ ℤ/m
    f(s) := Σ_{y∈D} T(y)·⟨s − φ(y)⟩  ≥  (d−1)·m(m−1)/2,      ⟨x⟩ := x mod m ∈ [0,m).        (Tile-CL)
CL for S is Tile-CL for (D, p mod m) at s = M mod m.  Directions a with D ⊆ {x_a = 0} add m(m−1)/2 to both sides.
Equivalent forms (all PROVED equivalent for tiles, using only Σ_y⟨σ+φ(y)⟩ = m(m−1)/2 and linear algebra):
 (II)  Σ_y T(y)·r(y) ≤ (d+1)·m(m−1)/2 for every labeling r = ⟨σ + φ⟩ (σ ∈ ℤ/m);   [r = m−1−R]
 (Diff) Σ_a Σ_{x∈D} (r(top_a x) − r(x)) ≤ Σ_{x∈D} r(x) = m(m−1)/2, top_a x = top of x's a-column;
 (Win) with c_a(y) = a-coordinate of φ^{-1}(y), Ȳ_a = mean of c_a, p̂_a ∈ [0,m) the residue of p_a:
       Φ(t) := Σ_a Σ_{j=1}^{p̂_a} (c_a(t+j) − Ȳ_a) ≥ −(m−1)/2 for all t   (f(t) − d m(m−1)/2 = m·Φ(t));
 (Wall) with N(y) = σ + ⟨y,p̂⟩, k = ⌊N/m⌋, r = N mod m:  Σ_y k(y) ≤ σ + Σ_y Σ_a y_a·[r(y) < p̂_a];
 (Walk) U(s) = Σ_{y=1}^{s}(T(φ^{-1}y) − d): max_s U − mean U ≤ (m−1)/2.
Two-sided corollary: applying Tile-CL to −φ gives |Φ(t)| ≤ (m−1)/2, so the residue-interval discrepancy
|Σ_{y∈I}(T(φ^{-1}y) − d)| ≤ m − 1 for every cyclic interval I (conditional on Tile-CL).
Local cell formula (PROVED): f(s) − (d−1)m(m−1)/2 = Σ_{z∈D} γ(z), γ(z) = (|z|+1)R(z) − Σ_a z_a R(z−e_a),
R = ⟨s − φ⟩ extended Λ-periodically; independent of shelling order.
Tightness families: e = 2 (single column); simplex tile {0, e_1..e_{m−1}} (T_{m,q}); "perfect" tiles where
⟨·,p̂⟩ maps D bijectively onto [0, m−1] (e.g. lex boxes) at s = −1.

### Ramp Lemma — PROVED 2026-10-17 (any down-set; no tiling hypothesis)
Let D ⊆ ℕ^d be a finite down-set, T(y) = Σ_{a: y+e_a∉D}(y_a+1), β = d+1−T, top_a x = top of x's a-column.
Call ρ: ℕ^d → ℝ *directionally convex* if Δ_aρ(u) := ρ(u+e_a) − ρ(u) is nondecreasing in every coordinate u_b
(b = a included). Then
    Σ_{y∈D} β(y)·ρ(y) ≤ |D|·ρ(0)        (≥ for directionally concave ρ; = for affine ρ).
Proof. Σ_y T(y)ρ(y) = Σ_aΣ_{x∈D} ρ(top_a x), so Σβρ = Σ_xρ(x) − Σ_aΣ_x(ρ(top_a x) − ρ(x)).
(1) With x^{(a)} = (x_1..x_a,0..0): ρ(x) − ρ(0) = Σ_a Σ_{i<x_a} Δ_aρ(x_1..x_{a−1},i,0..0)
    ≤ Σ_a Σ_{i<x_a} Δ_aρ(x_1..x_{a−1},i,x_{a+1}..x_d) = Σ_a (ρ(x) − ρ(x − x_a e_a))   (monotone in u_b, b>a).
(2) On an a-column with values ρ_0..ρ_{L−1} (convex in i): ρ_i + ρ_{L−1−i} ≤ ρ_0 + ρ_{L−1}, hence
    Σ_i(ρ_i − ρ_0) ≤ Σ_i(ρ_{L−1} − ρ_i). Summing: Σ_x(ρ(x) − ρ(0)) ≤ Σ_aΣ_x(ρ(top_a x) − ρ(x)). ∎
Instances: ρ = g(⟨y,q⟩), q ≥ 0, g convex. With g = (·−K)^+: Σ_{θ>K} β(H_θ) ≤ 0 where H_θ = {y∈D: ⟨y,q⟩ ≥ θ}.
Relation to Tile-CL: Tile-CL ⇔ Σ_y β(y)·k_σ(y) ∈ [σ−m+1, σ] with k_σ = ⌊(σ+⟨y,p̂⟩)/m⌋, a staircase that is
neither directionally convex nor concave; the lemma alone does not imply Tile-CL (see NOTEBOOK).

### Semigroup form of CL — PROVED equivalent 2026-10-17
With L = S ∩ [0,c), D the factorization tile, x(v) the D-cell of v mod m, δ(y) = ⌊(M − w(y))/m⌋ (left elements
in the class; Σδ = ell), κ(y) = ⌊w(y)/m⌋ (gaps in the class; Σκ = g):
    CL ⇔ W ≥ Σ_a Σ_{x∈D} δ(top_a x) ⇔ Σ_{y∈D} β(y)δ(y) ≥ c ⇔ Σ_{a=1}^{d} Σ_{v=c}^{c+n_a−1} x(v)_a ≥ g.
(Derivation: the left elements form the down-set 𝓛 = {(x,j): w(x)+jm < c} ⊆ D×ℕ; a good pair (s,a) is an
a-column of 𝓛 truncated by c rather than by D; counting truncated columns by their outer boundary cell
v ∈ [c, c+n_a) gives Σ_a Σ_v x(v)_a.)  Tile-CL at all s ⇔ the same with c replaced by any t ∈ ℤ.

### FALSE variants of CL (preserved)
- PDCL (per-direction: Σ_a min_s f_a(s) ≥ (d−1)m(m−1)/2): TRUE for d = 2 (m ≤ 12) but FALSE for d = 3,
  smallest D = {000,001,002,010,100,101}, p = (3,5,4), m = 6 (deficits 6+5+10 > 15).
- CL-inj (D a down-set with φ only injective, |D| < m): FALSE already for d = 1: D = {0,1,2}, p = 7, m = 10, σ = 3.

---------------------------------------------------------------------------------------------------
## FALSE strengthenings (preserved; see EXPERIMENTS.md)
- COV (H ⊆ union of e−1 sets f − L, f ∈ PF): FALSE whenever t > e−1 (each f ∈ PF is maximal, only
  f − L covers f). Smallest: ⟨7,9,10,15⟩.
- COV' (H ⊆ union of e−1 translates T − L, T ∈ ℤ arbitrary): FALSE; smallest found ⟨7,9,10,15⟩
  (e = 4, needs 4 translates, W = 2); 22 failures among t > e−1 cases with genus ≤ 16.
- S1 (Σ_a (C − Def_a)^+ ≤ C + E, C = m(m−1)/2): FALSE, ⟨7,11,12,20⟩ (W = 2).
- TOP_0 (Lemma A's predecessor without E): FALSE, e.g. ⟨9,13,14,15,16⟩.

---------------------------------------------------------------------------------------------------
## Tile-CL / Base-CL special cases — PROVED 2026-10-17 (true theorems; reach only e = 3 resp. symmetric S)
Carry form of Base-CL (PROVED, basecheck.py 0 mismatches): base-slack(σ) = σ + Σ_{x∈D} G(x),
G(x) = #{a : ℓ_a(x) > r(x)} − C(x), ℓ_a(x) = ⟨x_a p_a⟩, r(x) = ⟨σ + φ(x)⟩, C(x) = ⌊(σ + Σ_a ℓ_a(x))/m⌋
(= #{a : C(base_a x) = C(x) − 1} − C(x)).  Base-CL: base-slack ∈ [0, m−1].
(B2) **Base-CL for d = 2, every tile.** With u = m − σ: G ∈ {−1,0,1}; G = 1 ⇔ ℓ_1,ℓ_2 < u ≤ ℓ_1+ℓ_2 (forces r ≤ u−2);
     G = −1 ⇔ ℓ_1,ℓ_2 ≥ u, ℓ_1+ℓ_2 < m+u (forces r ≥ u). r: D → ℤ/m is a bijection, so −σ ≤ ΣG ≤ u−1. ∎
(BR) **Box reflection (any d).** For a box D with far corner κ, x ↦ κ − x swaps tops and bases of every column:
     slack_Tile(s) = base-slack(s − φ(κ)). Hence Tile-CL ⇔ Base-CL on boxes; with (B2), Tile-CL holds for all rectangles.
(BH) **Base-CL (hence Tile-CL) for every box tile in every dimension** (uses Hajós's theorem — CITED: G. Hajós, Math. Z. 47
     (1941); group form: a factorization of a finite abelian group into cyclic subsets {0,g,…,(k−1)g} has a subgroup
     factor; e.g. Szabó–Sands, "Factoring Groups into Subsets", 2009, Ch. on Hajós; statement not re-read this session).
     Proof: ΣG = (d−1)Σ_D C − Σ_a k_aΣ_{x_a=0}C. Let factor 1 be the subgroup nℤ/mℤ, n = m/k_1. Then Hermite's identity
     Σ_{i<k}⌊(Z+in)/m⌋ = ⌊Z/n⌋ and reduction of the other coordinates mod n give
        ΣG(σ) = ΣG'(σ mod n) − n⌊σ/n⌋ + Σ_{x'}⌊⟨σ + Σ_{a≥2}ℓ_a(x')⟩_m / n⌋   (n terms, each in [0, k_1−1]),
     with G' the carry function of the box tile (k_2..k_d; p mod n) of ℤ/n. Induct on d (d = 1: G ≡ 0). ∎ (E50 checks it.)
     Scope: a box Apéry tile forces S symmetric (w ↦ w_κ − w preserves Ap).
(TC) **τ-class identity (any d).** τ(x) = (t_1(x),…,t_d(x)) with t_a(x) the a-coordinate of top_a x; X_τ = τ^{-1}(τ);
     slack(s) = Σ_τ [Σ_{x∈X_τ} Ĝ(x) + |X_τ|·⟨s − φ(τ)⟩/m], Ĝ(x) = #{a : ℓ'_a(x) > ρ_x} − ⌈(Σ_aℓ'_a(x) − ρ_x)/m⌉,
     ℓ'_a = ⟨(t_a − x_a)p_a⟩, ρ_x = ⟨s − φ(x)⟩ (tauclass.py, 0 mismatches). For d = 2 Tile-CL would follow from the
     class-discrepancy inequality CDL (CONJ, checked m ≤ 11), which is no longer pursued (CL is false; e = 3 is known Wilf).

---------------------------------------------------------------------------------------------------
## Tile-TOP'' (lift-free, CONJ) — implication Tile-TOP'' ⇒ Wilf is LEAN-checked (lean/Wilf/TileTop.lean, 2026-10-17)
For a tile (D,p) (down-set, |D| = m, φ bijective), A = maximal cells (y + e_a ∉ D ∀a), π_s(y) = m − ⟨s − φ(y)⟩:
    (Tile-TOP'')  2·Σ_{y∈A} (d + |y|)·π_s(y) ≤ m((d+1)m + d − 1)   for every s ∈ ℤ/m.
Clean form (uses Σ_D π = m(m+1)/2): m + Σ_{y∈A}(|y| − 1)π(y) ≤ (d+1)·Σ_{z∈D∖A} π(z).
Proof of ⇒ Wilf: CH'; a non-maximal top t has M − w(t) ≥ n_b > m; a maximal top has M − w(t) ≥ ⟨s_M − φ(t)⟩ and tops
all d columns through it (total length d + |t|); total column length is dm per direction. ∎
LEAN: `TileTOPAt`, `TileTOP`, `wilf_of_tileTOPAt : TileTOPAt S.factDownSet S.genMod → c ≤ e·ℓ` (no S ≠ ℕ hypothesis),
`wilfConjecture_of_TileTOP : TileTOP → WilfConjecture`; axioms [propext, Classical.choice, Quot.sound], 0 sorry (verified
by the lead: lake build OK, PrintAxioms 124/124 standard).
Relations: Tile-CL ⇒ Tile-TOP'' ⇒ DR-CL ⇒ Wilf; Tile-TOP''(s_M) ⇒ TOP''. Wall form: Tile-TOP'' ⇔ Σ_yβ(y)W(y) ≤ π(0) − 1 +
(1/m)Σ_{y non-max}T(y)π(y), W(y) = ⌊(π(0) − 1 + ⟨y,p̂⟩)/m⌋ (Tile-CL is the same without the last term).
Status: CONJ; CHECKED all tiles d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7; 8008 adversarial Apéry tiles (E54, E55).
Proved special cases: boxes (all d; since d + |κ| = Σ k_a ≤ m + d − 1), d = 2 tiles for m ≥ 5 (crude bound).
FALSE strengthenings: R-TOP (rearranged), Box-TOP (|[0,y]| − 2 in place of |y| − 1), weight 2|y| − 2, semi-crude
(π(y) ↦ m on A; fails d=3 m=9: D = {000,001,002,010,011,020,100,101,200}, p = (1,3,4)).

---------------------------------------------------------------------------------------------------
## MaxCL (lift-free, CONJ, 2026-10-17) — MaxCL ⇒ Tile-TOP'' (PROVED, LEAN: tileTOPAt_of_maxCLAt) ⇒ Wilf (LEAN)
For a tile (D,p), A = maximal cells, N = D ∖ A, and every σ ∈ ℤ/m, with r = ⟨φ − σ⟩ (a bijection D → [0,m−1]):
    (MaxCL)  Σ_{y∈A} (|y| − 1)·r(y) ≤ (d+1)·Σ_{z∈N} r(z)   ⇔   Σ_{y∈A} (d + |y|)·r(y) ≤ (d+1)·m(m−1)/2.
Proof of MaxCL ⇒ Tile-TOP'': with r = π − 1 (r = ⟨φ − s − 1⟩), Tile-TOP'' ⇔ Σ_A T r ≤ (d+1)M' + Dep with
Dep = dm − Σ_A T(y) ≥ 0 (T(A) counts the cells of columns with maximal top, each direction ≤ m). ∎
Equivalence of the two forms: Σ_D r = M' and (d + |y|) = (|y| − 1) + (d+1). ∎
Wilf needs only σ = c mod m (r(x) = (w(x) − c) mod m).
Status: CONJ; CHECKED E58, E59 (all tiles d=2 m≤13, d=3 m≤10, d=4 m≤8, d=5 m≤7; 8008 adversarial tiles; 6800 random S, m ≤ 260).
Partial route (PROVED implication): Load Lemma (CONJ, E61) ⇒ MaxCL at σ = φ(0), via subadditivity r(u) + r(y−u) ≥ r(y)
when r(0) = 0. Open: general σ (bad-event bound m(B − P) ≤ (H + d + 1) r(0), unproved).

### Flat-MaxCL: MaxCL for tiles of height ≤ 2 — PROVED 2026-10-17; LEAN-checked (lean/Wilf/MaxCL.lean)
Statement. Let (D,p) be a tile with every cell of height |x| ≤ 2. Then MaxCL holds for every σ.
Notation: ρ_0 = r(0), ρ_a = r(e_a), ρ_ab = r(e_a+e_b); E = {ab : e_a+e_b ∈ D} (loops aa allowed);
deg(a) = #{b ≠ a : ab ∈ E} + 2[aa ∈ E] ≤ (d−1) + 2 = d+1. Cells: 0, the d unit vectors, the |E| height-2 cells, so
m = 1 + d + |E|. Every height-2 cell is maximal; e_a is maximal iff deg(a) = 0; 0 is non-maximal.
MaxCL reads Σ_{ab∈E} ρ_ab ≤ (d+1)(ρ_0 + Σ_{deg(a)≥1} ρ_a).
Proof. For ab ∈ E, ρ_a + ρ_b ≡ ρ_ab + ρ_0 (mod m) and both sides lie in [0, 2m−2], so ρ_a + ρ_b = ρ_ab + ρ_0 + mκ_ab
with κ_ab ∈ {−1,0,1}. Summing, Σ_E ρ_ab = Σ_a deg(a)ρ_a − |E|ρ_0 − mΣ_E κ_ab ≤ (d+1)Σ_{deg≥1}ρ_a − |E|ρ_0 + m·B,
B := #{ab : κ_ab = −1}. If κ_ab = −1 then ρ_ab = ρ_a + ρ_b + m − ρ_0 ≥ m − ρ_0, so the cells e_a+e_b with κ_ab = −1 have
pairwise distinct positions in [m − ρ_0, m − 1]; hence B ≤ ρ_0. Therefore Σ_E ρ_ab ≤ (d+1)Σ_{deg≥1}ρ_a + (m − |E|)ρ_0
= (d+1)Σ_{deg≥1}ρ_a + (d+1)ρ_0. ∎
Corollary (PROVED, via MaxCL ⇒ Tile-TOP'' ⇒ Wilf (LEAN)): Wilf holds for every numerical semigroup whose Apéry set
Ap(S,m) is contained in {0} ∪ P ∪ (P+P) (P = minimal generators other than m): every Apéry element has SOME factorization
of length ≤ 2, so the grlex factorization tile has height ≤ 2. This class contains reduction number ≤ 2 (max order of
Apéry elements ≤ 2), and is larger (an Apéry element may also lie in 3P). Checks: flat.py (400 S, all σ: proof inequalities deg ≤ d+1, B ≤ ρ_0 asserted).
Novelty: UNVERIFIED. Quick alphaXiv/web search found no such statement; but on 400 sampled height-2 S with q ≥ 4 Eliahou's
W_0 was always ≥ 0 and the class may be reachable by his method. 3 sampled height-2 S with 3e < m are outside every
condition implemented in src/known.py (e.g. ⟨33,69,70,71,74,80,81,82,85,87⟩, which misses Spirito #24 only by m).
Mechanism (the reusable part): **wrap events are confined to the top window [m − r(0), m−1]**, so they number ≤ r(0).
LEAN (2026-10-17, lean/Wilf/MaxCL.lean, 0 sorry, axioms propext/Classical.choice/Quot.sound; checked by lake build +
#print axioms by the lead): MaxCLAt (subtraction-free form Σ_A (d+|y|)⟨φ(y)−σ⟩ ≤ (d+1)Σ_D⟨φ−σ⟩);
tileTOPAt_of_maxCLAt; maxCLAt_of_height_le_two; wilf_of_factDownSet_height_le_two (lex tile);
wilf_of_apery_height_le_two: (∀ w ∈ Ap(S,m), ∃ x, wt x = w ∧ |x| ≤ 2) ⇒ c ≤ e·ℓ — the corollary exactly as stated above
(via a general IsFactTile reduction and the grlex factorization tile factDownSetG).

## Dependency graph
CH ⇒ Corollary H.  CH ⇒ Lemma A.  Lemma A + TOP'' ⇒ Wilf.  CH' + CL ⇒ Wilf (CL FALSE).  Tile-CL ⇒ CL ⇒ TOP''
(numerical; Tile-CL and CL FALSE, TOP'' survives E49).  MAIN ROUTE NOW: MaxCL ⇒ Tile-TOP'' ⇒ Wilf (LEAN) — prove MaxCL (Load Lemma + general σ). Also Lemma A + TOP'' ⇒ Wilf (LEAN).
SECONDARY: CL restricted to 3e < m, c > 3m, + LITERATURE #13, #21.
LEAN (kernel-checked, lean/Wilf/Chains.lean, axioms propext/choice/Quot.sound only, 0 sorry): CH, Corollary H,
Lemma A, TOP'' ⇒ Wilf (wilf_of_TOP2). lean/Wilf/Carry.lean (same axioms, 0 sorry): CH' (columnIdentity),
CL ⇒ Wilf (wilf_of_CL); Tile-CL stated as a Prop (TileCL), not proved.
