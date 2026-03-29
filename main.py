"""
PHANTOM PLAN — FastAPI Backend
Exposes the 6-agent pipeline via REST API.

Endpoints:
  POST /analyze       → Full analysis pipeline (Agents 1-5)
  POST /drift         → Monthly drift monitor (Agent 6)
  GET  /health        → Health check
  GET  /archetypes    → List all 8 archetypes with descriptions
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models import AnalysisRequest, PhantomPlanResponse, DriftRequest, DriftReport
from orchestrator import run_analysis_pipeline, run_drift_pipeline

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY not set — agent calls will fail!")
    else:
        logger.info("Anthropic API key loaded. Backend ready.")
    yield


app = FastAPI(
    title="Phantom Plan API",
    description="Behavioral-first financial planning. We Monte Carlo you, not the market.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "api_key_set": bool(os.getenv("ANTHROPIC_API_KEY")),
        "version": "1.0.0"
    }


@app.get("/archetypes")
async def get_archetypes():
    """Returns all 8 behavioral archetypes with descriptions."""
    return {
        "archetypes": [
            {"name": "Optimist Procrastinator", "tagline": "Plans brilliantly, executes inconsistently."},
            {"name": "Guilt Investor", "tagline": "Invests in bursts after panic, not strategy."},
            {"name": "Social Spender", "tagline": "Hemorrhages money during Indian social obligations."},
            {"name": "Anchor Holder", "tagline": "Irrationally attached to one bad investment."},
            {"name": "Invisible Saver", "tagline": "Actually disciplined but doesn't realize it."},
            {"name": "Crisis Planner", "tagline": "Only acts when something bad happens."},
            {"name": "Delegator", "tagline": "Wants someone else to decide everything."},
            {"name": "Optimizer", "tagline": "Data-driven, just needs the right framework."},
        ]
    }


@app.post("/analyze", response_model=PhantomPlanResponse)
async def analyze(request: AnalysisRequest):
    """
    Full behavioral analysis pipeline.
    Runs Agents 1-5 in sequence and returns complete PhantomPlanResponse.
    
    Expected time: 15-30 seconds (5 LLM calls, 3 models).
    """
    logger.info(f"Analysis request: {request.profile.name}, {len(request.transactions)} transactions")
    
    try:
        result = await run_analysis_pipeline(request)
        logger.info(f"Analysis complete for {request.profile.name}")
        return result
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis pipeline failed: {str(e)}")


@app.post("/drift", response_model=DriftReport)
async def drift_monitor(request: DriftRequest):
    """
    Monthly drift check — Agent 6.
    Re-fingerprints new transactions and computes plan divergence.
    
    Call this monthly with new transaction data to keep the plan alive.
    """
    logger.info(f"Drift check: {request.profile.name}, Month {request.month_number}")
    
    try:
        result = await run_drift_pipeline(request)
        logger.info(f"Drift level: {result.drift_level} (score: {result.drift_score})")
        return result
    except Exception as e:
        logger.error(f"Drift pipeline failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Drift analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
