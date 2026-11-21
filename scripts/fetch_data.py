"""Downloads the data that is too big for GitHub from the ORVEX-Prototype-Media dataset on Hugging Face (public, no token needed).

  python scripts/fetch_data.py            # the 3 large tables (~410 MB): required to start the app
  python scripts/fetch_data.py --media    # also every video listed in data/media_manifest.csv (~16.6 GB): only for a fully offline run

Reads ORVEX_MEDIA_BASE (e.g. https://huggingface.co/datasets/<user>/ORVEX-Prototype-Media/resolve/main). Standard library only."""
import csv, os, sys, time, urllib.request

ROOT = os.environ.get("ORVEX_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE = os.environ.get("ORVEX_MEDIA_BASE", "").rstrip("/")
TABLES = ["media_relationship_edges.csv", "real_world_media_master.csv", "platform_observations.csv"]


def get(rel, size=None):
    dest = os.path.join(ROOT, *rel.split("/"))
    if os.path.exists(dest) and os.path.getsize(dest) > 0 and (size is None or os.path.getsize(dest) == size):
        return False
    if not BASE: sys.exit("ORVEX_MEDIA_BASE is not set, cannot download " + rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True); tmp = dest + ".part"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(BASE + "/" + rel, headers={"User-Agent": "orvex-fetch"}), timeout=120) as r, open(tmp, "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b: break
                    f.write(b)
            if size is not None and os.path.getsize(tmp) != size: raise IOError("size mismatch")
            os.replace(tmp, dest); print("downloaded", rel, flush=True); return True
        except Exception as e:
            print("retry", rel, e, flush=True); time.sleep(2 * (attempt + 1))
    sys.exit("could not download " + rel)


if __name__ == "__main__":
    for t in TABLES: get("data/derived/tables/" + t)
    if "--media" in sys.argv:
        with open(os.path.join(ROOT, "data", "media_manifest.csv"), encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for i, r in enumerate(rows, 1):
            get(r["path"], int(r["bytes"]))
            if i % 100 == 0: print(i, "/", len(rows), flush=True)
    print("data ready")
