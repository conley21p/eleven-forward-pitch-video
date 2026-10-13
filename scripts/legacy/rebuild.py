"""Authoritative pipeline. Never restores legacy designs or mutates earlier revisions."""
from pathlib import Path
import subprocess,shutil,json
R=Path(__file__).resolve().parents[1]
VIDEO='/tmp/pitch-video-venv/bin/python'
DOC='/Users/conleyprice/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
assert shutil.disk_usage(R).free>=25*1024**3,'At least25GiB free is required before rebuilding. Preserve originals and current exports.'
# Detach reusable derived hardlinks before rebuilding, preserving the prior revision.
for relative in ['03_founder/Founder_Gradient_30fps.mkv','04_audio/Motion_Sounds.wav','04_audio/Dialogue_And_Motion.wav','00_references/final_powerpoint/Community_Dark_Original_Motion.mkv']+[str(p.relative_to(R)) for p in (R/'05_graphics/motion').glob('*.mov')]:
 p=R/relative
 if p.exists() and p.stat().st_nlink>1:
  temp=p.with_name(p.name+'.detached');shutil.copy2(p,temp);temp.replace(p)
steps=[(DOC,'design.py'),(VIDEO,'community.py'),(VIDEO,'founder.py'),(VIDEO,'quality.py'),(VIDEO,'audio.py'),(VIDEO,'preview.py'),(VIDEO,'motion.py'),(VIDEO,'composite.py'),(VIDEO,'project.py'),(VIDEO,'native_check.py'),(VIDEO,'full_scan.py'),(VIDEO,'color_metadata.py'),(VIDEO,'publish.py'),(DOC,'documentation.py'),(DOC,'fingerprint.py')]
for python,script in steps:
 print('Starting',script,flush=True);subprocess.run([python,str(R/'scripts'/script)],check=True)
print('Rebuild complete. Inspect review before running promote.py.')
