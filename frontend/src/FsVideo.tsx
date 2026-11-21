import { useRef, useState } from 'react'
import { Maximize2 } from 'lucide-react'
import CinemaPlayer from './CinemaPlayer'

/** Inline video (native play, seek and volume controls) with its own fullscreen button.
 *  The button opens a CinemaPlayer overlay starting at the current time. Each FsVideo owns its overlay state, so the
 *  Reference Video and the Selected Video never affect each other. */
export default function FsVideo({ src, poster, label, id, title }: { src: string; poster?: string; label: string; id: string; title: string }) {
  const v = useRef<HTMLVideoElement>(null); const [open, setOpen] = useState(false); const [start, setStart] = useState(0)
  const openIt = () => { const el = v.current; setStart(el?.currentTime || 0); el?.pause(); setOpen(true) }
  return <>
    <div data-fs-player={label} className="relative bg-black group rounded-md overflow-hidden aspect-video w-full">
      <video ref={v} controls controlsList="nofullscreen" poster={poster} src={src} className="w-full h-full object-contain bg-black" />
      <button type="button" onClick={openIt} aria-label={`Fullscreen: ${label}`} title="Fullscreen"
        className="absolute top-2 right-2 z-10 grid place-items-center w-8 h-8 rounded bg-black/65 text-white border border-white/30 hover:bg-amber-500 hover:text-black transition"><Maximize2 size={16} /></button>
    </div>
    {open && <CinemaPlayer id={id} title={title} subtitle={label} src={src} poster={poster} startAt={start} onClose={() => setOpen(false)} />}
  </>
}
