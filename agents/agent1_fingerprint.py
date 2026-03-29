"""
AGENT 1 — BEHAVIORAL FINGERPRINTING AGENT
Parses transactions, extracts 14-dimensional Behavioral Signature Vector (BSV).
Detects: impulse velocity, stress-spend correlation, savings consistency,
stated-vs-actual gap, social spend inflation, category drift.
"""

import json
from anthropic import Anthropic
from models import Transaction, UserProfile, BehavioralSignatureVector

client = Anthropic()

SYSTEM_PROMPT = """You are the Behavioral Fingerprinting Agent for Phantom Plan — a financial 
behavior analysis system built for Indian users.

Your job: analyze raw transaction data and extract a precise 14-dimensional 
Behavioral Signature Vector (BSV). You reason like a behavioral economist, 
not a budgeting app. You look for PATTERNS and SIGNALS, not just categories.

Key behavioral signals to detect:
1. Impulse Velocity — frequency of unplanned small purchases (food delivery, quick buys)
2. Savings Consistency Score — how regular are investment/savings transactions?
3. Social Spend Inflation — elevated spend around weekends, festivals, gifting
4. Stated vs Actual Gap — difference between claimed savings rate and actual
5. Stress-Trigger Spending — weekend/evening splurges after busy weeks
6. Category Drift — spend creeping up in one category over time
7. Guilt Investment Pattern — lump-sum investments after no activity (panic bursts)
8. Anchor Holding Signal — repeated small withdrawals from one investment
9. Delegation Tendency — lots of "auto" or "standing instruction" transactions
10. Crisis Reactivity — insurance/emergency-related purchases only
11. Festive Season Vulnerability — spike in Oct-Feb spend
12. EMI Burden Ratio — EMI as % of income
13. Discretionary Elasticity — how much does lifestyle spend flex?
14. Planning Horizon Signal — short-term vs long-term investment mix

Always respond with ONLY valid JSON. No markdown. No explanation outside the JSON."""


def run_fingerprinting_agent(
    transactions: list[Transaction],
    profile: UserProfile,
    stated_savings_rate: float
) -> BehavioralSignatureVector:
    """
    Runs the behavioral fingerprinting agent.
    Returns a 14-dimensional BSV dict.
    """
    
    txn_text = "\n".join([
        f"- {t.description} | {t.category} | ₹{t.amount} | {t.date or 'recent'}"
        for t in transactions
    ])
    
    income = profile.monthly_income
    total_spend = sum(t.amount for t in transactions if t.category != "Investment")
    actual_savings_rate = max(0, round(((income - total_spend) / income) * 100, 1))
    
    user_prompt = f"""
Analyze these transactions for {profile.name}, Age {profile.age}, Monthly Income ₹{income}:

TRANSACTIONS:
{txn_text}

FINANCIAL CONTEXT:
- Monthly Income: ₹{income}
- Total Tracked Spend: ₹{total_spend}
- Actual Savings Rate: {actual_savings_rate}%
- Stated/Target Savings Rate: {stated_savings_rate}%
- Stated vs Actual Gap: {stated_savings_rate - actual_savings_rate:+.1f}%

Self-reported behavior: {profile.self_reported_behavior or 'Not provided'}

Return ONLY this JSON object (all scores 0-100, higher = more of that trait):
{{
  "impulse_velocity": {{
    "score": <0-100>,
    "display": "<e.g. HIGH / 72>",
    "signal": "<1 sentence what you observed in the data>",
    "color": "<hex color: red for high risk, amber for medium, green for low>"
  }},
  "savings_consistency": {{
    "score": <0-100>,
    "display": "<e.g. 41%>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "social_spend_inflation": {{
    "score": <0-100>,
    "display": "<LOW/MEDIUM/HIGH>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "stated_vs_actual_gap": {{
    "score": <0-100>,
    "display": "<e.g. -22%>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "stress_trigger_spend": {{
    "score": <0-100>,
    "display": "<LOW/MEDIUM/HIGH>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "guilt_investment_pattern": {{
    "score": <0-100>,
    "display": "<LOW/MEDIUM/HIGH>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "emi_burden_ratio": {{
    "score": <0-100>,
    "display": "<e.g. 28%>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "festive_vulnerability": {{
    "score": <0-100>,
    "display": "<LOW/MEDIUM/HIGH>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "discretionary_elasticity": {{
    "score": <0-100>,
    "display": "<RIGID/FLEXIBLE/ELASTIC>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "planning_horizon": {{
    "score": <0-100>,
    "display": "<SHORT/MEDIUM/LONG>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "crisis_reactivity": {{
    "score": <0-100>,
    "display": "<PROACTIVE/REACTIVE>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "delegation_tendency": {{
    "score": <0-100>,
    "display": "<LOW/MEDIUM/HIGH>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "category_drift_risk": {{
    "score": <0-100>,
    "display": "<STABLE/DRIFTING/HIGH DRIFT>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "anchor_holding_signal": {{
    "score": <0-100>,
    "display": "<LOW/MEDIUM/HIGH>",
    "signal": "<1 sentence observation>",
    "color": "<hex>"
  }},
  "overall_behavioral_health": <0-100>,
  "key_insight": "<1 most important behavioral insight about this person, specific to their data>"
}}
"""

    messages = [{"role": "user", "content": user_prompt}]
    
    response = client.messages.create(
        model="claude-opus-4-5",  # Most capable for deep behavioral analysis
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    
    raw = response.content[0].text
    # Clean any accidental markdown
    raw = raw.replace("```json", "").replace("```", "").strip()
    bsv_dict = json.loads(raw)
    
    return BehavioralSignatureVector(
        raw=bsv_dict,
        overall_health=bsv_dict.get("overall_behavioral_health", 50),
        key_insight=bsv_dict.get("key_insight", "")
    )
