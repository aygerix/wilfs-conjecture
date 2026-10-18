#!/usr/bin/python3
"""Direct C++ versus independent 4ti2/gfan comparisons; no lead job changes."""
import sys
sys.dont_write_bytecode=True
import hashlib
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import tempfile
from ht4_tasks import tilekey


def main():
    assert socket.gethostname().split('.')[0]=='fejer'
    here=Path(__file__).resolve().parent
    tmp=here/'ht4_gfan_tmp';tmp.mkdir(exist_ok=True);tempfile.tempdir=str(tmp)
    source=Path.home()/'wilf/atop/fwx/gfan_hcr.py'
    spec=importlib.util.spec_from_file_location('independent_gfan_ht4',source)
    gf=importlib.util.module_from_spec(spec);spec.loader.exec_module(gf)
    cases=[(5,(1,2,3,4))]
    if '--small' not in sys.argv:cases += [(8,(1,2,3,4)),(13,(1,2,6,9))]
    results=[]
    for m,r in cases:
        expected={tilekey(D) for D in gf.tiles(m,r)}
        command=[str(here/'ht4_scan'),str(m),'--dump','--exact','--threads','1','--lattice',*map(str,r)]
        with (here/f'ht4_gfan_{m}.stderr').open('w') as err:
            result=json.loads(subprocess.run(command,stdout=subprocess.PIPE,text=True,stderr=err,check=True).stdout)
        actual={tilekey(D) for D in result['tiles']}
        assert len(actual)==len(result['tiles']) and actual==expected
        units={tuple(int(i==a) for i in range(4)) for a in range(4)}
        minimum=min((gf.hcr(D) for D in expected if units<=set(D)),default=None)
        assert result['metrics']['min_HCR']==str(minimum)
        row=dict(m=m,r=r,tiles=len(actual),min_HCR=str(minimum),status='PASS')
        results.append(row);print(json.dumps(row),flush=True)
    report=dict(status='PASS',cases=results,execution_host=socket.gethostname(),
                independent_source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    (here/('ht4_gfan_small.json' if '--small' in sys.argv else 'ht4_gfan_validation.json')).write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
