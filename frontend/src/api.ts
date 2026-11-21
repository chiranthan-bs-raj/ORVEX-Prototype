export const tok = () => localStorage.getItem('orvex_token') || ''
export async function api<T = any>(path: string, opts: { method?: string; body?: any; params?: Record<string, any> } = {}): Promise<T> {
  const q = opts.params ? '?' + new URLSearchParams(Object.entries(opts.params).filter(([, v]) => v !== '' && v != null).map(([k, v]) => [k, String(v)])) : ''
  const r = await fetch('/api' + path + q, { method: opts.method || 'GET', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + tok() }, body: opts.body ? JSON.stringify(opts.body) : undefined })
  if (r.status === 401 && !path.startsWith('/auth/')) { localStorage.removeItem('orvex_token'); location.href = '/login' }
  if (!r.ok) { let m = r.statusText; try { m = (await r.json()).detail || m } catch { /* ignore */ } throw new Error(m) }
  return r.json()
}
export const frame = (id: string, t = 1, w = 360) => `/api/media/${id}/frame?t=${t}&w=${w}`
export const stream = (id: string) => `/api/media/${id}/stream`
export const mmss = (s?: number | null) => s == null ? '–' : `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(Math.round(s % 60)).padStart(2, '0')}`
export const ROLE: Record<string, { c: string; name: string }> = {
  reference: { c: '#2563EB', name: 'Reference video' }, direct: { c: '#DC2626', name: 'Direct derivative' }, indirect: { c: '#F59E0B', name: 'Indirect derivative' },
  same: { c: '#7C3AED', name: 'Same incident (related)' }, unrelated: { c: '#6B7280', name: 'Unrelated' } }
export const TLABEL: Record<string, string> = { caption_burn_in: 'Caption added', watermark_overlay: 'Watermark added', trim_middle: 'Trimmed (middle)', trim_head: 'Trimmed (head)', trim_tail: 'Trimmed (tail)', crop_center: 'Cropped', recompress_low: 'Recompressed (low)', reencode_hq: 'Re-encoded (HQ)', audio_replace: 'Audio replaced', audio_mute: 'Audio muted', audio_noise_mix: 'Noise mixed into audio', mirror_color_shift: 'Mirrored + colour shift', speed_change: 'Speed changed', reupload_sim: 'Re-upload simulation' }
