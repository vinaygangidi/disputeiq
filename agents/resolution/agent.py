"""
resolution Agent

Stage 1: Claim Intake & Intelligence

Claude Code powered agent that:
- Parses vendor claim documents using NLP
- Extracts key facts (amount, measurement basis, time period)
- Scores risk/severity automatically
- Routes high-risk disputes for immediate processing

Built with UiPath Python SDK (uipath-langchain LangGraph framework).
Bonus points qualification: Claude Code powered.
"""

from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# Agent state schema
class DisputeIntakeState:
    """State for dispute intelligence agent"""

    messages: Annotated[list, add_messages]
    claim_text: str
    dispute_id: str
    vendor_id: str

    # Extracted fields
    claimed_amount: float | None
    claim_type: str | None
    claim_date: str | None
    measurement_basis: str | None

    # Analysis results
    risk_score: float  # 0.0 to 1.0
    severity: str  # "high", "medium", "low"
    flags: list[str]


# Node functions
def parse_claim(state: DisputeIntakeState) -> DisputeIntakeState:
    """Parse claim document and extract structured data

    Claude Code powered step: NLP extraction of claim details
    """
    # TODO: Implement NLP parsing using Claude API
    # Extract: amount, measurement basis, time period, vendor references
    pass


def score_risk(state: DisputeIntakeState) -> DisputeIntakeState:
    """Score dispute risk and severity

    Claude Code powered step: Risk assessment and severity classification
    """
    # TODO: Implement risk scoring logic
    # High risk: measurement methodology mismatch, large amounts, complex terms
    # Medium risk: partial mismatches, moderate amounts
    # Low risk: clear contractual violations, small amounts
    pass


def route_dispute(state: DisputeIntakeState) -> str:
    """Route to appropriate next stage based on risk

    High risk -> immediate Stage 2 processing
    Low risk -> batch queue
    """
    if state.risk_score > 0.7:
        return "stage_2_high_priority"
    else:
        return "stage_1_queue_batch"


# Build graph
def build_graph():
    """Build the dispute intelligence agent graph"""

    builder = StateGraph(DisputeIntakeState)

    # Add nodes
    builder.add_node("parse_claim", parse_claim)
    builder.add_node("score_risk", score_risk)
    builder.add_node("route_dispute", route_dispute)

    # Add edges
    builder.add_edge(START, "parse_claim")
    builder.add_edge("parse_claim", "score_risk")
    builder.add_edge("score_risk", "route_dispute")
    builder.add_conditional_edges(
        "route_dispute",
        lambda x: x,
        {
            "stage_2_high_priority": END,
            "stage_1_queue_batch": END,
        }
    )

    return builder.compile()


# Graph definition for UiPath
graph = build_graph()

if __name__ == "__main__":
    # Test locally
    initial_state = {
        "messages": [],
        "claim_text": "...",
        "dispute_id": "D-001",
        "vendor_id": "V-001",
        "claimed_amount": None,
        "claim_type": None,
        "claim_date": None,
        "measurement_basis": None,
        "risk_score": 0.0,
        "severity": "unknown",
        "flags": [],
    }

    result = graph.invoke(initial_state)
    print(result)
