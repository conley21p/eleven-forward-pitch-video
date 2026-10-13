"""Restore oversized media after git lfs pull, verifying every part and output."""
from pathlib import Path
import hashlib,json,os
R=Path(__file__).resolve().parents[1]
for item in json.loads((R/'media_parts/manifest.json').read_text()):
    target=R/item['path']
    if target.exists() and target.stat().st_size==item['bytes']:
        print('Present:',item['path']); continue
    target.parent.mkdir(parents=True,exist_ok=True)
    temporary=target.with_name(target.name+'.restoring'); total=hashlib.sha256()
    try:
        with temporary.open('wb') as output:
            for part in item['parts']:
                source=R/part['path']; digest=hashlib.sha256(); size=0
                with source.open('rb') as f:
                    while data:=f.read(8*1024**2):
                        output.write(data);total.update(data);digest.update(data);size+=len(data)
                assert size==part['bytes'] and digest.hexdigest()==part['sha256'], 'Download missing/corrupt: '+part['path']
        assert temporary.stat().st_size==item['bytes'] and total.hexdigest()==item['sha256']
        os.replace(temporary,target);print('Restored:',item['path'])
    except BaseException:
        temporary.unlink(missing_ok=True);raise
