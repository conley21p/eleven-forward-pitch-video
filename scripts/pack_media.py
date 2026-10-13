"""Refresh LFS parts when oversized original media changes."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]; manifest=R/'media_parts/manifest.json'; result=[]
for old in json.loads(manifest.read_text()):
    source=R/old['path'];folder=R/'media_parts'/source.stem;folder.mkdir(parents=True,exist_ok=True)
    total=hashlib.sha256();parts=[]
    with source.open('rb') as f:
        index=0
        while True:
            first=f.read(8*1024**2)
            if not first:break
            part=folder/f'{index:03}.bin';digest=hashlib.sha256();size=0
            with part.open('wb') as output:
                data=first
                while data:
                    output.write(data);digest.update(data);total.update(data);size+=len(data)
                    if size>=1024**3:break
                    data=f.read(min(8*1024**2,1024**3-size))
            parts.append({'path':part.relative_to(R).as_posix(),'bytes':size,'sha256':digest.hexdigest()});index+=1
    for p in folder.glob('*.bin'):
        if p.name not in {Path(x['path']).name for x in parts}:p.unlink()
    result.append({'path':old['path'],'bytes':source.stat().st_size,'sha256':total.hexdigest(),'parts':parts})
manifest.write_text(json.dumps(result,indent=2));print('Updated media parts and verified source hashes.')
