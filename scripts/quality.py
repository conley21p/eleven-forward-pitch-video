"""Pixel-level founder comparison, independent of rendered intermediate."""
import cv2,numpy as np,json,csv
from founder import R,SOURCE,CROP_W,CROP_H,CROP_Y,crop_x,amount,xweight,sha,locked
from video_io import VideoReader
pts=np.asarray(json.loads((R/'01_script/Source_Frame_Timestamps.json').read_text()))
source=VideoReader(SOURCE);out=VideoReader(R/'03_founder/Founder_Gradient_30fps.mkv');results=[];decoded=-1;im=None
for n in [30,90,106,600,1140,1440,1710,2250,2700,3090,3216,3228,3240,3630]:
 idx=min(len(pts)-1,max(0,int(np.searchsorted(pts,n/30,side='right')-1)))
 while decoded<idx:
  ok,im=source.read();assert ok;decoded+=1
 M=np.array([[CROP_W/1920,0,crop_x(n)+(CROP_W/1920-1)/2],[0,CROP_H/1080,CROP_Y+(CROP_H/1080-1)/2]])
 expected=cv2.warpAffine(im,M,(1920,1080),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP)
 if amount(n)>0:
  w=xweight*amount(n);b=cv2.GaussianBlur(expected,(0,0),4);raw=expected.copy();expected=np.clip(expected.astype(np.float32)*(1-w)+b*w,0,255).astype(np.uint8);expected[:,:881]=raw[:,:881]
 out.set(cv2.CAP_PROP_POS_FRAMES,n);ok,actual=out.read();assert ok
 err=np.abs(actual.astype(float)-expected);assert err.max()==0,(n,err.max());results.append({'frame':n,'maximum_pixel_error':float(err.max())})
source.release();out.release()
rows=list(csv.DictReader((R/'01_script/Actual_Framing.csv').open()));assert len(rows)==3851
for row in rows:
 n=int(row['frame']);assert abs(float(row['crop_x'])-crop_x(n))<1e-8;assert float(row['crop_y'])==382
for label,p in [('camera',SOURCE),('dialogue',R/'04_audio/Founder_Dialogue.wav')]:assert sha(p)==locked[label]
(R/'09_qc/Founder_Source_Quality.json').write_text(json.dumps({'status':'passed','source_hashes':locked,'lossless_samples':results,'crop_rows_verified':len(rows),'tracking':False,'matting':False},indent=2))
print('14 pixel-identical original-source samples and all3851 crop rows verified')
