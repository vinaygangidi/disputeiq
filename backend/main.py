"""
DisputeIQ Backend

FastAPI application that:
- Receives vendor dispute claims via webhook
- Orchestrates the dispute intelligence pipeline
- Streams agent execution via Server-Sent Events (SSE)
- Manages case data and orchestration

Reuses architecture patterns from Cash Application Foundry.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DisputeIQ",
    description="AI-Powered Vendor Dispute Defense System",
    version="0.1.0",
)

# CORS configuration (allow all origins for hackathon demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "mode": "demo",  # fixture mode by default
    }


@app.get("/samples")
async def list_samples():
    """List available demo dispute scenarios"""
    samples_dir = os.path.join(os.path.dirname(__file__), "data", "samples")
    if not os.path.exists(samples_dir):
        return {"scenarios": []}

    scenarios = []
    for scenario_dir in os.listdir(samples_dir):
        scenario_path = os.path.join(samples_dir, scenario_dir)
        if os.path.isdir(scenario_path):
            meta_file = os.path.join(scenario_path, "meta.json")
            if os.path.exists(meta_file):
                with open(meta_file, "r") as f:
                    meta = json.load(f)
                    scenarios.append({
                        "id": scenario_dir,
                        **meta
                    })

    return {"scenarios": scenarios}


@app.post("/analyze")
async def analyze_dispute(claim_data: dict):
    """
    Analyze a vendor dispute claim

    Streams agent execution via Server-Sent Events (SSE)
    """

    async def event_generator():
        """Generate SSE events as agents execute"""

        # TODO: Implement dispute orchestration pipeline
        # 1. Trigger Dispute Intelligence Agent
        # 2. Parse and score claim
        # 3. Route to appropriate stage
        # 4. Return structured result

        # For now, yield placeholder events
        yield f"data: {json.dumps({'event': 'init', 'status': 'starting'})}\n\n"
        yield f"data: {json.dumps({'event': 'agent_start', 'agent': 'dispute_intelligence'})}\n\n"
        yield f"data: {json.dumps({'event': 'agent_complete', 'status': 'demo_mode'})}\n\n"
        yield f"data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DisputeIQ - AI-Powered Vendor Dispute Defense",
        "docs": "/docs",
        "health": "/health",
        "samples": "/samples",
        "analyze": "/analyze (POST)",
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
