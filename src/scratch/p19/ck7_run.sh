#!/bin/bash
# CHAIN on class Q = {M >= 3 n1, 3e < m, q >= QMIN} (lead): annealing with class penalty, EMAX = floor((m-1)/3).
Q=$1
for m in 24 36 48 60 80; do
  E=$(( (m-1)/3 ))
  for s in 1 2 3; do ./chain_kunz5 $((s*5100+m*10+Q)) $m 2000000 4 $Q 2 $E 0 -3; done
done
