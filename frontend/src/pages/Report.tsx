import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Download } from 'lucide-react'
import { tok, frame } from '../api'
import { Card, Loading, Note, PageTitle, useActive, useApi } from '../ui'

const SECTIONS = ['Investigation information', 'Reference video', 'Candidate videos', 'Relationship graph', 'Media provenance', 'Video comparison', 'Transformation findings', 'Evidence ledger', 'Distribution timeline', 'Campaign-analysis findings', 'Investigator observations', 'Uncertainty and limitations', 'Final investigator conclusion']
export default function Report() {
  const { d, err, loading } = useApi<any[]>('/investigations'); const [act, setAct] = useActive(); const [pick, setPick] = useState<number>(act?.id || 0); const id = pick || d?.[0]?.id
  const { d: inv } = useApi<any>(id ? '/investigations/' + id : null); const [busy, setBusy] = useState(false)
  const dl = async () => { setBusy(true); const r = await fetch(`/api/report/${id}?token=${tok()}`); const b = await r.blob(); const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = `ORVEX_investigation_${id}.pdf`; a.click(); setBusy(false) }
  if (!d) return <Loading err={err} loading={loading} />
  return <div className="space-y-4"><PageTitle title="Investigation report" sub="A structured report built from the selected investigation’s real records: reference video, graph, provenance, measurements, evidence, reviews and limitations." right={id && <button className="btn btn-primary" onClick={dl} disabled={busy}><Download size={15} />{busy ? 'Building PDF…' : 'Download PDF'}</button>} />
    {!d.length ? <Card><Note>No investigation exists yet. <Link className="text-accent font-semibold" to="/investigations">Create one</Link> and its report can be generated here.</Note></Card> :
      <div className="grid lg:grid-cols-[260px_1fr] gap-4"><Card title="Investigation"><select className="inp" value={id} onChange={e => { setPick(+e.target.value); setAct({ id: +e.target.value }) }}>{d.map(i => <option key={i.id} value={i.id}>#{i.id} {i.title}</option>)}</select>
        <ol className="mt-3 text-[12.5px] space-y-1.5 list-decimal ml-5">{SECTIONS.map(s => <li key={s}>{s}</li>)}</ol></Card>
        {inv && <div className="card p-8 max-w-4xl bg-white"><div className="text-[11px] tracking-widest text-accent font-bold">ORVEX · INVESTIGATION REPORT</div><h2 className="text-2xl font-extrabold text-navy mt-1">#{inv.id} {inv.title}</h2><div className="text-[12px] text-gray-500">Opened {inv.created} by {inv.owner} · status {inv.status}</div>
          <h3 className="font-bold mt-5 text-navy">1–2. Reference video</h3><div className="flex gap-4 mt-2"><img src={frame(inv.reference_id, 1, 480)} className="w-72 rounded-lg" /><div className="text-[13px]">Reference <b>{inv.reference_id}</b>.<br />The PDF adds the candidate table, relationship graph, provenance, comparison measurements, transformation findings and the evidence ledger rows linked to the graph.</div></div>
          <h3 className="font-bold mt-5 text-navy">11. Investigator observations</h3>{inv.reviews.length ? <ul className="text-[13px] list-disc ml-5">{inv.reviews.map((r: any) => <li key={r.id}><b>{r.decision}</b> {r.edge_key}: {r.note || '(no note)'}</li>)}</ul> : <p className="text-[13px] text-gray-600">No review decisions yet; review edges in the relationship graph to include them.</p>}
          <h3 className="font-bold mt-5 text-navy">12. Uncertainty and limitations</h3><p className="text-[13px]">Relationships come from the controlled transformation log (certain by construction for these variants). The only measured detector is the non-learned dHash baseline. No trained model, OCR, speech or embedding evidence exists. Similarity is not proof of derivation, and derivation is not proof of coordination.</p>
          <h3 className="font-bold mt-5 text-navy">13. Final investigator conclusion</h3><p className="text-[13px]">{inv.summary || <i className="text-gray-500">No conclusion recorded. Add one in the investigation workspace.</i>}</p></div>}</div>}</div>
}
