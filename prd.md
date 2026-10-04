# Blind Spot --- Product Requirements Document

## 1. Product Overview

**Product:** Blind Spot\
**Tagline:** Normal AI gives you answers. Blind Spot gives you the
questions you didn't ask yourself.

Blind Spot is an AI-powered decision-reflection tool. A user describes a
decision and explains why they are leaning toward an option. The system
identifies stated factors, hidden assumptions, internal conflicts,
overlooked areas, and Socratic reflection questions.

Blind Spot must never make the decision for the user or recommend an
option.

## 2. Problem Statement

People often make decisions using the most visible information while
overlooking important factors, relying on unstated assumptions, or
missing conflicts in their own reasoning.

The hackathon challenge, "The Blind Spot", requires an AI-powered
solution that helps users discover these gaps without deciding for them.

## 3. Goals

-   Help users identify overlooked factors in their own reasoning.
-   Surface assumptions that may be risky or unverified.
-   Detect conflicts between stated priorities.
-   Generate blind spots tied directly to the user's words.
-   Generate 5--7 concise Socratic questions.
-   Provide a clear, accessible interface.
-   Deploy a working solution within the 3-hour challenge.
-   Optimize for Code Quality, Security, Efficiency, Testing,
    Accessibility, Problem Statement Alignment, and Google Services
    Usage.

## 4. Non-Goals

-   Making decisions for users.
-   Ranking options.
-   Giving a "best choice".
-   Providing professional decisions or guarantees.
-   Building a general-purpose chatbot.
-   Storing user decisions in a database.
-   User accounts or authentication in the MVP.

## 5. Target User

Anyone facing a meaningful personal, academic, career, relationship,
relocation, or similar decision who wants to examine their reasoning
more critically.

## 6. Core User Flow

1.  User opens Blind Spot.
2.  User enters the decision they are considering.
3.  User explains why they are leaning toward it.
4.  User clicks **Find My Blind Spots**.
5.  Frontend sends the input to the Python FastAPI backend.
6.  Server validates the request.
7.  Extractor LLM identifies:
    -   Decision
    -   Stated factors
    -   Assumptions
    -   Conflicts
8.  Challenger LLM identifies:
    -   Blind spots
    -   5--7 Socratic questions
9.  Server validates and applies output guardrails.
10. UI renders the analysis as plain text.
11. User can optionally revise their reasoning and run the analysis
    again.

## 7. Functional Requirements

### FR-01: Decision Input

The interface shall accept a user's decision and why they are leaning
toward it.

Validation: - POST request only. - JSON body only. - Both fields
required. - Trim whitespace. - Each field: 20--1500 characters.

### FR-02: Stated Factors

The system shall extract explicitly stated factors and classify each
as: - money - convenience - growth - academics - health -
relationships - career - other

### FR-03: Assumptions

The system shall identify assumptions reasonably supported by the user's
words and explain why each may be risky.

### FR-04: Conflicts

The system shall identify tensions between goals, priorities, or
statements. If no meaningful conflict exists, return an empty array.

### FR-05: Blind Spots

The system shall generate 3--5 blind spots connected to the user's own
reasoning.

### FR-06: Socratic Questions

The system shall generate 5--7 open-ended reflection questions without
recommending a decision.

### FR-07: Recommendation Guardrail

The system shall reject or regenerate output containing recommendation
language such as: - "you should" - "I recommend" - "choose X" - "best
option" - "definitely choose" - equivalent recommendation phrasing

### FR-08: Results UI

The UI shall show: - Decision - Stated factors - Assumptions - Internal
conflicts - Blind spots - Reflection questions

### FR-09: Balance Meter

If time permits, show a simple visual distribution of the user's stated
factors by category. This is secondary and must not become a decision
score.

### FR-10: Reflect and Re-run

If time permits, allow the user to revise their reasoning and run the
analysis again.

## 8. AI Requirements

The solution uses a two-step LLM chain.

### Step 1 --- Extractor

Output:

``` json
{
  "decision": "string",
  "stated_factors": [
    {
      "factor": "string",
      "category": "money|convenience|growth|academics|health|relationships|career|other"
    }
  ],
  "assumptions": [
    {
      "assumption": "string",
      "why_risky": "string"
    }
  ],
  "conflicts": [
    {
      "conflict": "string",
      "explanation": "string"
    }
  ]
}
```

### Step 2 --- Challenger

Output:

``` json
{
  "blind_spots": [
    {
      "area": "string",
      "why_it_matters_for_you": "string"
    }
  ],
  "questions": [
    {
      "question": "string",
      "linked_to": "string"
    }
  ]
}
```

All generated text should be concise and casual Hinglish.

## 9. UI/UX Requirements

-   Clean, modern, focused interface.
-   Clear primary CTA.
-   Strong visual hierarchy.
-   Mobile responsive.
-   Keyboard accessible.
-   Visible focus states.
-   Labels associated with inputs.
-   Loading state during analysis.
-   Friendly error state.
-   Results should be scannable.
-   AI output rendered as plain text only.

## 10. Security and Privacy Requirements

-   API key only in server-side environment variables.
-   `.env` ignored by Git.
-   `.env.example` contains placeholders only.
-   Server-side Pydantic validation.
-   Prompt injection defense.
-   User input treated as untrusted data.
-   Delimit user input using `<user_decision>`.
-   Strict JSON output.
-   Validate LLM output with Pydantic.
-   Retry invalid output once.
-   Per-IP rate limiting around 5 requests/minute.
-   Token cap.
-   Request timeout.
-   Provider spend limit.
-   Never log or store user decision text.
-   Never expose stack traces or raw provider errors.
-   No `dangerouslySetInnerHTML`.
-   No `eval`.
-   Security headers configured in `vercel.json`.
-   No wildcard CORS.

## 11. Testing Requirements

Test at minimum: - Internship decision. - College decision. - Relocation
decision. - Very short input. - Oversized input. - Empty input. -
Malformed JSON. - Prompt injection attempt. - LLM malformed JSON. -
Recommendation-containing output. - Provider timeout/error. - Rate-limit
behavior. - Live deployed application.

## 12. Hackathon Scope

### Must Have

-   Input form
-   FastAPI analysis endpoint
-   Extractor
-   Challenger
-   Strict structured validation
-   Blind spot cards
-   Assumptions
-   Conflicts
-   5--7 questions
-   Error handling
-   Security controls
-   Deployment
-   Public GitHub repository
-   README
-   SECURITY.md
-   Pre-deploy checklist

### Should Have

-   Reasoning balance meter
-   Preloaded examples
-   Strong loading/error states

### Could Have

-   Reflect-and-rerun
-   Additional visual polish

### Cut First If Time Runs Out

1.  Reflect-and-rerun
2.  Balance meter

Never cut the core extraction, blind spots, questions, security basics,
or deployment.

## 13. Success Metrics

The primary success metric is a strong AI evaluation score across the
seven published criteria.

Product-level indicators: - Users understand the blind spots quickly. -
Blind spots are grounded in their input. - Questions feel reflective
rather than prescriptive. - No recommendation is made. - Application
works reliably on the deployed URL.

## 14. Demo Plan

1.  Explain the problem: people overlook things in their own reasoning.
2.  Enter the internship example.
3.  Show extracted factors.
4.  Show assumptions and conflicts.
5.  Reveal blind spots.
6.  Show Socratic questions.
7.  Run a second, different decision to demonstrate generalization.
8.  Briefly explain the two-step AI pipeline and security.

## 15. Hackathon Submission

Each submission must include: - Public GitHub repository link. -
Deployed working solution link. - Brief project description.

Only the latest submission counts toward the final leaderboard.
