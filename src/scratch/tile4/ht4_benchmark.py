#!/usr/bin/python3
"""VM-only timing/projection; estimates are not mathematical certificates."""
import sys
sys.dont_write_bytecode=True
import json
import math
from pathlib import Path
import resource
import socket
import subprocess
import time

HERE=Path(__file__).resolve().parent


def phi(n):return sum(math.gcd(a,n)==1 for a in range(1,n))


def fit(rows):
    # Normalize the oscillating number of primitive lattice orbits by m/phi(m).
    xx=[math.log(r['m']) for r in rows]
    yy=[math.log(r['cpu_seconds']*phi(r['m'])/r['m']) for r in rows]
    mx=sum(xx)/len(xx);my=sum(yy)/len(yy)
    slope=sum((x-mx)*(y-my) for x,y in zip(xx,yy))/sum((x-mx)**2 for x in xx)
    return my-slope*mx,slope


def main():
    assert socket.gethostname().split('.')[0]=='fejer'
    rows=[]
    for m in (16,20,24,28,32,36):
        prefix=HERE/f'ht4_benchmark_{m}'
        before=resource.getrusage(resource.RUSAGE_CHILDREN);start=time.monotonic()
        with prefix.with_suffix('.stdout').open('w') as out:
            subprocess.run([str(HERE/'ht4_scan'),str(m),'--exact','--threads','1','--out',str(prefix)],stdout=out,check=True)
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        result=json.loads(prefix.with_suffix('.json').read_text())
        row=dict(m=m,wall_seconds=time.monotonic()-start,
                 cpu_seconds=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime),
                 cones=result['cones'],lattices=result['lattices'],min_HCR=result['metrics']['min_HCR'])
        rows.append(row);print(json.dumps(dict(kind='benchmark',**row)),flush=True)
    estimates=[]
    fits=[fit(rows[-3:]),fit(rows[-5:])]
    observed_cpu_share=sum(r['cpu_seconds'] for r in rows[-3:])/sum(r['wall_seconds'] for r in rows[-3:])
    assumed_shared_cores=min(2.0,2*observed_cpu_share)
    for target in (100,150,200):
        models=[]
        for intercept,slope in fits:
            predict=lambda m:math.exp(intercept+slope*math.log(m))*m/phi(m)
            per_m=predict(target);total=sum(predict(m) for m in range(37,target+1))
            models.append(dict(exponent=slope,per_m_cpu_seconds=per_m,
                               cumulative_cpu_seconds=total,
                               cumulative_hours_two_available_cores=total/7200,
                               cumulative_hours_shared_VM=total/assumed_shared_cores/3600))
        estimates.append(dict(target=target,models=models))
    result=dict(host=socket.gethostname(),benchmarks=rows,models=estimates,
                assumed_production_threads=2,measured_single_thread_CPU_share=observed_cpu_share,
                assumed_effective_shared_cores=assumed_shared_cores,
                caution='Power-law extrapolation from m<=36; allow order-of-magnitude error and possible memory/fan-complexity barriers. No production m>=37 is started by this script.')
    (HERE/'ht4_cost_projection.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(kind='cost_projection',**result)),flush=True)
    lines=['# Compiled scanner cost projection','',
      'Each measurement uses one native thread, distinct-nonzero residues, full fan traversal, exact matched facets, exact GMP rational volume sums, and volume sums modulo both primes.',
      'Two power-law fits normalize lattice-count oscillations by m/phi(m). Estimates are empirical and may be wrong by an order of magnitude. They exclude validation and use no sampling in the completeness checks.','',
      '| target | fitted exponent range | CPU hours for m=37..target | wall hours with two available cores | wall hours at measured shared-VM throughput |',
      '|---:|:--|:--|:--|:--|']
    for row in estimates:
        mods=row['models']
        span=lambda k,scale=1:f"{min(z[k] for z in mods)/scale:.2g}–{max(z[k] for z in mods)/scale:.2g}"
        lines.append(f"| {row['target']} | {span('exponent')} | {span('cumulative_cpu_seconds',3600)} | {span('cumulative_hours_two_available_cores')} | {span('cumulative_hours_shared_VM')} |")
    (HERE/'HT4_COST.md').write_text('\n'.join(lines)+'\n')


if __name__=='__main__':main()
