import React, { useState, useEffect } from "react";

export const Header: React.FC = () => {
  const [theme, setTheme] = useState<"light" | "dark">("dark");

  useEffect(() => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    if (currentTheme === "light" || currentTheme === "dark") {
      setTheme(currentTheme);
    } else {
      try {
        const stored = localStorage.getItem("blindspot-theme");
        if (stored === "light" || stored === "dark") {
          setTheme(stored);
        } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
          setTheme("light");
        }
      } catch {
        setTheme("dark");
      }
    }
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
    document.documentElement.setAttribute("data-theme", nextTheme);
    try {
      localStorage.setItem("blindspot-theme", nextTheme);
    } catch {
      // Storage blocked or unavailable
    }
  };

  return (
    <header className="border-b border-subtle bg-surface sticky top-0 z-40">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-baseline gap-2">
          <span className="font-serif text-lg font-semibold tracking-tight text-text-primary">
            Blind Spot
          </span>
          <span className="text-[11px] font-mono text-text-muted hidden sm:inline">
            / reasoning inquiry
          </span>
        </div>

        {/* Right side controls: privacy indicator and theme toggle */}
        <div className="flex items-center gap-3">
          <div className="text-xs text-text-muted flex items-center gap-1.5 font-mono px-2 py-1 border border-subtle bg-surface-elevated">
            <span className="w-1.5 h-1.5 bg-emerald-500"></span>
            <span className="hidden sm:inline">Stateless & Private</span>
          </div>

          {/* Theme toggle: small square icon button rounded to --radius */}
          <button
            type="button"
            onClick={toggleTheme}
            aria-label={
              theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
            }
            title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            className="w-8 h-8 flex items-center justify-center border border-subtle bg-surface-elevated text-text-primary hover:border-strong transition-colors cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent-primary"
          >
            {theme === "dark" ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-4 h-4 text-text-primary"
              >
                <circle cx="12" cy="12" r="4" />
                <path d="M12 2v2" />
                <path d="M12 20v2" />
                <path d="m4.93 4.93 1.41 1.41" />
                <path d="m17.66 17.66 1.41 1.41" />
                <path d="M2 12h2" />
                <path d="M20 12h2" />
                <path d="m6.34 17.66-1.41 1.41" />
                <path d="m19.07 4.93-1.41 1.41" />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-4 h-4 text-text-primary"
              >
                <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
