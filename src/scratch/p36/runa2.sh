#!/bin/bash
# RT2/UA2 annealing ladder in m (one core); log a2.log
cd ~/wilf/p36
for m in 20 25 30 35 40 50 60; do for d in 3 4 5; do
  [ $((3*(d+1))) -ge $m ] && continue
  for obj in RT2 RT2W UA2 UA2W; do
    /usr/bin/python3 rt2anneal.py $d $m 4 2500 $((m*10+d)) $obj 4 >> a2.log 2>&1
  done
done; done
echo DONE >> a2.log
