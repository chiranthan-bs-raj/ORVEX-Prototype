import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { frame, mmss, ROLE, TLABEL } from '../api'
import { Badge, FamilyPicker, Loading, Note, PageTitle, useApi, useRoot } from '../ui'

export default function Candidates() {
  const [root, setRoot] = useRoot(); const { d, err, loading } = useApi<any>('/graph/' + root, { all: true }); const [q, setQ] = useState(''); const [role, setRole] = useState(''); const [tr, setTr] = useState('')
  const rows = useMemo(() => (d?.nodes || []).filter((n: any) => n.role !== 'reference').filter((n: any) => (!role || n.role === role) && (!tr || n.transformation === tr) && (!q || (n.id + (n.transformation || '')).toLowerCase().includes(q.toLowerCase()))), [d, q, role, tr])
  const edge = (id: string) => d.edges.find((e: any) => e.target === id)
  const ref = d?.nodes.find((n: any) => n.role === 'reference'); const trs = [...new Set((d?.nodes || []).map((n: any) => n.transformation).filter(Boolean))] as string[]
  return <div className="space-y-4"><PageTitle title="Candidate discovery" sub="Candidates for the reference video, taken from the real records of its source family: every controlled variant (ground truth) plus a sampled unrelated video. Features are measured values, not model scores." right={<FamilyPicker root={root} onPick={setRoot} />} />
    <Loading err={err} loading={loading && !d} />
    {d && <div className="grid lg:grid-cols-[300px_1fr] gap-4"><div className="card p-3 h-fit"><div className="font-bold mb-2">Selected reference video</div><img src={frame(ref.id, 1, 480)} className="w-full rounded-lg aspect-video object-cover" />
      <div className="text-[12px] leading-5 mt-2"><b>{ref.id}</b><br />{ref.title}<br />{ref.source} · {mmss(ref.duration)} · {ref.width}×{ref.height}<br />Published: {ref.published?.slice(0, 10) || 'not recorded'}<br />Licence: {ref.license}</div>
      <div className="mt-3 text-[12px]"><b>{d.total_variants}</b> validated variants exist for this video; {d.nodes.length - 1} are listed.</div></div>
      <div className="card p-3"><div className="flex gap-2 mb-3 flex-wrap"><input className="inp !w-56" placeholder="Search ID or transformation" value={q} onChange={e => setQ(e.target.value)} />
        <select className="inp !w-48" value={role} onChange={e => setRole(e.target.value)}><option value="">All relationship labels</option>{['direct', 'indirect', 'unrelated'].map(r => <option key={r} value={r}>{ROLE[r].name}</option>)}</select>
        <select className="inp !w-52" value={tr} onChange={e => setTr(e.target.value)}><option value="">All transformations</option>{trs.map(t => <option key={t} value={t}>{TLABEL[t] || t}</option>)}</select><span className="text-xs self-center text-gray-500">{rows.length} candidates</span></div>
        <div className="max-h-[70vh] overflow-auto"><table className="t"><thead><tr><th>Video</th><th>Label</th><th>Transformation</th><th>Source</th><th>Duration</th><th>Resolution</th><th>dHash match</th><th>Audio identical</th><th>Evidence</th></tr></thead><tbody>{rows.map((n: any) => { const e = edge(n.id); return <tr key={n.id}>
          <td><div className="flex gap-2 items-center"><img src={frame(n.id, 1, 140)} className="w-16 h-10 object-cover rounded" /><span className="font-mono text-[11px]">{n.id}</span></div></td><td><Badge c={ROLE[n.role].c}>{ROLE[n.role].name}</Badge></td><td>{TLABEL[n.transformation] || (n.role === 'unrelated' ? 'none (negative pair)' : '–')}{n.depth > 1 && <div className="text-[10.5px] text-gray-500">depth {n.depth}</div>}</td>
          <td>{n.source}</td><td>{mmss(n.duration)}</td><td>{n.width}×{n.height}</td><td>{e?.sims?.dhash_match_fraction != null ? (e.sims.dhash_match_fraction * 100).toFixed(0) + '%' : '–'}</td><td>{e?.sims?.audio_md5_identical == null ? '–' : e.sims.audio_md5_identical ? 'yes' : 'no'}</td>
          <td className="text-[11px]">{e?.evidence_ids?.length ? <Link className="text-accent font-semibold" to={`/evidence?id=${e.evidence_ids[0]}`}>{e.evidence_ids[0]}</Link> : e?.label_source}</td></tr> })}</tbody></table></div>
        <div className="mt-2"><Note>“dHash match” is the share of 24 sampled frames with a near-identical frame in the parent (≤8 of 64 bits; rule from scripts/datasets/s9). “Audio identical” compares an 8 kHz audio MD5. No OCR, speech or embedding features exist yet.</Note></div></div></div>}</div>
}
