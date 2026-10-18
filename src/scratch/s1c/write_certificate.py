#!/usr/bin/python3
"""Render the mathematical certificate and complete extremal lists."""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]

TEXT = r'''# S1-C is false

## Definitions

For positive non-increasing integer sequences
\(h=(h_0,\ldots,h_{L_1-1})\),
\(F=(F_0,\ldots,F_{L_1-1})\), and
\(G=(G_0,\ldots,G_{L_2-1})\), with \(h_0=L_2\) and \(F_0=G_0\), put
\[
D(h,F,G)=\{(i,j,k)\in\mathbb N^3:0\le i<L_1,\ 0\le j<h_i,\
0\le k<\min(F_i,G_j)\}.
\]
A cell \(y\in D\) is maximal if \(y+e_a\notin D\) for every
\(a\in\{1,2,3\}\). Write
\[
m=|D|,\qquad S_1(D)=\sum_{y\in\operatorname{Max}(D)}(3+y_1+y_2+y_3).
\]
The non-two-face condition is \(e_a+e_b\in D\) for all \(a\ne b\),
equivalently \(h_1,F_1,G_1\ge2\).

## Counterexample

**Proposition.** There is a non-two-face class-C set of volume \(25\)
with \(S_1=56>50=2m\). In particular S1-C is false.

**Proof.** Take
\[
\boxed{h=(4,2,1,1,1),\qquad F=(8,4,3,2,1),\qquad G=(8,2,2,1).}
\]
These are positive non-increasing sequences, \(h_0=4=|G|\), and
\(F_0=G_0=8\). Monotonicity of the defining inequalities makes \(D\)
a down-set. Moreover \(h_1=2,F_1=4,G_1=2\), so \(D\) is non-two-face.
Explicitly, \((1,1,0),(1,0,1),(0,1,1)\in D\).

The positive height rows \((\min(F_i,G_j))_{0\le j<h_i}\) are
\[
(8,2,2,1),\quad(4,2),\quad(3),\quad(2),\quad(1).
\]
Consequently
\[
m=(8+2+2+1)+(4+2)+3+2+1=25.
\]
Every cell below a column's top has its successor in direction \(e_3\)
in \(D\). Of the nine column tops, the cell \((0,1,1)\) is nonmaximal,
because \((0,2,1)\in D\). The other eight column tops are
\[
\begin{split}
&(0,0,7),\ (0,2,1),\ (0,3,0),\ (1,0,3),\\
&(1,1,1),\ (2,0,2),\ (3,0,1),\ (4,0,0).
\end{split}
\]
For each listed cell all three positive coordinate successors are absent,
as follows directly from the displayed height rows. Thus this is exactly
\(\operatorname{Max}(D)\), by the definition of maximality, and
\[
S_1(D)=10+6+6+7+6+7+7+7=56,
\qquad S_1(D)-2|D|=6>0.\qquad\square
\]

## Finite enumeration

**Parameter uniqueness and bounds.** For any non-two-face class-C set,
\(h_i,F_i,G_j\) are its respective coordinate-face column lengths:
\[
h_i=|\{j:(i,j,0)\in D\}|,\quad
F_i=|\{k:(i,0,k)\in D\}|,\quad
G_j=|\{k:(0,j,k)\in D\}|.
\]
Thus the triple determines and is determined by the labelled set.
The non-two-face condition implies \(\{0,1\}^3\subseteq D\): for
\(i,j,k\le1\), the three defining upper bounds are at least \(2\).
If the three axis lengths are \(L_1,L_2,L_3=F_0\), this cube together
with the remaining axis cells has size
\[
8+(L_1-2)+(L_2-2)+(L_3-2)=L_1+L_2+L_3+2.
\]
In particular there are no non-two-face class-C sets with \(m<8\), and
\(m\ge L_1+L_2+L_3+2\).

**Enumeration domain.** A set is the intersection of its coordinate-face
cylinders exactly when membership of a point is equivalent to membership
of all three of its coordinate-face projections. This condition is
unchanged by a coordinate permutation. The defining conditions of class C
give precisely this equivalence, and its face lengths recover the displayed
representation after any permutation. Coordinate permutations therefore
preserve class C, the non-two-face condition, volume, and \(S_1\).
Hence it suffices to take
\(2\le L_1\le L_2\le L_3\). The finite enumeration at volume \(m\)
uses exactly the following domain:

1. \(2\le L_2\le\lfloor(m-4)/2\rfloor\) and
   \(L_2\le L_3\le m-L_2-4\).
2. All positive non-increasing \(G\) of length \(L_2\), with
   \(G_0=L_3\), \(G_1\ge2\), and \(\sum_jG_j\le m-4\).
3. All sequences of rows \((h_i,F_i)\), starting at
   \((h_0,F_0)=(L_2,L_3)\), with both entries non-increasing,
   \(h_1,F_1\ge2\), and subsequent entries at least \(1\).
   A row \((u,v)\) contributes
   \(A_G(u,v)=\sum_{j=0}^{u-1}\min(v,G_j)\) cells.
   The number of rows lies between \(2\) and \(L_2\), and their
   total contribution is exactly \(m\).

These conditions are necessary and sufficient for a sorted-axis triple
of the desired volume. In particular, row zero has volume \(\sum_jG_j\)
and row one has volume at least \(4\), giving the bound in step 2.
The row recursion discards a branch only if its next row exceeds the
remaining volume or the remaining volume exceeds the number of available
row slots times the last row's volume. These exclusions are valid because
subsequent row volumes are positive and non-increasing. Conversely each
admissible triple has a unique sequence of choices in these three steps.

For a sorted-axis triple, its weight in the labelled count is the number
of distinct permutations of \((L_1,L_2,L_3)\): \(6\), \(3\), or \(1\).
Indeed coordinate permutations give a bijection between the sets with
any two prescribed orderings of the same axis-length multiset.
For each triple, \(S_1\) is checked from the constructed cell set by
testing the three successors of every cell. The independent audit also
computes maximal cells as the complement in \(D\) of the predecessors
of cells of \(D\). All tabulated extrema are exact integers.

## Checked cases

All non-two-face class-C sets of each volume \(8\le m\le25\) are covered
below. Volumes \(0\le m\le7\) have no such sets. Every recorded set
satisfies face reconstruction, downward closure, cube containment, the
axis-length bound, and agreement of the direct maximal-cell sum with the
strict-corner sum. Every recorded set is also included in the independent
cell-set audit, which reproduces the counts and all extremal orbits.

Let \(E_m=\max_{|D|=m}(S_1(D)-2m)\), with the maximum taken over
non-two-face class-C sets. An extremal orbit means an orbit under all
six coordinate permutations.

| m | Sorted-axis triples | Labelled sets | E_m | Extremal orbits |
|---:|---:|---:|---:|---:|
'''


def main():
    results = [json.loads(p.read_text()) for p in sorted(HERE.glob('result_*.json'))]
    results = [r for r in results if r['complete']]
    audit = json.loads((HERE / 'audit.json').read_text())
    assert audit['complete']
    assert [r['m'] for r in results] == list(range(8, 26))
    text = TEXT
    for r in results:
        text += '| {m} | {sorted_axis_count} | {labelled_count} | {max_excess} | {n} |\n'.format(
            n=len(r['extrema']), **r)
    text += '\nThe total is %d sorted-axis triples, representing %d labelled sets.\n' % (
        audit['sorted_axis_total'], audit['labelled_total'])
    text += r'''
Define a nonvacuous finite-range threshold to be an integer
\(M_0\le25\) for which every checked volume
\(\max(8,M_0)\le m\le25\) has \(E_m\le0\).
No such threshold exists, since \(E_{25}=6\).
In particular \(M_0=25\) is invalid. The existence or value of any
larger infinite-range threshold is not determined by these finite cases.

## All extremal sets in the checked range

For each volume the following is the complete list of triples
\((h;F;G)\), one representative per extremal orbit. Every labelled
extremal set is obtained from one of these sets by a coordinate permutation.
The representative is the lexicographically least face triple among its
coordinate permutations; its axis lengths need not be sorted.

'''
    for r in results:
        text += '### m = %d, E_m = %d\n\n' % (r['m'], r['max_excess'])
        for h, f, g in r['extrema']:
            parts = ['(' + ','.join(map(str, seq)) + ')' for seq in (h, f, g)]
            text += '- `' + '; '.join(parts) + '`\n'
        text += '\n'
    destination = ROOT / '.research/drafts/S1C_PROOF.md'
    destination.write_text(text)
    print(str(destination))


if __name__ == '__main__':
    main()
