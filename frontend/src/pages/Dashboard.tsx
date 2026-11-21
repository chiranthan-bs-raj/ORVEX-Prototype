import { Link } from 'react-router-dom'
import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Card, Loading, Note, PageTitle, Stat, useActive, useApi } from '../ui'
import { TLABEL } from '../api'

const COL = ['#252C5C', '#E86A16', '#2563EB', '#7C3AED', '#0F766E', '#DC2626', '#F59E0B', '#6B7280']
const f = (n: number) => n?.toLocaleString()
export default function Dashboard() {
  const [act] = useActive(); const { d, err, loading } = useApi<any>('/summary'); const { d: q } = useApi<any>('/quality')
  if (!d) return <Loading err={err} loading={loading} />
  const cls = Object.entries(d.relationship_classes).map(([k, v]) => ({ name: k.replace(/_/g, ' '), n: v }))
  const tr = Object.entries(d.transformation_counts).map(([k, v]) => ({ name: TLABEL[k] || k, n: v }))
  const ds = Object.keys(d.by_dataset).map(k => ({ name: k, records: d.by_dataset[k], local: d.local_by_dataset[k] || 0 }))
  const ev = Object.entries(d.evidence_by_type).map(([k, v]) => ({ name: k.replace(/_/g, ' '), value: v }))
  return <div className="space-y-4">
    <PageTitle title="Dashboard" sub="Every number on this page is computed from the repository tables on request (data/derived/tables), the local media folders and the application database." />
    <div className="grid lg:grid-cols-3 gap-3" data-command-band>
      <div className="card p-4 border-l-4 !border-l-accent"><div className="label-cap !text-slate-500">Case file</div>
        {act?.id ? <><div className="font-extrabold text-navy text-[15px]">#{act.id} {act.title}</div><div className="text-[12px] text-gray-600 mt-1">Investigation ID <b>#{act.id}</b> · reference media <b className="font-mono">{act.reference_id}</b></div><Link to="/graph" className="btn btn-navy mt-3">Open relationship analysis</Link></>
          : <><div className="font-bold text-navy">No active investigation</div><div className="text-[12px] text-gray-600 mt-1">The graph pages use the demo family <b className="font-mono">RW-CMN-P10491224</b> until a case is opened.</div><Link to="/investigations" className="btn btn-primary mt-3">Open a case file</Link></>}</div>
      <div className="card p-4 border-l-4 !border-l-[#2FA36B]"><div className="label-cap !text-slate-500">Data holdings (loaded from the repository)</div>
        <div className="text-[12.5px] mt-1 leading-6"><b>{f(d.local_files)}</b> local reference videos · <b>{f(d.variants_passed)}</b> validated variants<br /><b>{f(d.edges)}</b> relationship records · <b>{f(d.evidence)}</b> evidence records<br /><b>{d.families}</b> source families</div></div>
      <div className="card p-4 border-l-4 !border-l-steel"><div className="label-cap !text-slate-500">Processing queue</div>
        <div className="text-[12.5px] mt-1 leading-6">No background jobs. The demo has no processing queue: uploads are checked with FFprobe when sent, and features come from precomputed files, so there is nothing to animate here.</div></div></div>
    <div className="grid grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-3">
      <Stat label="Media records" value={f(d.media_records)} sub={`from ${d.datasets} source datasets (metadata)`} /><Stat label="Local media files" value={f(d.local_files)} sub={`${d.commons_local} Commons + ${d.anakin_local} ANAKIN videos`} c="#E86A16" />
      <Stat label="Validated variants" value={f(d.variants_passed)} sub="controlled FFmpeg edits (2 more failed)" /><Stat label="Labelled pairs" value={f(d.pairs)} sub={`${f(d.pairs_in_splits)} usable in split-v2`} />
      <Stat label="Relationship edges" value={f(d.edges)} sub={`${f(d.edges_local)} with media on disk`} /><Stat label="Evidence records" value={f(d.evidence)} sub="evidence ledger" c="#E86A16" />
      <Stat label="Platform observations" value={f(d.observations)} sub="no coordination assessed" /><Stat label="Source families" value={d.families} sub="split units" /><Stat label="Candidate clusters" value={d.clusters} sub="needs account + time data" c="#6B7280" />
      <Stat label="Investigations" value={d.investigations} sub="in this application" /><Stat label="Review decisions" value={d.reviews} sub="made in this application" /><Stat label="Data folder" value={`${d.data_gb} GB`} sub={`of ${d.budget_gb} GB budget`} /></div>
    <div className="grid lg:grid-cols-2 gap-4">
      <Card title="Labelled pairs by relationship class"><ResponsiveContainer height={260}><BarChart data={cls} layout="vertical" margin={{ left: 70 }}><CartesianGrid horizontal={false} stroke="#eee" /><XAxis type="number" /><YAxis type="category" dataKey="name" width={170} tick={{ fontSize: 11 }} /><Tooltip /><Bar dataKey="n" fill="#252C5C" radius={4} /></BarChart></ResponsiveContainer></Card>
      <Card title="Controlled variants by transformation"><ResponsiveContainer height={260}><BarChart data={tr} margin={{ bottom: 50 }}><CartesianGrid vertical={false} stroke="#eee" /><XAxis dataKey="name" interval={0} angle={-35} textAnchor="end" tick={{ fontSize: 10 }} /><YAxis /><Tooltip /><Bar dataKey="n" fill="#E86A16" radius={4} /></BarChart></ResponsiveContainer></Card>
      <Card title="Records in tables vs files on disk, by source dataset"><ResponsiveContainer height={260}><BarChart data={ds}><CartesianGrid vertical={false} stroke="#eee" /><XAxis dataKey="name" tick={{ fontSize: 11 }} /><YAxis scale="sqrt" /><Tooltip /><Legend /><Bar dataKey="records" fill="#252C5C" name="records in tables" /><Bar dataKey="local" fill="#E86A16" name="local media files" /></BarChart></ResponsiveContainer>
        <div className="text-[11px] text-gray-500">Square-root scale. Record counts, downloaded media and local files are different quantities; FIVR, VCSL, FVC and COVID are metadata only.</div></Card>
      <Card title="Evidence ledger by type"><div className="flex items-center"><ResponsiveContainer height={240} width="55%"><PieChart><Pie data={ev} dataKey="value" nameKey="name" outerRadius={90} innerRadius={45}>{ev.map((_, i) => <Cell key={i} fill={COL[i % COL.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer>
        <ul className="text-[12px] space-y-1">{ev.map((e, i) => <li key={i}><i className="inline-block w-2.5 h-2.5 rounded-full mr-1.5" style={{ background: COL[i % COL.length] }} />{e.name}: <b>{f(e.value as number)}</b></li>)}</ul></div></Card></div>
    <div className="grid lg:grid-cols-3 gap-4">
      <Card title="Baseline experiment results" right={<Link to="/evaluation" className="text-accent text-xs font-semibold">Open evaluation</Link>}><table className="t"><tbody>{d.experiments.map((e: any) => <tr key={e.experiment_id}><td>{e.metric_name.replace(/_/g, ' ')}</td><td className="font-bold">{e.metric_value}</td></tr>)}</tbody></table><div className="text-[11px] text-gray-500 mt-2">BASE-DHASH-v1: non-learned baseline, not the ORVEX model.</div></Card>
      <Card title="Dataset quality indicators" right={<Link to="/quality" className="text-accent text-xs font-semibold">Open quality</Link>}>{q ? <ul className="text-[12.5px] space-y-1.5">
        <li>Acceptance checks passing: <b>{q.checks.filter((c: any) => c.ok).length} / {q.checks.length}</b></li><li>Tests: <b>{q.pytest}</b></li><li>Missing local media files: <b>{q.missing_natural + q.missing_variant}</b></li><li>Dangling relationship references: <b>{f(q.dangling_edges)}</b></li>
        <li>dHash features: <b>{q.hashes}</b> / {q.local_files} local files; OCR, ASR, embeddings: <b>0</b></li></ul> : <Loading loading />}</Card>
      <Card title="Recent investigator activity">{d.activity.length ? <ul className="text-[12px] space-y-2">{d.activity.map((a: any, i: number) => <li key={i}><b>{a.actor}</b> {a.action}<div className="text-gray-500 text-[11px]">{a.ts}{a.inv_id ? ` · investigation #${a.inv_id}` : ''}</div></li>)}</ul>
        : <Note>No investigator activity yet. Create an investigation or review a graph edge and it appears here.</Note>}<Link to="/investigations" className="btn btn-primary mt-3">Start an investigation</Link></Card></div></div>
}
