import { useEffect, useRef, useState } from 'react'
import type { ReactNode } from 'react'
import { useLocation } from 'react-router-dom'
import { ChevronDown } from 'lucide-react'
import { api } from './api'
import { SECTION } from './nav'

export const prefersReducedMotion = () => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches

/** Counts up to a real, already-loaded number (once, ~0.8 s). Shows the final value immediately when motion is reduced. */
export function CountUp({ to }: { to: number }) {
  const [v, setV] = useState(prefersReducedMotion() ? to : 0)
  useEffect(() => {
    if (prefersReducedMotion()) { setV(to); return }
    let raf = 0; const t0 = performance.now(); const tick = (t: number) => { const k = Math.min((t - t0) / 800, 1); setV(Math.round(to * (1 - Math.pow(1 - k, 3)))); if (k < 1) raf = requestAnimationFrame(tick) }
    raf = requestAnimationFrame(tick); return () => cancelAnimationFrame(raf)
  }, [to])
  return <>{v.toLocaleString()}</>
}
const animatable = (v: ReactNode): number | null => { if (typeof v === 'number') return v; if (typeof v === 'string' && /^\d{1,3}(,\d{3})*$|^\d+$/.test(v)) return parseInt(v.replace(/,/g, ''), 10); return null }

export const Card = ({ title, children, right, className = '' }: { title?: ReactNode; children: ReactNode; right?: ReactNode; className?: string }) => (
  <div className={'card p-4 ' + className}>{title && <div className="flex items-center justify-between mb-3"><h3 className="font-bold text-[15px]">{title}</h3>{right}</div>}{children}</div>)
export const Badge = ({ c = '#6B7280', children }: { c?: string; children: ReactNode }) => <span style={{ background: c + '1f', color: c, border: `1px solid ${c}55` }} className="px-2 py-0.5 rounded-full text-[11px] font-semibold whitespace-nowrap">{children}</span>
export const Stat = ({ label, value, sub, c = '#14233B' }: { label: string; value: ReactNode; sub?: string; c?: string }) => { const n = animatable(value); return (
  <div className="card lift p-4"><div className="text-[10.5px] uppercase tracking-[.12em] text-gray-500 font-semibold">{label}</div><div className="text-2xl font-extrabold" style={{ color: c }}>{n != null ? <CountUp to={n} /> : value}</div>{sub && <div className="text-[11px] text-gray-500 mt-1">{sub}</div>}</div>) }
export const Note = ({ children, kind = 'info' }: { children: ReactNode; kind?: 'info' | 'warn' }) => (
  <div className={'text-[12px] rounded-md px-3 py-2 border ' + (kind === 'warn' ? 'bg-orange-50 border-orange-200 text-orange-900' : 'bg-blue-50 border-blue-200 text-blue-900')}>{children}</div>)
export function useApi<T = any>(path: string | null, params?: any, deps: any[] = []) {
  const [d, setD] = useState<T | null>(null); const [err, setErr] = useState(''); const [loading, setL] = useState(!!path)
  useEffect(() => { if (!path) return; let ok = true; setL(true); api<T>(path, { params }).then(x => { if (ok) { setD(x); setErr('') } }).catch(e => ok && setErr(e.message)).finally(() => ok && setL(false)); return () => { ok = false } },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [path, JSON.stringify(params), ...deps])
  return { d, err, loading }
}
/** Shown only while a request is really in flight (scan bar) or after it really failed. */
export const Loading = ({ err, loading }: { err?: string; loading?: boolean }) => err ? <Note kind="warn">Could not load: {err}</Note> : loading ? <div role="status" className="p-6 text-sm text-gray-500"><div className="scan-track mb-2"><i /></div>Retrieving real records…</div> : null
export const PageTitle = ({ title, sub, right }: { title: string; sub?: ReactNode; right?: ReactNode }) => { const loc = useLocation(); const sec = SECTION['/' + loc.pathname.split('/')[1]] ; return (
  <div className="flex items-end justify-between mb-4"><div>{sec && <div className="eyebrow">{sec}</div>}<h1 className="text-2xl font-extrabold text-navy">{title}</h1>{sub && <p className="text-[13px] text-gray-600 mt-1 max-w-3xl">{sub}</p>}</div>{right}</div>) }
export const Thumb = ({ id, t = 1, w = 240, className = '' }: { id: string; t?: number; w?: number; className?: string }) =>
  <img loading="lazy" src={`/api/media/${id}/frame?t=${t}&w=${w}`} className={'object-cover bg-gray-200 ' + className} onError={e => ((e.target as HTMLImageElement).style.opacity = '0.2')} />
/** Expand / collapse section with a smooth height animation. */
export function Collapsible({ title, children, open: o = true, badge }: { title: ReactNode; children: ReactNode; open?: boolean; badge?: ReactNode }) {
  const [open, setOpen] = useState(o); const id = useRef('c' + Math.random().toString(36).slice(2, 7)).current
  return <div className="mt-3 border-t border-line pt-2"><button type="button" aria-expanded={open} aria-controls={id} onClick={() => setOpen(!open)} className="w-full flex items-center gap-2 text-left font-bold text-[12.5px] text-navy"><ChevronDown size={14} className={'transition-transform ' + (open ? '' : '-rotate-90')} />{title}{badge}</button>
    <div id={id} className={'collapse-body ' + (open ? 'open' : '')}><div className="overflow-hidden">{children}</div></div></div>
}
export function useActive() {   // active investigation, kept in localStorage
  const [v, setV] = useState<any>(() => JSON.parse(localStorage.getItem('orvex_active') || 'null'))
  useEffect(() => { const f = () => setV(JSON.parse(localStorage.getItem('orvex_active') || 'null')); window.addEventListener('orvex_active', f); return () => window.removeEventListener('orvex_active', f) }, [])
  return [v, (x: any) => { localStorage.setItem('orvex_active', JSON.stringify(x)); window.dispatchEvent(new Event('orvex_active')) }] as const
}
export const DEFAULT_ROOT = 'RW-CMN-P10491224'
export function useRoot() { const [a, setA] = useActive(); const root = a?.root || DEFAULT_ROOT; return [root, (r: string) => setA({ ...(a || {}), root: r, reference_id: r })] as const }
export function FamilyPicker({ root, onPick }: { root: string; onPick: (r: string) => void }) {
  const { d } = useApi<any[]>('/families')
  return <select className="inp !w-auto max-w-[420px]" value={root} onChange={e => onPick(e.target.value)}>{(d || []).slice(0, 60).map(f => <option key={f.root} value={f.root}>{f.root} · {f.n_variants} variants · depth {f.max_depth} · {f.title.replace('File:', '').slice(0, 34)}</option>)}</select>
}
