"""Run on fejer to record exact output counts and SHA256 hashes."""
import hashlib, json
from pathlib import Path


def main():
    files = [*Path('.').glob('*.py'), Path('P9_REPORT.md'),
             *[Path(s) for s in ['probe901.json', 'sidon_examples.jsonl', 'audit910.json',
                                  'algebra.json', 'hill911.json', 'families.jsonl', 'periodic.json']]]
    hashes = {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(files)}
    family = [json.loads(s) for s in Path('families.jsonl').read_text().splitlines()]
    audit = json.loads(Path('audit910.json').read_text())
    hill = json.loads(Path('hill911.json').read_text())
    output = dict(status='FINITE CHECK: zero failures of asserted inequalities',
                  remote='fejer:~/wilf/p9/p18/',
                  commands=['nice -n 10 ~/mathenv/bin/python audit.py --maxm 18 --trials 15000 --seed 910',
                            'nice -n 10 ~/mathenv/bin/python hill.py --seed 911 --chains 100 --steps 120',
                            'nice -n 10 ~/mathenv/bin/python algebra.py',
                            'nice -n 10 ~/mathenv/bin/python families.py',
                            'nice -n 10 ~/mathenv/bin/python periodic.py'],
                  audit_counts=audit['counts'], hill_counts=hill['counts'],
                  family_count=len(family)-1, family_counts=family[-1]['counts'],
                  maximum_family_m=max(x['m'] for x in family[:-1]),
                  all_family_yz_multi=all(x['yz_multi'] for x in family[:-1]),
                  preserved_false_candidates=audit['failures'],
                  algebra=json.loads(Path('algebra.json').read_text()), sha256=hashes)
    assert not family[-1]['failures']
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
