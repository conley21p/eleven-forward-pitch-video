from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Direct original 4K source; modest waist crop and spatial right-side blur, no person matte."""
from video_io import VideoReader
from pathlib import Path
import cv2,numpy as np,subprocess,json,hashlib,sys,time,csv
R=Path(__file__).resolve().parents[1];Q=R/'09_qc';FF=FFMPEG;N=3851;cv2.setNumThreads(3)
SOURCE=R/'03_founder/Original_Camera_Take.mov'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
locked=json.loads((R/'01_script/Locked_Source_SHA256.json').read_text());assert sha(SOURCE)==locked['camera'];assert sha(R/'04_audio/Founder_Dialogue.wav')==locked['dialogue']
settings=json.loads((R/'01_script/Cinematic_Settings.json').read_text());settings['source_hashes']=locked
CROP_W,CROP_H=settings['crop_size'];CROP_Y=settings['crop_y'];OPEN_X=settings['opening_x'];MAIN_X=settings['main_x']
def ease(v):v=np.clip(v,0,1);return v*v*(3-2*v)
def amount(n):
 a,b=settings["opening_move_frames"];c,d=settings["closing_move_frames"]
 return float(ease((n-a)/(b-a))-ease((n-c)/(d-c)))
def crop_x(n):return OPEN_X+(MAIN_X-OPEN_X)*amount(n)
xweight=ease((np.arange(1920,dtype=np.float32)-880)/280)[None,:,None]
def encoder(p):
 return subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264rgb','-crf','0','-preset','medium','-pix_fmt','bgr24','-color_primaries','bt709','-color_trc','bt709','-threads','4',str(p)],stdin=subprocess.PIPE)
def render(test=False):
 cap=VideoReader(SOURCE);a=0;b=120 if test else N;raw=None;enc=None if test else encoder(R/'03_founder/Founder_Gradient_30fps.mkv');decoded=-1;last=None;rows=[];samples=[];start=time.time()
 for n in range(a,b):
  pts=np.asarray(json.loads((R/'01_script/Source_Frame_Timestamps.json').read_text())) if n==a else pts
  srcidx=min(len(pts)-1,max(0,int(np.searchsorted(pts,n/30,side='right')-1)))
  while decoded<srcidx:
   ok,last=cap.read();assert ok,(n,srcidx,decoded);decoded+=1
  x=crop_x(n);matrix=np.array([[CROP_W/1920,0,x+(CROP_W/1920-1)/2],[0,CROP_H/1080,CROP_Y+(CROP_H/1080-1)/2]],dtype=np.float64);frame=cv2.warpAffine(last,matrix,(1920,1080),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP);weight=xweight*amount(n)
  if amount(n)>0:
   blurred=cv2.GaussianBlur(frame,(0,0),4);out=np.clip(frame.astype(np.float32)*(1-weight)+blurred*weight,0,255).astype(np.uint8)
   out[:,:881]=frame[:,:881]
  else:out=frame
  if enc:enc.stdin.write(out.tobytes())
  rows.append([n,n/30,srcidx,x,CROP_Y,CROP_W,CROP_H])
  if n in [30,90,105,600,645,1020,1740,1770,1790,2400,3090,3450,3570,3591,3630]:
   cv2.imwrite(str(Q/f'Founder_Source_{n:04}.png'),frame);cv2.imwrite(str(Q/f'Founder_Gradient_{n:04}.png'),out);samples.append(n)
  if n%300==0:print('Founder source crop + spatial blur',n/30,flush=True)
 cap.release()
 for p in [raw,enc]:
  if p:p.stdin.close();assert p.wait()==0
 with (R/'01_script'/('Framing_Test.csv' if test else 'Actual_Framing.csv')).open('w') as f:w=csv.writer(f);w.writerow(['frame','time','source_frame','crop_x','crop_y','crop_w','crop_h']);w.writerows(rows)
 (Q/'Founder_Render.json').write_text(json.dumps({'status':'rendered','frames':len(rows),'samples':samples,'elapsed_seconds':time.time()-start,'settings':settings},indent=2));print('Founder complete',len(rows),flush=True)
if __name__=='__main__':render('--test' in sys.argv)
