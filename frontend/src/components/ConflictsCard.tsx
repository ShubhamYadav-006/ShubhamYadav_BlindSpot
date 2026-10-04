import React from "react";
import { Conflict } from "../types/analysis";

interface ConflictsCardProps {
  conflicts: Conflict[];
}

export const ConflictsCard: React.FC<ConflictsCardProps> = ({ conflicts }) => {
  return (
    <div
      className="bg-surface border border-subtle p-4 sm:p-5"
      style={{ borderRadius: "var(--radius)" }}
    >
      <div className="flex items-center justify-between pb-2 mb-3 border-b border-subtle">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
          Internal Conflicts ({conflicts.length})
        </h3>
        <span className="text-[11px] text-text-muted">Competing priorities</span>
      </div>

      {conflicts.length === 0 ? (
        <p className="text-xs text-text-muted italic py-2">
          No explicit contradictions were detected in your statement.
        </p>
      ) : (
        <div className="divide-y divide-subtle">
          {conflicts.map((item, idx) => (
            <div key={idx} className="py-2.5 first:pt-0 last:pb-0 space-y-1">
              <div className="flex items-start gap-2">
                <span className="text-[11px] font-mono text-text-muted mt-0.5 shrink-0">
                  {idx + 1}.
                </span>
                <p className="text-xs sm:text-sm font-medium text-text-primary leading-snug">
                  {item.conflict}
                </p>
              </div>
              <div className="pl-5 text-xs text-text-muted leading-relaxed">
                <span className="text-[10px] font-mono uppercase text-accent-primary font-semibold mr-1">
                  Tension:
                </span>
                {item.explanation}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
