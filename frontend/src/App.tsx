import { createContext, useContext, useEffect, useRef, useState } from 'react'
import { BrowserRouter, NavLink, Navigate, Outlet, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import { LogOut, Bell, ScanEye, Lock, ChevronDown } from 'lucide-react'
import { api, tok } from './api'
import { useActive, useApi } from './ui'
import { NAV, TITLES } from './nav'
import Ambient from './Ambient'
import { Login, Register, Forgot, ResetPw } from './pages/Auth'
import Dashboard from './pages/Dashboard'
import { Investigations, InvestigationDetail } from './pages/Investigations'
import Candidates from './pages/Candidates'
import Graph from './pages/Graph'
import { Compare, Provenance, Manipulation } from './pages/Analysis'
import Distribution from './pages/Distribution'
import Evidence from './pages/Evidence'
import { Datasets, Variants, Quality } from './pages/Data'
import { ModelLab, Evaluation } from './pages/Models'
import Report from './pages/Report'
import Admin from './pages/Admin'

const Ctx = createContext<any>(null)
export const useUser = () => useContext(Ctx)

/** Notification bell. Entries are real rows of the application history table (reviews, investigations created/updated) from /api/summary. */
function Notifications() {
  const { d } = useApi<any>(tok() ? '/summary' : null); const [open, setOpen] = useState(false); const [seen, setSeen] = useState(() => localStorage.getItem('orvex_seen') || ''); const box = useRef<HTMLDivElement>(null)
  const items: any[] = d?.activity || []; const unread = items.filter(x => x.ts > seen).length
  useEffect(() => {
    if (!open) return
    const off = (e: MouseEvent) => { if (!box.current?.contains(e.target as Node)) setOpen(false) }; const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false) }
    document.addEventListener('mousedown', off); document.addEventListener('keydown', esc); return () => { document.removeEventListener('mousedown', off); document.removeEventListener('keydown', esc) }
  }, [open])
  const toggle = () => { setOpen(!open); if (!open && items[0]) { localStorage.setItem('orvex_seen', items[0].ts); setSeen(items[0].ts) } }
  return <div ref={box} className="relative"><button type="button" onClick={toggle} aria-label={`Notifications (${unread} new)`} aria-expanded={open} className="relative grid place-items-center w-9 h-9 rounded border border-white/15 hover:bg-white/10"><Bell size={17} />{unread > 0 && <i className="absolute -top-1 -right-1 min-w-[16px] h-4 px-1 rounded-full bg-evidence text-white text-[10px] not-italic font-bold grid place-items-center">{unread}</i>}</button>
    {open && <div role="menu" className="absolute right-0 top-11 w-[340px] z-50 card text-ink p-3 text-[12px]"><div className="font-bold text-navy mb-2">Investigation activity</div>
      {items.length ? <ul className="space-y-2">{items.map((x, i) => <li key={i} className="border-l-2 border-accent pl-2"><b>{x.actor}</b> {x.action}<div className="text-gray-500 text-[11px]">{x.ts}{x.inv_id ? ` · investigation #${x.inv_id}` : ''}</div></li>)}</ul> : <div className="text-gray-500">No activity recorded yet. Review decisions and investigation changes appear here.</div>}</div>}</div>
}

function Shell() {
  const u = useUser(); const nav = useNavigate(); const loc = useLocation(); const [act] = useActive()
  const [shut, setShut] = useState<Record<string, boolean>>(() => { try { return JSON.parse(localStorage.getItem('orvex_nav_closed') || '{}') } catch { return {} } })
  const flip = (g: string) => setShut(s => { const n = { ...s, [g]: !s[g] }; try { localStorage.setItem('orvex_nav_closed', JSON.stringify(n)) } catch { /* ignore */ } return n })
  if (!tok()) return <Navigate to="/login" />
  const title = TITLES[loc.pathname] || (loc.pathname.startsWith('/investigations/') ? 'Investigation workspace' : '')
  return <div className="h-full flex">
    <aside className="sidebar w-[240px] shrink-0 text-white flex flex-col overflow-y-auto border-r border-black/50" aria-label="Main navigation">
      <div className="side-brand px-[18px] py-4 flex items-center gap-3 border-b border-white/10"><div className="w-9 h-9 rounded bg-accent/15 border border-accent/60 grid place-items-center text-accent"><ScanEye size={20} /></div>
        <div className="text-xl font-extrabold tracking-[.18em] leading-none">ORVEX<span className="block text-[9px] font-medium text-[#8FA3C0] tracking-normal mt-1">Trace the Origin. Reveal the Connections.</span></div></div>
      <div className="px-[18px] py-2 text-[10px] tracking-[.18em] text-[#8FA3C0] uppercase border-b border-white/10 flex items-center gap-1.5"><Lock size={11} />Video forensics workstation</div>
      {NAV.map(([g, items]) => <div key={g} className="mb-0.5"><button type="button" className="side-grp" aria-expanded={!shut[g]} onClick={() => flip(g)}>{g}<ChevronDown size={12} className={'transition-transform ' + (shut[g] ? '-rotate-90' : '')} /></button>
        <div className={'side-body ' + (shut[g] ? 'closed' : '')}><div>{items.map(([p, n, Icon]) => <NavLink key={p} to={p} end={p === '/'} className={({ isActive }) => 'side-link' + (isActive ? ' on' : '')}><Icon size={16} />{n}</NavLink>)}</div></div></div>)}
      <div className="mt-auto p-4 text-[10px] text-[#8FA3C0] border-t border-white/10">Data: repository snapshot 2026-10-26. Ground-truth lineage and dHash measurements; no trained ORVEX model. Independent research tool, not an official or government system.</div>
    </aside>
    <div className="flex-1 min-w-0 flex flex-col workspace">
      <Ambient />
      <header className="topbar h-14 text-white flex items-center px-6 gap-4 shrink-0 mb-[2px]">
        <div><div className="label-cap">Section</div><div className="font-bold tracking-wide uppercase text-[14px] leading-none">{title}</div></div>
        <div className="flex-1 border-l border-white/20 pl-4 text-[12px] text-[#C3D0E4] flex items-center gap-5 min-w-0">
          <div className="min-w-0"><div className="label-cap">Case file</div>{act?.id ? <b className="text-white truncate block">#{act.id} {act.title}</b> : <span className="truncate block">none active · demo family <b className="text-white">RW-CMN-P10491224</b></span>}</div>
          {act?.id && <div><div className="label-cap">Investigation ID</div><b className="text-white">#{act.id}</b></div>}
          <div className="min-w-0"><div className="label-cap">Reference media</div><b className="text-white font-mono text-[11.5px]">{act?.reference_id || act?.root || 'RW-CMN-P10491224'}</b></div></div>
        <span className="hidden xl:flex items-center gap-2 text-[11px] text-[#9FB2CC]"><i className="pulse-dot" />Session active</span>
        <Notifications />
        <div className="flex items-center gap-2 text-[13px]"><div className="w-8 h-8 rounded-full bg-accent text-white grid place-items-center font-bold">{(u?.name || '?')[0]}</div><div className="leading-tight"><div className="font-semibold">{u?.name}</div><div className="text-[11px] text-[#9FB2CC]">{u?.role}</div></div></div>
        <button className="btn !bg-transparent !text-white !border-white/25 hover:!bg-white/10" onClick={() => { localStorage.removeItem('orvex_token'); nav('/login') }}><LogOut size={14} />Sign out</button>
      </header>
      <main className="flex-1 overflow-auto p-5"><div key={loc.pathname} className="page-enter"><Outlet /></div></main>
    </div></div>
}

export default function App() {
  const [user, setUser] = useState<any>(() => JSON.parse(localStorage.getItem('orvex_user') || 'null'))
  useEffect(() => { if (tok()) api('/auth/users').catch(() => { }) }, [])
  const set = (u: any) => { localStorage.setItem('orvex_user', JSON.stringify(u)); setUser(u) }
  return <Ctx.Provider value={{ ...user, setUser: set }}><BrowserRouter><Routes>
    <Route path="/login" element={<Login onUser={set} />} /><Route path="/register" element={<Register onUser={set} />} /><Route path="/forgot" element={<Forgot />} /><Route path="/reset" element={<ResetPw />} />
    <Route element={<Shell />}>
      <Route path="/" element={<Dashboard />} /><Route path="/investigations" element={<Investigations />} /><Route path="/investigations/:id" element={<InvestigationDetail />} />
      <Route path="/candidates" element={<Candidates />} /><Route path="/graph" element={<Graph />} /><Route path="/compare" element={<Compare />} /><Route path="/provenance" element={<Provenance />} />
      <Route path="/manipulation" element={<Manipulation />} /><Route path="/distribution" element={<Distribution />} /><Route path="/evidence" element={<Evidence />} />
      <Route path="/datasets" element={<Datasets />} /><Route path="/variants" element={<Variants />} /><Route path="/quality" element={<Quality />} />
      <Route path="/models" element={<ModelLab />} /><Route path="/evaluation" element={<Evaluation />} /><Route path="/report" element={<Report />} /><Route path="/admin" element={<Admin />} />
    </Route></Routes></BrowserRouter></Ctx.Provider>
}
