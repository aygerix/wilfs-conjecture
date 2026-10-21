#!/bin/bash
# profiling of the exact height-4 MILP: where does the time go (finding vs proving)?  log prof.log
cd ~/wilf/p36
for m in 14 15; do for o in RT2 UA2; do
  /usr/bin/python3 kunz_prof.py $m 4 $o --open --h4 --K 12 --tl 600 --threads 2 >> prof.log 2>&1
done; done
/usr/bin/python3 kunz_prof.py 16 4 RT2 --open --h4 --K 12 --tl 600 --threads 2 --rlist 1,3,5,7,9 >> prof.log 2>&1
echo DONE >> prof.log
