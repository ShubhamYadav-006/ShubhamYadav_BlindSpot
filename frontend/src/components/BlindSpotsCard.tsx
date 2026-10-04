import React, { useState } from "react";
import { BlindSpot } from "../types/analysis";

interface BlindSpotsCardProps {
  blindSpots: BlindSpot[];
}

export const BlindSpotsCard: React.FC<BlindSpotsCardProps> = ({ blindSpots }) => {
  // Track expanded state per item index
  const [expandedIndices, setExpandedIndices] = useState<Record<number, boolean>>({});

  const toggleExpand = (idx: number) => {
    setExpandedIndices((prev) => ({
      ...prev,
      [idx]: !prev[idx],
    }));
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between pb-1 border-b border-subtle">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-accent-primary" style={{ borderRadius: "1px" }}></span>
          <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
            Blind Spots ({blindSpots.length})
          </h3>
        </div>
        <span className="text-[11px] text-text-muted">Overlooked considerations</span>
      </div>

      {blindSpots.length === 0 ? (
        <p className="text-xs text-text-muted italic py-3">
          No significant blind spots were identified.
        </p>
      ) : (
        /* Responsive grid: 2-3 columns on desktop, 1 on mobile */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {blindSpots.map((item, idx) => {
            const isExpanded = !!expandedIndices[idx];
            return (
              <div
                key={idx}
                className="bg-surface border border-subtle border-l-2 border-l-accent-primary p-3.5 sm:p-4 flex flex-col justify-between transition-colors hover:border-strong"
                style={{ borderRadius: "var(--radius)" }}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[11px] font-mono text-text-muted">
                      #{idx + 1}
                    </span>
                    <span className="text-[10px] font-mono uppercase text-accent-primary px-1.5 py-0.5 bg-accent-subtle border border-accent-border">
                      Unseen Angle
                    </span>
                  </div>

                  <h4 className="text-sm font-semibold text-text-primary tracking-tight mb-2 leading-snug">
                    {item.area}
                  </h4>

                  <div className="text-xs text-text-muted leading-relaxed">
                    <p className={isExpanded ? "" : "line-clamp-2"}>
                      {item.why_it_matters_for_you}
                    </p>
                  </div>
                </div>

                <div className="pt-2 mt-2 border-t border-subtle flex justify-end">
                  <button
                    type="button"
                    onClick={() => toggleExpand(idx)}
                    aria-expanded={isExpanded}
                    className="text-[11px] font-medium text-accent-primary hover:underline cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent-primary px-1"
                  >
                    {isExpanded ? "Show less" : "Show more"}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
