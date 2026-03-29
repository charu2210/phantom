"""
AGENT 6 — MONTHLY DRIFT MONITOR
Re-runs fingerprinting on new transaction data each month.
Computes plan divergence score — how much is the real user drifting 
from the planned user?
Triggers re-simulation if drift > threshold.
Updates guardrails without changing core goals.
"""

import json
from anthropic import Anthropic
from models import BehavioralSignatureVector, FinancialPlan, DriftReport

client = Anthropic()

SYSTEM_PROMPT = """You are the Monthly Drift Monitor for Phantom Plan.
Your job is to compare a user's PLANNED behavior vs their ACTUAL behavior this month,
and produce a non-judgmental drift report.

You look for:
- Savings execution gap (did they save what they planned?)
- Investment continuity (any SIP pauses?)
- Spend category drift (which categories ballooned?)
- Guardrail compliance (did they follow the commitment devices?)
- Archetype regression (are they getting more or less aligned with their archetype?)

Tone: Supportive coach, not disappointed parent. Never shame. 
Acknowledge wins. Flag risks without catastrophizing.

Always respond with ONLY valid JSON. No markdown."""


def run_drift_monitor(
    original_bsv: BehavioralSignatureVector,
    current_month_bsv: BehavioralSignatureVector,
    plan: FinancialPlan,
    month_number: int,
    recent_transactions_summary: str
) -> DriftReport:
    """
    Computes drift between planned and actual behavior.
    """
    
    # Compare key BSV dimensions
    bsv_deltas = {}
    for dim in original_bsv.raw:
        if isinstance(original_bsv.raw.get(dim), dict) and isinstance(current_month_bsv.raw.get(dim), dict):
            orig_score = original_bsv.raw[dim].get("score", 50)
            curr_score = current_month_bsv.raw[dim].get("score", 50)
            bsv_deltas[dim] = {
                "original": orig_score,
                "current": curr_score,
                "delta": curr_score - orig_score,
                "direction": "worsening" if curr_score > orig_score and dim in ["impulse_velocity", "stated_vs_actual_gap"] else "improving"
            }
    
    user_prompt = f"""
Run Month {month_number} drift analysis for this user.

RECENT TRANSACTIONS THIS MONTH:
{recent_transactions_summary}

PLAN TARGETS:
- Monthly savings target: ₹{sum(v for k,v in plan.monthly_allocation.items() if k not in ['lifestyle_budget'])}
- Lifestyle budget: ₹{plan.monthly_allocation.get('lifestyle_budget', 0)}

BSV DIMENSION CHANGES (original → current):
{json.dumps(bsv_deltas, indent=2)}

ORIGINAL BEHAVIORAL HEALTH: {original_bsv.overall_health}/100
CURRENT BEHAVIORAL HEALTH: {current_month_bsv.overall_health}/100
HEALTH DELTA: {current_month_bsv.overall_health - original_bsv.overall_health:+.1f}

Return ONLY this JSON:
{{
  "drift_score": <0-100, where 0=perfectly on track, 100=completely off plan>,
  "drift_level": "<GREEN/AMBER/RED>",
  "month_number": {month_number},
  "headline": "<1 sentence summary of this month — lead with a win if possible>",
  "wins": [
    "<specific win from this month's data>",
    "<another win if applicable>"
  ],
  "drift_signals": [
    {{
      "signal": "<what drifted>",
      "magnitude": "<small/medium/large>",
      "action_needed": "<what to do about it>"
    }}
  ],
  "guardrail_compliance": {{
    "score": <0-100>,
    "assessment": "<how well did they follow their commitment devices?>"
  }},
  "rerun_simulation": <true if drift_score > 30, else false>,
  "updated_guardrail": {{
    "trigger": "<what caused this recommendation>",
    "action": "<specific updated guardrail action for next month>"
  }},
  "motivational_message": "<2 sentences. Acknowledge where they are, point toward next 30 days. Non-toxic positivity — honest and warm.>"
}}
"""

    response = client.messages.create(
        model="claude-haiku-4-5",  # Cost-efficient for monthly runs
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    raw = response.content[0].text.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    
    return DriftReport(
        drift_score=result["drift_score"],
        drift_level=result["drift_level"],
        month_number=result["month_number"],
        headline=result["headline"],
        wins=result["wins"],
        drift_signals=result["drift_signals"],
        guardrail_compliance=result["guardrail_compliance"],
        rerun_simulation=result["rerun_simulation"],
        updated_guardrail=result["updated_guardrail"],
        message=result["motivational_message"]
    )
