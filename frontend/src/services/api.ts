import { AnalyzeRequest, AnalyzeResponse } from "../types/analysis";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/+$/, "");

export class ApiError extends Error {
  status?: number;
  code?: string;

  constructor(message: string, status?: number, code?: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

/**
 * Defensive runtime validator for the backend response shape.
 */
function isValidAnalyzeResponse(data: unknown): data is AnalyzeResponse {
  if (!data || typeof data !== "object") {
    return false;
  }

  const res = data as Record<string, unknown>;

  if (typeof res.decision !== "string") {
    return false;
  }

  if (
    !Array.isArray(res.stated_factors) ||
    !Array.isArray(res.assumptions) ||
    !Array.isArray(res.conflicts) ||
    !Array.isArray(res.blind_spots) ||
    !Array.isArray(res.questions)
  ) {
    return false;
  }

  return true;
}

/**
 * Parses error responses safely without leaking raw server paths, credentials, or stack traces.
 */
function parseSafeErrorMessage(status: number, errorBody: unknown): string {
  if (status === 429) {
    return "Too many requests right now. Please wait a moment and try again.";
  }

  if (status === 413) {
    return "Your input is too large. Please shorten your decision or reasoning.";
  }

  if ((status === 400 || status === 422) && errorBody && typeof errorBody === "object") {
    const detail = (errorBody as Record<string, unknown>).detail;
    if (typeof detail === "string" && detail.length > 0 && detail.length < 200) {
      return detail;
    }
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0];
      if (first && typeof first === "object" && typeof first.msg === "string") {
        const cleanMsg = first.msg.replace(/^Value error,\s*/i, "");
        if (cleanMsg.length > 0 && cleanMsg.length < 150) {
          return cleanMsg;
        }
      }
    }
    return "Please ensure both your decision and reasoning are between 20 and 1500 characters.";
  }

  if (status >= 500) {
    return "Something went wrong while analyzing your reasoning. Please try again.";
  }

  return "Something went wrong while analyzing your reasoning. Please try again.";
}

/**
 * Sends a decision and reasoning to the Blind Spot FastAPI backend for reflection analysis.
 */
export async function analyzeDecision(
  request: AnalyzeRequest
): Promise<AnalyzeResponse> {
  const url = `${API_BASE_URL}/api/analyze`;

  let response: Response;
  try {
    response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        decision: request.decision.trim(),
        reasoning: request.reasoning.trim(),
      }),
    });
  } catch (err) {
    // Network failure / server unreachable
    throw new ApiError(
      "Couldn't connect to Blind Spot. Please check your connection and try again.",
      0,
      "NETWORK_ERROR"
    );
  }

  if (!response.ok) {
    let errorData: unknown = null;
    try {
      errorData = await response.json();
    } catch {
      // Non-JSON error response
    }

    const safeMessage = parseSafeErrorMessage(response.status, errorData);
    throw new ApiError(safeMessage, response.status);
  }

  let data: unknown;
  try {
    data = await response.json();
  } catch {
    throw new ApiError(
      "Received an unexpected response format from the server. Please try again.",
      response.status,
      "PARSE_ERROR"
    );
  }

  if (!isValidAnalyzeResponse(data)) {
    throw new ApiError(
      "Received an unexpected response structure. Please try again.",
      response.status,
      "SCHEMA_MISMATCH"
    );
  }

  return data;
}

/**
 * Health check helper for testing backend connectivity.
 */
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      headers: { Accept: "application/json" },
    });
    if (!res.ok) return false;
    const json = await res.json();
    return json?.status === "ok" || json?.status === "healthy";
  } catch {
    return false;
  }
}
