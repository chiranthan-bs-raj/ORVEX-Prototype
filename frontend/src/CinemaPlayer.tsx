import { useCallback, useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { Play, Pause, Volume2, VolumeX, X } from 'lucide-react'
import { canLockEsc, enterFs, exitFs, fsElement, lockEsc, unlockEsc } from './fs'
import { mmss } from './api'

/** Full-viewport "cinema" video overlay. It is an in-page modal (not a browser-fullscreen video element), so whatever is
 *  underneath, e.g. the expanded relationship graph, stays mounted and unchanged. Esc, the close button and the X close it.
 *  Where Keyboard Lock is available it also asks the browser for real fullscreen. */
export default function CinemaPlayer({ src, poster, id, title, subtitle, startAt = 0, onClose }: { src: string; poster?: string; id: string; title: string; subtitle?: string; startAt?: number; onClose: () => void }) {
  const box = useRef<HTMLDivElement>(null); const vid = useRef<HTMLVideoElement>(null); const entered = useRef(false)
  const [t, setT] = useState(0); const [dur, setDur] = useState(0); const [playing, setPlaying] = useState(false); const [muted, setMuted] = useState(false); const [vol, setVol] = useState(1); const [err, setErr] = useState('')
  const close = useCallback(() => { onClose() }, [onClose])
  useEffect(() => {
    const el = box.current!; el.focus()
    if (canLockEsc() && !fsElement()) { entered.current = true; enterFs(el).then(lockEsc).catch(() => { entered.current = false }) }
    const key = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { e.preventDefault(); e.stopImmediatePropagation(); close(); return }
      const tag = (e.target as HTMLElement)?.tagName; const v = vid.current; if (!v || tag === 'BUTTON') return
      if (e.key === ' ' || e.key === 'k') { e.preventDefault(); v.paused ? v.play() : v.pause() }
      else if (tag !== 'INPUT' && e.key === 'ArrowRight') v.currentTime = Math.min(v.duration || 1e9, v.currentTime + 5)
      else if (tag !== 'INPUT' && e.key === 'ArrowLeft') v.currentTime = Math.max(0, v.currentTime - 5)
      else if (e.key === 'm') v.muted = !v.muted
    }
    window.addEventListener('keydown', key, true)
    return () => { window.removeEventListener('keydown', key, true); if (entered.current) { unlockEsc(); if (fsElement()) exitFs().catch(() => { }) } }
  }, [close])
  const toggle = () => { const v = vid.current; if (v) v.paused ? v.play() : v.pause() }
  return createPortal(
    <div ref={box} tabIndex={-1} role="dialog" aria-modal="true" aria-label={`Video player: ${id}`} data-cinema-player className="cinema fixed inset-0 z-[200] bg-[#05080f] flex flex-col outline-none">
      <div className="flex items-center gap-3 px-5 py-3 border-b border-white/10 bg-[#0a111d] text-white">
        <span className="text-[10px] tracking-[.2em] text-amber-400 font-bold">EVIDENCE VIDEO</span>
        <b className="font-mono text-[14px]">{id}</b><span className="text-[13px] text-slate-300 truncate">{title}{subtitle ? ' · ' + subtitle : ''}</span>
        <button type="button" onClick={close} data-cinema-close aria-label="Close video (Esc)" title="Close (Esc)" className="ml-auto grid place-items-center w-9 h-9 rounded border border-white/25 text-white hover:bg-amber-500 hover:text-black"><X size={18} /></button></div>
      <div className="flex-1 min-h-0 grid place-items-center relative" onClick={toggle}>
        <video ref={vid} src={src} poster={poster} autoPlay playsInline className="max-w-full max-h-full object-contain bg-black" data-cinema-video
          onLoadedMetadata={e => { const v = e.currentTarget; setDur(v.duration); if (startAt > 0) v.currentTime = Math.min(startAt, v.duration) }}
          onTimeUpdate={e => setT(e.currentTarget.currentTime)} onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onVolumeChange={e => { setMuted(e.currentTarget.muted); setVol(e.currentTarget.volume) }}
          onError={() => setErr('This video file could not be loaded.')} />
        {err && <div className="absolute text-red-300 bg-red-950/70 border border-red-500/50 rounded px-4 py-2 text-sm">{err}</div>}</div>
      <div className="flex items-center gap-3 px-5 py-3 bg-[#0a111d] border-t border-white/10 text-white" onClick={e => e.stopPropagation()}>
        <button type="button" onClick={toggle} data-cinema-play aria-label={playing ? 'Pause' : 'Play'} className="w-9 h-9 grid place-items-center rounded border border-white/25 hover:bg-white/10">{playing ? <Pause size={18} /> : <Play size={18} />}</button>
        <span className="text-[12px] font-mono w-[92px] text-center">{mmss(t)} / {mmss(dur)}</span>
        <input type="range" aria-label="Seek" data-cinema-seek min={0} max={dur || 1} step={0.1} value={t} onChange={e => { if (vid.current) vid.current.currentTime = +e.target.value }} className="flex-1 accent-amber-500" />
        <button type="button" onClick={() => { if (vid.current) vid.current.muted = !vid.current.muted }} aria-label={muted ? 'Unmute' : 'Mute'} className="w-9 h-9 grid place-items-center rounded border border-white/25 hover:bg-white/10">{muted || vol === 0 ? <VolumeX size={18} /> : <Volume2 size={18} />}</button>
        <input type="range" aria-label="Volume" min={0} max={1} step={0.05} value={muted ? 0 : vol} onChange={e => { if (vid.current) { vid.current.volume = +e.target.value; vid.current.muted = +e.target.value === 0 } }} className="w-24 accent-amber-500" />
        <span className="text-[11px] text-slate-400 hidden md:inline">Esc closes · Space play/pause · ←/→ seek 5 s</span></div>
    </div>, document.body)
}
