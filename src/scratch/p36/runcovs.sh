#!/bin/bash
# hill-climb full-pair height-3 covers for d = 6..10 across m (largest first per d); log covs.log, covers in hc_d_m.txt
cd ~/wilf/p36
for d in 6 7 8 9 10; do
  N3=$(python3 -c "from math import comb; print(comb($d+3,3))")
  lo=$((N3*55/100)); hi=$((N3*85/100))
  for m in $(seq $hi -1 $lo); do
    ~/mathenv/bin/python -I covsearch.py $d $m 200 6000 $m > hc_${d}_$m.txt 2>> covs.log
    n=$(wc -l < hc_${d}_$m.txt)
    if [ "$n" -gt 0 ]; then echo "d=$d max m found=$m (N3=$N3)" >> covs.log; break; fi
    rm -f hc_${d}_$m.txt
  done
done
echo DONE >> covs.log
