export type FactorCategory =
  | "money"
  | "convenience"
  | "growth"
  | "academics"
  | "health"
  | "relationships"
  | "career"
  | "other";

export interface StatedFactor {
  factor: string;
  category: FactorCategory;
}

export interface Assumption {
  assumption: string;
  why_risky: string;
}

export interface Conflict {
  conflict: string;
  explanation: string;
}

export interface BlindSpot {
  area: string;
  why_it_matters_for_you: string;
}

export interface Question {
  question: string;
  linked_to: string;
}

export interface AnalyzeResponse {
  decision: string;
  stated_factors: StatedFactor[];
  assumptions: Assumption[];
  conflicts: Conflict[];
  blind_spots: BlindSpot[];
  questions: Question[];
}

export interface AnalyzeRequest {
  decision: string;
  reasoning: string;
}
