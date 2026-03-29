"""
AGENT 4 — BEHAVIORAL SIMULATION ENGINE (THE CORE)
This is what makes Phantom Plan different.

We don't Monte Carlo market returns. Everyone does that.
We Monte Carlo YOU — injecting archetype-calibrated life disruptions
into 500 simulated versions of your financial life over 5 years.

Each simulation injects:
- Archetype-specific behavioral failures (the SIP you'll pause, the wedding you'll overspend)
- Realistic Indian life events (job change, medical, festival, family obligations)
- Market conditions (but secondary — behavior is primary)

Output: Exactly where and why most simulated versions of you fail your own plan.
"""

import json
from anthropic import Anthropic
from models import ArchetypeResult, FinancialPlan, SimulationResult

client = Anthropic()

# Archetype-specific disruption libraries
ARCHETYPE_DISRUPTIONS = {
    "Optimist Procrastinator": [
        "Q3 work pressure → 60-day SIP pause (probability: 74%)",
        "New year 'fresh start' → 3 weeks delay in resuming investments",
        "Job switch excitement → 2-month financial limbo",
        "Holiday planning derails savings for the month",
        "'I'll start properly from next salary' — 4x per year on average"
    ],
    "Guilt Investor": [
        "Market dip news → panic lump-sum at wrong time (too high after rally)",
        "3-month guilt-free period → sudden ₹50K dump into random fund",
        "Friend's portfolio brag → impulsive sector fund purchase",
        "Annual bonus → 100% invested in one shot, zero SIP discipline",
        "WhatsApp tip → speculative stock purchase"
    ],
    "Social Spender": [
        "Cousin's wedding in Year 2 → ₹45-80K unplanned spend",
        "Diwali gifting + bonus season → ₹20-40K overflow",
        "Friend's destination wedding → ₹60-120K trip + gift",
        "Birthday celebration culture → ₹5-8K/month on average",
        "Office farewell/joining parties → consistent ₹2-4K/month drain"
    ],
    "Anchor Holder": [
        "LIC policy surrender blocked by sunk cost → ₹5K/month wasted premium",
        "Refuses to sell underperforming stock → opportunity cost compounds",
        "Real estate EMI anchors entire financial plan",
        "Gold accumulation over productive investments",
        "Fixed deposit addiction despite post-tax negative real returns"
    ],
    "Invisible Saver": [
        "Under-invests due to lack of confidence → money sits in savings account",
        "Doesn't negotiate salary → income gap vs peers widens",
        "Avoids equity due to 'risk' → misses 10-year bull run",
        "Keeps emergency fund too large → drag on returns",
        "Never asks for tax optimization → leaves 80C money on table"
    ],
    "Crisis Planner": [
        "No emergency fund → first medical event breaks investment streak",
        "No term insurance → family dependence anxiety triggers bad decisions",
        "Medical event in Year 2 → liquidates SIP to cover costs",
        "Job loss fear → panic-moves equity to FD at market bottom",
        "Parent's health → recurring ₹15-25K/month unplanned expense"
    ],
    "Delegator": [
        "RM recommends ULIP → 5-year lock-in at suboptimal returns",
        "CA 'manages everything' → over-exposure to LIC endowment plans",
        "Trust in friend's tip → concentrated portfolio risk",
        "Avoids reviewing investments → drift goes uncorrected for years",
        "Mis-sold guaranteed return plans → actual returns under inflation"
    ],
    "Optimizer": [
        "Paralysis by analysis → 4-month delay before starting investment",
        "12 mutual funds for 'diversification' → near-identical underlying holdings",
        "Chases best-performing fund → sell low buy high pattern",
        "Over-engineers tax strategy → misses simple 80C deadline",
        "Constant portfolio rebalancing → excess transaction costs"
    ]
}

SYSTEM_PROMPT = """You are the Behavioral Simulation Engine for Phantom Plan.
You run a behavioral Monte Carlo — simulating 500 versions of a person's financial future 
by injecting archetype-calibrated disruptions, NOT just market volatility.

You think like a behavioral economist and actuary combined.
You are specific, data-driven, and non-judgmental.
You identify EXACT failure modes with timing, triggers, and probabilities.

Always respond with ONLY valid JSON. No markdown. No preamble."""


def run_simulation_engine(
    archetype: ArchetypeResult,
    plan: FinancialPlan,
    profile_context: str
) -> SimulationResult:
    """
    Runs the behavioral Monte Carlo simulation.
    """
    
    disruptions = ARCHETYPE_DISRUPTIONS.get(archetype.primary, [])
    disruption_text = "\n".join([f"  {i+1}. {d}" for i, d in enumerate(disruptions)])
    
    fragility_text = "\n".join([
        f"  - {fp['month']}: {fp['risk']} (severity: {fp['severity']})"
        for fp in plan.fragility_points
    ])
    
    user_prompt = f"""
Run a 500-simulation behavioral Monte Carlo for this user.

USER CONTEXT: {profile_context}
ARCHETYPE: {archetype.primary} ({archetype.confidence}% confidence)
ARCHETYPE TAGLINE: {archetype.tagline}
CORE VULNERABILITY: {archetype.vulnerability}

FINANCIAL PLAN:
- Monthly SIP target: ₹{plan.monthly_allocation.get('index_fund_sip', 0) + plan.monthly_allocation.get('elss_sip', 0)}
- FIRE target: {plan.fire_projection.get('projected_fire_age')} years old
- On track currently: {plan.fire_projection.get('on_track')}

KNOWN PLAN FRAGILITY POINTS:
{fragility_text}

ARCHETYPE-SPECIFIC DISRUPTION LIBRARY (inject these into simulations):
{disruption_text}

SIMULATION PARAMETERS:
- Horizon: 5 years (60 months)
- Simulations: 500
- Primary variable: Behavioral execution probability per month
- Secondary variable: Market returns (Nifty 50 historical distribution: mean 14%, std 18%)
- Disruption injection: Archetype-calibrated, probability-weighted

Return ONLY this JSON:
{{
  "simulation_summary": {{
    "total_simulations": 500,
    "success_rate": <% of simulations where user hits 80%+ of plan goals>,
    "failure_rate": <100 - success_rate>,
    "median_first_failure_month": "<e.g. Month 7>",
    "average_plan_completion": <% of plan goals completed across simulations>,
    "behavioral_drag": "<% reduction in returns due to behavioral failures vs pure market simulation>"
  }},
  "top_failure_modes": [
    {{
      "rank": 1,
      "icon": "<single emoji>",
      "title": "<short title, 4-6 words>",
      "trigger": "<exact event that causes this failure>",
      "timing": "<when this typically happens, e.g. Month 5-7, or Q3 Year 1>",
      "probability": <40-85>,
      "financial_impact": "<₹ amount or % plan derailment>",
      "description": "<2 sentences: what happens and why it compounds. Very specific to this archetype>",
      "cascade_effect": "<what goes wrong AFTER this failure if uncorrected>"
    }},
    {{
      "rank": 2,
      "icon": "<emoji>",
      "title": "<short title>",
      "trigger": "<exact trigger>",
      "timing": "<when>",
      "probability": <30-70>,
      "financial_impact": "<amount>",
      "description": "<2 sentences>",
      "cascade_effect": "<cascade>"
    }},
    {{
      "rank": 3,
      "icon": "<emoji>",
      "title": "<short title>",
      "trigger": "<exact trigger>",
      "timing": "<when>",
      "probability": <20-55>,
      "financial_impact": "<amount>",
      "description": "<2 sentences>",
      "cascade_effect": "<cascade>"
    }}
  ],
  "critical_month": {{
    "month": "<e.g. Month 7 or Month 14>",
    "why_critical": "<exact scenario that makes this the highest-risk month>",
    "survival_rate": <% of simulations that survive this month intact>
  }},
  "simulation_narrative": "<3–4 sentence summary of what the simulations reveal. Speak to the user directly. Be specific about their archetype pattern. End with what this means for their plan.>",
  "best_case_scenario": "<what happens in the 20% of simulations where everything works — what did those versions of this person do differently?>",
  "worst_case_scenario": "<what happens in the bottom 10% of simulations — the compounding disaster path>"
}}
"""

    response = client.messages.create(
        model="claude-opus-4-5",  # Most capable — this is the core differentiator
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    raw = response.content[0].text.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    
    return SimulationResult(
        summary=result["simulation_summary"],
        failure_modes=result["top_failure_modes"],
        critical_month=result["critical_month"],
        narrative=result["simulation_narrative"],
        best_case=result["best_case_scenario"],
        worst_case=result["worst_case_scenario"]
    )
