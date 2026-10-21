#!/bin/bash
# full-pair height-3 covers for d = 6 (C(9,3) = 84) near the top, then RT/W on S built from them; log cov6.log
cd ~/wilf/p36
for m in 64 62 60 58 57 56 55 54 53 52; do
  timeout 3000 ./nearcov 6 $m > nc6_$m.txt 2>> cov6.log
  n=$(wc -l < nc6_$m.txt)
  if [ "$n" -gt 0 ]; then head -400 nc6_$m.txt > nc6h_$m.txt; /usr/bin/python3 covfam.py nc6h_$m.txt 1,2 2 1 >> cov6.log 2>&1; fi
done
echo DONE >> cov6.log
