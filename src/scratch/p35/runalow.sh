#!/bin/bash
# lead 2026-10-20: minimize the CASEB-WINDOW slack (d+1)|A_<| - mu on Haanpaa delta and affine images (Z/63).
cd ~/wilf/p35
: > alow63.txt
nice /usr/bin/python3 minalow_fix.py 63 1,3,8,12,18,22,27,29,30,43,50 6 900 1 1 4 >> alow63.txt 2>&1
nice /usr/bin/python3 minalow_fix.py 63 1,3,8,12,18,22,27,29,30,43,50 3 900 1 1 4 >> alow63.txt 2>&1
head -6 aff63.txt | while read D; do nice /usr/bin/python3 minalow_fix.py 63 $D 6 600 1 1 4 >> alow63.txt 2>&1; done
echo DONE >> alow63.txt
