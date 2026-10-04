# Blind Spot --- System Design

## 1. Objective

Design a small, secure, stateless AI reasoning system that transforms a
user's decision narrative into structured reasoning gaps and reflection
questions.

## 2. High-Level Architecture

``` text
                    ┌──────────────────────┐
                    │      User / Browser  │
                    └──────────┬───────────┘
                               │ HTTPS
                               ▼
                    ┌──────────────────────┐
                    │ React + TypeScript   │
                    │ Vite + Tailwind      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Python FastAPI       │
                    │ POST /api/analyze    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Pydantic Validation  │
                    │ + Rate Limit         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Extractor LLM        │
                    │ Factors/Assumptions/ │
                    │ Conflicts             │
                    └──────────┬───────────┘
                               │
                         JSON validation
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Challenger LLM       │
                    │ Blind Spots/Questions│
                    └──────────┬───────────┘
                               │
                         JSON validation
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Output Guardrails    │
                    │ Recommendation check│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Sanitized JSON       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Results UI           │
                    └──────────────────────┘
```

## 3. Components

### Frontend

-   Collect decision and reasoning.
-   Client-side UX validation.
-   Submit request.
-   Show loading state.
-   Render results.
-   Show errors.
-   Never expose the provider API key.

### FastAPI Backend

-   Validate HTTP method/content type.
-   Validate request body with Pydantic.
-   Apply rate limiting.
-   Call LLM provider.
-   Validate structured output.
-   Retry invalid output once.
-   Apply recommendation guardrail.
-   Return safe JSON.
-   Return generic errors.

### Extractor

Converts free-form reasoning into structured evidence: - decision -
stated factors - assumptions - conflicts

### Challenger

Uses the extracted reasoning and original user input to identify: -
blind spots - reflection questions

### Output Guardrail

Checks generated strings for recommendation patterns. If detected,
reject and regenerate once.

## 4. Request Contract

``` json
{
  "decision": "string",
  "reasoning": "string"
}
```

Constraints: - JSON only. - Both strings trimmed. - 20--1500 characters
each.

## 5. Response Contract

``` json
{
  "decision": "string",
  "stated_factors": [],
  "assumptions": [],
  "conflicts": [],
  "blind_spots": [],
  "questions": []
}
```

## 6. Failure Handling

  Failure                     Response
  --------------------------- -------------------------
  Wrong method                405
  Invalid content type/body   400
  Validation failure          400 generic message
  Rate limit                  429
  Provider timeout            503/500 generic message
  Invalid LLM JSON            Retry once
  Invalid schema              Retry once
  Recommendation detected     Regenerate once
  Second failure              Generic 500/503

No stack traces or provider errors are sent to the browser.

## 7. Privacy Model

MVP has: - No database. - No authentication. - No user accounts. - No
persistent decision storage.

Decision text should not be logged.

## 8. Performance

-   Keep prompts focused.
-   Limit output tokens.
-   Set provider request timeout.
-   Avoid unnecessary LLM calls.
-   Use exactly two LLM calls in the normal path.
-   One retry is allowed for invalid/unsafe output.

## 9. Rate Limiting

Target: - Approximately 5 requests per IP per minute.

If exceeded:

``` text
HTTP 429
```

## 10. Deployment

Recommended: - React frontend deployed on Vercel. - Python FastAPI
backend deployed on a Python-compatible service such as Render. -
Production HTTPS. - Server-side environment variables.

## 11. Security Headers

Configure: - Content-Security-Policy - X-Content-Type-Options: nosniff -
X-Frame-Options: DENY - Referrer-Policy: no-referrer -
Permissions-Policy

CSP should use `default-src 'self'` and `connect-src 'self'` plus only
explicitly required trusted origins.

## 12. LLM Provider

The application uses a provider abstraction.

Candidate providers: - Gemini - Claude - OpenAI

Because Google Services Usage is an explicit evaluation criterion,
Gemini is a strong candidate.

## 13. Observability

For the MVP: - Do not log user decision text. - Log only safe
operational metadata if needed. - Never log API keys or full provider
responses containing user content.

## 14. Scalability

The system is intentionally stateless: - No database. - No session
dependency. - Serverless-style API architecture.

This is sufficient for the hackathon MVP.
