#!/bin/bash
# rtobs3 (fakes + R/RT/RT2/UA/UA2) on all d=6 covers (K=1), d=7 multiplier images (K=1), d=5 covers (K in {1,2}); one core
cd ~/wilf/p36
/usr/bin/python3 rtobs3.py -cov nc6_55.txt 1 420 > obs3_6.txt 2>&1
/usr/bin/python3 rtobs3.py -cov hc7m.txt 1 200 > obs3_7.txt 2>&1
cat nc5_40.txt nc5_39.txt nc5_38.txt > nc5_all.txt
/usr/bin/python3 rtobs3.py -cov nc5_all.txt 1,2 300 > obs3_5.txt 2>&1
echo DONE >> obs3_5.txt
