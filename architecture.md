# Blind Spot --- Architecture

## 1. Architecture Style

Blind Spot uses a **small, stateless web architecture** optimized for a
3-hour hackathon build.

``` text
React + TypeScript + Vite + Tailwind
                │
                │ HTTPS
                ▼
       Python + FastAPI Backend
                │
                ├── Pydantic Validation
                ├── Rate Limit
                ├── Prompt Builder
                ├── Extractor LLM
                ├── Pydantic Output Validation
                ├── Challenger LLM
                ├── Pydantic Output Validation
                └── Recommendation Guardrail
                │
                ▼
           Sanitized JSON
                │
                ▼
          React Results UI
```

## 2. Technology Stack

### Frontend

-   React
-   TypeScript
-   Vite
-   Tailwind CSS

### Backend

-   Python
-   FastAPI
-   Pydantic

### AI

-   Gemini API is the preferred candidate because Google Services Usage
    is an explicit evaluation criterion.
-   Claude/OpenAI remain possible provider alternatives.

### Hosting

-   Frontend: Vercel
-   Backend: Render or another Python-compatible deployment platform

### Storage

-   None for MVP.

### Version Control

-   Git
-   GitHub

## 3. Suggested Project Structure

``` text
blind-spot/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DecisionForm.tsx
│   │   │   ├── Results.tsx
│   │   │   ├── FactorList.tsx
│   │   │   ├── AssumptionCard.tsx
│   │   │   ├── ConflictCard.tsx
│   │   │   ├── BlindSpotCard.tsx
│   │   │   ├── QuestionList.tsx
│   │   │   └── BalanceMeter.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── analyze.py
│   │   ├── schemas/
│   │   │   ├── request.py
│   │   │   └── response.py
│   │   ├── prompts/
│   │   │   ├── extractor.py
│   │   │   └── challenger.py
│   │   ├── services/
│   │   │   ├── llm.py
│   │   │   ├── guardrails.py
│   │   │   └── rate_limit.py
│   │   └── config.py
│   ├── requirements.txt
│   └── .env.example
│
├── tests/
│
├── SECURITY.md
├── README.md
├── vercel.json
└── .gitignore
```

## 4. Frontend Architecture

### App

Controls: - Input state. - Loading state. - Error state. - Results
state.

### DecisionForm

Fields: - Decision. - Reasoning / why the user is leaning toward it.

Primary CTA: **Find My Blind Spots**

### Results

Sections: 1. Your Decision 2. What You're Considering 3. Assumptions 4.
Conflicts 5. Blind Spots 6. Questions to Ask Yourself

Optional: - Balance Meter. - Reflect & Re-run.

## 5. API Architecture

Endpoint:

``` text
POST /api/analyze
```

Pipeline:

``` text
Request
  ↓
Method/content-type check
  ↓
Pydantic input validation
  ↓
Rate limit
  ↓
Extractor
  ↓
Pydantic extractor validation
  ↓
Challenger
  ↓
Pydantic challenger validation
  ↓
Recommendation phrase scan
  ↓
Final response
```

## 6. Environment Variables

Example:

``` text
LLM_API_KEY=your_provider_key
LLM_MODEL=your_selected_model
```

Never commit real credentials.

## 7. Provider Abstraction

Conceptual interface:

``` python
class LLMProvider:
    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str
    ):
        ...
```

This keeps the provider replaceable.

## 8. Security Architecture

### Secrets

``` text
Browser
   X
   │ API key never exposed
   │
FastAPI Server
   │
   └── LLM Provider
```

### Input

``` text
Untrusted User Text
       ↓
Delimit
       ↓
Prompt
       ↓
LLM
```

### Output

``` text
LLM JSON
   ↓
Pydantic
   ↓
Recommendation Guard
   ↓
Safe Response
```

## 9. Google Services Consideration

The published hackathon evaluation explicitly includes **Google Services
Usage**.

Therefore, the preferred AI provider is **Gemini**, subject to final API
availability and setup.

If another provider is selected, any Google service should be added only
if it meaningfully improves the product and can be implemented safely
within the 3-hour limit.

Do not add meaningless integrations solely for appearance.

## 10. Deployment Architecture

``` text
GitHub Repository
       │
       ├───────────────┐
       ▼               ▼
   Vercel            Render
 Frontend            FastAPI
       │               │
       └───────HTTPS───┘
               │
               ▼
          Gemini API
```

## 11. Security Headers

Frontend/deployment configuration should include: -
Content-Security-Policy - X-Content-Type-Options: nosniff -
X-Frame-Options: DENY - Referrer-Policy: no-referrer -
Permissions-Policy

Avoid wildcard CORS.

## 12. Architecture Priorities

1.  Problem alignment.
2.  Reliable AI pipeline.
3.  Security.
4.  Accessibility.
5.  Deployment stability.
6.  Testing.
7.  Visual polish.
8.  Optional features.

## 13. 3-Hour Delivery Plan

### 0:00--0:20

-   Finalize prompts.
-   Finalize schemas.
-   Test three decisions.

### 0:20--1:10

-   FastAPI endpoint.
-   Provider integration.
-   Validation.
-   Guardrails.
-   Basic input form.

### 1:10--2:00

-   Results UI.
-   Blind spot cards.
-   Assumptions.
-   Conflicts.
-   Questions.
-   Balance meter if time permits.

### 2:00--2:30

-   Deploy frontend.
-   Deploy backend.
-   Test production API.
-   Fix deployment issues.

### 2:30--2:50

-   Polish UI.
-   Error states.
-   Example decisions.

### 2:50--3:00

-   README.
-   SECURITY.md.
-   Pre-deploy checklist.
-   GitHub cleanup.
-   Submission preparation.

## 14. Final Architecture Principle

Blind Spot is not an "AI that knows the answer."

It is:

``` text
USER'S THINKING
      ↓
EXTRACT
      ↓
CHALLENGE
      ↓
REFLECT
```

The system's job ends with better questions---not a decision.
