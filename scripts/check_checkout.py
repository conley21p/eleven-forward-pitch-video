"""Check native-project dependencies without rendering or changing the edit."""
from pathlib import Path
import xml.etree.ElementTree as E,json
R=Path(__file__).resolve().parents[1]; missing=[]; checked=0
for project in sorted((R/'07_kdenlive').glob('*')):
    if project.suffix not in ['.kdenlive','.mlt']:continue
    for prop in E.parse(project).iter('property'):
        if prop.get('name') not in ['resource','av.filename']:continue
        value=prop.text or ''
        if not value.startswith('../'):continue
        checked+=1
        if not (project.parent/value).exists():missing.append((project.name,value))
assert not missing, missing
print('All',checked,'native media and caption references resolve.')
