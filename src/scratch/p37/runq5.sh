#!/bin/bash
# q = 5 counting decomposition (q5cnt): level-1 exhaustive m = 10..32; mixed levels {1,2,3} exhaustive m = 10..17, d <= 7 for m = 18..22
cd ~/wilf/p37
run(){ m=$1; L=$2; dmin=$3; dmax=$4; t0=$(date +%s)
  for p in 0 1 2 3 4 5; do ./q5cnt $m $L $dmin $dmax $p 6 > q5_${m}_L${L}_d${dmax}_p$p.txt & done; wait
  echo "m=$m L=$L d=$dmin..$dmax done in $(( $(date +%s) - t0 ))s" >> runq5.log; }
for m in $(seq 10 32); do run $m 1 2 $((m-1)); done
for m in $(seq 10 17); do run $m 3 2 $((m-1)); done
for m in 18 19 20 21 22; do run $m 3 2 7; done
echo DONE >> runq5.log
