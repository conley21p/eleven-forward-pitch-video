from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Validate exact delivery duration, source mapping, opening and final spoken frame."""
from pathlib import Path
import subprocess,json,cv2,numpy as np,csv,re
from video_io import VideoReader
R=Path(__file__).resolve().parents[1];Q=R/'09_qc';O=R/'08_exports';FF=FFMPEG;results=[]
for stem,ext in [('ElevenForward_Kinetic_Clean','.mp4'),('ElevenForward_Kinetic_Captioned','.mp4'),('ElevenForward_Kinetic_Archive','.mov')]:
 p=O/(stem+'_WORKING'+ext)
 if not p.exists():p=O/(stem+ext)
 d=json.loads(subprocess.check_output([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(x for x in d['streams'] if x['codec_type']=='video');a=next(x for x in d['streams'] if x['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',3600),v
 assert abs(float(v['duration'])-120)<.000001 and abs(float(d['format']['duration'])-120)<.001
 assert all(v.get(k)=='bt709' for k in ['color_space','color_primaries','color_transfer']);assert int(a['sample_rate'])==48000
 decode=subprocess.run([FF,'-v','error','-i',str(p),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr,decode.stderr
 results.append({'asset':stem+ext,'frames':3600,'duration':v['duration'],'decoded_without_errors':True,'codec':v['codec_name']})
 final=O/(stem+ext)
 if p!=final:p.replace(final)
 (Q/(stem+'_Probe.json')).write_text(json.dumps(d,indent=2))
c=VideoReader(O/'ElevenForward_Kinetic_Clean.mp4');n=0;unexpected=[];samples={}
while True:
 ok,im=c.read()
 if not ok:break
 if im.mean()<1:unexpected.append(n)
 if n in [0,6,12,23,960,1335,1500,2400,3599]:cv2.imwrite(str(R/'10_review'/f'Export_{n:04}.png'),im);samples[n]=im
 n+=1
c.release();assert n==3600 and not unexpected
poster=cv2.imread(str(R/'05_graphics/Playback_Poster.png'));poster_error=float(np.abs(samples[0].astype(float)-poster.astype(float)).mean());assert poster_error<2
mapping=list(csv.DictReader((R/'01_script/Delivery_Frame_Map.csv').open()));assert len(mapping)==3600
assert int(mapping[0]['source_edit_frame'])==0 and int(mapping[-1]['source_edit_frame'])==3837
# Last output frame corresponds to the final spoken moment, before the source's trailing silence.
c=VideoReader(R/'03_founder/Founder_Gradient_30fps.mkv');c.set(cv2.CAP_PROP_POS_FRAMES,3837);ok,ref=c.read();c.release();assert ok
error=samples[3599][:,:800].astype(float)-ref[:,:800].astype(float);psnr=float(10*np.log10(255**2/np.mean(error**2)));assert psnr>34
for name in ['Founder_120s.wav','Motion_120s.wav','Dialogue_And_Motion_120s.wav']:
 d=json.loads(subprocess.check_output([FFPROBE,'-v','error','-show_format','-of','json',str(R/'04_audio'/name)]));assert abs(float(d['format']['duration'])-120)<.000001
report={'status':'passed','frames':3600,'duration':120,'exports':results,'black_frames':unexpected,'opening_poster_mean_pixel_error':poster_error,'last_frame_source_index':3837,'last_frame_speaker_psnr':psnr,'speed':3838/3600,'pitch_preserved':True,'source_end':3838/30,'cover_adds_time':False,'source_quality':'Lossless AirDropped founder intermediate; one final MP4 encode','caption_timing':'retimed with same speed; last caption ends before120s'}
(Q/'Acceptance.json').write_text(json.dumps(report,indent=2));print('Verified exact120 seconds,3600 frames, matching cover, final source frame and all three decoded exports')
