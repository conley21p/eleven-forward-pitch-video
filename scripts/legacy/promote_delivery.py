from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];base=R.parent
for name in ['Acceptance.json','Native_Comparison.json','Founder_Source_Quality.json']:assert json.loads((R/'09_qc'/name).read_text())['status']=='passed',name
shutil.copy2(base/'CURRENT_REVISION.json',R/'01_script/Previous_Current_Revision.json')
state={'status':'verified_exact_two_minute_delivery','name':'Eleven Forward · Final two-minute pitch','root':R.name,'native_project':R.name+'/07_kdenlive/ElevenForward_Kinetic.kdenlive','editable_source_project':R.name+'/07_kdenlive/Source_ElevenForward_Kinetic.kdenlive','clean_video':R.name+'/08_exports/ElevenForward_Kinetic_Clean.mp4','captioned_video':R.name+'/08_exports/ElevenForward_Kinetic_Captioned.mp4','archive':R.name+'/08_exports/ElevenForward_Kinetic_Archive.mov','review_player':R.name+'/10_review/Review.html','poster':R.name+'/05_graphics/Playback_Poster.png','duration':120,'frames':3600,'fps':30,'playback_speed':3838/3600,'source_revision':'AirDrop_Source_Revision','source_end':3838/30,'pitch_preserved':True,'color_grading_applied':False,'source_performance_retained':'All spoken content; trailing silence trimmed','previous_revision_preserved':'AirDrop_Source_Revision'}
(base/'CURRENT_REVISION.json').write_text(json.dumps(state,indent=2));(R/'01_script/CURRENT_PRODUCTION.json').write_text(json.dumps(state,indent=2))
print('Promoted verified exact120-second delivery')
