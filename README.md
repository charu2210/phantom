# 👻 Phantom Plan — Backend (6-Agent System)

> "We don't Monte Carlo market returns. We Monte Carlo **you**."

---

## Architecture

```
                     ┌─────────────────────────────────┐
                     │      FastAPI (main.py)           │
                     │   POST /analyze   POST /drift    │
                     └────────────┬────────────────────-┘
                                  │
                     ┌────────────▼────────────────────┐
                     │     Orchestrator (stateful)      │
                     │  PipelineState flows through     │
                     │  all agents, enriched each step  │
                     └──┬──────┬──────┬──────┬─────────┘
                        │      │      │      │
          ┌─────────────▼─┐ ┌──▼──┐ ┌▼────┐ ┌▼──────────┐ ┌──────────┐
          │  Agent 1       │ │  2  │ │  3  │ │    4      │ │    5     │
          │  Fingerprint   │ │Arch │ │Plan │ │ Simulate  │ │Guardrail │
          │  (14-D BSV)    │ │type │ │     │ │ (500 sims)│ │Architect │
          │  claude-opus   │ │haiku│ │sonnet│ │  opus     │ │  sonnet  │
          └────────────────┘ └─────┘ └──────┘ └──────────┘ └──────────┘
                                                        
          ┌──────────────────────────────────────────────────────────────┐
          │  Agent 6 — Monthly Drift Monitor (POST /drift endpoint)      │
          │  Re-fingerprints new txns · Computes divergence · Re-sims    │
          │  claude-haiku (cost-efficient monthly runs)                  │
          └──────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
phantom-plan-backend/
├── main.py                    ← FastAPI app, all endpoints
├── orchestrator.py            ← Stateful agent pipeline + fallbacks
├── models.py                  ← Pydantic models (inputs/outputs for all agents)
├── requirements.txt           ← pip dependencies
├── .env.example               ← Copy to .env and add API key
└── agents/
    ├── __init__.py
    ├── agent1_fingerprint.py  ← Behavioral Fingerprinting (14-D BSV)
    ├── agent2_archetype.py    ← Archetype Classifier (8 types)
    ├── agent3_plan.py         ← Financial Plan Constructor (FIRE/SIP/tax)
    ├── agent4_simulation.py   ← Behavioral Monte Carlo (500 simulations)
    ├── agent5_guardrails.py   ← Guardrail Architect (commitment devices)
    └── agent6_drift.py        ← Monthly Drift Monitor (continuous loop)
```

---

## Setup

### 1. Clone & install

```bash
cd phantom-plan-backend
pip install -r requirements.txt
```

### 2. Configure API key

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the server

```bash
python main.py
# OR with auto-reload for development:
uvicorn main:app --reload --port 8000
```

Server starts at: `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

---

## API Reference

### `POST /analyze`

Full 5-agent behavioral analysis. Returns the complete `PhantomPlanResponse`.

**Expected time:** 20–40 seconds (5 LLM calls across 3 models)

**Request body:**
```json
{
  "profile": {
    "name": "Aryan Sharma",
    "age": 26,
    "monthly_income": 75000,
    "fire_target_age": 45,
    "target_monthly_savings": 15000,
    "top_goal": "Build 6-month emergency fund",
    "self_reported_behavior": "I save well for 3 months then blow it on travel"
  },
  "transactions": [
    { "description": "Zomato", "category": "Food", "amount": 3200 },
    { "description": "SIP - Nifty Index", "category": "Investment", "amount": 5000 },
    { "description": "Amazon shopping", "category": "Shopping", "amount": 8500 }
  ],
  "stated_savings_rate": 20.0
}
```

**Response shape:**
```json
{
  "bsv": { "raw": {...}, "overall_health": 54, "key_insight": "..." },
  "archetype": {
    "primary": "Optimist Procrastinator",
    "confidence": 82,
    "secondary": "Guilt Investor",
    "narrative": "...",
    "tagline": "You save in drafts, not deposits.",
    "strength": "...",
    "vulnerability": "..."
  },
  "plan": {
    "monthly_allocation": { "index_fund_sip": 7500, "elss_sip": 3750, ... },
    "fire_projection": { "projected_fire_age": 47, "on_track": false, ... },
    "tax_optimization": { "current_regime_recommendation": "new", ... },
    "milestones": [...]
  },
  "simulation": {
    "summary": { "success_rate": 43, "median_first_failure_month": "Month 7", ... },
    "failure_modes": [...],
    "critical_month": {...},
    "narrative": "..."
  },
  "guardrails": {
    "guardrails": [...],
    "combined_lift": "+28% plan success rate",
    "first_action": "..."
  }
}
```

---

### `POST /drift`

Monthly re-analysis (Agent 6). Call with new transaction data each month.

```json
{
  "profile": { ... },
  "new_transactions": [ ... ],
  "original_bsv_raw": { ... },
  "plan_allocation": { ... },
  "month_number": 2
}
```

**Response:** `DriftReport` with drift score, level (GREEN/AMBER/RED), wins, signals, updated guardrail.

---

### `GET /health`

```json
{ "status": "ok", "api_key_set": true, "version": "1.0.0" }
```

### `GET /archetypes`

Returns all 8 archetypes with taglines.

---

## Model Routing

Each agent uses the right model for cost/quality tradeoff:

| Agent | Task | Model | Why |
|-------|------|-------|-----|
| Agent 1 | 14-D Behavioral Fingerprinting | claude-opus-4-5 | Deep pattern analysis needs best reasoning |
| Agent 2 | Archetype Classification | claude-haiku-4-5 | Fast classification, cost-efficient |
| Agent 3 | Financial Plan Construction | claude-sonnet-4-5 | Balanced — complex but structured |
| Agent 4 | 500 Behavioral Simulations | claude-opus-4-5 | THE core differentiator — needs best model |
| Agent 5 | Guardrail Architecture | claude-sonnet-4-5 | Creative + structured |
| Agent 6 | Monthly Drift Monitor | claude-haiku-4-5 | Runs every month — must be cheap |

---

## Graceful Degradation

Every agent has a hardcoded fallback in `orchestrator.py`. If any agent fails (API timeout, JSON parse error, etc.), the pipeline continues with sensible defaults. **The API never returns a 500 unless ALL agents fail.**

This means the hackathon demo never crashes — even if you have quota issues.

---

## Connecting to the Frontend

The frontend (`index.html`) is pre-configured to call `http://localhost:8000`.

To change the backend URL, edit the top of the `<script>` block:
```js
const BACKEND_URL = "http://localhost:8000"; // ← change this
```

For production deployment (Railway, Render, Fly.io):
```js
const BACKEND_URL = "https://your-app.railway.app";
```

---

## CORS

CORS is open (`allow_origins=["*"]`) for hackathon speed. Lock it down in production to your frontend domain.

---

## Roadmap (Post-Hackathon)

- [ ] Setu Account Aggregator for real UPI/bank feed
- [ ] CAMS/KFintech parser for MF statement overlay  
- [ ] Fine-tune Llama 3.1 8B on Indian spending data for Agent 2 (cost reduction)
- [ ] LangGraph proper integration with persistent memory store
- [ ] WhatsApp / push notification triggers from Agent 6 drift alerts
- [ ] Form 16 / salary slip parser for tax layer
- [ ] PostgreSQL persistence for multi-month behavioral history
