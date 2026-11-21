#!/bin/sh
# Container entry point: fetch the large tables once (needs ORVEX_MEDIA_BASE), then start the API + web app on $PORT (7860 on Hugging Face).
set -e
python scripts/fetch_data.py
exec python -m uvicorn main:app --app-dir src/orvex/api --host 0.0.0.0 --port "${PORT:-7860}" --log-level info
