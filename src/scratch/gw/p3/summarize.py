"""Aggregate completed verification logs. Run only on fejer."""
import csv,hashlib,json,pathlib,platform,subprocess

root=pathlib.Path(__file__).resolve().parent
out={"machine":"fejer", "python":platform.python_version(),"compiler":subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],"exhaustive":{},"independent":{}}
expected={"proof_res_d2.csv":24,"proof_res_d3.csv":18,"proof_res_d4.csv":14,"proof_nores_d2.csv":24,"proof_nores_d3.csv":14,"proof_nores_d4.csv":11}
for name,last in expected.items():
    rows=list(csv.DictReader((root/name).open()))
    assert int(rows[-1]['m'])==last,(name,'unfinished',rows[-1]['m'])
    assert 'high_lemma_checks' in rows[0],(name,'old scanner')
    keys=['labeled_shapes','instances','residue_complete','P3fail','Kge4fail','LP3fail','TCI3fail','K3_lemma_checks','high_lemma_checks','carried_pair_checks','cubic_charges','column_charges']
    totals={key:sum(int(row[key]) for row in rows) for key in keys}
    totals.update(d=int(rows[0]['d']),m_first=int(rows[0]['m']),m_last=last,mode=int(rows[0]['mode']))
    assert totals['Kge4fail']==0
    if totals['mode']:assert totals['P3fail']==totals['LP3fail']==totals['TCI3fail']==0
    assert totals['carried_pair_checks']==totals['cubic_charges']+totals['column_charges']
    out['exhaustive'][name]=totals
for name in ['independent_d2.log','independent_d3.log','independent_d4.log','independent_random.log']:
    js=[json.loads(line) for line in (root/name).read_text().splitlines() if line.startswith('{')]
    out['independent'][name]=js[-1]
    if 'd' in js[-1]:
        rr=list(csv.DictReader((root/f"proof_res_d{js[-1]['d']}.csv").open()))
        rr=[r for r in rr if int(r['m'])<=js[-1]['m']]
        assert sum(int(r['instances']) for r in rr)==js[-1]['total']
        assert sum(int(r['high_lemma_checks']) for r in rr)==js[-1]['high']
        assert sum(int(r['K3_lemma_checks']) for r in rr)==js[-1]['low']
for name in ['closure.log','closure_highdim.log']:
    out[name]=(root/name).read_text().splitlines()[-1]
out['totals']={
    'residue_complete_instances':sum(x['instances'] for x in out['exhaustive'].values() if x['mode']),
    'no_residue_instances':sum(x['instances'] for x in out['exhaustive'].values() if not x['mode']),
    'no_residue_high_checks':sum(x['high_lemma_checks'] for x in out['exhaustive'].values() if not x['mode']),
    'no_residue_carried_pairs':sum(x['carried_pair_checks'] for x in out['exhaustive'].values() if not x['mode']),
    'independent_exhaustive_instances':sum(x['total'] for x in out['independent'].values() if 'total' in x),
}
out['source_sha256']={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ['p3scan.c','verify_proof.py','closure_test.py','summarize.py']}
result=json.dumps(out,indent=2,sort_keys=True)
(root/'verification_summary.json').write_text(result+'\n')
print(result)
