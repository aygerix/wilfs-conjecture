#!/bin/bash
# min RT over genuine S (all r) for small m, e in 3..5; log to rt_small.log
cd ~/wilf/p36
for m in 8 9 10 11 12 13 14; do for e in 3 4 5; do
  [ $e -ge $m ] && continue
  /usr/bin/python3 kunz_cert_milp.py $m $e RT --K 10 --tl 120 >> rt_small.log 2>&1
done; done
echo DONE >> rt_small.log
