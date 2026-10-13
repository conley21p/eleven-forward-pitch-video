"""Native Kdenlive master with separate original voice, motion sounds, glass, scene and product layers."""
from pathlib import Path
import json,xml.etree.ElementTree as E,uuid,cv2,numpy as np
from motion import R,G,CFG,smooth,layer
N=3851;P=R/'07_kdenlive';uid='{'+str(uuid.uuid5(uuid.NAMESPACE_URL,'elevenforward-premium-cinematic-20261011'))+'}'
events=json.loads((R/'01_script/Rendered_Layers.json').read_text())
root=E.Element('mlt',{'LC_NUMERIC':'en_US.UTF-8','producer':'project','version':'7.41.0'})
E.SubElement(root,'profile',dict(colorspace='709',description='HD 1080p 30 fps',width='1920',height='1080',progressive='1',frame_rate_num='30',frame_rate_den='1',sample_aspect_num='1',sample_aspect_den='1',display_aspect_num='16',display_aspect_den='9'))
def prop(el,k,v):E.SubElement(el,'property',name=k).text=str(v)
def producer(id,asset,movie=True,audio=False,length=N):
    p=E.SubElement(root,'producer',id=id,**{'in':'0','out':str(length-1)})
    for k,v in {'resource':'../'+asset,'mlt_service':'avformat' if movie else 'qimage','length':length,'eof':'pause','kdenlive:id':1000+len(root.findall('producer')),'kdenlive:clipname':Path(asset).stem,'set.test_audio':0 if audio else 1,'set.test_image':1 if audio else 0,'ttl':1}.items():prop(p,k,v)
    return p
def animation(p,keys,L):
    f=E.SubElement(p,'filter',{'in':'0','out':str(L-1)})
    for k,v in {'mlt_service':'affine','kdenlive:id':'pan_zoom','kdenlive:sync_in_out':1,'kdenlive:ix':1,'transition.rect':';'.join(keys),'transition.distort':0,'transition.fill':1,'transition.b_alpha':0,'background':'color:0x00000000'}.items():prop(f,k,v)
black=E.SubElement(root,'producer',id='black',**{'in':'0','out':str(N-1)});prop(black,'mlt_service','color');prop(black,'resource','black');prop(black,'length',N)
defs=[]
for id,name,asset,audio in [('dialogue','A1 · Original dialogue · unchanged','04_audio/Founder_Dialogue.wav',True),('sounds','A2 · Quiet motion sounds · no music','04_audio/Motion_Sounds.wav',True),('founder','V1 · Continuous original camera take','03_founder/Founder_Gradient_30fps.mkv',False),('frost','V2 · Opaque dark-green surfaces','05_graphics/motion/Dark_Surfaces.mov',False)]:
    producer(id,asset,audio=audio);defs.append((id,name,0,N,audio))
for i,e in enumerate(events):
    id=f'layer_{i}';producer(id,e['asset'],length=e['end']-e['start']);defs.append((id,'V · '+e['name'],e['start'],e['end'],False))
for id,a,b in [('banner_open',0,107)]:
    p=producer(id,'05_graphics/01_wordmark.png',movie=False,length=b-a);keys=[]
    for f in range(b-a):
        dx=-round(540*smooth((f-83)/24));keys.append(f'{f}={dx} 0 1920 1080 1')
    animation(p,keys,b-a);defs.append((id,'V · Opening founder banner',a,b,False))
# Original still images and SVG render layers are also in the project bin for replacement.
extra=[]
for e in CFG['elements']:
    asset=e.get('image') or e.get('extra',{}).get('asset') or (e['png'] if (R/e['png']).exists() else None)
    if asset and asset not in extra:extra.append(asset)
extra.extend(['03_founder/Original_Camera_Take.mov','00_references/final_powerpoint/Community_Dark_Original_Motion.mkv'])
for i,a in enumerate(extra):producer('editable_'+str(i),a,movie=Path(a).suffix.lower() in ['.mp4','.mov','.mkv'])
main=E.SubElement(root,'playlist',id='main_bin')
for k,v in {'xml_retain':1,'kdenlive:docproperties.version':'1.1','kdenlive:docproperties.projectid':'20261010','kdenlive:docproperties.groups':'[]','kdenlive:docproperties.activetimeline':uid,'kdenlive:docproperties.opensequences':uid,'kdenlive:docproperties.profile':'atsc_1080p_30','kdenlive:folder.-1.2':'Sequences','kdenlive:sequenceFolder':2,'kdenlive:docproperties.uuid':uid,'kdenlive:docproperties.documentid':'202610101830','kdenlive:docproperties.audioChannels':1,'kdenlive:docproperties.kdenliveversion':'26.08.1','kdenlive:docproperties.patchversion':1}.items():prop(main,k,v)
E.SubElement(main,'entry',producer=uid,**{'in':'0','out':str(N-1)})
for id in [d[0] for d in defs]+['editable_'+str(i) for i in range(len(extra))]:E.SubElement(main,'entry',producer=id)
tracks=[]
for i,(src,name,a,b,audio) in enumerate(defs):
    id='track_'+str(i);pl=E.SubElement(root,'playlist',id=id+'_a')
    if a:E.SubElement(pl,'blank',length=str(a))
    E.SubElement(pl,'entry',producer=src,**{'in':'0','out':str(b-a-1)});E.SubElement(root,'playlist',id=id+'_b')
    tr=E.SubElement(root,'tractor',id=id,**{'in':'0','out':str(N-1)})
    for k,v in {'kdenlive:track_name':name,'kdenlive:trackheight':60,'kdenlive:timeline_active':1,'kdenlive:collapsed':0}.items():prop(tr,k,v)
    if audio:prop(tr,'kdenlive:audio_track',1)
    for suffix in ['a','b']:E.SubElement(tr,'track',producer=id+'_'+suffix,hide='video' if audio else 'audio')
    tracks.append((id,audio))
t=E.SubElement(root,'tractor',id=uid,**{'in':'0','out':str(N-1)})
for k,v in {'kdenlive:sequenceuuid':uid,'kdenlive:sequenceproperties.name':'Eleven Forward · Final graphics redesign','kdenlive:sequenceproperties.tracks':len(tracks),'kdenlive:sequenceproperties.duration':N,'kdenlive:uuid':uid,'kdenlive:clipname':'MASTER KINETIC SPEECH','kdenlive:sequenceproperties.hasAudio':1,'kdenlive:sequenceproperties.hasVideo':1,'kdenlive:sequenceproperties.activeTrack':3,'kdenlive:sequenceproperties.tracksCount':len(tracks),'kdenlive:sequenceproperties.documentuuid':uid,'kdenlive:control_uuid':uid,'kdenlive:duration':N,'kdenlive:maxduration':N,'kdenlive:producer_type':17,'kdenlive:id':900,'kdenlive:folderid':2,'kdenlive:sequenceproperties.audioTarget':0,'kdenlive:sequenceproperties.videoTarget':2,'kdenlive:sequenceproperties.position':0,'kdenlive:sequenceproperties.zoom':8,'kdenlive:sequenceproperties.zonein':0,'kdenlive:sequenceproperties.zoneout':N,'kdenlive:sequenceproperties.groups':'[]'}.items():prop(t,k,v)
guides=[{'pos':s['start'],'comment':s['id'],'type':0} for s in CFG['scenes']]+[{'pos':e['start'],'comment':e['id'],'type':1} for e in CFG['elements'] if e['channel']=='Typography']
prop(t,'kdenlive:sequenceproperties.guides',json.dumps(guides));E.SubElement(t,'track',producer='black')
for id,audio in tracks:E.SubElement(t,'track',producer=id,hide='video' if audio else 'audio')
for i,(_,audio) in enumerate(tracks,1):
    tr=E.SubElement(t,'transition',{'in':'0','out':str(N-1)});prop(tr,'mlt_service','mix' if audio else 'qtblend');prop(tr,'a_track',0);prop(tr,'b_track',i)
    if audio:prop(tr,'always_active',1);prop(tr,'sum',1)
    else:prop(tr,'compositing',0);prop(tr,'distort',0)
project=E.SubElement(root,'tractor',id='project',**{'in':'0','out':str(N-1)});E.SubElement(project,'track',producer=uid)
E.indent(root);E.ElementTree(root).write(P/'Source_ElevenForward_Kinetic.kdenlive',encoding='utf-8',xml_declaration=True)
E.ElementTree(root).write(P/'Source_preview.mlt',encoding='utf-8',xml_declaration=True)
f=E.SubElement(t,'filter',{'in':'0','out':str(N-1)})
for k,v in {'mlt_service':'avfilter.ass','av.filename':'../01_script/Founder_Source_Delivery.ass','kdenlive:id':'subtitles','kdenlive:ix':1,'kdenlive:sync_in_out':1}.items():prop(f,k,v)
E.indent(root);E.ElementTree(root).write(P/'Source_ElevenForward_Kinetic_Captioned.kdenlive',encoding='utf-8',xml_declaration=True)
print('Native layered Kdenlive project with',len(tracks),'tracks written')
