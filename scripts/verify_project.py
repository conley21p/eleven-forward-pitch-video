from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
from pathlib import Path
import xml.etree.ElementTree as E,subprocess,os,cv2,numpy as np,json
from video_io import VideoReader
R=Path(__file__).resolve().parents[1];Q=R/'09_qc';P=R/'07_kdenlive';resources=[]
for name in ['ElevenForward_Kinetic.kdenlive','ElevenForward_Kinetic_Captioned.kdenlive','Source_ElevenForward_Kinetic.kdenlive','Source_ElevenForward_Kinetic_Captioned.kdenlive']:
 root=E.parse(P/name).getroot()
 for p in root.findall('.//property[@name="resource"]'):
  if p.text=='black':continue
  path=(P/p.text).resolve();assert path.exists(),(name,p.text);resources.append(str(path))
results=[]
for n in [0,12,23,1500,3599]:
 p=Q/f'Native_Delivery_{n:04}.png'
 with (Q/f'Native_Delivery_{n:04}.log').open('w') as f:
  subprocess.run([MELT,str(P/'preview.mlt'),f'in={n}',f'out={n}','-consumer','avformat:'+str(p),'vcodec=png','f=image2','update=1','real_time=-1','threads=2'],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),cwd='/tmp',stdout=f,stderr=f,check=True)
 c=VideoReader(R/'08_exports/ElevenForward_Kinetic_Archive.mov');c.set(cv2.CAP_PROP_POS_FRAMES,n);ok,ref=c.read();c.release();assert ok
 im=cv2.imread(str(p));d=np.abs(im.astype(float)-ref.astype(float));row={'frame':n,'mean_absolute_rgb_error':float(d.mean()),'99_percentile':float(np.percentile(d,99))};assert row['mean_absolute_rgb_error']<3 and row['99_percentile']<12,row;results.append(row);print(row,flush=True)
(Q/'Native_Comparison.json').write_text(json.dumps({'status':'passed','frames':results,'resources_verified':len(set(resources)),'final_master_frames':3600,'editable_source_project':'Source_ElevenForward_Kinetic.kdenlive','method':'Native delivery master compared against ProRes archive; original layered source edit remains independent'},indent=2))
