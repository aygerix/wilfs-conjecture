#!/bin/bash
# lead 2026-10-20: smallest lifts K for which a height-3 case-B tile is realizable, over the affine images of Z/63.
cd ~/wilf/p35; : > smallK.txt
while read D; do
  for K in 2 3 4 5; do
    r=$(nice /usr/bin/python3 caseb_fixlift.py 63 $D $K 120 1 - 1)
    echo "$r" | grep -q REALIZED && { echo "K=$K $r" >> smallK.txt; break; }
    [ $K = 5 ] && echo "K>5 none: $D" >> smallK.txt
  done
done < aff63.txt
echo DONE >> smallK.txt
