# -*- coding: utf-8 -*-
"""Gate 4: controlled variants rendered ONLY from eligible real-world media (RW-01 Commons, usable_for_variants=True)."""
import os, sys, re, json, hashlib, unicodedata, time, csv
import cv2
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from transformations import *

VB = os.path.join(BUILD, "variants"); os.makedirs(VB, exist_ok=True)
STD = ["-threads", "4", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", "-map_metadata", "-1"]
EVEN = "scale=trunc(iw/2)*2:trunc(ih/2)*2"
TOOLV = ffmpeg_version()

def ascii_text(s, n=48):
    s = re.sub(r"^File:", "", s); s = re.sub(r"\.[A-Za-z0-9]{3,4}$", "", s); s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9 ,.\-]", " ", s); return (re.sub(r"\s+", " ", s).strip()[:n].strip()) or "untitled"
def pick(seq, key): return seq[int(hashlib.sha256(key.encode()).hexdigest(), 16) % len(seq)]

def build(tid, inp, outp, info, ctx):
    d = info["duration_s"] or 10; has_a = info["has_audio"]
    meta = ["-metadata", f"comment=ORVEX controlled variant {ctx['vid']} of {ctx['root']}; not authentic media"]
    pre, post, extra_in, fc, af = [], [], [], None, None; vf = [EVEN]; params = {}
    if tid == "T01": post += ["-crf", "18"]; params = dict(crf=18)
    elif tid == "T02": vf = ["scale=-2:360", EVEN]; post += ["-crf", "34", "-b:a", "64k"]; params = dict(crf=34, height=360, audio_bitrate="64k")
    elif tid in ("T03", "T04", "T05"):
        a, b = {"T03": (0.15, 0.75), "T04": (0.20, 1.0), "T05": (0.0, 0.75)}[tid]; ss, to = round(d * a, 2), round(d * b, 2)
        pre += ["-ss", str(ss)]; post += ["-t", str(round(to - ss, 2)), "-crf", "23"]; params = dict(start_s=ss, end_s=to, kept_fraction=round((to - ss) / d, 3))
    elif tid == "T06": vf = ["crop=trunc(iw*0.8/2)*2:trunc(ih*0.8/2)*2", EVEN]; post += ["-crf", "23"]; params = dict(crop_fraction=0.8, anchor="centre")
    elif tid == "T07":
        vf += [f"drawtext=fontfile='{FONT}':text='{ctx['caption']}':fontsize=h/18:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8:x=(w-text_w)/2:y=h-text_h-h/12"]
        post += ["-crf", "23"]; params = dict(caption=ctx["caption"], position="bottom-centre")
    elif tid == "T08":
        vf += [f"drawtext=fontfile='{FONT}':text='repost':fontsize=h/24:fontcolor=white@0.7:box=1:boxcolor=black@0.35:boxborderw=6:x=w-text_w-w/30:y=h/30"]; post += ["-crf", "23"]; params = dict(text="repost", opacity=0.7, position="top-right")
    elif tid == "T09": extra_in = ["-stream_loop", "-1", "-i", ctx["donor_path"]]; post += ["-map", "0:v:0", "-map", "1:a:0", "-t", str(d), "-crf", "23"]; params = dict(audio_donor=ctx["donor_id"], looped=True)
    elif tid == "T10": post += ["-an", "-crf", "23"]; params = dict(audio="removed")
    elif tid == "T11": vf = ["hflip", "eq=brightness=0.06:saturation=1.25:contrast=1.05", EVEN]; post += ["-crf", "23"]; params = dict(hflip=True, brightness=0.06, saturation=1.25, contrast=1.05)
    elif tid == "T12": vf = ["setpts=PTS/1.25", EVEN]; af = "atempo=1.25" if has_a else None; post += ["-crf", "23"]; params = dict(speed=1.25)
    elif tid == "T13": vf = ["scale=480:270:force_original_aspect_ratio=decrease", "pad=480:270:(ow-iw)/2:(oh-ih)/2:color=black"]; post += ["-r", "24", "-crf", "36", "-ac", "1", "-ar", "48000", "-b:a", "48k"]; params = dict(canvas="480x270", fps=24, crf=36)
    elif tid == "T14":
        extra_in = ["-stream_loop", "-1", "-i", ctx["donor_path"]]; fc = "[0:a][1:a]amix=inputs=2:weights='1 0.3':duration=first:dropout_transition=0[a]"; post += ["-map", "0:v:0", "-map", "[a]", "-crf", "23"]; params = dict(audio_donor=ctx["donor_id"], donor_level=0.3)
    args = [FFMPEG, "-y", "-v", "error"] + pre + ["-i", inp] + extra_in
    if fc: args += ["-filter_complex", fc]
    args += ["-vf", ",".join(vf)]
    if af: args += ["-af", af]
    return args + STD + meta + post + [outp], params

def validate(tid, outp, pinfo, oinfo):
    ch = {}; ok = bool(oinfo and oinfo.get("width"))
    ch["probe_ok"] = ok
    if not ok: return False, ch
    dp, do = pinfo["duration_s"] or 0, oinfo["duration_s"] or 0
    exp = {"T03": dp * 0.6, "T04": dp * 0.8, "T05": dp * 0.75, "T12": dp / 1.25}.get(tid, dp)
    ch["duration_expected_s"] = round(exp, 2); ch["duration_actual_s"] = do; ch["duration_ok"] = abs(do - exp) <= max(0.6, 0.04 * exp)
    if tid == "T02": ch["height_ok"] = oinfo["height"] == 360 or abs(oinfo["height"] - 360) <= 2
    if tid == "T06": ch["width_ok"] = abs(oinfo["width"] - round(pinfo["width"] * 0.8)) <= 3
    if tid == "T13": ch["canvas_ok"] = (oinfo["width"], oinfo["height"]) == (480, 270)
    ch["audio_ok"] = (oinfo["has_audio"] is False) if tid == "T10" else (True if tid in ("T09", "T14") and oinfo["has_audio"] else (oinfo["has_audio"] == pinfo["has_audio"] if tid not in ("T09", "T14") else False))
    err = decode_errors(outp); ch["decode_errors"] = err[:80]; ch["decode_ok"] = not err
    cap = cv2.VideoCapture(outp); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0); lum = 0
    if n > 2:
        cap.set(cv2.CAP_PROP_POS_FRAMES, n // 2); r, fr = cap.read()
        if r: lum = float(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).std())
    cap.release(); ch["sample_frame_contrast_std"] = round(lum, 1); ch["sample_frame_ok"] = lum > 2.0
    good = all(v for k, v in ch.items() if k.endswith("_ok") or k == "probe_ok")
    return good, ch

def process(src, pool, master):
    sid = src["media_id"]; ck = os.path.join(VB, sid + ".json")
    if os.path.exists(ck): return json.load(open(ck, encoding="utf-8"))
    root = sid.replace("RW-CMN-", ""); sdir = os.path.join(CVMEDIA, root); os.makedirs(sdir, exist_ok=True); orig = os.path.join(ROOT, src["local_path"]); oinfo = probe(orig)
    donors = [r for r in pool if r["media_id"] != sid and r["has_audio"] == "True"]; od = [r for r in donors if r["_domain"] != src["_domain"]] or donors
    donor = pick(od, sid + "audio"); capsrc = pick([r for r in pool if r["media_id"] != sid], sid + "cap"); caption = ascii_text(capsrc["title"])
    node = {sid: dict(path=orig, info=oinfo)}; recs, logs, k = [], [], [0]
    def make(tid, parent, depth, chain):
        k[0] += 1; vid = f"CV-{root}-V{k[0]:02d}"; p = node[parent]; outp = os.path.join(sdir, vid + ".mp4")
        if tid in ("T10", "T14") and not p["info"]["has_audio"]: return None
        ctx = dict(vid=vid, root=sid, donor_path=os.path.join(ROOT, donor["local_path"]), donor_id=donor["media_id"], caption=caption)
        args, params = build(tid, p["path"], outp, p["info"], ctx); t0 = now(); cat = BY_ID[tid]
        if not budget_ok(300_000_000) or dir_bytes(CVMEDIA) > ALLOC["controlled_variants"]: return "BUDGET"
        rc, err = run(args)
        if rc != 0 and tid in ("T09", "T14"):                    # looping a webm/ogg donor can fail -> retry from decoded WAV copy
            wav = os.path.join(BUILD, "donor_wav", donor["media_id"] + ".wav"); os.makedirs(os.path.dirname(wav), exist_ok=True)
            if not os.path.exists(wav): run([FFMPEG, "-y", "-v", "error", "-i", ctx["donor_path"], "-vn", "-ac", "2", "-ar", "44100", wav])
            ctx["donor_path"] = wav; args, params = build(tid, p["path"], outp, p["info"], ctx); params["donor_decoded_to_wav"] = True; rc, err = run(args)
        vinfo = probe(outp) if rc == 0 and os.path.exists(outp) else None
        good, ch = validate(tid, outp, p["info"], vinfo) if vinfo else (False, {"probe_ok": False})
        b = os.path.getsize(outp) if os.path.exists(outp) else 0
        roots = ["RW-01"]; chain_ids = [parent] if parent != sid else []; anc = []; n = parent
        while n in node and n != sid: anc.append(n); n = [x["parent"] for x in recs if x["variant_media_id"] == n][0]
        rec = dict(variant_media_id=vid, direct_parent_media_id=parent, root_source_media_id=sid, ancestor_chain="|".join(anc + [sid]), video_source_media_id=sid,
                   audio_source_media_id=donor["media_id"] if tid in ("T09", "T14") else "", caption_text_source_media_id=capsrc["media_id"] if tid == "T07" else "", caption_text=caption if tid == "T07" else "",
                   caption_text_origin_field="title" if tid == "T07" else "", transformation_id=tid, transformation_name=cat[1], transformation_family=cat[2], parameters_json=json.dumps(params, ensure_ascii=False),
                   tool_name="ffmpeg", tool_version=TOOLV, run_id=f"RUN-{vid}", seed=f"sha256-pick:{sid}", created_utc=t0, local_path=rel(outp) if good else "", sha256=sha256(outp) if good else "", bytes=b if good else 0,
                   duration_s=vinfo and vinfo["duration_s"], width=vinfo and vinfo["width"], height=vinfo and vinfo["height"], fps=vinfo and vinfo["fps"], has_audio=vinfo and vinfo["has_audio"], generation_depth=depth,
                   chain_id=chain, permission_basis=f"{src['license']} permits adaptation (root); audio/caption sources: {donor['license'] if tid in ('T09','T14') else capsrc['license'] if tid == 'T07' else 'n/a'}",
                   root_license=src["license"], validation_status="passed" if good else "failed", validation_checks_json=json.dumps(ch), failure_reason="" if good else (err.strip()[-150:] or "validation checks failed"),
                   media_origin="controlled_variant", record_origin="orvex_controlled_variant_record", transformation_status="controlled_transformation_applied" if good else "controlled_transformation_failed",
                   usable_for_training=False, source_split="", parent=parent)
        recs.append(rec)
        logs.append(dict(run_id=rec["run_id"], variant_media_id=vid, input_media_ids=parent + ("|" + donor["media_id"] if tid in ("T09", "T14") else ""), tool_name="ffmpeg", tool_version=TOOLV,
                         command_config=" ".join(a if " " not in a else f'"{a}"' for a in args[1:]).replace(ROOT, "<ROOT>"), parameters_json=rec["parameters_json"], started_utc=t0, return_code=rc,
                         output_validation_status="passed" if good else "failed", output_bytes=b, storage_delta_bytes=b, error="" if rc == 0 else err.strip()[-200:], deterministic_notes="parameters fixed; donor/caption picked by sha256 of root id", seed=rec["seed"]))
        if good: node[vid] = dict(path=outp, info=vinfo); return vid
        return None
    first = {}; stop = False
    for t in CATALOGUE:
        r = make(t[0], sid, 1, ""); first[t[0]] = r
        if r == "BUDGET": stop = True; break
    if not stop:
        for cid, start, steps in CHAINS:
            pid = first.get(start)
            if not pid or pid == "BUDGET": continue
            for step_k, tid in enumerate(steps, 2):
                v = make(tid, pid, step_k, cid)
                if not v or v == "BUDGET": break
                pid = v
    out = dict(recs=recs, logs=logs); json.dump(out, open(ck, "w", encoding="utf-8"), ensure_ascii=False); print("done", sid, len(recs), flush=True); return out

if __name__ == "__main__":
    master = load("real_world_media_master"); cj = {f"RW-CMN-P{c['pageid']}": c for c in json.load(open(os.path.join(RWMETA, "commons", "commons_candidates.json"), encoding="utf-8"))}
    pool = [dict(r, _domain=cj[r["media_id"]]["domain"]) for r in master if r["source_dataset_id"] == "RW-01" and r["usable_for_variants"] == "True"]
    pool.sort(key=lambda r: r["media_id"]); print("eligible real-world sources:", len(pool), "payload", payload_bytes())
    with ThreadPoolExecutor(max_workers=6) as ex: res = list(ex.map(lambda s: process(s, pool, master), pool))
    print("variants", sum(len(r["recs"]) for r in res), "payload", payload_bytes())
