# DisputeIQ

Vendor dispute defense scaffold on UiPath + LangGraph: 5 agent stubs, FastAPI backend. Pipeline unimplemented.

![Language](https://img.shields.io/badge/language-Python-blue?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/vinaygangidi/disputeiq?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

> **Status: incomplete scaffold.** This was a UiPath AgentHack 2026 (Track 1) submission
> built while waiting on UiPath Labs access that did not arrive. The architecture, agent
> topology, and dispute scenarios are worked out; the agent logic is not implemented. See
> [Limitations](#limitations) before evaluating this as working software.

## What This Does

Sketches a system for defending against vendor overbilling disputes — the recurring
enterprise problem where a vendor claims money owed based on a measurement methodology
that differs from what the contract specifies.

The design intent is a five-stage case lifecycle on UiPath Maestro, with LangGraph agents
handling intake, evidence gathering, strategy, negotiation support, and resolution, and
human approval gates at the decisions that matter. What exists today is the FastAPI
scaffold, the LangGraph graph wiring, and three fully specified dispute scenarios.

The domain modeling is the substantive part. Each scenario captures a real methodology
mismatch — claimed basis versus actual contractual basis — and its resolution.

## How It Works

Two of the four endpoints are implemented:

| Method | Path | Status | Description |
|---|---|---|---|
| `GET` | `/health` | ✅ Works | Returns status, version, and `mode: demo` |
| `GET` | `/samples` | ✅ Works | Reads `meta.json` from each scenario directory |
| `GET` | `/` | ✅ Works | Endpoint index |
| `POST` | `/analyze` | ⚠️ Stub | Yields 3 hardcoded SSE events, then `[DONE]`. Does not analyze the posted claim |

Each agent under `agents/` defines a LangGraph `StateGraph` with the same three nodes:

```
START → parse_claim → score_risk → route_dispute → END
                                         │
                        risk_score > 0.7 ├→ stage_2_high_priority
                        otherwise        └→ stage_1_queue_batch
```

The graph compiles and the routing threshold is real. `parse_claim` and `score_risk` are
`pass` with `# TODO` comments, so the state they are meant to populate stays empty and
`route_dispute` always reads `risk_score` as its initial `0.0`.

### Dispute scenarios

The three fixtures in `backend/data/samples/` are the most complete artifact here:

| Scenario | Claim | Methodology mismatch | Modeled outcome |
|---|---|---|---|
| Cloud overage (AWS) | $500K | Vendor measured by calendar month; contract caps by billing cycle | Liability reduced to $0 |
| License true-up | $250K | Vendor counted 150 connections; contract defines 112 concurrent sessions | Settled at $60K |
| Consulting scope creep | $180K | SOW ambiguous on feature customization | $80K legitimate, $100K unsubstantiated; settled at $90K |

## Quickstart

Only the backend runs. There is no frontend and no deployable UiPath package.

1. Clone and install:
   ```bash
   git clone https://github.com/vinaygangidi/disputeiq.git
   cd disputeiq/backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start the service:
   ```bash
   python main.py          # or: uvicorn main:app --reload --port 8000
   ```

3. Exercise the working endpoints:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/samples
   ```

4. `POST /analyze` accepts any JSON object and returns the same placeholder stream
   regardless of input:
   ```bash
   curl -N -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" -d '{}'
   ```

### Agents

Each agent is a separate installable package. They are not wired into the backend.

```bash
cd agents/dispute_intelligence
pip install -e .
python agent.py       # compiles the graph and invokes it with a placeholder state
```

Running an agent directly will not produce useful output — the node functions return
`None`.

## Configuration

The code reads exactly one environment variable. `load_dotenv()` is called, so a
`backend/.env` file is honored.

| Name | Required | Default | Description |
|---|---|---|---|
| `PORT` | No | `8000` | Port for the uvicorn server when running `python main.py` |

No credentials are read anywhere. `requirements.txt` pins `openai`, `boto3`,
`azure-identity`, and `azure-storage-blob`, but none of these are imported by any file in
the repository — no API key, AWS profile, or Azure credential is needed or used.

## Limitations

- **The dispute pipeline is not implemented.** `POST /analyze` yields three hardcoded SSE
  events and ignores the posted claim entirely. No agent is invoked.
- **`parse_claim` and `score_risk` are empty.** Both are `pass` with `# TODO`. There is no
  NLP extraction and no risk scoring anywhere in the repository — roughly 21 TODO or stub
  markers remain across the codebase.
- **The five agents are the same file.** `dispute_intelligence`, `evidence_synthesis`,
  `strategy`, `resolution`, and `contract_analysis` are byte-identical apart from one
  docstring line. They are five copies of one scaffold, not five specialists. Each has its
  own `pyproject.toml` with a distinct package name.
- **No LLM is called.** Nothing imports `openai`, `anthropic`, or any model client, despite
  `openai==1.3.0` being pinned and the README history describing "Claude Code powered"
  agents.
- **No UiPath integration exists.** There is no `maestro/` directory, no `.xaml`, no
  Orchestrator queue definition, and no Action Center task. UiPath Maestro and Action
  Center are design intent only; `uipath-langchain` is declared as a dependency but never
  imported.
- **No frontend.** Earlier versions of this README described a `frontend/` directory and a
  `frontend/README.md`. Neither exists.
- **Sample scenarios have metadata only.** Each directory under
  `backend/data/samples/` contains `meta.json` and nothing else — no `vendor_claim.json`,
  no contract text, no evidence documents. An earlier version of this README included a
  `curl` command posting a `vendor_claim.json` that is not in the repository.
- **CI passes without testing anything.** `.github/workflows/ci.yml` runs
  `pytest tests/ -v --tb=short || true` against a `tests/` directory that does not exist.
  The `|| true` means the step succeeds regardless, so a green check mark on this repo
  does not indicate working code.
- **Unused dependencies.** `boto3`, `azure-identity`, `azure-storage-blob`, `httpx`,
  `pydantic-settings`, and `openai` are all pinned and none are imported.
- **CORS is wide open.** `allow_origins=["*"]` combined with `allow_credentials=True`,
  with all methods and headers permitted. This must be restricted to a real origin
  allowlist before the service is exposed anywhere.
- **Dependency versions are from late 2023.** `fastapi==0.104.1`, `openai==1.3.0`,
  `pydantic==2.5.0` — these will need updating before the code is extended.

## License

MIT — see [LICENSE](LICENSE).
