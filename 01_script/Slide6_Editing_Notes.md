# Slide6 source-preserving animation

The original9-second source is media2.mp4. It has270frames at30fps on960×640. community.py preserves the actual row text and counter pixels, recovers the row opacity and horizontal positions from each original frame, and composites those pixels over the new palette. It does not approximate the animated counter values. The resulting lossless clip is sampled across120outputframes for43–47seconds.

Source layout: rows at(38,137),(38,276),(38,415), each885×124. Initial circles68px atx58. Names anchoredx146. Counts right-aligned nearx885. Eyebrowx38/y30; headingx38/y66. Footer atx38/y581 and608.

Content stays Louise is getting better / @louisethompson /188.7K /TikTok; mrcolitiscrohns / @mrcolitiscrohns /398K /Instagram; Sara Levitt /The Bag Bish /57.4K /Instagram. Keep both historical-count and overlapping-audience qualifications.

Edit palette in community.py. To edit wording, replace the relevant source row artwork and counters; the original clip is raster and its words are not native editable text. The measured per-frame motion remains available in Slide6_Measured_Motion.json. Original media is preserved unchanged.
