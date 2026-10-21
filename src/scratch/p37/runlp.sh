#!/bin/bash
# exhaustive RT2/UA2 over the MILP domain (--open --h4, Kunz <= 12) for m = 16..20, all e with 3e < m; 6 parallel parts
cd ~/wilf/p37; export LD_LIBRARY_PATH=$HOME/gurobi1303/linux64/lib
for me in "17 4" "18 4" "19 4" "20 4" "17 5" "18 5" "19 5" "20 5" "19 6" "20 6"; do
  set -- $me; t0=$(date +%s)
  for p in 0 1 2 3 4 5; do ./enumlp $1 $2 12 $p 6 > lp_$1_$2_p$p.txt & done; wait
  echo "m=$1 e=$2 done in $(( $(date +%s) - t0 ))s" >> runlp.log
done
echo DONE >> runlp.log
