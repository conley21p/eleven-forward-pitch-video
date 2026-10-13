from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Authoritative Final Graphics Redesign: all coordinates are local to x816/y72."""
from pathlib import Path
import json,html,csv,subprocess,base64
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];G=R/'05_graphics';E=[];S=[]
T={'surface':'#0F1712','black':'#000000','accent':'#D3F928','text':'#F7F8F5','secondary':'#A6B4A1','row':'#193728'}
SCENES=[('Anatomy',4,6.5),('Race',6.5,14.8),('Product',14.8,29.133333),('Details',32,43.5),('Community',44.5,48.5),('Market',48.5,59),('Comparison',68,78),('StealthWebsite',79,83),('Economics',83.9,91.2),('Giving',91.2,99.166667),('Funding',99.166667,108)]
def tx(s,x,y,size=32,bold=False,color='text',anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" font-weight="{700 if bold else 400}" fill="{T.get(color,color)}" text-anchor="{anchor}">{html.escape(s)}</text>'
def item(id,a,b,body='',image=None,box=None,channel='Typography',kind=None,extra=None,entrance=10,exit=8,travel=16,radius=16,mode='contain'):
 p=G/'svg'/f'{id}.svg';p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="936">{body}</svg>')
 E.append(dict(id=id,channel=channel,start=round(a*30),end=round(b*30),svg=str(p.relative_to(R)),png=f'05_graphics/png/{id}.png',image=image,box=box,mode=mode,radius=radius,keys=None,kind=kind,extra=extra or {},entrance_frames=entrance,exit_frames=exit,travel=travel,group=id))
def text(id,a,b,*body,**kw):item(id,a,b,''.join(body),**kw)
def img(id,a,b,asset,box,**kw):item(id,a,b,image='00_references/'+asset,box=box,channel='Images',**kw)
def surface(id,a,b,box,exit=8,entrance=10):S.append(dict(id=id,start=round(a*30),end=round(b*30),box=box,style='opaque',radius=16,entrance_frames=entrance,exit_frames=exit,keys=None))
def media(id,a,b,file,box,**kw):item(id,a,b,channel='Images',kind='source_video',box=box,extra={'asset':'00_references/final_powerpoint/'+file},**kw)
surface('anatomy',4,6.5,[40,100,960,704])
text('anatomy_title',4,6.5,tx('Colostomy / Ileostomy',80,170,48,True))
img('anatomy_illustration',4,6.5,'final_powerpoint/Anatomy_Cutout.png',[240,196,560,510],radius=0)
surface('race_header',6.5,14.8,[40,64,960,80])
text('nine_months',6.5,14.8,tx('9 months later',80,119,44,True))
img('race_swim',6.5,14.8,'powerpoint/race_swim.png',[40,168,468,616],mode='cover')
img('race_finish',6.5,14.8,'powerpoint/race_finish.png',[532,168,468,616],mode='cover')
surface('paired_product',14.8,29.133333,[40,160,960,544])
text('product_title',14.8,29.133333,tx('Ostomy Belt',80,235,48,True),tx('Exterior',80,640,28,color='secondary'),tx('Design concept',532,640,28,color='secondary'))
img('product_exterior',14.8,29.133333,'final_powerpoint/image2.png',[80,296,428,300],mode='contain',radius=24,extra={'tile_background':True})
img('product_interior',14.8,29.133333,'final_powerpoint/image3.png',[532,296,428,300],mode='contain',radius=24,extra={'tile_background':True})
item('material_shape_design',32,43.5,channel='Images',kind='belt_trace',box=[40,124,960,640],extra={'asset':'00_references/final_powerpoint/Belt_Trace_Source.png'},entrance=1,exit=1,travel=0)
item('community_animation',44.5,48.5,channel='Images',kind='community_video',box=[40,124,960,640],extra={'asset':'00_references/final_powerpoint/media2.mp4'},entrance=1,exit=1,travel=0)
surface('market_population',48.5,50.7,[80,248,880,330])
surface('market_audience',50.7,54.166667,[80,218,880,400])
surface('market_calculation',54.166667,59,[80,222,880,460])
text('population',48.5,50.7,tx('725K–1M',120,366,88,True),tx('Americans living with an ostomy',120,436,36,True),tx('Source: UOAA',120,520,24,color='secondary'),travel=0)
text('audience',50.7,54.166667,tx('200,000',120,350,88,True),tx('Potential customers',120,418,38,True),tx('Ages 13–44',120,474,32,color='secondary'),tx('Founder’s class-research estimate',120,550,24,color='secondary'),travel=0)
text('market_inputs',54.166667,59,tx('200,000',120,296,54,True),tx('Potential customers',460,296,30),tx('× $120',120,380,54,True),tx('Target price per belt',460,380,30),travel=0)
text('market_result',54.566667,59,'<path d="M120 418H920" stroke="#A6B4A1" stroke-opacity=".4"/>',tx('$24,000,000.00',120,498,72,True),tx('Estimated market value',120,546,32),tx('Class-research estimate · One belt per potential customer',120,602,23,color='secondary'),tx('Purchase frequency not established',120,640,23,color='secondary'),travel=0)
img('stealth_comparison',68,78,'final_powerpoint/image7.png',[40,112,960,640])
item('stealth_website',79,83,channel='Images',kind='website',box=[88,60,864,816],extra={'site':'stealth','play_start':79,'fit_complete':True},entrance=1,exit=1,travel=0)
surface('economics',83.9,91.2,[80,230,880,472])
text('economics_title',83.9,91.2,tx('Target economics',120,304,44,True))
text('retail',85.666667,91.2,tx('Target retail',120,404,32,True),tx('$120',120,524,88,True))
text('cogs',88,91.2,tx('Target COGS',550,404,32,True),tx('≈10%',550,524,88,True),tx('of retail price',550,578,28,color='secondary'))
surface('giving',91.2,99.166667,[40,224,960,500])
text('giving_title',91.2,99.166667,tx('Intended giving program',80,294,30,True,color='secondary'),'<path d="M80 330H156" stroke="#D3F928" stroke-width="3"/>')
text('giving_purchase',91.2,99.166667,tx('A purchase with purpose',80,412,52,True))
text('giving_supplies',93.133333,99.166667,tx('Essential ostomy supplies',80,504,42,True))
text('giving_people',95.7,99.166667,tx('For people without health insurance',80,616,36))
img('funding_studio',99.166667,108,'final_powerpoint/image8.png',[0,148,1040,585],exit=24,extra={'exit_travel':1100})
# Exact source logo is embedded into the editable SVG; keep founder subtitle separately editable.
logo=base64.b64encode((R/'00_references/final_powerpoint/image1.png').read_bytes()).decode()
logo_image=Image.open(R/'00_references/final_powerpoint/image1.png').convert('RGB');red,green,blue=logo_image.split();logo_mask=ImageChops.multiply(green.point(lambda v:255 if v>150 else 0),blue.point(lambda v:255 if v<100 else 0));bounds=logo_mask.getbbox();lx,ly,lx1,ly1=bounds
banner=f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><defs><clipPath id="b"><path d="M0 826H530L500 970H0Z"/></clipPath></defs><g clip-path="url(#b)"><path d="M0 826H530L500 970H0Z" fill="#000"/><svg x="32" y="844" width="456" height="66" viewBox="{lx} {ly} {lx1-lx} {ly1-ly}" preserveAspectRatio="xMidYMid meet"><image width="2172" height="724" href="data:image/png;base64,{logo}"/></svg>{tx("Founder: Manning Price",32,947,25,True)}</g></svg>'
(G/'01_wordmark.svg').write_text(banner)
for site,label in [('stealth','Stealth Belt'),('siil','SIIL Ostomy')]:
 (G/'svg'/f'website_label_{site}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="864" height="816">'+tx(label,432,54,40,True,anchor='middle')+'</svg>')
config={'name':'Eleven Forward · Final Graphics Redesign','fps':30,'frames':3851,'canvas':[1920,1080],'panel':[816,72,1040,936],'planning_lane':[816,72,1040,936],'theme':T,'founder_asset':'03_founder/Founder_Gradient_30fps.mkv','cinematic_settings':'01_script/Cinematic_Settings.json','scenes':[dict(id=n,start=round(a*30),end=round(b*30)) for n,a,b in SCENES],'elements':E,'surfaces':S,'sounds':[4,6.5,14.8,32,44.5,48.5,54.166667,68,79,83.9,91.2,99.166667],'graphics_clear_frame':3240,'market_clear_frame':1770,'source_take_untrimmed':True,'source_fps':24,'website_crop':[12,12]}
(R/'01_script/Production_Config.json').write_text(json.dumps(config,indent=2))
with (R/'01_script/Graphic_Cues.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['element','channel','start_frame','end_frame','start_seconds','end_seconds','source_asset'])
 for e in E:w.writerow([e['id'],e['channel'],e['start'],e['end'],e['start']/30,e['end']/30,e.get('image') or e['extra'].get('asset','')])
node=NODE;sharp=SHARP
js=f"const fs=require('fs'),sharp=require({json.dumps(sharp)});(async()=>{{for(const f of fs.readdirSync({json.dumps(str(G/'svg'))}).filter(f=>f.endsWith('.svg'))){{await sharp({json.dumps(str(G/'svg'))}+'/'+f).png().toFile({json.dumps(str(G/'png'))}+'/'+f.replace('.svg','.png'));}}await sharp({json.dumps(str(G/'01_wordmark.svg'))}).png().toFile({json.dumps(str(G/'01_wordmark.png'))});}})();"
subprocess.run([node,'-e',js],check=True)
print('Prepared',len(E),'elements and',len(S),'opaque surfaces')
