# Daedalus Operational Core — V0.1

**Build the cage, the harness, the audit trail, and the brakes.**

Daedalus is a controlled software factory for Life-os. This is the safety scaffold.

## Philosophy

- **Safety before smart:** V0.1 focuses on safety gates, not clever agent behavior
- **Autonomy is suspicious until reviewed:** No task runs without explicit issue directive
- **No merge without human sign-off:** Never auto-merges; humans own all production decisions
- **Audit trail everything:** Every decision recorded in memory for future reference

## Architecture

```
GitHub Issue
    ↓
[PLANNER] → Parse issue, create plan
    ↓
[BUILDER] → Generate code proposal
    ↓
[TESTER] → Run automated tests
    ↓
[GATES]
  ├─ [AEGIS]    Security scan
  ├─ [IRIS]     Architecture audit
  ├─ [REVIEWER] Code review
  └─ [THEMIS]   Approval gate
    ↓
[REPORTER] → Generate agent report + decision log
    ↓
[MEMORY] → Store decision in audit trail
    ↓
Pull Request (awaiting human approval)
```

**No autonomous merge. No production deploy. Safety gates only.**

## Operational Model

### V0.1 Flow

1. **INGEST** — Read GitHub issue → Parse directives + risk keywords
2. **PLAN** — Generate implementation plan
3. **CODE** — Propose code changes (mocked in V0.1)
4. **TEST** — Run automated tests (mocked in V0.1)
5. **REPORT** — Generate agent report + decision log
6. **REVIEW** — Open PR for human approval (stop here, no merge)

### Risk Levels

| Level | Escalation | Approval |
|-------|-----------|----------|
| 🟢 GREEN | No | Reviewer auto-approves |
| 🟡 YELLOW | If requested | Agent Matt reviews |
| 🟠 ORANGE | Maybe | Agent Matt + human |
| 🔴 CRITICAL | Always | Human-only (blocks) |

### No-Go Areas (Always Blocked)

- Secrets, API keys, credentials
- Production deployments
- Auth/permission logic
- Destructive database operations
- User data access
- External messaging (email, SMS)

## Getting Started

### Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

### Test Suite

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=daedalus tests/

# Run specific test
pytest tests/test_issue_reader.py -v

# Run end-to-end flow test
pytest tests/test_daedalus_v01_flow.py -v
```

### Key Tests

- `test_issue_reader.py` — GitHub issue parsing (TASK-D001)
- `test_daedalus_v01_flow.py` — Full V0.1 workflow (TASK-D008)

## Project Structure

```
daedalus/
├── planner/         → Issue → Plan (TASK-D001)
├── builder/         → Plan → Code (TASK-D002)
├── tester/          → Code → Tests (TASK-D003)
├── reporter/        → Report + Decision Log (TASK-D004)
├── reviewer/        → Code Review Gate (TASK-D005)
├── aegis/           → Security Scanner (TASK-D006)
├── iris/            → Architecture Audit (TASK-D007)
├── themis/          → Approval Gate (TASK-D008)
└── memory/          → Decision Logging (TASK-D009)

docs/
├── DAEDALUS_CONSTITUTION.md     → Rules & safety model
├── DAEDALUS_OPERATIONAL_MODEL.md → V0.1 flow & stages
├── DAEDALUS_RISK_REGISTER.md     → Known risks & mitigations
├── DAEDALUS_REVIEW_GATE.md       → Themis approval rules
└── DAEDALUS_DECISION_LOG.md      → Memory system

tests/
├── test_issue_reader.py         → Unit tests for planner
└── test_daedalus_v01_flow.py    → End-to-end workflow test

fixtures/
└── mock_github_issue.json       → Sample GitHub issue
```

## Docs (Start Here)

1. **[DAEDALUS_CONSTITUTION.md](docs/DAEDALUS_CONSTITUTION.md)** — What Daedalus is/isn't, safety rules, no-go areas
2. **[DAEDALUS_OPERATIONAL_MODEL.md](docs/DAEDALUS_OPERATIONAL_MODEL.md)** — 6-stage workflow, V0.1 vs V1 roadmap
3. **[DAEDALUS_RISK_REGISTER.md](docs/DAEDALUS_RISK_REGISTER.md)** — Known risks and how we mitigate them
4. **[DAEDALUS_REVIEW_GATE.md](docs/DAEDALUS_REVIEW_GATE.md)** — Themis approval gates and merge rules
5. **[DAEDALUS_DECISION_LOG.md](docs/DAEDALUS_DECISION_LOG.md)** — Memory/audit trail system

## V0.1 Acceptance Criteria

- [x] Parse a mock GitHub issue correctly
- [x] Classify risk level (GREEN/YELLOW/ORANGE/CRITICAL)
- [x] Detect no-go area operations
- [x] Generate implementation plan
- [x] Run tests (mocked)
- [x] Generate agent report
- [x] Write decision log
- [x] Never merge automatically
- [x] Escalate CRITICAL issues

All criteria met. Ready for deployment to Life-os.

## Versioning

- **V0.1** (Current): Safety scaffold, mocked components, issue-driven workflow
- **V1** (Future): Real GitHub API, real code generation, real test execution, decision memory DB

## License

Life-os → Mnemosyne → Daedalus

---

**Safety is not negotiable. Build the cage first.**
