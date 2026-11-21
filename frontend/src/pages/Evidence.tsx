import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../api'
import { Badge, Card, Loading, Note, PageTitle, Thumb, useApi } from '../ui'

export default function Evidence() {
  const [sp] = useSearchParams(); const [q, setQ] = useState(''); const [type, setType] = useState(''); const [subject, setSubject] = useState(sp.get('subject') || ''); const [page, setPage] = useState(0)
  const { d, err, loading } = useApi<any>('/evidence', { q, type, subject, limit: 30, offset: page * 30 }); const [sel, setSel] = useState(sp.get('id') || ''); const [tick, setTick] = useState(0)
  const { d: one } = useApi<any>(sel ? '/evidence/' + sel : null, undefined, [tick]); const [note, setNote] = useState(''); const [dec, setDec] = useState('note')
  useEffect(() => setPage(0), [q, type, subject])
  const add = async () => { await api('/reviews', { method: 'POST', body: { edge_key: sel, decision: dec, note, evidence_ids: [sel] } }); setNote(''); setTick(tick + 1) }
  return <div className="space-y-4"><PageTitle title="Evidence ledger" sub="Every claim the dataset makes about a video, relationship or right is a ledger row with its source, method and verification status. Open a record, trace it to the media and relationships it supports, and add review notes." />
    <div className="grid lg:grid-cols-[1fr_420px] gap-4"><div className="card p-3"><div className="flex gap-2 mb-2 flex-wrap"><input className="inp !w-52" placeholder="Search claim or ID" value={q} onChange={e => setQ(e.target.value)} /><input className="inp !w-52" placeholder="Related media ID" value={subject} onChange={e => setSubject(e.target.value)} />
      <select className="inp !w-56" value={type} onChange={e => setType(e.target.value)}><option value="">All evidence types</option>{Object.entries(d?.types || {}).map(([k, v]) => <option key={k} value={k}>{k} ({String(v)})</option>)}</select></div>
      <Loading err={err} loading={loading && !d} />
      {d && <><div className="text-xs text-gray-500 mb-1">{d.total.toLocaleString()} records</div><div className="max-h-[68vh] overflow-auto"><table className="t"><thead><tr><th>Evidence ID</th><th>Related media</th><th>Type</th><th>Claim supported</th><th>Status</th><th>Reviewer</th></tr></thead><tbody>{d.items.map((r: any) => <tr key={r.evidence_id} className={sel === r.evidence_id ? 'sel' : ''} onClick={() => setSel(r.evidence_id)}>
        <td className="font-mono text-[11px]">{r.evidence_id}</td><td className="font-mono text-[11px]">{r.subject_id}</td><td>{r.evidence_type}</td><td>{r.claim_supported}</td><td><Badge c="#2563EB">{r.claim_status}</Badge></td><td>{r.reviewer_status}</td></tr>)}</tbody></table></div>
        <div className="flex gap-2 mt-2"><button className="btn" disabled={!page} onClick={() => setPage(page - 1)}>Previous</button><button className="btn" disabled={(page + 1) * 30 >= d.total} onClick={() => setPage(page + 1)}>Next</button></div></>}</div>
      <Card title={sel ? `Evidence ${sel}` : 'Evidence details'}>{!sel ? <Note>Select a ledger row to inspect it.</Note> : !one ? <Loading loading /> : <div className="space-y-2 text-[12.5px]">
        {one.subject?.path && <Thumb id={one.subject.id} w={480} className="w-full aspect-video rounded-lg" />}
        <table className="t"><tbody>{[['Type', one.record.evidence_type], ['Claim', one.record.claim_supported], ['Fact or inference', one.record.observed_fact_vs_inference], ['Source record', one.record.source_record_ref], ['Verification method', one.record.verification_method], ['Time', `${one.record.evidence_time_utc} (${one.record.temporal_precision})`], ['File SHA-256', one.record.file_sha256 || '–'], ['Permission', one.record.permission_status], ['Confidence basis', one.record.confidence_basis], ['Limitations', one.record.limitations || '–']].map(r => <tr key={r[0]}><td className="font-semibold w-36">{r[0]}</td><td className="break-words">{r[1]}</td></tr>)}</tbody></table>
        {one.record.source_url && <a className="text-accent font-semibold" target="_blank" href={one.record.source_url}>Source URL</a>}
        {one.edges.length > 0 && <><div className="font-bold">Relationship edges backed by this evidence</div>{one.edges.map((e: any) => <div key={e.relationship_id} className="text-[11.5px] border-l-2 border-accent pl-2">{e.relationship_id}: {e.normalized_relation_type} ({e.media_a_id.slice(-10)} → {e.media_b_id.slice(-10)})</div>)}</>}
        <div className="font-bold pt-2">Review history</div>{one.reviews.length ? one.reviews.map((r: any) => <div key={r.id} className="text-[11.5px]"><Badge>{r.decision}</Badge> {r.note} <span className="text-gray-500">{r.actor} · {r.ts}</span></div>) : <div className="text-gray-500">No review notes yet.</div>}
        <div className="flex gap-1"><select className="inp !w-32" value={dec} onChange={e => setDec(e.target.value)}>{['note', 'accepted', 'uncertain', 'rejected'].map(x => <option key={x}>{x}</option>)}</select><input className="inp" placeholder="Review note" value={note} onChange={e => setNote(e.target.value)} /><button className="btn btn-primary" disabled={!note} onClick={add}>Add</button></div></div>}</Card></div></div>
}
