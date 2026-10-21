#!/bin/bash
# lead 2026-10-20: CASEB-ALL test.  Realize case-B S (flat and height-3) from extremal covers, then SUPP at every n.
cd ~/wilf/p35
out=caseball.txt; : > $out
run() { # m delta H3MIN tag
  nice /usr/bin/python3 caseb_fixlift.py $1 $2 8 300 1 cb_$4.json $3 >> $out 2>&1
  if [ -s cb_$4.json ]; then
    G=$(/usr/bin/python3 -c "import json; print(' '.join(map(str, sorted(json.load(open('cb_$4.json'))['gens']))))")
    echo "S: $1 $G" >> $out; (cd ../p34 && timeout 1800 nice ~/mathenv/bin/python -I multin.py $1 $G) >> $out 2>&1; rm -f cb_$4.json
  fi
}
run 13 1,2,8,10 -1 a1; run 13 1,3,5,6 -1 a2; run 19 1,3,12,14,15 -1 b1; run 19 1,4,5,11,13 -1 b2
run 30 1,3,9,11,12,16,26 -1 c1; run 43 1,2,3,10,15,21,25,31,36 -1 d1; run 51 1,3,7,10,15,18,22,24,25,38 -1 e1
run 63 1,3,8,12,18,22,27,29,30,43,50 -1 f1
i=0; while read D; do i=$((i+1)); [ $i -gt 8 ] && break; run 63 $D -1 g$i; run 63 $D 1 h$i; done < aff63.txt
echo DONE >> $out
