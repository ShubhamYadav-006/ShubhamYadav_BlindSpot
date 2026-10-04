# Blind Spot 🎯

> **"Normal AI gives you answers. Blind Spot gives you the questions you didn't ask yourself."**

Blind Spot is an AI-powered decision-reflection engine. When facing a consequential personal, academic, or career dilemma, people often fixate on prominent factors while missing unstated assumptions, competing priorities, and critical trade-offs.

Blind Spot does **not** make the decision for you or rank options. Instead, it extracts your stated reasoning, uncovers hidden assumptions and internal conflicts, surfaces overlooked angles (blind spots), and poses Socratic reflection questions to help you think clearly.

---

## Key Features

- 🧠 **Structured Reasoning Extraction**: Identifies explicitly stated factors categorized by domain (`money`, `convenience`, `growth`, `academics`, `health`, `relationships`, `career`, `other`).
- 🔍 **Assumption Surfacing**: Detects unverified premises underlying your thinking and explains why each introduces risk.
- ⚖️ **Internal Conflict Detection**: Flags genuine friction between competing goals and priorities.
- 🎯 **Blind Spot Discovery (Centerpiece)**: Pinpoints overlooked perspectives, systemic dependencies, and secondary effects grounded directly in your words.
- ❓ **Socratic Reflection Questions**: Generates 5–7 deep, open-ended questions designed to probe uncertainty without directing the outcome.
- 🛡️ **Zero Recommendation Guardrail**: Strict multi-layer regex and prompt guardrails ensure the AI never tells you what to choose.
- 🔒 **Ephemeral & Privacy-Preserving**: Strictly stateless architecture with zero database storage, no user accounts, and no data retention.

---

## Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite 6, Tailwind CSS 3 | Modern, responsive, accessible decision-reflection UI |
| **Backend** | Python 3.14, FastAPI, Pydantic v2 | High-performance, schema-validated asynchronous API |
| **AI Engine** | Google Gemini (`google-genai` SDK) | 2-Stage pipeline: Extractor stage & Challenger stage |
| **Testing** | Pytest, TestClient | Comprehensive test suite covering validation, guardrails, and security |
| **Deployment** | Vercel (Frontend), Render (Backend) | Production-ready stateless cloud architecture |

---

## Architecture Overview

```text
User Decision + Reasoning Narrative
              │
              │ HTTPS POST /api/analyze
              ▼
   FastAPI Application Gateway
   ├── Payload Size Guard (50 KB max)
   ├── Sliding-Window Rate Limiter (5 req/min per IP)
   ├── Pydantic Input Validation (20–1500 chars)
   │
   ├── [Stage 1] Extractor LLM (Gemini)
   │     └── Extracts: Decision, Stated Factors, Assumptions, Conflicts
   │
   ├── Pydantic Schema Validation & Retry Handler
   │
   ├── [Stage 2] Challenger LLM (Gemini)
   │     └── Generates: Blind Spots (3–5), Socratic Questions (5–7)
   │
   ├── Recommendation Guardrails (Regex Pattern Scanner)
   │
   ▼ Sanitized JSON FinalResponse
React Client UI
   ├── Accessible Focus Management
   └── Scannable Reflection Cards (No recommendation scores)
```

---

## Local Setup & Quickstart

### Prerequisites

- **Python 3.10+** (tested on Python 3.14)
- **Node.js 18+** and **npm**
- **Google Gemini API Key** (obtain from [Google AI Studio](https://aistudio.google.com/))

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment configuration
cp .env.example .env
```

Edit `backend/.env` with your Gemini API credentials:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

Start the backend server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

Health check verification:
```bash
curl http://localhost:8000/health
# Returns: {"status": "ok"}
```

---

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment configuration
cp .env.example .env
```

`frontend/.env` default:
```env
VITE_API_BASE_URL=http://localhost:8000
```

Start the Vite development server:
```bash
npm run dev
```

Open your browser at `http://localhost:5173`.

---

## API Specification

### `POST /api/analyze`

Executes the stateless 2-stage AI analysis pipeline.

#### Request Body
```json
{
  "decision": "Should I accept a 6-month startup internship in Bangalore over continuing college coursework locally?",
  "reasoning": "The stipend is high and working with ex-FAANG founders will accelerate my skills, though living costs are high and attendance might be an issue."
}
```

#### Response (200 OK)
```json
{
  "decision": "Accept a 6-month startup internship in Bangalore over college coursework locally",
  "stated_factors": [
    { "factor": "High stipend", "category": "money" },
    { "factor": "Working with ex-FAANG founders", "category": "growth" },
    { "factor": "High living costs", "category": "money" },
    { "factor": "College attendance requirements", "category": "academics" }
  ],
  "assumptions": [
    {
      "assumption": "Working with experienced founders automatically guarantees effective mentorship.",
      "why_risky": "Founders at early-stage startups often have limited time for structured guidance."
    }
  ],
  "conflicts": [
    {
      "conflict": "Gaining practical work experience vs fulfilling academic attendance criteria.",
      "explanation": "Relocating for a full-time internship directly competes with in-person university attendance."
    }
  ],
  "blind_spots": [
    {
      "area": "Academic Policy & Exam Timelines",
      "why_it_matters_for_you": "If exams overlap with key deliverables, you may face academic penalties without prior college approval."
    }
  ],
  "questions": [
    {
      "question": "What contingency plan do you have if the startup requires 60+ hours a week and conflicts with semester exams?",
      "linked_to": "Academic Policy & Exam Timelines"
    }
  ]
}
```

---

## Security & Privacy Architecture

See [`SECURITY.md`](file:///d:/MERN_PRACTICE/Hack@SKill/SECURITY.md) for full documentation:

1. **Zero Data Retention**: No database, ORM, or cache. Requests are processed in-memory and discarded.
2. **Key Isolation**: `GEMINI_API_KEY` is strictly server-side; zero secrets exist in frontend client bundles.
3. **Prompt Injection Defense**: User input is strictly encapsulated in untrusted delimiters (`<user_decision>`, `<user_reasoning>`).
4. **Rate Limiting**: Sliding-window rate limiting (5 requests/min per IP) prevents API abuse.
5. **Output Guardrails**: Automated regex scanner prevents prescriptive language (*"you should"*, *"choose X"*).
6. **Defensive Headers**: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, and strict `CSP`.

---

## Running Automated Tests

Run the full pytest suite from the project root:

```bash
# Run all 80 unit, integration, and security tests
pytest -v
```

Frontend build and type verification:
```bash
cd frontend
npm run build
```

---

## Production Deployment

- **Frontend**: Deployed on [Vercel](https://vercel.com) (configured via `vercel.json` with security headers).
- **Backend**: Deployed on [Render](https://render.com) as a Python web service running Uvicorn.
- **Production URL**: `https://blindspot-ai.vercel.app` *(Placeholder / Deployed URL)*
- **Backend API**: `https://blindspot-api.onrender.com` *(Placeholder / Deployed URL)*

---

## License & Submission

Built for the **PromptWars 2026 Hackathon** — *The Blind Spot Challenge*.
