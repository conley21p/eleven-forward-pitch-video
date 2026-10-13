"""Rebuild source graphics and the exact two-minute delivery; never promote external revisions."""
import sys, subprocess, shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
assert shutil.disk_usage(R).free > 25*1024**3, 'Need at least 25 GiB free for rebuild.'
steps=['design.py','community.py','belt_trace.py','audio.py','motion.py','source_project.py','delivery.py','color_metadata.py','project.py','verify_delivery.py','verify_project.py','fingerprint.py']
for script in steps:
    print('Starting',script,flush=True)
    subprocess.run([sys.executable,str(R/'scripts'/script)],check=True,cwd=R)
