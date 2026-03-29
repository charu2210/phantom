"""
AGENT 2 — ARCHETYPE CLASSIFIER
Maps the 14-D Behavioral Signature Vector to one of 8 Indian spending archetypes.
Returns primary archetype, confidence, secondary blend, and a plain-English narrative.
Grounded in Indian financial psychology — not generic MBTI nonsense.
"""

import json
from anthropic import Anthropic
from models import BehavioralSignatureVector, ArchetypeResult

client = Anthropic()

ARCHETYPES = {
    "Optimist Procrastinator": {
        "description": "Plans brilliantly, executes inconsistently. High financial IQ, low follow-through. SIPs get paused, goals get revised, next month is always the fresh start.",
        "key_triggers": ["good_income", "low_savings_consistency", "high_stated_actual_gap"],
        "indian_context": "Very common among salaried professionals in Tier-1 cities aged 25–35."
    },
    "Guilt Investor": {
        "description": "Invests in emotional bursts — panic after market news or guilt after a splurge. No steady cadence. Lump-sum heavy, SIP-light.",
        "key_triggers": ["high_guilt_investment_pattern", "irregular_investments", "reactive"],
        "indian_context": "Often triggered by WhatsApp forwards about gold, crypto, or 'market crash' news."
    },
    "Social Spender": {
        "description": "Hemorrhages money during Indian social obligations — weddings, festivals, gifting, dining out. Financially disciplined in isolation, derailed by relationships.",
        "key_triggers": ["high_social_spend_inflation", "festive_vulnerability", "gifting_spend"],
        "indian_context": "Especially acute in joint/extended family contexts. Wedding season is a financial disaster."
    },
    "Anchor Holder": {
        "description": "Irrationally attached to one bad investment (real estate, LIC policy, one stock). Won't cut losses. Portfolio has a 'sacred cow' that drags everything down.",
        "key_triggers": ["high_anchor_holding", "sunk_cost_behavior", "non_diversified"],
        "indian_context": "LIC endowment plans and ancestral real estate are the classic Indian anchors."
    },
    "Invisible Saver": {
        "description": "Actually disciplined — saves consistently, spends intentionally — but doesn't realize it. Under-invests because they assume they're 'not good with money'.",
        "key_triggers": ["high_savings_consistency", "low_investment_confidence", "conservative"],
        "indian_context": "Often women in dual-income households who manage household budgets but don't invest."
    },
    "Crisis Planner": {
        "description": "Only acts when something bad happens. No proactive financial planning. Insurance bought after illness, emergency fund after job scare, will written after parent's death.",
        "key_triggers": ["high_crisis_reactivity", "reactive_only", "no_proactive_planning"],
        "indian_context": "Very common in first-generation earners who didn't have financial safety nets growing up."
    },
    "Delegator": {
        "description": "Wants someone else to decide everything. High trust in 'expert' opinions — CA uncle, bank RM, mutual fund agent. Low financial self-efficacy.",
        "key_triggers": ["high_delegation_tendency", "agent_reliance", "low_self_research"],
        "indian_context": "Common pattern: 'My CA handles everything.' Often over-exposed to ULIPs and LIC."
    },
    "Optimizer": {
        "description": "Data-driven, researches everything, over-engineers solutions. Paralysis by analysis sometimes. Needs the right framework, not motivation.",
        "key_triggers": ["high_planning_horizon", "low_impulse", "systematic"],
        "indian_context": "The r/IndiaInvestments user who has 12 mutual funds for 'diversification'."
    }
}

SYSTEM_PROMPT = """You are the Archetype Classifier for Phantom Plan.
You receive a 14-dimensional Behavioral Signature Vector and map it to one of exactly 8 archetypes.
Your classification must be grounded in the specific data — not generic.
You also compute a secondary archetype blend (many people are 70% one archetype, 30% another).
Always respond with ONLY valid JSON. No markdown. No preamble."""


def run_archetype_classifier(
    bsv: BehavioralSignatureVector,
    profile_context: str
) -> ArchetypeResult:
    """
    Maps BSV to an archetype with confidence scoring.
    """
    
    archetype_list = "\n".join([
        f"- {name}: {info['description']} | Indian context: {info['indian_context']}"
        for name, info in ARCHETYPES.items()
    ])
    
    # Summarize BSV for the classifier
    bsv_summary = "\n".join([
        f"- {dim}: {data['display']} (score: {data['score']}/100) — {data['signal']}"
        for dim, data in bsv.raw.items()
        if isinstance(data, dict) and 'score' in data
    ])
    
    user_prompt = f"""
Classify this user's behavioral archetype based on their BSV.

USER CONTEXT: {profile_context}

BEHAVIORAL SIGNATURE VECTOR (14 dimensions):
{bsv_summary}

KEY INSIGHT: {bsv.key_insight}
OVERALL BEHAVIORAL HEALTH: {bsv.overall_health}/100

THE 8 ARCHETYPES:
{archetype_list}

Return ONLY this JSON:
{{
  "primary_archetype": "<one of the 8 archetype names exactly>",
  "primary_confidence": <65-94>,
  "secondary_archetype": "<one of the 8 archetype names exactly, different from primary>",
  "secondary_weight": <10-35>,
  "archetype_narrative": "<3–4 sentence non-judgmental explanation of WHY this person is this archetype, referencing their specific transaction signals. Speak directly to the user as 'you'. Warm tone.>",
  "archetype_tagline": "<one punchy sentence that captures their pattern. e.g. 'You save in drafts, not deposits.'>",
  "biggest_strength": "<their genuine financial strength based on the data>",
  "core_vulnerability": "<their most dangerous financial blind spot, specific to their data>",
  "archetype_match_reasoning": "<2 sentences explaining the classification logic — which BSV dimensions drove this decision>"
}}
"""

    response = client.messages.create(
        model="claude-haiku-4-5",  # Fast, cost-efficient for classification
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    raw = response.content[0].text.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    
    return ArchetypeResult(
        primary=result["primary_archetype"],
        confidence=result["primary_confidence"],
        secondary=result["secondary_archetype"],
        secondary_weight=result["secondary_weight"],
        narrative=result["archetype_narrative"],
        tagline=result["archetype_tagline"],
        strength=result["biggest_strength"],
        vulnerability=result["core_vulnerability"],
        reasoning=result["archetype_match_reasoning"]
    )
