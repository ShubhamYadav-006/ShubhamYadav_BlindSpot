import React from "react";
import { AnalyzeResponse } from "../types/analysis";
import { StatedFactorsCard } from "./StatedFactorsCard";
import { AssumptionsCard } from "./AssumptionsCard";
import { ConflictsCard } from "./ConflictsCard";
import { BlindSpotsCard } from "./BlindSpotsCard";
import { QuestionsCard } from "./QuestionsCard";

interface ResultsProps {
  data: AnalyzeResponse;
  onReset: () => void;
}

export const Results: React.FC<ResultsProps> = ({ data, onReset }) => {
  const totalItems =
    data.stated_factors.length +
    data.assumptions.length +
    data.conflicts.length +
    data.blind_spots.length;

  const factorsPct = totalItems > 0 ? (data.stated_factors.length / totalItems) * 100 : 0;
  const assumptionsPct = totalItems > 0 ? (data.assumptions.length / totalItems) * 100 : 0;
  const conflictsPct = totalItems > 0 ? (data.conflicts.length / totalItems) * 100 : 0;
  const blindSpotsPct = totalItems > 0 ? (data.blind_spots.length / totalItems) * 100 : 0;

  return (
    <div className="max-w-4xl mx-auto px-4 space-y-6">
      {/* Top action header */}
      <div className="flex items-center justify-between pb-3 border-b border-subtle">
        <button
          type="button"
          onClick={onReset}
          className="px-3.5 py-1.5 text-xs font-medium text-text-muted hover:text-text-primary border border-subtle bg-surface hover:border-strong transition-colors cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent-primary"
          style={{ borderRadius: "var(--radius)" }}
        >
          ← New Reflection
        </button>

        <span className="text-[11px] font-mono text-text-muted">
          Reasoning Reflection Report
        </span>
      </div>

      {/* 1. Stagger 1: Input Statement */}
      <div
        className="stagger-1 bg-surface border border-subtle p-4 sm:p-6"
        style={{ borderRadius: "var(--radius)" }}
      >
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-text-muted">
            The Decision Evaluated
          </span>
          <span className="text-[11px] font-mono text-text-muted">Original Input</span>
        </div>
        <p className="font-serif text-base sm:text-xl font-normal text-text-primary leading-snug">
          &ldquo;{data.decision}&rdquo;
        </p>
      </div>

      {/* 2. Stagger 2: Reasoning Balance Meter */}
      <div
        className="stagger-2 bg-surface border border-subtle p-4 sm:p-5 space-y-2.5"
        style={{ borderRadius: "var(--radius)" }}
      >
        <div className="flex items-center justify-between text-xs text-text-muted">
          <span className="font-semibold uppercase tracking-wider">
            Reasoning Balance Meter
          </span>
          <span className="font-mono text-[11px]">{totalItems} elements surfaced</span>
        </div>

        {/* Slim segmented horizontal bar */}
        <div
          className="w-full h-2.5 bg-surface-elevated border border-subtle flex overflow-hidden"
          style={{ borderRadius: "var(--radius)" }}
        >
          {factorsPct > 0 && (
            <div
              style={{
                width: `${factorsPct}%`,
                backgroundColor: "var(--meter-stated)",
              }}
              title={`Stated Factors: ${data.stated_factors.length}`}
              className="h-full border-r border-base last:border-none"
            />
          )}
          {assumptionsPct > 0 && (
            <div
              style={{
                width: `${assumptionsPct}%`,
                backgroundColor: "var(--meter-assumptions)",
              }}
              title={`Assumptions: ${data.assumptions.length}`}
              className="h-full border-r border-base last:border-none"
            />
          )}
          {conflictsPct > 0 && (
            <div
              style={{
                width: `${conflictsPct}%`,
                backgroundColor: "var(--meter-conflicts)",
              }}
              title={`Conflicts: ${data.conflicts.length}`}
              className="h-full border-r border-base last:border-none"
            />
          )}
          {blindSpotsPct > 0 && (
            <div
              style={{
                width: `${blindSpotsPct}%`,
                backgroundColor: "var(--meter-blindspots)",
              }}
              title={`Blind Spots: ${data.blind_spots.length}`}
              className="h-full"
            />
          )}
        </div>

        {/* Meter Legend */}
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-[11px] text-text-muted font-mono pt-1">
          <div className="flex items-center gap-1.5">
            <span
              className="w-2 h-2 shrink-0"
              style={{ backgroundColor: "var(--meter-stated)", borderRadius: "1px" }}
            />
            <span>Stated Factors ({data.stated_factors.length})</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span
              className="w-2 h-2 shrink-0"
              style={{
                backgroundColor: "var(--meter-assumptions)",
                borderRadius: "1px",
              }}
            />
            <span>Assumptions ({data.assumptions.length})</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span
              className="w-2 h-2 shrink-0"
              style={{ backgroundColor: "var(--meter-conflicts)", borderRadius: "1px" }}
            />
            <span>Conflicts ({data.conflicts.length})</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span
              className="w-2 h-2 shrink-0"
              style={{
                backgroundColor: "var(--meter-blindspots)",
                borderRadius: "1px",
              }}
            />
            <span>Blind Spots ({data.blind_spots.length})</span>
          </div>
        </div>
      </div>

      {/* 3. Stagger 3: Blind Spots (Visual centerpiece) */}
      <div className="stagger-3">
        <BlindSpotsCard blindSpots={data.blind_spots} />
      </div>

      {/* 4. Stagger 4: Assumptions & Conflicts in 2 columns */}
      <div className="stagger-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <AssumptionsCard assumptions={data.assumptions} />
        <ConflictsCard conflicts={data.conflicts} />
      </div>

      {/* 5. Stagger 5: Stated Factors */}
      <div className="stagger-5">
        <StatedFactorsCard factors={data.stated_factors} />
      </div>

      {/* 6. Stagger 6: Socratic Questions */}
      <div className="stagger-6">
        <QuestionsCard questions={data.questions} />
      </div>

      {/* Bottom Action: Secondary Rectangular Button */}
      <div className="pt-6 pb-10 flex justify-center">
        <button
          type="button"
          onClick={onReset}
          className="px-5 py-2.5 border border-subtle bg-surface hover:border-strong text-text-primary text-sm font-medium transition-colors cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent-primary"
          style={{ borderRadius: "var(--radius)" }}
        >
          Reflect on Another Decision
        </button>
      </div>
    </div>
  );
};
