# Eleven Forward pitch video — editable collaboration project

This repository contains the current approved two-minute edit and the media needed to reopen it: original AirDropped 4K camera take, dialogue, graphics, images, website recordings, animation clips, editable SVGs, Python generators, captions, Kdenlive projects, and clean/captioned/archive exports. Historical revisions and application installers are not included.

## Open the edit

Install Git LFS and Kdenlive. Clone normally; **Download ZIP on GitHub does not reliably supply LFS media**.

```sh
git clone <repository-url>
cd <repository-folder>
git lfs install
git lfs pull
python3 scripts/restore_media.py
python3 scripts/check_checkout.py
```

Open `07_kdenlive/Source_ElevenForward_Kinetic.kdenlive` to edit the independent scene/graphics layers. This full-length source timeline is 128.37 seconds. The current final `ElevenForward_Kinetic.kdenlive` is a 120-second delivery assembly using the rendered archive; it is not the layered authoring timeline. Captioned variants of both are included.

The final delivery retains all spoken content, trims trailing silence, and plays at 1.066111111× with original voice pitch preserved. It is 1920×1080, 30 fps, 3,600 frames. Use `01_script/Production_Config.json` for source graphic timing and `Delivery_Config.json` / `Delivery_Graphic_Cues.csv` for delivery timing. Changing the layered Kdenlive timeline manually does **not** update the procedural renderer: either render that timeline in Kdenlive and retime the result yourself, or change generator/configuration sources and use the scripted build.

## Large media

All binary media is tracked with Git LFS. Two oversized files are stored as ≤1 GiB LFS parts under `media_parts/`; the restore command verifies hashes and reconstructs their original paths. The original full files remain available in this local checkout but are ignored by Git to avoid duplicate storage. The complete project is approximately 11 GiB; allow 30–40 GiB for a clone including LFS cache, restored media, and a rebuild. Check hosting LFS storage/bandwidth allowances before uploading. Anyone with repository access also receives the founder footage and supplied reference media.

After changing either oversized file, run `python3 scripts/pack_media.py` before committing to refresh its parts and hashes. Do not manually edit part files.

## Build dependencies

Use Python 3.11+, Node.js LTS, FFmpeg/FFprobe with libx264, prores_ks and libass, and Kdenlive/MLT. Keep Arial installed for consistent typography. Required downloads are from the vendors: https://kdenlive.org/en/download/ , https://git-lfs.com/ , https://www.python.org/downloads/ , https://nodejs.org/ , https://ffmpeg.org/download.html . No paid software or Mac installers are bundled.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm install
python scripts/check_checkout.py
```

Scripts locate tools on PATH. Override `EF_FFMPEG`, `EF_FFPROBE`, `EF_NODE`, `EF_SHARP`, `EF_CAPTION_FFMPEG`, and `EF_MELT` if needed. On macOS MLT may be inside `/Applications/kdenlive.app/Contents/MacOS/melt`; Kdenlive's bundled FFmpeg can be used for libass captions. Preserve Rec.709 interpretation. The speaker intermediate is lossless; do not replace it with a low-bitrate proxy for final rendering.

`python scripts/rebuild.py` regenerates source graphics and the exact two-minute delivery, then verifies outputs and native projects. It uses the included lossless founder intermediate. To change founder cropping, modify cinematic settings and run `python scripts/founder.py` then `python scripts/quality.py` before rebuilding. `scripts/legacy/` contains historical commands for provenance and is not the supported pipeline. A complete render is intentionally not run during repository setup.

## Work together

Create a branch for each change (`git switch -c editor/your-change`). Commit scripts/SVGs/configuration and regenerated assets together, push the branch, and review before merging. Kdenlive XML files can conflict: agree on one editor per timeline at a time. Use Git LFS for media; never commit credentials, API keys, caches, installers, or temporary renders. Keep the known-good exports until the new export passes review.

```sh
git add .
git commit -m "Describe the edit"
git push -u origin editor/your-change
```

The collaboration repository is private: https://github.com/conley21p/eleven-forward-pitch-video .

```sh
git clone https://github.com/conley21p/eleven-forward-pitch-video.git
cd eleven-forward-pitch-video
git lfs pull
python3 scripts/restore_media.py
python3 scripts/check_checkout.py
```

Add the collaborator through repository Settings → Collaborators after publishing. Verification evidence supplied in `09_qc/` describes the current exported video; it is historical evidence until rerun on subsequent edits.
