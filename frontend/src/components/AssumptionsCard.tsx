import React from "react";
import { Assumption } from "../types/analysis";

interface AssumptionsCardProps {
  assumptions: Assumption[];
}

export const AssumptionsCard: React.FC<AssumptionsCardProps> = ({ assumptions }) => {
  return (
    <div
      className="bg-surface border border-subtle p-4 sm:p-5"
      style={{ borderRadius: "var(--radius)" }}
    >
      <div className="flex items-center justify-between pb-2 mb-3 border-b border-subtle">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
          Unexamined Assumptions ({assumptions.length})
        </h3>
        <span className="text-[11px] text-text-muted">Premises taken for granted</span>
      </div>

      {assumptions.length === 0 ? (
        <p className="text-xs text-text-muted italic py-2">
          No distinct unstated assumptions were identified.
        </p>
      ) : (
        <div className="divide-y divide-subtle">
          {assumptions.map((item, idx) => (
            <div key={idx} className="py-2.5 first:pt-0 last:pb-0 space-y-1">
              <div className="flex items-start gap-2">
                <span className="text-[11px] font-mono text-text-muted mt-0.5 shrink-0">
                  {idx + 1}.
                </span>
                <p className="text-xs sm:text-sm font-medium text-text-primary leading-snug">
                  &ldquo;{item.assumption}&rdquo;
                </p>
              </div>
              <div className="pl-5 text-xs text-text-muted flex items-start gap-1.5 leading-relaxed">
                <span className="text-[10px] font-mono uppercase text-amber-500 font-semibold shrink-0">
                  Risk:
                </span>
                <span>{item.why_risky}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
