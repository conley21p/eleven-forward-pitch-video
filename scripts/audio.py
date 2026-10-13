from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
from pathlib import Path
import subprocess,json,numpy as np
R=Path(__file__).resolve().parents[1];C=json.loads((R/'01_script/Production_Config.json').read_text());rate=48000;N=round(C['frames']/30*rate)
raw=subprocess.check_output([FFMPEG,'-v','error','-i',str(R/'04_audio/Founder_Dialogue.wav'),'-f','f32le','-ac','1','-ar',str(rate),'-'])
v=np.frombuffer(raw,np.float32).copy();v=np.pad(v,(0,max(0,N-len(v))))[:N];s=np.zeros(N,np.float32);rng=np.random.default_rng(1108);report=[]
for t in C['sounds']:
 a=round(t*rate);L=round(.14*rate);noise=rng.standard_normal(L);noise=np.convolve(noise,np.ones(17)/17,'same');env=np.sin(np.linspace(0,np.pi,L))**2
 effect=noise*env;rms=np.sqrt(np.mean(v[max(0,a-rate//2):min(N,a+rate)]**2));effect*=rms*10**(-28/20)/max(1e-8,np.sqrt(np.mean(effect**2)));s[a:a+L]+=effect.astype(np.float32);report.append({'time':t,'rms_below_nearby_dialogue_db':28,'length_seconds':.14})
assert not np.any(s[108*rate:]);assert np.max(np.abs(v+s))<=1
for name,data in [('Motion_Sounds.wav',s),('Dialogue_And_Motion.wav',v+s)]:
 p=subprocess.run([FFMPEG,'-v','error','-y','-f','f32le','-ar',str(rate),'-ac','1','-i','-','-c:a','pcm_s24le',str(R/'04_audio'/name)],input=data.astype('<f4').tobytes());assert p.returncode==0
(R/'09_qc/Sound_Cues.json').write_text(json.dumps(report,indent=2))
print('Original dialogue retained; new quiet sound cues finish before 108s')
