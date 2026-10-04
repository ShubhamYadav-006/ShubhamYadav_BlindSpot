import React from "react";

interface HeroProps {
  onStartClick?: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onStartClick }) => {
  const handleScrollToForm = () => {
    if (onStartClick) {
      onStartClick();
    } else {
      const formEl = document.getElementById("decision-input");
      if (formEl) {
        formEl.scrollIntoView({ behavior: "smooth", block: "center" });
        formEl.focus();
      }
    }
  };

  return (
    <section className="py-8 sm:py-14 max-w-3xl mx-auto px-4 text-center">
      {/* Sharp One-Line Headline */}
      <h1 className="font-serif text-2xl sm:text-4xl md:text-5xl text-text-primary tracking-tight font-normal mb-3 sm:mb-4 leading-tight">
        Find what your reasoning is missing.
      </h1>

      {/* Subtext */}
      <p className="text-sm sm:text-base text-text-muted max-w-xl mx-auto leading-relaxed mb-6 sm:mb-8 font-sans font-normal">
        A tool that questions your thinking, not one that decides for you.
      </p>

      {/* Primary Rectangular CTA */}
      <div className="flex justify-center">
        <button
          type="button"
          onClick={handleScrollToForm}
          className="px-5 py-2.5 bg-accent-primary hover:bg-accent-hover text-white text-sm font-medium transition-colors border border-transparent cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent-primary focus:ring-offset-2"
          style={{ borderRadius: "var(--radius)" }}
        >
          Begin Reflection
        </button>
      </div>
    </section>
  );
};
