import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api, mmss, tok } from '../api'
import { Badge, Card, FamilyPicker, Loading, Note, PageTitle, Thumb, useActive, useApi } from '../ui'

export function Investigations() {
  const [tick, setTick] = useState(0); const { d, err, loading } = useApi<any[]>('/investigations', undefined, [tick]); const nav = useNavigate(); const [act, setAct] = useActive()
  const [f, setF] = useState({ title: '', summary: '', hypothesis: '' }); const [root, setRoot] = useState('RW-CMN-P10491224'); const [ref, setRef] = useState(''); const [q, setQ] = useState(''); const [msg, setMsg] = useState('')
  const { d: m } = useApi<any>('/media', { q, kind: 'natural', source: 'RW-01', limit: 12 }); const [up, setUp] = useState<any>(null)
  const create = async () => { const r = await api('/investigations', { method: 'POST', body: { ...f, reference_id: ref || up?.id || root } }); setAct({ id: r.id, title: f.title, reference_id: ref || up?.id || root, root: ref.startsWith('RW-CMN') || !ref ? (ref || root) : root }); nav('/investigations/' + r.id) }
  const upload = async (file: File) => { const fd = new FormData(); fd.append('f', file); setMsg('Uploading and probing…'); const r = await fetch('/api/upload', { method: 'POST', headers: { Authorization: 'Bearer ' + tok() }, body: fd }); if (r.ok) { setUp(await r.json()); setMsg('') } else setMsg((await r.json()).detail) }
  return <div className="space-y-4"><PageTitle title="Investigations" sub="Each investigation starts from a reference video chosen from the real media collection (or a local upload) and keeps its own history, review decisions and report." />
    <div className="grid lg:grid-cols-[1fr_440px] gap-4">
      <Card title="All investigations"><Loading err={err} loading={loading} />{d && (d.length ? <table className="t"><thead><tr><th>#</th><th>Title</th><th>Reference</th><th>Status</th><th>Owner</th><th>Created</th><th /></tr></thead><tbody>{d.map(i => <tr key={i.id} onClick={() => nav('/investigations/' + i.id)}>
        <td>{i.id}</td><td className="font-semibold">{i.title}</td><td className="font-mono text-[11px]">{i.reference_id}</td><td><Badge c={i.status === 'open' ? '#2563EB' : i.status === 'closed' ? '#0F766E' : '#E86A16'}>{i.status}</Badge></td><td>{i.owner}</td><td>{i.created.slice(0, 10)}</td><td>{act?.id === i.id && <Badge c="#E86A16">active</Badge>}</td></tr>)}</tbody></table> : <Note>No investigations yet. Create the first one on the right: pick a reference video and the graph, comparison and report pages will use it.</Note>)}</Card>
      <Card title="New investigation"><div className="space-y-2.5">
        <input className="inp" placeholder="Title, e.g. Re-uploads of ‘Ashs-learning-common’" value={f.title} onChange={e => setF({ ...f, title: e.target.value })} />
        <div><div className="text-xs font-semibold mb-1">Reference video: source family with controlled variants</div><FamilyPicker root={root} onPick={r => { setRoot(r); setRef('') }} /><div className="flex gap-3 mt-2 items-center"><Thumb id={ref || root} w={240} className="w-40 h-24 rounded-lg" /><div className="text-[12px] text-gray-600">Selected: <b>{ref || root}</b></div></div></div>
        <div><div className="text-xs font-semibold mb-1">…or search any local Commons video</div><input className="inp" placeholder="Search title or ID" value={q} onChange={e => setQ(e.target.value)} />
          {q && <div className="max-h-40 overflow-auto mt-1 border border-line rounded-lg">{m?.items.map((x: any) => <div key={x.id} onClick={() => { setRef(x.id); setQ('') }} className="flex gap-2 items-center p-1.5 hover:bg-soft cursor-pointer"><Thumb id={x.id} w={120} className="w-14 h-9 rounded" /><div className="text-[11.5px]">{x.title?.slice(0, 48)}<br /><span className="text-gray-500">{x.id} · {mmss(x.duration)}</span></div></div>)}</div>}</div>
        <div><div className="text-xs font-semibold mb-1">…or upload a local video (stored and probed; no ORVEX features are computed for uploads)</div><input type="file" accept="video/*" onChange={e => e.target.files?.[0] && upload(e.target.files[0])} className="text-xs" />{msg && <div className="text-xs">{msg}</div>}
          {up && <div className="text-[12px] mt-1">Registered <b>{up.id}</b>: {up.width}×{up.height}, {mmss(up.duration)}</div>}</div>
        <textarea className="inp" rows={2} placeholder="Summary / reason for investigation" value={f.summary} onChange={e => setF({ ...f, summary: e.target.value })} />
        <textarea className="inp" rows={2} placeholder="Investigator hypothesis (kept apart from findings)" value={f.hypothesis} onChange={e => setF({ ...f, hypothesis: e.target.value })} />
        <button disabled={!f.title} className="btn btn-primary" onClick={async () => { await create(); setTick(tick + 1) }}>Create investigation</button></div></Card></div></div>
}

export function InvestigationDetail() {
  const { id } = useParams(); const [tick, setTick] = useState(0); const { d, err, loading } = useApi<any>('/investigations/' + id, undefined, [tick]); const [act, setAct] = useActive(); const [e, setE] = useState<any>(null)
  if (!d) return <Loading err={err} loading={loading} />
  const root = d.reference_id; const form = e || { title: d.title, summary: d.summary || '', hypothesis: d.hypothesis || '', status: d.status }
  const save = async () => { await api('/investigations/' + id, { method: 'PUT', body: { ...form, reference_id: d.reference_id } }); setE(null); setTick(tick + 1) }
  const make = () => setAct({ id: d.id, title: d.title, reference_id: d.reference_id, root: d.reference_id.startsWith('CV-') ? d.reference_id : d.reference_id })
  return <div className="space-y-4"><PageTitle title={`#${d.id} ${d.title}`} sub={`Opened ${d.created} by ${d.owner}`} right={<div className="flex gap-2"><button className="btn btn-navy" onClick={make}>{act?.id === d.id ? 'Active investigation' : 'Make active'}</button><Link className="btn btn-primary" to="/graph" onClick={make}>Open relationship graph</Link><Link className="btn" to="/report" onClick={make}>Report</Link></div>} />
    <div className="grid lg:grid-cols-[340px_1fr_340px] gap-4">
      <Card title="Reference video"><Thumb id={root} w={480} className="w-full aspect-video rounded-lg" /><div className="font-mono text-[11px] mt-2">{root}</div>
        <div className="flex flex-col gap-1.5 mt-3 text-[13px]"><Link className="text-accent font-semibold" to="/candidates" onClick={make}>Candidate discovery →</Link><Link className="text-accent font-semibold" to="/compare" onClick={make}>Video comparison →</Link><Link className="text-accent font-semibold" to="/provenance" onClick={make}>Provenance →</Link><Link className="text-accent font-semibold" to="/evidence" onClick={make}>Evidence ledger →</Link></div></Card>
      <Card title="Investigation workspace"><div className="space-y-2"><label className="text-xs font-semibold">Title<input className="inp mt-1" value={form.title} onChange={x => setE({ ...form, title: x.target.value })} /></label>
        <label className="text-xs font-semibold">Status<select className="inp mt-1" value={form.status} onChange={x => setE({ ...form, status: x.target.value })}>{['open', 'in review', 'closed'].map(s => <option key={s}>{s}</option>)}</select></label>
        <label className="text-xs font-semibold">Summary / conclusion<textarea className="inp mt-1" rows={3} value={form.summary} onChange={x => setE({ ...form, summary: x.target.value })} /></label>
        <label className="text-xs font-semibold">Investigator hypothesis (not a finding)<textarea className="inp mt-1" rows={3} value={form.hypothesis} onChange={x => setE({ ...form, hypothesis: x.target.value })} /></label>
        <button className="btn btn-primary" onClick={save} disabled={!e}>Save</button></div>
        <div className="font-bold mt-5 mb-2">Review decisions ({d.reviews.length})</div>{d.reviews.length ? <table className="t"><thead><tr><th>Edge</th><th>Decision</th><th>Note</th><th>By</th></tr></thead><tbody>{d.reviews.map((r: any) => <tr key={r.id}><td className="font-mono text-[11px]">{r.edge_key}</td><td><Badge c={r.decision === 'accepted' ? '#0F766E' : r.decision === 'rejected' ? '#DC2626' : '#E86A16'}>{r.decision}</Badge></td><td>{r.note}</td><td>{r.actor}</td></tr>)}</tbody></table>
          : <Note>No edge has been reviewed in this investigation yet. Open the relationship graph (make this investigation active first) and mark an edge accepted, uncertain or rejected.</Note>}</Card>
      <Card title="Investigation history"><ul className="text-[12.5px] space-y-2.5">{d.history.map((h: any) => <li key={h.id} className="border-l-2 border-accent pl-2.5"><b>{h.actor}</b> {h.action}<div className="text-[11px] text-gray-500">{h.ts}</div></li>)}</ul></Card></div></div>
}
