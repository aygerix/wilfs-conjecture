# P13 computational commands

All commands below are executed on fejer in `~/wilf/p13/`.
Input files are copied with `gcloud compute scp --zone us-east1-b`.
The laptop is used for reading, editing and copying only. No commits.
At most four of our nice single-core jobs are run concurrently.

```sh
cc -O3 search.c -lm -o search
cc -O3 structured.c -o structured
cc -O3 gensearch.c -lm -o gensearch
cc -O3 tree.c -o tree

nice -n 10 ./search 61 20 150000 0 130061 0 >anneal_cu61.log 2>&1
nice -n 10 ./search 87 20 150000 1 130087 0 >anneal_poor87.log 2>&1
nice -n 10 ./search 211 12 100000 2 130211 1 >anneal_plus211.log 2>&1
nice -n 10 ./structured 5 90 >structured.log 2>&1

nice -n 10 ./search 61 40 200000 3 130361 0 >anneal_top61.log 2>&1
nice -n 10 ./search 127 30 150000 3 130327 1 >anneal_top127.log 2>&1
nice -n 10 ./gensearch 101 60 30000 0 >gensearch101.log 2>&1
nice -n 10 ~/mathenv/bin/python quick.py >quick.log 2>&1
nice -n 10 ./tree 28 >tree28.log 2>&1
nice -n 10 ~/mathenv/bin/python local_scan.py >local_scan.log 2>&1

# After adding the new MF/count/shadow assertions to core.h:
cc -O3 tree.c -o tree_structural
nice -n 10 ./tree_structural 28 >tree28_structural.log 2>&1
cc -O3 structured.c -o structured_new
nice -n 10 ./structured_new 5 90 >structured_verified.log 2>&1
cc -O3 search.c -lm -o search_shaped
nice -n 10 ./search_shaped 527 4 30000 0 130527 1 1 >anneal_shaped527.log 2>&1
nice -n 10 ~/mathenv/bin/python case_checks.py >case_checks.log 2>&1
cc -O3 local_verify.c -o local_verify
nice -n 10 ./local_verify >local_verify.log
```

Initial anneals predate the final structural assertions. The updated
tree, structured rerun, shaped anneal and independent Python checks
verify the final statements. Printed witness lines in the initial logs
have fewer diagnostic fields than the final evaluator; numerical
objectives are unchanged. The source files in this directory are the
final versions.

`case_checks.py` initially rejected the assumption that `<53,85..95>`
was a depth-four named case: its actual depth is five. It is now kept
as an outside-scope context check, separate from the 232 depth-four
evaluations. The retained final log is from the corrected driver.

Seeds, proposal counts, rejected initializations and best witnesses are
preserved in the logs. Evaluation counts can include repeated states;
only the genus-tree count is a count of distinct semigroups.
