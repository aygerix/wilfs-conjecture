"""Audit P6b finite bases, polynomial certificates, actual witnesses.
Run on fejer only, after all substantive jobs finish. No optimizer.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import re,json,hashlib,platform,sys

root=Path('.')
assert not Path('MAXCL_COUNTEREXAMPLE.json').exists()
report=Path(sys.argv[1]) if len(sys.argv)>1 else Path('P6B_REPORT.md')
assert report.exists()
def data(name):return json.loads(Path(name+'.json').read_text())
def fields(line):return {k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
def marker(file,word):assert word in Path(file+'.log').read_text(),(file,word)

marker('core3','CORE3_SUMMARY');marker('shape3','SHAPE3_ALL_PASS')
line=next(l for l in Path('core3.log').read_text().splitlines() if l.startswith('CORE3_SUMMARY'))
c3=fields(line)
assert c3==dict(shapes=2246,rows=11,nominal_vectors=6941,injective_vectors=112,
               phases=1700,realized_rows=9,max_cr_threshold=25,min=39,FAILURES=0)
c3ind=data('core3_independent')
assert [(z['m'],z['ordered_injections'],z['phases'],z['min_slack']) for z in c3ind]==[
    (14,24,336,39),(15,168,2520,52),(17,32,544,69)]
assert sum(z['ordered_injections'] for z in c3ind)==2*c3['injective_vectors']
assert sum(z['phases'] for z in c3ind)==2*c3['phases']
sh=data('shape3');assert sh['shadow']=={'0':0,'1':1,'2':2,'3':4,'4':5,'5':7,'6':10}
assert len(sh['bad'])==5 and len(sh['equality3'])==3
marker('core3_independent','CORE3_INDEPENDENT_PASS')

one=[]
for l in Path('one_cubic4.log').read_text().splitlines():
    if l.startswith('ONE_CUBIC4 m='):
        z=fields(l);assert z['vectors']==comb(z['m']-1,4) and z['FAILURES']==0;one.append(z)
assert [z['m'] for z in one]==list(range(21,28))
oi=data('one_cubic4_independent')
for a,b in zip(one,oi):
    assert a['m']==b['m'] and 6*a['injections']==b['ordered_injections']
    assert 6*a['phases']==b['phases']
    assert a['injections']==0 or a['min']==b['min_slack']>=0
assert sum(z['injections'] for z in one)==3028
assert sum(z['phases'] for z in one)==79180
marker('one_cubic4','ONE_CUBIC4_PASS');marker('one_cubic4_independent','ONE4_INDEPENDENT_PASS')

tw=data('two_cubic45')['rows']
assert [(z['k'],z['m'],z['injections'],z['phases'],z['min_slack']) for z in tw]==[
    (4,21,24,504,147),(5,31,120,3720,420),(5,32,0,0,None)]
tw6=[fields(l) for l in Path('two_cubic6.log').read_text().splitlines() if l.startswith('TWO_CUBIC6 m=')]
p6=data('pair6_independent')
assert [z['m'] for z in tw6]==[43,44,45]
for a,b in zip(tw6,p6):
    assert a['m']==b['m'] and a['nodes']==b['nodes'] and a['bases']==b['bases']==0
    assert a['injections']==a['phases']==a['FAILURES']==0
marker('two_cubic45','TWO45_ALL_PASS');marker('two_cubic6','TWO_CUBIC6_PASS');marker('pair6_independent','PAIR6_INDEPENDENT_PASS')
f5=data('frontier_two5')['rows']
assert [(z['m'],z['instances'],z['phases'],z['min_slack']) for z in f5]==[(31,120,3720,420),(32,0,0,None)]
bin4=data('frontier_search')['rows'];assert [z['m'] for z in bin4]==[21,22,23,24]
assert all(z['instances']==0 for z in bin4)

for filename,word in [('dense_poly','DENSE_POLY_ALL_PASS'),('generic_density','GENERIC_DENSITY_ALL_PASS'),
                      ('certificate_tables','CERTIFICATE_TABLES_PASS'),('few_poly','FEW_POLY_ALL_PASS')]:marker(filename,word)
ct=data('certificate_tables')
for row in ct.values():
    p=row['poly'];A=row['shift'];L=row['denominator'];cf=row['coeff']
    assert L>0 and all(x>0 for x in cf)
    assert cf==[sum(p[j]*comb(j,i)*A**(j-i) for j in range(i,len(p))) for i in range(len(p))]
fp=data('few_poly')
for tag in ('2','3'):
    z=fp[tag];p=z['poly4'];A=z['shift'];cf=z['coeff4']
    assert all(x>0 for x in cf)
    assert cf==[sum(p[j]*comb(j,i)*A**(j-i) for j in range(i,len(p))) for i in range(len(p))]
assert all(z['CR']>=0 for z in fp['small'])

sc=[fields(l) for l in Path('shadow_cover.log').read_text().splitlines() if l.startswith('SHADOW_COVER k=')]
assert [z['k'] for z in sc]==list(range(1,7))
assert all(z['graphs']==1<<comb(z['k']+1,2) and z['min']==z['FAILURES']==0 for z in sc)
marker('shadow_cover','SHADOW_COVER_ALL_PASS')
pack=data('packing_checks');marker('packing_checks','PACKING_CHECKS_ALL_PASS')
assert pack['seed']==2026101991 and pack['trials']==1200
assert pack['stats']['tiles']==1228 and pack['stats']['phase_checks']==119462
named={z['name']:z for z in pack['named']}
assert named['E47']['min_slack']==90 and named['E51']['min_slack']==104
assert named['NO_FULL_Q_FALSE_B2']['m']==6 and named['NO_FULL_Q_FALSE_B2']['min_slack']==10
assert named['CR_TABLE_CORRECTION']['min_slack']==147 and named['CR_TABLE_CORRECTION']['CR']==-5
assert named['HYBRID_UNPAID']['min_slack']==473 and named['HYBRID_UNPAID']['CR']==-12 and named['HYBRID_UNPAID']['FLAT_CR']==-83
assert len(pack['unpaid'])==2 and all(z['min_slack']>=0 for z in pack['unpaid'])
amin=data('adversary_min');marker('adversary_min','ADVERSARY_MIN_PASS')
assert amin['m']==16 and amin['CR']==-2 and amin['FLAT_CR']==-33 and amin['min_slack']==78
assert amin['elementary_profiles_below16']==405 and amin['negative_profiles_below16']==[]

out=dict(status='PASS',python=platform.python_version(),core3=c3,core3_independent=c3ind,
         one_cubic4=one,one_cubic4_independent=oi,two_cubic45=tw,pair6=p6,
         dense_certificates=ct,shadow_graphs=sc,packing_stats=pack['stats'],
         unpaid_examples=pack['unpaid'],minimal_scalar_failure=amin,binary4_excluded=bin4,
         report_sha256=hashlib.sha256(report.read_bytes()).hexdigest())
Path('P6B_AUDIT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
files=sorted(p for p in root.iterdir() if p.suffix in ('.c','.py','.json','.log','.md') and p.name not in
             ('P6B_AUDIT.json','audit.log','P6B_REPORT.md'))
Path('SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files))
print('CORE3',c3)
print('ONE4',sum(z['injections'] for z in one),sum(z['phases'] for z in one))
print('TWO45',[(z['k'],z['m'],z['injections'],z['phases']) for z in tw])
print('PACKING_STATS',json.dumps(pack['stats'],sort_keys=True))
print('P6B_AUDIT_PASS')
