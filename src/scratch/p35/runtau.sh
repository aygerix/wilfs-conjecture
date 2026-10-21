#!/bin/bash
# lead 2026-10-20: lift-free leading-order test of CASEB-U (min tau* over case-B tiles, fixed delta). Waits for runU.sh.
cd ~/wilf/p35
while ! grep -q DONE minU63.txt; do sleep 30; done
: > tau.txt
H=1,3,8,12,18,22,27,29,30,43,50
for H3 in 0 1 3; do nice /usr/bin/python3 tau_fix.py 63 $H 600 1 $H3 >> tau.txt 2>&1; done
nice /usr/bin/python3 tau_fix.py 67 1,2,3,4,5,6,16,24,33,40,49,57 600 1 0 >> tau.txt 2>&1
nice /usr/bin/python3 tau_fix.py 67 1,2,3,4,5,6,16,24,33,40,49,57 600 1 1 >> tau.txt 2>&1
for spec in "30 1,3,9,11,12,16,26" "35 1,3,13,15,17,27,29,30" "43 1,2,3,10,15,21,25,31,36" "51 1,3,7,10,15,18,22,24,25,38"; do
  set -- $spec; nice /usr/bin/python3 tau_fix.py $1 $2 300 1 0 >> tau.txt 2>&1; nice /usr/bin/python3 tau_fix.py $1 $2 300 1 1 >> tau.txt 2>&1
done
echo DONE >> tau.txt
