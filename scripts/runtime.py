"""Portable executable locations. Override through environment variables."""
import os, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def executable(variable,name):
    return os.environ.get(variable) or shutil.which(name) or name
FFMPEG=executable('EF_FFMPEG','ffmpeg')
FFPROBE=executable('EF_FFPROBE','ffprobe')
NODE=executable('EF_NODE','node')
SHARP=os.environ.get('EF_SHARP',str(ROOT/'node_modules/sharp'))
CAPTION_FFMPEG=os.environ.get('EF_CAPTION_FFMPEG',FFMPEG)
MELT=executable('EF_MELT','melt')
