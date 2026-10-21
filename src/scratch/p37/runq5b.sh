#!/bin/bash
# level-1 q5cnt for m = 25..32 with d <= (m-1)/2 (rigorous: d >= m/2 puts every class in A u (A+A), so max Ap <= 4m-2 and q <= 3)
cd ~/wilf/p37
until grep -q DONE runq5.log; do sleep 20; done
for m in $(seq 25 32); do t0=$(date +%s); dm=$(( (m-1)/2 ))
  for p in 0 1 2 3 4 5; do ./q5cnt $m 1 2 $dm $p 6 > q5_${m}_L1_d${dm}_p$p.txt & done; wait
  echo "m=$m L=1 d=2..$dm done in $(( $(date +%s) - t0 ))s" >> runq5.log; done
echo DONE2 >> runq5.log
