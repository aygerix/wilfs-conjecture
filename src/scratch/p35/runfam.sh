#!/bin/bash
# lead 2026-10-20: height-3 case-B family from affine images of Haanpaa's Z/63 cover; then measure each S.
cd ~/wilf/p35
: > fam63.txt
i=0
while read D; do i=$((i+1))
  nice /usr/bin/python3 caseb_fixlift.py 63 $D 10 300 1 fam63_$i.json >> fam63.txt 2>&1
  if [ -s fam63_$i.json ]; then
    G=$(/usr/bin/python3 -c "import json; print(' '.join(map(str, sorted(json.load(open('fam63_$i.json'))['gens']))))")
    nice ~/mathenv/bin/python -I nk0.py 63 $G >> fam63.txt; nice ~/mathenv/bin/python -I tilechecks.py 63 $G | tail -2 >> fam63.txt
  fi
done < aff63.txt
for spec in "30 1,3,9,11,12,16,26" "35 1,3,13,15,17,27,29,30" "43 1,2,3,10,15,21,25,31,36" "51 1,3,7,10,15,18,22,24,25,38"; do
  set -- $spec; nice /usr/bin/python3 caseb_fix.py $1 $2 300 0 >> fam_small.txt; nice /usr/bin/python3 caseb_fix.py $1 $2 300 1 >> fam_small.txt
done
echo DONE >> fam63.txt
