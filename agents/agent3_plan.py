"""
AGENT 3 — FINANCIAL PLAN CONSTRUCTOR
Builds a standard FIRE/SIP/tax-aware financial plan, then injects
archetype-specific constraints and behavioral friction points into the structure.
The plan is built to be stress-tested by Agent 4.
"""

import json
from anthropic import Anthropic
from models import UserProfile, ArchetypeResult, FinancialPlan

client = Anthropic()

SYSTEM_PROMPT = """You are the Financial Plan Constructor for Phantom Plan.
You build realistic, India-specific financial plans grounded in behavioral reality — not textbook theory.

You know:
- Indian tax slabs (old vs new regime), Section 80C, 80D, HRA
- SIP mechanics, index funds, ELSS, PPF, NPS
- FIRE calculations for Indian cost of living
- Emergency fund standards (6–12 months expenses)
- Insurance needs (term + health)

CRITICAL: You don't build an idealized plan. You build a plan that accounts for WHO this person actually is.
The archetype shapes the STRUCTURE of the plan — not just the advice.

Always respond with ONLY valid JSON. No markdown."""


def run_plan_constructor(
    profile: UserProfile,
    archetype: ArchetypeResult,
    bsv_health: float
) -> FinancialPlan:
    """
    Constructs a behavioral-aware financial plan.
    """
    
    income = profile.monthly_income
    fire_age = profile.fire_target_age or 45
    current_age = profile.age or 28
    years_to_fire = fire_age - current_age
    target_monthly_savings = profile.target_monthly_savings or int(income * 0.25)
    
    user_prompt = f"""
Build a behavioral-aware financial plan for this user.

PROFILE:
- Name: {profile.name}
- Age: {current_age}
- Monthly Income: ₹{income}
- FIRE Target Age: {fire_age} ({years_to_fire} years)
- Target Monthly Savings: ₹{target_monthly_savings}
- Top Goal: {profile.top_goal or 'Financial independence'}
- Behavioral Health Score: {bsv_health}/100

ARCHETYPE: {archetype.primary} (confidence: {archetype.confidence}%)
- Core Vulnerability: {archetype.vulnerability}
- Biggest Strength: {archetype.strength}
- Secondary Archetype: {archetype.secondary} ({archetype.secondary_weight}%)

Return ONLY this JSON:
{{
  "monthly_allocation": {{
    "emergency_fund_sip": <amount in ₹, 0 if already built>,
    "index_fund_sip": <amount>,
    "elss_sip": <amount for tax saving>,
    "ppf_monthly": <amount>,
    "nps_monthly": <amount>,
    "term_insurance_premium": <monthly equivalent>,
    "health_insurance_premium": <monthly equivalent>,
    "lifestyle_budget": <remaining for discretionary>,
    "buffer_fund": <archetype-specific buffer, e.g. wedding buffer for social spender>
  }},
  "allocation_rationale": "<2 sentences on why this specific split, referencing the archetype>",
  "fire_projection": {{
    "target_corpus": <₹ amount needed for FIRE>,
    "monthly_sip_needed": <₹>,
    "projected_fire_age": <age>,
    "assumed_return_rate": <% annual>,
    "inflation_assumed": <% annual>,
    "on_track": <true/false>
  }},
  "tax_optimization": {{
    "current_regime_recommendation": "<old/new>",
    "section_80c_utilized": <₹ per year>,
    "estimated_tax_saved": <₹ per year>,
    "key_action": "<one specific tax action for this person>"
  }},
  "emergency_fund_status": {{
    "target": <₹ — 6x monthly expenses>,
    "months_to_build": <at current savings rate>,
    "priority": "<high/medium/low>"
  }},
  "archetype_plan_modifications": [
    "<modification 1: how the plan structure is adapted for this archetype>",
    "<modification 2>",
    "<modification 3>"
  ],
  "plan_fragility_points": [
    {{
      "month": "<e.g. Month 3, or 'Festive Season'>",
      "risk": "<what could go wrong>",
      "severity": "<high/medium/low>"
    }},
    {{
      "month": "<e.g. Month 7>",
      "risk": "<what could go wrong>",
      "severity": "<high/medium/low>"
    }},
    {{
      "month": "<e.g. Year 2>",
      "risk": "<what could go wrong>",
      "severity": "<high/medium/low>"
    }}
  ],
  "one_year_milestones": [
    {{"month": 1, "milestone": "<specific, measurable>"}},
    {{"month": 3, "milestone": "<specific, measurable>"}},
    {{"month": 6, "milestone": "<specific, measurable>"}},
    {{"month": 12, "milestone": "<specific, measurable>"}}
  ]
}}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    raw = response.content[0].text.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    
    return FinancialPlan(
        monthly_allocation=result["monthly_allocation"],
        allocation_rationale=result["allocation_rationale"],
        fire_projection=result["fire_projection"],
        tax_optimization=result["tax_optimization"],
        emergency_fund=result["emergency_fund_status"],
        archetype_modifications=result["archetype_plan_modifications"],
        fragility_points=result["plan_fragility_points"],
        milestones=result["one_year_milestones"]
    )
