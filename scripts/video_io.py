from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""FFmpeg RGB decode with source color metadata honored; avoids OpenCV YUV-matrix ambiguity."""
from pathlib import Path
import subprocess,json,numpy as np,cv2
FF=FFMPEG;PROBE=FFPROBE
class VideoReader:
 def __init__(self,path):
  self.path=str(path);s=json.loads(subprocess.check_output([PROBE,'-v','error','-select_streams','v:0','-show_streams','-of','json',self.path]))['streams'][0]
  self.w=s['width'];self.h=s['height'];a,b=s['r_frame_rate'].split('/');self.fps=float(a)/float(b);self.frames=int(s.get('nb_frames',round(float(s.get('duration',0))*self.fps)));self.p=None;self.frame=0
 def _start(self):
  args=[FF,'-v','error','-threads','2']
  if self.frame:args+=['-ss',str(self.frame/self.fps)]
  self.p=subprocess.Popen(args+['-i',self.path,'-an','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 def read(self):
  if self.p is None:self._start()
  b=self.p.stdout.read(self.w*self.h*3)
  if len(b)!=self.w*self.h*3:return False,None
  self.frame+=1;return True,np.frombuffer(b,np.uint8).reshape(self.h,self.w,3).copy()
 def set(self,key,value):
  assert key==cv2.CAP_PROP_POS_FRAMES
  self.release();self.frame=int(value);return True
 def get(self,key):
  return {cv2.CAP_PROP_FRAME_COUNT:self.frames,cv2.CAP_PROP_FPS:self.fps,cv2.CAP_PROP_FRAME_WIDTH:self.w,cv2.CAP_PROP_FRAME_HEIGHT:self.h,cv2.CAP_PROP_POS_FRAMES:self.frame}.get(key,0)
 def release(self):
  if self.p:
   self.p.stdout.close()
   if self.p.poll() is None:self.p.terminate()
   self.p.wait();self.p=None
