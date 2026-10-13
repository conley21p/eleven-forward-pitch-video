from runtime import FFMPEG,FFPROBE,NODE,SHARP,CAPTION_FFMPEG,MELT
"""Write explicit Rec.709 bitstream/container tags with stream copy, never re-encode."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1];FF=FFMPEG;report=[]
for p in sorted((R/'08_exports').glob('*_WORKING.*')):
 d=json.loads(subprocess.check_output([FFPROBE,'-v','error','-show_streams','-of','json',str(p)]));v=next(x for x in d['streams'] if x['codec_type']=='video')
 if all(v.get(k)=='bt709' for k in ['color_space','color_primaries','color_transfer']):continue
 bsf='h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0' if v['codec_name']=='h264' else 'prores_metadata=color_primaries=bt709:color_trc=bt709:colorspace=bt709'
 tmp=p.with_name(p.stem+'_tagged'+p.suffix)
 subprocess.run([FF,'-v','error','-y','-i',str(p),'-map','0','-c','copy','-bsf:v',bsf,'-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart+write_colr',str(tmp)],check=True)
 tmp.replace(p);report.append({'asset':p.name,'method':'stream copy; bitstream and container Rec.709 tags; no image/audio re-encoding'})
(R/'09_qc/Color_Metadata.json').write_text(json.dumps(report,indent=2))
print('Rec.709 metadata verified or explicitly tagged on all working exports')
