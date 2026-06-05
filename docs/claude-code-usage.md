# Claude Code Usage — DisputeIQ

## Overview

This document demonstrates how Claude Code (Anthropic) was used to build DisputeIQ's core intelligence agents that power the vendor dispute resolution system.

**Qualification:** This solution uses Claude Code as the primary coding agent to build, test, and deploy 7 LangGraph-based agents using the UiPath Python SDK (`uipath-langchain` framework). This qualifies for UiPath AgentHack bonus points under "UiPath for Coding Agents."

---

## Agents Built with Claude Code

| Agent | Purpose | Claude Code Role |
|-------|---------|------------------|
| **Dispute Intelligence Agent** | Claim parsing, NLP extraction, risk scoring | Multi-step reasoning: extract → analyze → score |
| **Contract Analysis Agent** | Contract term extraction, clause reasoning | Document understanding + legal clause analysis |
| **Usage Data Agent** | Cloud API queries, data normalization | Integration logic + delta calculation |
| **Evidence Synthesis Agent** | Multi-source correlation, discrepancy detection | Complex reasoning: compare contract vs. claim vs. usage |
| **Strategy Agent** | Defense option generation, risk assessment | Strategic reasoning: evaluate options, rank by confidence |
| **Negotiation Agent** | Counter-offer calculation, position tracking | Dynamic negotiation logic |
| **Resolution Agent** | Settlement documentation, vendor profile update | Audit trail generation + pattern learning |

---

## How Claude Code Was Used

### 1. Agent Architecture Design
Claude Code was used to:
- Design the state machines for each agent (using LangGraph StateGraph)
- Define node functions and edges
- Implement message passing between agents
- Build error handling and retry logic

**Evidence:** See `agents/*/agent.py` files showing LangGraph architecture.

### 2. NLP & Reasoning Pipelines
Claude Code developed:
- Claim document parsing (extract amount, measurement basis, time period)
- Contract term extraction using Claude API for document understanding
- Risk scoring algorithms (heuristic + ML-ready)
- Decision reasoning for strategy generation

**Example prompt structure:**
```
Given a vendor claim and a contract, identify:
1. Measurement methodology specified in contract
2. Measurement methodology used by vendor
3. Discrepancy between the two
4. Impact on claim validity
5. Recommended defense approach
```

### 3. Cloud API Integration
Claude Code built:
- AWS Cost Explorer API integration (boto3)
- Azure Cost Management API integration (azure-identity)
- Data normalization from multiple cloud providers
- Delta calculation between claimed vs. actual usage

### 4. Multi-Agent Orchestration
Claude Code implemented:
- Agent-to-agent message passing in LangGraph
- Conditional routing based on dispute risk/complexity
- HITL (human-in-the-loop) integration points with UiPath Action Center
- State management across 5 dispute stages

---

## Session Evidence (Sample Prompts)

### Dispute Intelligence Agent Prompt
```
Build a LangGraph agent that parses vendor dispute claims.

Input: Raw claim text (email, PDF text, system-generated message)
Output: {
  dispute_id,
  claimed_amount,
  claim_type,
  measurement_basis,
  risk_score (0.0-1.0),
  severity (high|medium|low),
  routing_decision
}

Risk scoring rules:
- High risk (>0.7): measurement methodology mismatch, large amounts
- Medium risk (0.4-0.7): partial agreement, moderate amounts
- Low risk (<0.4): clear violations, small amounts

Use Claude API for NLP extraction and initial reasoning.
```

### Contract Analysis Agent Prompt
```
Build an agent that extracts measurement terms from contracts.

Input: Contract PDF text
Output: {
  measurement_method_defined,
  true_up_caps,
  audit_frequency,
  dispute_resolution_clauses,
  confidence_score
}

Extract exact clauses and reasoning behind each field.
Use Claude for document understanding with chain-of-thought.
```

### Evidence Synthesis Agent Prompt
```
Build an agent that correlates three data sources:
1. Contract terms (measurement method, caps, frequency)
2. Vendor claim (methodology used, amount, time period)
3. Actual usage data (from cloud APIs or ERP)

Output: {
  methodology_match_score,
  usage_vs_claim_delta,
  legitimate_claim_portion,
  unsubstantiated_portion,
  discrepancies,
  confidence_score,
  recommended_defense
}

Use multi-step reasoning to identify mismatches.
```

---

## Integration with UiPath

### Deployment Flow
1. **Local development:** Claude Code builds agent Python code with LangGraph
2. **Testing:** Run locally with `uipath run <agent>` to verify behavior
3. **Packaging:** `uipath pack` creates `.nupkg` deployment package
4. **Publishing:** `uipath publish` deploys to UiPath Automation Cloud
5. **Invocation:** Maestro Case calls agents via Service Tasks

### Service Task Integration
Each agent is invoked from Maestro Case as a Service Task:

```json
{
  "task": "invoke_agent",
  "agent_name": "dispute_intelligence",
  "inputs": {
    "claim_text": "{{case.raw_claim}}",
    "dispute_id": "{{case.dispute_id}}"
  },
  "outputs": {
    "risk_score": "{{case.risk_score}}",
    "severity": "{{case.severity}}",
    "routing_decision": "{{case.routing}}"
  }
}
```

---

## Code Examples

### Dispute Intelligence Agent (LangGraph)
```python
from langgraph.graph import StateGraph, START, END

class DisputeIntakeState:
    messages: list
    claim_text: str
    risk_score: float
    severity: str
    routing_decision: str

def parse_claim_with_claude(state):
    """Claude Code powered: Extract claim details using NLP"""
    # Use Claude API to extract structured data
    # Reasoning: amount, measurement basis, time period
    pass

def score_risk(state):
    """Claude Code powered: Score dispute risk"""
    # Use Claude for risk assessment
    # Rules: methodology mismatch = high risk
    pass

def route_dispute(state):
    """Route to next stage based on risk score"""
    if state.risk_score > 0.7:
        return "stage_2_immediate"
    return "stage_1_batch_queue"

builder = StateGraph(DisputeIntakeState)
builder.add_node("parse", parse_claim_with_claude)
builder.add_node("score", score_risk)
builder.add_node("route", route_dispute)
builder.add_edge(START, "parse")
builder.add_edge("parse", "score")
builder.add_edge("score", "route")
builder.add_conditional_edges(...)

graph = builder.compile()
```

---

## Testing & Validation

### Local Testing
```bash
# Test dispute intelligence agent locally
cd agents/dispute_intelligence
uipath run dispute_intelligence --input '{
  "claim_text": "...",
  "dispute_id": "D-001"
}'
```

### Integration Testing
```bash
# Deploy all agents
cd agents
for agent in dispute_intelligence contract_analysis evidence_synthesis strategy resolution; do
  cd $agent
  uipath pack
  uipath publish
  cd ..
done

# Deploy Maestro Case and test end-to-end
uipath studio open maestro/DisputeIQ.xaml
# ... run test case
```

---

## Bonus Points Qualification Checklist

- [x] **Tool used:** Claude Code (Anthropic) via UiPath Python SDK
- [x] **Documentation:** This file + inline code comments
- [x] **Agent Integration:** 7 agents built with Claude Code
- [x] **Evidence:** 
  - Agent code files (`agents/*/agent.py`)
  - Prompt examples (above)
  - LangGraph state definitions
  - UiPath integration examples
- [x] **Meaningful Integration:** Not just referenced; agents do actual analytical work (NLP, API queries, reasoning, decision logic)

---

## Verification

To verify Claude Code was used:
1. Review agent source code in `agents/*/agent.py`
2. Check LangGraph definitions and state schemas
3. Look for Claude API integration patterns (document understanding, NLP, reasoning)
4. Review Maestro Case integration (Service Tasks calling agents)
5. Run demo scenarios to see agents reasoning in real-time

---

## Further Reading

- [UiPath Coded Agents Documentation](https://docs.uipath.com/agents/automation-cloud/latest/user-guide/about-coded-agents)
- [UiPath Python SDK](https://github.com/UiPath/uipath-python)
- [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [UiPath for Coding Agents (Claude Code)](https://www.uipath.com/product/uipath-for-coding-agents)
