import { useCallback, useRef, useState } from "react";
import { ParticlesProvider } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";
import StarField from "./StarField";

/* ------------------------------------------------------------------ */
/*  Props                                                              */
/* ------------------------------------------------------------------ */
interface EdenSignInProps {
  onSubmit?: (value: string, mode: "email" | "code") => void | Promise<void>;
}

/* ------------------------------------------------------------------ */
/*  Validation helpers                                                 */
/* ------------------------------------------------------------------ */
const isEmailValid = (v: string) => /^\S+@\S+\.\S+$/.test(v);
const isCodeValid = (v: string) => v.trim().length >= 4;

/* ------------------------------------------------------------------ */
/*  Logo – leaf + 4-point sparkle                                      */
/* ------------------------------------------------------------------ */
function Logo() {
  return (
    <svg
      width="32"
      height="32"
      viewBox="0 0 32 32"
      fill="none"
      aria-hidden="true"
      className="mb-8.5"
    >
      {/* leaf */}
      <path
        d="M8 26C8 26 6 16 16 10C26 4 28 2 28 2C28 2 28 14 20 20C12 26 8 26 8 26Z"
        fill="#e8e8e5"
        fillOpacity="0.9"
      />
      <path
        d="M8 26C8 26 10 18 16 14"
        stroke="#030303"
        strokeWidth="1.2"
        strokeLinecap="round"
      />
      {/* 4-point sparkle */}
      <path
        d="M7 6L8 3L9 6L12 7L9 8L8 11L7 8L4 7L7 6Z"
        fill="#e8e8e5"
      />
    </svg>
  );
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */
export default function EdenSignIn({ onSubmit }: EdenSignInProps) {
  const [value, setValue] = useState("");
  const [codeMode, setCodeMode] = useState(false);
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const mode = codeMode ? "code" : "email";
  const valid = codeMode ? isCodeValid(value) : isEmailValid(value);

  /* ---- submit ---------------------------------------------------- */
  const handleSubmit = useCallback(async () => {
    if (!valid) {
      setMessage(codeMode ? "Enter your code." : "Enter a valid email.");
      return;
    }
    setMessage(codeMode ? "Checking code\u2026" : "Sending you a code\u2026");
    if (onSubmit) {
      await onSubmit(value, mode);
    }
  }, [valid, codeMode, value, mode, onSubmit]);

  /* ---- toggle mode ----------------------------------------------- */
  const toggleMode = useCallback(() => {
    setCodeMode((prev) => !prev);
    setValue("");
    setMessage("");
    // Focus after React re-render
    setTimeout(() => inputRef.current?.focus(), 0);
  }, []);

  /* ---- key handler ----------------------------------------------- */
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleSubmit();
      }
    },
    [handleSubmit],
  );

  return (
    <ParticlesProvider init={loadSlim}>
    <div className="eden-bg eden-grain relative min-h-dvh overflow-hidden">
      <StarField />

      {/* content */}
      <div
        className="relative z-10 flex flex-col items-center justify-center text-center min-h-dvh mx-auto px-6 max-w-[560px]"
        style={{
          fontFamily: "'Inter', system-ui, sans-serif",
          paddingTop: "env(safe-area-inset-top)",
          paddingBottom: "env(safe-area-inset-bottom)",
        }}
      >
        <Logo />

        <h1 className="text-[28px] font-bold tracking-tight text-[#ececea]">
          Enter the NorthEast
        </h1>

        <p className="text-[15px] text-[#8c8c8a] mt-3.5">
          Sign up or sign in to survell.
        </p>

        {/* input */}
        <input
          ref={inputRef}
          type={codeMode ? "text" : "email"}
          autoComplete={codeMode ? "one-time-code" : "email"}
          aria-label={codeMode ? "Access code" : "Email"}
          placeholder={codeMode ? "Enter your code" : "you@email.com"}
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            setMessage("");
          }}
          onKeyDown={handleKeyDown}
          className="w-full bg-transparent border-none outline-none text-center text-[32px] text-[#e9e9e6] caret-white placeholder-[#5a5a58] focus-visible:ring-0"
          style={{ marginTop: "clamp(70px, 16vh, 130px)" }}
        />

        {/* status */}
        <p
          role="status"
          className="text-[13px] text-[#8c8c8a] min-h-[18px] mt-4"
        >
          {message}
        </p>

        {/* submit button */}
        <button
          type="button"
          onClick={handleSubmit}
          className={[
            "rounded-full w-full max-w-85 h-13.5 text-[15px] font-semibold",
            "transition-colors active:scale-[.98]",
            "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40",
            valid
              ? "bg-[#dcdcd8] text-[#1a1a1a]"
              : "bg-white/10 text-[#2a2a2a]",
          ].join(" ")}
          style={{ marginTop: "clamp(60px, 14vh, 110px)" }}
        >
          Continue
        </button>

        {/* toggle link */}
        <button
          type="button"
          onClick={toggleMode}
          className="text-xs font-medium text-[#a5a5a2] hover:text-[#e9e9e6] mt-[18px] bg-transparent border-none cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40 rounded"
        >
          {codeMode ? "Use email instead" : "I already have a code"}
        </button>

        {/* footer */}
        <p className="text-[11.5px] text-[#6f6f6d] mt-8">
          By signing in, you agree to our{" "}
          <a
            href="#"
            className="underline underline-offset-2 hover:text-[#a5a5a2]"
          >
            Terms
          </a>{" "}
          and{" "}
          <a
            href="#"
            className="underline underline-offset-2 hover:text-[#a5a5a2]"
          >
            Privacy Policy
          </a>
          .
        </p>
      </div>
    </div>
    </ParticlesProvider>
  );
}
