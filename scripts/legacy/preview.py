from pathlib import Path
import cv2,numpy as np,json
from motion import R,CFG,draw_element,Websites
from composite import frosted,banner,over
from founder import crop_x,CROP_W,CROP_H,CROP_Y,amount,xweight,SOURCE
from video_io import VideoReader

cap=VideoReader(SOURCE);web=Websites();out=R/'10_review';tiles=[]
times=[1.5,5.5,10,18,28,32,38,41.5,43.2,44,45,46.6,48.5,52,57,65,75,81,90,97,103,107.5,108,123]
for t in times:
 n=round(t*30);cap.set(cv2.CAP_PROP_POS_FRAMES,round(n*24/30));ok,src=cap.read();assert ok
 mat=np.array([[CROP_W/1920,0,crop_x(n)+(CROP_W/1920-1)/2],[0,CROP_H/1080,CROP_Y+(CROP_H/1080-1)/2]])
 im=cv2.warpAffine(src,mat,(1920,1080),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP)
 if amount(n)>0:
  w=xweight*amount(n);blur=cv2.GaussianBlur(im,(0,0),4);im=np.clip(im*(1-w)+blur*w,0,255).astype(np.uint8)
 base=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA);frosted(base,n);panel=np.zeros((936,1040,4),np.uint8)
 for e in CFG['elements']:
  if e['start']<=n<e['end']:
   if e['kind']=='website':web.draw(panel,n,e)
   else:draw_element(panel,e,n)
 over(base,panel,816,72);banner(base,n);p=out/f'Preview_{n:04}.png';cv2.imwrite(str(p),base)
 tile=cv2.resize(base[:,:,:3],(480,270));canvas=np.full((296,480,3),17,np.uint8);canvas[26:]=tile;cv2.putText(canvas,f'{t:.2f}s',(10,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1);tiles.append(canvas)
 print('Preview',t,flush=True)
cap.release()
for page in range(3):
 contact=np.full((888,1440,3),17,np.uint8)
 for i,tile in enumerate(tiles[page*9:(page+1)*9]):contact[(i//3)*296:(i//3+1)*296,(i%3)*480:(i%3+1)*480]=tile
 cv2.imwrite(str(out/f'Contact_{page+1}.jpg'),contact)
