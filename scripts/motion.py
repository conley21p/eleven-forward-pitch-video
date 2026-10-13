from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
from video_io import VideoReader
"""Deterministic 30fps typography, image, product and website animation from shared inputs."""
from pathlib import Path
from functools import lru_cache
import cv2,numpy as np,json,subprocess,math,sys,hashlib
R=Path(__file__).resolve().parents[1];G=R/'05_graphics';CFG=json.loads((R/'01_script/Production_Config.json').read_text());FPS=30
cv2.setNumThreads(2)
def smooth(v):v=max(0,min(1,v));return v*v*(3-2*v)
def fade(e,n):
    f=e['entrance_frames'];end=e['end'];exit=e['exit_frames']
    return min(smooth((n-e['start'])/f),smooth((end-n)/exit))
def over(dst,im,x=0,y=0,op=1):
    x,y=round(x),round(y);h,w=im.shape[:2];x0=max(0,x);y0=max(0,y);x1=min(dst.shape[1],x+w);y1=min(dst.shape[0],y+h)
    if x1<=x0 or y1<=y0 or op<=0:return
    pix=im[y0-y:y1-y,x0-x:x1-x];a=pix[:,:,3:4].astype(np.float32)/255*op;b=dst[y0:y1,x0:x1];ba=b[:,:,3:4].astype(np.float32)/255
    out=a+ba*(1-a);rgb=(pix[:,:,:3]*a+b[:,:,:3]*ba*(1-a))/np.maximum(out,1e-6)
    b[:,:,:3]=np.clip(rgb,0,255).astype(np.uint8);b[:,:,3:4]=np.clip(out*255,0,255).astype(np.uint8)
@lru_cache(maxsize=100)
def layer(path):
    im=cv2.imread(str(path),cv2.IMREAD_UNCHANGED);assert im is not None,path
    if im.shape[2]==3:im=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA)
    if im.dtype!=np.uint8:im=(im/257).astype(np.uint8)
    yy,xx=np.where(im[:,:,3]>0)
    if not len(xx):return np.zeros((1,1,4),np.uint8),0,0
    x,y=xx.min(),yy.min();return im[y:yy.max()+1,x:xx.max()+1],int(x),int(y)
def rounded(im,r=16):
    h,w=im.shape[:2];m=np.zeros((h,w),np.uint8);r=min(r,h//2,w//2)
    cv2.rectangle(m,(r,0),(w-r-1,h-1),255,-1);cv2.rectangle(m,(0,r),(w-1,h-r-1),255,-1)
    for x in [r,w-r-1]:
        for y in [r,h-r-1]:cv2.circle(m,(x,y),r,255,-1,cv2.LINE_AA)
    im=im.copy();im[:,:,3]=(im[:,:,3].astype(np.float32)*m/255).astype(np.uint8);return im
def fitted(im,w,h,cover=False,r=16):
    w,h=round(w),round(h);ih,iw=im.shape[:2];scale=max(w/iw,h/ih) if cover else min(w/iw,h/ih)
    size=(max(1,round(iw*scale)),max(1,round(ih*scale)))
    # Area downsampling suppresses textile moire; premultiplied alpha avoids dark rims.
    pm=im.astype(np.float32);pm[:,:,:3]*=pm[:,:,3:4]/255
    pm=cv2.resize(pm,size,interpolation=cv2.INTER_AREA if scale<1 else cv2.INTER_LANCZOS4)
    pm[:,:,:3]/=np.maximum(pm[:,:,3:4]/255,1e-6);out=np.clip(pm,0,255).astype(np.uint8)
    if cover:out=out[(out.shape[0]-h)//2:(out.shape[0]-h)//2+h,(out.shape[1]-w)//2:(out.shape[1]-w)//2+w]
    else:
        a=np.zeros((h,w,4),np.uint8);over(a,out,(w-out.shape[1])/2,(h-out.shape[0])/2);out=a
    return rounded(out,r) if r else out
@lru_cache(maxsize=50)
def image_source(eid):
    e=next(x for x in CFG['elements'] if x['id']==eid);im=cv2.imread(str(R/e['image']),-1)
    if im.shape[2]==3:im=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA)
    if 'crop' in e['extra']:
        x,y,x1,y1=e['extra']['crop'];im=im[y:y1,x:x1]
    return im
@lru_cache(maxsize=80)
def fitted_image(eid,w,h,cover,r):return fitted(image_source(eid),w,h,cover,r)
@lru_cache(maxsize=160)
def product_frame(kind,index):
    if kind.startswith('hero'):
        p=R/'06_blender/renders/hero'/f'{index:04}.png';im=cv2.imread(str(p),-1);assert im is not None,p
        bounds=CFG.get('product_bounds',{}).get('hero',[0,0,1600,1200]);x,y,x1,y1=bounds
        return im[y:y1,x:x1]
    p=R/'06_blender/renders/turntable'/f'frame_{index:04}.png';im=cv2.imread(str(p),-1);assert im is not None,p
    # Waist-only viewport excludes anatomical detail below the band.
    return im[267:950,333:1267]
def geometry(e,t):
    keys=e.get('keys')
    if not keys:return e['box']
    if t<=keys[0][0]:return keys[0][1:]
    for a,b in zip(keys,keys[1:]):
        if a[0]<=t<=b[0]:
            u=smooth((t-a[0])/(b[0]-a[0]));return [x+(y-x)*u for x,y in zip(a[1:],b[1:])]
    return keys[-1][1:]
def draw_element(dst,e,n):
    op=fade(e,n);age=(n-e['start'])/FPS;t=n/FPS;dx=e['travel']*(1-smooth((n-e['start'])/e['entrance_frames']))-e['travel']*(1-smooth((e['end']-n)/e['exit_frames']))
    if op<=0 and e['kind'] not in ['source_video','community_video','belt_trace']:return
    if e['extra'].get('exit_travel'):dx+=e['extra']['exit_travel']*(1-smooth((e['end']-n)/e['exit_frames']))
    k=e['kind']
    if k=='belt_trace':
        from belt_trace import frame
        x,y,w,h=e['box'];over(dst,frame(n-e['start']),x,y);return
    if k in ['source_video','community_video']:
        x,y,w,h=e['box'];frames=source_video(e['id']);idx=min(len(frames)-1,max(0,round((n-e['start'])*(len(frames)-1)/max(1,e['end']-e['start']-1))));im=fitted(frames[idx],w,h,r=e['radius']);over(dst,im,x,y,1);return
    if e['image']:
        x,y,w,h=geometry(e,t);im=fitted_image(e['id'],round(w),round(h),e['mode']=='cover',e['radius'])
        if e['extra'].get('tile_background'):
            tile=np.full((round(h),round(w),4),(0,0,0,255),np.uint8);over(tile,im,0,0);im=rounded(tile,e['radius'])
        over(dst,im,x+dx,y,op);return
    if k in ['hero','hero_still','mannequin_still','turntable']:
        x,y,w,h=e['box']
        if k=='hero':idx=min(640,e['extra'].get('first',1)+max(0,n-e['start']))
        elif k=='hero_still':idx=250
        elif k=='mannequin_still':idx=1
        else:idx=min(180,max(1,n-e['start']-15+1))
        im=product_frame('hero' if k.startswith('hero') else 'turntable',idx);im=fitted(im,w,h,r=0)
        if e['extra'].get('well'):
            well=np.full(im.shape,255,np.uint8);over(well,im);im=rounded(well,16)
        over(dst,im,x+dx,y,op);return
    if k=='grid':
        im=np.zeros_like(dst)
        for i in range(20):
            p=smooth((age-.6-i*(2.05/19))/.15);neutral=np.array([155,166,156]);green=np.array([34,62,37]);c=tuple(int(v) for v in neutral*(1-p)+green*p)+(255,)
            x=52+i%10*96;y=68+i//10*96;sq=np.zeros((72,72,4),np.uint8);sq[:]=c;over(im,rounded(sq,4),x,y)
        over(dst,im,dx,0,op);return
    if k=='activity':
        im=np.zeros_like(dst);points=[(26.07,168,64),(26.79,488,64),(28.33,808,64)]
        x,w=168,64
        for i in range(1,len(points)):
            cue,x1,w1=points[i]
            if t>=cue:
                u=smooth((t-cue)/.4);x0,w0=points[i-1][1:];x=x0+(x1-x0)*u;w=w0+(w1-w0)*u
        cv2.line(im,(round(x),862),(round(x+w),862),(34,62,37,255),4,cv2.LINE_AA);over(dst,im,dx,0,op);return
    if k=='bar':
        im=np.zeros_like(dst);cv2.rectangle(im,(52,868),(988,884),(189,193,192,255),-1);cv2.rectangle(im,(52,868),(round(52+93.6*smooth(age/.6)),884),(34,62,37,255),-1)
        over(dst,im,dx,0,op);return
    if k=='revenue':
        idx=min(18,max(0,n-e['start']));im,x,y=layer(G/'png'/f'revenue_{idx:02}.png');over(dst,im,x,y,op);return
    im,x,y=layer(R/e['png'])
    if e['extra'].get('axis')=='y':y+=dx;dx=0
    if k=='feature_label' and n>=e['extra']['active_until']:
        im=im.copy();im[:,:,:3]=10
    over(dst,im,x+dx,y,op)

@lru_cache(maxsize=3)
def source_video(eid):
    e=next(x for x in CFG['elements'] if x['id']==eid)
    path=R/e['extra']['asset']
    if e['kind']=='community_video':path=R/'00_references/final_powerpoint/Community_Dark_Original_Motion.mkv'
    cap=VideoReader(path);frames=[]
    while True:
        ok,im=cap.read()
        if not ok:break
        frames.append(cv2.cvtColor(im,cv2.COLOR_BGR2BGRA))
    cap.release();return frames

class Websites:
    def __init__(self):
        self.frames={};self.posters={};self.labels={}
        for id,label in [('stealth','Stealth Belt'),('siil','SIIL Ostomy')]:
            cap=VideoReader(str(R/'00_references/competitors'/id/f'{id}_square.mp4'));frames=[]
            while True:
                ok,im=cap.read()
                if not ok:break
                im=cv2.resize(im,(720,720),interpolation=cv2.INTER_AREA)[:,12:708];frames.append(cv2.cvtColor(im,cv2.COLOR_BGR2BGRA))
            cap.release();assert len(frames)>=126,(id,len(frames));self.frames[id]=frames[:126];self.posters[id]=frames[0]
            # Company labels use the same typography renderer as the rest of the project.
            p=G/'png'/f'website_label_{id}.png';self.labels[id]=layer(p)
    def card(self,id,index,width=864):
        im=np.full((816,864,4),(18,23,15,255),np.uint8)
        label,x,y=self.labels[id];over(im,label,x,y)
        over(im,self.frames[id][index],84,72)
        return rounded(im,20)
    def draw(self,dst,n,e):
        site=e['extra']['site'];op=fade(e,n)
        age=n-e['start'];dx=e['travel']*(1-smooth(age/e['entrance_frames']))-e['travel']*(1-smooth((e['end']-n)/e['exit_frames']))
        x,y,w,h=e['box']
        if e['kind']=='website_thumb':
            # Faithful page opening, cropped reversibly to the principal upper page area.
            crop=self.frames[site][125][180:540] if site=='stealth' else self.frames[site][125][320:680]
            im=fitted(crop,w,h,cover=True,r=12)
        else:
            idx=min(125,max(0,round((n-e['start'])*125/max(1,e['end']-e['start']-1)))) if e['extra'].get('fit_complete') else min(125,max(0,n-round(e['extra']['play_start']*30)))
            im=self.card(site,idx)
        over(dst,im,x+dx,y,op)

def encode(path,w,h):
    args=[FFMPEG,'-v','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{w}x{h}','-r','30','-i','-']
    if (w,h)==(1040,936):args+=['-vf','pad=1920:1080:816:72:color=black@0']
    return subprocess.Popen(args+['-an','-c:v','qtrle','-pix_fmt','argb','-threads','2',str(path)],stdin=subprocess.PIPE)
def render(preview=False,products=False):
    wanted=sys.argv[1:] if len(sys.argv)>1 else []
    web=None;entries=[]
    # No universal plate mask: imagery is clipped only by its own asset cell.
    for scene in CFG['scenes']:
        if wanted and scene['id'] not in wanted:continue
        own=[e for e in CFG['elements'] if scene['start']<=e['start']<scene['end']]
        for channel in ['Images','Typography','Product']:
            els=[e for e in own if e['channel']==channel]
            if not els:continue
            start=min(e['start'] for e in els);end=max(e['end'] for e in els);path=G/'motion'/f'{scene["id"]}_{channel}.mov'
            h=hashlib.sha256(Path(__file__).read_bytes()+json.dumps(els,sort_keys=True).encode()+json.dumps(CFG.get('product_bounds',{}),sort_keys=True).encode())
            for e in els:
                if e['kind']=='belt_trace':
                    h.update((R/'scripts/belt_trace.py').read_bytes());h.update((R/e['extra']['asset']).read_bytes())
                if e['kind'] in ['source_video','community_video']:
                    h.update((R/e['extra']['asset']).read_bytes())
                    if e['kind']=='community_video':h.update((R/'00_references/final_powerpoint/Community_Dark_Original_Motion.mkv').read_bytes())
                for key in ['svg','png','image']:
                    if e.get(key) and (R/e[key]).exists():h.update((R/e[key]).read_bytes())
            if any(e['kind']=='revenue' for e in els):
                for p in sorted((G/'png').glob('revenue_*.png')):h.update(p.read_bytes())
            if any(e['kind'] in ['website','website_thumb'] for e in els):
                for id in ['stealth','siil']:
                    h.update((R/'00_references/competitors'/id/f'{id}_square.mp4').read_bytes());h.update((G/'png'/f'website_label_{id}.png').read_bytes())
            digest=h.hexdigest();q=R/'09_qc'/f'{scene["id"]}_{channel}_frames.json'
            if path.exists() and q.exists() and json.loads(q.read_text()).get('input_hash')==digest and int(json.loads(subprocess.check_output([FFPROBE,'-v','error','-select_streams','v:0','-show_streams','-of','json',str(path)]))['streams'][0].get('nb_frames',0))==end-start:
                print('Retaining verified inputs',path.name,flush=True);continue
            if any(e['kind'] in ['website','website_thumb'] for e in els) and web is None:web=Websites()
            enc=encode(path,1040,936);hashes=[]
            for n in range(start,end):
                im=np.zeros((936,1040,4),np.uint8)
                for e in els:
                    if e['start']<=n<e['end']:
                        if e['kind'] in ['website','website_thumb']:web.draw(im,n,e)
                        else:draw_element(im,e,n)
                enc.stdin.write(im.tobytes())
                if n%30==0:hashes.append(hashlib.sha256(im.tobytes()).hexdigest())
            enc.stdin.close();assert enc.wait()==0,path
            print('Rendered',path.name,start,end,flush=True)
            q.write_text(json.dumps({'start':start,'end':end,'frames':end-start,'input_hash':digest,'sampled_hashes':hashes},indent=2))
    for scene in CFG['scenes']:
        own=[e for e in CFG['elements'] if scene['start']<=e['start']<scene['end']]
        for channel in ['Images','Typography','Product']:
            els=[e for e in own if e['channel']==channel]
            if els:entries.append({'name':scene['id']+' '+channel,'asset':f'05_graphics/motion/{scene["id"]}_{channel}.mov','start':min(e['start'] for e in els),'end':max(e['end'] for e in els),'rect':[0,0,1920,1080],'elements':[e['id'] for e in els]})
    (R/'01_script/Rendered_Layers.json').write_text(json.dumps(entries,indent=2))
if __name__=='__main__':render()
