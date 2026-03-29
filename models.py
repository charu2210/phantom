"""
Pydantic data models shared across all agents.
These define the clean interfaces between agents in the pipeline.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any


# ── INPUT MODELS ──────────────────────────────────────────────────

class Transaction(BaseModel):
    description: str
    category: str  # Food, Transport, Shopping, Entertainment, Investment, EMI, Medical, Utilities, Gifting, Other
    amount: float
    date: Optional[str] = None  # ISO date string, optional for MVP


class UserProfile(BaseModel):
    name: str
    age: int
    monthly_income: float
    fire_target_age: Optional[int] = 45
    target_monthly_savings: Optional[float] = None
    top_goal: Optional[str] = None
    self_reported_behavior: Optional[str] = None


class AnalysisRequest(BaseModel):
    """
    Full input payload sent to /analyze endpoint.
    """
    profile: UserProfile
    transactions: list[Transaction]
    stated_savings_rate: Optional[float] = 20.0  # % of income user claims to save


# ── AGENT OUTPUT MODELS ──────────────────────────────────────────

class BehavioralSignatureVector(BaseModel):
    """Output of Agent 1 — Behavioral Fingerprinting"""
    raw: dict[str, Any]          # Full 14-D BSV dict
    overall_health: float        # 0-100 composite behavioral health score
    key_insight: str             # Most important behavioral insight


class ArchetypeResult(BaseModel):
    """Output of Agent 2 — Archetype Classifier"""
    primary: str
    confidence: int
    secondary: str
    secondary_weight: int
    narrative: str               # 3-4 sentence non-judgmental explanation
    tagline: str                 # Punchy one-liner
    strength: str                # Genuine financial strength
    vulnerability: str           # Core blind spot
    reasoning: str               # Classification logic


class FinancialPlan(BaseModel):
    """Output of Agent 3 — Financial Plan Constructor"""
    monthly_allocation: dict[str, Any]     # SIPs, EMIs, buffers
    allocation_rationale: str
    fire_projection: dict[str, Any]        # Corpus, timeline, on-track status
    tax_optimization: dict[str, Any]       # 80C, regime recommendation
    emergency_fund: dict[str, Any]         # Target, timeline
    archetype_modifications: list[str]     # How plan is adapted for archetype
    fragility_points: list[dict[str, Any]] # Known weak spots in the plan
    milestones: list[dict[str, Any]]       # 1, 3, 6, 12 month milestones


class SimulationResult(BaseModel):
    """Output of Agent 4 — Behavioral Simulation Engine"""
    summary: dict[str, Any]            # 500-sim aggregate stats
    failure_modes: list[dict[str, Any]] # Top 3 ranked failure modes
    critical_month: dict[str, Any]      # The highest-risk single month
    narrative: str                      # 3-4 sentence plain-English summary
    best_case: str                      # What happens in top 20%
    worst_case: str                     # What happens in bottom 10%


class GuardrailSet(BaseModel):
    """Output of Agent 5 — Guardrail Architect"""
    guardrails: list[dict[str, Any]]   # 6 commitment devices (2 HIGH, 2 MED, 2 NTH)
    combined_lift: str                  # Total estimated success rate improvement
    first_action: str                   # Single most important action TODAY


class DriftReport(BaseModel):
    """Output of Agent 6 — Monthly Drift Monitor"""
    drift_score: int           # 0-100
    drift_level: str           # GREEN / AMBER / RED
    month_number: int
    headline: str
    wins: list[str]
    drift_signals: list[dict[str, Any]]
    guardrail_compliance: dict[str, Any]
    rerun_simulation: bool
    updated_guardrail: dict[str, Any]
    message: str               # Supportive closing message


# ── FULL RESPONSE MODEL ──────────────────────────────────────────

class PhantomPlanResponse(BaseModel):
    """
    Complete response from /analyze endpoint.
    Aggregates outputs from all 5 active agents.
    """
    # Agent 1
    bsv: BehavioralSignatureVector
    
    # Agent 2
    archetype: ArchetypeResult
    
    # Agent 3
    plan: FinancialPlan
    
    # Agent 4
    simulation: SimulationResult
    
    # Agent 5
    guardrails: GuardrailSet
    
    # Metadata
    analysis_version: str = "1.0"
    sebi_disclaimer: str = (
        "This analysis is for educational and planning purposes only. "
        "It does not constitute investment advice. All projections are illustrative. "
        "Please consult a SEBI-registered investment advisor before making financial decisions."
    )


class DriftRequest(BaseModel):
    """Input for /drift endpoint (monthly re-analysis)"""
    profile: UserProfile
    new_transactions: list[Transaction]
    original_bsv_raw: dict[str, Any]
    plan_allocation: dict[str, Any]
    month_number: int
