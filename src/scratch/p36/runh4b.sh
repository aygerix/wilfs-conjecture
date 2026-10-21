#!/bin/bash
# continuation of runh4.sh with 6 Gurobi threads (restarted 2026-10-21 after stopping the obsolete depth-four jobs)
cd ~/wilf/p36
/usr/bin/python3 kunz_cert_milp.py 16 4 RT2 --open --h4 --K 12 --tl 240 --threads 6 --rlist 10,11,12,13,14,15 >> h4_rt2.log 2>&1
/usr/bin/python3 kunz_cert_milp.py 16 4 UA2 --open --h4 --K 12 --tl 240 --threads 6 >> h4_ua2.log 2>&1
for m in 16 17 18 19 20; do for e in 4 5 6; do
  [ $((3*e)) -ge $m ] && continue
  [ $m -eq 16 ] && [ $e -eq 4 ] && continue
  /usr/bin/python3 kunz_cert_milp.py $m $e RT2 --open --h4 --K 12 --tl 240 --threads 6 >> h4_rt2.log 2>&1
  /usr/bin/python3 kunz_cert_milp.py $m $e UA2 --open --h4 --K 12 --tl 240 --threads 6 >> h4_ua2.log 2>&1
done; done
echo DONE >> h4_rt2.log
