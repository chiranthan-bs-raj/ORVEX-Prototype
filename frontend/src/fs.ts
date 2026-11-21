/** Browser fullscreen helpers (standard API with the WebKit-prefixed fallback). */
export const fsElement = (): Element | null => document.fullscreenElement || (document as any).webkitFullscreenElement || null
export const enterFs = (el: HTMLElement): Promise<void> => {
  try { const r = el.requestFullscreen ? el.requestFullscreen() : (el as any).webkitRequestFullscreen?.(); return Promise.resolve(r).then(() => undefined) } catch (e) { return Promise.reject(e) }
}
export const exitFs = (): Promise<void> => {
  try { const r = document.exitFullscreen ? document.exitFullscreen() : (document as any).webkitExitFullscreen?.(); return Promise.resolve(r).then(() => undefined) } catch (e) { return Promise.reject(e) }
}
/** Keyboard Lock lets a short Esc press reach the page while in browser fullscreen (Chrome / Edge, secure contexts only).
 *  Without it Esc would leave browser fullscreen before the page could close its own overlay. */
export const canLockEsc = (): boolean => !!(navigator as any).keyboard?.lock && window.isSecureContext
export const lockEsc = () => { try { (navigator as any).keyboard.lock(['Escape']).catch(() => { }) } catch { /* not supported */ } }
export const unlockEsc = () => { try { (navigator as any).keyboard?.unlock?.() } catch { /* not supported */ } }
