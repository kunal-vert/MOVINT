const navigationItems = ['Tracking', 'Alerts', 'Geomap']

export default function Navbar() {
  return (
    <nav
      className="grid min-h-[68px] grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center rounded-2xl border border-[rgb(255_255_255_/_0.07)] bg-[rgb(71_77_80_/_0.1)] px-7 font-medium tracking-[0.025em] text-white max-[600px]:min-h-0 max-[600px]:grid-cols-[1fr_auto] max-[600px]:gap-y-[14px] max-[600px]:px-[18px] max-[600px]:py-[17px]"
      aria-label="Main navigation"
    >
      <a
        className="justify-self-start text-[1.35rem] font-bold tracking-[0.16em] no-underline text-inherit focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-white/80 focus-visible:outline-offset-[5px] max-[600px]:text-[1.15rem]"
        href="#home"
        aria-label="MOVINT home"
      >
        MOVINT
      </a>

      <div className="flex items-center justify-center gap-[clamp(24px,4vw,58px)] max-[600px]:col-span-full max-[600px]:justify-between max-[600px]:gap-3">
        {navigationItems.map((item) => (
          <a
            className="text-[0.92rem] text-white/80 no-underline transition-colors duration-[160ms] hover:text-white focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-white/80 focus-visible:outline-offset-[5px] max-[600px]:text-[0.82rem]"
            href={`#${item.toLowerCase()}`}
            key={item}
          >
            {item}
          </a>
        ))}
      </div>

      <a
        className="justify-self-end text-[0.92rem] text-white/80 no-underline transition-colors duration-[160ms] hover:text-white focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-white/80 focus-visible:outline-offset-[5px] max-[600px]:col-start-2 max-[600px]:row-start-1 max-[600px]:text-[0.82rem]"
        href="#deployment"
      >
        Deployment
      </a>
    </nav>
  )
}
