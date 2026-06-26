# 👻 Phantom

> **We don't Monte Carlo market returns. We Monte Carlo you.**

An AI-powered behavioral financial planning system that predicts **how your financial habits—not just the market—affect your future wealth.**

Traditional financial planners assume you'll stick to the plan.

**Phantom assumes you won't.**

Instead of asking *"What if the market crashes?"*, Phantom asks:

* What if you skip your SIP after three months?
* What if lifestyle inflation catches up?
* What if impulse purchases become more frequent?
* What if your financial discipline slowly drifts over time?

Using a multi-agent AI architecture, Phantom analyzes spending behavior, builds a personalized financial roadmap, simulates hundreds of possible behavioral futures, and continuously adapts as your habits evolve.

---

## Why Phantom?

Financial planning today focuses almost entirely on **market uncertainty**.

Human behavior causes far more financial plans to fail than market volatility.

Phantom shifts the focus from predicting markets to predicting **people**.

| Traditional Financial Planning | Phantom                              |
| ------------------------------ | ------------------------------------ |
| Assumes perfect discipline     | Models real human behavior           |
| Static financial plan          | Adaptive behavioral planning         |
| Market-based simulations       | Behavior-based simulations           |
| One-time recommendations       | Continuous monthly monitoring        |
| Generic advice                 | Personalized AI-generated guardrails |

---

# Demo

> **Frontend:** *(Add deployment link here)*

> **Backend API:** *(Add deployment link here)*

> **Video Demo:** *(Add YouTube link here)*

---

# Features

## Behavioral Fingerprinting

Extracts a 14-dimensional Behavioral Signature Vector (BSV) from user transactions.

Examples include:

* Spending consistency
* Present bias
* Impulse tendency
* Savings discipline
* Goal persistence
* Lifestyle inflation risk
* Financial resilience

---

## Financial Archetype Detection

Classifies every user into behavioral archetypes such as:

* Optimist Procrastinator
* Guilt Investor
* Lifestyle Maximizer
* Goal Chaser
* Stability Seeker

Each archetype includes:

* Confidence score
* Strengths
* Weaknesses
* Personalized narrative
* Actionable insights

---

## AI Financial Plan

Generates a personalized financial roadmap including:

* Monthly allocation strategy
* SIP recommendations
* Emergency fund planning
* FIRE projection
* Tax optimization
* Milestones

---

## Behavioral Monte Carlo Simulation

Unlike traditional Monte Carlo simulations that randomize market returns, Phantom randomizes **human decisions**.

Examples:

* Skipping investments
* Overspending
* Salary growth
* Unexpected expenses
* Lifestyle inflation
* Motivation decay

500 behavioral futures are simulated to estimate the probability of long-term financial success.

---

## Personalized Guardrails

Instead of simply saying *"Spend less,"* Phantom creates commitment systems such as:

* Automatic savings rules
* Spending caps
* Emergency fund triggers
* Investment automation
* Monthly accountability checkpoints

---

## Monthly Drift Monitoring

Financial behavior changes over time.

Each month Phantom:

* Re-analyzes transactions
* Detects behavioral drift
* Measures divergence from the original plan
* Updates recommendations
* Suggests new guardrails

---

# Example Workflow

```
User uploads transactions
            │
            ▼
Behavioral Fingerprinting
            │
            ▼
Financial Archetype Detection
            │
            ▼
AI Financial Planning
            │
            ▼
500 Behavioral Simulations
            │
            ▼
Behavioral Guardrails
            │
            ▼
Monthly Drift Monitoring
```

---

# Example

### Input

```
Income:
₹75,000

Goal:
Retire by 45

Behavior:
"I save consistently for three months,
then spend heavily on travel."
```

↓

### Behavioral Fingerprint

```
Savings Discipline: 61

Impulse Risk: 82

Present Bias: 76

Consistency: 54
```

↓

### Archetype

```
Optimist Procrastinator
Confidence: 82%
```

↓

### Simulation

```
500 behavioral futures

Success Probability:
43%

Most likely failure:
Month 7
```

↓

### Guardrail

```
Automatically transfer bonuses
into emergency savings before
they reach the spending account.
```

---

# Architecture

```
                     ┌─────────────────────────────────┐
                     │      FastAPI (main.py)          │
                     │ POST /analyze   POST /drift     │
                     └────────────┬────────────────────┘
                                  │
                     ┌────────────▼────────────────────┐
                     │         Orchestrator            │
                     │ Stateful multi-agent pipeline   │
                     └──┬──────┬──────┬──────┬─────────┘
                        │      │      │      │
                        ▼      ▼      ▼      ▼

                 Agent 1  Behavioral Fingerprint
                 Agent 2  Archetype Detection
                 Agent 3  Financial Plan
                 Agent 4  Behavioral Simulation
                 Agent 5  Guardrails
                 Agent 6  Drift Monitoring
```

---

# Multi-Agent System

## Agent 1 — Behavioral Fingerprint

Produces a 14-dimensional Behavioral Signature Vector from spending history.

**Model**

Claude Opus 4.5

---

## Agent 2 — Archetype Classifier

Assigns one of eight behavioral financial personalities.

**Model**

Claude Haiku 4.5

---

## Agent 3 — Financial Planner

Builds personalized investment and savings strategies.

Includes:

* FIRE roadmap
* SIP allocation
* Tax optimization
* Milestones

**Model**

Claude Sonnet 4.5

---

## Agent 4 — Behavioral Simulation

Runs 500 behavioral futures to estimate plan success.

**Model**

Claude Opus 4.5

---

## Agent 5 — Guardrail Architect

Designs commitment systems that reduce behavioral risk.

**Model**

Claude Sonnet 4.5

---

## Agent 6 — Drift Monitor

Runs monthly behavioral reassessments.

**Model**

Claude Haiku 4.5

---

# Tech Stack

### Backend

* FastAPI
* Python
* Pydantic
* Anthropic Claude API

### Frontend

* HTML
* CSS
* JavaScript

### AI

* Multi-Agent Orchestration
* Behavioral Reasoning
* Monte Carlo Simulation

---

# Repository Structure

```
phantom-plan-backend/
│
├── main.py
├── orchestrator.py
├── models.py
├── requirements.txt
├── .env.example
│
└── agents/
    ├── agent1_fingerprint.py
    ├── agent2_archetype.py
    ├── agent3_plan.py
    ├── agent4_simulation.py
    ├── agent5_guardrails.py
    └── agent6_drift.py
```

---

# Installation

## Clone

```bash
git clone <repository-url>

cd phantom-plan-backend
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

```
cp .env.example .env
```

Add:

```
ANTHROPIC_API_KEY=YOUR_KEY
```

---

## Run

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

---

# API

## POST /analyze

Runs the complete five-agent behavioral analysis.

Returns:

* Behavioral fingerprint
* Archetype
* Financial plan
* Monte Carlo simulation
* Personalized guardrails

---

## POST /drift

Monthly behavioral re-analysis.

Returns:

* Drift score
* Behavioral changes
* Updated recommendations
* New guardrails

---

## GET /health

Returns service status.

---

## GET /archetypes

Returns all supported behavioral archetypes.

---

# Model Routing

| Agent                  | Model             | Reason                             |
| ---------------------- | ----------------- | ---------------------------------- |
| Behavioral Fingerprint | Claude Opus 4.5   | Deep reasoning                     |
| Archetype              | Claude Haiku 4.5  | Fast classification                |
| Planning               | Claude Sonnet 4.5 | Structured reasoning               |
| Simulation             | Claude Opus 4.5   | Complex behavioral modeling        |
| Guardrails             | Claude Sonnet 4.5 | Creative reasoning                 |
| Drift                  | Claude Haiku 4.5  | Cost-efficient recurring inference |

---

# Design Decisions

### Why Multi-Agent?

Separating responsibilities makes each component easier to evaluate, improve, and replace independently.

### Why Behavioral Simulation?

Most financial plans fail because of inconsistent human behavior rather than poor investment products.

### Why Claude?

Different models are selected based on reasoning complexity and cost efficiency.

### Why Graceful Degradation?

Every agent has a fallback, ensuring the pipeline continues even if an individual model fails.

---

# Current Limitations

* Uses manually provided transaction data
* No direct banking integrations
* No persistent user history
* Monthly monitoring is API-driven
* Prototype optimized for hackathon deployment

---

# Roadmap

## Integrations

* Setu Account Aggregator
* CAMS
* KFintech

## AI

* Fine-tuned open-source behavioral models
* Persistent agent memory
* LangGraph orchestration

## User Experience

* WhatsApp reminders
* Push notifications
* Mobile application

## Infrastructure

* PostgreSQL
* Authentication
* User dashboard
* Long-term behavioral analytics

---

# Contributing

Contributions, feature requests, and discussions are welcome.

Please open an issue before submitting large changes.

---

# License

MIT License.

---

> **Phantom doesn't predict markets.**
>
> **It predicts the person making the decisions.**
