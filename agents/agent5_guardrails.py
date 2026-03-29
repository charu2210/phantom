"""
AGENT 5 — GUARDRAIL ARCHITECT
Reads the failure simulation report and builds archetype-specific 
commitment devices into the plan.

These are NOT advice. They are PRE-WIRED ACTIONS — behavioral economics 
interventions designed to route around the user's own failure modes.

Draws from: commitment devices, mental accounting, pre-commitment theory,
loss aversion framing, friction design, defaults architecture (Thaler & Sunstein).
"""

import json
from anthropic import Anthropic
from models import ArchetypeResult, SimulationResult, GuardrailSet

client = Anthropic()

# Behavioral economics intervention library
INTERVENTION_TYPES = {
    "commitment_device": "Pre-commit to behavior before temptation arrives. Make deviation costly.",
    "friction_addition": "Add friction to bad behavior — extra steps, confirmation delays, cooling-off periods.",
    "friction_removal": "Remove friction from good behavior — auto-debit, one-click investing.",
    "mental_accounting": "Create separate 'buckets' for specific purposes to prevent cross-contamination.",
    "loss_framing": "Frame the cost of inaction as a loss, not a missed gain.",
    "social_accountability": "Use a partner, public commitment, or tracking system as external accountability.",
    "micro_milestone": "Break large goals into 11-day checkpoints — small enough to never feel overwhelming.",
    "if_then_rule": "Pre-decided 'if X happens, then I will Y' — removes in-the-moment willpower requirement.",
    "buffer_fund": "Pre-allocated bucket for predictable disruptions so they don't raid the main plan.",
    "default_setting": "Set the right behavior as default — inaction now means the plan succeeds."
}

SYSTEM_PROMPT = """You are the Guardrail Architect for Phantom Plan.
You design behavioral commitment devices — pre-wired actions that protect a financial plan 
from the user's own predictable failure modes.

You draw from behavioral economics: commitment devices, loss aversion, mental accounting,
friction design, if-then planning, defaults architecture.

These are NOT generic advice. They are SPECIFIC, ACTIONABLE interventions
designed for this exact archetype and their exact failure modes.

The best guardrails are:
1. Automatic (require zero willpower once set up)
2. Proportional (sized to the risk they're protecting against)  
3. Non-punitive (make it easy to succeed, not hard to fail)
4. Specific to Indian financial products and context

Always respond with ONLY valid JSON. No markdown."""


def run_guardrail_architect(
    archetype: ArchetypeResult,
    simulation: SimulationResult,
    plan_context: str
) -> GuardrailSet:
    """
    Designs behavioral guardrails based on simulation failure modes.
    """
    
    failure_summary = "\n".join([
        f"  {fm['rank']}. {fm['title']} (prob: {fm['probability']}%) — {fm['trigger']}"
        for fm in simulation.failure_modes
    ])
    
    intervention_library = "\n".join([
        f"  - {k}: {v}" for k, v in INTERVENTION_TYPES.items()
    ])
    
    user_prompt = f"""
Design behavioral guardrails for this user.

ARCHETYPE: {archetype.primary}
TAGLINE: {archetype.tagline}
CORE VULNERABILITY: {archetype.vulnerability}
CORE STRENGTH: {archetype.strength}

TOP FAILURE MODES FROM SIMULATION:
{failure_summary}

CRITICAL MONTH: {simulation.critical_month.get('month')} — {simulation.critical_month.get('why_critical')}

PLAN CONTEXT: {plan_context}

BEHAVIORAL ECONOMICS INTERVENTION TYPES AVAILABLE:
{intervention_library}

Design 6 guardrails — 2 high priority, 2 medium, 2 nice-to-have.
Each guardrail must:
- Directly address a specific failure mode from the simulation
- Name the intervention type it uses
- Give exact implementation steps (specific to Indian banking/investment products)
- Estimate the % improvement in plan success rate

Return ONLY this JSON:
{{
  "guardrails": [
    {{
      "priority": "HIGH",
      "icon": "<single emoji>",
      "title": "<4-6 word name>",
      "intervention_type": "<one of the intervention types>",
      "failure_mode_addressed": "<which simulation failure mode this fixes>",
      "description": "<2 sentences: what it is and why it works for this archetype>",
      "implementation": {{
        "step1": "<exact action — e.g. 'Log into HDFC NetBanking → Standing Instructions → SIP on 2nd of month'>",
        "step2": "<next action>",
        "step3": "<next action if needed, else null>"
      }},
      "estimated_success_lift": "<e.g. +12% plan success rate>",
      "time_to_set_up": "<e.g. 15 minutes>"
    }},
    {{
      "priority": "HIGH",
      "icon": "<emoji>",
      "title": "<title>",
      "intervention_type": "<type>",
      "failure_mode_addressed": "<failure mode>",
      "description": "<2 sentences>",
      "implementation": {{
        "step1": "<action>",
        "step2": "<action>",
        "step3": "<action or null>"
      }},
      "estimated_success_lift": "<lift>",
      "time_to_set_up": "<time>"
    }},
    {{
      "priority": "MEDIUM",
      "icon": "<emoji>",
      "title": "<title>",
      "intervention_type": "<type>",
      "failure_mode_addressed": "<failure mode>",
      "description": "<2 sentences>",
      "implementation": {{
        "step1": "<action>",
        "step2": "<action>",
        "step3": "<action or null>"
      }},
      "estimated_success_lift": "<lift>",
      "time_to_set_up": "<time>"
    }},
    {{
      "priority": "MEDIUM",
      "icon": "<emoji>",
      "title": "<title>",
      "intervention_type": "<type>",
      "failure_mode_addressed": "<failure mode>",
      "description": "<2 sentences>",
      "implementation": {{
        "step1": "<action>",
        "step2": "<action>",
        "step3": "<action or null>"
      }},
      "estimated_success_lift": "<lift>",
      "time_to_set_up": "<time>"
    }},
    {{
      "priority": "NICE_TO_HAVE",
      "icon": "<emoji>",
      "title": "<title>",
      "intervention_type": "<type>",
      "failure_mode_addressed": "<failure mode>",
      "description": "<2 sentences>",
      "implementation": {{
        "step1": "<action>",
        "step2": "<action>",
        "step3": "<action or null>"
      }},
      "estimated_success_lift": "<lift>",
      "time_to_set_up": "<time>"
    }},
    {{
      "priority": "NICE_TO_HAVE",
      "icon": "<emoji>",
      "title": "<title>",
      "intervention_type": "<type>",
      "failure_mode_addressed": "<failure mode>",
      "description": "<2 sentences>",
      "implementation": {{
        "step1": "<action>",
        "step2": "<action>",
        "step3": "<action or null>"
      }},
      "estimated_success_lift": "<lift>",
      "time_to_set_up": "<time>"
    }}
  ],
  "combined_success_lift": "<total estimated improvement in plan success rate if all HIGH guardrails implemented>",
  "first_action_today": "<the single most important thing this person should do TODAY, in the next 30 minutes>"
}}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    raw = response.content[0].text.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    
    return GuardrailSet(
        guardrails=result["guardrails"],
        combined_lift=result["combined_success_lift"],
        first_action=result["first_action_today"]
    )
