import React from "react";

export const LoadingState: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div className="text-center space-y-2 mb-6">
        <h3 className="font-serif text-lg sm:text-xl font-medium text-text-primary">
          Examining your reasoning
        </h3>
        <p className="text-xs text-text-muted">
          Deconstructing stated factors, hidden assumptions, and potential blind spots...
        </p>
      </div>

      {/* Skeleton 1: Input & Balance Meter */}
      <div
        className="bg-surface border border-subtle p-4 sm:p-5 space-y-3"
        style={{ borderRadius: "var(--radius)" }}
      >
        <div className="flex justify-between items-center">
          <div className="w-24 h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
          <div className="w-16 h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
        </div>
        <div className="w-3/4 h-5 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
        <div className="w-full h-2.5 bg-surface-elevated skeleton-pulse mt-4" style={{ borderRadius: "var(--radius)" }} />
      </div>

      {/* Skeleton 2: Blind spots 3-col grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-surface border border-subtle border-l-2 border-l-accent-primary p-4 space-y-3"
            style={{ borderRadius: "var(--radius)" }}
          >
            <div className="flex justify-between">
              <div className="w-6 h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
              <div className="w-16 h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
            </div>
            <div className="w-4/5 h-4 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
            <div className="w-full h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
            <div className="w-2/3 h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
          </div>
        ))}
      </div>

      {/* Skeleton 3: 2-column lists */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[1, 2].map((i) => (
          <div
            key={i}
            className="bg-surface border border-subtle p-4 space-y-3"
            style={{ borderRadius: "var(--radius)" }}
          >
            <div className="w-32 h-3.5 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
            <div className="w-full h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
            <div className="w-5/6 h-3 bg-surface-elevated skeleton-pulse" style={{ borderRadius: "2px" }} />
          </div>
        ))}
      </div>
    </div>
  );
};
