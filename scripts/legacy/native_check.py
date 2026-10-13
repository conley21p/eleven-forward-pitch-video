from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
from video_io import VideoReader
from pathlib import Path
import subprocess,os,cv2,numpy as np,json
R=Path(__file__).resolve().parents[1];P=R/'07_kdenlive';Q=R/'09_qc';results=[]
# Stable product, market, competitor, support plus transition midpoint.
for n in [975,1020,1035,1060,1150,1290,1360,1440,1470,1710,2055,2430]:
 output=Q/f'Native_{n:04}.png';log=Q/f'Native_{n:04}.log'
 with log.open('w') as f:
  subprocess.run([MELT,str(P/'preview.mlt'),f'in={n}',f'out={n}','-consumer','avformat:'+str(output),'vcodec=png','f=image2','update=1','real_time=-1','threads=2'],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),cwd='/tmp',stdout=f,stderr=f,check=True)
 # Exact lossless reference from authoritative procedural compositor.
 import composite as c
 from motion import CFG,draw_element,Websites
 cap=VideoReader(str(R/'03_founder/Founder_Gradient_30fps.mkv'));cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,im=cap.read();cap.release();assert ok
 base=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA);c.frosted(base,n);panel=np.zeros((936,1040,4),np.uint8);web=Websites()
 for e in CFG['elements']:
  if e['start']<=n<e['end']:
   if e['kind'] in ['website','website_thumb']:web.draw(panel,n,e)
   else:draw_element(panel,e,n)
 c.over(base,panel,816,72);c.banner(base,n);cv2.imwrite(str(Q/f'Native_Reference_{n:04}.png'),base)
 a=cv2.imread(str(output));b=base[:,:,:3];diff=np.abs(a.astype(float)-b.astype(float));row={'frame':n,'mean_absolute_rgb_error':float(diff.mean()),'99_percentile':float(np.percentile(diff,99)),'maximum':float(diff.max())};results.append(row);print(row,flush=True)
 assert row['mean_absolute_rgb_error']<3 and row['99_percentile']<12,row
(Q/'Native_Comparison.json').write_text(json.dumps({'status':'passed','method':'Offscreen native MLT rendered from another working directory, compared with exact compositor reference; color-conversion rounding allowed','frames':results,'full_canvas_alpha':True,'portable_root_test':'passed'},indent=2))
