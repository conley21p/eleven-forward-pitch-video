from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Retheme original moving artwork, preserving exact glyphs, counters and measured motion.
Source MP4 is immutable; this transformation and editable layout specification are retained.
"""
from pathlib import Path
import cv2,numpy as np,json,subprocess
from video_io import VideoReader
R=Path(__file__).resolve().parents[1];D=R/'00_references/final_powerpoint'
def render():
 cap=VideoReader(D/'media2.mp4');frames=[]
 while True:
  ok,im=cap.read()
  if not ok:break
  frames.append(im)
 cap.release();last=frames[-1].astype(np.float32)
 C=last[125,500];F=last[150,500];dark=np.array([18,23,15],np.float32);white=np.array([245,248,247],np.float32)
 # Header/footer coverage recovers source antialiasing while exchanging ink and paper.
 header=last.copy();coverage=np.clip(np.linalg.norm(header-C,axis=2)/np.linalg.norm(F-C),0,1)[:,:,None]
 base=dark*(1-coverage)+white*coverage;base[137:539]=dark
 for yy in [0,612]:
  for xx in [0,932]:base[yy:yy+28,xx:xx+28]=dark
 base[110:113,38:110]=[40,249,211]
 base[550:]=dark # Remove follower-count qualification footer.
 # New source colors, applied only to opaque row artwork after removing original fade.
 old=np.array([[*F,1],[228,240,243,1],[40,249,211,1],[170,190,173,1]],np.float32)
 new=np.array([[40,55,25],[245,248,247],[40,249,211],[161,180,166]],np.float32)
 transform=np.linalg.lstsq(old,new,rcond=None)[0]
 out=D/'Community_Dark_Original_Motion.mkv'
 enc=subprocess.Popen([FFMPEG,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','960x640','-r','30','-i','-','-an','-c:v','ffv1','-pix_fmt','bgr0',str(out)],stdin=subprocess.PIPE)
 profiles=[]
 for name,crop in [('louise',(290,0,830,540)),('mesha',None),('sara',(100,0,265,165))]:
  photo=cv2.imread(str(R/'00_references/community'/f'{name}_profile.jpg'))
  if crop is not None:
   a,b,c,d=crop;photo=photo[b:d,a:c]
  profiles.append(cv2.resize(photo,(80,80),interpolation=cv2.INTER_AREA))
 motion=[]
 for n,src in enumerate(frames):
  canvas=base.copy();r=[]
  for row,y in enumerate([137,276,415]):
   line=src[y+12].astype(float);a=np.clip(((line-C)*(F-C)).sum(1)/((F-C)**2).sum(),0,1);alpha=float(np.percentile(a[200:850],90));xs=np.where(a>max(.025,alpha*.8))[0]
   if not len(xs) or alpha<.025:r.append({'opacity':0,'x':None});continue
   x=int(xs[0])-1;w=min(885,960-x);patch=src[y:y+124,x:x+w].astype(np.float32)
   un=(patch-C*(1-alpha))/max(alpha,.001)
   mapped=np.clip(np.concatenate([un,np.ones((*un.shape[:2],1),np.float32)],2)@transform,0,255)
   # Discard original cream antialiasing at all edges before applying the new radius.
   mapped[:5]=new[0];mapped[-5:]=new[0];mapped[:,:5]=new[0]
   if w==885:mapped[:,-5:]=new[0]
   for cx,cy in [(32,32),(852,32),(32,91),(852,91)]:
    xa=max(0,cx-32);xb=min(w,cx+33);ya=max(0,cy-32);yb=min(124,cy+33)
    yy,xx=np.ogrid[ya:yb,xa:xb]
    edge=((xx-cx)**2+(yy-cy)**2>27**2) & ((xx<32) | (xx>852)) & ((yy<32) | (yy>91))
    mapped[ya:yb,xa:xb][edge]=new[0]
   pm=np.zeros((80,80),np.uint8);cv2.circle(pm,(40,40),39,255,-1,cv2.LINE_AA)
   pa=pm[:,:,None]/255
   mapped[22:102,16:96]=profiles[row]*pa+mapped[22:102,16:96]*(1-pa)
   mask=np.zeros((124,885),np.uint8);cv2.rectangle(mask,(32,0),(852,123),255,-1);cv2.rectangle(mask,(0,32),(884,91),255,-1)
   for xx in [32,852]:
    for yy in [32,91]:cv2.circle(mask,(xx,yy),32,255,-1,cv2.LINE_AA)
   blend=mask[:,:w,None]/255*alpha
   canvas[y:y+124,x:x+w]=mapped*blend+canvas[y:y+124,x:x+w]*(1-blend)
   r.append({'opacity':alpha,'x':x})
  enc.stdin.write(np.clip(canvas,0,255).astype(np.uint8).tobytes());motion.append({'frame':n,'rows':r})
 enc.stdin.close();assert enc.wait()==0
 (R/'01_script/Slide6_Measured_Motion.json').write_text(json.dumps(motion,indent=2))
 print('Rethemed',len(frames),'original frames; exact source counter progression retained')
if __name__=='__main__':render()
