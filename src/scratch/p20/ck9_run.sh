#!/bin/bash
# CHAIN-UNION search (lead): minimize (B_chain + E_U)/need by Kunz annealing, EMAX = m/2 and m/3 (away from the MED/T equality cases).
Q=$1
for m in 20 30 40 56 72; do
  for E in $(( m/2 )) $(( (m-1)/3 )); do
    for s in 1 2; do ./chain_kunz6 $((s*4400+m*10+Q)) $m 2000000 4 $Q 2 $E 3 0; done
  done
done
