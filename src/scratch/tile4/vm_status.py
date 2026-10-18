#!/usr/bin/python3
"""Small VM-only status/readout helper; no enumeration is performed here."""
import sys
sys.dont_write_bytecode = True
import json
import socket
from pathlib import Path

assert socket.gethostname().split('.')[0] == 'fejer'
here = Path(__file__).resolve().parent
s = json.loads((here/'vm_status.json').read_text())
checked = sorted(int(p.stem.split('_')[-1]) for p in here.glob('checked_all_*.json')
                 if json.loads(p.read_text()).get('execution_host','').split('.')[0] == 'fejer')
records = sorted((json.loads(p.read_text()) for p in here.glob('results_all_*.json')),
                 key=lambda r:r['m'])
if '--brief' in sys.argv:
    last = records[-1]
    print(json.dumps(dict(phase=s.get('phase'),m=s.get('active_m'),
          done=s.get('lattices_done'),total=s.get('lattices_total'),
          checked_through=max(checked,default=0),elapsed=s.get('elapsed_seconds'),
          remaining=s.get('remaining_seconds'),
          tiles=sum(r['tiles'] for r in records),
          failures=sum(len(r['hcr_failures']) for r in records),
          last={k:last[k] for k in ('m','lattices','tiles','non_two_face','min_hcr')},
          error=s.get('error'))))
    sys.exit(0)
print(json.dumps({k:s.get(k) for k in ('phase','active_m','lattices_done','lattices_total',
                                      'elapsed_seconds','remaining_seconds','error')}))
print('VM checked multiplicities:', checked)
print('Completed:',len(records),'Total tiles:',sum(r['tiles'] for r in records),
      'HCR failures:',sum(len(r['hcr_failures']) for r in records))
for r in records[-2:]:
    print(json.dumps({k:r[k] for k in ('m','lattices','tiles','non_two_face','min_hcr','seconds')}))
