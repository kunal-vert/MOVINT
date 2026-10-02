import { useMemo } from "react";
import Particles from "@tsparticles/react";
import { useParticlesProvider } from "@tsparticles/react";
import type { ISourceOptions } from "@tsparticles/engine";

const REDUCED_MOTION =
  typeof window !== "undefined" &&
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/**
 * Renders an animated star field behind the sign-in content.
 * Must be rendered inside a <ParticlesProvider>.
 */
export default function StarField() {
  const { loaded } = useParticlesProvider();

  const options: ISourceOptions = useMemo(
    () => ({
      fullScreen: { enable: false },
      background: { color: "transparent" },
      detectRetina: true,
      particles: {
        number: { value: 120, density: { enable: true } },
        color: { value: "#ffffff" },
        shape: { type: "circle" },
        size: { value: { min: 0.5, max: 1.4 } },
        opacity: {
          value: { min: 0.2, max: 0.7 },
          animation: {
            enable: !REDUCED_MOTION,
            speed: 0.4,
            sync: false,
          },
        },
        move: {
          enable: !REDUCED_MOTION,
          speed: 0.15,
          random: true,
          direction: "none",
          outModes: { default: "out" },
        },
      },
    }),
    [],
  );

  if (!loaded) return null;

  return (
    <div className="fixed inset-0 z-0 pointer-events-none">
      <Particles id="eden-stars" options={options} />
    </div>
  );
}
