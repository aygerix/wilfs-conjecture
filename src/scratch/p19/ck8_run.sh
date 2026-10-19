#!/bin/bash
# REST-M3 search (lead): maximize REST = sum_{w != 0} con(w) over the class M >= 3 n1 (OBJ = 2, class penalty), any e.
Q=$1
for m in 16 24 36 48; do
  for E in $m $(( (m-1)/3 )); do
    for s in 1 2; do ./chain_kunz5 $((s*3300+m*10+Q)) $m 1500000 4 $Q 2 $E 2 -3; done
  done
done
