from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];base=R.parent
for name in ['Acceptance.json','Full_Scan.json','Founder_Source_Quality.json','Native_Comparison.json']:
 assert json.loads((R/'09_qc'/name).read_text())['status']=='passed',name
old=base/'CURRENT_REVISION.json';backup=R/'01_script/Previous_Current_Revision.json'
if not backup.exists():shutil.copy2(old,backup)
state={'status':'verified_airdrop_source_revision','name':'Eleven Forward · AirDropped original source','root':R.name,'native_project':R.name+'/07_kdenlive/ElevenForward_Kinetic.kdenlive','clean_video':R.name+'/08_exports/ElevenForward_Kinetic_Clean.mp4','captioned_video':R.name+'/08_exports/ElevenForward_Kinetic_Captioned.mp4','archive':R.name+'/08_exports/ElevenForward_Kinetic_Archive.mov','design_review':R.name+'/10_review/Review.html','duration':3851/30,'frames':3851,'fps':30,'source_take_untrimmed':True,'graphics_end':108,'additional_4_percent_crop_rendered':True,'previous_revision_preserved':'Speaker_Quality_Revision','independent_astra_review':'Not performed for this revision'}
old.write_text(json.dumps(state,indent=2));(R/'01_script/CURRENT_PRODUCTION.json').write_text(json.dumps(state,indent=2))
settings_path=R/'01_script/Cinematic_Settings.json';settings=json.loads(settings_path.read_text());settings['status']='verified_render';settings_path.write_text(json.dumps(settings,indent=2))
print('Promoted verified AirDrop_Source_Revision; previous revision preserved')
