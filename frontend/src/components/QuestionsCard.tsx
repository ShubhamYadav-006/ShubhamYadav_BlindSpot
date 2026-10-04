import React from "react";
import { Question } from "../types/analysis";

interface QuestionsCardProps {
  questions: Question[];
}

export const QuestionsCard: React.FC<QuestionsCardProps> = ({ questions }) => {
  return (
    <div
      className="bg-surface border border-subtle p-5 sm:p-6"
      style={{ borderRadius: "var(--radius)" }}
    >
      <div className="flex items-center justify-between pb-2 mb-4 border-b border-subtle">
        <div>
          <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
            Questions to Challenge Your Perspective ({questions.length})
          </h3>
          <p className="text-xs text-text-muted mt-0.5">
            Socratic inquiries designed to clarify what matters most to you.
          </p>
        </div>
      </div>

      {questions.length === 0 ? (
        <p className="text-xs text-text-muted italic py-2">
          No reflection questions were generated.
        </p>
      ) : (
        <ol className="divide-y divide-subtle list-none p-0 m-0">
          {questions.map((item, idx) => {
            const formattedNum = String(idx + 1).padStart(2, "0");
            return (
              <li key={idx} className="py-3.5 first:pt-1 last:pb-1">
                <div className="flex items-baseline gap-3">
                  <span className="font-mono text-xs text-text-muted select-none shrink-0 font-medium">
                    {formattedNum}
                  </span>
                  <div className="space-y-1.5 flex-1">
                    <p className="text-sm sm:text-base text-text-primary font-normal leading-relaxed">
                      {item.question}
                    </p>
                    {item.linked_to && (
                      <div className="flex items-center gap-1.5 text-[11px] text-text-muted font-mono">
                        <span>Pertains to:</span>
                        <span
                          className="px-1.5 py-0.5 border border-subtle text-text-primary bg-surface-elevated"
                          style={{ borderRadius: "var(--radius)" }}
                        >
                          {item.linked_to}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
};
