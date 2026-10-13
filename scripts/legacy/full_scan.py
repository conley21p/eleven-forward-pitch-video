from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Decode entire clean export and inspect every graphics-alpha frame against allowed windows."""
from pathlib import Path
import cv2,numpy as np,json,subprocess
from video_io import VideoReader
R=Path(__file__).resolve().parents[1];Q=R/'09_qc';C=json.loads((R/'01_script/Production_Config.json').read_text())
p=R/'08_exports/ElevenForward_Kinetic_Clean_WORKING.mp4'
if not p.exists():p=R/'08_exports/ElevenForward_Kinetic_Clean.mp4'
cap=VideoReader(p);count=0;black=[];sample=[]
while True:
 ok,im=cap.read()
 if not ok:break
 if im.mean()<2:black.append(count)
 if count%30==0:sample.append({'frame':count,'mean_luminance':float(im.mean())})
 count+=1
cap.release();assert count==3851 and not black,(count,black)
layers=json.loads((R/'01_script/Rendered_Layers.json').read_text());alpha_counts={}
for e in layers+[{'name':'Dark surfaces','asset':'05_graphics/motion/Dark_Surfaces.mov','start':0,'end':3851}]:
 process=subprocess.Popen([FFMPEG,'-v','error','-i',str(R/e['asset']),'-vf','alphaextract','-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
 n=e['start'];nonempty=0
 while True:
  raw=process.stdout.read(1920*1080)
  if not raw:break
  assert len(raw)==1920*1080
  mask=np.frombuffer(raw,np.uint8).reshape(1080,1920)
  if mask.max():
   nonempty+=1;assert 120<=n<3240,(e['name'],n)
   assert not mask[:,:816].any(),(e['name'],n,'crossed founder region')
   assert not mask[1008:,:].any(),(e['name'],n,'caption clearance')
  n+=1
 process.stdout.close();assert process.wait()==0;assert n==e['end'],(e,n);alpha_counts[e['name']]={'frames':n-e['start'],'nonempty':nonempty}
# Last1:48 onward consists only of original founder (captions are a separate accessibility export).
assert all(e['end']<=3240 for e in layers)
(Q/'Full_Scan.json').write_text(json.dumps({'status':'passed','decoded_frames':count,'black_frames':black,'every_layer_alpha_frame_checked':alpha_counts,'editorial_graphics_clear_at':108,'samples':sample},indent=2));print('Complete video and every overlay-alpha frame passed')
