import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-subtle bg-surface py-6 px-4 mt-auto">
      <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
        <div>
          <p className="text-xs font-medium text-text-primary">
            Blind Spot — Decision Reflection Engine
          </p>
          <p className="text-[11px] text-text-muted mt-0.5">
            A tool that questions your thinking, not one that decides for you.
          </p>
        </div>

        <div className="text-[11px] text-text-muted font-mono flex items-center gap-2">
          <span>Stateless</span>
          <span>•</span>
          <span>Zero Server Retention</span>
        </div>
      </div>
    </footer>
  );
};
