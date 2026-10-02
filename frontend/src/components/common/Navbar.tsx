import { Link } from 'react-router-dom'
import deploymentPoints from '../deployment/deploymentPoints'

const navigationItems = [
  { label: 'Tracking', to: '/tracking' },
  { label: 'Alerts', to: '/alerts' },
  { label: 'Geomap', to: '/geomap' },
]

export default function Navbar() {
  return (
    <nav
      className="relative z-20 grid min-h-[68px] grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center rounded-2xl border border-[rgb(255_255_255_/_0.07)] bg-[rgb(71_77_80_/_0.1)] px-7 font-medium tracking-[0.025em] text-white max-[600px]:min-h-0 max-[600px]:grid-cols-[1fr_auto] max-[600px]:gap-y-[14px] max-[600px]:px-[18px] max-[600px]:py-[17px]"
      aria-label="Main navigation"
    >
      <Link
        className="justify-self-start text-[1.35rem] font-bold tracking-[0.16em] no-underline text-inherit focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-white/80 focus-visible:outline-offset-[5px] max-[600px]:text-[1.15rem]"
        to="/tracking"
        aria-label="MOVINT home"
      >
        MOVINT
      </Link>

      <div className="flex items-center justify-center gap-[clamp(24px,4vw,58px)] max-[600px]:col-span-full max-[600px]:justify-between max-[600px]:gap-3">
        {navigationItems.map((item) => (
          <Link
            className="text-[0.92rem] text-white/80 no-underline transition-colors duration-[160ms] hover:text-white focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-white/80 focus-visible:outline-offset-[5px] max-[600px]:text-[0.82rem]"
            to={item.to}
            key={item.to}
          >
            {item.label}
          </Link>
        ))}
      </div>

      <div className="group relative justify-self-end max-[600px]:col-start-2 max-[600px]:row-start-1">
        <Link
          className="inline-flex items-center gap-2 text-[0.92rem] text-white/80 no-underline transition-colors duration-[160ms] hover:text-white focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-white/80 focus-visible:outline-offset-[5px] max-[600px]:text-[0.82rem]"
          to="/deployment"
          aria-haspopup="true"
        >
          Deployment
          <PlusIcon className="h-3.5 w-3.5 fill-current" />
        </Link>

        <div className="invisible pointer-events-none absolute right-0 top-full z-50 w-56 translate-y-1 pt-2 opacity-0 transition-[opacity,transform] duration-150 group-hover:visible group-hover:pointer-events-auto group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:visible group-focus-within:pointer-events-auto group-focus-within:translate-y-0 group-focus-within:opacity-100">
          <div className="rounded-xl border border-white/10 bg-[rgb(12_16_19_/_0.96)] p-2 shadow-2xl backdrop-blur-xl">
            {deploymentPoints.map((point) => (
              <Link
                key={point.path}
                to={`/deployment/${point.path}`}
                className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-white/75 no-underline transition-colors duration-150 hover:bg-white/5 hover:text-white focus-visible:bg-white/5 focus-visible:text-white focus-visible:outline-none"
              >
                <PlusIcon className="h-3.5 w-3.5 shrink-0 fill-current text-white/60" />
                {point.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

function PlusIcon({ className }: { className: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 640 640"
      aria-hidden="true"
      className={className}
    >
      <path d="M352 128C352 110.3 337.7 96 320 96C302.3 96 288 110.3 288 128L288 288L128 288C110.3 288 96 302.3 96 320C96 337.7 110.3 352 128 352L288 352L288 512C288 529.7 302.3 544 320 544C337.7 544 352 529.7 352 512L352 352L512 352C529.7 352 544 337.7 544 320C544 302.3 529.7 288 512 288L352 288L352 128z" />
    </svg>
  )
}
