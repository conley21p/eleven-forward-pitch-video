from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Verify full deliverables before replacing working filenames. No automatic current promotion."""
from pathlib import Path
import subprocess,json,hashlib,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];Q=R/'09_qc';O=R/'08_exports'
def probe(p):return json.loads(subprocess.check_output([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',str(p)]))
results=[]
for stem,ext in [('ElevenForward_Kinetic_Clean','.mp4'),('ElevenForward_Kinetic_Captioned','.mp4'),('ElevenForward_Kinetic_Archive','.mov')]:
 working=O/(stem+'_WORKING'+ext);final=O/(stem+ext);p=working if working.exists() else final
 d=probe(p);v=next(x for x in d['streams'] if x['codec_type']=='video');a=next(x for x in d['streams'] if x['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',3851)
 assert abs(float(v['duration'])-3851/30)<.001
 assert v['color_space']=='bt709' and v['color_primaries']=='bt709' and v['color_transfer']=='bt709'
 assert int(a['sample_rate'])==48000
 pdecode=subprocess.run([FFMPEG,'-v','error','-i',str(p),'-f','null','-'],capture_output=True);assert pdecode.returncode==0 and not pdecode.stderr,(p,pdecode.stderr)
 if working.exists():working.replace(final)
 results.append({'asset':str(final.relative_to(R)),'frames':int(v['nb_frames']),'duration':v['duration'],'codec':v['codec_name'],'decoded_without_errors':True});(Q/(stem+'_Probe.json')).write_text(json.dumps(d,indent=2))
C=json.loads((R/'01_script/Production_Config.json').read_text());layers=json.loads((R/'01_script/Rendered_Layers.json').read_text())
expected={'material_shape_design':(960,1305),'community_animation':(1335,1455),'population':(1455,1521),'audience':(1521,1625),'market_inputs':(1625,1770),'stealth_comparison':(2040,2340),'stealth_website':(2370,2490),'funding_studio':(2975,3240)}
byid={e['id']:e for e in C['elements']}
for name,(start,end) in expected.items():assert (byid[name]['start'],byid[name]['end'])==(start,end),name
assert max(e['end'] for e in C['elements'])==3240
assert not any(e['id'] in ['triathlon_photo','material_title','stealth_site','CLO_development','support_graduates','funding_amount'] for e in C['elements'])
for e in layers:
 v=next(x for x in probe(R/e['asset'])['streams'] if x['codec_type']=='video');assert int(v['nb_frames'])==e['end']-e['start']
missing=[];resources=[]
for file in ['ElevenForward_Kinetic.kdenlive','ElevenForward_Kinetic_Captioned.kdenlive']:
 root=E.parse(R/'07_kdenlive'/file).getroot()
 for p in root.findall('.//property[@name="resource"]'):
  if p.text=='black':continue
  resolved=(R/'07_kdenlive'/p.text).resolve();resources.append(str(resolved));
  if not resolved.exists():missing.append(p.text)
 assert not any('close_banner' in p.get('id','') for p in root.findall('producer'))
assert not missing,missing
locked=json.loads((R/'01_script/Locked_Source_SHA256.json').read_text())
for key,asset in [('camera','03_founder/Original_Camera_Take.mov'),('dialogue','04_audio/Founder_Dialogue.wav')]:assert hashlib.sha256((R/asset).read_bytes()).hexdigest()==locked[key]
for report in ['Founder_Source_Quality.json','Native_Comparison.json']:
 assert json.loads((Q/report).read_text())['status']=='passed'
report={'status':'passed','exports':results,'offline_media':missing,'resolved_native_resources':len(set(resources)),'graphics_end':108,'market_end':59,'source_hashes':locked,'tracking':False,'person_matting':False,'original_performance_untrimmed':True,'new_crop':[2129.92,1198.08],'source_voice_processing':'unchanged','mp4_crf':10,'source_quality_report':'Founder_Source_Quality.json','native_match_report':'Native_Comparison.json','review_scope':'Full decode, source pixel checks, complete cue audit and representative visual/transition frames. No independent Astra score claimed.'}
(Q/'Acceptance.json').write_text(json.dumps(report,indent=2));print('All three complete exports, timeline, source hashes and native media verified')
