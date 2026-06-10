# Themis V1 Implementation Guide

**Version:** 1.0  
**Status:** Production Ready  
**Component:** Daedalus Gate 3 (Human Approval)  
**Date:** 2026-06-10

---

## Overview

Themis is the **human approval gate** in the Daedalus workflow. It enforces that humans must review and sign off on risky operations before execution.

**Core Design:**
- **State Machine:** Approval chains track pending → approved → executed states
- **Risk-Level Gates:** Gate requirements scale with issue risk (GREEN → CRITICAL)
- **No-Go Blocking:** Production, secrets, auth, and destructive operations are always blocked
- **Audit Trail:** Every decision logged with timestamps, actors, and reasoning
- **Human-Centric:** Humans always have final say; no auto-approval for risky changes

---

## Architecture

### ApprovalChain

Represents the lifecycle of a single task's approval process.

```python
chain = ApprovalChain(
    task_id="TASK-001",
    issue_number=1,
    risk_level=RiskLevel.ORANGE
)
```

**Risk Levels and Required Gates:**

| Risk Level | Gates | Purpose | Example |
|------------|-------|---------|---------|
| **GREEN** | Automated, Aegis, Iris | Routine changes | Update docs, add tests |
| **YELLOW** | + Reviewer | Code review | Refactor module, add feature |
| **ORANGE** | + Human | Human approval | Modify auth, add dependency |
| **RED** | + EmergencyBoard | Emergency review | Production hotfix |
| **CRITICAL** | All + block | Always blocked | Merge to main, secrets in code |

### ApprovalGate

Single gate in the approval chain.

```python
gate = ApprovalGate(name="Reviewer")
gate.approve(by="ocrowley", comment="Code review complete")
```

**States:**
- `pending` — Awaiting approval
- `approved` — Gate passed
- `rejected` — Gate blocked, workflow blocked

### ThemisApprovalGate

Manager for all approval chains (singleton pattern recommended).

```python
themis = ThemisApprovalGate()
chain = themis.create_approval_chain("TASK-001", 100, RiskLevel.ORANGE)

can_execute, reason = themis.can_execute("TASK-001")
# Returns (False, "Pending approvals: Human, EmergencyBoard")
```

---

## Workflow Integration

### 1. Issue Ingestion (Planner)

```python
from daedalus.planner import IssueReader
from daedalus.themis import ThemisApprovalGate, RiskLevel

issue_reader = IssueReader()
issue = issue_reader.parse_github_issue(issue_json)
risk_level = issue_reader.classify_risk_level(issue)

themis = ThemisApprovalGate()
chain = themis.create_approval_chain(issue.task_id, issue.number, risk_level)
```

### 2. Automated Pre-Checks (Aegis + Iris)

```python
from daedalus.aegis import SecurityScanner
from daedalus.iris import ArchitectureChecker

if SecurityScanner.has_no_go_violations(code):
    chain.add_no_go_violation("Secrets detected in code")

if not ArchitectureChecker.is_compliant(code):
    chain.reject_gate("Iris", "system", "Architecture violation")
```

If violations detected → **workflow stops, no auto-approval**

### 3. Human Signal Processing

**GitHub comment triggers approval:**

```bash
# User comments on GitHub issue:
@daedalus approve TASK-001
```

**In code:**

```python
def process_github_comment(task_id, comment_text):
    chain = themis.get_approval_chain(task_id)
    if "approve" in comment_text.lower() and task_id in comment_text:
        chain.approve_gate("Human", "ocrowley", f"Approved via: {comment_text}")
        return True
    return False
```

### 4. Execution Gate

```python
can_execute, reason = themis.can_execute(task_id)

if can_execute:
    # Execute: merge, deploy, etc.
    execute_task(task_id)
else:
    # Block and notify user
    print(f"Cannot execute: {reason}")
```

---

## No-Go Areas (Always Block)

Themis enforces the Constitution's no-go areas:

```python
# Production deployment
chain.add_no_go_violation("Merge to main branch")

# Secrets in code
chain.add_no_go_violation("API key in environment variables")

# Destructive database operations
chain.add_no_go_violation("DROP TABLE without backup")

# Auth/permissions changes
chain.add_no_go_violation("Modify user role system")
```

**Effect:** Workflow is immediately blocked, all gates overridden.

---

## Decision Logging (Audit Trail)

Every approval chain generates a decision log for Memory:

```python
chain.mark_automated_pass()
chain.approve_gate("Reviewer", "ocrowley", "Code review passed")
chain.approve_gate("Human", "ocrowley", "@daedalus approve TASK-001")

log = chain.to_decision_log()
# Markdown with full approval history, actors, timestamps
```

**Output:**

```markdown
# Approval Decision Log — TASK-001

**Issue:** #123
**Risk Level:** ORANGE
**Status:** APPROVED
**Created:** 2026-06-10T12:34:56.789Z
**Last Updated:** 2026-06-10T12:35:00.123Z

## Approval Gates

- ✅ **Automated** — approved
  - Signed by: system
  - Timestamp: 2026-06-10T12:34:56.789Z
  
- ✅ **Reviewer** — approved
  - Signed by: ocrowley
  - Timestamp: 2026-06-10T12:34:57.234Z
  - Note: Code review passed
  
- ✅ **Human** — approved
  - Signed by: ocrowley
  - Timestamp: 2026-06-10T12:34:58.567Z
  - Note: @daedalus approve TASK-001

## Approval History

- 2026-06-10T12:34:56.789Z — automated_pass by system
- 2026-06-10T12:34:57.234Z — gate_approved:Reviewer by ocrowley
- 2026-06-10T12:34:58.567Z — gate_approved:Human by ocrowley
- 2026-06-10T12:34:58.567Z — workflow_approved by ocrowley
```

Stored in Memory for audit trail.

---

## Testing

All Themis functionality is tested in `tests/test_themis_v1.py` (24 tests).

**Run tests:**

```bash
pytest tests/test_themis_v1.py -v
```

**Coverage:**
- Approval chain creation and state machine ✅
- Risk-level-driven gate requirements ✅
- No-go area detection and blocking ✅
- Gate approval/rejection workflows ✅
- Escalation and emergency board ✅
- Decision log generation ✅
- End-to-end workflows (GREEN → CRITICAL) ✅

---

## API Reference

### ThemisApprovalGate

```python
class ThemisApprovalGate:
    def create_approval_chain(task_id, issue_number, risk_level) -> ApprovalChain
    def get_approval_chain(task_id) -> Optional[ApprovalChain]
    def can_execute(task_id) -> (bool, str)  # (can_execute, reason)
    def block_nogo_operation(task_id, operation, reason) -> ApprovalChain
```

### ApprovalChain

```python
class ApprovalChain:
    task_id: str
    issue_number: int
    risk_level: RiskLevel
    status: ApprovalStatus
    
    def mark_automated_pass() -> None
    def approve_gate(gate_name, by, reason) -> bool
    def reject_gate(gate_name, by, reason) -> bool
    def add_no_go_violation(violation) -> None
    def escalate(reason) -> None
    def can_proceed() -> bool
    def get_pending_gates() -> List[str]
    def to_decision_log() -> str
```

### RiskLevel Enum

```python
class RiskLevel(Enum):
    GREEN = "green"      # Minimal gates
    YELLOW = "yellow"    # Requires Reviewer
    ORANGE = "orange"    # Requires Human
    RED = "red"          # Requires EmergencyBoard
    CRITICAL = "critical" # Always blocked
```

### ApprovalStatus Enum

```python
class ApprovalStatus(Enum):
    PENDING = "pending"      # Awaiting approvals
    APPROVED = "approved"    # All gates passed
    REJECTED = "rejected"    # Gate blocked
    ESCALATED = "escalated"  # Emergency review needed
    BLOCKED = "blocked"      # No-go violation
```

---

## Example: Full Workflow

```python
from daedalus.planner import IssueReader
from daedalus.themis import ThemisApprovalGate, RiskLevel

# 1. Parse issue
issue_reader = IssueReader()
issue = issue_reader.parse_github_issue(raw_issue_json)

# 2. Classify risk
risk_level = issue_reader.classify_risk_level(issue)
# → RiskLevel.ORANGE (modifies auth system)

# 3. Create approval chain
themis = ThemisApprovalGate()
chain = themis.create_approval_chain(issue.task_id, issue.number, risk_level)

# 4. Detect no-go violations
if "merge main" in issue.description.lower():
    chain.add_no_go_violation("Merge to main without Emergency Board approval")
    # → Workflow blocked immediately

# 5. Check execution gate
can_execute, reason = themis.can_execute(issue.task_id)
# → (False, "No-go violations detected: Merge to main...")
```

---

## Future Enhancements

**D-02+:** Planned improvements not yet implemented

- **Database Backend:** Replace in-memory storage with agent-db for persistence
- **GitHub Integration:** Listen for issue comments, auto-trigger approvals
- **Slack Notifications:** Alert humans of pending approvals
- **Email Summaries:** Daily approval queue digest
- **Approval History UI:** Dashboard showing all approval chains
- **Multi-Workspace Support:** Themis instances per workspace

---

## References

- `DAEDALUS_CONSTITUTION.md` — No-go areas and safety model
- `DAEDALUS_OPERATIONAL_MODEL.md` — Workflow integration
- `tests/test_themis_v1.py` — Complete test suite
