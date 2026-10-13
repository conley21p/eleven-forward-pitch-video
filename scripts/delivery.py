from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""120s delivery directly from lossless source composition; pitch-preserving audio."""
from pathlib import Path
import cv2,numpy as np,json,subprocess,csv
from video_io import VideoReader
from composite import over,frosted,banner,Clip
R=Path(__file__).resolve().parents[1];D=json.loads((R/'01_script/Delivery_Config.json').read_text());FF=FFMPEG;N=D['frames'];END=D['source_frames_retained'];speed=D['speed']
poster=cv2.imread(str(R/D['poster']),-1)
if poster.shape[2]==3:poster=cv2.cvtColor(poster,cv2.COLOR_BGR2BGRA)
def cover(base,k):
 t=k/30
 if t<=D['cover_hold']:return poster.copy()
 if t>=D['cover_fade_end']:return base
 v=(t-D['cover_hold'])/(D['cover_fade_end']-D['cover_hold']);a=1-v*v*(3-2*v)
 return np.clip(base.astype(float)*(1-a)+poster.astype(float)*a,0,255).astype(np.uint8)
def audio():
 for source,target in [('Founder_Dialogue.wav','Founder_120s.wav'),('Motion_Sounds.wav','Motion_120s.wav'),('Dialogue_And_Motion.wav','Dialogue_And_Motion_120s.wav')]:
  subprocess.run([FF,'-v','error','-y','-i',str(R/'04_audio'/source),'-af',f'atrim=end={D["source_end"]},asetpts=PTS-STARTPTS,atempo={speed},apad,atrim=end=120','-ar','48000','-c:a','pcm_s24le',str(R/'04_audio'/target)],check=True)
def encoder(path,archive=False,caption=False):
 exe=CAPTION_FFMPEG if caption else FF
 filters='scale=out_color_matrix=bt709:out_range=tv,format='+('yuv422p10le' if archive else 'yuv420p')
 if caption:filters=f"ass=filename='{R/'01_script/Founder_Actual_Delivery.ass'}',"+filters
 codec=['-c:v','prores_ks','-profile:v','3','-pix_fmt','yuv422p10le','-threads','2','-c:a','pcm_s24le'] if archive else ['-c:v','libx264','-crf','10','-preset','slow','-x264-params','aq-mode=3:qcomp=0.8:deblock=-1,-1','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-b:a','192k']
 return subprocess.Popen([exe,'-v','error','-y','-f','rawvideo','-pix_fmt','bgra','-s','1920x1080','-r','30','-i','-','-i',str(R/'04_audio/Dialogue_And_Motion_120s.wav'),'-map','0:v','-map','1:a','-vf',filters,*codec,'-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','-frames:v','3600','-t','120',str(path)],stdin=subprocess.PIPE)
def render():
 audio();events=json.loads((R/'01_script/Rendered_Layers.json').read_text());cap=VideoReader(R/'03_founder/Founder_Gradient_30fps.mkv');active={}
 selected=np.floor((np.arange(N)+.5)*END/N).astype(int);lookup={int(n):k for k,n in enumerate(selected)}
 encoders=[encoder(R/'08_exports/ElevenForward_Kinetic_Clean_WORKING.mp4'),encoder(R/'08_exports/ElevenForward_Kinetic_Captioned_WORKING.mp4',caption=True),encoder(R/'08_exports/ElevenForward_Kinetic_Archive_WORKING.mov',archive=True)]
 rows=[]
 for n in range(END):
  ok,im=cap.read();assert ok,n;base=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA);frosted(base,n)
  for i,e in enumerate(events):
   if e['start']<=n<e['end']:
    if i not in active:active[i]=Clip(R/e['asset'],1920,1080)
    over(base,active[i].read())
   elif i in active:active.pop(i).close()
  banner(base,n)
  if n in lookup:
   k=lookup[n];base=cover(base,k);data=base.tobytes()
   for enc in encoders:enc.stdin.write(data)
   rows.append([k,k/30,n,n/30])
   if k in [0,6,12,23,600,960,1350,1500,1800,2400,3000,3540,3599]:cv2.imwrite(str(R/'10_review'/f'Delivery_{k:04}.png'),base)
   if k%300==0:print('Two-minute delivery',k/30,flush=True)
 cap.release()
 for c in active.values():c.close()
 for enc in encoders:enc.stdin.close();assert enc.wait()==0
 assert len(rows)==3600
 with (R/'01_script/Delivery_Frame_Map.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['delivery_frame','delivery_seconds','source_edit_frame','source_edit_seconds']);w.writerows(rows)
 print('Three exact120-second exports rendered')
if __name__=='__main__':render()
