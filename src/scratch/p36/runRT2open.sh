#!/bin/bash
# min RT2 and min UA2 over genuine S in the open regime (c >= 4m+1, 3e < m), all r; logs rt2_open.log, ua2_open.log
cd ~/wilf/p36
for m in 13 14 15 16 17 18; do for e in 3 4 5; do
  [ $((3*e)) -ge $m ] && continue
  /usr/bin/python3 kunz_cert_milp.py $m $e RT2 --open --K 12 --tl 180 >> rt2_open.log 2>&1
  /usr/bin/python3 kunz_cert_milp.py $m $e UA2 --open --K 12 --tl 180 >> ua2_open.log 2>&1
done; done
echo DONE >> rt2_open.log
