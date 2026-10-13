from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];C=json.loads((R/'01_script/Production_Config.json').read_text());paths=set()
for e in C['elements']:
 for key in ['image','svg','png']:
  if e.get(key):paths.add(e[key])
 if e.get('extra',{}).get('asset'):paths.add(e['extra']['asset'])
paths.update(['03_founder/Original_Camera_Take.mov','04_audio/Founder_Dialogue.wav','00_references/final_powerpoint/Community_Dark_Original_Motion.mkv','05_graphics/01_wordmark.svg','05_graphics/01_wordmark.png'])
M=[]
for name in sorted(paths):
 p=R/name;h=hashlib.sha256(p.read_bytes()).hexdigest();M.append({'asset':name,'sha256':h,'bytes':p.stat().st_size})
(R/'01_script/Asset_Manifest.json').write_text(json.dumps(M,indent=2))
settings=json.loads((R/'01_script/Cinematic_Settings.json').read_text());settings.pop('status',None)
inputs={'settings':settings,'source_assets':M,'config':C,'scripts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'scripts').glob('*.py'))}}
(R/'01_script/Build_Fingerprint.json').write_text(json.dumps({'sha256':hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest(),'inputs':inputs},indent=2))
print('Recorded active assets, source hashes, configuration and script fingerprint')
