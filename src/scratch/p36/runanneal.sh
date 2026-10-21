#!/bin/bash
# RT annealing, d = 4,5 (e = 5,6), m around and above e^2; one process; log anneal.log
cd ~/wilf/p36
for rep in 1 2; do
for m in 26 28 30 32 34 37 40 43 46 50 53 56; do
  d=5; [ $m -le 34 ] && d=4
  for obj in RT lead; do
    /usr/bin/python3 rtanneal.py $d $m 3 4000 $((rep*100+m)) $obj >> anneal.log 2>&1
  done
done; done
echo DONE >> anneal.log
