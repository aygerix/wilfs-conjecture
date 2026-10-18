#!/usr/bin/python3
"""Finalize completed VM artifacts; run only on fejer after all checks."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import socket
from fractions import Fraction as F
from pathlib import Path


def main():
    host = socket.gethostname()
    assert host.split('.')[0] == 'fejer'
    here = Path(__file__).resolve().parent
    records = sorted((json.loads(p.read_text()) for p in here.glob('results_all_*.json')),
                     key=lambda r:r['m'])
    assert [r['m'] for r in records] == list(range(5,records[-1]['m']+1))
    validation = json.loads((here/'validation.json').read_text())
    audit = json.loads((here/'audit.json').read_text())
    assert validation['status'] == audit['status'] == 'PASS'
    assert validation['random']['accepted'] >= 2000 and validation['random']['missing'] == 0
    artifacts = [here/'validation.json',here/'audit.json',here/'hcr_failures_all.json',
                 here/'RESULTS.md',here/'table_all.csv']
    for r in records:
        m = r['m']
        checked = json.loads((here/f'checked_all_{m}.json').read_text())
        assert checked['status'] == 'PASS' and checked['execution_host'].split('.')[0] == 'fejer'
        assert checked['tiles'] == r['tiles'] and checked['min_hcr'] == r['min_hcr']
        assert checked['hcr_failures'] == len(r['hcr_failures'])
        assert r['certificate'] == 'exact-volume+facets'
        artifacts.extend([here/f'results_all_{m}.json',here/f'checked_all_{m}.json',
                          here/f'certificate_all_{m}.jsonl.gz'])
    failures = json.loads((here/'hcr_failures_all.json').read_text())
    expected = [f for r in records for f in r['hcr_failures']]
    assert [{k:f[k] for k in ('m','r','hcr','tile')} for f in failures] == expected
    summary = dict(status='PASS',execution_host=host,range=[5,records[-1]['m']],
                   multiplicities=len(records),lattices=sum(r['lattices'] for r in records),
                   tiles=sum(r['tiles'] for r in records),
                   non_two_face=sum(r['non_two_face'] for r in records),
                   min_hcr=str(min(F(r['min_hcr']) for r in records)),
                   hcr_failures=len(failures),independently_checked_through=records[-1]['m'],
                   validation_semigroups=validation['random']['accepted'],
                   validation_ties=validation['random']['boundary_weight_cases'])
    (here/'FINAL_STATUS.json').write_text(json.dumps(summary,indent=2)+'\n')
    columns = 3
    rows = math.ceil(len(records)/columns)
    lines = ['| m, L, tiles, NT, C, min HCR | m, L, tiles, NT, C, min HCR | m, L, tiles, NT, C, min HCR |',
             '|:--|:--|:--|']
    for i in range(rows):
        cells = []
        for j in range(columns):
            k = i+j*rows
            if k < len(records):
                r = records[k]
                cells.append('`{m}, {lattices}, {tiles}, {non_two_face}, V, {min_hcr}`'.format(**r))
            else:
                cells.append('')
        lines.append('| '+' | '.join(cells)+' |')
    (here/'FINAL_TABLE.md').write_text('\n'.join(lines)+'\n')
    artifacts.extend([here/'FINAL_STATUS.json',here/'FINAL_TABLE.md'])
    manifest = []
    for path in artifacts:
        digest = hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
        manifest.append(digest+'  '+path.name)
    (here/'artifact_manifest.sha256').write_text('\n'.join(manifest)+'\n')
    print(json.dumps(summary),flush=True)
    print('\n'.join(lines),flush=True)


if __name__ == '__main__':
    main()
