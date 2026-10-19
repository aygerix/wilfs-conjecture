**LEAN-P2 — GW-16 and GW-17: kernel-checked, with proof audit**

Both requested statements are proved in `Wilf/Window2.lean`, imported by `Wilf.lean:15`.
The final `lake build` and `scripts/PrintAxioms.lean` run succeeded on **fejer** with zero errors
and zero warnings. All new audited results depend only on
`[propext, Classical.choice, Quot.sound]`. There is no `sorry`, `native_decide` invocation, or new
axiom declaration. No Lean/lake command ran on the laptop, and no commit was made.

The exact requested GW-16 statement is retained. A separately named strengthening proves that
the active-weight condition can be relaxed from `m < n a` to **`m ≤ n a`**. GW-17 is proved for
every library `NumericalSemigroup`, including `S = nat`. Both required translation equalities
are proved for every window length `K*m`, not only `K = 2`.

**Exact statements and locations**

All declarations below are in namespace `NumericalSemigroup.Window2`; `open Finset` is in
effect. `IsDownSetFin` is the existing pointwise down-set predicate from `Wilf/Carry.lean:38`.
There is no residue, nonemptiness, positive-dimension, or all-unit-vectors hypothesis.

GW-16, [Wilf/Window2.lean:407](Wilf/Window2.lean#L407):

```lean
theorem depth_two (D : Finset (Fin d → ℕ)) (hD : IsDownSetFin D) (n : Fin d → ℕ)
    (hn : ∀ a, Pi.single a 1 ∈ D → D.card < n a) :
    (∑ x ∈ D, min 2 ((∑ a, x a * n a) / D.card)) ≤
      d * ∑ x ∈ D, min 2 ((D.sup (fun y => ∑ a, y a * n a) -
        (∑ a, x a * n a)) / D.card)
```

Here `d : ℕ` is implicit. Thus `m = D.card`, `v x = ∑ a, x a * n a`, and `M = D.sup v`
are literally the requested definitions. `Finset.sup` on the empty finset is zero, and all
divisions and subtractions in this statement have type `ℕ`.

The strengthening, [Wilf/Window2.lean:393](Wilf/Window2.lean#L393), has the same conclusion and
the hypothesis

```lean
theorem depth_two_of_le (D : Finset (Fin d → ℕ)) (hD : IsDownSetFin D) (n : Fin d → ℕ)
    (hn : ∀ a, Pi.single a 1 ∈ D → D.card ≤ n a) :
    (∑ x ∈ D, min 2 ((∑ a, x a * n a) / D.card)) ≤
      d * ∑ x ∈ D, min 2 ((D.sup (fun y => ∑ a, y a * n a) -
        (∑ a, x a * n a)) / D.card)
```

The first required translation, [Wilf/Window2.lean:604](Wilf/Window2.lean#L604):

```lean
theorem tile_gap_count (S : NumericalSemigroup) (K : ℕ) :
    (∑ x ∈ S.factDownSet, min K (S.wt x / S.multiplicity)) =
      (S.gaps.filter (fun x => x < K * S.multiplicity)).card
```

The second required translation, [Wilf/Window2.lean:610](Wilf/Window2.lean#L610):

```lean
theorem tile_left_count (S : NumericalSemigroup) (K : ℕ) :
    (∑ x ∈ S.factDownSet,
      min K ((S.aperyMax S.multiplicity - S.wt x) / S.multiplicity)) =
      (S.left.filter (fun x => S.conductor - K * S.multiplicity ≤ x)).card
```

The displayed `S` parameters are introduced by the source's `variable (S : NumericalSemigroup)`.
`card_factDownSet` identifies the tile's cardinality with `S.multiplicity`, and `fact_sup`
([line 589](Wilf/Window2.lean#L589)) identifies its maximum weight with
`S.aperyMax S.multiplicity`. Consequently these are exactly the two tile equalities in the task.

GW-17, [Wilf/Window2.lean:618](Wilf/Window2.lean#L618):

```lean
theorem semigroup_depth_two (S : NumericalSemigroup) :
    (S.gaps.filter (fun x => x < 2 * S.multiplicity)).card ≤
      (S.embDim - 1) *
        (S.left.filter (fun x => S.conductor - 2 * S.multiplicity ≤ x)).card
```

This uses the actual library definitions: `mem_gaps` means `x ∉ S`, while `mem_left` means
`x ∈ S ∧ x < S.conductor`. Thus the right filter is exactly the half-open window in the task.
For a natural number `x`, the natural-number condition `c - 2*m ≤ x` is equivalent to
the integer condition `(c : ℤ) - 2*m ≤ x`; negative lower endpoints do not discard any natural
elements. No conductor-depth restriction is present.

**Kernel-checked combinatorial argument**

The source follows Steps 1–5, using cardinal inequalities without subtraction so that empty
sets need no artificial positive-cardinality assumption. Write `z = |D \ {0}|`, `b = |NonMax|`,
`t = |T|`, `a = |A|`, and `y = |Y|`.

| Declaration | Location | Proved assertion |
| --- | --- | --- |
| `routing` | [line 80](Wilf/Window2.lean#L80) | `z ≤ d * |NonMax \ T| + y` |
| `corner_count` | [line 123](Wilf/Window2.lean#L123) | `2*y ≤ a*t + a`, for every `A ⊆ Fin d` |
| `counting` | [line 216](Wilf/Window2.lean#L216) | `2*z + d*t ≤ 2*d*b + a` |
| `left_sum` | [line 261](Wilf/Window2.lean#L261) | left window sum `+ a = 2*z` |
| `right_sum` | [line 328](Wilf/Window2.lean#L328) | `2*b ≤` right window sum `+ t` |

The exact type of the main counting lemma is:

```lean
theorem counting (hD : IsDownSetFin D) (A : Finset (Fin d)) :
    2 * (D.erase 0).card + d * (terminal D A).card ≤
      2 * d * (nonMax D).card + A.card
```

For nonempty `D`, down-closure gives `0 ∈ D`, so `z = m - 1`. Over ordinary integer arithmetic
this is precisely the paper's Step 3 inequality after rearrangement. `routing` injects the
nonzero cells outside `Y` into `(NonMax \ T) × Fin d`. `corner_count` injects all supported
corner/direction pairs into `T × A`, and injects the support-one corners into `A` using
maximality on each coordinate axis. It proves the suggested `2|Y| ≤ |A|(|T|+1)` bound.

The source's `trapped` initially omits the explicit maximality conjunct in the paper's `Y`.
`trapped_max` at line 55 proves that conjunct from the remaining conditions. This is an
equivalent definition, not an extra assumption or an enlarged unverified set of corners.

**Adversarial audit of the paper**

The nonempty case of the theorem and the substantive counting argument are correct. The
following omissions, convention differences, and locally false unqualified statement were found.
References are to `.research/PROOFS.md` as read for this task.

1. **Empty `D` is not defined in the paper statement** (lines 992–993). `max_D v` has no value
   when `D = ∅`, and the floor quotients then have denominator zero. The task explicitly supplies
   a natural-number convention; the formal theorem follows it. Its conclusion is `0 ≤ 0`.
   A paper version should either supply those conventions or state and dispose of the empty
   case before introducing `M`, `κ`, and `λ`.

2. **The formulas involving `m - 1` silently use nonemptiness** (Steps 1 and 4, lines 1001,
   1012, 1017). For a nonempty down-set, `0 ∈ D` and `|D \ {0}| = m - 1`. With ordinary signed
   subtraction, that cardinality formula fails at `m = 0`. The formal argument uses
   `|D \ {0}|` throughout; it does not apply signed rearrangements to truncated natural
   subtraction.

3. **Step 1's last equivalence is false without restricting to active directions** (line 1004).
   The sentence “κ(e_a) ≥ 2 iff a ∉ A” needs **`e_a ∈ D`**. Take `d = 1`, `D = {0}`,
   `m = 1`, and `n_0 = 0`. The active-weight hypothesis is vacuous and `A = ∅`, but
   `κ(e_0) = 0`. This counterexample is itself kernel-checked as
   `inactive_unit_counterexample` at [line 633](Wilf/Window2.lean#L633). The omission does not
   invalidate the sum over `D`; the formal proof applies the equivalence only to units in `D`.

4. **Inactive directions must be removed from weight estimates**, not assumed positive
   (Steps 1–2). If `x ∈ D` and `x_a > 0`, then `e_a ≤ x`, hence `e_a ∈ D`. If
   `w + e_a ∈ D`, then likewise `e_a ∈ D`. These implications justify every use of the
   weight hypothesis. Conversely, `e_a ∉ D` forces `x_a = 0` for every `x ∈ D`.
   The proof never needs all units in `D`, or positivity of weights on inactive directions.

5. **The paper uses integer weights; the requested theorem uses natural weights** (line 993).
   The exact requested natural-number statement is proved. There is no separately exported
   theorem quantified over `ℤ`-valued weights. For the paper's nonempty setting this is no
   mathematical obstruction: active integer weights are positive and inactive coordinates
   vanish on `D`, so replacing `n_a` by its natural part preserves every weight on `D`;
   integer floor division then agrees with natural division. This observation is explanatory,
   not an additional claimed kernel-checked signed-weight theorem.

6. **The two directions in Step 1 can coincide** (line 1003). For example, `x = 2e_a` requires
   taking `a = b`; one must not accidentally assume distinct directions. The formal proof
   removes one unit and bounds the remaining nonzero vector, so it covers this case.

7. **Strictness is unnecessary** (lines 993, 1002–1003, 1006–1008). With `n_a ≥ m` on active
   directions, nonzero cells still have `κ ≥ 1`, cells of degree at least two have `κ ≥ 2`,
   nonmaximal cells have `λ ≥ 1`, and cells in `N` have `λ ≥ 2`. Strict `> m` and `> 2m`
   in the paper's estimates can be replaced by the corresponding weak inequalities.
   `depth_two_of_le` kernel-checks this strengthening; `depth_two` still exports the exact
   strict statement requested.

8. **The descent's domain must explicitly be `D \ {0}`**, and its arbitrary choice needs no
   direction when `d = 0` (line 1011). A nonzero cell has nonempty support; the zero-dimensional
   function space has only the zero cell. The formal routing proof splits `d = 0` before
   choosing a direction. No positive-dimension assumption was introduced.

9. **The Step 4 deficit comparison requires the fiber bound** (lines 1012–1017). Dropping the
   terms outside `T` is legitimate because each fiber has at most `d` cells, so every
   `d - |φ⁻¹(w)|` is nonnegative. The paper states the necessary bound; there is no hidden
   surjectivity assumption. The formal proof instead uses an injection into pairs and derives
   the same inequality without deficits.

10. **The Step 5 singleton-support correction is essential** (lines 1020–1024). The pair count
    alone bounds the support sum, not twice the number of corners: axis corners contribute
    only one pair. The injection `Y₁ → A` supplies the missing allowance. “A maximal cell on
    the a-axis is unique” should be read as **at most one**, not an existence assertion for
    every axis. The formal proof establishes the required uniqueness using down-closure and
    maximality. No gap remains in this step.

11. **`m = 1` and `d = 0` were not discussed**. A one-element nonempty down-set is `{0}`;
    then `A`, `NonMax`, `T`, and `Y` are empty, both window sums vanish, and no active-weight
    condition is needed. In dimension zero, `D` is either empty or `{0}`. Both cases are in
    the kernel-checked universal statements.

12. **The paper and library choose different normal forms** (GW-17, line 1037). The paper says
    lex-largest; `Carry.lean` defines a lex-least normal form (`nf`, line 197). Both give the
    needed factorization down-set. The corollary uses the existing lex-least `factDownSet`,
    its proved down-closure, and the proved bijection with the Apéry set. Its ambient type is
    already `Fin S.primitives'.card → ℕ`; the identity
    `card_primitives' : S.primitives'.card = S.embDim - 1` supplies the final dimension factor.
    A transport of the function space to `Fin (e - 1)` is unnecessary.

13. **The semigroup translation needs the exact maximum and endpoint identities**
    (lines 936–940, 1037–1038). The proof uses `M = c + m - 1`, equivalently `M + 1 = c + m`.
    On the residue column beginning at `w`, the indices in the last `K*m` window are exactly
    `Ico (λ - K) λ`, of cardinality `min K λ`; `chain_window` at line 482 kernel-checks the
    half-open endpoint arithmetic. The paper's reference to “the last one” in a residue class
    is conditional on `λ > 0`; if `λ = 0` the class has no element below `c`. The formal
    translation handles empty columns and negative integer lower endpoints explicitly.

14. **The trivial semigroup is included in “every numerical semigroup”** (GW-17).
    The library has `S = nat`, `m = 1`, `e = 1`, `c = 0`, with empty gap and left sets.
    Both translation identities and GW-17 include this case; the corollary is `0 ≤ 0`.
    No `S ≠ nat` hypothesis was added.

No residue assumption enters GW-16. Residue classes enter only the semigroup counting
identities, where they are justified by the existing Apéry definitions and lemmas. The stated
bounded experiments and literature/novelty claims were not re-run or independently surveyed;
they are not used as premises in any formal proof.

**Axiom audit — actual final output**

The following lines are from the successful final run of `scripts/PrintAxioms.lean` on fejer.
The entries were added to that script at lines 249–264.

```text
'NumericalSemigroup.Window2.routing' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.corner_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.counting' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.left_sum' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.right_sum' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.depth_two' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.depth_two_of_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.apery_gap_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.chain_window' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.apery_left_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.sum_fact' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.fact_sup' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.tile_gap_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.tile_left_count' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.semigroup_depth_two' depends on axioms: [propext, Classical.choice, Quot.sound]
'NumericalSemigroup.Window2.inactive_unit_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound]
```

**Fejer setup, commands, and timings**

Host: `fejer`, zone `us-east1-b`; project: `/home/jmercedes/wilf/lean`.
Official Lean reports:

```text
Lean (version 4.33.1, x86_64-unknown-linux-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)
```

The checked-out mathlib revision is exactly `0df444a360eaa60ab8c11dca51a86af692955474`.
Elan was installed with the requested official installer, inside `nice -n 10 taskset -c 0-3`:

```sh
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
```

The initial copy was a tar archive made from `lean/` with `./.lake` excluded and transferred
using `gcloud compute scp --zone us-east1-b`. No laptop `.lake/` contents were copied.
`lake exe cache get` downloaded and decompressed 8,690 cache files for the pinned revision.
The unchanged source library was built successfully before any new source was copied to fejer.
The semigroup formalization was added only after GW-16 had passed its kernel check.

Every timed command below ran on fejer through this command pattern:

```sh
gcloud compute ssh fejer --zone us-east1-b --command '
  cd ~/wilf/lean
  export PATH="$HOME/.elan/bin:$PATH"
  export LEAN_NUM_THREADS=4
  /usr/bin/time -p nice -n 10 taskset -c 0-3 lake build
'
```

Replace `lake build` with `lake exe cache get`, `lake env lean Wilf/Window2.lean`, or
`lake env lean scripts/PrintAxioms.lean` for the other rows. CPU affinity `0-3` limits the
whole command and its children to four cores; `LEAN_NUM_THREADS=4` also bounds Lean threads.
No unrelated processes were stopped or modified.

Logs are retained under `/home/jmercedes/wilf/lean-logs/`. These timings are measured by
`/usr/bin/time -p` on fejer and exclude SCP/SSH startup time.

| Log basename | Command / stage | Result | Real / user / sys seconds |
| --- | --- | --- | --- |
| `p2-cache.log` | `lake exe cache get` | success | 122.69 / 155.57 / 51.67 |
| `p2-baseline.log` | unchanged `lake build` | success, 1,632 jobs, 0 errors/warnings | 67.68 / 126.26 / 10.38 |
| `p2-check-01.log` | `lake env lean Wilf/Window2.lean`, initial GW-16 draft | elaboration errors | 5.22 / 6.85 / 1.14 |
| `p2-check-02.log` | same, revised draft | remaining empty-finset helper error | 4.84 / 6.76 / 1.15 |
| `p2-check-03.log` | same, exact GW-16 | success, 0 errors/warnings | 4.81 / 6.73 / 1.14 |
| `p2-gw16-build.log` | `lake build`, GW-16 imported | success, 1,633 jobs | 7.08 / 8.69 / 2.02 |
| `p2-gw16-axioms.log` | `lake env lean scripts/PrintAxioms.lean` | success, standard axioms | 3.10 / 2.41 / 1.07 |
| `p2-check-04.log` | `lake env lean Wilf/Window2.lean`, semigroup draft | elaboration errors | 7.51 / 12.29 / 1.18 |
| `p2-check-05.log` | same, revised draft | one remaining local cardinal identity error | 7.35 / 12.33 / 1.16 |
| `p2-check-06.log` | same, GW-16 + GW-17 + translations | success, 0 errors/warnings | 7.13 / 12.10 / 1.20 |
| `p2-check-07.log` | same, also non-strict strengthening | success, 0 errors/warnings | 7.34 / 12.26 / 1.18 |
| `p2-final-build.log` | `lake build`, both main theorems | success, 1,633 jobs | 9.79 / 14.59 / 1.84 |
| `p2-final-axioms.log` | axiom script, both main theorems | success, standard axioms | 3.15 / 2.53 / 1.05 |
| `p2-release-build.log` | `lake build`, also the inactive-unit counterexample | success, 1,633 jobs, 0 errors/warnings | 10.18 / 14.77 / 1.99 |
| `p2-release-axioms.log` | final axiom script, including counterexample | success, standard axioms | 3.34 / 2.54 / 1.08 |

The second full build/axiom run followed the addition of the kernel-checked audit counterexample;
it was not a repetition after an unchanged successful check. Laptop work was limited to source
and report editing, source inspection, Git status/diff inspection, and copying files. The
pre-existing untracked `.claude/` directory was left alone. `.research/PROOFS.md` was not edited;
the corrections above are supplied for the lead researcher to review and commit.
