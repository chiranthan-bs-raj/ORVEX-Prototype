import { useEffect, useRef } from 'react'

/** Restrained "intelligence board" background: a few slow particles joined by faint lines. Purely decorative (aria-hidden).
 *  Pauses when the tab is hidden, draws one still frame when the user prefers reduced motion, and cleans up everything on unmount. */
export default function Ambient() {
  const ref = useRef<HTMLCanvasElement>(null)
  useEffect(() => {
    const cv = ref.current!; const cx = cv.getContext('2d')!; let w = 0, h = 0, raf = 0
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const P = Array.from({ length: 34 }, () => ({ x: Math.random(), y: Math.random(), vx: (Math.random() - .5) * 0.00006, vy: (Math.random() - .5) * 0.00006 }))
    const size = () => { const d = Math.min(window.devicePixelRatio || 1, 2); w = cv.clientWidth; h = cv.clientHeight; cv.width = w * d; cv.height = h * d; cx.setTransform(d, 0, 0, d, 0, 0) }
    const draw = (step: boolean) => {
      cx.clearRect(0, 0, w, h)
      for (const p of P) { if (step) { p.x += p.vx * 16; p.y += p.vy * 16; if (p.x < 0 || p.x > 1) p.vx *= -1; if (p.y < 0 || p.y > 1) p.vy *= -1 } }
      for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) {
        const dx = (P[i].x - P[j].x) * w, dy = (P[i].y - P[j].y) * h, d = Math.hypot(dx, dy)
        if (d < 170) { cx.strokeStyle = `rgba(120,160,215,${0.16 * (1 - d / 170)})`; cx.lineWidth = 1; cx.beginPath(); cx.moveTo(P[i].x * w, P[i].y * h); cx.lineTo(P[j].x * w, P[j].y * h); cx.stroke() } }
      for (const p of P) { cx.fillStyle = 'rgba(217,131,36,.55)'; cx.beginPath(); cx.arc(p.x * w, p.y * h, 1.6, 0, 6.3); cx.fill() }
    }
    const loop = () => { draw(true); raf = requestAnimationFrame(loop) }
    const vis = () => { cancelAnimationFrame(raf); if (!document.hidden && !reduce) raf = requestAnimationFrame(loop) }
    size(); draw(false); window.addEventListener('resize', size); document.addEventListener('visibilitychange', vis); vis()
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', size); document.removeEventListener('visibilitychange', vis) }
  }, [])
  return <canvas ref={ref} aria-hidden="true" className="fixed inset-0 w-full h-full pointer-events-none z-0" />
}
