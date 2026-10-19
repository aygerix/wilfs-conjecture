# LITERATURE.md — what is PROVED about Wilf's conjecture (as of 2026-10-17; e = 4 corrections 2026-10-18)

Scope: bounded literature check (Phase 0). Goal: exact hypotheses of every known result, the
standard tools, the known-false strengthenings, and the precise uncovered region.

Notation (project convention, = CLAUDE.md): m multiplicity, e embedding dimension, c conductor,
g genus, n = ell = |L| = c - g, L = S ∩ [0,c), P primitives (minimal generators), t type,
PF pseudo-Frobenius set. Eliahou's constants: q = ceil(c/m) ("depth"), rho = qm - c ∈ [0,m),
I_j = [jm - rho, (j+1)m - rho), S_j = S ∩ I_j, P_j = P ∩ S_j, p_j = |P_j|, D_j = S_j \ P_j,
d_j = |D_j|. I_q = [c, c+m) ("threshold/critical interval"). X = Ap(S,m)\{0}, X_j = X ∩ S_j.
Wilf number W(S) = e·n - c.

Verification-status legend used below:
- READ = theorem statement read in the paper's own text (arXiv version unless noted; arXiv theorem
  numbers may differ from the journal version).
- SECONDARY = statement read in the text of another paper/survey that cites it; primary not opened.
- ABSTRACT = only abstract/slide text seen.
- RECOMPUTED = numerical example re-checked by us (scripts in session scratchpad, exact integer
  arithmetic; not saved to repo).
- UNVERIFIED = from memory or a search snippet only.

---------------------------------------------------------------------------------------------------

## 1. Table of proved results

| # | Result (Wilf holds / stated inequality) | Exact hypothesis | Authors, year, venue, id | Thm no. | Status |
|---|---|---|---|---|---|
| 1 | W(S) = 0 | e = 2 | Sylvester (1884) | — | SECONDARY (Delgado survey §2.3; Marashdeh L.2.1(vii)) |
| 2 | c ≤ (t+1)·n (FGH inequality) ⇒ Wilf whenever t ≤ e-1 | none (all S) | Fröberg–Gottlieb–Häggkvist, Semigroup Forum 35 (1987) 63–83 | Thm 20 | SECONDARY (Delgado Prop 3.1; Marashdeh eq.(1)); re-derived by us via identity in §2.6 |
| 3 | Wilf | e ≤ 3 (FGH: t ≤ 2 when e = 3, plus c ≥ 2n) | FGH 1987 (Th.11, Th.20); Dobbs–Matthews, Focus on Comm. Rings Research (2006) 193–202 | FGH Th.11/20; DM Cor 2.6, Th 2.11 | SECONDARY (Delgado Thm 3.2) |
| 4 | Wilf | S irreducible (symmetric or pseudo-symmetric) | Dobbs–Matthews 2006 | Prop 2.2 | SECONDARY |
| 5 | Wilf | S almost symmetric | Barucci, in "Commutative Algebra and its Applications", de Gruyter 2009, 49–60; alt. proof D'Anna–Moscariello, Math. Z. 304 (2023) Paper 35, arXiv:2208.14090 | DM Cor 4 | READ (D'Anna–Moscariello); Barucci SECONDARY |
| 6 | Wilf | S positioned (F - x + m ∈ S for all gaps x) | Branco–Faria–Rosales, Quaest. Math. 44 (2021) 679–691 | — | SECONDARY (D'Anna–Moscariello arXiv:2502.17989 §2) |
| 7 | Wilf | c ≤ 4n (equivalently c ≥ 4g/3) | Dobbs–Matthews 2006 Cor 2.7; DEF 2025 Prop 3.6 (proof: e ≥ 4 ⇒ en ≥ 4n ≥ c; e ≤ 3 by #3) | — | READ (DEF Prop 3.6) |
| 8 | Wilf | P = generalized arithmetic sequence ⟨m, hm+d, …, hm+ℓd⟩ | Sammartano, Semigroup Forum 85 (2012) 439–447 | Prop 20 | SECONDARY |
| 9 | t ≤ e-1 (hence Wilf) | e ≥ 3 and ∃ two distinct primitives p, p' with every sum of two primitives in (p+S) ∪ (p'+S) | Kunz–Waldi, J. Algebra 478 (2017) 397–409 | Cor 3.1 | SECONDARY (Delgado Prop 3.6) |
| 10 | Wilf; moreover W_0 ≥ rho | c ≤ 2m (q ≤ 2) | Kaplan, J. Pure Appl. Algebra 216 (2012) 1016–1032; short proof Eliahou JEMS 2018 | Kaplan Thm 24 or Prop 26 (sources conflict, see note A); Eliahou arXiv:1703.01761 Prop 3.13 | READ (Eliahou Prop 3.13); Kaplan SECONDARY |
| 11 | Wilf | 2g < 3m | Kaplan 2012 | Thm 24 (per Delgado–Kumar–Marion) | SECONDARY |
| 12 | Wilf | g < 2m - sqrt(2m) | Delgado–Kumar–Marion, arXiv:2501.04417 (v3, Oct 2026) | Cor 1.6 | READ |
| 13 | **W_0(S) ≥ 0, hence Wilf** | **c ≤ 3m (q ≤ 3)** | **Eliahou, JEMS 20 (2018) 2105–2129, arXiv:1703.01761** | **Thm 6.4 + Prop 6.2 ⇒ Cor 6.5** | READ |
| 14 | W_0 ≥ rho ≥ 0 | "true grading": S_i + S_j = S_{i+j} for all i + j ≤ q-1 | Eliahou JEMS 2018 | Thm 7.1 | READ |
| 15 | Wilf | q ≥ 4 and P ∩ L ⊆ [m, m + (m-rho)/(q-1)) | Eliahou JEMS 2018 | Cor 7.2 | READ |
| 16 | Wilf | gcd(L) ≥ 2 (⇔ subtree of S in the semigroup tree is infinite); includes inductive semigroups | Eliahou JEMS 2018 (via Sammartano) | Prop 7.6 | READ |
| 17 | Wilf | n = |L| ≤ 4 / ≤ 6 / ≤ 10 | DM 2006 Th 2.11 / Eliahou Prop 7.4 ("informally") / Eliahou Thm 7.5 (announced; W_0 ≥ rho except profile (1,0,1,0) where W_0 ≥ rho-1) | — | READ (Eliahou arXiv v1) |
| 18 | **W_0 ≥ 0, hence Wilf** | **n = |L| ≤ 12** (sharp for the W_0 method: |L| = 13 counterexample, see §4) | Eliahou–Marín-Aragón, Comm. Algebra 49 (2021) 2402–2422 | — | SECONDARY (Delgado Prop 3.15; DEF Thm 1.1(4)) |
| 19 | Wilf | 2e ≥ m; in particular m ≤ 8 | Sammartano 2012 | Th 18, Cor 19 | SECONDARY |
| 20 | Wilf | (2 + 1/q)·e ≥ m; also m - e ≤ 5; m ≤ 9 | Dhayni, Palest. J. Math. 7 (2018) 385–396 (thesis Angers 2017) | Th 4.12, Th 4.9, Cor 4.10 | SECONDARY |
| 21 | **Wilf** | **3e ≥ m** | **Eliahou, Electron. J. Combin. 27(2) (2020) P2.15, arXiv:1909.03699** | **Thm 1.1** | READ |
| 22 | **Wilf**; general part: e·n ≥ c - m + rho = (q-1)m | **4e ≥ m AND m \| c ("special")**; general part needs only 4e ≥ m | **Eliahou, "Divsets, numerical semigroups and Wilf's conjecture", Comm. Algebra 53 (2025) 2025–2048, HAL hal-04234167** | (DEF Thm 4.2 quotes it) | SECONDARY (DEF 2310.07742 Thm 4.2) + ABSTRACT (Eliahou IMNS 2024 abstract). Primary text not accessible (HAL bot-block) |
| 23 | Wilf | ρ' := ceil(m/e) > 3, m ≥ ρ'(3ρ'^2-ρ'-4)(3ρ'^2-ρ'-2)/(8(ρ'-2)), gcd(m, φ) = 1 where φ = product of primes dividing ρ' | Moscariello–Sammartano, Math. Z. 280 (2015) 47–53 | Th 1 | SECONDARY (Delgado Prop 3.22) |
| 24 | Wilf | e ≥ 10, second generator r > (c+m)/3, m ≤ (8/25)e^2 + e/5 - 5/4 (d ≤ 9 restriction removable via #21) | Spirito, J. Algebra Appl. 20 (2021) 2150197, arXiv:1710.09245 | Prop 4.6 | SECONDARY (Delgado Prop 3.25) |
| 25 | Wilf (computer + polyhedral) | m ≤ 18 | Bruns–García-Sánchez–O'Neill–Wilburne, IJAC 30 (2020) 861–882, arXiv:1903.04342 | Thm 4.3 | READ |
| 26 | Wilf | m ≤ 19 | Kliem–Stump, Discrete Comput. Geom. 67 (2022) 1147–1173 (face iterator applied to Kunz cone) | — | SECONDARY (DEF Thm 1.1(5), Marashdeh, Delgado–Kumar, Bacher all cite m ≤ 19) |
| 27 | Wilf | m - e ≤ 9 (BGOW Cor 4.5); m - e ≤ 12 (BGOW Cor 4.6 using 3e ≥ m); with m ≤ 19 + 3e ≥ m one gets m - e ≤ 13 | BGOW; last item our derivation: if m ≤ 19 use #26; if m ≥ 20 and e ≥ m-13 then 3e ≥ 3m-39 ≥ m (as 2m ≥ 40 > 39), use #21 | Cor 4.5, 4.6 | READ / derived |
| 28 | Wilf | S·dilation: S Wilf ⇒ D(S,a) = {0} ∪ (S\{0} + a) Wilf | Barucci–Strazzanti, Semigroup Forum 98 (2019) 251–260 | — | SECONDARY |
| 29 | Wilf | S = gluing k1·A ⊔ k2·B of two Wilf semigroups | Singh–Srinivasan, arXiv:2306.09876 | Thm 2.3 | READ |
| 30 | W ≥ 9 (although W_0 = -C(n,3)) | S = ⟨{m} ∪ A⟩_{4m}, A ⊂ [(3m+1)/2, (5m-1)/3], |A| = n-1, A a B_3-set mod m | Eliahou–Fromentin, Semigroup Forum 98 (2019) 285–298, arXiv:1710.03623 | Prop 3.3, Prop 4.1 | READ |
| 31 | W > 0 | Delgado's families S(p) = ⟨μ, γ, γ+1⟩_{pμ} (unbounded depth, negative W_0) | Delgado, Math. Z. 288 (2018) 595–627, arXiv:1608.01353 | Prop 6 | SECONDARY |
| 32 | W ≥ 0 | S h-regular, collision-free, and r ≥ ℓ (r = #right primitives, ℓ = |P∩L|) | Bacher, arXiv:2604.25051 (Apr 2026) | Thm 15 | READ |
| 33 | Wilf | q > 2 and |S ∩ (m,2m)| ≥ sqrt(qm/(q-2)); in particular |S ∩ (m,2m)| ≥ sqrt(2m) | Delgado–Kumar–Marion arXiv:2501.04417 | Thm 1.5 | READ |
| 34 | m ≤ (e-1)n + 1; c ≤ q·e·n; c ≤ e·n^2; t ≤ (e-2)(n-q+1) + 2 | all S | D'Anna–Moscariello, Math. Z. 304 (2023), arXiv:2208.14090 | Thm 2, Thm 1, Thm 3 | READ |
| 35 | Exact identity W = (e-t-1)n + σ + Θ; t ≤ Σ_{p∈P\{m}} ν(p-m) ≤ e-1+Ξ ≤ e-1+Θ; g + σ ≤ e-1 + t(n-1); W ≥ Θ - Σ_{i≤d} λ(f_i) when t ≥ e | all S | Marashdeh, arXiv:2608.12531 (Aug 2026, not refereed) | Prop 3.2, Thm 1.2/4.4, Cor 4.8, Prop 5.1 | READ |
| 36 | W = 0 ⇔ e = 2 or S = T_{m,k} | e ≥ t+1 (FGH range); separately for c ≤ 2m: W = 0 ⇔ S ∈ {T_{m,1}, T_{m,2}, ⟨3,4⟩} | Marashdeh 2026 | Thm 1.3 (=6.4), Thm 1.4 (=7.3) | READ |
| 37 | W = 0 only for known families | c ≤ 3m | Sammartano, in Eliahou JEMS Remark 6.6 | Rem 6.6 | READ |
| 38 | e(c) ≤ ν·ℓ(R/c) (ring analogue of Wilf) | R 1-dim, analytically unramified, CM, local, infinite residue field, almost Gorenstein | D'Anna–Moscariello, arXiv:2502.17989 | Thm 9 | READ |
| 39 | Computer: Wilf for g ≤ 50 / 60 / 65 / 66 / **100** | genus bound | Bras-Amorós SF 76 (2008) / Fromentin–Hivert Math. Comp. 85 (2016) / Bras-Amorós–Marín Rodríguez (MDAI 2021, arXiv:2307.10682) / Bras-Amorós Math. Comp. 93 (2024) / **Delgado–Eliahou–Fromentin, J. Algebra 664 (2025) 150–163, arXiv:2310.07742** | DEF Thm 3.5 | READ (DEF) |
| 40 | Computer: Wilf for special S (m \| c) with g ≤ 120 | m \| c, g ≤ 120 | DEF 2025 | Thm 4.4 | READ |
| 41 | Computer: Wilf for max primitive ≤ 60 | max P ≤ 60 | Delgado–Kumar, arXiv:2512.23891 | Thm 3 | READ |
| 42 | Computer, CONDITIONAL: all Eliahou semigroups (W_0 < 0) with c ≤ 320 listed (17,064, all Wilf) ⇒ Wilf for c ≤ 320 (⇒ g ≤ 160) **if** Bacher's Conjecture 20 holds | c ≤ 320 | Bacher arXiv:2604.25051 | §5 | READ (conditional) |
| 43 | Asymptotic: proportion of S of genus g that are Wilf → 1 | counting by genus | Zhai, Semigroup Forum 86 (2013) (prop. with c ≤ 3m → 1) + #13; alternatively Kaplan–Singhal, Enum. Comb. Appl. 3 (2023) Cor 7 (prop. with e ≥ m/2 → 1) + #19 | — | SECONDARY (DKM Prop 2.11, 2.12, Cor 2.16) |
| 44 | Asymptotic: proportion of S with Frobenius number F that are Wilf → 1 | counting by F | Backelin, Math. Scand. 66 (1990) Prop 2 (m ≈ F/2) + #13 | DKM Cor 2.17 | READ (in DKM) |
| 45 | Asymptotic: proportion of S with max primitive N that are Wilf → 1 | counting by max primitive | Delgado–Kumar–Marion | Thm 1.7 | READ |

Note A (Kaplan numbering): Delgado's survey says Kaplan Th. 24 = "c ≤ 2m ⇒ Wilf" and Prop. 26 = equality
case for m ≥ c/2; Delgado–Kumar–Marion say Th. 24 = "2g < 3m ⇒ Wilf" and Prop. 26 = depth ≤ 2;
Marashdeh says Th. 24 = c ≤ 2m and Prop. 26 = equality claim. The primary paper was not accessible in
this session (not on alphaXiv). Treat numbering as UNVERIFIED; both statements (c ≤ 2m; 2g < 3m) are
true and the c ≤ 2m case is independently re-proved in Eliahou Prop 3.13 (READ).

Note B (2406.13580, "Wilf's question in numerical semigroups S_3 revisited"): seen only as a search
hit; content not read (UNVERIFIED). e ≤ 3 is in any case settled (#3).

---------------------------------------------------------------------------------------------------

## 2. Precise statements of the key tools

### 2.1 Eliahou's partition and level structure (JEMS 2018, §3; READ)
- I_j = [jm - rho, (j+1)m - rho), S_j = S ∩ I_j; L = S_0 ⊔ … ⊔ S_{q-1}; S_0 = {0}; S_j = I_j for j ≥ q.
- m + S_j ⊆ S_{j+1}, so 1 = |S_0| ≤ |S_1| ≤ … ≤ |S_{q-1}| (Lemma 3.4).
- Weak grading (Prop 3.5): S_1 + S_j ⊆ S_{1+j} ∪ S_{2+j}; S_i + S_j ⊆ S_{i+j-1} ∪ S_{i+j} ∪ S_{i+j+1} (i,j ≥ 2).
  If rho = 0: S_i + S_j ⊆ S_{i+j} ∪ S_{i+j+1} (graph paper Prop 2.4).
- "Deficit" bound (Prop 3.6): |(S_i+S_j) ∩ S_{i+j-1}| ≤ rho and |(S_i+S_j) ∩ S_{i+j+1}| ≤ m - rho - 1.
- P ⊆ [m, c+m); D_1 = ∅; P_q = I_q \ D; S = ⟨P∩L⟩ ∪ [c,∞) (eq. (1)). Profile = (p_1,…,p_{q-1}).

### 2.2 W_0 (Eliahou number E(S)) and Apéry formulas (READ)
- Definition 3.10: **W_0(S) = |P∩L|·|L| - q·d_q + rho**, d_q = |D ∩ [c, c+m)|.
  Equivalent (Bacher): E = k·ℓ + q·r - c with k = |L|, ℓ = |P∩L|, r = p_q.
- Identity (2): **W(S) = p_q·(|L| - q) + W_0(S)**; since |L| ≥ q, W ≥ W_0 (Prop 3.11). Re-derived by us.
- With α_i = |X_i| (i ≤ q-1), α_q = |X_q \ P| (Prop 4.5): **d_q = Σ_{i=0}^{q} α_i**, **|L| = Σ_{i=0}^{q-1} (q-i)·α_i**.
- Graph-paper form (EJC 2020, Prop 2.9 / Cor 2.10): depth δ(x) defined by x + δ(x)m ∈ [c, c+m),
  τ(X) = Σ_{x∈X} δ(x). Then **|L| = q + τ(X)**, **m = e + |X ∩ D|**, **W = e·τ(X) - |X∩D|·q + rho**.
- Summand-closure (Lemma 2.12): any summand of a decomposable Apéry element is an Apéry element
  (X is a "downset"/divset in multiplicative notation).

### 2.3 q = 2 and q = 3 proofs (READ)
- q = 2 (Prop 3.13): k = p_1, |L| = 1+k, every element of D_2 is a sum of two elements of P_1, so
  d_2 ≤ k(k+1)/2 and W_0 - rho = k(1+k) - 2d_2 ≥ 0.
- q = 3: Prop 6.2 reduces to profile (k,0): with S' = ⟨P_1⟩_c, W_0(S) ≥ W_0(S') - rho (uses Prop 3.6 to
  cap |2P_2 ∩ I_3| by rho). Lemma 6.3 (Macaulay): if |2X_1 ∩ X_2| = C(x,2) (x ≥ 1 real) then
  |3X_1 ∩ X_3| ≤ C(x+1,3), proved by building the standard graded algebra R' = K[t^{a_i}u]/J with
  dim R'_i = |iX_1 ∩ X_i| for i = 2,3 and applying Macaulay's bound h_{i+1} ≤ h_i^{⟨i⟩}.
  Thm 6.4: W_0 - rho ≥ C(k,2) + (k-x-1)C(x,2) ≥ (k-x)C(x,2) ≥ 0.
- Condensed Macaulay used in Thm 7.1 (true grading): **q·h_q ≤ h_1(1 + h_1 + … + h_{q-1})** for a
  standard graded algebra (Eliahou Thm 5.11, statement quoted in proof of Thm 7.1).
- Equality for q = 3 (Rem 6.6): only profiles (1,0) and (1,1) with p_3 = 0.

### 2.4 The 3e ≥ m proof (EJC 2020, READ)
- Reduction (Lemma 5.2): if e ≥ m/3 and |L| ≥ 3q then e|L| ≥ mq ≥ c. General principle:
  **e ≥ m/k and |L| ≥ kq ⇒ Wilf.** So only τ(X) ≤ 2q-1 remains.
- Graph G(S): vertices/edges on X with edge {x,y} (loops allowed) iff x+y ∈ X; weight map
  E(G) → X∩D, {x,y} ↦ x+y is onto (Prop 3.11), so |X∩D| ≤ |E(G)|.
- Edges are "weak" if δ(x)+δ(y) = q-1 (possible only in ≤ rho residue classes: Prop 3.20 |X_0| ≤ rho),
  "normal" if ≥ q. Thm 3.24: **τ(X) ≥ (k(q-1) + ν)/2 + (n_V - k)**, k = vertex-maximal matching
  number vm(G), ν = normality number, n_V = |V(G)|.
- With τ(X) ≤ 2q-1 and q ≥ 4 ⇒ k ≤ 4 (Prop 5.3); finite case analysis on loopy graphs with vm ≤ 4.
- Divsets (Comm. Algebra 2025, ABSTRACT/SECONDARY): for 4e ≥ m and c ∈ mN it suffices to analyse
  divsets X with vm(X) ≤ 5.

### 2.5 Kunz polyhedron / Apéry posets (BGOW 2020, READ)
- Kunz coordinates x_i = (w_i - i)/m (w_i ∈ Ap(S,m), w_i ≡ i): integer points of P_m:
  x_i ≥ 1; x_i + x_j ≥ x_{i+j} (i+j < m); x_i + x_j + 1 ≥ x_{i+j-m} (i+j > m).
  g = Σ x_i; F = max_i (m x_i + i) - m (Lemma 3.2).
- Faces of the relaxed polyhedron P'_m ↔ Apéry posets (Thm 3.10); on a face interior e and t are
  constant: **e - 1 = #minimal elements, t = #maximal elements of the Apéry poset** (Cor 3.11).
- Wilf on a face interior ⇔ for each maximal f, the system "(4.1) m x_i + i ≤ m x_f + f ∀i" ∧
  "¬(4.2) m x_f + f - m + 1 ≤ e(m x_f + f - m - Σ x_i + 1)" has no integer point. For m ≤ 18 every
  such region is even rationally infeasible. **Conjecture 4.4: every region is empty for all m ⇒ Wilf.**
- "Wilf game" (Thm 6.5): a winning sequence of moves using face equalities certifies the face.
- Face counts explode: m = 18 has 2.8·10^10 faces (1.0·10^8 "bad"); m = 19 handled by Kliem–Stump.

### 2.6 Type-based tools (READ: Marashdeh 2026; D'Anna–Moscariello 2023)
- FGH: every gap x has some f ∈ PF with f - x ∈ S (hence f - x ∈ L), so the sets f - (L ∩ [0,f])
  cover the gaps: g ≤ Σ_f λ(f) ≤ t·n, i.e. c ≤ (t+1)n.
- Exact version (Marashdeh Prop 3.2): with λ(y) = |S ∩ [0,y]|, ν(x) = #{f ∈ PF : f - x ∈ S},
  σ = Σ_f |S ∩ (f, F]| = tn - Σ_f λ(f), Θ = Σ_{gaps x} (ν(x) - 1):
  **W = (e - t - 1)·n + σ + Θ**, σ, Θ ≥ 0. (Re-derived by us: g = Σ_f λ(f) - Θ.)
  Outside FGH range Wilf ⇔ σ + Θ ≥ (t+1-e)·n; proven: Θ ≥ t + 1 - e only.
- Apéry poset Q(S) = (Ap(S,m)\{0}, ≤_S): minimal elements = P \ {m}; maximal = PF + m.
- D'Anna–Moscariello injection (Thm 2): φ(ω) = {(ω - g_i, g_i) : ω - g_i ∈ S}, ω ∈ X, are nonempty
  and pairwise disjoint subsets of L × (P\{m}) ⇒ **m - 1 ≤ (e-1)·n**. (A charging argument giving
  Wilf up to the factor q: c ≤ qm ≤ q((e-1)n + 1) ≤ qen.)
- Trivial bounds: n ≥ q (0, m, …, (q-1)m ∈ L); c ≤ qm; hence **m·n ≥ c always** (equality iff
  S = T_{m,q}); c ≥ 2n (g ≥ c/2) with equality iff symmetric.

### 2.7 Verification machinery (READ: DEF 2025)
- Tree T: children of S are S \ {a}, a a right primitive (a > F). Along descendants (S ≠ O_m):
  m constant, e_l = |P∩L| nondecreasing, e drops by ≤ 1 per generation (Prop 3.2).
- Trimming: if e_l ≥ m/3, or e ≥ m/3 + (G - g), all descendants of genus ≤ G are Wilf (Cor 3.3, 3.4);
  if |L| ≥ G/3 then descendants of genus ≤ G are Wilf (Cor 3.7). T_100(3) has 4.55·10^15 nodes.

---------------------------------------------------------------------------------------------------

## 3. 2021–2026 developments (newer than Delgado's survey, arXiv:1902.03461 / INdAM 40, 2020)

1. Eliahou–Marín-Aragón (Comm. Algebra 2021): |L| ≤ 12 ⇒ W_0 ≥ 0 ⇒ Wilf. (SECONDARY)
2. Kliem–Stump (DCG 2022): multiplicity bound pushed to **m ≤ 19**. No later extension (m ≥ 20)
   found in this search (searched alphaXiv + web, 2020–2026). (SECONDARY)
3. D'Anna–Moscariello (Math. Z. 2023): first unconditional bounds c ≤ q e n, c ≤ e n^2, m ≤ (e-1)n+1. (READ)
4. Bras-Amorós–Marín Rodríguez (2021, g ≤ 65), Bras-Amorós (Math. Comp. 2024, g ≤ 66; seeds
   algorithm); **DEF (J. Algebra 2025): g ≤ 100; special case m | c: g ≤ 120.** n_g known to g = 75
   (DEF) / 76 (Bras-Amorós arXiv:2503.14664, per Delgado–Kumar). (READ DEF)
5. **Eliahou, Divsets (Comm. Algebra 2025): 4e ≥ m and m | c ⇒ Wilf; 4e ≥ m ⇒ e n ≥ (q-1)m.**
   The general 4e ≥ m case is NOT proved (only with m | c). (SECONDARY)
6. Singh–Srinivasan (arXiv 2023): gluing preserves Wilf. (READ)
7. D'Anna–Moscariello (arXiv:2502.17989, 2025): ring version e(c) ≤ ν ℓ(R/c) for almost Gorenstein
   1-dim rings; Question 8 asks it for all analytically unramified 1-dim CM local rings. (READ)
8. Delgado–Kumar–Marion (arXiv:2501.04417, v3 Oct 2026): |S∩(m,2m)| ≥ sqrt(2m) ⇒ Wilf;
   g < 2m - sqrt(2m) ⇒ Wilf; almost all by max primitive; **Problem 1.8: is every S with max primitive
   < 2m Wilf?** (open; such S can have e < m^{1/k}). Delgado–Kumar (arXiv:2512.23891): max primitive ≤ 60. (READ)
9. Bacher (arXiv:2604.25051, Apr 2026): structure theory of Eliahou semigroups via h-Farey intervals,
   B_h-sets; 17,064 Eliahou semigroups with c ≤ 320 (complete modulo Conjecture 20); all Wilf;
   Thm 15 (collision-free, r ≥ ℓ ⇒ W ≥ 0); Eliahou semigroups exist with rho/m arbitrarily close to 1. (READ)
10. Marashdeh (arXiv:2608.12531, Aug 2026, unrefereed): exact defect identity W = (e-t-1)n + σ + Θ;
    type bound t ≤ e - 1 + Ξ ≤ e - 1 + Θ; reduction of Wilf to a c-free, n-free inequality
    (Conj 5.2: t ≥ e ⇒ Θ ≥ Σ_{i=1}^{t+1-e} λ(f_i), f_1 < … < f_t the PF numbers; verified g ≤ 35,
    slack ≥ 2; Prop 5.3: Conj 5.2 ⇒ Wilf; Remark 5.4: Conj 5.2 is pointwise at least as strong as Wilf);
    equality case W = 0 settled on the FGH range; correction of Kaplan's equality classification
    for c ≤ 2m. Computation: every S with g ≤ 31 and e ≤ t has W ≥ 2 (attained by ⟨7,8,10,19⟩,
    ⟨7,9,10,15⟩: e = t = 4, n = 4, c = 14 — RECOMPUTED). (READ)

11. **kseth/wilf-e4 (GitHub, https://github.com/kseth/wilf-e4; repo created 2026-09-18, commits 2026-09-11 … 2026-09-24,
    HEAD caa574d; K. Sethuraman; no formalization).** Gives a complete computer-assisted proof of
    **Wilf for e = 4**. The main theorem (manuscript/introduction.tex:17–22) has no extra hypotheses. The proof was generated
    with AI models ("GPT-6 Astra", then "GPT-5.6 Sol via Codex", per manuscript/construction.tex).
    - Method: lex factorization ideal T (Zhai); identity m·W₄ = A·D₀ − m(m−1); mass-transport lemma; final-window
      projection inequality m·W ≥ m·Φ(T,Z) + E(Z); continuous κ-bounds plus box thickening; a case split by the unique
      full-support corner p; 7 finite lemmas checked by two implementations each (Python + C++).
    - Audit 2026-10-18 (subagent; report in session scratchpad, kseth_wilf_e4_report.md): analytic steps traced, no error
      found; strip lemma 2.7 reproduced independently. Lemmas 2.2–2.6, 2.8 and C.3.1/C.4.1 NOT verified, and repo code NOT run.
    - Status: treated as a real result. Our independent verification is PARTIAL: analytic chain traced, Lemma 2.7
      recomputed, no error found. Lemmas 2.2–2.6, 2.8 and C.3.1/C.4.1 are not yet checked by us. The lead spot-checked the
      theorem statement, dates, AI provenance and the absence of Lean files.
    - Also archived (not in the manuscript): a fixed-e finiteness claim (m ≥ B_e ⇒ W_e > 0, astronomically large B_e). UNCHECKED.
12. **Earlier e = 4 sources MISSED by the Phase-0 search (found by the 2026-10-18 audit):**
    - **Zhai, arXiv:1111.2779 (2011): Thm 1, e·n ≥ c − (e−2)(m−1)/2. This is our Corollary H.** Lemmas 1 and 3 are our CH′
      in exact form. Thm 2: for fixed e, all but finitely many S have n/c > 1/e − ε.
    - **Hellus–Rechenauer–Waldi, arXiv:1804.06141 (2018):**
      - Prop 2.3/2.5: the lex ideal is an initial ideal and tessellates.
      - **Prop 2.6(b) = our cylinder lemma (a)** (at most one full-support minimal excluded point, and it lies in Λ).
      - Remark 2.9: Wilf for e = 4 when the ideal is the double staircase B_n (a two-face family).
    - HRW, Semigroup Forum 97 (2018) 64–74 ("Note on a theorem of Eliahou"): the family ⟨n², n²+1, n²+n, n²+n+1⟩. NOT read.
    - HRW arXiv:2107.06752 (2021): n/c ≥ 2/(e² − e + 2). HRW arXiv:2106.07246: a weaker explicit bound. Abstracts only.
    - Chomicz arXiv:2604.25653 and 2609.04000 (2026): Apéry sets / type for e = 4; no Wilf statement. Abstracts only.
    (Statements in item 12 are as reported by the audit agent, which read Zhai and HRW 2018 in full; not re-read by the lead.)

No claimed full proof or counterexample of Wilf's conjecture (all e) was found in 2021–2026 sources examined. For e = 4 there
is a complete computer-assisted proof (item 11), which we have only partly verified. Epoch AI (2026) still lists the conjecture as unsolved (§5).

13. **GitHub sweep 2026-10-18.** Searched with `gh search repos`: "wilf conjecture", "wilf's conjecture", "wilf numerical
    semigroup", "numerical semigroup(s)", "Apery set", "wilf inequality", "wilf multiplicity" (repos updated since 2025-06).
    Wilf-relevant results (README level only; CLAIMED, UNCHECKED):
    - **JC8267/wilf-multiplicity-23** (J. Collier, manuscript dated 2026-10-05, AI-assisted, arXiv submission prepared):
      computer-assisted proof of **Wilf for m ≤ 23**, extending Kliem–Stump m ≤ 19. Uses a "path certificate" and the shape
      inequality W ≥ PC ≥ R0 − D, with one exceptional shape at (d, m) = (3, 21). It says it does not rely on "an
      unrestricted e = 4 claim".
    - alhafs-hue/wilf-verification (2026-08-12): verification code for Marashdeh's type bound / reduction (item 10).
    - wytyKen/ai4math-width-bounds (2026-10-06): width bounds for four-generated semigroups and Lean formalization of
      three-variable lex ideals (Tor/Betti). Not a Wilf statement.
    - Not Wilf: benkeene/semigroup-betti (Lean, Betti numbers e = 4), stksk310/* (Lean, nearly Gorenstein e = 4),
      Flaman55/NumericalSemigroups (Huang's quadratic form), michaeliu4/bras-amoros-monotonicity, AxiomMath/fel-polynomial.
    - aygerix/wilfs-conjecture is THIS project's own remote (origin); its last pushed commit is 73b2c86 (2026-10-18 06:53Z).
    Observation: many AI-assisted numerical-semigroup projects have appeared on GitHub since Sept 2026. Re-run this sweep
    before every change of sub-target.

14. **Literature check for the general-e final-window (FW) sub-target, 2026-10-18.**
    - kseth manuscript/extensions.tex: for e > 4 it states only the moment identity mW_e = A·D_e − ((e−2)/2)m(m−1), a
      conditional mesh-transfer principle, and an obstruction to the three-horn decomposition (⟨9,19,12,20,15⟩). It does
      NOT state the final-window inequality (p:6) for general e. Neither our sharpened FWx/FWy nor the c > 3m conjecture
      appears there.
    - alphaXiv (recency-ranked: Wilf, Apéry, embedding dimension): nothing new for e ≥ 5 or on line/residue criteria
      beyond items already listed. Newest hits: 2608.12531 (item 10) and 2609.18136 / 2609.39218 (determinantal
      presentations, not Wilf).
    - GitHub: repo searches "wilf semigroup proof", "wilf conjecture lean", "numerical semigroup wilf five generators",
      "apery wilf" found nothing new. Lean code search "Wilf" found only Fine–Wilf, Stanley–Wilf and Calkin–Wilf.
    - The exact identity is Zhai's Lemma 3 (KNOWN). The FW inequality for general e is an immediate generalization of
      kseth (p:6). FWx/FWy and "FWx for c > 3m" were not found anywhere searched (novelty still not claimed).

15. **Sethuraman's foundational geometry, read 2026-10-18 by the lead (manuscript/proof.tex §2.1, 2.5, 2.7, 2.9, 2.10).**
    Facts relevant to our tile route:
    - Collision rules (= HRW Prop 2.6): a corner and its representative have disjoint supports; two distinct corners
      sharing a positive coordinate have distinct residues. Hence there is ≤ 1 full-support corner p, with
      representative 0. (Our cylinder lemma (a) and (b).)
    - (p:11) T = U ∖ (p + ℕ³), with U a finite no-full-corner ideal (= our cone class: U = Cyl ∈ 𝒞, p = q*).
    - Thm A.1.1: every finite no-full-corner ideal is a central box [0, z] plus at most three nonincreasing horns. This is
      a structure theorem for our class 𝒞, proved via a chordal compatibility graph.
    - §2.7, p = (1,1,1): each plane has ≤ 1 mixed corner, with representative h_k e_k. (Our Wall Lemma with q* = (1,1,1).)
    - **(p:19)** each ij-plane has ≤ (p_i − 1) + (p_j − 1) + p_k = |p| − 2 mixed corners. Corners with q_i < p_i are an
      antichain with distinct i-coordinates; corners ≥ (p_i, p_j) are bounded by collision with the k-axis.
      (Our Wall Lemma plus the antichain count; matches our "refined Wall count".)
    - **(p:20)** for every residue-bijective lower ideal (any 3-D lattice tile), |F_i ∩ F_j| ≤ 2 n_k, where
      F_i = {x : x + e_i ∉ T} and n_k = L_k. Proof: the h_s − 1 inner corners of each k-slice are excluded points whose
      representatives lie on the k-axis, distinct for distinct corners. So Σ_s (h_s − 1) ≤ L_k. Consequence: t ≤ 2 min_k L_k.
      **NEW TO US; a reusable tool.**
    - (p:17) for p a permutation of (2,1,1), |T| ≤ 2r² − r + 3.
    - Not used by Sethuraman: forest/elimination arguments, tripod/qO/qU graphs, LCL/PW, the height criterion HT. Our
      cone-tile route remains a different mechanism.

**Search-scope failure (2026-10-18).** The Phase-0 search covered journals, arXiv/alphaXiv and the web, but NOT GitHub. It
missed item 11 (public since 2026-09-18) and the e = 4 papers in item 12. STATE.md then called e = 4 "open in the
literature" from 2026-10-17 to 2026-10-18, and nights 13–17 were spent on it. Rule from now on: before any sub-target
becomes the focus, search GitHub + arXiv (newest first) + the reference page for that exact statement, and record the
scope and date here.

16. **Search for Wilf with e = 5, and for m | c (2026-10-18, afternoon).**
    - Scope: alphaXiv discovery, newest first ("Wilf's conjecture", "embedding dimension", "numerical semigroup"; results
      through 2026-09-30), plus web searches including site:github.com.
    - e = 5: no proof found. The newest relevant items are e = 4 papers (2604.25653, 2609.04000, kseth/wilf-e4) and the
      type bound and reduction 2608.12531.
    - github.com/michelfgaspar-spec/Wilfs13: an archival manuscript with a Lean proof of Wilf for |L| = 13 left
      elements. This extends Eliahou–Marín-Aragón (#18, |L| ≤ 12). Not read in detail; status unverified by us.
    - The-Last-Math-Competition PRs #169/#714: claimed disproofs of a "Wilf surplus/Frobenius ratio → 0" conjecture for
      e = 3. That is a different statement, not Wilf itself. Unverified.
    - m | c: no result beyond #22 (Eliahou divsets: 4e ≥ m and m | c) was found in this search. So Wilf for all S with
      m | c is treated as open.

---------------------------------------------------------------------------------------------------

## 4. Known-FALSE strengthenings / generalizations (and open stronger conjectures)

FALSE:
- **(F1) "W_0(S) ≥ 0 for all S" (Eliahou number nonnegative) — FALSE.** Fromentin (exhaustive, g ≤ 60):
  exactly 5 exceptions, all c = 4m, W_0 = -1: ⟨14,22,23⟩_56 (g=43), ⟨16,25,26⟩_64 (g=51),
  ⟨17,26,28⟩_68, ⟨17,27,28⟩_68 (g=55), ⟨18,28,29⟩_72 (g=59). Smallest: **⟨14,22,23⟩_56** =
  ⟨14,22,23,57,61,62,63⟩: m=14, c=56, g=43, n=13, e=7, q=4, rho=0, W_0=-1, W=35, t=8 (RECOMPUTED).
  W_0 takes every integer value infinitely often (Delgado 2018); W_0 = -C(n,3) with q = 4,
  |P∩L| = n (Eliahou–Fromentin Prop 3.3); unbounded depth (Delgado S(p)); rho/m → 1 (Bacher Prop 18).
  Second example checked: ⟨30,44,48,49⟩_118: W_0 = -2, W = 148 (RECOMPUTED).
- **(F2) "|L| ≤ N ⇒ W_0 ≥ 0" fails for N = 13** (same example, |L| = 13); 12 is optimal for the W_0 route.
- **(F3) "t ≤ e - 1" (FGH range covers everything) — FALSE**: type is unbounded for e ≥ 4 (Backelin's
  example in FGH p.75). Explicit: ⟨213,216,226,227⟩ has e = 4, t = 14 (Almirón–Moyano-Fernández
  Rem 2.3; RECOMPUTED: m=213, F=3419, t=14). FGH's claimed type formula t = 2n+3 for their family
  Γ_{s,n} = ⟨s, s+3, s+3n+1, s+3n+2⟩ is wrong (Stamate; same remark).
- **(F4) Kaplan's equality classification for c ≤ 2m (only ⟨m,…,2m-1⟩ and ⟨3,4⟩) — claimed
  incomplete by Marashdeh (Thm 7.3/Rem 7.4)**: T_{m,2} = ⟨m, 2m+1, …, 3m-1⟩ also has W = 0 and c = 2m.
  Smallest ⟨3,7,8⟩: c = 6, n = 2, e = 3, W = 0 (RECOMPUTED). Kaplan's original text not read.
- **(F5) Monotonicity "adding a left generator does not lower E"**: false, ⟨23,39,40,42⟩_77 has E = 15,
  ⟨23,39,40,42,54⟩_77 has E = 14 (Bacher; RECOMPUTED). Also "E + |L| - q ≥ 0" (would give Wilf with
  ≥ 1 right primitive) fails in general: a uniform collision-free semigroup with h = 3, a/b = 5/3,
  ℓ = 8 has E + k - q = -7 (Bacher §3.3; no explicit generators given; not recomputed).
- **(F6) Natural Wilf for semimodules, W_Δ(e(Δ)) ≥ 0 — FALSE** (Almirón–Moyano-Fernández,
  arXiv:2012.01358 §4.2). Our recomputation with Γ = ⟨6,8,35⟩, Δ = Γ ∪ (10 + Γ): e(Δ) = 2, c(Δ) = 40,
  δ(Δ) = 19, 2·19 - 40 = -2 < 0. (Their Table 2 appears to use the opposite sign convention; under
  either convention negative values occur.)
- **(F7) Pure degree/density heuristics**: W(S) ≥ ρ-type statements fail (Eliahou Thm 7.5: profile
  (1,0,1,0) has W_0 = rho - 1, e.g. ⟨5,13⟩_22: W_0 = 2, rho = 3 — RECOMPUTED).

OPEN stronger statements (true so far, each implies or refines Wilf):
- Moscariello–Sammartano Question 8 / Delgado Problem 2.5 ("Frögohämosa"): W = 0 ⇔ e = 2 or S = T_{m,k}.
  Proved for c ≤ 3m, for e ≥ t+1 (Marashdeh), computationally for m ≤ 15 (BGOW) and g ≤ 31 (Marashdeh).
- BGOW Conjecture 4.4 (all Kunz regions empty; rationally infeasible observed for m ≤ 18).
- Eliahou–Fromentin Conj 4.2: q = 4 and |P∩L| = n ⇒ W_0 ≥ -C(n,3).
- Marashdeh Conj 4.9: t ≤ e - 1 + σ (sharp, g ≤ 35); Conj 5.2 (⇒ Wilf); Conj 7.6.
- Bacher Conj 20 (pruning) and belief that no h-regular collision-free counterexample exists.
- Almirón–Moyano-Fernández "Bound conjecture" min_g W(g) ≥ -W_Γ(e) (⇒ Wilf).
- Delgado–Kumar–Marion Problem 1.8 (max primitive < 2m ⇒ Wilf?).
- Ring version (D'Anna–Moscariello Question 8); Generalized Wilf for generalized numerical semigroups
  (Cisto–DiPasquale–Failla–Flores–Peterson–Utano, Semigroup Forum 101 (2020), arXiv:1909.13120);
  Extended Wilf for C-semigroups (García-García–Marín-Aragón–Vigneron-Tenorio, Semigroup Forum 96
  (2018)); Unipotent Wilf (Can–Sakran arXiv:2306.05530). No counterexample to these found in this
  search (search was not exhaustive; status UNVERIFIED beyond the sources read).

---------------------------------------------------------------------------------------------------

## 5. Epoch AI page (https://epoch.ai/frontiermath/open-problems/numerical-semigroups), fetched 2026-10-17

- Title "A counterexample to Wilf's Conjecture"; FrontierMath: Open Problems; tags Unsolved, Number
  theory, Construction-Finite, Counterexample. No difficulty number shown.
- Statement: (F+1-G)/(F+1) ≥ 1/E, i.e. e·n ≥ c with n = c - g, c = F + 1.
- What counts: a single explicit S with e·n < c. Generators positive, gcd 1, smallest ≥ 2, exact
  arithmetic. Certificate: JSON {"generators": [...]}; if m ≤ 200000 the verifier builds S directly;
  for larger m the submission must include the Apéry set and, for each Apéry element, a predecessor
  chain through submitted generators back to 0. No other size limit stated. Example given:
  ⟨5,7,9⟩: g = 8, F = 13, c = 14, m = 5, e = 3, n = 6.
- It asks only for a counterexample (not a proof); cites no partial results.

---------------------------------------------------------------------------------------------------

## 6. Dependency map and exact gaps

Proved regions (any one suffices):
- q ≤ 3 (c ≤ 3m)  [W_0 ≥ 0 there]
- e ≥ m/3 (3e ≥ m); e ≥ m/4 only together with m | c
- m ≤ 19; m - e ≤ 13 (derived from m ≤ 19 + 3e ≥ m)
- e ≤ 3; t ≤ e - 1 (includes symmetric, pseudo-symmetric, MED); almost symmetric; positioned
- n ≤ 12; c ≤ 4n; g ≤ 100; (m | c and g ≤ 120); max P ≤ 60; g < 2m - sqrt(2m)
- |S ∩ (m,2m)| ≥ sqrt(qm/(q-2)); gcd(L) ≥ 2; true grading up to level q-1;
  P∩L ⊆ [m, m+(m-rho)/(q-1)) with q ≥ 4; Moscariello–Sammartano arithmetic condition;
  Spirito large-ratio condition; gluings/dilations of Wilf semigroups.

Hence a counterexample S must satisfy simultaneously (all READ/SECONDARY above):
  **q ≥ 4 (c > 3m), m ≥ 20, 4 ≤ e < m/3 (and e < m/4 if m | c), t ≥ e, n ≥ 13, c > 4n
  (i.e. g > 3c/4), g ≥ 101, gcd(L) = 1, |S ∩ (m,2m)| < sqrt(qm/(q-2)) ≤ sqrt(2m),
  g ≥ 2m - sqrt(2m), not almost symmetric, max primitive ≥ 61.**
  Also by Marashdeh's identity: σ + Θ < (t+1-e)·n. From n ≥ q and e·n < c ≤ qm: q ≤ n < qm/e,
  so a counterexample has fewer than m/e left elements per "level" on average (|L|/q < m/e).

Exact gaps (what a universal proof must supply):
- G1 (depth): no argument for general q ≥ 4. W_0 ≥ 0 FAILS at q = 4, so any proof for q ≥ 4 must use
  the right primitives p_q (term p_q(|L|-q)) — W_0 alone is insufficient. Lemma 5.2-type reductions
  show the hard case for e ≈ m/k is |L| < kq, i.e. very "thin" L (few left elements per level).
- G2 (e/m ratio): proven for e/m ≥ 1/3 (and ≥ 1/4 when m | c). Gap: e < m/3. The graph/divset
  method's case analysis grows with vm (≤ 4 for 1/3, ≤ 5 for 1/4 special); no uniform mechanism.
- G3 (type): FGH covers t < e; outside, only Θ ≥ t+1-e is known, short of the needed (t+1-e)·n by a
  factor ~n/2 (Marashdeh §9).
- G4 (charging): D'Anna–Moscariello's injection gives m - 1 ≤ (e-1)n (sharp form loses factor q
  relative to Wilf). A charging argument that gains the factor q (e.g. injecting X × levels into
  L × P) is exactly the missing ingredient for a direct proof.
- G5 (Kunz): fixed-m reduction is finite per m but face counts explode (m = 18: 2.8·10^10 faces);
  no structural proof of Conj 4.4 for general m.

---------------------------------------------------------------------------------------------------

## 7. Sources consulted / not accessible
Read (text): arXiv 1703.01761 (Eliahou JEMS), 1909.03699 (Eliahou EJC), 1902.03461 (Delgado survey),
1903.04342 (BGOW), 1710.03623 (Eliahou–Fromentin), 2310.07742 (DEF genus 100), 2208.14090 and
2502.17989 (D'Anna–Moscariello), 2501.04417 (DKM), 2512.23891 (Delgado–Kumar), 2604.25051 (Bacher),
2608.12531 (Marashdeh), 2012.01358 (Almirón–Moyano-Fernández), 2306.05530 (Can–Sakran),
2306.09876 (Singh–Srinivasan); Eliahou IMNS 2024 abstract (pdf); Epoch AI page.
Not accessed: Kaplan JPAA 2012 (not indexed), Eliahou Divsets full text (HAL bot-blocked),
Eliahou–Marín-Aragón 2021, Kliem–Stump 2022, Sammartano 2012, Dhayni 2018, Spirito 2021,
Moscariello–Sammartano 2015, FGH 1987, Dobbs–Matthews 2006, Zhai 2013, Kaplan–Singhal 2023,
Barucci 2009, Bras-Amorós papers, Cisto et al. 2020, García-García et al. 2018, arXiv:2406.13580.
Statements from these are SECONDARY (quoted from papers that were read) or UNVERIFIED as marked.

### Night-12 additions (2026-10-18)
- Nakamura, "Hilbert schemes of abelian group orbits", J. Algebraic Geom. 10 (2001): our tiles = Nakamura's G-graphs for
  G = ℤ/m ⊂ GL(d) diagonal with weights p; for abelian G ⊂ GL(3) the cones σ(Γ) form a fan (normalization of G-Hilb).
  SECONDARY (via web summary). Craw–Reid / Craw–Maclagan–Thomas for SL(3) structure. Not read in full.
- Gomory group problem: coherent tiles = solution sets of min w·x, Σ x_a p_a ≡ g (mod m) (standard; our observation
  that all tiles d ≤ 3, m ≤ 9 are coherent is OURS, computational).
- Marashdeh 2608.12531 re-checked: Θ(S) = Σ_{gaps}(ν_S(x) − 1); Prop 5.1 W ≥ Θ − Σ_{i≤t+1−e} λ_S(f_i) for t ≥ e;
  Conj 5.2 Θ ≥ Σ λ_S(f_i) (open, checked g ≤ 35). Different mechanism from our τ-criterion.
- 2604.25653 (Apéry sets for e = 4, geometric procedure), 2609.04000 (type vs minimal presentations, e = 4): found by
  discovery search, not read; no Wilf statement in abstracts.
- τ-criterion novelty search (limited): nothing equivalent found.

### 17. Dated search, 2026-10-18 (night): column-height and residue criteria (HCR); e = 5
Scope: alphaXiv discover (newest first; keywords Wilf conjecture, numerical semigroup, Apéry set, embedding dimension);
web search for an e = 5 proof (2026); web search for GitHub or Lean repositories.
- Nothing found that combines Zhai's column identity with heights of column tops and distinctness of residues (HCR,
  HCR+, HCR++). Novelty is UNVERIFIED beyond this scope.
- No proof of Wilf for e = 5 found.
- New references:
  - M. F. Marashdeh, arXiv:2608.12531 (2026-08). Type bound t ≤ e − 1 + Ξ(S), genus bound g ≤ e − 1 + t(n − 1), and a
    reduction of Wilf to an inequality free of c and n. It also corrects Kaplan's c ≤ 2m equality list. Its survey
    credits Kliem–Stump with extending BGOW to **m ≤ 19**, so our small range is m ≤ 19.
  - arXiv:2604.25653 (2026-04): a geometric procedure for Apéry sets in e = 4. It is not a Wilf proof.
  - preprints202604.0551 (prereview, 2026): a first-Kunz-layer bound claimed to imply Wilf under an inequality. Not
    checked.

18. **Search before making "HCR / the height functional for 4-D tiles (e = 5)" the focus, 2026-10-18 (late night).**
    - Web, extended: "Wilf conjecture numerical semigroups embedding dimension five". Found only known items:
      Sammartano 1111.1863 (2e ≥ m, m ≤ 8), Dobbs–Matthews 1610.08726 (m − e = 5), Marashdeh 2608.12531 (#35),
      Singh–Srinivasan (gluing, #29), DEF genus 100 (#39).
    - Web: Wilf with reduction number, or with Apéry elements that are sums of two generators. Nothing.
    - GitHub, `gh search repos` "wilf conjecture" and "numerical semigroup", sorted by update. New since #13:
      Flaman55/NumericalSemigroups (Huang's quadratic form, not Wilf); Aurantium-47 (shifted semigroups, endpoint
      residues); methodtrace/2026-numerical-semigroup-mass (no README).
    - Result: no e = 5 proof, no height or column criterion, and no statement that shape-only criteria fail for large e.
19. **Search before making Down-set Wilf (GW) the focus (2026-10-18, late night).**
    - Queries (web, arXiv-weighted):
      - Wilf + monomial ideal / standard monomials / complete residue system / non-minimal Apéry set;
      - Wilf + order ideal / lattice tile / fundamental domain (2025–2026);
      - Wilf + Apéry set of the largest generator.
    - Hits: only items already listed. These are:
      - the generalized numerical semigroups of Cisto et al. (1909.13120);
      - the semimodule extension (2012.01358, false, F6);
      - BGOW (1903.04342), the graph approach (1909.03699), DKM (2501.04417), Marashdeh (2608.12531), and Eliahou's
        Macaulay paper (1703.01761).
    - None states Wilf for arbitrary residue-complete down-sets (non-minimal factorization domains), nor the
      lattice-tile/dual-lattice form.
    - Background fact used: Selmer's formulas for Ap(T, t) hold for every t ∈ T, so Wilf has the same Apéry form for every
      element (standard).
    - Absence of hits is not proof of novelty. GitHub was not searched in this pass.

20. **Search before making the prefix/window family (PGW, WW_i) the focus (2026-10-19, early).**
    - Queries:
      - web: Wilf + gaps below km + elements in [c − km, c) + Apéry set of km;
      - web: Wilf + "for every k" + windows below the conductor;
      - arXiv API: abs:Wilf AND abs:semigroup, newest first (through 2609.32078, submitted 2026-09-25);
      - GitHub: repositories "wilf conjecture", "numerical semigroups", "wilf inequality", "kunz polyhedron".
    - GitHub: Delgado's bibliography repository ManuelAFDelgado/NumericalS-bib, last commit 2026-10-12, read as data.
      Its numericals.bib and preprints.bib were scanned for Wilf titles.
    - The semimodule paper 2012.01358 was read (ar5iv). Its "Wilf function" is W_Δ(k) = k·δ(Δ) − c(Δ): a family in the
      multiplier k, not in the window. It does not state WW_i.
    - No source found states WW_i, P_i, or any window/prefix interpolation between WW_1 and Wilf. WW_1 itself is
      elementary (GW-15) and may be folklore.
    - New items seen, NOT READ (metadata/abstract only):
      - Chatterjee–Narula, "A note on Wilf's Conjecture", Semigroup Forum 113 (2026) 387–396,
        doi 10.1007/s00233-026-10640-8. Springer is behind a login; no arXiv version found.
      - Gaspar, arXiv:2609.32078 (2026-09-25): forcing results plus Wilf for semigroups with 13 left elements.
        Unverified.
      - Hellus–Hübl–Rechenauer, arXiv:2604.21948: semigroups with largest generator 2g + 1.
      - Ojeda–Rosales, arXiv:2605.14775: semigroups with a fixed quotient.
      - Almirón–Moyano-Fernández, arXiv:2104.03793 (Quaest. Math. 46 (2023)): Eliahou number, Wilf function,
        concentration.
    - Absence of hits is not proof of novelty.
21. **Search for the PF-count criterion GW-18 (2026-10-19, night).** Query: Wilf + number of pseudo-Frobenius numbers
    above the multiplicity / above km + embedding dimension (web, extended).
    - Found: e > t ⇒ Wilf (FGH 1987, as quoted in BGOW 1903.04342); Sammartano 2e ≥ m; Dhayni (2 + 1/q)e ≥ m;
      Marashdeh 2608.12531 (smallest t + 1 − e PF numbers, Prop 5.1).
    - Not found: any criterion that counts only PF numbers ≥ 2m (GW-18) or ≥ m.
    - Absence of hits is not proof of novelty.
22. **Search before making "Wilf for c ≤ 4m (K = 4 band counting)" the focus (2026-10-18).**
    - Queries:
      - web, extended: Wilf + conductor c ≤ 4m / depth 4 / q = 4;
      - web: GitHub + Lean + "4m";
      - `gh search repos` "wilf semigroup" and "numerical semigroups wilf" (no public hits).
    - Found:
      - Eliahou JEMS 2018 (c ≤ 3m, via Macaulay; W_0 counterexamples sit at c = 4m);
      - Eliahou divsets (m | c, 4e ≥ m);
      - DEF g ≤ 100 (computer);
      - preprints202604.0551 (first Kunz layer, item 19);
      - Marashdeh 2608.12531 (item 10).
    - Not found: any proof of Wilf for all S with c ≤ 4m (3m < c ≤ 4m open as far as searched).
    - Absence of hits is not proof of novelty.

## Search 2026-10-19 (scope: GW-25, Wilf for 3m < c ≤ 4m with generators in [(c−m)/2, c−2m))
- Queries: web (arXiv/preprints) "Wilf conjecture conductor 4m Apéry", "Wilf second generator large Apéry length",
  2026 items. Found: Spirito 1710.09245 (#24; needs n_1 > (c+m)/3, e ≥ 10, m ≤ (8/25)e² + …); Eliahou–Fromentin
  1710.03623 (#30; the c = 4m B₃ near-miss family, W ≥ 9 proved for it); Eliahou divsets (#22; m | c, 4e ≥ m);
  preprints.org 202604.0551 (abstract only: m | c and e(3η+4) ≥ 4m with η = #S∩(m,2m); not read).
- None states the GW-25 class result. Spirito's hypothesis n_1 > (c+m)/3 implies Ap = A_{≤2} (GW-25a with k = 2).
  For c ≤ 5m, the GW-25 hypothesis n_1 ≥ (c−m)/2 is the weaker one, but GW-25 also assumes pure A and 3m < c ≤ 4m.
  GW-25 covers e of every size, whereas Spirito's needs m ≤ (8/25)e² + …, which fails here since m can be ≈ e³/6.
- The arc lemma GW-25a is elementary and may be folklore. No priority is claimed for it.

