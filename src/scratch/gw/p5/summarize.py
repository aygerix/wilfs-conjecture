"""Summarize already completed fejer checks. Execute on fejer."""
from pathlib import Path
import re
for name in ['scan2','scan3','scan4']:
    lines=Path(name+'.log').read_text().splitlines()
    total=sum(int(re.search(r' instances=(\d+)',s)[1]) for s in lines)
    print(name,'weight assignments=',total,'final:',lines[-1])
