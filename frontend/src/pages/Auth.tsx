import { useState } from 'react'
import type { ReactNode } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../api'
import { Note } from '../ui'

function Frame({ title, sub, children }: { title: string; sub: string; children: ReactNode }) {
  return <div className="min-h-full grid md:grid-cols-[1.1fr_1fr] bg-white">
    <div className="hidden md:flex flex-col justify-between bg-navy text-white p-12">
      <div><div className="text-3xl font-extrabold tracking-wide">ORVEX</div><div className="text-white/70 text-sm">Origin and Relationship Verification Explorer</div></div>
      <div><div className="text-4xl font-extrabold leading-tight">Trace the Origin.<br /><span className="text-accent">Reveal the Connections.</span></div>
        <p className="mt-5 text-white/75 max-w-md text-[15px]">An investigation platform for finding how videos are connected: copies, edits and re-uploads, with the evidence behind every relationship.</p></div>
      <div className="text-[12px] text-white/55 max-w-md">Similarity is not proof of derivation, and derivation is not proof of coordination. ORVEX supports investigators; it does not declare anyone guilty.</div>
    </div>
    <div className="grid place-items-center p-8"><div className="w-full max-w-sm"><h1 className="text-2xl font-extrabold text-navy">{title}</h1><p className="text-sm text-gray-600 mb-5">{sub}</p>{children}</div></div></div>
}
const useForm = (init: any) => { const [f, set] = useState(init); return [f, (k: string) => (e: any) => set({ ...f, [k]: e.target.value })] as const }
export function Login({ onUser }: { onUser: (u: any) => void }) {
  const [f, h] = useForm({ email: 'demo.investigator@orvex.local', password: 'OrvexDemo!2026' }); const [err, setErr] = useState(''); const nav = useNavigate()
  const go = async (e: any) => { e.preventDefault(); try { const r = await api('/auth/login', { method: 'POST', body: f }); localStorage.setItem('orvex_token', r.token); onUser(r.user); nav('/') } catch (x: any) { setErr(x.message) } }
  return <Frame title="Investigator sign in" sub="Use your investigator account.">
    <form onSubmit={go} className="space-y-3"><label className="text-xs font-semibold">E-mail<input className="inp mt-1" value={f.email} onChange={h('email')} /></label>
      <label className="text-xs font-semibold">Password<input type="password" className="inp mt-1" value={f.password} onChange={h('password')} /></label>
      {err && <Note kind="warn">{err}</Note>}<button className="btn btn-primary w-full justify-center">Sign in</button></form>
    <div className="flex justify-between text-sm mt-3"><Link className="text-accent font-semibold" to="/register">Create account</Link><Link className="text-gray-600" to="/forgot">Forgot password?</Link></div>
    <div className="mt-6"><Note>Demo accounts are pre-filled: <b>demo.investigator@orvex.local</b> (admin) and <b>demo.reviewer@orvex.local</b> (reviewer), password <b>OrvexDemo!2026</b>. They exist only in the local SQLite database.</Note></div></Frame>
}
export function Register({ onUser }: { onUser: (u: any) => void }) {
  const [f, h] = useForm({ name: '', email: '', password: '' }); const [err, setErr] = useState(''); const nav = useNavigate()
  const go = async (e: any) => { e.preventDefault(); try { const r = await api('/auth/register', { method: 'POST', body: f }); localStorage.setItem('orvex_token', r.token); onUser(r.user); nav('/') } catch (x: any) { setErr(x.message) } }
  return <Frame title="Register as an investigator" sub="New accounts get the investigator role; an admin can change roles.">
    <form onSubmit={go} className="space-y-3"><input className="inp" placeholder="Full name" value={f.name} onChange={h('name')} /><input className="inp" placeholder="E-mail" value={f.email} onChange={h('email')} />
      <input type="password" className="inp" placeholder="Password (8+ characters)" value={f.password} onChange={h('password')} />{err && <Note kind="warn">{err}</Note>}<button className="btn btn-primary w-full justify-center">Create account</button></form>
    <div className="text-sm mt-3"><Link className="text-accent font-semibold" to="/login">Back to sign in</Link></div></Frame>
}
export function Forgot() {
  const [email, setE] = useState(''); const [r, setR] = useState<any>(null)
  return <Frame title="Forgot password" sub="Enter your e-mail to receive a reset token.">
    <form onSubmit={async e => { e.preventDefault(); setR(await api('/auth/forgot', { method: 'POST', body: { email } })) }} className="space-y-3"><input className="inp" placeholder="E-mail" value={email} onChange={e => setE(e.target.value)} /><button className="btn btn-primary w-full justify-center">Send reset token</button></form>
    {r && <div className="mt-3 space-y-2"><Note>{r.note}</Note>{r.demo_token && <Link className="btn btn-navy" to={`/reset?token=${r.demo_token}`}>Continue to reset</Link>}</div>}
    <div className="text-sm mt-3"><Link className="text-accent font-semibold" to="/login">Back to sign in</Link></div></Frame>
}
export function ResetPw() {
  const [sp] = useSearchParams(); const [f, h] = useForm({ token: sp.get('token') || '', password: '' }); const [msg, setM] = useState(''); const nav = useNavigate()
  return <Frame title="Reset password" sub="Choose a new password (8+ characters).">
    <form onSubmit={async e => { e.preventDefault(); try { await api('/auth/reset', { method: 'POST', body: f }); setM('Password changed.'); setTimeout(() => nav('/login'), 900) } catch (x: any) { setM(x.message) } }} className="space-y-3">
      <input className="inp" placeholder="Reset token" value={f.token} onChange={h('token')} /><input type="password" className="inp" placeholder="New password" value={f.password} onChange={h('password')} />
      {msg && <Note>{msg}</Note>}<button className="btn btn-primary w-full justify-center">Change password</button></form></Frame>
}
