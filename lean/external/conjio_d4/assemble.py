"""Independent kernel check of the conjectures.io proof of Wilf for c <= 4m (result fd12daa7-..., solver "Elias").
Builds ConjCheck.lean = [Mathlib imports minus notation-clashing modules] + ConjCheckPreamble.lean (OUR definitions of
numerical semigroups / Wilf, all API lemmas proved) + the UNMODIFIED proof body of Main.lean (SHA-256 checked) with
`fcTypeOfName% "Math30Catalog.source23"` replaced by our own statement, + a restatement in elementary terms and
#print axioms.

Run from a Lake project with lean-toolchain leanprover/lean4:v4.35.0-rc2 and Mathlib at tag v4.35.0-rc2
(fejer: ~/wilf/ext/cc35):
  python3 -I assemble.py MAIN.lean ConjCheckPreamble.lean .lake/packages/mathlib OUT.lean
  lake env lean OUT.lean      # 2026-10-20: 0 errors, ~7 min, 11 GB; axioms propext, Classical.choice, Quot.sound

Why imports are filtered: the original build imported only a subset of Mathlib. Three Mathlib notations glue to
identifiers in the proof text and change its tokenization when imported:
  "≤m" (Matroid.Minor.Order), "≤r" (Matroid.Minor.Restrict), "→g" (SimpleGraph.Maps).
E.g. `x≤m3_value` lexes as `≤m` + `3_value`. We drop every module that (transitively) imports a file declaring such a
token (364 of 8,536 modules) instead of editing the proof text."""
import hashlib, pathlib, re, sys

SHA = "b1bdde55334bfbbc4c408f3e8749faa566da7cab620a4787c7881515ea986447"
main_p, pre_p, mathlib_root, out_p = map(pathlib.Path, sys.argv[1:5])
b = main_p.read_bytes()
assert hashlib.sha256(b).hexdigest() == SHA, "Main.lean is not the audited file"
proof = b.decode()
old = 'theorem target : fcTypeOfName% "Math30Catalog.source23" := by'
assert proof.count(old) == 1
proof = proof.replace(old, "theorem target : ∀ S : Math30.Wilf.NumericalSemigroup, "
                           "S.conductor ≤ 4 * S.multiplicity → S.SatisfiesWilf := by")

mods, toks = {}, {}
for p in (mathlib_root / "Mathlib").rglob("*.lean"):
    mod = ".".join(p.relative_to(mathlib_root).with_suffix("").parts)
    txt = p.read_text(errors="ignore")
    mods[mod] = re.findall(r"^(?:public\s+)?(?:meta\s+)?import\s+(\S+)", txt, re.M)
    for mt in re.finditer(r"(?:infixl?|infixr|notation|prefix|postfix)(?::\d+)?\s+\"\s*([^\"\s]+)\s*\"", txt):
        tok = mt.group(1)
        if (len(tok) >= 2 and not tok.isalnum() and any(ord(ch) > 127 for ch in tok)
                and any(ch.isalpha() and ord(ch) < 128 for ch in tok) and tok in proof):
            toks.setdefault(tok, set()).add(mod)
bad = set().union(*toks.values()) if toks else set()
changed = True
while changed:
    changed = False
    for mod, imps in mods.items():
        if mod not in bad and any(i in bad for i in imps):
            bad.add(mod); changed = True
keep = sorted(m for m in mods if m not in bad and m != "Mathlib")
print("clashing tokens:", {k: sorted(v) for k, v in toks.items()}, "| excluded", len(bad), "| kept", len(keep))

pre = pre_p.read_text()
assert pre.startswith("import Mathlib\n")
tail = """
end Bounty

/-- Independent restatement in elementary terms: for every numerical semigroup `S` with
`c(S) ≤ 4 m(S)`, `c(S) ≤ e(S) · ℓ(S)`. -/
theorem wilf_conductor_le_four_mul_multiplicity :
    ∀ S : Math30.Wilf.NumericalSemigroup, S.conductor ≤ 4 * S.multiplicity →
      S.conductor ≤ S.primitiveElements.card * S.leftElements.card :=
  fun S h => Bounty.target S h

#print axioms wilf_conductor_le_four_mul_multiplicity
#print axioms Bounty.an_anchor_bound
#print axioms Bounty.t11_reduce_to_pruned
"""
out_p.write_text("\n".join("import " + m for m in keep) + "\n" + pre[len("import Mathlib\n"):]
                 + "\nnamespace Bounty\n\n" + proof + "\n" + tail)
