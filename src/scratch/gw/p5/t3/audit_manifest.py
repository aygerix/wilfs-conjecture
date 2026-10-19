"""Record final research sources, data, logs and versions. fejer only."""
from pathlib import Path
import hashlib,json,re,sys,subprocess
import numpy,scipy
sources='two_low.h multi_low.h two_semigroups.c two_tiles.c frontier_adversary.c read_sparse.c symbolic_two.py identities.py three_low_table.py three_profiles.py three_profiles.c verify_saved.py compress_counter.py audit_manifest.py'.split()
data='compressed_counter.json cold_mixed_minimal.json a7_beta3.json a7_beta3_C.json three_tile_fixture.json frontier_best.json semigroup_alpha2_mode0_min_p.json tile_fixed_negative.json'.split()
profiles='three_profiles_survivors.json three_profiles_survivors_13.json'.split()
assert json.loads(Path(profiles[0]).read_text())==[z for z in json.loads(Path(profiles[1]).read_text()) if z['a']>=14]
logs='two_semigroups_final.log multi_semigroups_final.log multi_large.log three_semigroups_sharp.log four_semigroups_window.log two_tiles_targeted.log three_tiles_sharp.log frontier_alpha4.log symbolic_two.log three_low_table.log identities.log three_profiles.log three_profiles_c.log three_profiles13.log three_profiles13_c.log independent_final.log independent_boundaries.log frontier_validate.log compress_counter.log compressed_verify.log uniform_hloc_boundaries.log uniform_hloc_check.log'.split()
entries=[]
for label,files in (('',sources),('fixtures/',data),('',profiles),('logs/',logs)):
    for fn in files:
        p=Path(fn);assert p.is_file(),fn
        entries.append(dict(path=label+fn,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
semilogs=logs[:5]
counts={fn:int(re.search(r'^seed=.* actual=(\d+)',Path(fn).read_text(),re.M).group(1)) for fn in semilogs}
out=dict(python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,
    gcc=subprocess.check_output(['gcc','--version'],text=True).splitlines()[0],
    primary_semigroup_instances_main_runs=counts,total_primary_semigroup_instances_main_runs=sum(counts.values()),
    auxiliary_HLOC_primary_instances=int(re.search(r'^seed=.* actual=(\d+)',Path('uniform_hloc_check.log').read_text(),re.M).group(1)),files=entries)
Path('MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
Path('SHA256SUMS').write_text(''.join(z['sha256']+'  '+z['path']+'\n' for z in entries))
print(json.dumps({k:v for k,v in out.items() if k!='files'},sort_keys=True),flush=True)
