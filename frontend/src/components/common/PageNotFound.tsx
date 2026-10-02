/// <reference types="vite/client" />

import { Link } from 'react-router-dom'
import backgroundVideo from '../../assets/gemini_generated_video_daf115a6.mp4'

export default function PageNotFound() {
  return (
    <main className="fixed inset-0 z-[100] h-screen min-h-screen w-screen overflow-hidden bg-black text-white">
      <video
        className="absolute inset-0 h-full w-full object-cover"
        src={backgroundVideo}
        autoPlay
        muted
        loop
        playsInline
        preload="auto"
        aria-hidden="true"
      />

      <div className="absolute inset-0 bg-black/65" aria-hidden="true" />

      <section className="relative z-10 flex h-full flex-col items-center justify-center px-6 text-center">
     
        <Link
          className="mt-9 inline-flex min-h-12 items-center justify-center border border-white/25 bg-white/5 px-7 py-3 text-xs font-semibold tracking-[0.16em] text-white no-underline transition-colors hover:border-white/50 hover:bg-white/10 focus-visible:outline-2 focus-visible:outline-white focus-visible:outline-offset-4 sm:text-sm"
          to="/tracking"
        >
          RETURN TO TRACKING
        </Link>
      </section>
    </main>
  )
}
