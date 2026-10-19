"""Aggregate only completed fejer logs and independently evaluate examples.
Run on fejer. Logs are canonical-shape (not orbit-weighted) counts.
"""
import hashlib
import json
import re
from pathlib import Path
from explore import simplex, stats


def aggregate(filename, first, last):
    rows=[];high=[]
    for line in Path(filename).read_text().splitlines():
        row={k:int(v) for k,v in re.findall(r'([A-Za-z_][A-Za-z_0-9]*)=(\d+)',line)}
        if line.startswith('d='):rows.append(row)
        if line.startswith('H4='):high.append(row)
    assert [r['m'] for r in rows]==list(range(first,last+1)),filename
    assert len(rows)==len(high),filename
    fields=['instances','K4','quadratic','no_A','saturated_rho0','short_members',
            'carry_units','A_le2','A2_negative_face','A_le3','A3_negative_face']
    ans={key:sum(row[key] for row in rows) for key in fields}
    ans.update({key:sum(row[key] for row in high) for key in high[0]})
    ans.update(d=rows[0]['d'],first=first,last=last)
    return ans


def examples():
    ex=[]
    for d,k,n in [(2,3,(16,17)),(3,4,(52,52,52))]:
        D=simplex(d,k);s=stats(D,n,len(D));assert s['slack']==-1
        ex.append(s)
    # Full simplex in dimension two at the q=35 sharpness scale holds.
    D=simplex(2,4);assert stats(D,(52,52),35)['slack']==0
    # Exact tight two-generator example.
    D={(j,) for j in range(5)};tight=stats(D,(6,),5);assert tight['slack']==0
    ex.append(tight)
    # All class-E completions, including rho near m; W=rho.
    starchecks=0
    for m in range(2,101):
        for rho in range(m-1):
            n=tuple(z for z in range(4*m-rho,5*m-rho) if z%m)
            d=m-1;D={(0,)*d}|{tuple(int(j==k) for j in range(d)) for k in range(d)}
            st=stats(D,n,m);assert st['slack']==rho;starchecks+=1
    ex.append(dict(class_E_family_checks=starchecks,mfirst=2,mlast=100))
    m=23;A=(35,37);c=4*m;S=[False]*(c+m);S[0]=True
    for z in range(1,c):S[z]=any(z>=w and S[z-w] for w in (m,)+A)
    for z in range(c,c+m):S[z]=True
    ap=[next(z for z in range(r,c+m,m) if S[z]) for r in range(m)]
    face={sum(xi*ni for xi,ni in zip(x,A)) for x in simplex(2,3)}
    extra=tuple(z for z in ap if z not in face);nn=A+extra;d=len(nn)
    D={x+(0,)*len(extra) for x in simplex(2,3)}
    D.update(tuple(int(j==k) for j in range(d)) for k in range(2,d))
    from explore import independent_verify
    st=independent_verify(D,nn);assert st['WA']==-1 and st['slack']>=0
    ex.append(dict(EF_m23=st))
    return ex


def main():
    out=dict(residue=[aggregate('scan2_h4.log',3,24),aggregate('scan3_h4.log',4,18),
                      aggregate('scan4_h4.log',5,14)],
             noresidue=[aggregate('nores2.log',3,12),aggregate('nores3.log',4,9),
                        aggregate('nores4.log',5,7)],examples=examples())
    for f in ['tree28_h4.log','random_final.log','ef90_final.log','quad_final.log',
              'closure4_sharp.log']:
        out[f]=Path(f).read_text()
    sources=['p4_check.h','h4_check.h','p4_scan.c','p4_tree.c','explore.py','closure4.py','summarize.py']
    out['sha256']={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in sources}
    Path('verification_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['random_final.log','sha256']},indent=2))


if __name__=='__main__':main()
