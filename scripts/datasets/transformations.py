# -*- coding: utf-8 -*-
"""Controlled transformation catalogue: deterministic, FFmpeg-only, no generative AI.
(id, name, family, relation label, meaning_change_potential, modalities, heldout_test_only, description)"""
CATALOGUE = [
 ("T01", "reencode_hq", "compression", "identical_content_reencoded", "none", "video+audio", False, "Re-encode H.264/AAC CRF 18 (format conversion, visually near-identical)."),
 ("T02", "recompress_low", "compression", "near_duplicate_recompressed", "none", "video+audio", False, "Downscale to 360p, CRF 34, AAC 64k (platform-style recompression)."),
 ("T03", "trim_middle", "temporal", "partial_temporal_copy", "possible", "video+audio", False, "Keep 15%-75% of the duration."),
 ("T04", "trim_head", "temporal", "partial_temporal_copy", "possible", "video+audio", False, "Remove the first 20%."),
 ("T05", "trim_tail", "temporal", "partial_temporal_copy", "possible", "video+audio", False, "Remove the last 25%."),
 ("T06", "crop_center", "spatial", "spatial_edit", "possible", "video", False, "Centre crop to 80% width/height."),
 ("T07", "caption_burn_in", "text", "text_overlay_added", "possible", "video", False, "Burn in a caption taken from the title of a DIFFERENT real source record (constructed pairing, not a natural post)."),
 ("T08", "watermark_overlay", "overlay", "text_overlay_added", "none", "video", False, "Semi-transparent 'repost' watermark top-right."),
 ("T09", "audio_replace", "audio", "audio_replaced", "possible", "audio", False, "Replace the audio track with audio from a DIFFERENT real source recording (looped/trimmed); controlled composite."),
 ("T10", "audio_mute", "audio", "audio_removed", "none", "audio", False, "Remove the audio track."),
 ("T11", "mirror_color_shift", "spatial", "spatial_edit", "none", "video", True, "Horizontal flip + brightness/saturation/contrast shift. TEST-ONLY unseen transformation."),
 ("T12", "speed_change", "temporal", "speed_altered", "possible", "video+audio", True, "1.25x speed. TEST-ONLY unseen transformation."),
 ("T13", "reupload_sim", "compression", "reupload_screen_record_like", "none", "video+audio", True, "480x270 letterbox, 24 fps, CRF 36, mono 48k. TEST-ONLY unseen."),
 ("T14", "audio_noise_mix", "audio", "audio_mixed", "none", "audio", True, "Mix a different real source's audio at 30% under the original. TEST-ONLY unseen."),
]
BY_ID = {c[0]: c for c in CATALOGUE}
# chains extend an existing first-generation variant: (chain_id, start transform, further transforms)
CHAINS = [("C1", "T03", ["T07", "T02"]), ("C2", "T03", ["T08"]), ("C3", "T06", ["T08"]), ("C4", "T09", ["T02"]), ("C5", "T04", ["T06", "T02"])]
