"""Compare delivery compression against the unchanged lossless founder pixels."""
from video_io import VideoReader
from pathlib import Path
import cv2,numpy as np,json
R=Path(__file__).resolve().parents[1];old=R.parent/'Glowing_Belt_Revision/08_exports/ElevenForward_Kinetic_Clean.mp4';new=R/'08_exports/ElevenForward_Kinetic_Clean_WORKING.mp4'
if not new.exists():new=R/'08_exports/ElevenForward_Kinetic_Clean.mp4'
rows=[]
for n in [600,1440,2670]:
 ims=[]
 for p in [R/'03_founder/Founder_Gradient_30fps.mkv',old,new]:
  c=VideoReader(p);c.set(cv2.CAP_PROP_POS_FRAMES,n);ok,im=c.read();c.release();assert ok;ims.append(im[60:820,180:760])
 ref=ims[0].astype(float);row={'frame':n}
 for label,im in zip(['previous','revised'],ims[1:]):
  d=ref-im.astype(float);row[label]={'mean_absolute_error':float(np.abs(d).mean()),'psnr_db':float(10*np.log10(255**2/np.mean(d*d)))}
 canvas=np.concatenate(ims,axis=1);cv2.imwrite(str(R/'10_review'/f'Speaker_Quality_{n:04}.png'),canvas)
 rows.append(row);print(row,flush=True)
assert np.mean([x['revised']['psnr_db'] for x in rows])>np.mean([x['previous']['psnr_db'] for x in rows])
(R/'09_qc/Speaker_Encoding_Comparison.json').write_text(json.dumps({'status':'passed','reference':'Unchanged lossless founder intermediate, previously verified against original-source crops','layout':'left: source crop; middle: prior export; right: revised export','frames':rows,'limitation':'Cannot restore detail absent from the supplied source; no artificial face reconstruction or sharpening applied.'},indent=2))
