from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
from video_io import VideoReader
from pathlib import Path
import cv2,numpy as np,json,subprocess,sys
from motion import R,G,CFG,over as sparse_over,rounded,smooth,layer,draw_element,Websites
N=3851;FF=FFMPEG
def over(dst,im,x=0,y=0,op=1):
    if op<=0:return
    rx,ry,rw,rh=cv2.boundingRect(im[:,:,3])
    if not rw or not rh:return
    im=im[ry:ry+rh,rx:rx+rw];x=round(x+rx);y=round(y+ry)
    x0=max(0,x);y0=max(0,y);x1=min(dst.shape[1],x+rw);y1=min(dst.shape[0],y+rh)
    if x1<=x0 or y1<=y0:return
    b=dst[y0:y1,x0:x1];p=im[y0-y:y1-y,x0-x:x1-x]
    if np.all(b[:,:,3]==255):
        a=p[:,:,3:4].astype(np.float32)*(op/255);b[:,:,:3]=np.clip(p[:,:,:3]*a+b[:,:,:3]*(1-a),0,255).astype(np.uint8)
    else:sparse_over(dst,im,x,y,op)
from functools import lru_cache
from motion import fade,geometry
@lru_cache(maxsize=100)
def surface_mask(w,h,r,style):
    if style=='oval':
        m=np.zeros((h,w),np.uint8);cv2.ellipse(m,(w//2,h//2),(max(1,w//2-40),max(1,h//2-40)),0,0,360,255,-1,cv2.LINE_AA)
        return cv2.GaussianBlur(m,(0,0),28).astype(np.float32)/255
    return rounded(np.full((h,w,4),255,np.uint8),r)[:,:,3].astype(np.float32)/255
def frosted(base,n,save=False):
    """Historical function name; now renders opaque theme surfaces without frost."""
    full=np.zeros((1080,1920,4),np.uint8)
    for s in CFG['surfaces']:
        if not s['start']<=n<s['end']:continue
        x,y,w,h=[round(v) for v in geometry(s,n/30)]
        im=np.full((h,w,4),(18,23,15,255),np.uint8);im=rounded(im,s['radius'])
        over(full,im,x+816,y+72,fade(s,n))
    over(base,full);return full

def banner(base,n):
    if n>=107:return
    dx=-round(540*smooth((n-83)/24))
    im,x,y=layer(G/'01_wordmark.png');over(base,im,x+dx,y)

def review():
    import motion
    original=motion.product_frame
    # Draft QA only may use the nearest completed product pose while Blender is running.
    count=len(list((R/'06_blender/renders/hero').glob('*.png')))
    turncount=len(list((R/'06_blender/renders/turntable').glob('*.png')))
    motion.product_frame=lambda kind,index:original(kind,min(count,index) if kind.startswith('hero') else min(turncount,index))
    cap=VideoReader(str(R/'03_founder/Founder_Gradient_30fps.mkv'));web=Websites()
    times=[1.5,5.8,9,16,28,32,38,41.5,44,45,46.6,48.5,52,57,65,75,81,90,97,103,107.8,109,123]
    for t in times:
        n=round(t*30);cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,im=cap.read();assert ok
        base=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA);frosted(base,n)
        panel=np.zeros((936,1040,4),np.uint8)
        for e in CFG['elements']:
            if e['start']<=n<e['end']:
                if e['kind'] in ['website','website_thumb']:web.draw(panel,n,e)
                else:draw_element(panel,e,n)
        over(base,panel,816,72);banner(base,n)
        cv2.imwrite(str(R/'09_qc'/f'Review_{n:04}.png'),base)
    cap.release();print('Representative full-size compositions written')
class Clip:
    def __init__(self,path,w,h):
        self.w=w;self.h=h;self.p=subprocess.Popen([FF,'-v','error','-i',str(path),'-an','-f','rawvideo','-pix_fmt','bgra','-'],stdout=subprocess.PIPE)
    def read(self):
        b=self.p.stdout.read(self.w*self.h*4);assert len(b)==self.w*self.h*4
        return np.frombuffer(b,np.uint8).reshape(self.h,self.w,4)
    def close(self):self.p.stdout.close();self.p.wait()
def render():
    events=json.loads((R/'01_script/Rendered_Layers.json').read_text());assert all((R/e['asset']).exists() for e in events)
    cap=VideoReader(str(R/'03_founder/Founder_Gradient_30fps.mkv'));active={}
    clean=R/'08_exports/ElevenForward_Kinetic_Clean_WORKING.mp4'
    enc=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','bgra','-s','1920x1080','-r','30','-i','-','-i',str(R/'04_audio/Dialogue_And_Motion.wav'),'-map','0:v','-map','1:a','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-crf','10','-preset','slow','-x264-params','aq-mode=3:qcomp=0.8:deblock=-1,-1','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-b:a','192k','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(clean)],stdin=subprocess.PIPE)
    archive=R/'08_exports/ElevenForward_Kinetic_Archive_WORKING.mov'
    arch=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','bgra','-s','1920x1080','-r','30','-i','-','-i',str(R/'04_audio/Dialogue_And_Motion.wav'),'-map','0:v','-map','1:a','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv422p10le','-c:v','prores_ks','-profile:v','3','-pix_fmt','yuv422p10le','-threads','2','-c:a','pcm_s24le','-ar','48000','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(archive)],stdin=subprocess.PIPE)
    from motion import encode
    caption=R/'08_exports/ElevenForward_Kinetic_Captioned_WORKING.mp4'
    caption_filter=f"ass=filename='{R/'01_script/Founder_Actual_Delivery.ass'}',scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
    captions=subprocess.Popen([CAPTION_FFMPEG,'-v','error','-y','-f','rawvideo','-pix_fmt','bgra','-s','1920x1080','-r','30','-i','-','-i',str(R/'04_audio/Dialogue_And_Motion.wav'),'-map','0:v','-map','1:a','-vf',caption_filter,'-c:v','libx264','-crf','10','-preset','slow','-x264-params','aq-mode=3:qcomp=0.8:deblock=-1,-1','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-b:a','192k','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(caption)],stdin=subprocess.PIPE)
    blur=encode(G/'motion/Dark_Surfaces.mov',1920,1080)
    for n in range(N):
        ok,im=cap.read();assert ok,n;base=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA);f=frosted(base,n);blur.stdin.write(f.tobytes())
        for i,e in enumerate(events):
            if e['start']<=n<e['end']:
                if i not in active:active[i]=Clip(R/e['asset'],1920,1080)
                over(base,active[i].read())
            elif i in active:active.pop(i).close()
        banner(base,n);data=base.tobytes();enc.stdin.write(data);arch.stdin.write(data);captions.stdin.write(data)
        if n in [90,150,240,402,600,1080,1440,1611,1660,2085,2235,2320,2450,2670,2900,3090,3450,3552,3570,3630]:cv2.imwrite(str(R/'09_qc'/f'Final_{n:04}.png'),base)
        if n%300==0:print('Composite',n/30,'seconds',flush=True)
    cap.release();enc.stdin.close();arch.stdin.close();captions.stdin.close();blur.stdin.close();assert enc.wait()==0;assert arch.wait()==0;assert captions.wait()==0;assert blur.wait()==0
    for c in active.values():c.close()
    print('Clean composite and live background frost complete')
if __name__=='__main__':review() if '--review' in sys.argv else render()
