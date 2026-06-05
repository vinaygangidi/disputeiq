# DisputeIQ

AI-Powered Vendor Dispute Defense System on UiPath Maestro Case + Claude Code

> Built for UiPath AgentHack 2026 (Track 1: Maestro Case)

**Live Demo:** [Coming soon — awaiting UiPath Labs access]

---

## What Problem Does This Solve?

Enterprise IT organizations under a CIO routinely face vendor claims worth $500K+ (cloud overages, software license true-ups, usage audits). Today these disputes are resolved manually over 3–6 months with scattered evidence, no audit trail, and significant financial risk.

**Real examples:**
- Cloud vendor claims $500K overage for exceeding committed spend, but uses different time window than contract specifies
- Software vendor claims $250K license true-up for 150 concurrent users, but vendor counts connections (not sessions) — actual = 112 users
- Consulting firm claims $180K for out-of-scope work with ambiguous SOW language — 40% legitimate, 60% unsubstantiated

**Current approach:** Hire consultants, manually review everything, argue with vendor for 6 months, settle for 60% of claim. Cost: $50K-$200K per dispute. Time: 3–6 months.

**DisputeIQ approach:** Each dispute is a **Maestro Case** with AI agents gathering evidence autonomously and humans deciding at critical gates. Result: resolution in weeks, not months, with full audit trail showing evidence considered and reasoning applied.

---

## How It Works: The 5-Stage Case Lifecycle

```
Claim Arrives
    ↓
Stage 1: Claim Intake & Intelligence
    [Claude Code Agent → risk scoring, claim parsing, auto-triage]
    ↓
Stage 2: Evidence Gathering
    [Claude Code Agents → contract analysis, usage data queries, discrepancy detection]
    ↓
Stage 3: Defense Strategy & Human Decision
    [Claude Code Agent → defense option generation] → [Human Legal/Finance review]
    ↓
Stage 4: Negotiation (Agent-Assisted)
    [Claude Code Agent → negotiation support] + [Human negotiator]
    ↓
Stage 5: Resolution & Learning
    [Claude Code Agents → settlement documentation, vendor risk profile update]
    ↓
Case Closed (with full audit trail)
```

### Stage 1: Claim Intake & Intelligence
- **Trigger:** Vendor claim arrives (email, letter, portal notification)
- **Agents:** Dispute Intelligence Agent (Claude Code)
  - Parses claim document using NLP
  - Extracts key facts: claimed amount, measurement basis, time period
  - Scores risk/severity automatically
  - Routes high-risk disputes to Stage 2 immediately; low-risk queued for batch review
- **Output:** Case created with severity score, extracted details, initial risk flags

### Stage 2: Evidence Gathering
- **Agents:** Contract Analysis, Usage Data, Evidence Synthesis (Claude Code)
  - **Contract Analysis:** Extracts exact terms from contract PDF
    - What measurement method is specified?
    - What are true-up caps and audit frequency limits?
    - What dispute resolution clauses apply?
  - **Usage Data:** Queries cloud cost APIs (AWS Cost Explorer, Azure Cost Management) for actual usage
  - **Evidence Synthesis:** Correlates contract terms vs. vendor claim vs. actual usage
    - Identifies measurement methodology mismatches
    - Calculates actual vs. claimed delta
    - Generates evidence report with confidence score
- **Human:** Legal reviews extracted contract terms for accuracy (SLA: 72 hours, escalate to Legal Manager if breached)
- **Output:** Evidence package with contract terms, usage data, discrepancies, confidence score

### Stage 3: Defense Strategy & Human Decision
- **Agent:** Strategy Agent (Claude Code)
  - Analyzes evidence, generates defense options:
    - **Option A:** Challenge measurement methodology (if contract specifies different method)
    - **Option B:** Accept partial liability (if usage exceeded but vendor overstated)
    - **Option C:** Reject in full (if vendor error confirmed)
  - Ranks options by confidence and financial impact
- **Human:** Senior Legal/Finance review in Action Center
  - Decision form shows claim, evidence, agent recommendations side-by-side
  - Outputs: `{decision: fight|negotiate|settle, authorized_amount, notes}`
  - SLA: 48h reminder, 5-day escalate to CIO/VP
- **Routing:** DMN Decision Table routes to Stage 4 (negotiate), Stage 5 (fight), or auto-reject
- **Output:** Approved defense strategy with authorized parameters

### Stage 4: Negotiation (Agent-Assisted)
- **Agent:** Negotiation Agent (Claude Code)
  - Monitors vendor responses as negotiation progresses
  - Re-analyzes with new information
  - Generates counter-offer positions
- **Human:** Negotiator updates case via Action App as negotiation evolves
- **Loop:** Vendor responds → agent re-analyzes → human decides → continue or resolve
- **Output:** Negotiation log, updated positions, settlement parameters

### Stage 5: Resolution & Learning
- **Agents:** Resolution Agent + Learning Agent (Claude Code)
  - **Resolution:** Documents final settlement, posts payment instruction to ERP
  - **Learning:** Extracts patterns and updates vendor risk profile
    - "This vendor overstates claims by ~15% on average"
    - "When vendor claims X, historical accuracy is Y%"
  - **Notification:** Sends resolution notice to vendor
- **Output:** Closed case with full audit trail, updated vendor risk profile, lessons learned

---

## UiPath Components Used

| Component | Purpose |
|-----------|---------|
| **Maestro Case** | Orchestrates dispute lifecycle with stages, SLAs, escalations, human decision gates |
| **Agent Builder** | Low-code agents for notification and triage (future: claim classification) |
| **Document Understanding (IXP)** | Extracts data from vendor claim PDFs and contract documents |
| **Action Center + Action Apps** | Human review forms for Legal, Finance, Negotiators |
| **API Workflows** | Connects to cloud cost APIs, ERP systems for data retrieval |
| **Coded Agents (Python SDK `uipath-langchain`)** | Claude-powered agents for intelligence, reasoning, analysis |
| **Orchestrator Buckets** | Stores dispute documents and evidence artifacts |
| **Orchestrator Assets** | Stores API keys, configuration, thresholds |

---

## Claude Code Agents (Bonus Points)

**All 7 coded agents built with Claude Code using UiPath's Python SDK (`uipath-langchain` LangGraph framework):**

| Agent | Stage | Purpose |
|-------|-------|---------|
| **Dispute Intelligence Agent** | 1 | NLP claim parsing, risk scoring, severity classification, auto-triage |
| **Contract Analysis Agent** | 2 | Contract term extraction, measurement method analysis, clause reasoning |
| **Usage Data Agent** | 2 | Cloud API queries (AWS/Azure), data normalization, delta calculation |
| **Evidence Synthesis Agent** | 2 | Multi-source correlation, discrepancy identification, confidence scoring |
| **Strategy Agent** | 3 | Defense option generation, risk assessment, recommendation ranking |
| **Negotiation Agent** | 4 | Counter-offer calculation, vendor response analysis, position tracking |
| **Resolution Agent** | 5 | Settlement documentation, vendor risk profile update, audit trail generation |

**Evidence of Claude Code usage:** See `docs/claude-code-usage.md` for prompt logs, session transcripts, and agent integration details.

---

## Demo Scenarios (Pre-Built Fixtures)

### Scenario 1: Cloud Overage Dispute
**Setup:** AWS claims $500K overage for exceeding committed spend by 30%
- Contract specifies: calendar month measurement
- Vendor uses: billing cycle measurement (5 days offset)
- Actual usage: within committed limits if measured correctly
- **Agent output:** Methodology mismatch identified, dispute liability = $0
- **Resolution:** Vendor drops claim

### Scenario 2: Software License True-Up
**Setup:** Vendor claims $250K for 150 concurrent users vs. 100-user contract
- Contract defines: concurrent sessions (not connections)
- Vendor counts: connections (includes idle sessions)
- Actual usage: 112 concurrent sessions
- **Agent output:** Methodology dispute documented, legitimate portion = $60K
- **Resolution:** Settlement at $60K

### Scenario 3: Consulting Scope Creep
**Setup:** Consulting firm claims $180K for out-of-scope work
- SOW language: ambiguous around feature customization scope
- Agent analysis: $80K legitimate, $100K unsubstantiated
- Vendor willingness: flexible given client relationship
- **Agent output:** Recommendation = split difference
- **Resolution:** Settlement at $90K ($80K legitimate + $10K goodwill)

---

## Repository Structure

```
disputeiq/
├── README.md                                  # This file
├── LICENSE                                    # MIT
├── .gitignore
│
├── maestro/
│   ├── DisputeIQ.xaml                        # Maestro Case definition (exported from Studio Web)
│   └── README.md                             # Setup instructions for Maestro
│
├── agents/                                    # Claude Code powered Coded Agents
│   ├── dispute_intelligence/
│   │   ├── agent.py                          # LangGraph agent definition
│   │   ├── pyproject.toml                    # Python package config
│   │   └── langgraph.json                    # Graph definition (auto-generated)
│   ├── contract_analysis/
│   │   ├── agent.py
│   │   ├── pyproject.toml
│   │   └── langgraph.json
│   ├── evidence_synthesis/
│   │   ├── agent.py
│   │   ├── pyproject.toml
│   │   └── langgraph.json
│   ├── strategy/
│   │   ├── agent.py
│   │   ├── pyproject.toml
│   │   └── langgraph.json
│   ├── resolution/
│   │   ├── agent.py
│   │   ├── pyproject.toml
│   │   └── langgraph.json
│   └── README.md                             # Agent development guide
│
├── backend/
│   ├── main.py                               # FastAPI webhook + SSE streaming
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── data/
│   │   └── samples/
│   │       ├── scenario_1_cloud_overage/
│   │       │   ├── meta.json                 # Scenario metadata
│   │       │   ├── vendor_claim.json         # Raw claim document
│   │       │   ├── contract.pdf              # Sample contract
│   │       │   └── usage_data.json           # Cloud usage data
│   │       ├── scenario_2_license_trueup/
│   │       │   └── ... (same structure)
│   │       └── scenario_3_scope_creep/
│   │           └── ... (same structure)
│   └── README.md                             # Backend setup
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── DisputeCase.tsx               # Case timeline view
│   │   │   ├── EvidencePanel.tsx             # Contract vs. usage comparison
│   │   │   ├── AgentActivity.tsx             # Live agent streaming
│   │   │   └── DecisionGate.tsx              # Human review interface
│   │   └── styles/
│   └── README.md                             # Frontend setup
│
├── docs/
│   ├── architecture.md                       # Full technical architecture
│   ├── claude-code-usage.md                  # Claude Code bonus points documentation
│   ├── maestro-case-design.md               # Maestro Case definition details
│   ├── agent-prompts.md                     # System prompts for each agent
│   └── deployment.md                        # Deployment to UiPath Automation Cloud
│
└── .github/
    └── workflows/
        └── ci.yml                            # GitHub Actions CI (lint + test)
```

---

## Quick Start (Once UiPath Labs Access Arrives)

### 1. Prerequisites
```bash
# Python 3.11+
python --version

# UiPath CLI
npm install -g @uipath/cli

# Clone repo
git clone https://github.com/vinaygangidi/disputeiq.git
cd disputeiq
```

### 2. Set Up Coded Agents
```bash
cd agents/dispute_intelligence
pip install -e .
uipath auth  # Browser-based authentication to UiPath Cloud
uipath init
uipath run dispute_intelligence --input '{"claim_text": "..."}'
```

### 3. Deploy to UiPath Automation Cloud
```bash
uipath pack
uipath publish
```

### 4. Define Maestro Case in Studio Web
- Open UiPath Studio Web
- Import `maestro/DisputeIQ.xaml`
- Configure Service Tasks to invoke deployed agents
- Configure Action Center User Tasks for human review
- Deploy to Automation Cloud

### 5. Test End-to-End
```bash
cd backend
pip install -r requirements.txt
python main.py  # Starts webhook receiver on localhost:8000

# In another terminal, trigger a demo scenario:
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d @backend/data/samples/scenario_1_cloud_overage/vendor_claim.json
```

---

## Setup Instructions (Detailed)

See individual README files in each directory:
- **Backend setup:** `backend/README.md`
- **Frontend setup:** `frontend/README.md`
- **Coded agents setup:** `agents/README.md`
- **Maestro Case setup:** `maestro/README.md`

---

## Architecture & Design

Full technical documentation: `docs/architecture.md`

Key design decisions:
- **Case over Process:** Disputes are inherently variable (each one is unique). Maestro Case paradigm fits better than rigid BPMN.
- **Multi-stage with HITL:** Each stage has clear human decision gates. Agents propose, humans decide.
- **Evidence-driven:** Every decision is documented with evidence, reasoning, and confidence scores. Satisfies audit & compliance requirements.
- **Audit trail:** Maestro logs every decision, evidence, and reasoning. Supports dispute resolution challenges and compliance reviews.

---

## Bonus Points: Claude Code Usage

This solution uses Claude Code (Anthropic) via UiPath's Python SDK (`uipath-langchain` LangGraph framework) to build all 7 coded agents that power the system.

**What was built with Claude Code:**
- Multi-step reasoning agents for contract analysis, evidence synthesis, and strategy generation
- NLP pipelines for claim parsing and risk scoring
- API integration with cloud cost platforms
- Complex decision logic for dispute routing and settlement calculation

**Evidence:**
- See `docs/claude-code-usage.md` for detailed documentation
- Session transcripts and prompts showing Claude Code usage
- Agent code showing integration with UiPath platform

---

## Submission Details

**Track:** UiPath AgentHack 2026 — Track 1 (Maestro Case)

**GitHub:** https://github.com/vinaygangidi/disputeiq (public, MIT license)

**Components:**
- Maestro Case orchestration (5 stages, HITL gates, SLAs)
- 7 Claude Code powered agents (Python `uipath-langchain`)
- Document Understanding for contract/claim PDFs
- Action Center forms for human review
- FastAPI + React dashboard

**Demo scenarios:** 3 pre-built dispute cases (fixtures)

---

## Contributing

This is a hackathon submission. Contributions welcome after the competition ends.

---

## License

MIT — See LICENSE file for details.

---

## Contact

**Team:** DisputeIQ (UiPath AgentHack 2026 participant)

Questions? See `docs/` directory or GitHub Issues.
