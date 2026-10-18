#!/usr/bin/python3
"""VM-only sequential pipeline, sharing cores with the lead's jobs."""
import sys
sys.dont_write_bytecode=True
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import time

HERE=Path(__file__).resolve().parent


def main():
    assert socket.gethostname().split('.')[0]=='fejer'
    source={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('ht4_*') if p.suffix in ('.py','.cpp','.hpp')}
    (HERE/'ht4_source_manifest.json').write_text(json.dumps(source,indent=2)+'\n')
    tasks=[('independent-gfan',['/usr/bin/python3','-B',str(HERE/'ht4_gfan_check.py')]),
           ('finite-product-proof',['/usr/bin/python3','-B',str(HERE/'ht4_product_check.py')]),
           ('data',['/usr/bin/python3','-B',str(HERE/'ht4_tasks.py'),'data','5','39']),
           ('validation',['/usr/bin/python3','-B',str(HERE/'ht4_tasks.py'),'validate','5','36']),
           ('benchmark',['/usr/bin/python3','-B',str(HERE/'ht4_benchmark.py')]),
           ('adversarial',[str(Path.home()/'mathenv/bin/python'),'-B',str(HERE/'ht4_cp.py'),'--seconds','60'])]
    for phase,cmd in tasks:
        start=time.time();(HERE/'ht4_pipeline_status.json').write_text(json.dumps(dict(phase=phase,start_unix=start,command=cmd))+'\n')
        print('START '+json.dumps(dict(phase=phase,command=cmd)),flush=True)
        try:
            subprocess.run(cmd,check=True)
        except BaseException as exc:
            (HERE/'ht4_pipeline_status.json').write_text(json.dumps(dict(phase='ERROR',task=phase,error=repr(exc)))+'\n')
            raise
        print('DONE '+json.dumps(dict(phase=phase,seconds=time.time()-start)),flush=True)
    subprocess.run(['/usr/bin/python3','-B',str(HERE/'ht4_tasks.py'),'report'],check=True)
    (HERE/'ht4_pipeline_status.json').write_text(json.dumps(dict(phase='PASS',host=socket.gethostname()))+'\n')


if __name__=='__main__':main()
