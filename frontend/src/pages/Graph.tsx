import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { ReactFlow, ReactFlowProvider, Background, MiniMap, MarkerType, BaseEdge, EdgeLabelRenderer, getStraightPath, Handle, Position, useReactFlow, useNodesState } from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { Plus, Minus, Maximize2, Minimize2, ScanSearch, RotateCcw, Play } from 'lucide-react'
import FsVideo from '../FsVideo'
import CinemaPlayer from '../CinemaPlayer'
import { canLockEsc, enterFs, exitFs, fsElement, lockEsc, unlockEsc } from '../fs'
import { api, frame, stream, mmss, ROLE, TLABEL } from '../api'
import { Badge, Collapsible, FamilyPicker, Loading, Note, useActive, useApi, useRoot } from '../ui'

const lab = (t?: string) => (t && TLABEL[t]) || t || ''
const NW = 146, NH = 120   // node box used for layout and for clipping edges at the node border
function VideoNode({ data }: any) {
  const r = ROLE[data.role]; const sel = data.selected; const dim = data.dim
  return <div className={'text-center cursor-pointer ' + (sel ? 'node-pulse' : '')} style={{ width: NW, opacity: dim ? 0.5 : 1, transition: 'opacity .2s' }}>
    <Handle type="target" position={Position.Top} style={{ opacity: 0, top: '50%', left: '50%' }} /><Handle type="source" position={Position.Bottom} style={{ opacity: 0, top: '50%', left: '50%' }} />
    <div style={{ border: `3px solid ${r.c}`, borderRadius: 8, boxShadow: sel ? `0 0 0 4px ${r.c}66, 0 8px 18px #0008` : '0 2px 8px #0008', overflow: 'hidden', background: '#000' }}>
      <img src={frame(data.id, 1, 300)} draggable={false} style={{ width: NW - 6, height: 82, objectFit: 'cover', display: 'block' }} /></div>
    <div className="vn-id text-[12.5px] font-extrabold mt-1 leading-tight rounded px-1" style={{ background: sel ? r.c : 'transparent', color: sel ? '#fff' : undefined }}>{data.short}</div><div className="vn-cap text-[11px] leading-tight">{data.caption}<br />({mmss(data.duration)})</div></div>
}
function RelEdge({ id, sourceX, sourceY, targetX, targetY, data, markerEnd, selected }: any) {
  const c = ROLE[data.role].c; const dx = targetX - sourceX, dy = targetY - sourceY
  const L = Math.hypot(dx, dy) || 1; const ux = dx / L, uy = dy / L
  const tx = ux ? (NW / 2 + 4) / Math.abs(ux) : Infinity, ty = uy ? (NH / 2 - 10) / Math.abs(uy) : Infinity; const t = Math.min(tx, ty)
  const x1 = sourceX + ux * t, y1 = sourceY + uy * t, x2 = targetX - ux * (t + 4), y2 = targetY - uy * (t + 4)
  const [p, lx, ly] = getStraightPath({ sourceX: x1, sourceY: y1, targetX: x2, targetY: y2 }); const lit = data.lit !== false
  return <><BaseEdge id={id} path={p} markerEnd={markerEnd} className={selected ? 'edge-flow' : ''} style={{ stroke: c, strokeWidth: selected ? 4 : lit ? 2.4 : 1.4, opacity: lit ? 1 : 0.4, strokeDasharray: data.directed ? undefined : '6 5' }} />
    {Math.hypot(x2 - x1, y2 - y1) > 40 && <EdgeLabelRenderer><div style={{ position: 'absolute', transform: `translate(-50%,-50%) translate(${lx}px,${ly}px)`, color: c, border: `1px solid ${c}88`, borderRadius: 5, fontSize: 10.5, padding: '0 6px', background: '#0a1424', opacity: lit ? 1 : 0.5, pointerEvents: 'none', whiteSpace: 'nowrap' }} className="font-semibold">{data.label}</div></EdgeLabelRenderer>}</>
}
const nodeTypes = { video: VideoNode }; const edgeTypes = { rel: RelEdge }

/** Radial tree layout: depth rings, an angular wedge per subtree proportional to its leaf count, and ring radii grown so that
 *  neighbouring nodes do not overlap. Unrelated (negative-pair) videos get their own wedge. Positions are node centres. */
function layout(g: any) {
  const kids: Record<string, string[]> = {}
  g.edges.forEach((e: any) => (kids[e.source] ||= []).push(e.target))
  const depth: Record<string, number> = { [g.root]: 0 }; const leaves: Record<string, number> = {}; const seen = new Set<string>()
  const walk = (id: string, d: number): number => { seen.add(id); depth[id] = d; const k = (kids[id] || []).filter(x => !seen.has(x)); leaves[id] = k.length ? k.reduce((a, x) => a + walk(x, d + 1), 0) : 1; return leaves[id] }
  walk(g.root, 0)
  const perDepth: Record<number, number> = {}; Object.values(depth).forEach(d => (perDepth[d] = (perDepth[d] || 0) + 1))
  const R: number[] = [0]; const maxD = Math.max(...Object.values(depth))
  for (let d = 1; d <= maxD; d++) R[d] = Math.max(R[d - 1] + 235, (perDepth[d] * (NW + 44)) / (2 * Math.PI) * 1.25)
  const pos: Record<string, { x: number; y: number }> = { [g.root]: { x: 0, y: 0 } }; const KX = 1.5, KY = 0.74
  const place = (id: string, a0: number, a1: number) => {
    let a = a0; const k = (kids[id] || []).filter(x => depth[x] === depth[id] + 1); const tot = k.reduce((s2, x) => s2 + leaves[x], 0) || 1
    k.forEach(x => { const w = (a1 - a0) * leaves[x] / tot; const m = a + w / 2; pos[x] = { x: Math.cos(m) * R[depth[x]] * KX, y: Math.sin(m) * R[depth[x]] * KY }; place(x, a, a + w); a += w })
  }
  place(g.root, -Math.PI / 2, 1.5 * Math.PI)
  return pos
}

function Inner() {
  const [root, setRoot] = useRoot(); const [act] = useActive(); const [showAll, setAll] = useState(false)
  const { d: g, err, loading } = useApi<any>('/graph/' + root, { all: showAll || '' }); const { d: tl } = useApi<any[]>('/timeline/' + root)
  const [sel, setSel] = useState(root); const [nodes, setNodes, onNodesChange] = useNodesState<any>([]); const rf = useReactFlow(); const [tf, setTf] = useState<string[]>([]); const [hover, setHover] = useState<any>(null)
  const [note, setNote] = useState(''); const [saved, setSaved] = useState('')
  const gbox = useRef<HTMLDivElement>(null)
  const [ws, setWs] = useState(false); const [video, setVideo] = useState<string | null>(null); const videoRef = useRef<string | null>(null); videoRef.current = video; const wsRef = useRef(false); wsRef.current = ws
  /** Graph workspace = the same graph card switched to a fixed, viewport-filling layout (CSS only), so React Flow is never remounted and keeps nodes, zoom, pan and selection. */
  const enterWs = () => { setWs(true); if (canLockEsc() && !fsElement()) enterFs(document.documentElement).then(lockEsc).catch(() => { }) }
  const exitWs = useCallback(() => { setWs(false); unlockEsc(); if (fsElement()) exitFs().catch(() => { }) }, [])
  useEffect(() => {   // Esc closes the video overlay first (the overlay handles that itself); only when no video is open does Esc leave the graph workspace
    if (!ws) return; const k = (ev: KeyboardEvent) => { if (ev.key === 'Escape' && !videoRef.current) { ev.preventDefault(); exitWs() } }
    window.addEventListener('keydown', k); return () => window.removeEventListener('keydown', k) }, [ws, exitWs])
  useEffect(() => () => { if (wsRef.current && fsElement()) { unlockEsc(); exitFs().catch(() => { }) } }, [])
  const fit = useCallback(() => rf.fitView({ padding: 0.04, duration: 250, maxZoom: 1.4 }), [rf])
  useEffect(() => { if (!g) return; const pos = layout(g)
    setNodes(g.nodes.map((n: any) => ({ id: n.id, type: 'video', position: { x: (pos[n.id]?.x ?? 0) - NW / 2, y: (pos[n.id]?.y ?? 0) - NH / 2 }, data: { ...n, short: n.id === g.root ? n.id.replace('RW-CMN-P', 'R-') : n.id.replace('CV-P', 'V-').replace(/^V-\d+-/, ''), caption: n.role === 'reference' ? 'Original video' : n.role === 'unrelated' ? 'Unrelated video' : lab(n.transformation) } })))
    setSel(g.root); setTimeout(() => rf.fitView({ padding: 0.04, maxZoom: 1.4 }), 80) }, [g])
  useEffect(() => { const el = gbox.current; if (!el) return; let t: any; const ro = new ResizeObserver(() => { clearTimeout(t); t = setTimeout(() => rf.fitView({ padding: 0.04, duration: 200, maxZoom: 1.4 }), 120) }); ro.observe(el); return () => { clearTimeout(t); ro.disconnect() } }, [rf, !!g])
  const resetLayout = () => { if (!g) return; const pos = layout(g); setNodes(ns => ns.map(n => ({ ...n, position: { x: (pos[n.id]?.x ?? 0) - NW / 2, y: (pos[n.id]?.y ?? 0) - NH / 2 } }))); setSel(g.root); setTimeout(fit, 60) }
  const byId = useMemo(() => Object.fromEntries((g?.nodes || []).map((n: any) => [n.id, n])), [g]); const edgeOf = (id: string) => (g?.edges || []).find((e: any) => e.target === id)
  const edges = useMemo(() => (g?.edges || []).map((e: any) => ({ id: e.id, source: e.source, target: e.target, type: 'rel', selected: sel === e.target, data: { ...e, lit: sel === g.root || e.source === sel || e.target === sel }, markerEnd: e.directed ? { type: MarkerType.ArrowClosed, color: ROLE[e.role].c, width: 18, height: 18 } : undefined })), [g, sel])
  const linked = useMemo(() => { const s2 = new Set([sel]); (g?.edges || []).forEach((x: any) => { if (x.source === sel) s2.add(x.target); if (x.target === sel) s2.add(x.source) }); return s2 }, [g, sel])
  const nodesV = nodes.map(n => ({ ...n, data: { ...n.data, selected: n.id === sel, dim: sel !== g?.root && !linked.has(n.id) } }))
  const s = byId[sel]; const e = s && edgeOf(sel); const rootN = g && byId[g.root]
  const submit = async (decision: string) => { if (!e) return; await api('/reviews', { method: 'POST', body: { inv_id: act?.id || 0, edge_key: e.id, decision, note, evidence_ids: e.evidence_ids } }); setSaved(`Recorded “${decision}” for ${e.id}`); setNote('') }
  const events = useMemo(() => { if (!tl || !g) return []; const vis = new Set(g.nodes.map((n: any) => n.id)); const keep = tl.filter(x => !tf.length || tf.includes(x.type)); const shown = keep.filter(x => x.type !== 'variant_creation' || vis.has(x.media)); return shown }, [tl, g, tf])
  const TC: any = { original_publication: '#2563EB', platform_observation: '#7C3AED', dataset_collection: '#0F766E', variant_creation: '#DC2626' }
  const TN: any = { original_publication: 'Original publication', platform_observation: 'Platform observation', dataset_collection: 'Dataset collection', variant_creation: 'Variant creation' }
  const related = (g?.nodes || []).filter((n: any) => n.id !== g.root)
  const bar = (v?: number) => v == null ? null : <div className="h-2 rounded bg-gray-200 mt-1"><div className="h-2 rounded bg-green-500" style={{ width: `${Math.round(v * 100)}%` }} /></div>
  const detailHead = (x: any) => <>
    <div className="flex items-center gap-2 mt-2"><span className="font-extrabold">{x.id.replace('CV-', '')}</span><Badge c={ROLE[x.role].c}>{ROLE[x.role].name}</Badge></div>
    <div className="font-semibold text-[13px]">{x.role === 'reference' ? x.title : x.role === 'unrelated' ? 'Unrelated video (sampled negative)' : lab(x.transformation)}</div>
    <table className="t mt-2"><tbody>{[['Source', x.source], ['Duration', mmss(x.duration)], ['Resolution', `${x.width}×${x.height}`], ['File size', x.bytes ? (x.bytes / 1e6).toFixed(1) + ' MB' : '–'], ['Transformation', x.transformation ? `${lab(x.transformation)} (${x.transformation_family})` : '–'],
      [x.kind === 'variant' ? 'Created (variant record)' : 'Published (source)', (x.created_utc || x.published || '–').slice(0, 10)], ['Licence', x.license || '–'], ['Split', x.split || '–']].map(([a, b]) => <tr key={a}><td className="font-semibold w-[44%]">{a}</td><td>{b}</td></tr>)}</tbody></table></>
  const detailBody = () => !s ? null : e ? <>
    <Collapsible title="Measured features vs parent">
      <div className="text-[12px] mt-1">dHash matched frames: <b>{e.sims?.dhash_match_fraction != null ? (e.sims.dhash_match_fraction * 100).toFixed(0) + '%' : 'n/a'}</b>{bar(e.sims?.dhash_match_fraction)}</div>
      <div className="text-[12px] mt-1">Audio envelope agreement: <b>{e.sims?.audio_envelope_agreement != null ? (e.sims.audio_envelope_agreement * 100).toFixed(0) + '%' : 'n/a'}</b>{bar(e.sims?.audio_envelope_agreement)}</div>
      <div className="text-[12px] mt-1">Audio MD5 identical: <b>{String(e.sims?.audio_md5_identical ?? 'n/a')}</b></div>
      <div className="text-[10.5px] text-gray-500 mt-1">Measurements from data/derived/features (dHash rule of s9; 1-second audio envelope). Not a model score.</div></Collapsible>
    <Collapsible title="Recorded changes"><ul className="text-[12px] list-disc ml-4 mt-1"><li>{e.role === 'unrelated' ? 'Sampled negative pair: no relationship recorded.' : `Logged operation: ${lab(e.label)}`}</li>{s.params && <li className="break-all">Parameters: {s.params}</li>}{s.caption_text && <li>Caption text (title of another real record): “{s.caption_text}”</li>}{s.audio_source && <li>Audio taken from {s.audio_source}</li>}</ul></Collapsible>
    <Collapsible title="Evidence record" badge={<Badge c="#2FA36B">{e.label_source.split(' ')[0]}</Badge>}><div className="text-[11.5px] mt-1">{e.relationship_id && <div>Edge record: <b>{e.relationship_id}</b> ({e.normalized_relation_type})</div>}<div>Label source: {e.label_source}</div>{e.evidence_ids.map((x: string) => <a key={x} href={`/evidence?id=${x}`} className="block text-accent font-semibold">{x}</a>)}</div></Collapsible>
    <Collapsible title="Frame comparison"><div className="grid grid-cols-2 gap-2 mt-1"><div><img src={frame(e.source, 2, 300)} className="rounded w-full" /><div className="text-[10.5px] text-gray-600">Frame: parent {e.source.slice(-10)}</div></div><div><img src={frame(sel, 2, 300)} className="rounded w-full" /><div className="text-[10.5px] text-gray-600">Frame: {sel.slice(-10)}</div></div></div></Collapsible>
    <Collapsible title="Forensic review of this edge"><textarea className="inp mt-1" rows={2} placeholder="Review note" value={note} onChange={x => setNote(x.target.value)} />
      <div className="flex gap-1.5 mt-1.5">{['accepted', 'uncertain', 'rejected'].map(k => <button key={k} className="btn !px-2.5 !py-1" onClick={() => submit(k)}>{k}</button>)}</div>{saved && <div className="text-[11px] text-green-700 mt-1">{saved}</div>}</Collapsible></>
    : s.role === 'reference' ? <div className="mt-3"><Note>Reference video. Select a derivative to see how it differs and what the dataset records about it.</Note></div> : null
  const timeline = <div className={'card p-3 shrink-0 ' + (ws ? 'm-2 mt-0' : '')} data-graph-timeline><div className="flex items-center gap-3 mb-2"><b>Timeline View</b><span className="text-[11.5px] text-gray-500">Dates from different fields, kept apart. Click a marker to select the video.</span>
    <span className="ml-auto flex gap-1.5">{Object.keys(TN).map(k => <button key={k} onClick={() => setTf(tf.includes(k) ? tf.filter(x => x !== k) : [...tf, k])} className="text-[11px] px-2 py-0.5 rounded-full border" style={{ borderColor: TC[k], background: tf.includes(k) ? TC[k] : '#fff', color: tf.includes(k) ? '#fff' : TC[k] }}>{TN[k]}</button>)}</span></div>
    <div className="relative overflow-x-auto"><div className="flex gap-0 min-w-full" style={{ borderTop: '2px solid #cfd2e3', paddingTop: 0 }}>{events.map((x: any, i: number) => <div key={i} onClick={() => byId[x.media] && setSel(x.media)} className="flex-1 min-w-[96px] text-center cursor-pointer -mt-[7px]">
      <i className="inline-block w-3 h-3 rounded-full" style={{ background: TC[x.type], outline: sel === x.media ? '3px solid #E86A1666' : 'none' }} /><div className="text-[10.5px] text-gray-600 mt-1">{x.date?.slice(0, 10)}</div><div className="text-[11px] font-bold">{x.media === g?.root ? 'Root' : x.media.replace('CV-', '').slice(-9)}</div><div className="text-[10px] text-gray-500 leading-tight px-1">{TN[x.type]}</div></div>)}</div></div></div>
  const legend = <div data-graph-legend className="absolute left-3 top-12 z-10 glegend px-3 py-2 text-[12px]"><div className="label-cap mb-1">Relationship legend</div>{Object.entries(ROLE).map(([k, v]) => <div key={k} className="flex items-center gap-2"><i style={{ background: v.c }} className="w-3 h-3 rounded-full inline-block" />{v.name}</div>)}<div className="mt-1 text-[10.5px] text-slate-400">solid arrow = parent to child (transformation log)<br />dashed = sampled negative pair</div></div>
  return <div className="min-h-full flex flex-col gap-3 min-w-0" style={{ minHeight: 'calc(100vh - 96px)' }}>
    <div className="flex items-start justify-between gap-4">
      <div><div className="eyebrow">Media investigation · Relationship analysis</div><h1 className="text-2xl font-extrabold text-navy">Video Relationship Graph</h1><p className="text-[13px] text-gray-600">How the reference video and related videos are connected, from the controlled transformation log of the ORVEX dataset (ground truth, not a model prediction).</p></div>
      <div className="card px-4 py-2 flex gap-4 text-[12px] items-center flex-wrap justify-end">{Object.entries(ROLE).map(([k, v]) => <span key={k} className="flex items-center gap-1.5"><i style={{ background: v.c }} className="w-3 h-3 rounded-full inline-block" />{v.name}</span>)}</div></div>
    <div className="flex items-center gap-3 text-[12px]"><span className="font-semibold">Source family</span><FamilyPicker root={root} onPick={setRoot} />
      <label className="flex items-center gap-1"><input type="checkbox" checked={showAll} onChange={e => setAll(e.target.checked)} />Show all {g?.total_variants} variants</label></div>
    <Loading err={err} loading={loading && !g} />
    {g && <div className="grid gap-3 flex-1 min-h-[540px]" style={{ gridTemplateColumns: '270px minmax(0,1fr) 310px' }}>
      <div className="card p-3 overflow-auto"><div className="font-bold mb-2">Reference Video</div>
        <FsVideo key={g.root} label="Reference Video" id={g.root} title={rootN.title} poster={frame(g.root, 1, 480)} src={stream(g.root)} />
        <div className="mt-2 flex items-center gap-2"><span className="font-extrabold text-[15px]">{g.root.replace('RW-CMN-P', 'R-')}</span><Badge c="#2563EB">Reference</Badge></div>
        <div className="text-[12px] leading-5 mt-1"><b>Title:</b> {rootN.title}<br /><b>Source:</b> {rootN.source}<br /><b>Published:</b> {rootN.published?.slice(0, 10) || 'not recorded'}<br /><b>Duration:</b> {mmss(rootN.duration)}<br /><b>Resolution:</b> {rootN.width}×{rootN.height}</div>
        <div className="font-bold mt-4 mb-2">Related Videos ({related.length}{g.total_variants > related.length ? ` of ${g.total_variants}` : ''})</div>
        <div className="space-y-2">{related.map((n: any) => <div key={n.id} onClick={() => setSel(n.id)} className={'flex gap-2 p-1.5 rounded-lg border cursor-pointer transition ' + (sel === n.id ? 'border-accent bg-orange-50' : 'border-line hover:bg-soft')}>
          <img src={frame(n.id, 1, 160)} className="w-[64px] h-[42px] object-cover rounded" /><div className="min-w-0"><div className="text-[12px] font-bold truncate">{n.id.replace('CV-', '')}</div><Badge c={ROLE[n.role].c}>{n.role === 'unrelated' ? 'Unrelated' : lab(n.transformation)}</Badge><div className="text-[10.5px] text-gray-500">{mmss(n.duration)} · {n.role === 'unrelated' ? 'sampled negative pair' : n.depth > 1 ? `depth ${n.depth} (via ${n.parent?.replace('CV-', '')})` : 'derived from the reference'}</div></div></div>)}</div></div>
      <div className="flex flex-col gap-3 min-h-0 min-w-0">
        <div ref={gbox} data-graph-panel data-ws={ws ? 'open' : 'closed'} role={ws ? 'dialog' : undefined} aria-label="Relationship graph workspace" className={'gpanel flex-1 min-h-[340px] flex ' + (ws ? 'ws' : '')}>
          <div className="flex-1 min-w-0 flex flex-col">
            <div className="relative flex-1 min-h-0">
              <div className="absolute left-4 top-3 z-10 flex items-center gap-3"><span className="label-cap !text-amber-400">Relationship analysis</span><b className="text-[14px]">Relationship Graph</b>{ws && g && <span className="text-[12px] text-slate-400">{g.nodes.length} videos · {g.edges.length} connections · ground-truth transformation log</span>}</div>
              <div className="absolute inset-0"><ReactFlow nodes={nodesV} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes} onNodesChange={onNodesChange} onNodeClick={(_, n) => setSel(n.id)} onEdgeClick={(_, ed) => setSel(ed.target)}
                onNodeMouseEnter={(_, n) => setHover(n.data)} onNodeMouseLeave={() => setHover(null)} fitView fitViewOptions={{ padding: 0.04, maxZoom: 1.4 }} minZoom={0.1} maxZoom={2.2} proOptions={{ hideAttribution: true }}><Background gap={26} color="#1b3050" /><MiniMap pannable zoomable style={{ width: ws ? 190 : 120, height: ws ? 130 : 80 }} maskColor="#0a142499" nodeColor={(n: any) => ROLE[n.data.role]?.c} /></ReactFlow></div>
              <div data-graph-toolbar className="absolute right-3 top-3 flex flex-col gap-1.5 z-10">{[[Plus, () => rf.zoomIn({ duration: 150 }), 'Zoom in'], [Minus, () => rf.zoomOut({ duration: 150 }), 'Zoom out'], [ScanSearch, fit, 'Fit to screen'], [RotateCcw, resetLayout, 'Reset view'], [ws ? Minimize2 : Maximize2, ws ? exitWs : enterWs, ws ? 'Exit fullscreen (Esc)' : 'Fullscreen graph']].map(([I, f, t]: any, i) => <button key={i} type="button" className="gbtn" title={t} aria-label={t} onClick={f}><I size={16} /></button>)}</div>
              {ws && legend}
              {hover && !ws && <div className="absolute left-3 bottom-3 z-10 glegend px-3 py-2 text-[11.5px]"><b>{hover.id}</b> · {ROLE[hover.role].name}<br />{hover.kind === 'variant' ? `${lab(hover.transformation)} · created ${hover.created_utc?.slice(0, 10)}` : hover.title}<br />{mmss(hover.duration)} · {hover.width}×{hover.height}</div>}
            </div>
            {ws && timeline}
          </div>
          {ws && s && <aside data-graph-drawer aria-label="Selected video details" className="drawer p-3">
            <div className="label-cap !text-slate-500">Forensic review · selected video</div>
            <button type="button" data-open-video onClick={() => setVideo(s.id)} aria-label="Play selected video fullscreen" className="relative block w-full mt-2 rounded overflow-hidden group bg-black"><img src={frame(s.id, 1, 480)} className="w-full aspect-video object-cover" />
              <span className="absolute inset-0 grid place-items-center bg-black/35 group-hover:bg-black/15 transition"><span className="w-14 h-14 rounded-full bg-accent text-white grid place-items-center shadow-lg"><Play size={24} /></span></span><span className="absolute bottom-1.5 right-2 text-[11px] bg-black/75 text-white px-1.5 py-0.5 rounded">Play fullscreen</span></button>
            {detailHead(s)}{detailBody()}</aside>}
        </div>
        {!ws && timeline}
      </div>
      <div className="card p-3 overflow-auto">{s && <><div className="font-bold mb-2">Selected Video Details</div>
        <FsVideo key={s.id} label="Selected Video" id={s.id} title={s.title || lab(s.transformation)} poster={frame(s.id, 1, 480)} src={stream(s.id)} />
        {detailHead(s)}{detailBody()}</>}</div>
    </div>}
    {g && <Note>{g.note}</Note>}
    {video && byId[video] && <CinemaPlayer key={video} id={video} title={byId[video].title || lab(byId[video].transformation)} subtitle={ROLE[byId[video].role].name} src={stream(video)} poster={frame(video, 1, 640)} onClose={() => setVideo(null)} />}
  </div>
}
export default function Graph() { return <ReactFlowProvider><Inner /></ReactFlowProvider> }
