# PROTOTYPE_IMPLEMENTATION.md - What the ORVEX Prototype really does

This file explains, in simple English, what is implemented in the **ORVEX Prototype** (the hackathon demo), where it lives in this repository, and what is not built. It describes the code as it is; planned parts are labelled as planned.

**Read this first.** The prototype is a *viewer and review tool built on real dataset records*. Every video you can play is a real file (public videos, or an edited copy that we made with FFmpeg). The relationships in the graph come from our **log of those edits (ground truth)**. They are **not** predictions of a trained model. The only detector measured so far is a simple, non-learned dHash baseline (test AUC 0.8307). The planned learned model (DINOv2 + similarity head) is **not built**. The prototype is not a production investigation platform.

Status labels used below: **VERIFIED** (tested), **IMPLEMENTED** (code exists, not specifically tested), **PARTIAL**, **CONFIGURED, UNUSED**, **NOT IMPLEMENTED**.

---

## 0. Deployment architecture (new in the published prototype)

```
Browser  ->  Hugging Face Space (Docker, one container)
                 |  React app (built, served as static files)       /, /graph, /evidence ... (page refresh works)
                 |  FastAPI                                        /api/...
                 |  SQLite in the container (users, cases, reviews) - resets when the Space restarts
                 |  FFmpeg (thumbnails)                             reads frames straight from the dataset over HTTPS
                 v
        Hugging Face Dataset "ORVEX-Prototype-Media"  (public)
                 1,727 videos (596 originals + 1,131 variants), 3 large tables, media_manifest.csv
```
- `GET /api/media/{id}/stream` answers with a **307 redirect** to the same path in the dataset, so the browser streams and seeks directly from Hugging Face's storage (`media_src()` in `src/orvex/api/main.py`). If the file also exists on local disk, the local file is used instead.
- `GET /api/media/{id}/frame` runs FFmpeg on the file or on the https address (FFmpeg reads only the bytes it needs) and caches the JPEG.
- Three tables are over 100 MB (the limit of a normal GitHub file), so they are in the dataset and downloaded at container start by `scripts/fetch_data.py` (VERIFIED against a local stand-in server).
- `GET /api/health` returns `{"status": "ok", ...}`.
- Settings come from environment variables (see `.env.example`): `ORVEX_MEDIA_BASE`, `ORVEX_SECRET`, `ORVEX_APP_DIR`, `ORVEX_CORS`, `ORVEX_FFMPEG`, `ORVEX_LOG`.
- Unhandled errors are logged on the server and returned as `{"detail": "internal server error"}` (HTTP 500).
- **Persistence limit:** on the free Space the SQLite file is on temporary disk. Demo accounts are re-created at every start; investigations and review decisions made on the public demo are lost when the Space restarts or rebuilds. The dataset itself is never changed by the app.

---

## 1. Project overview

**ORVEX** (Origin and Relationship Verification Explorer) is a capstone project (PES University, PW_27_BS_01). The idea: given one *reference video*, find other videos that are copies, edits or re-uploads of it, work out which one came first, and keep the evidence so that a human investigator can accept or reject each finding.

**The problem:** the same video is trimmed, cropped, captioned, re-compressed or re-shared many times. Looking at two files, it is hard to tell whether they are related, and which one is the parent.

**What the demo does today:**

1. A user signs in.
2. They pick a reference video from a real collection (Wikimedia Commons videos).
3. The app shows the family of edited versions made from it, as a graph, with real thumbnails, real video playback, real measurements (perceptual hash and audio fingerprint) and links to evidence records.
4. The investigator records a decision per edge (accepted / uncertain / rejected), and downloads a PDF report.

**Who uses it:** an investigator (finds and reviews relationships), a reviewer (the second seeded account, role `reviewer`), and an administrator (role `admin`; the first seeded account). In the code, only `admin` vs. not-admin changes behaviour (the user list on the Admin page).

**Main workflow (real, as implemented):**

```
Login -> Dashboard -> Investigations (create, choose reference video)
      -> Candidate discovery (table of the family)
      -> Relationship graph (inspect, play videos, review each edge)
      -> Video comparison / Provenance / Evidence ledger (look deeper)
      -> Investigation report (PDF download)
```

---

## 2. Technology stack

Verified by reading imports, `frontend/package.json` and running the code. Versions are those found on this machine.

| Technology | Where it is used | What it does in simple English | Status |
|---|---|---|---|
| React 19 + TypeScript | `frontend/src/**` | Builds the pages in the browser. | VERIFIED |
| Vite 8 | `frontend/vite.config.ts` | Dev server and bundler. Also forwards `/api/...` calls to the backend (port 8001). | VERIFIED |
| React Router 7 | `frontend/src/App.tsx` | Switches pages by URL without reloading. | VERIFIED |
| Tailwind CSS 4 | `frontend/src/index.css` + class names everywhere | Styling. Theme colours live in one `@theme` block. | VERIFIED |
| `@xyflow/react` (React Flow) | `pages/Graph.tsx`, `pages/Distribution.tsx` | Draws the node-and-edge graph; gives zoom, pan, drag and a mini-map. | VERIFIED |
| Recharts | `pages/Dashboard.tsx`, `Data.tsx`, `Models.tsx` | Bar and pie charts. | VERIFIED |
| lucide-react | `App.tsx`, `Graph.tsx`, `FsVideo.tsx` | Icons. | VERIFIED |
| Browser Fullscreen API + Keyboard Lock API | `frontend/src/fs.ts`, `CinemaPlayer.tsx`, `pages/Graph.tsx` | Optional real browser fullscreen for the graph workspace and the video overlay. Keyboard Lock lets a short Esc press reach the page (Chrome/Edge on localhost or https only). | VERIFIED (Chrome; the Keyboard Lock path itself was not separately proven) |
| HTML canvas (no library) | `frontend/src/Ambient.tsx` | The faint moving particles-and-lines background. | VERIFIED (renders; no console errors) |
| CSS animations (no animation library) | `frontend/src/index.css` | Moving grid, page transitions, scan bar, pulses, collapsible panels, animated edge. All switched off by `prefers-reduced-motion`. | VERIFIED |
| Python 3.12 + FastAPI 0.139 | `src/orvex/api/main.py`, `routes2.py` | The backend: answers API requests with JSON, images and video. | VERIFIED |
| Uvicorn | start command | Runs the FastAPI app. | VERIFIED |
| pandas 3.0 / NumPy 2.2 | `main.py` | Reads the CSV tables and does the dHash comparison arithmetic. | VERIFIED |
| SQLite (`sqlite3`) | `data/app/orvex_app.db`, `main.py` `init()` | Stores users, investigations, reviews, history, uploads, reset tokens. | VERIFIED |
| CSV files | `data/derived/tables/*.csv` | The real dataset tables (read-only for the app). | VERIFIED |
| JSON Lines files | `data/derived/features/*.jsonl` | Stored dHash and audio fingerprints. | VERIFIED |
| PyJWT + PBKDF2-SHA256 | `main.py` `pw()`, `token()`, `user()` | Password hashing (120,000 rounds, random salt) and signed login tokens (HS256, 24 h). | VERIFIED |
| FFmpeg / FFprobe 9.0.2 | `tools/ffmpeg-9.0.2-essentials_build/bin/` | Makes thumbnails (`/api/media/{id}/frame`), checks uploads, and (offline) made the edited variants and audio fingerprints. | VERIFIED |
| OpenCV (`cv2`) | `scripts/datasets/s5_features_pairs_splits.py` `feat()` | Reads video frames to compute the perceptual hashes (offline script, not in the live API). | IMPLEMENTED (script run earlier; not re-run today) |
| ReportLab + Matplotlib | `routes2.py` `report()` | Builds the PDF report and draws the graph picture inside it. | IMPLEMENTED |
| scikit-learn (`roc_auc_score`) | `scripts/datasets/s9_feature_baseline.py` | Computes the AUC of the baseline. Offline script. | IMPLEMENTED |
| pytest | `tests/test_dataset_package.py` | Dataset package checks. | VERIFIED (38 passed) |
| Playwright (Python) | `tests/browser/ui_workflow_test.py`, `data/app/ui_test.py` | Drives a real Chrome for browser tests / screenshots. | VERIFIED |
| PyTorch, DINOv2, similarity-matrix CNN, TransVCL | design document only | The planned learned model. | **NOT IMPLEMENTED** (no code, no weights; the API text calls it "specified") |
| OCR, speech recognition, embeddings | `feature_manifest.csv` rows marked `not_computed` | Planned features. | **NOT IMPLEMENTED** (Data quality page shows 0) |
| LangGraph agents, MCP server, RAG, Chroma, Ollama LLM, n8n, Neo4j, PostgreSQL | architecture diagrams in `docs/design/*.png` and the design document | Planned supporting services. | **NOT IMPLEMENTED** (searching `src/`, `scripts/`, `frontend/src/` finds none as code) |

---

## 3. Project folder structure

This repository is the published copy of the working project folder (only the demo code, small data tables and documentation; videos are in the Hugging Face dataset).

| Path | Purpose | Contents / why needed |
|---|---|---|
| `src/orvex/api/main.py` | Backend part 1 | Config, SQLite setup, login, dataset readers (cached), media/frame/stream, families, graph, compare, provenance, timeline. |
| `src/orvex/api/routes2.py` | Backend part 2 | Dashboard summary, datasets, variants, evidence, reviews, investigations, upload, distribution, quality, models, evaluation, PDF report. Imported at the end of `main.py`. |
| `frontend/` | The web app | `package.json`, `vite.config.ts`, `index.html`. |
| `frontend/src/App.tsx` | Layout and routes | Sidebar groups, top bar, route table, login state (`Shell`, `App`). |
| `frontend/src/api.ts` | Backend helper | `api()` fetch wrapper adding the token, URL builders `frame()` / `stream()`, colour table `ROLE`, edit-name table `TLABEL`. |
| `frontend/src/ui.tsx` | Shared UI | `Card`, `Badge`, `Stat`, `Note`, `useApi` hook, `useActive`/`useRoot` (remember the chosen investigation/family), `FamilyPicker`, `Thumb`. |
| `frontend/src/FsVideo.tsx` | Inline video with a fullscreen button (new) | Used for the Reference Video and Selected Video panels; the button opens `CinemaPlayer`. |
| `frontend/src/CinemaPlayer.tsx` | Full-viewport video overlay (new) | Custom controls, Esc / close handling, own keyboard handler with cleanup. |
| `frontend/src/fs.ts` | Fullscreen helpers (new) | Enter/exit fullscreen, Keyboard Lock helpers. |
| `frontend/src/nav.ts` | Sidebar structure (new) | Groups, routes and icons; also gives each page its section label. |
| `frontend/src/Ambient.tsx` | Animated background (new) | Canvas particles; pauses when the tab is hidden. |
| `tests/browser/ui_workflow_test.py` | Browser test (new) | 58 checks in real Chrome; screenshots in `tests/browser/shots/`. |
| `frontend/src/index.css` | Theme | Colours, buttons, tables, sidebar styles. |
| `frontend/src/pages/*.tsx` | One file per page area | See section 4. |
| `data/derived/tables/` | The real dataset tables | 12 CSV files (see section 12). |
| `data/derived/features/` | Stored features | `visual_dhash24.jsonl`, `audio_fingerprint.jsonl` (1,727 records each). |
| `data/derived/splits/split_manifest.csv` | Train/validation/test split by source family | Used for family counts. |
| `data/real_world/media/` | Real videos | Wikimedia Commons (`commons/`) and ANAKIN videos. |
| `data/controlled_variants/media/` | Edited versions | FFmpeg-made `.mp4` variants, e.g. `P10491224/CV-P10491224-V03.mp4`. |
| `data/app/` | Application state | `orvex_app.db` (SQLite), `thumbs/` (cached frames), `uploads/`, `.secret` (token-signing key, generated on first run; never share it). |
| `data/reports/` | Test evidence | `acceptance_checks.json`, `pytest_summary.txt`. |
| `scripts/datasets/` | Offline data pipeline | `s1`…`s9` scripts: fetch metadata, collect media, normalise, make variants (`s4_variants.py`, `transformations.py`), compute features/pairs/splits (`s5`, `s5b`), baseline evaluation (`s9_feature_baseline.py`). Not called by the web app. |
| `tests/test_dataset_package.py` | Automated tests | Dataset acceptance tests. |
| `docs/datasets/`, `docs/design/` | Documentation | Dataset catalogue, audits, architecture pictures. |
| `ORVEX_run_demo.bat` | Windows starter | Opens two windows: API on 8001, frontend on 5173 (development). |
| `Dockerfile`, `start.sh`, `requirements.txt` | Deployment | One container: builds the React app, installs FFmpeg and the Python packages, downloads the 3 large tables, starts the API and the web app. |
| `scripts/fetch_data.py` | Data download | Fetches the 3 large tables (and, with `--media`, all videos) from the Hugging Face dataset. |
| `data/media_manifest.csv` | Media list | Every published video: path, size, SHA-256, licence. |
| `.env.example` | Settings | Names of the environment variables with safe placeholders. |

---

## 4. Pages

Routes are defined in `frontend/src/App.tsx`. Every page except the four login pages sits inside `Shell`, which redirects to `/login` if there is no token in `localStorage`. All calls go through `api()` in `frontend/src/api.ts`, which sends `Authorization: Bearer <token>` to `/api/...`.

**A note on login protection.** Many read endpoints (`/api/graph`, `/api/compare`, `/api/media/...`, `/api/families`, `/api/timeline`, `/api/provenance`, `/api/transformations`) do **not** check the token in the backend (verified by reading `main.py`; only the endpoints with `Depends(user)` check it). The frontend hides them behind login; the API itself does not.

### Login, Register, Forgot, Reset — `pages/Auth.tsx` (**VERIFIED** login)
- Purpose: sign in or create an account.
- Calls: `POST /api/auth/login`, `/auth/register`, `/auth/forgot`, `/auth/reset`.
- Login stores the token (`orvex_token`) and user (`orvex_user`) in `localStorage`. Register creates a user with role `investigator` (password at least 8 characters).
- Forgot password: no e-mail server exists; the API returns the reset token on screen ("demo mode"). **PARTIAL** by design.
- Data: table `users` / `resets` in SQLite.

### Dashboard `/` — `pages/Dashboard.tsx` (**VERIFIED**)
- Command-centre layout: a top band with three panels (Case file from the active investigation; Data holdings; Processing queue) above the counters and charts. Calls `GET /api/summary` and `GET /api/quality`. The counters count up once from 0 to the real loaded value (`CountUp` in `ui.tsx`; no animation when reduced motion is requested).
- The "Processing queue" panel honestly says there are no background jobs, because the backend has no job queue.
- Every number is computed on request from the CSV tables, the media folders and SQLite (`summary()` in `routes2.py`). Exceptions hard-coded in that function: `data_gb=17.24`, `budget_gb=30`, and "2 more failed" variants (`variants_records = len(VAR()) + 2`).
- Examples today: 252,270 media records, 596 local files, 1,131 validated variants, 13,659 labelled pairs, 299,875 relationship edges, 1,237 evidence records.

### Investigations `/investigations` and `/investigations/:id` — `pages/Investigations.tsx` (**VERIFIED** by page load; create/edit **IMPLEMENTED**)
- Create an investigation: title, reference video (picked from `GET /api/media?kind=natural&source=RW-01`, or an uploaded file), summary, hypothesis. Button "create" -> `POST /api/investigations`. It becomes the *active investigation* (stored in `localStorage` as `orvex_active`, shown in the top bar).
- Upload: `POST /api/upload` (multipart). The backend only validates with FFprobe and stores the file. **No features are computed for uploads.**
- Detail page: `GET /api/investigations/{id}` returns the record plus its history and reviews; `PUT` updates status/summary/hypothesis.

### Candidate discovery `/candidates` — `pages/Candidates.tsx` (**VERIFIED** load)
- A table for the chosen source family. Calls `GET /api/graph/{root}?all=true`.
- Filters (search, relationship label, transformation) run in the browser.
- Columns: thumbnail, label, transformation, source, duration, resolution, dHash match, audio identical, evidence link. The "candidates" are **the family's known variants (ground truth) plus one sampled unrelated video**, not the result of searching a collection. Search/retrieval over a large collection is **NOT IMPLEMENTED**.

### Relationship graph `/graph` — `pages/Graph.tsx` (**VERIFIED**; see sections 5-7)

### Video comparison `/compare` — `pages/Analysis.tsx` `Compare` (**VERIFIED** load)
- Choose two videos of the family. Calls `GET /api/compare?a=..&b=..`.
- Shows both videos, a frame slider (frames from `/api/media/{id}/frame?t=`), metadata table, measured features (dHash fraction, audio MD5 identical, envelope agreement), the recorded relationship and evidence links.
- This page still uses the plain `<video controls>` element (the browser's own fullscreen control); it does **not** use `FsVideo` or the cinema overlay.
- "OCR / speech text: not extracted" is shown honestly.
- No frame-difference image is computed.

### Media provenance `/provenance` — `Provenance` in `Analysis.tsx` (**VERIFIED** load)
- Tree of root -> children with the edit applied at each step. Calls `GET /api/provenance/{root}`. Built from `controlled_variant_registry.csv` (`direct_parent_media_id`, `ancestor_chain`).

### Manipulation analysis `/manipulation` — `Manipulation` in `Analysis.tsx` (**VERIFIED** load)
- Lists the 14 edit types (T01–T14). Calls `GET /api/transformations`: counts per edit, an example original/variant pair, whether it is held out, and the baseline detection rate read from `docs/datasets/necessity_audit/dhash_baseline_results.json`.
- These are ordinary FFmpeg edits. **No deepfake/synthetic-media detection exists.**

### Distribution and campaigns `/distribution` — `pages/Distribution.tsx` (**VERIFIED** load)
- Calls `/api/distribution/top`, `/distribution/video/{id}`, `/distribution/accounts`. Reads `platform_observations.csv` (share references, YouTube channel pseudonyms).
- All rows have `coordination_status = not_assessed`; `campaign_candidate_clusters.csv` is empty (Dashboard shows 0). The page states this. **Coordination analysis is NOT IMPLEMENTED.**

### Evidence ledger `/evidence` — `pages/Evidence.tsx` (**VERIFIED** load; review button **IMPLEMENTED**)
- Search/filter the ledger: `GET /api/evidence`, one record: `GET /api/evidence/{id}`. A review decision here posts `POST /api/reviews`.
- Data: `evidence_ledger.csv` (1,133 controlled-transformation-log records, 96 licence records, 6 source annotations, 1 source metadata, 1 machine measurement).

### Dataset explorer `/datasets` — `Datasets` in `pages/Data.tsx` (**VERIFIED** load)
- `GET /api/datasets` (from `data/manifests/source_registry.csv` plus counts) and `GET /api/datasets/{id}/records`.

### Variants and labels `/variants` — `Variants` in `Data.tsx` (**VERIFIED** load)
- `GET /api/variants` with filters, `GET /api/variants/{id}` (ancestor chain, run log, edge records, label provenance text).

### Data quality `/quality` — `Quality` in `Data.tsx` (**VERIFIED** load)
- `GET /api/quality`: acceptance checks from `data/reports/acceptance_checks.json`, missing-file counts (it really checks the disk), dangling edges, duplicates, feature coverage (dHash 1,727; OCR, ASR, embeddings 0). The "pytest" line is read from `data/reports/pytest_summary.txt`, i.e. a stored text file, not a live test run.

### Model lab `/models` and Evaluation `/evaluation` — `pages/Models.tsx` (**VERIFIED** load)
- `GET /api/models` and `GET /api/evaluation`. Show the non-learned dHash baseline, its rule and its measured numbers, and the *specified* (not built) DINOv2 + CNN model. The text on the page says there is no trained model.

### Investigation report `/report` — `pages/Report.tsx` (**IMPLEMENTED**; PDF generated in an earlier session, not retested today)
- Choose an investigation, click download -> `GET /api/report/{id}?token=...` returns a PDF built with ReportLab (reference, candidates, graph picture, comparison table, evidence, observations, reviews, limitations).
- The token is passed in the URL query because the download is opened as a file. The PDF's graph picture uses its own simple circle layout (Matplotlib), not the on-screen layout.

### Profile and roles `/admin` — `pages/Admin.tsx` (**VERIFIED** load)
- `GET /api/auth/users`: admins see all users, others see only themselves. There is no UI to change roles.

---

## 5. Reference video — implementation

Code: `frontend/src/pages/Graph.tsx` (left panel), `frontend/src/FsVideo.tsx`, `frontend/src/CinemaPlayer.tsx`, backend `stream()` in `main.py`.

- **Selection.** `useRoot()` (`ui.tsx`) returns the chosen family root, kept in `localStorage` (`orvex_active.root`), default `RW-CMN-P10491224`. The "Source family" dropdown (`FamilyPicker`) lists families from `GET /api/families`.
- **Where the file comes from.** `media()` in `main.py` finds the row in `real_world_media_master.csv`; its `local_path` is e.g. `data/real_world/media/commons/RW-CMN-P10491224.ogv`.
- **Loading and playback.** `<FsVideo src="/api/media/{id}/stream" poster="/api/media/{id}/frame?t=1&w=480">` shows a normal `<video controls>` (native play, seek, volume, time). The `stream` route returns the file with `FileResponse`, which supports byte ranges, so seeking works.
- **Fullscreen.** The button at the top-right of the video opens `CinemaPlayer` (an overlay that covers the whole browser window, see below) starting at the time where the inline video was, and pauses the inline video. The overlay shows the video with `object-fit: contain`, so the picture is never stretched.
- **Exit.** Esc, the X button, or leaving the page. `CinemaPlayer` registers one `keydown` listener on `window` (capture phase) and removes it when it closes.
- **Errors.** If the file is missing the backend returns 404; the overlay shows "This video file could not be loaded." The inline player has no custom message. **PARTIAL.**
- **Independence.** Each `FsVideo` owns its own `open` state, so the Reference and Selected players cannot open each other (tested).

### The CinemaPlayer overlay (`frontend/src/CinemaPlayer.tsx`)
- A React portal on `document.body` (`position: fixed; inset: 0; z-index: 200`), dark "cinema" background, title bar with the video id and title, a close button.
- Own controls: play/pause, seek bar, current time / total time, mute, volume. Keys: **Esc** close, **Space** or **k** play/pause, **Left/Right** seek 5 s, **m** mute.
- It is an in-page overlay, not the browser's fullscreen of the `<video>` element. That is deliberate: whatever is underneath (for example the expanded graph) stays mounted and unchanged.
- If the browser supports Keyboard Lock (Chrome/Edge on a secure context such as `localhost`) and nothing is already fullscreen, it also asks for real browser fullscreen and locks Esc so that one short press reaches the page. It leaves fullscreen when it closes.
- **VERIFIED** in Chrome: opens at 1600x900 filling the window, `object-fit: contain`, Esc closes, close button closes, play/pause, seek and mute work.

---

## 6. Selected video details — implementation

Code: right panel and the workspace drawer in `pages/Graph.tsx` (`detailHead()`, `detailBody()`).

- **How a node becomes selected.** State `sel` (a media id). It changes when you click a node, click an edge (selects its target), click an item in the "Related Videos" list, or click a timeline marker.
- **Data.** No extra API call: `s = byId[sel]` is the node object already inside the `/api/graph/{root}` response (built by `media()` in `main.py`). The edge pointing to it is `edgeOf(sel)`.
- **Player.** A second `<FsVideo key={s.id} label="Selected Video" ...>`. The `key` makes React create a fresh player when the selection changes.
- **Metadata table.** Source, duration, resolution, file size, transformation (name and family), created/published date, licence, split — from `controlled_variant_registry.csv` (variants) or `real_world_media_master.csv` (originals).
- **Expandable sections** (`Collapsible` in `ui.tsx`, smooth height animation): *Measured features vs parent* (dHash matched frames, audio envelope agreement, audio MD5 identical; labelled "not a model score"), *Recorded changes* (logged operation and its parameters, e.g. `{"start_s": 4.07, "end_s": 20.35, "kept_fraction": 0.6}` for `CV-P10491224-V03`), *Evidence record* (edge record id, label source, links to `/evidence?id=...`), *Frame comparison* (parent and child frames), *Forensic review of this edge* (note + accepted / uncertain / rejected -> `POST /api/reviews`).
- **Inside the graph workspace** the same content is shown in a right-hand drawer (`data-graph-drawer`) with a large poster and a **Play fullscreen** button (`data-open-video`) that opens `CinemaPlayer` for that video.

---

## 7. Relationship graph — implementation

Code: `frontend/src/pages/Graph.tsx`; backend `graph()` in `main.py`.

**Library:** React Flow (`@xyflow/react`). Custom node type `VideoNode`, custom edge type `RelEdge`.

**Data retrieval.** `useApi('/graph/' + root, { all: showAll })`. Default view shows up to 9 variants (distinct direct edits plus up to 3 deepest, with their ancestors so every edge has a visible parent); the checkbox "Show all 21 variants" asks for all. The timeline comes from `GET /api/timeline/{root}`.

**Nodes.** One per video in the response. Fields include id, title, duration, size, `role` (`reference`, `direct`, `indirect`, `unrelated`), transformation and parent.

**Thumbnails.** `<img src="/api/media/{id}/frame?t=1&w=300">`. The backend runs `ffmpeg -ss 1 -i file -frames:v 1 -vf scale=300:-2` on first request and caches the JPEG in `data/app/thumbs/`.

**Edges.** One per record: `parent > child` for each variant (directed, arrow, solid) and, for the sampled negative pair, `video ~ unrelated` (not directed, dashed). The edge label is the logged transformation name (e.g. `trim_middle`) or "no relation".

**Look.** The graph panel is a dark canvas (`.gpanel`) so thumbnails stand out; labels and legend are light on dark. **Colours.** `ROLE` in `api.ts`: blue = reference, red = direct derivative (depth 1), orange = indirect (depth >= 2), grey = unrelated, purple = "same incident". Purple is defined and in the legend but **never appears**: the "same incident" relations (FIVR) exist only as metadata with no local video, so no purple node can be built (the API note says so).

**Layout algorithm** (`layout()`, rewritten in this session): a *radial tree*.
1. Walk the directed edges from the reference to get each node's depth and the number of leaves below it.
2. Each depth gets a ring; the ring radius is the larger of "previous ring + 235 px" and "enough circumference for all nodes on that ring" (so neighbours cannot touch).
3. The 360 degrees around the reference are split into wedges proportional to each child's number of leaves; a child sits at the middle of its wedge, its own children inside that wedge on the next ring. The unrelated node gets its own wedge because it is attached to the family by an edge.
4. Positions are squeezed vertically (x 1.5, y 0.74) to suit wide screens. The test counted node boxes that overlap: 0 with 12 nodes and 0 with all 23.

**Edge drawing.** `RelEdge` computes the line between node centres, shortens it so it stops at the thumbnail border (and the arrowhead is visible), and puts the label in a white box on the middle of the line.

**Zoom and pan.** Provided by React Flow (mouse wheel, drag the background; drag a node to move it). The toolbar buttons call `zoomIn`, `zoomOut`, `fitView` (Fit to screen) and "Reset view" (recompute the layout, select the reference again, fit). A mini-map is shown.

**Selection.** Click a node or edge -> `sel` changes (section 6). The selected node gets a glow, a short pulse (`node-pulse`) and a coloured name label; its edge flows (`edge-flow`). If the selected node is not the reference, nodes and edges not connected to it are dimmed (opacity 0.5 / 0.4). The view is not re-centred on selection, so your zoom and pan are preserved.

**Timeline.** The strip under the graph lists events from `/api/timeline/{root}`: original publication, platform observation, dataset collection (these three from the original's record) and one "variant creation" per variant (its `created_utc`). Clicking a marker calls `setSel(...)`, so it selects the same video as a node click. Filter chips hide event types. Dates from different fields are kept apart on purpose.

**Graph workspace (fullscreen)** (`ws` state in `Graph.tsx`).
- The toolbar button (top-right of the graph: Zoom in, Zoom out, Fit to screen, Reset view, Fullscreen) switches the **same graph card** to a fixed, viewport-filling layout using CSS only (`.gpanel.ws` in `index.css`). Because the React Flow instance is never unmounted, nodes, node positions, zoom, pan, selection and loaded data are kept. The graph data is not fetched again (the browser test counts the `/api/graph/` requests and they do not increase).
- If the browser supports Keyboard Lock, it also asks for real browser fullscreen (`enterFs(document.documentElement)`); otherwise the workspace simply fills the browser window. The two are separate: leaving browser fullscreen does not close the workspace.
- The workspace shows: title and counts, the relationship legend, a larger mini-map, the zoom/fit/reset toolbar, the **timeline** along the bottom, and the **selected-video drawer** on the right.
- A `ResizeObserver` on the card calls `fitView` (debounced 120 ms) whenever the size changes (entering the workspace, resizing the window); it is disconnected on cleanup.

**Graph + video workflow (the key interaction).**
1. Enter the workspace.
2. Click a node: it is highlighted (glow + pulse), its edge is animated (`edge-flow`), unconnected nodes are dimmed, the drawer updates.
3. Click **Play fullscreen** in the drawer: `CinemaPlayer` opens over the workspace (it is a separate portal; the graph is untouched below it).
4. Press **Esc**: `CinemaPlayer`'s own capture-phase listener closes only the video and stops the event. The workspace's Esc handler also checks a ref (`videoRef`) and does nothing while a video is open. So you return to exactly the same graph.
5. Press **Esc** again (no video open): the workspace closes and the normal page is back.
Cleanup: both listeners are removed when they are no longer needed; if the page is left while the workspace is open, browser fullscreen is exited.
Honest limits: in browsers without Keyboard Lock (Firefox, Safari, or an insecure `http://<LAN-IP>` address) the workspace does not request browser fullscreen, so Esc still reaches the page and the workflow is the same. If a user holds Esc in Chrome fullscreen, the browser leaves fullscreen itself (the workspace stays open).

**Worked example (real).** Family `RW-CMN-P10491224` = Wikimedia Commons file `File:Ashs-learning-common.ogv` (27 s, 720x576, CC BY-SA 3.0).
- Centre (blue): `RW-CMN-P10491224`, the original.
- Red nodes around it: its direct edits, e.g. `CV-P10491224-V03` "Trimmed (middle)" (`{"start_s": 4.07, "end_s": 20.35}`, 16 s), `V05` trimmed tail, `V06` cropped, `V01` re-encoded.
- Orange node: `V15` "Caption added" is a child of `V03` (depth 2); `V16` is a re-compression of `V15` (depth 3). So a chain `V03 -> V15 -> V16` appears.
- Grey dashed: one sampled unrelated video.

**Where each relationship comes from (do not mix):**

| Edge type | Source |
|---|---|
| Parent -> child (red/orange) | **Ground truth**: `controlled_variant_registry.csv` (`direct_parent_media_id`), i.e. the log of the FFmpeg edit that produced the file. Edge label source is shown as `controlled_transformation_log`. Cross-referenced with `media_relationship_edges.csv` (scope `controlled_lineage`). |
| Grey dashed | **Dataset label**: a negative pair from `training_pairs.csv` made by a sampling rule (`negative_sampling_rule`): two videos from different sources. |
| dHash / audio numbers on edges | **Algorithm measurement** (non-learned), shown next to the edge, not used to create it. |
| Trained model prediction | **None.** No model exists. |
| Purple "same incident" | Not drawn (no local data). |

---

## 8. Video processing pipeline (what really happens)

There are **two separate pipelines**. Only the first is part of the running demo.

### A. Live (demo) — when a user uploads a video (`POST /api/upload`, `routes2.py` `upload()`)

| Stage | What happens | Tool / code | Output |
|---|---|---|---|
| 1 Receive | The file is saved as `data/app/uploads/UP-xxxxxxxx.<ext>` | FastAPI `UploadFile` | file on disk |
| 2 Validate | `ffprobe -print_format json -show_format -show_streams` | FFprobe | If no video stream: file deleted, HTTP 400 "not a readable video file" |
| 3 Metadata | duration, width, height, bytes, has_audio | JSON parsing | stored in SQLite `uploads.meta` |
| 4 Return | media record with `/frame` and `/stream` URLs | `media_get()` | JSON |

**Nothing else happens.** No hashing, fingerprinting, candidate search or analysis runs on uploads (the Investigations page says so). Frames for thumbnails are made on demand by FFmpeg (`frame()` in `main.py`).

### B. Offline — how the dataset and its features were made (scripts, run earlier)

| Stage | Script | What it does | Output |
|---|---|---|---|
| Fetch metadata | `scripts/datasets/s1_fetch_metadata.py` | Collects records of source datasets | tables |
| Collect media | `s2_collect_media.py`, `s3_normalize.py` | Downloads licence-permitted videos, normalises records | `data/real_world/media/...` |
| Make variants | `s4_variants.py`, `transformations.py` | FFmpeg applies 14 edit types (T01–T14) with logged parameters | `data/controlled_variants/media/...`, `controlled_variant_registry.csv` |
| Features | `s5_features_pairs_splits.py` `feat()` and `s5b_feature_hashes.py` | OpenCV reads 24 evenly spaced frames, shrinks each to 9x8 grey, builds a 64-bit "difference hash" (dHash); FFmpeg decodes audio to 8 kHz mono, then MD5 of the audio and a 1-second loudness envelope | `visual_dhash24.jsonl`, `audio_fingerprint.jsonl`, `feature_manifest.csv` |
| Pairs and splits | same script | Builds labelled pairs and train/val/test splits by source family; T11-T14 edits are held out for test | `training_pairs.csv`, `split_manifest.csv` |
| Baseline | `s9_feature_baseline.py` | Scores pairs with dHash matching and reports AUC | `dhash_baseline_results.json`, `experiment_registry.csv` |

Feature files hold 1,727 records. Embeddings, OCR, ASR, text embeddings and scene boundaries are listed in `feature_manifest.csv` as `not_computed`.

---

## 9. Relationship analysis and model implementation

| Method | Implemented? | Algorithm / file | Input -> output |
|---|---|---|---|
| **Perceptual hashing (dHash)** | **Yes** (features precomputed offline; comparison in the live API) | `feat()` in `s5_...py` makes hashes. `frac()`/`sims()` in `main.py` compare: for each of 24 frames of A, is there a frame of B within 8 of 64 bits; fraction of matches both ways, take the larger. Rule copied from `s9_feature_baseline.py`. | two media ids -> `dhash_match_fraction` between 0 and 1 |
| **Audio fingerprint** | **Yes** | MD5 of 8 kHz audio plus 1-second envelope (`audio_fingerprint.jsonl`). `sims()` returns `audio_md5_identical` (true/false) and `audio_envelope_agreement` (share of equal envelope seconds; needs at least 5 seconds) | two ids -> booleans/fractions |
| **Visual feature extraction beyond dHash** | **No** | — | — |
| **Embeddings (DINOv2 etc.)** | **NOT IMPLEMENTED** | Only specified in `ORVEX_Requirements_and_System_Design.docx` | — |
| **Similarity calculation** | **Yes (rule only)** | The two above. Threshold 0.45 is used only in the baseline *evaluation* script and `/api/models`; the graph does not use a threshold. | — |
| **Relationship classification (7 classes)** | **Labels only, not predicted** | Classes exist as labels in `training_pairs.csv` (same_family_other 5,827; sibling_same_parent 4,759; unrelated_distinct_source 1,142; direct_derivation 1,131; indirect_derivation 495; edited_version 250; audio_source_only 55). They come from the logs and sampling rules, not from a classifier. | — |
| **Direction (which is the parent)** | **Labels only** | `direct_parent_media_id`, `ancestor_chain` in the variant registry give direction by construction. No model predicts it. | — |
| **Evidence validation** | **Records only** | `evidence_ledger.csv` stores evidence with a claim, a status and "observed fact vs inference". The API links ids to edges; nothing validates new evidence automatically. | — |
| **Confidence scores** | **No model confidence.** | The numbers shown are the dHash/audio measurements, labelled "not a model score". Calibration is only specified. | — |
| **Actual trained model** | **None** | — | — |
| **Algorithmic baseline** | **Yes** | `dhash24-frame-match v1`, threshold 0.45 fixed in advance. Measured in `docs/datasets/necessity_audit/dhash_baseline_results.json` (9,928 pairs): AUC train 0.8734, validation 0.8992, test 0.8307. `/api/evaluation` reads this file. | — |
| **Configured but unused** | `feature_manifest.csv` rows for OCR/ASR/embeddings (`not_computed`). | — | — |
| **Planned** | DINOv2 + similarity-matrix CNN (1,310,547 parameters in the design), temperature calibration, TransVCL for segment localisation, agents/RAG/LLM. | design document | — |
| **LLM assistance** | **None** in the app. | — | — |

**Does the current graph use ground truth or predictions?** Ground truth. The edges are the controlled transformation log. Nothing is predicted by a model, and the page says so ("not a model prediction"). The API (`graph()`) sets `label_source = "controlled_transformation_log"` for derivation edges.

A consequence you should know: because edges come from the log, the graph shows what was *made*, not what a system *found*. A demonstration of real detection on unlabelled videos would need the learned model and a retrieval step, which do not exist yet.

---

## 10. Backend and API communication

- The browser calls relative URLs `/api/...`. In development, Vite forwards them to `http://127.0.0.1:8001` (`frontend/vite.config.ts`). CORS is open (`allow_origins=["*"]`).
- `api()` in `frontend/src/api.ts` adds the token. A 401 (except on auth routes) clears the token and sends the user to `/login`. Other errors become `Error(detail)` and pages show "Could not load: ..." (`Loading` in `ui.tsx`).
- Auth: `user()` in `main.py` decodes the JWT (HS256, 24 h) with the key in `data/app/.secret`. Endpoints with `Depends(user)` need it.
- Uploads: `POST /api/upload`. Retrieval: `GET /api/media/{id}/stream` (video) and `/frame` (JPEG).

| Method and route | Auth | What it does |
|---|---|---|
| `POST /api/auth/login` | no | Check password; return token and user |
| `POST /api/auth/register` | no | Create investigator account; log in |
| `POST /api/auth/forgot`, `/auth/reset` | no | Demo reset (token returned on screen) |
| `GET /api/auth/users` | yes | Users (all for admin) |
| `GET /api/summary` | yes | Dashboard numbers |
| `GET /api/families` | no | Source families that have variants |
| `GET /api/graph/{root}?all=` | no | Nodes and edges for a family (ground truth + measurements) |
| `GET /api/timeline/{root}` | no | Events for the timeline |
| `GET /api/compare?a=&b=` | no | Metadata, measurements, recorded relationship, evidence refs |
| `GET /api/provenance/{id}` | no | Lineage tree data |
| `GET /api/transformations` | no | 14 edit types with counts and baseline rates |
| `GET /api/media`, `/media/{id}`, `/media/{id}/frame`, `/media/{id}/stream` | no | List, details, thumbnail, video |
| `POST /api/upload` | yes | Store and FFprobe-check a video |
| `GET /api/datasets`, `/datasets/{id}/records` | yes | Dataset registry and records |
| `GET /api/variants`, `/variants/{id}` | yes | Variant registry and one variant |
| `GET /api/evidence`, `/evidence/{id}` | yes | Evidence ledger |
| `POST /api/reviews`, `GET /api/reviews` | yes | Save / list review decisions |
| `GET/POST /api/investigations`, `GET/PUT /api/investigations/{id}` | yes | Investigation records |
| `GET /api/distribution/top`, `/video/{id}`, `/accounts` | yes | Platform observation views |
| `GET /api/quality`, `/models`, `/evaluation` | yes | Checks, model description, baseline results |
| `GET /api/report/{id}?token=` | token in query | PDF report |

Security notes: the seeded demo accounts are created when the user table is empty (see `init()` in `main.py`; the demo password is documented there and in the login screen, not repeated here). Passwords are stored salted and hashed. The unauthenticated read routes are a limitation for any non-demo use.

---

## 11. Database and data storage

**Application database: SQLite**, file `data/app/orvex_app.db`, created in `init()` (`main.py`).

| Table | Holds |
|---|---|
| `users` | email, name, role (`admin`, `reviewer`, `investigator`), salted PBKDF2 password hash |
| `resets` | password-reset tokens with expiry |
| `investigations` | title, `reference_id`, status, owner, summary, hypothesis |
| `history` | activity log lines per investigation (created, updated, review decisions) |
| `reviews` | per-edge decision (`accepted/rejected/uncertain/note`), note, `evidence_ids`, actor, time |
| `uploads` | uploaded file id (`UP-...`), name, path, metadata JSON, owner |

Relations: `investigations.id` is referenced by `history.inv_id` and `reviews.inv_id`; `reviews.edge_key` is the graph edge id (`parent>child`); `investigations.reference_id` and `reviews.evidence_ids` point into the CSV data by id (no SQL foreign keys).

**Dataset: CSV and JSONL files, read-only** (no dataset database). Loaded with pandas once and cached with `lru_cache` (`M()`, `LOCAL()`, `VAR()`, `EDGES()`, `LEDGER()`, `PAIRS()`, `OBS()`, `HASH()`, `AUD()`), warmed in a background thread at startup (`_warm()` in `routes2.py`).

| What | Where |
|---|---|
| Original videos | files under `data/real_world/media/`, listed in `real_world_media_master.csv` (`local_path`) |
| Variants | files under `data/controlled_variants/media/`, listed in `controlled_variant_registry.csv` |
| Relationship records | `media_relationship_edges.csv` (299,875 rows: 298,645 `real_native` source annotations and 1,230 `controlled_lineage`) |
| Labelled pairs | `training_pairs.csv` |
| Evidence | `evidence_ledger.csv` |
| Features | `data/derived/features/*.jsonl`; catalogue in `feature_manifest.csv` |
| Thumbnails | cached in `data/app/thumbs/` |

**Not used:** PostgreSQL, Neo4j and a Chroma vector index appear in the design diagrams only.

---

## 12. Dataset implementation

Connected to the app (from `real_world_media_master.csv` and the dashboard): 252,270 records from 8 source datasets, but **only 596 videos exist locally**: 96 from Wikimedia Commons (`RW-01`) and 500 from ANAKIN (`RW-02`). FIVR, VCSL, FVC and COVID are metadata only (no local video files). Plus 1,131 validated controlled variants (1,133 in the registry, 2 failed validation) made from the Commons videos.

- **IDs:** originals look like `RW-CMN-P10491224`; variants like `CV-P10491224-V03` (`CV-` + family number + `-V` + sequence). `main.py` checks variant ids first, then originals, then uploads, then metadata-only records (`media()`).
- **Variant -> original link:** `root_source_media_id` and `direct_parent_media_id` columns; deeper chains in `ancestor_chain`, split by `|`.
- **Where relationship labels come from:** the edit log (variants), sampling rules (negatives), source annotations (the 298,645 native edges; mostly metadata-only).
- **Real example shown in the app:** `RW-CMN-P10491224` and its 21 variants (see section 7), including a real record: `CV-P10491224-V03`, `trim_middle`, parameters `{"start_s": 4.07, "end_s": 20.35, "kept_fraction": 0.6}`, file `data/controlled_variants/media/P10491224/CV-P10491224-V03.mp4`.
- **Splits:** 305 source families split into train/validation/test (`split_manifest.csv`); 9,928 of 13,659 labelled pairs are usable.
- Licences and attribution are in `docs/datasets/ORVEX_ATTRIBUTION.md` and shown in the Selected Video panel.

---

## 13. UI design and investigation theme

Implemented in `frontend/src/index.css` (tokens, animations), `frontend/src/App.tsx` (`Shell`, `Notifications`), `frontend/src/nav.ts`, `frontend/src/Ambient.tsx`, `frontend/src/ui.tsx` and `pages/Graph.tsx`. It is visual inspiration only: no official logo, seal or branding, and the sidebar footer says ORVEX is an independent tool, not an official or government system.

**Design system.**
- *Dark investigation workspace + light evidence panels.* The area behind the pages (`.workspace`) is midnight navy with a faint grid that moves slowly (CSS, 60 s loop) and soft amber/steel glows. Content sits on white "evidence" cards (`.card`) so tables and charts stay readable. Text that sits directly on the dark background is light; text inside cards is dark (CSS rules in `index.css`).
- *Palette:* midnight navy `#0A1424`/`#14233B`, charcoal `#1B2230`, graphite, steel blue `#4A6A96`, amber `#D98324` for highlights and the active item, evidence red `#D64545` (notification count), verified green `#2FA36B` (session dot). Relationship colours are unchanged.
- *Labels:* small spaced capitals ("CASE FILE", "REFERENCE MEDIA", "RELATIONSHIP ANALYSIS", section eyebrows above page titles). Existing technical field names were not renamed.

**Sidebar** (`nav.ts`): COMMAND CENTRE (Dashboard, Investigations), MEDIA INVESTIGATION (Candidate discovery, Relationship graph, Video comparison, Media provenance), FORENSIC ANALYSIS (Manipulation analysis, Distribution and campaigns), EVIDENCE MANAGEMENT (Evidence ledger), DATA INTELLIGENCE (Dataset explorer, Variants and labels, Data quality), MODELS AND EVALUATION (Model lab, Evaluation), plus Reports and Administration which already existed. Routes and page names are unchanged. Each group header is a button that collapses or expands its links with a smooth height animation (state kept in `localStorage`). The active page has an amber marker and glow; hover slides the link slightly.

**Top bar:** section name, CASE FILE (active investigation title or "none active · demo family ..."), INVESTIGATION ID (only when a case is active), REFERENCE MEDIA, a "Session active" dot, the **notification bell** (see below), user chip and sign-out. A thin amber line under it slowly moves.

**Animation system** (all CSS except the canvas and the counters; every one is disabled by `prefers-reduced-motion`, and the test checks that):
| Effect | Where | Condition |
|---|---|---|
| Moving grid, soft glows | `.workspace` | always (decorative) |
| Particles and faint connection lines | `Ambient.tsx` canvas | always; pauses when the tab is hidden; one still frame under reduced motion |
| Scanning sweep on the logo block, moving header line | `.side-brand`, `.topbar` | always (decorative) |
| Page transition and card entrance | `.page-enter` around the `Outlet` | each time the route changes (about 0.3 s) |
| Scan bar "Retrieving real records…" | `Loading` in `ui.tsx` | **only while a request is actually running** |
| Counters counting up | `Stat` -> `CountUp` | once, when the real value has loaded |
| Hover lift / border highlight | `.card`, `.card.lift` | on hover |
| Sidebar and `Collapsible` expand/collapse | `.side-body`, `.collapse-body` | on click |
| Node pulse, animated selected edge, drawer slide-in | graph | when a node is selected / workspace opens |
No fake scanning or analysis is shown anywhere. The Dashboard "Processing queue" panel states that there are no background jobs.

**Notifications** (`Notifications` in `App.tsx`): the bell lists the latest rows of the application `history` table from `GET /api/summary` (review decisions, investigations created or updated). The red number counts entries newer than the last time the panel was opened (`localStorage` key `orvex_seen`). With no activity it says so. There are no processing-completion or error notifications because no such events exist in the application.

**Responsive behaviour:** Tailwind grid classes; the graph page was tested at 1600x900 and 1280x720 (no page-level horizontal overflow; the page scrolls vertically at 720 px height). Narrow/mobile widths were **not** tested.

**Accessibility:** buttons have `aria-label`s, the video overlay is a `role="dialog"`, visible focus outlines, collapsible headers expose `aria-expanded`, reduced motion supported. A full accessibility audit (screen reader, contrast measurement) was **not** done.

---

## 14. Testing and verification

Results below were obtained on 15 November 2026.

| Test | Result |
|---|---|
| `python -m pytest -q tests/test_dataset_package.py` (system Python 3.12) | **38 passed.** Backend API routes still have **no automated tests**. |
| `npx tsc -b` (type check) | **Passed**, no errors. |
| `npm run build` | **Passed.** |
| `npx oxlint` | **No errors**; 21 warnings (React hook / fast-refresh style rules). |
| Browser test `tests/browser/ui_workflow_test.py` (real Chrome via Playwright, 1600x900, real backend and data) | **58 / 58 passed.** Covers: command band; counter shows real value (252,270); sidebar groups, collapse and expand; page-transition class; notification panel opens and closes on Esc; Reference Video overlay opens (fills 1600x900, `object-fit: contain`), Esc and close button close it; Selected Video overlay opens independently; graph workspace opens and fills the viewport; legend, timeline and drawer visible; zoom/fit/reset buttons present; zoom and pan change the view; node click updates the drawer and highlights the relationship; **overlay opens over the expanded graph, play/pause, seek (real mouse click on the seek bar) and mute work, Esc closes only the video, and zoom, pan, every node position, selection and node count are identical before and after; the graph is not fetched again** (done for two different nodes); second Esc closes the workspace; no overlapping nodes; all 15 pages load with exactly one active sidebar item; no horizontal overflow at 1280 px; reduced motion switches the page animation off; no console errors. |
| Frontend unit tests | **Not run: none exist.** |
| Pressing Esc by hand | Playwright sends Esc to the page, which proves the page's handlers. A physical Esc in browser fullscreen depends on Keyboard Lock and was **not** tried by hand. |
| Browsers other than Chrome; phone widths; screen-reader audit | **Not tested.** |
| PDF report download, file upload | **Not re-run** after the redesign. |

The browser test needs the app running; see section 15.

---

## 15. How to run the project

See **section 18 (Deployment and running)** below, which replaces the old laptop-only instructions.

---

## 16. End-to-end workflow (as implemented)

```
Login (JWT) 
  -> Dashboard (real counts)
  -> Investigations: create, pick a Commons reference video (or upload a file)   [becomes "active"]
  -> Candidate discovery: table of the family's known variants + 1 unrelated video
  -> Relationship graph: inspect nodes/edges, play reference and selected video,
        full-screen video or graph, read measurements and evidence ids,
        record accepted / uncertain / rejected for an edge (saved in SQLite)
  -> Video comparison / Provenance / Manipulation / Evidence ledger / Distribution (supporting views)
  -> Investigation report (PDF download)
```
Steps that do **not** exist: automatic search for candidates in a large collection, feature extraction for new videos, model-based relationship prediction, campaign/coordination analysis, e-mail, notifications.

---

## 17. Implementation summary

| Feature | What it does | Main files | Actual implementation | Status |
|---|---|---|---|---|
| Login / accounts | Sign in, register, demo reset | `Auth.tsx`; `main.py` auth routes | PBKDF2 hashes, JWT 24 h, SQLite `users` | VERIFIED (login) |
| Dashboard | Counters and charts | `Dashboard.tsx`; `routes2.py summary()` | Computed from CSVs/SQLite; 3 constants hard-coded (17.24 GB, 30 GB, "2 failed") | VERIFIED |
| Investigations | Create/edit cases, upload | `Investigations.tsx`; `routes2.py` | SQLite tables; upload = FFprobe check only | IMPLEMENTED |
| Candidate discovery | Table of family members | `Candidates.tsx`; `graph()` | Reads known variants; no retrieval | PARTIAL |
| Relationship graph | Interactive graph | `Graph.tsx`; `graph()` | React Flow, radial layout, ground-truth edges | VERIFIED |
| Reference video player | Play and fullscreen | `FsVideo.tsx`, `CinemaPlayer.tsx`; `stream()` | Native inline controls; button opens the cinema overlay | VERIFIED |
| Selected video details | Metadata, measurements, review | `Graph.tsx` | Data from graph response; second `FsVideo` | VERIFIED |
| Graph workspace (fullscreen) | Big graph with legend, timeline, drawer, tools | `Graph.tsx`, `index.css`, `fs.ts` | Same graph card switched to a fixed full-viewport layout; `ResizeObserver` refit | VERIFIED |
| Video inside the expanded graph | Play the selected video over the graph; Esc returns to the same graph | `Graph.tsx`, `CinemaPlayer.tsx` | In-page overlay portal, own Esc handling, graph never unmounted | VERIFIED (Chrome) |
| Animated investigation UI | Background, transitions, counters, scan bar, collapsibles | `index.css`, `Ambient.tsx`, `ui.tsx`, `App.tsx` | CSS + one canvas; reduced-motion aware | VERIFIED |
| Notifications | Recent activity list | `App.tsx` `Notifications`; `/api/summary` | Real `history` rows | IMPLEMENTED (opens/closes tested; unread count not tested) |
| Timeline | Events linked to selection | `Graph.tsx`; `timeline()` | From media master, observations, variant creation dates | IMPLEMENTED |
| Video comparison | Side-by-side and measurements | `Analysis.tsx`; `compare()` | dHash/audio numbers; no frame-difference image; plain `<video controls>` (not the overlay player) | PARTIAL |
| Provenance | Lineage tree | `Analysis.tsx`; `provenance()` | From variant registry | IMPLEMENTED |
| Manipulation analysis | 14 edit types with examples | `Analysis.tsx`; `transformations()` | Registry counts and baseline rates; not forgery detection | IMPLEMENTED |
| Distribution | Observations by platform | `Distribution.tsx`; `routes2.py` | Reads observations; coordination not assessed | PARTIAL |
| Evidence ledger | Browse and review evidence | `Evidence.tsx`; `routes2.py` | Reads `evidence_ledger.csv` | IMPLEMENTED |
| Dataset / variants / quality | Explore data and checks | `Data.tsx`; `routes2.py` | Reads registries and checks the disk | IMPLEMENTED |
| Model lab / evaluation | Show baseline and specification | `Models.tsx`; `models()`, `evaluation()` | dHash baseline numbers; specified model text | IMPLEMENTED (no trained model) |
| PDF report | Investigation report | `Report.tsx`; `report()` | ReportLab + Matplotlib | IMPLEMENTED (not retested) |
| dHash comparison | Visual similarity | `s5_...py feat()`; `main.py sims()` | 24 frames, 64-bit hash, Hamming <= 8 | VERIFIED (via graph numbers) |
| Audio fingerprint | Audio similarity | `s5_...py feat()`; `sims()` | 8 kHz MD5 and 1 s envelope | IMPLEMENTED |
| Embeddings, OCR, ASR | — | — | not computed | NOT IMPLEMENTED |
| Trained relationship model | — | design document only | not built | NOT IMPLEMENTED |
| Agents, MCP, RAG, LLM, n8n, Neo4j, PostgreSQL, Chroma | — | diagrams only | no code | NOT IMPLEMENTED |
| Investigation theme | Dark workspace, evidence panels, grouped sidebar, case-file top bar | `index.css`, `App.tsx`, `nav.ts` | CSS tokens and shared classes | VERIFIED (all pages load; look reviewed on screenshots) |

---

## 18. Deployment and running

### A. Run locally (Windows, macOS or Linux)
Needs: Python 3.12, Node.js 22 or newer, FFmpeg on PATH (or set `ORVEX_FFMPEG`).
```
git clone <this repository>
cd ORVEX-Prototype
pip install -r requirements.txt
cp .env.example .env            # then edit; export the variables, e.g. ORVEX_MEDIA_BASE=...
python scripts/fetch_data.py    # downloads the 3 large tables (~410 MB). Add --media for all videos (~16.6 GB, only for a fully offline run)
cd frontend && npm ci && npm run build && cd ..
python -m uvicorn main:app --app-dir src/orvex/api --port 8000
# open http://localhost:8000   (the API serves the built web app too)
```
Without `--media`, set `ORVEX_MEDIA_BASE` to the dataset address and the videos stream from there. For development with hot reload: run the API as above on port 8001 and `cd frontend && npm run dev` (Vite proxies `/api` to 8001).

Demo sign-in (public demo accounts, created automatically, no real data): `demo.investigator@orvex.local` and `demo.reviewer@orvex.local`, password `OrvexDemo!2026`. This is a shared demo password, not a secret; change it before any real use.

### B. Deploy (what was done)
- Code: GitHub repository (this one).
- Media and large tables: Hugging Face Dataset `ORVEX-Prototype-Media` (git + Git LFS upload).
- App: Hugging Face Space (SDK: Docker) built from this repository's `Dockerfile`. Space variables: `ORVEX_MEDIA_BASE` (the dataset's `resolve/main` address); Space secret: `ORVEX_SECRET`.

### C. Tests
- `python -m pytest -q tests/test_dataset_package.py`: dataset acceptance tests. Four of them (`K06_hashes`, `K18_native_files_intact`, `K30_manifests_present`, `K33_layer_a_read_only`) re-hash or count the authors' complete local dataset (all videos, raw API dumps), so they are skipped unless those folders exist (`scripts/fetch_data.py --media` provides the videos; the raw dumps are not published).
- `tests/browser/ui_workflow_test.py`: 58 browser checks in real Chrome (Playwright). Run with `ORVEX_URL=<address>`.

### D. What is stored where
| Data | Where | Why |
|---|---|---|
| Code, small tables (CSV, JSONL), manifests, docs, screenshots | GitHub | normal files under 100 MB |
| 596 original videos, 1,131 variants | Hugging Face dataset | 16.6 GB |
| 3 tables over 100 MB (`media_relationship_edges.csv`, `real_world_media_master.csv`, `platform_observations.csv`) | Hugging Face dataset | GitHub file limit |
| Not published | raw API dumps (`data/real_world/raw_metadata`), mask archives, 2 variants that failed validation, local database, secrets | not needed for the demo; third-party metadata dumps; private |

## 19. Known limitations of the prototype
- No trained model; no embeddings, OCR or speech features; candidate search over a large collection is not implemented.
- Uploaded videos are only validated with FFprobe and stored (temporary disk on the Space).
- Many read endpoints do not check the login token in the backend (the web app hides them behind login). Acceptable for a public demo of public data, not for real investigations.
- Case files, reviews and uploads reset when the free Space restarts.
- Video playback depends on Hugging Face storage availability.
- Tested in Chrome only.
