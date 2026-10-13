from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Native 30fps editable contour animation; source pixels remain unchanged."""
from pathlib import Path
from functools import lru_cache
import cv2,numpy as np,json,subprocess
R=Path(__file__).resolve().parents[1];G=R/'05_graphics';W,H=960,640
SOURCE=R/'00_references/final_powerpoint/Belt_Trace_Source.png'
# Exact source image is proportionally fitted; outline derives from its alpha.
SCALE=.44;LEFT=100;TOP=118;COLOR=(40,249,211)
def ease(x):x=np.clip(x,0,1);return x*x*(3-2*x)
def resample(p,step=1):
 p=np.asarray(p,np.float32);d=np.linalg.norm(np.diff(p,axis=0),axis=1);s=np.r_[0,np.cumsum(d)];q=np.linspace(0,s[-1],max(2,int(s[-1]/step)))
 return np.column_stack([np.interp(q,s,p[:,0]),np.interp(q,s,p[:,1])])
def cubic(a,b,c,d):
 t=np.linspace(0,1,60)[:,None];return (1-t)**3*np.array(a)+3*(1-t)**2*t*np.array(b)+3*(1-t)*t*t*np.array(c)+t**3*np.array(d)
@lru_cache(maxsize=1)
def assets():
 src=cv2.imread(str(SOURCE),-1);mask=(src[:,:,3]>120).astype(np.uint8)*255;contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);p=max(contours,key=cv2.contourArea)[:,0,:].astype(float)
 start=np.argmin(np.sum((p-[1490,52])**2,axis=1));p=np.roll(p,-start,axis=0)
 # Clockwise traversal: from top-right descend right edge before reaching bottom-left.
 if np.mean(p[1:120,0])<p[0,0]-10:p=np.r_[p[:1],p[:0:-1]]
 p=resample(np.r_[p,p[:1]],2)*SCALE+[LEFT,TOP]
 target=np.argmin(np.sum((p-([170*SCALE+LEFT,780*SCALE+TOP]))**2,axis=1))
 belt=cv2.resize(src,None,fx=SCALE,fy=SCALE,interpolation=cv2.INTER_AREA)
 pocket=np.concatenate([cubic((318,378),(320,505),(388,770),(466,851)),cubic((466,851),(512,908),(585,900),(750,910)),cubic((750,910),(815,922),(955,816),(1008,762)),cubic((1008,762),(1070,699),(1044,611),(1009,534)),cubic((1009,534),(980,443),(953,406),(932,375)),cubic((932,375),(763,424),(536,464),(334,444)),cubic((334,444),(324,427),(319,399),(318,378))])*SCALE+[LEFT,TOP]
 pocket=resample(pocket)
 return src,belt,p,target,pocket
@lru_cache(maxsize=1)
def text_layer():
 def tx(s,x,y,z=20,c='#F7F8F5',weight=400):return f'<text x="{x}" y="{y}" font-family="Arial" font-size="{z}" font-weight="{weight}" fill="{c}">{s}</text>'
 body=tx('RETHINKING THE CATEGORY',38,43,15,'#D3F928',700)+tx('Every detail has a purpose.',38,85,34,weight=700)
 for x,title,sub in [(38,'Material','Mesh texture'),(339,'Shape','Belt silhouette'),(640,'Design','Pocket + lime trim')]:body+=tx(title,x,590,23,weight=700)+tx(sub,x,621,16,'#A6B4A1')
 p=G/'svg/Belt_Trace_Labels.svg';p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640">{body}</svg>');out=G/'png/Belt_Trace_Labels.png'
 node=NODE;sharp=SHARP
 subprocess.run([node,'-e',f'require({json.dumps(sharp)})({json.dumps(str(p))}).png().toFile({json.dumps(str(out))})'],check=True)
 return cv2.imread(str(out),-1)
def over(dst,im,x=0,y=0,opacity=1):
 h,w=im.shape[:2];a=im[:,:,3:4]/255*opacity;dst[y:y+h,x:x+w,:3]=np.clip(im[:,:,:3]*a+dst[y:y+h,x:x+w,:3]*(1-a),0,255).astype(np.uint8)
def glow(dst,p,progress=1,opacity=1):
 p=np.asarray(p[:max(2,round(len(p)*min(1,max(0,progress))))],np.int32)
 mask=np.zeros((H,W),np.uint8);cv2.polylines(mask,[p],False,255,2,cv2.LINE_AA)
 strength=(cv2.GaussianBlur(mask,(0,0),9).astype(float)*2+cv2.GaussianBlur(mask,(0,0),3).astype(float)*1.7+mask.astype(float))[:,:,None]/255*opacity
 color=np.array(COLOR);dst[:,:,:3]=np.clip(dst[:,:,:3]+strength*color*.9,0,255).astype(np.uint8)
 # Cream-yellow sharp luminous center; bloom remains lime.
 core=mask[:,:,None]/255*opacity;dst[:,:,:3]=np.clip(dst[:,:,:3]*(1-core)+np.array([150,255,246])*core,0,255).astype(np.uint8)
def frame(n):
 from motion import rounded
 t=n/30;src,belt,outline,target,pocket=assets();out=np.full((H,W,4),(18,23,15,255),np.uint8);over(out,text_layer());over(out,belt,LEFT,TOP)
 # Complete the entire exterior glow, then hold before the material callout.
 if t<2.7:glow(out,outline,ease(t/2.0),1-ease((t-2.4)/.3))
 active=-1 if t<2.7 else 0 if t<4.8 else 1 if t<7.1 else 2
 if 2.7<=t<4.8:
  a=min(ease((t-2.7)/.25),1-ease((t-4.55)/.25));cx,cy,rad=184,234,91
  patch=src[270:520,1180:1430];patch=cv2.resize(patch,(182,182),interpolation=cv2.INTER_LANCZOS4);yy,xx=np.ogrid[:182,:182];patch[:,:,3]=np.where((xx-90.5)**2+(yy-90.5)**2<=90**2,255,0).astype(np.uint8);over(out,patch,cx-rad,cy-rad,a)
  theta=np.linspace(0,np.pi*2,500);circle=np.column_stack([cx+rad*np.cos(theta),cy+rad*np.sin(theta)])
  glow(out,circle,ease((t-2.7)/.45),a);link=resample([[cx+rad,cy],[365,cy],[697,317]])
  glow(out,link,ease((t-3.05)/.45),a)
 if 4.8<=t<7.1:glow(out,outline,ease((t-4.8)/1.5),1-ease((t-6.85)/.25))
 if t>=7.1:glow(out,pocket,ease((t-7.1)/1.6),1)
 for i,x in enumerate([38,339,640]):
  cv2.line(out,(x,555),(x+275,555),(75,88,78,255),1,cv2.LINE_AA)
  if i==active:
   start=[2.7,4.8,7.1][i];length=[2.1,2.3,2.1][i];cv2.line(out,(x,555),(x+round(275*np.clip((t-start)/length,0,1)),555),(*COLOR,255),2,cv2.LINE_AA)
 return rounded(out,16)
if __name__=='__main__':
 for n in [30,60,75,100,165,240,330]:cv2.imwrite(str(R/'10_review'/f'Belt_Trace_{n:03}.png'),frame(n))
 _,_,outline,target,pocket=assets();(R/'01_script/Belt_Trace_Paths.json').write_text(json.dumps({'source':str(SOURCE.relative_to(R)),'scale':SCALE,'position':[LEFT,TOP],'outline':outline.tolist(),'intro_end_index':int(target),'pocket':pocket.tolist(),'fps':30,'frames':345,'stages_seconds':[0,2.7,4.8,7.1,9.2,11.5]},indent=2))
 print('Editable path data and animation previews created')
