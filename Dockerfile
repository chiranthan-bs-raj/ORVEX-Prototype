# ORVEX Prototype: one container = React build + FastAPI. Videos are streamed from object storage (ORVEX_MEDIA_BASE), not baked into the image.
FROM node:22-slim AS web
WORKDIR /w
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app src ./src
COPY --chown=app:app scripts/fetch_data.py ./scripts/fetch_data.py
COPY --chown=app:app data ./data
COPY --chown=app:app docs/datasets ./docs/datasets
COPY --chown=app:app start.sh ./start.sh
COPY --from=web --chown=app:app /w/dist ./frontend/dist
RUN chmod +x start.sh && mkdir -p /tmp/orvex_app && chown app:app /tmp/orvex_app /app/data/derived/tables
ENV ORVEX_APP_DIR=/tmp/orvex_app PORT=7860 PYTHONUNBUFFERED=1
USER app
EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:7860/api/health')"
CMD ["./start.sh"]
