import React from "react";

interface ErrorStateProps {
  message?: string;
  onRetry: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  message = "Something went wrong while analyzing your reasoning. Please try again.",
  onRetry,
}) => {
  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div
        className="bg-surface border border-rose-500/30 p-6 text-center space-y-4"
        style={{ borderRadius: "var(--radius)" }}
      >
        <div className="space-y-1.5">
          <span className="text-xs font-mono uppercase tracking-wider text-rose-500 font-semibold">
            Analysis Paused
          </span>
          <p className="text-sm text-text-primary max-w-md mx-auto leading-relaxed">
            {message}
          </p>
        </div>

        <div>
          <button
            type="button"
            onClick={onRetry}
            className="px-4 py-2 border border-subtle bg-surface hover:border-strong text-text-primary text-xs font-medium transition-colors cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent-primary"
            style={{ borderRadius: "var(--radius)" }}
          >
            Retry Analysis
          </button>
        </div>
      </div>
    </div>
  );
};
