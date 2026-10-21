#!/bin/bash
# min RT over genuine S in the open regime (c >= 4m+1, 3e < m), all r; log to rt_open.log
cd ~/wilf/p36
for m in 13 14 15 16 17 18 19 20 22 24; do for e in 3 4 5 6 7; do
  [ $((3*e)) -ge $m ] && continue
  /usr/bin/python3 kunz_cert_milp.py $m $e RT --open --K 12 --tl 180 >> rt_open.log 2>&1
done; done
echo DONE >> rt_open.log
