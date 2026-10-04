import React from "react";
import { FactorCategory, StatedFactor } from "../types/analysis";

interface StatedFactorsCardProps {
  factors: StatedFactor[];
}

const CATEGORY_NAMES: Record<FactorCategory, string> = {
  money: "Financial",
  growth: "Growth",
  career: "Career",
  convenience: "Convenience",
  health: "Health",
  relationships: "Social",
  academics: "Academic",
  other: "Other",
};

export const StatedFactorsCard: React.FC<StatedFactorsCardProps> = ({ factors }) => {
  return (
    <div
      className="bg-surface border border-subtle p-4 sm:p-5"
      style={{ borderRadius: "var(--radius)" }}
    >
      <div className="flex items-center justify-between pb-2 mb-3 border-b border-subtle">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
          Identified Factors ({factors.length})
        </h3>
        <span className="text-[11px] text-text-muted">Explicit inputs recognized</span>
      </div>

      {factors.length === 0 ? (
        <p className="text-xs text-text-muted italic py-2">
          No explicit factors were identified from your statement.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          {factors.map((item, idx) => {
            const label = CATEGORY_NAMES[item.category] || "General";
            return (
              <div
                key={idx}
                className="flex items-center justify-between gap-3 px-3 py-2 bg-surface-elevated border border-subtle"
                style={{ borderRadius: "var(--radius)" }}
              >
                <span className="text-xs sm:text-sm font-medium text-text-primary leading-snug">
                  {item.factor}
                </span>
                <span
                  className="text-[10px] font-mono uppercase tracking-wider px-1.5 py-0.5 border border-subtle text-text-muted shrink-0"
                  style={{ borderRadius: "var(--radius)" }}
                >
                  {label}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
