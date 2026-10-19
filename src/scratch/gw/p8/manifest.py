"""Record reproducibility hashes on fejer; no mathematical inference."""
import hashlib,json,platform
from pathlib import Path

files=sorted([*Path('.').glob('*.py'),*Path('.').glob('*.c'),
              *Path('.').glob('*.md'),*Path('results').glob('*.json'),
              *Path('results').glob('*.log')])
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
out=dict(python=platform.python_version(),system=platform.system(),
         work_directory=str(Path.cwd()),sha256=hashes)
Path('MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
print('Recorded',len(hashes),'files; Python',platform.python_version())
