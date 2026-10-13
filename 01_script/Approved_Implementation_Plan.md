# Eleven Forward Final Graphics Redesign

## 1. Summary and confirmed decisions

Rebuild the pitch graphics around the **black, deep-green, lime, and white theme from PowerPoint slides 1 and 7**. Use the supplied photographs, product images, and embedded animations as the source assets. Restyle light-background graphics to match the new theme while preserving their content and composition.

The revision will:

- Preserve the complete original founder performance: **1920×1080, 30 fps, 3,851 frames, approximately 128.37 seconds**.
- Include the pending **additional 4% wider crop**.
- Keep every graphic as a right-side pop-up, with the founder visible.
- Return the founder to center by **1:48**, then show the founder alone through the end.
- Include still previews, an editable project, and final clean and captioned exports.

The confirmed market sequence is population → target audience → market calculation, with all market graphics gone by **0:59**. Entrances may follow nearby spoken phrases; explicit exit deadlines take priority.

The new funding graphic will use **slide 8 alone**, without adding a separate $3,000 heading.

## 2. Source assets and consistent visual theme

### PowerPoint asset handling

The deck contains six still images and two embedded videos. Extract the original media directly from the PPTX rather than capturing screenshots of slides.

| Slide | Supplied asset | Planned use |
|---|---|---|
| **1** | 2172×724 Eleven Forward logo image | Opening founder banner and brand reference |
| **2** | 1795×876 exterior belt image | Left image in the paired product presentation |
| **3** | 1726×911 interior belt composite | Right image in the paired product presentation |
| **4** | 1810×869 screenshot containing an ostomy illustration | Extract and restyle the illustration for the opening explanation |
| **5** | 960×640, 30 fps, **8-second video** | Material/shape/design animation |
| **6** | 960×640, 30 fps, **9-second video** | Community animation, rebuilt in the dark theme |
| **7** | 1536×1024 Eleven Forward/Stealth Belt comparison | Comparison pop-up |
| **8** | 1672×941 development-to-studio graphic | Funding/prototype-development pop-up |

Preserve the originals and record the slide number, embedded filename, dimensions, duration, and checksum in an asset manifest.

For composite images, reuse their original picture regions wherever possible. Do not regenerate the people, belt geometry, or product details simply to change surrounding styling. Recreate text, backgrounds, and layout elements separately when required for the new theme.

### Theme specification

Use these shared design tokens:

| Element | Treatment |
|---|---|
| Main surface | Opaque deep green **#0F1712** |
| Logo background | Black **#000000** |
| Accent | Lime **#D3F928**, sampled from slide 1 |
| Primary text | Warm white **#F7F8F5** |
| Supporting text | Muted sage **#A6B4A1** |
| Secondary surfaces | Dark green **#193728** |
| Corners | 16 px on new pop-ups; preserve supplied artwork’s internal geometry |
| Padding and gaps | 40 px outer padding; 24 px between major elements |
| Typography | Arial Bold/Regular for rebuilt text; retain original raster lettering where the supplied graphic is used intact |
| Motion | Brief fades and restrained horizontal movement; steady holds |

Remove the translucent white surfaces and their moving frosted-background layers. Keep the separate right-side background blur on the founder footage, fading away as the founder returns to center.

Use lime for small labels, rules, selected details, and emphasis. Avoid lime-filled large panels or additional decorative effects.

### Layout families

- **Media pop-ups:** fit within the right-side region **x816–1856**, using widths of 960–1040 px and preserving image proportions.
- **Embedded-video pop-ups:** use their native **960×640** canvas at approximately **x856, y196**, avoiding enlargement.
- **Market pop-ups:** use one consistent **880×520** surface at **x896, y270**, smaller than the current market card.
- **Text hierarchy:** headings 40–48 px; principal statistics 80–88 px; calculation result approximately 64 px; supporting copy 28–32 px; qualifications 22–24 px.
- Keep the lower caption area clear. Original screenshot/interface text may be smaller, but principal messages and qualifications must remain readable at normal 1080p playback.

Retain the source arrows within slide 8 because they are part of the newly supplied design. Do not introduce additional arrows elsewhere.

## 3. Revised timeline and graphic behavior

Times below are snapped to the 30 fps timeline. Short intentional gaps remain founder-only.

| Time | Implementation |
|---|---|
| **Opening–0:03.57** | Replace the existing italic wordmark with the exact slide 1 logo. Preserve the lower-left banner’s position, shape, founder name, and departure timing. Use a black surface and white **Founder: Manning Price** subtitle. |
| **0:04–0:06.50** | Replace “2022 / An ostomy saved my life” with the slide 4 ostomy illustration. Preserve the current entrance and exit timing. |
| **0:06.50–0:14.80** | Retain both race photographs and “9 months later,” restyled in the new theme. Extend their hold to the new product entrance. |
| **0:14.80–0:29.13** | Show slides 2 and 3 beside each other, entering on “product.” Retain **Ostomy Belt** as the heading. Remove the current single cutout and all activity-label pop-ups. |
| **0:29.13–0:36.40** | Remove the current Material graphic completely. No replacement pop-up during this interval. |
| **0:36.40–0:42** | Replace the existing Rethinking graphic with slide 5’s animation, entering on “material.” Speed its complete eight seconds into **5.6 seconds**, approximately **1.43×**. |
| **0:42–0:43** | Founder only. Remove the triathlon photograph that previously appeared around 0:41. |
| **0:43–0:47** | Replace the existing community graphic with the slide 6 animation, rebuilt in the dark theme. Compress the complete nine-second sequence into four seconds: **2.25×**. |
| **0:47–0:50.70** | Show **725K–1M Americans living with an ostomy**, with UOAA attribution. |
| **0:50.70–0:54.17** | Show **200,000 potential customers**, **Ages 13–44**, and the class-research qualification. Enter on the spoken demographic figure. |
| **0:54.17–0:59** | Show the aligned **200,000 × $120 = $24,000,000.00** calculation. Reveal the result near its spoken cue and clear the whole graphic by 0:59. |
| **0:59–1:12.97** | Founder only. Remove the existing Stealth Belt website section beginning around 1:05. |
| **1:12.97–1:18** | Show slide 7’s comparison, entering on “Stealth Belt.” Preserve both photographs, headings, and the distinction between **AI concept visualization** and **Original photo**. |
| **1:18–1:19** | Founder only. |
| **1:19–1:23** | Move the existing SIIL website graphic into this interval. Remove the old three-panel comparison. |
| **1:23–1:23.90** | Founder only. |
| **1:23.90–1:31.20** | Retain target retail and COGS in a smaller dark economics pop-up. Remove the belt image. Preserve the existing spoken reveal cues for **$120** and **≈10% of retail**. |
| **1:31.20–1:39.17** | Retain the giving-program content, rebuilt in the new theme. Preserve the existing sentence-level reveal timing. |
| **1:39.17–1:48** | Replace the current funding/belt graphic with slide 8. Use the supplied composition without an additional $3,000 label. |
| **1:47.20–1:48** | Fade the final pop-up out and move the founder smoothly back to center over 24 frames. Fade the right-side background blur out with that move. |
| **1:48–2:08.37** | Centered founder only. Remove the support-network illustration, role labels, and closing banner. Dialogue continues in full. |

### Specific asset treatments

**Slide 4 — ostomy illustration**

Use the anatomical illustration and its wording, rather than displaying a screenshot containing a second copy of the founder. Remove the screenshot’s surrounding presentation content and Canvas interface overlay from the new composition.

Rebuild the dark surface, white heading **Colostomy / Ileostomy**, and supporting text **Illustration · placement varies**. Preserve the illustrated anatomy, pouch position, and proportions. If the illustration cannot be cleanly isolated, use a reference-guided image edit to match it closely; do not invent additional anatomical details.

**Slides 2 and 3 — paired belt images**

Display both complete images in equal-width columns with matching top alignment and balanced padding. Keep the dark studio backgrounds, image proportions, and all supplied interior details. Label the interior image **Design concept** so it does not imply a verified functional mechanism.

**Slide 5 — product-detail animation**

Its existing dark styling already matches the new theme closely. Use the actual embedded animation, including its detail magnifier and Material/Shape/Design sequence. Apply time remapping without looping, optical-flow interpolation, or invented intermediate product poses.

**Slide 6 — community animation**

Rebuild the cream canvas as deep green, with white headings, sage secondary text, and lime figures. Match the supplied row order, entrances, counter progression, and final holds.

Preserve the supplied content:

- **Louise is getting better — 188.7K TikTok followers**
- **mrcolitiscrohns — 398K Instagram followers**
- **Sara Levitt — 57.4K Instagram followers**

Retain both qualifications: follower counts are from the supplied profiles, and audiences may overlap. These figures remain historical supplied content, not a current market-size calculation or endorsement.

**Market cards**

Use fixed left anchors and consistent line spacing. Keep the market calculation to two input rows, a quiet divider, and the result—without arrows or animated counters.

Retain the qualifications that the demographic figure is class research, the calculation assumes one belt per potential customer, and purchase frequency is not established. Do not label the graphic as proven annual revenue.

**SIIL website**

Reuse the existing square webpage recording and its matching crop. Preserve webpage colors and branding inside the new dark shell. Keep the existing scrollbar removal and retime the 4.2-second source to the four-second slot without looping.

**Slide 8 — funding**

Preserve the supplied CAD view, interior construction image, professional-studio message, and development stages. Use the entire composition with proportional scaling. Keep **in progress** and **planned** statuses intact.

## 4. Implementation and production workflow

### Preserve source quality and framing

Create a separate revision based on the current verified edit and its pending crop settings.

Use the approved pending crop:

- Source crop: **2129.92×1198.08**
- Source y: **382**
- Opening/closing x: **858.04**
- Main-pitch x: **1381.52**
- Opening movement: frames **83–107**
- Revised return movement: frames **3216–3240**

Sample the original 4K recording once into the output frame. Retain the lossless FFV1 RGB speaker intermediate, no face/body tracking, no person matting, and no artificial sharpening.

Preserve the original voice, recording speed, and 24-to-30 fps source cadence. Keep motion sounds quiet and remove sounds belonging to deleted graphics. Finish all motion sounds by 1:48.

### Update the editable system

Use the existing Kdenlive, procedural graphics, and FFmpeg workflow. No additional application is required.

Extend the shared configuration with:

- The new theme colors, typography, spacing, and surface styles.
- Asset references linked to PowerPoint slide numbers.
- Revised scene intervals and source-video speed mappings.
- The earlier founder-centering cue.
- Explicit removal of the closing banner and all post-1:48 graphic layers.

Keep text, photographs, source videos, and surrounding graphic elements separately editable where practical. Retain supplied raster composites as original assets even when their presentation is rebuilt.

Update the Kdenlive project, cue table, asset manifest, graphic guide, rebuild scripts, and cache fingerprints together. Rebuilding must preserve the new theme, crop, timing, and removals.

### Build order

1. **Storage preflight:** the last inspection showed only about 117 MiB free. Require at least **25 GiB free** before full rendering. Reclaim only verified redundant archives or reproducible caches; preserve source media, current deliverables, and the developer handoff.
2. Extract and inventory the PowerPoint assets.
3. Build the shared theme and restyled still layouts.
4. Prepare the two timed video inserts and the SIIL insert.
5. Produce representative still previews against the pending wider founder framing.
6. Inspect and correct layout, asset fidelity, and readable text.
7. Build the complete native timeline and regenerate the speaker intermediate with the earlier return to center.
8. Export clean and captioned MP4s directly from the same composition, plus a ProRes archive.
9. Complete final checks, then promote the new revision as current.

## 5. Verification and delivery

### Acceptance checks

- Every requested PowerPoint asset is accounted for in the timeline and manifest.
- Supplied photographs and belt imagery retain their proportions and details.
- All rebuilt surfaces follow the dark-green/black, lime, and white theme.
- Both embedded animation sequences reach their intended final state before their exit.
- Market graphics disappear by **0:59**.
- The removed Material, triathlon, Stealth website, old comparison, funding belt, support-network, and closing-banner graphics do not reappear.
- Slide 7’s AI/original-photo distinction remains visible.
- SIIL playback has no scrollbar, stretching, or poster jump.
- Retail and COGS remain targets; the giving program remains an intention.
- The founder is centered and all graphic overlays are gone at **1:48**.
- No graphics cover the founder’s face or hands.
- Both final MP4s contain **3,851 frames at 30 fps**, decode completely, and retain synchronized dialogue.
- The lossless speaker intermediate matches its uncompressed processing output in representative checks.
- The native project opens with all media resolved and matches the rendered composition at sampled states.

### Deliverables

- Updated clean and captioned MP4s.
- ProRes archive.
- Editable Kdenlive project.
- Extracted original PowerPoint media and restyled graphic sources.
- Updated captions, cue table, asset manifest, and graphic guide.
- Representative previews and a concise verification report.

The original performance and its spoken wording remain intact. The new theme and supplied asset choices supersede earlier graphic styling; the explicit 1:48 founder-only ending supersedes the previous 1:59.7 centering cue.
