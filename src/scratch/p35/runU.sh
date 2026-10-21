#!/bin/bash
# lead 2026-10-20: falsification of CONJ CASEB-U (case B => unit truncation U >= 0) on Haanpaa delta (Z/63) and affine images.
cd ~/wilf/p35
: > minU63.txt
for H3 in 1 0; do for CM in 4 0; do
nice /usr/bin/python3 minU_fix.py 63 1,3,8,12,18,22,27,29,30,43,50 6 600 1 $H3 $CM >> minU63.txt 2>&1
done; done
head -6 aff63.txt | while read D; do nice /usr/bin/python3 minU_fix.py 63 $D 6 400 1 1 0 >> minU63.txt 2>&1; done
echo DONE >> minU63.txt
