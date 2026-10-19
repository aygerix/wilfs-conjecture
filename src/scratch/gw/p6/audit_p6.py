"""Exact audit of the finite P6 certificate and independent checks. fejer only."""
import hashlib,json,platform
from math import comb
from pathlib import Path
import re
from collections import Counter

def parse(path):
    out=[]
    for ln in Path(path).read_text().splitlines():
        if not ln.startswith('d='):continue
        z={k:int(v) for k,v in (s.split('=') for s in ln.split())}
        assert z['FAILURES']==0 and z['vectors']==comb(z['m']-1,z['d'])
        assert z['shape']+z['forced']+z['dp_faces']==z['h3_pairfaces']
        if z['h3_pairfaces']:assert z['min_bound']>=0
        out.append(z)
    return out
old={}
for name in ['cert_d2.log','cert_d3.log','cert_d4.log','cert_d5_6_19.log','cert_d5_20_29.log','cert_d5_30_56.log']:
    for row in parse(name):
        key=(row['d'],row['m']);assert key not in old;old[key]=row
new={}
for d in (2,3,4,5):
    for row in parse('container_d'+str(d)+'.log'):
        key=(d,row['m']);assert key not in new;new[key]=row
        for field in ['vectors','covers','h3_pairfaces','flat','shape','forced','dp_faces']:
            assert row[field]==old[key][field],(key,field,row[field],old[key][field])
assert set(old)==set(new)
for d in (2,3,4,5):
    assert {m for dd,m in old if dd==d}==set(range(d+1,comb(d+3,3)+1))
assert sum(z['vectors'] for z in old.values())==sum(comb(comb(d+3,3),d+1) for d in (2,3,4,5))
ind=json.loads(Path('independent_small.json').read_text())
for z in ind:
    ref=old[z['d'],z['m']]
    assert z['pairfaces']==ref['h3_pairfaces'] and z['flat']==ref['flat']
    assert z['min_slack'] is None or z['min_slack']>=0
for ln in Path('coverage_d5.log').read_text().splitlines():
    if not ln.startswith('d='):continue
    z={k:int(v) for k,v in (s.split('=') for s in ln.split())}
    assert z['three_cover']==old[5,z['m']]['covers']
core=json.loads(Path('core2.json').read_text());assert all(z['min_slack'] is None or z['min_slack']>=0 for z in core)
charge=json.loads(Path('charging_summary.json').read_text())
assert 'CHARGING_ALL_PASS' in Path('charging.log').read_text()
assert 'CORE2_ALL_PASS' in Path('core2.log').read_text()
assert 'INDEPENDENT_EXPLICIT_TILES_PASS' in Path('independent_small.log').read_text()
assert charge['pairform_counterexample']['m']==4
milp=json.loads(Path('milp_2026101982.json').read_text())
assert all(not z['incumbent'] or z['min_slack']>=0 for z in milp)
statuses=dict(Counter(z['status'] for z in milp))
assert 'FAILURE_CHECKS_PASS' in Path('failure_checks.log').read_text()
summary=[]
for d in (2,3,4,5):
    a=[z for (dd,m),z in old.items() if dd==d];b=[z for (dd,m),z in new.items() if dd==d]
    summary.append(dict(d=d,bound=comb(d+3,3),vectors=sum(z['vectors'] for z in a),
        covering_vectors=sum(z['covers'] for z in a),h3_pairfaces=sum(z['h3_pairfaces'] for z in a),
        flat_faces=sum(z['flat'] for z in a),shape=sum(z['shape'] for z in a),forced=sum(z['forced'] for z in a),
        hard_faces=sum(z['dp_faces'] for z in a),dp_unions=sum(z['dp_masks'] for z in a),
        feasible_containers=sum(z['dp_masks'] for z in b),sigma_tests_dp=sum(z['sigma_tests'] for z in a),
        sigma_tests_container=sum(z['sigma_tests'] for z in b),maxdp=max(z['maxdp'] for z in a),
        largest_covering_m=max(z['m'] for z in a if z['covers'])))
out=dict(status='PASS',python=platform.python_version(),certificate=summary,
         independent_explicit_tiles=sum(z['actual_tiles'] for z in ind),
         independent_phase_pairs=sum(z['sigma_pairs'] for z in ind),
         core2_phase_pairs=sum(z['sigma_pairs'] for z in core),charging=charge,
         milp_calls=len(milp),milp_incumbents=sum(z['incumbent'] for z in milp),milp_statuses=statuses)
for row in summary:print('FINITE',json.dumps(row,sort_keys=True))
print('INDEPENDENT',out['independent_explicit_tiles'],out['independent_phase_pairs'])
print('CORE2',out['core2_phase_pairs'])
print('MILP_STATUSES',statuses)
Path('P6_AUDIT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
# This remote directory predates P6 and also holds unrelated P5 experiments.
# Hash only this certificate's stated inputs and outputs. Neither the audit's
# open stdout log nor the generated audit summary is a substantive input.
source_names=['P6_REPORT.md','README.md','height3_certificate.c','coverage.c',
              'independent_small.py','core2.py','charging_checks.py',
              'failure_checks.py','milp_adversary.py','audit_p6.py']
data_names=['cert_d2.log','cert_d3.log','cert_d4.log','cert_d5_6_19.log',
            'cert_d5_20_29.log','cert_d5_30_56.log',
            'container_d2.log','container_d3.log','container_d4.log',
            'container_d5.log','coverage_d5.log','independent_small.log',
            'independent_small.json','core2.log','core2.json','core2_named.json',
            'charging.log','charging_named.json','charging_summary.json',
            'charging_witnesses.json','failure_checks.log',
            'milp_2026101982.log','milp_2026101982.json']
files=sorted(Path(p) for p in source_names+data_names)
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
Path('SHA256SUMS').write_text(''.join(h+'  '+p+'\n' for p,h in hashes.items()))
print('P6_AUDIT_PASS')
