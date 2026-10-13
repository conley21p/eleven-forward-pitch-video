# AirDropped source replacement

Source: Flow_VID_20261010_112849_02_081.MOV, copied unchanged to03_founder/Original_Camera_Take.mov. 3840×2160, HEVC SDR Rec.709, approximately26.3Mbps. Earlier transferred source was8.65Mbps H.264.

The AAC audio payload hashes match exactly, so existing dialogue and speech cues are retained. Actual source presentation timestamps select frames on the30fps timeline. No optical flow, face restoration or tracking. Original fixed framing and spatial right-side blur are unchanged.

The RGB founder intermediate uses mathematically lossless libx264rgb CRF0 in Matroska to avoid intermediate color subsampling. Fourteen independent source comparisons are pixel identical. Final MP4s are encoded once from the composited RGB frames usingCRF10. The archive isProRes422HQ.

Disk cleanup: user-authorized removal of the generated archives inGlowing_Belt_Revision andSpeaker_Quality_Revision. TheirMP4s, projects and media remain. Subsequently verified and removed44 closed abandoned Git tmp_pack files, freeing300.73GiB. No valid Git objects or refs were removed. Other older archives were retained.
