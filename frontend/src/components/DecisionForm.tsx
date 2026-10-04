import React, { useState } from "react";
import { AnalyzeRequest } from "../types/analysis";

interface DecisionFormProps {
  onSubmit: (data: AnalyzeRequest) => void;
  isLoading: boolean;
}

const EXAMPLE_DECISION =
  "Should I accept the 6-month startup internship in Bangalore over continuing college coursework locally?";
const EXAMPLE_REASONING =
  "I'm leaning toward accepting it because the ₹45,000 stipend is great and working directly under ex-FAANG founders will accelerate my practical engineering skills, even though relocation is expensive and college might not grant attendance waivers easily.";

export const DecisionForm: React.FC<DecisionFormProps> = ({
  onSubmit,
  isLoading,
}) => {
  const [decision, setDecision] = useState<string>("");
  const [reasoning, setReasoning] = useState<string>("");
  const [touched, setTouched] = useState<{ decision: boolean; reasoning: boolean }>({
    decision: false,
    reasoning: false,
  });

  const decisionLength = decision.trim().length;
  const reasoningLength = reasoning.trim().length;

  const isDecisionValid = decisionLength >= 20 && decisionLength <= 1500;
  const isReasoningValid = reasoningLength >= 20 && reasoningLength <= 1500;
  const isFormValid = isDecisionValid && isReasoningValid;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setTouched({ decision: true, reasoning: true });
    if (!isFormValid || isLoading) return;
    onSubmit({ decision: decision.trim(), reasoning: reasoning.trim() });
  };

  const loadExample = () => {
    setDecision(EXAMPLE_DECISION);
    setReasoning(EXAMPLE_REASONING);
    setTouched({ decision: true, reasoning: true });
  };

  return (
    <div className="max-w-3xl mx-auto px-4">
      <div
        className="bg-surface border border-subtle p-5 sm:p-8"
        style={{ borderRadius: "var(--radius)" }}
      >
        <div className="flex items-center justify-between mb-6 pb-3 border-b border-subtle">
          <div>
            <h2 className="font-serif text-lg sm:text-xl font-medium text-text-primary">
              Describe your decision
            </h2>
            <p className="text-xs text-text-muted mt-0.5">
              Enter your pending choice and the underlying thoughts guiding it.
            </p>
          </div>
          <button
            type="button"
            onClick={loadExample}
            disabled={isLoading}
            className="text-xs font-mono text-accent-primary hover:underline transition-colors cursor-pointer disabled:opacity-50"
          >
            Load example
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Decision Input */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label
                htmlFor="decision-input"
                className="block text-xs font-medium uppercase tracking-wider text-text-muted"
              >
                1. The Choice You Are Evaluating
              </label>
              <span
                className={`text-[11px] font-mono ${
                  decisionLength > 0 && !isDecisionValid
                    ? "text-amber-500"
                    : "text-text-muted"
                }`}
              >
                {decisionLength}/1500 (min 20)
              </span>
            </div>
            <input
              id="decision-input"
              type="text"
              value={decision}
              onChange={(e) => setDecision(e.target.value)}
              onBlur={() => setTouched((prev) => ({ ...prev, decision: true }))}
              disabled={isLoading}
              placeholder="e.g., Should I take the 6-month startup internship in Bangalore?"
              className="w-full px-3.5 py-2.5 bg-surface-elevated border border-subtle text-text-primary placeholder:text-text-muted text-sm focus:outline-none focus:border-strong focus:ring-1 focus:ring-accent-primary transition-colors disabled:opacity-50"
              style={{ borderRadius: "var(--radius)" }}
            />
            {touched.decision && decisionLength > 0 && decisionLength < 20 && (
              <p className="mt-1 text-xs text-amber-500 font-sans">
                Please enter at least 20 characters ({20 - decisionLength} more needed).
              </p>
            )}
          </div>

          {/* Reasoning Input */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <div>
                <label
                  htmlFor="reasoning-input"
                  className="block text-xs font-medium uppercase tracking-wider text-text-muted"
                >
                  2. Why You Are Leaning This Way
                </label>
                <p className="text-xs text-text-muted mt-0.5">
                  The factors, pros, cons, and inclinations on your mind.
                </p>
              </div>
              <span
                className={`text-[11px] font-mono ${
                  reasoningLength > 0 && !isReasoningValid
                    ? "text-amber-500"
                    : "text-text-muted"
                }`}
              >
                {reasoningLength}/1500 (min 20)
              </span>
            </div>
            <textarea
              id="reasoning-input"
              rows={5}
              value={reasoning}
              onChange={(e) => setReasoning(e.target.value)}
              onBlur={() => setTouched((prev) => ({ ...prev, reasoning: true }))}
              disabled={isLoading}
              placeholder="e.g., I'm leaning toward it because the stipend is good and working with senior engineers will help my career, but I'm worried about missing college exams and living expenses."
              className="w-full px-3.5 py-2.5 bg-surface-elevated border border-subtle text-text-primary placeholder:text-text-muted text-sm focus:outline-none focus:border-strong focus:ring-1 focus:ring-accent-primary transition-colors disabled:opacity-50 resize-y"
              style={{ borderRadius: "var(--radius)" }}
            />
            {touched.reasoning && reasoningLength > 0 && reasoningLength < 20 && (
              <p className="mt-1 text-xs text-amber-500 font-sans">
                Please explain your reasoning in at least 20 characters ({20 - reasoningLength} more needed).
              </p>
            )}
          </div>

          {/* Submit Button: Rectangular, solid fill, padding ~10px 18px, medium weight */}
          <div className="pt-1 flex justify-end">
            <button
              type="submit"
              disabled={!isFormValid || isLoading}
              className={`px-5 py-2.5 font-medium text-sm transition-colors border cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent-primary ${
                isFormValid && !isLoading
                  ? "bg-accent-primary hover:bg-accent-hover text-white border-transparent"
                  : "bg-surface-elevated text-text-muted border-subtle cursor-not-allowed opacity-60"
              }`}
              style={{ borderRadius: "var(--radius)" }}
            >
              Analyze Reasoning
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
