#!/bin/bash
# exact MILP: min RT2 and min UA2, open regime, e >= 4, Apery height >= 4; logs h4_rt2.log, h4_ua2.log
cd ~/wilf/p36
for m in 13 14 15 16 17 18 19 20; do for e in 4 5 6; do
  [ $((3*e)) -ge $m ] && continue
  /usr/bin/python3 kunz_cert_milp.py $m $e RT2 --open --h4 --K 12 --tl 240 >> h4_rt2.log 2>&1
  /usr/bin/python3 kunz_cert_milp.py $m $e UA2 --open --h4 --K 12 --tl 240 >> h4_ua2.log 2>&1
done; done
echo DONE >> h4_rt2.log
