"""Produce continuation artifacts on fejer; never run locally."""
from pathlib import Path
import json
import hashlib
import re
import subprocess
import sys
from continuation_probe import monos,completed,a4_checks
from explore import independent_verify


def main():
    m=74;h=37;n=(83,102,104,107);M=4*m+h-1
    core={x for x in monos(4,4) if sum(a*b for a,b in zip(x,n))<=M}
    D,nn=completed(core,n,m,h)
    original=independent_verify(D,nn);st=a4_checks(D,nn)
    assert len(core)==36 and st['WA']==-4 and st['W']==945 and st['k']==1
    case=dict(stats=st,n=nn,D=sorted(D))
    Path('quartic_counterexample.json').write_text(json.dumps(case,indent=2)+'\n')
    # Export exact coordinates to an independent C checker.
    cases=[case];art=json.loads(Path('completion_examples.json').read_text())
    cases.extend(x for x in art['best'] if x['stats']['m']<128 and len(x['n'])<128)
    with Path('cases.txt').open('w') as out:
        for item in cases:
            d=len(item['n']);out.write(f'{len(item["D"])} {d}\n')
            out.write(' '.join(map(str,item['n']))+'\n')
            for x in item['D']:out.write(' '.join(map(str,x))+'\n')
    logs=['a4_catalog.log','a5_catalog.log','a5_critical.log','uniform_lowcost.log',
          'packing_linear.log','packing_fibers.log','packing_fibers_hp.log',
          'tree28_a4.log','tree28_a5.log','tree28_fiber_noinline.log','tree28_fiber_stack.log',
          'tree12_fiber_asan.log','stack_usage.log','scan4_a4.log','scan4_fiber.log',
          'hd4_nores3.log','hd4_nores4.log',
          'hd4_closure31.log','hd4_closure30.log','quartic_min_full.log',
          'completions.log','completions_B.log','completions_a5.log','a5_stars.log',
          'completions_a6.log','cases_check.log','a6_catalog.log','a6_reduction_check.log',
          'a6_critical_before_hp.log','a6_critical_after_hp.log','a6_critical_b11.log',
          'a6_count_check.log','a6_one_pair.log','a6_one_pair_py.log',
          'a7_m107.log','a7_m108.log','a7_independent.log']
    summary={f:Path(f).read_text() for f in logs}
    summary['quartic_counterexample']=st
    summary['saved_cases']=len(cases)
    parent=Path(__file__).resolve().parent.parent
    # Independent C/Python certificates must agree before archival.
    a6=json.loads(Path('a6_critical.json').read_text())
    c6=Path('a6_count_check.log').read_text().splitlines()[-1]
    fields={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',c6)}
    expected=dict(profiles=75,bmax=11,critical=a6['counts']['critical_vectors'],
                  A=a6['counts']['A_packing'],global_=a6['counts']['global_packing'],
                  HP=a6['counts']['complete_support_packing'],
                  forced=a6['counts'].get('forced_cubic_count',0),
                  deleted=a6['counts']['delete_pair_endpoints'],
                  good_B=a6['counts']['one_good_B_face'],survivors=a6['survivor_count'])
    expected['global']=expected.pop('global_')
    assert fields==expected,(fields,expected)
    py6=[json.loads(line) for line in Path('a6_one_pair_py.log').read_text().splitlines()]
    c6s=[dict((k,int(v)) for k,v in re.findall(r'(\w+)=(\d+)',line))
         for line in Path('a6_one_pair.log').read_text().splitlines() if line.startswith('SUMMARY')]
    assert len(c6s)==len(py6)==2
    for cc,pp in zip(c6s,py6):
        assert cc['rho']==pp['rho'] and cc['m']==pp['m']
        for ck,pk in [('nodes','nodes'),('pairsets','pair_sets'),('eligible','eligible'),('top_eligible','top_eligible')]:
            assert cc[ck]==pp['counts'].get(pk,0)
    c6cases=[]
    for line in Path('a6_one_pair.log').read_text().splitlines():
        if not line.startswith('CASE '):continue
        hit=re.fullmatch(r'CASE rho=(\d+) missing_pair=(\d+),(\d+) holes=(\d+) eligible_cubics=(\d+) t=([\d,]+)',line)
        assert hit,line
        rho,u,v,holes,good=map(int,hit.groups()[:5]);tt=tuple(map(int,hit.group(6).split(',')))
        c6cases.append((rho,(u,v),tt,holes,good))
    p6cases=[(item['rho'],tuple(case['omitted']),tuple(case['t']),len(case['holes']),case['good'])
             for item in py6 for case in item['cases']]
    assert sorted(c6cases)==sorted(p6cases)
    py7=[json.loads(line) for line in Path('a7_independent.log').read_text().splitlines()]
    c7s=[]
    for file in ['a7_m107.log','a7_m108.log']:
        for line in Path(file).read_text().splitlines():
            if line.startswith('SUMMARY'):
                c7s.append(dict((k,int(v)) for k,v in re.findall(r'(\w+)=(-?\d+)',line)))
    assert len(py7)==len(c7s)==12
    for cc,pp in zip(c7s,py7):
        assert (cc['m'],cc['rho'])==(pp['m'],pp['rho'])
        for field in ['eligible','top_eligible']:assert cc[field]==pp['counts'].get(field,0)
        assert cc['potential_W']==pp['potential_W']
        assert cc['minholes']==(pp['best']['holes'] if pp['best'] else pp['m'])
    summary['certificate_agreement']=dict(a6_count=fields,a6_weight_parameters=len(py6),
                                         a7_parameters=len(py7),
                                         a7_min_holes=min(x['best']['holes'] for x in py7 if x['best']))
    before=json.loads(Path('a6_critical_before_hp.json').read_text())
    summary['smallest_SP_only_survivor']=min(before['survivors'],key=lambda x:(x['m'],x['b']))
    assert summary['smallest_SP_only_survivor']['m']==148
    summary['nonempty_error_logs']={str(p):p.read_text() for p in Path('.').glob('*.err') if p.stat().st_size}
    summary['versions']=dict(python=sys.version,gcc=subprocess.check_output(['gcc','-dumpfullversion'],text=True).strip())
    sources=['a4_stability.py','a5_critical.py','uniform_lowcost.py','continuation_probe.py',
             'hd4_closure.py','quartic_face_search.c','a4_extra.h','a4_scan.c','a4_tree.c',
             'a4_cases.c','hd4_check.h','a5_star_probe.py','packing_fibers.py','fiber_check.h',
             'a6_critical.py','a6_count_check.c','a6_one_pair.c','a6_one_pair.py','a6_reduction_check.py',
             'a7_cover.c','a7_independent.py','continuation_summary.py','P4_REPORT.md']
    summary['sha256']={f:hashlib.sha256((Path(f) if Path(f).exists() else parent/f).read_bytes()).hexdigest() for f in sources}
    Path('continuation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(dict(quartic_counterexample=st,saved_cases=len(cases),
                         certificate_agreement=summary['certificate_agreement'],
                         nonempty_error_logs=list(summary['nonempty_error_logs'])),indent=2))


if __name__=='__main__':main()
