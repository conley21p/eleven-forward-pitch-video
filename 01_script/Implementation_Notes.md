# Eleven Forward · Final Graphics Redesign

This revision implements the supplied Final pitch prompting updates and slides 1–8. The previous Speaker_Quality_Revision remains unchanged. The approved plan is in 01_script/Approved_Implementation_Plan.md.

## Edit and rebuild

Open 07_kdenlive/ElevenForward_Kinetic.kdenlive (or the captioned project). All required media paths are relative to this revision. V1 is the new lossless RGB founder intermediate; the next layer contains opaque dark surfaces. Each scene has independent image and typography clips, with the original assets in the project bin. A1 is unchanged original dialogue; A2 contains quiet motion sounds. The opening banner is separate. There is no closing banner.

Edit layout, copy, timings and theme in scripts/design.py; it generates Production_Config.json and Graphic_Cues.csv. Edit founder crop and the two movements in Cinematic_Settings.json. scripts/rebuild.py runs the authoritative production pipeline. No legacy backup-restoration hooks are used. Source media and the previous revision are never overwritten. Rebuild requires Python with numpy/OpenCV, Python with Pillow, Node with sharp, FFmpeg/FFprobe and Kdenlive/MLT. The current tool paths are documented in scripts/rebuild.py; set them for another machine. No paid tools or new downloads are needed on this computer.

## Founder quality

3851 frames at 30 fps, 1920×1080 SDR Rec.709. The complete original 4K/24 fps performance and unchanged dialogue stem are preserved. Crop 2129.92×1198.08 at y382; x858.04 opening/closing, x1381.52 main. Smooth moves: frames83–107 and3216–3240. No tracking, person segmentation, portrait blur, optical flow, sharpening or lossy intermediate H.264. Original pixels are sampled once with Lanczos4 into lossless H.264 RGB (CRF0). The established spatial blur ramps only on the right (x880–1160, sigma4), and disappears during the return to center.

## Theme and animation

Surface #0F1712; black banner; lime #D3F928; white #F7F8F5; sage #A6B4A1; row green #193728. Main surfaces have16px corners; community rows use32px corners with clean masked edges and restored creator portraits. Market surfaces fit each state:880×330,880×400 and880×460. Text and statistics use Arial. There are no translucent white cards or live frosted plates.

The belt detail section at32–43.5s is recreated at native30fps using Belt_Trace_Source.png. belt_trace.py derives the external silhouette from alpha, animates a complete top-right-origin perimeter glow that finishes before the material callout, magnifies actual mesh pixels with a glowing connector, traces the full silhouette for Shape and traces the pocket for Design. JSON paths and the editable title SVG are retained. The original slide5 MP4 remains as a reference only. Slide6 uses all270 source frames rethemed by scripts/community.py; original lettering, counting figures and row trajectories are preserved. It maps9s into44.5–48.5s. The first market state starts48.5s; subsequent market cues remain unchanged. This is a faithful color restyle of the original animation, not a static poster or approximation of the counter curve. Slide6_Measured_Motion.json records per-frame row positions and opacity; the immutable source remains available for recoloring. Pixel artwork remains raster; use the accompanying layout specification when editing its words.

The source image on slide4 included a second founder and screenshot UI. Anatomy_Cutout.png is a reference-guided generated extraction; it preserves the depicted torso/pouch arrangement and is identified as an illustration. Slide2 and3 use matching428×300 center crops with24px rounded corners, side by side; slide3 is labeled Design concept. Slide7 remains intact, including AI concept and Original photo labels. Slide8 is intact with its planned/in-progress stages and original arrows; there is no added $3,000 title.

At1:47.2 the funding card moves right and fades while the founder centers, avoiding an overlap with the speaker. At1:48 all editorial overlays and motion sounds are absent. The captioned export still contains the spoken closing captions; “founder only” removes graphics, not accessibility captions.

The “Same person. Different design.” comparison starts entering at68.0s and holds until78s. The79–83s website slot now uses Stealth Belt, with its original square recording and the established scrollbar crop.

## Claims and sound

UOAA supports only725K–1M overall population.200,000 aged13–44 is founder-supplied class research. $24,000,000.00 =200,000 ×$120, one belt per customer; purchase frequency is not established. Historical creator counts are retained from the supplied animation, not verified current counts or endorsements. Target price and COGS remain targets. Giving is an intended program. Spoken wording is unchanged.

Motion sounds are deterministic seeded swishes,0.14s,28dB RMS below nearby dialogue, separate from the original voice. No music. Caption timestamps and words are unchanged.

## Speaker quality refinement

Matched source decoding confirms the lossless speaker intermediate preserves the original crop exactly. H.264 delivery now uses CRF10, adaptive quantization mode3, qcomp0.8 and deblock −1/−1 to retain fine texture. No sharpening, face restoration, tracking or framing changes. The AirDropped source is3840×2160 HEVC SDR Rec.709 at26.3Mbps. It replaces the8.65Mbps transferred H.264 file. Frames are selected by presentation timestamp; decoded audio payloads match exactly. No iOS conversion was applied.

## Outputs and validation

Clean and captioned H.264 CRF10 slow encodes come directly from the same RGB composition, with AAC48kHz192kbps, Rec.709 metadata and faststart. The archive uses ProRes422HQ with PCM audio. Review the Acceptance, Founder_Source_Quality and Native_Comparison reports in09_qc. Full-frame visual previews and source comparisons are in10_review. Final publication is gated on frame counts, full decode, native media resolution, source hashes and sampled source/native comparisons. No new independent Astra grade is claimed for this revision.
