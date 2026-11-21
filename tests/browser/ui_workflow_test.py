"""Browser test of the ORVEX investigation UI (real Chrome, real backend, real data).
Needs the app running (backend on :8001, frontend on :5173) and Playwright for Python.
Run:  .venv-orvex-test\\Scripts\\python.exe tests\\browser\\ui_workflow_test.py
The Chromium path below is the one installed on this machine; change CHROME if yours differs. Screenshots go to tests/browser/shots/."""
import os, sys
from playwright.sync_api import sync_playwright

B = os.environ.get("ORVEX_URL", "http://localhost:5173")
CHROME = os.environ.get("CHROME", "")   # optional: path to a Chrome/Chromium executable; empty = Playwright's own browser
OUT = os.path.join(os.path.dirname(__file__), "shots"); os.makedirs(OUT, exist_ok=True)
res = []


def ok(name, cond, extra=""):
    res.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name, extra)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None, args=["--autoplay-policy=no-user-gesture-required"])
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    errs, graph_reqs = [], []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("request", lambda r: graph_reqs.append(r.url) if "/api/graph/" in r.url else None)
    pg.goto(B + "/login"); pg.fill("form input.inp >> nth=0", "demo.investigator@orvex.local"); pg.fill("input[type=password]", os.environ.get("ORVEX_DEMO_PW", "OrvexDemo!2026")); pg.keyboard.press("Enter")
    pg.wait_for_url(B + "/", timeout=10000); pg.wait_for_timeout(2500)

    # ---- command centre / theme
    ok("command band present", pg.locator("[data-command-band]").count() == 1)
    first = pg.locator("main .card.lift").first.inner_text()
    ok("counter shows the real final value", "252,270" in first, first.replace("\n", " ")[:60])
    groups = [t.strip().lower() for t in pg.locator(".side-grp").all_inner_texts()]
    ok("sidebar investigation groups", all(x in groups for x in ["command centre", "media investigation", "forensic analysis", "evidence management", "data intelligence", "models and evaluation"]), str(groups))
    pg.locator(".side-grp", has_text="Evidence management").click(); pg.wait_for_timeout(400)
    ok("sidebar group collapses", pg.locator(".side-body.closed").count() == 1)
    pg.locator(".side-grp", has_text="Evidence management").click(); pg.wait_for_timeout(400)
    ok("sidebar group expands", pg.locator(".side-body.closed").count() == 0)
    ok("page transition class", pg.locator(".page-enter").count() == 1)
    pg.screenshot(path=OUT + "/dashboard.png")
    pg.locator("button[aria-label^='Notifications']").click(); pg.wait_for_timeout(300)
    ok("notification panel opens", pg.locator("[role=menu]").is_visible())
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    ok("notification panel closes on Esc", pg.locator("[role=menu]").count() == 0)

    # ---- graph page
    pg.goto(B + "/graph"); pg.wait_for_selector("[data-graph-panel] .react-flow__node", timeout=15000); pg.wait_for_timeout(2500)
    pg.screenshot(path=OUT + "/graph_normal.png")
    n0 = len(graph_reqs)
    # independent inline players with their own overlay
    def cinema(): return pg.locator("[data-cinema-player]").count()
    pg.locator("[data-fs-player='Reference Video'] button").click(); pg.wait_for_timeout(700)
    ok("reference fullscreen overlay opens", cinema() == 1 and "Reference Video" in pg.locator("[data-cinema-player]").inner_text())
    dims = pg.evaluate("(()=>{const v=document.querySelector('[data-cinema-video]');const r=document.querySelector('[data-cinema-player]').getBoundingClientRect();return [r.width,r.height,innerWidth,innerHeight,getComputedStyle(v).objectFit]})()")
    ok("overlay fills viewport, keeps aspect ratio", dims[0] >= dims[2] - 1 and dims[1] >= dims[3] - 1 and dims[4] == "contain", str(dims))
    pg.screenshot(path=OUT + "/cinema.png")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    ok("Esc closes reference overlay", cinema() == 0)
    pg.locator("[data-fs-player='Selected Video'] button").click(); pg.wait_for_timeout(700)
    ok("selected fullscreen overlay opens independently", cinema() == 1 and "Selected Video" in pg.locator("[data-cinema-player]").inner_text())
    pg.locator("[data-cinema-close]").click(); pg.wait_for_timeout(400)
    ok("close button closes overlay", cinema() == 0)

    # ---- enter the graph workspace
    nodes = pg.locator(".react-flow__node")
    pg.locator("[data-graph-toolbar] button[title='Fullscreen graph']").click(); pg.wait_for_timeout(1800)
    ok("graph workspace open", pg.locator("[data-graph-panel][data-ws=open]").count() == 1)
    box = pg.evaluate("(()=>{const r=document.querySelector('[data-graph-panel]').getBoundingClientRect();return [r.width,r.height,innerWidth,innerHeight]})()")
    ok("workspace fills the viewport", box[0] >= box[2] - 1 and box[1] >= box[3] - 1, str(box))
    ok("legend + timeline + drawer visible", pg.locator("[data-graph-legend]").is_visible() and pg.locator("[data-graph-timeline]").is_visible() and pg.locator("[data-graph-drawer]").is_visible())
    for t in ("Zoom in", "Zoom out", "Fit to screen", "Reset view"):
        ok("toolbar: " + t, pg.locator(f"[data-graph-toolbar] button[title='{t}']").count() == 1)
    vp = lambda: pg.evaluate("document.querySelector('.react-flow__viewport').style.transform")
    pg.locator("[data-graph-toolbar] button[title='Zoom in']").click(); pg.wait_for_timeout(400)
    z1 = vp(); pg.mouse.move(700, 450); pg.mouse.down(); pg.mouse.move(640, 410, steps=5); pg.mouse.up(); pg.wait_for_timeout(300)
    ok("zoom and pan change the view", z1 != vp())
    ov = pg.evaluate("""(()=>{const r=[...document.querySelectorAll('.react-flow__node')].map(n=>n.getBoundingClientRect());let c=0;for(let i=0;i<r.length;i++)for(let j=i+1;j<r.length;j++){const a=r[i],b=r[j];if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)c++}return c})()""")
    pg.screenshot(path=OUT + "/graph_workspace.png")

    def state():
        return pg.evaluate("""(()=>({vp:document.querySelector('.react-flow__viewport').style.transform,
          pos:[...document.querySelectorAll('.react-flow__node')].map(n=>n.getAttribute('data-id')+':'+n.style.transform).join('|'),
          sel:document.querySelector('[data-graph-drawer] .font-extrabold')?.textContent,
          n:document.querySelectorAll('.react-flow__node').length}))()""")

    def workflow(idx, label):
        nodes.nth(idx).click(force=True); pg.wait_for_timeout(700)
        sel = state()["sel"]
        ok(f"{label}: node click updates the drawer", bool(sel), str(sel))
        highlighted = pg.locator(".react-flow__edge .edge-flow").count()
        ok(f"{label}: selected relationship highlighted", highlighted >= 1, str(highlighted))
        before = state(); reqs = len(graph_reqs)
        pg.locator("[data-open-video]").click(); pg.wait_for_timeout(900)
        ok(f"{label}: video overlay opens over the graph", cinema() == 1 and pg.locator("[data-graph-panel][data-ws=open]").count() == 1)
        # controls
        playing0 = pg.evaluate("!document.querySelector('[data-cinema-video]').paused")
        pg.locator("[data-cinema-play]").click(); pg.wait_for_timeout(400)
        playing1 = pg.evaluate("!document.querySelector('[data-cinema-video]').paused")
        ok(f"{label}: play/pause works", playing0 != playing1, f"{playing0}->{playing1}")
        pg.evaluate("document.querySelector('[data-cinema-video]').muted = true")
        bx = pg.locator("[data-cinema-seek]").bounding_box(); pg.mouse.click(bx["x"] + bx["width"] * 0.4, bx["y"] + bx["height"] / 2); pg.wait_for_timeout(600)
        ct = pg.evaluate("document.querySelector('[data-cinema-video]').currentTime")
        ok(f"{label}: seek works", ct >= 5, f"{ct:.2f}s")
        pg.screenshot(path=OUT + f"/cinema_over_graph_{label}.png")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(700)
        after = state()
        ok(f"{label}: Esc closes only the video", cinema() == 0 and pg.locator("[data-graph-panel][data-ws=open]").count() == 1)
        ok(f"{label}: graph state unchanged (zoom, pan, positions, selection, node count)", before == after, "" if before == after else f"{before} != {after}")
        ok(f"{label}: no graph refetch", len(graph_reqs) == reqs)
        return after

    workflow(3, "first node")
    workflow(6, "second node")
    ok("no overlapping nodes in workspace", ov == 0, str(ov))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(900)
    ok("second Esc leaves the graph workspace", pg.locator("[data-graph-panel][data-ws=closed]").count() == 1)
    ok("graph not refetched during the whole workflow", len(graph_reqs) == n0, f"{n0} -> {len(graph_reqs)}")

    # ---- every page
    for path in ["/", "/investigations", "/candidates", "/compare", "/provenance", "/manipulation", "/distribution", "/evidence", "/datasets", "/variants", "/quality", "/models", "/evaluation", "/report", "/admin"]:
        pg.goto(B + path); pg.wait_for_timeout(1300)
        body = pg.inner_text("main")
        ok("page " + path, pg.locator("a.side-link.on").count() == 1 and len(body) > 40 and "Could not load" not in body)
        pg.screenshot(path=OUT + "/p" + path.replace("/", "_") + ".png")
    # ---- responsive + reduced motion
    pg.set_viewport_size({"width": 1280, "height": 720}); pg.goto(B + "/graph"); pg.wait_for_timeout(2500); pg.screenshot(path=OUT + "/graph_1280.png")
    ok("1280px layout has no page-level horizontal overflow", pg.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"))
    pg.emulate_media(reduced_motion="reduce"); pg.goto(B + "/investigations"); pg.wait_for_timeout(800)
    ok("reduced motion disables page animation", pg.evaluate("getComputedStyle(document.querySelector('.page-enter')).animationName") == "none")
    real = [e for e in errs if "favicon" not in e]
    ok("no console errors", not real, "; ".join(real)[:300])
    b.close()
fails = [n for n, c in res if not c]
print(len(res) - len(fails), "/", len(res), "passed")
sys.exit(1 if fails else 0)
