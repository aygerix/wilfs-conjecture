#!/bin/bash
# min TX (exact-tau signed certificate value) over genuine S, all r, small m, e = 3..5; then open regime; log tx.log
cd ~/wilf/p36
for m in 8 9 10 11 12 13; do for e in 3 4 5; do
  [ $e -ge $m ] && continue
  /usr/bin/python3 kunz_cert_milp.py $m $e TX --K 10 --tl 120 --threads 1 >> tx.log 2>&1
done; done
for m in 13 14 15 16 17 18; do for e in 3 4 5; do
  [ $((3*e)) -ge $m ] && continue
  /usr/bin/python3 kunz_cert_milp.py $m $e TX --open --K 12 --tl 180 --threads 1 >> tx_open.log 2>&1
done; done
echo DONE >> tx.log
