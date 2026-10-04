# Security Policy & Architecture

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security & Privacy Guardrails

Blind Spot is designed with security and privacy as first-class constraints:

### 1. Zero Persistence & Privacy
- **Stateless Operation**: No database, ORM, caching store, or persistent storage is used (no PostgreSQL, Prisma, MongoDB, or Redis).
- **No Data Retention**: User decisions and reasoning are processed ephemerally in-memory and discarded immediately after response delivery.
- **Privacy-Preserving Logs**: User decisions, reasoning texts, prompts, and raw AI outputs are never written to server log files or stdout.

### 2. API Key & Secret Management
- **Server-Side Only**: `GEMINI_API_KEY` is loaded strictly on the backend from server environment variables.
- **Zero Secrets in Source**: `.env` is ignored by git and never committed. `.env.example` contains placeholders only.
- **Frontend Isolation**: Secrets are never passed or exposed to the frontend client.

### 3. Input Validation & Request Size Limits
- **Strict Boundary Enforcement**: Inbound requests must satisfy $20 \le \text{characters} \le 1500$ for both `decision` and `reasoning`.
- **Sanitization**: Whitespace is trimmed before validation; empty and whitespace-only payloads are strictly rejected.
- **Extra Fields Forbidden**: Pydantic models forbid unexpected fields (`extra = "forbid"`).
- **Payload Size Capping**: HTTP middleware enforces a strict 50 KB request body limit to reject oversized payloads early.

### 4. Prompt Injection Defense
- **Untrusted Delimiters**: User text is encapsulated inside `<user_decision>`, `<user_reasoning>`, and `<extracted_reasoning>` tags.
- **System Instructions**: System prompts explicitly command the model to treat content inside delimiters strictly as untrusted raw data and ignore all embedded commands or override attempts.

### 5. Recommendation Guardrail
- **Non-Prescriptive Constraint**: The AI is prohibited from recommending options or making decisions for the user.
- **Output Scanning**: Output is scanned using normalized regex patterns for directive phrases (e.g., *"you should"*, *"I recommend"*, *"best option"*, *"definitely choose"*, *"go with"*).
- **One Retry Policy**: Output violating guardrails triggers exactly one retry before failing safely with a generic error.

### 6. API Abuse Protection (Rate Limiting)
- **Sliding-Window Limiter**: Process-local in-memory rate limiter restricts requests to **5 requests per IP per minute** on `POST /api/analyze`.
- **429 Response**: Returns `429 Too Many Requests` with `Retry-After` header when threshold is reached.
- *Limitation Note*: Rate limits are process-local in the MVP and reset upon instance restart.

### 7. CORS Configuration
- **Origin Restriction**: Configured via `ALLOWED_ORIGINS` (defaults to local development origins; configurable for production domains).
- **No Production Wildcards**: Wildcard `allow_origins=["*"]` is forbidden in production.

### 8. Response Security Headers
All responses include standard defensive headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer`
- `Permissions-Policy: accelerometer=(), camera=(), microphone=(), geolocation=()`
- `Content-Security-Policy: default-src 'self'`

### 9. Controlled Error Handling
- **No Information Leakage**: Python tracebacks, internal filesystem paths, Gemini API keys, and raw model errors are never returned to the client.
- **Standardized JSON Responses**: Client errors return standard 4xx responses; internal/provider errors return safe, generic 5xx messages.

---

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly by contacting the maintainers directly. Do not open public issues for sensitive security vulnerabilities.
