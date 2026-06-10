# DAEDALUS AGENT ROLES — Definitions & Responsibilities

**Version:** 1.0  
**Effective:** 2026-06-10  
**Architecture:** 8-role frozen design

---

## ROLE ARCHITECTURE OVERVIEW

```
┌─ MNEMOSYNE (Orchestrator) ──────────────────────┐
│                                                  │
│ ┌──────────────────────────────────────────┐   │
│ │ GITHUB ISSUE LISTENER (Iris bridge)      │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ AEGIS (Safety Gate)                      │   │
│ │ • Sacred object detection                │   │
│ │ • Blocker detection                      │   │
│ │ • Escalation to Themis                   │   │
│ └──────────────────────────────────────────┘   │
│                ↓ [PASS]                         │
│ ┌──────────────────────────────────────────┐   │
│ │ ATHENA (Planner)                         │   │
│ │ • Scope analysis                         │   │
│ │ • Dependency mapping                     │   │
│ │ • Risk assessment                        │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ CHRONOS (Tool Manager)                   │   │
│ │ • Resolve dependencies                   │   │
│ │ • Build toolchain                        │   │
│ │ • Set environment                        │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ CODE GENERATION                          │   │
│ │ (LLM: LiteLLM or Mnemosyne Router)       │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ ARGUS (Reviewer)                         │   │
│ │ • Test execution                         │   │
│ │ • Lint & style check                     │   │
│ │ • Code audit                             │   │
│ │ • Risk classification                    │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ IRIS (Auditor)                           │   │
│ │ • Log all decisions                      │   │
│ │ • GitHub PR comment                      │   │
│ │ • Audit trail creation                   │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ THEMIS (Approval Gate) ⚖️                │   │
│ │ • Risk-level assessment                  │   │
│ │ • Decision (APPROVE/ESCALATE/BLOCK)      │   │
│ │ • Final authority                        │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ MORPHEUS (Memory)                        │   │
│ │ • Trajectory storage                     │   │
│ │ • Pattern learning (future)              │   │
│ │ • Issue archive                          │   │
│ └──────────────────────────────────────────┘   │
│                ↓                                 │
│ ┌──────────────────────────────────────────┐   │
│ │ COMPLETION & REPORTING                   │   │
│ │ • PR created (not merged)                │   │
│ │ • Report posted                          │   │
│ │ • Issue status updated                   │   │
│ └──────────────────────────────────────────┘   │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## DETAILED ROLE DEFINITIONS

### 1. MNEMOSYNE — Orchestrator & Factory Brain

**Purpose:** Coordinate the entire workflow from issue to PR.

**Responsibilities:**
- Listen for new GitHub issues (or manual trigger)
- Dispatch to Aegis for safety check
- Chain each role in sequence
- Catch and handle exceptions
- Notify user of blockers
- Archive completed workflows to Morpheus

**Authority:** Can request any role to run; cannot override decisions

**Constraints:**
- Cannot modify code directly
- Cannot approve/merge
- Cannot write to main branch
- Cannot delete files
- Cannot install dependencies autonomously

**Interface:**
```python
class Mnemosyne:
    def listen_for_issues() -> Issue
    def dispatch_to_aegis(issue: Issue) -> SafetyDecision
    def chain_roles(issue: Issue, safety_ok: bool) -> WorkflowState
    def notify_user(message: str) -> None
    def archive_to_morpheus(trajectory: Trajectory) -> None
```

**Example Flow:**
```
Issue #42 created
  → Mnemosyne.listen_for_issues() finds it
  → dispatch_to_aegis(#42) → "PASS"
  → chain_roles(#42, True) starts Athena
  → ...
  → archive_to_morpheus(full trajectory)
```

---

### 2. THEMIS — Approval Gate & Risk Assessor ⚖️

**Purpose:** Final veto point. No code ships without Themis sign-off.

**Responsibilities:**
- Evaluate all code changes for risk
- Assign risk level (1–5)
- Make decision: APPROVE / ESCALATE / BLOCK
- Post decision to GitHub PR
- Log decision immutably
- Block merge if risk too high

**Authority:**
- Can BLOCK anything
- Cannot be overridden (only Themis can override itself)
- Can escalate to user for urgent safety issues
- Veto is law

**Risk Levels:**
```
Level 1: AUTO-APPROVE
  ├─ Tests, docs, new files
  ├─ No sacred objects
  └─ All tests passing → "Approved"

Level 2: APPROVE + CAUTION
  ├─ Simple feature
  ├─ Low risk
  └─ "Approved with notes"

Level 3: REQUIRES REVIEW
  ├─ Modify existing code
  ├─ Dependency changes
  └─ "Requires human approval" (blocks merge)

Level 4: ESCALATION
  ├─ Touch sensitive areas
  ├─ Auth, storage, secrets
  └─ "ESCALATION REQUIRED" (user notified)

Level 5: BLOCKED
  ├─ Sacred object touch
  ├─ Security violation
  └─ "BLOCKED" (manual override needed)
```

**Interface:**
```python
class Themis:
    def evaluate_risk(pr: PullRequest) -> RiskLevel
    def make_decision(risk: RiskLevel) -> Decision  # APPROVE | ESCALATE | BLOCK
    def post_to_github(pr: PullRequest, decision: Decision) -> None
    def log_decision(pr: PullRequest, decision: Decision) -> AuditEntry
```

**Non-Negotiable:**
- Immutable once deployed
- Cannot be modified by any role
- Decision = final authority
- No merge until Themis approves

---

### 3. AEGIS — Safety Blocker & Gatekeeper

**Purpose:** Detect sacred object touches and unsafe patterns before code runs.

**Responsibilities:**
- Check if issue modifies secrets, auth, storage, main branch
- Detect attempt to delete files
- Detect dependency installs without approval
- Detect attempts to modify Themis/core Daedalus code
- Escalate violations to Themis
- Block unsafe patterns (force-push, autonomous merge, etc.)

**Authority:**
- Can BLOCK at safety gate
- Can escalate to Themis
- Cannot override Themis
- Can request user confirmation

**Safety Stop List (Automatic BLOCK):**
```
1. Modified .env, secrets/*, auth/*
2. Deleted /tasklet/agent/blocks/* or PR history
3. Force-push to main/develop
4. `pip install` without approval
5. Modified Themis state machine code
6. Modify Daedalus core (scaffold only)
7. Production DB write without Themis + human
8. Hidden commits or branches
9. Attempted autonomous merge
10. Modify sacred object list without Themis approval
```

**Interface:**
```python
class Aegis:
    def check_sacred_objects(changes: List[FileChange]) -> SafetyDecision
    def detect_unsafe_patterns(plan: Plan) -> List[Violation]
    def escalate_to_themis(violation: Violation) -> None
    def block(reason: str) -> None
```

**Example:**
```
Issue #50 proposes changes to .env
  → Aegis.check_sacred_objects() → VIOLATION detected
  → escalate_to_themis("Sacred object .env touched")
  → Themis BLOCKS
  → User notified
```

---

### 4. ATHENA — Planner & Analyst

**Purpose:** Understand the issue and plan the solution.

**Responsibilities:**
- Parse GitHub issue (title, description, acceptance criteria)
- Perform scope analysis (what files touched, how many lines)
- Identify dependencies (what needs to be imported, installed)
- Map to Daedalus roles (who will do what)
- Estimate risk and complexity
- Create plan document
- Propose branch name: `feature/{issue-number}-{slug}`

**Authority:** Can request information from user; cannot execute code

**Output Artifacts:**
```
docs/plans/ISSUE_{number}_PLAN.md
├─ Issue summary
├─ Acceptance criteria
├─ Scope (files, LOC estimate)
├─ Dependencies (packages, tools)
├─ Role mapping (Argus → tests, Chronos → tools, etc.)
├─ Risk assessment
├─ Estimated hours
└─ Assumptions & blockers
```

**Interface:**
```python
class Athena:
    def analyze_issue(issue: Issue) -> IssueAnalysis
    def assess_scope(analysis: IssueAnalysis) -> ScopeReport
    def map_dependencies(analysis: IssueAnalysis) -> DependencyGraph
    def create_plan(analysis: IssueAnalysis) -> Plan
    def generate_branch_name(issue: Issue) -> str
```

**Example:**
```
Issue #42: "Add user login form"
  → Athena.analyze_issue() 
  → Scope: 3 files, ~150 LOC, React components
  → Dependencies: react, react-router, axios
  → Risk: Level 2 (new feature, isolated)
  → Plan created: docs/plans/ISSUE_42_PLAN.md
  → Branch: feature/42-user-login
```

---

### 5. CHRONOS — Tool Manager & Dependency Resolver

**Purpose:** Set up the environment and tools needed for coding.

**Responsibilities:**
- Parse dependency list from plan
- Resolve package versions
- Check compatibility
- Load tools (GitHub API, test runner, linter, etc.)
- Set environment variables
- Create virtual environment (if needed)
- Report readiness

**Authority:** Can request approval for dependency install (routed to user)

**Constraints:**
- Cannot install without explicit user approval
- Cannot modify global pip/npm
- Cannot write to production env

**Interface:**
```python
class Chronos:
    def resolve_dependencies(plan: Plan) -> DependencyResolution
    def check_compatibility(deps: List[Dependency]) -> CompatibilityReport
    def load_tools(tool_list: List[str]) -> ToolRegistry
    def setup_environment(resolution: DependencyResolution) -> EnvironmentState
    def report_readiness() -> ReadinessReport
```

**Example:**
```
Plan requires: pytest, requests, pydantic
  → Chronos.resolve_dependencies()
  → Compatibility check: all compatible
  → Load pytest runner, requests HTTP client
  → Setup virtual env (if isolated)
  → Report: "Ready to code"
```

---

### 6. CODE GENERATION (LLM + Mnemosyne)

**Purpose:** Generate code proposal based on plan.

**Method:**
- Use LiteLLM (preferred) or Mnemosyne AI router
- Pass system prompt (role-specific)
- Pass issue analysis and plan
- Return code proposal (no execution yet)
- Log prompt + response (for audit)

**System Prompt Structure:**
```
You are {ROLE_NAME}, a specialized code generator.

Context:
- Issue: {issue summary}
- Plan: {Athena plan}
- Constraints: {safety rules}
- Tests: {test framework}

Generate code that:
1. Satisfies acceptance criteria
2. Passes all tests
3. Follows style guide
4. Has full docstrings
5. Is reviewed by Argus

Return ONLY valid code (no prose).
```

**Constraints:**
- Temperature = 0.0 (deterministic)
- No system prompt modification
- All prompts logged
- LiteLLM required (not direct API)

---

### 7. ARGUS — Code Reviewer & Quality Gatekeeper

**Purpose:** Ensure all code is tested, audited, and ready.

**Responsibilities:**
- Run full test suite on proposal
- Run linter (flake8, black, mypy)
- Perform code audit (security, style, logic)
- Generate coverage report
- Classify risk level
- Create audit log for Iris
- Mark ready/not-ready

**Authority:** Can request code changes; cannot approve/block (Themis decides)

**Output:**
```
reports/audit/ISSUE_{number}_AUDIT.md
├─ Test results (pass/fail count)
├─ Coverage % (target: >80%)
├─ Lint violations (if any)
├─ Code audit (security findings)
├─ Risk classification (1–5)
└─ Recommendation (PASS / NEEDS WORK)
```

**Interface:**
```python
class Argus:
    def run_tests(code: str) -> TestResults
    def run_linter(code: str) -> LintReport
    def audit_security(code: str) -> SecurityAudit
    def calculate_coverage(test_results: TestResults) -> float
    def classify_risk(audit: SecurityAudit, coverage: float) -> RiskLevel
    def mark_ready(status: bool) -> None
```

**Example:**
```
Generated code for login form
  → run_tests() → 12 tests PASS, 0 FAIL
  → run_linter() → 0 violations
  → audit_security() → No SQL injection, XSS safe
  → coverage: 89%
  → classify_risk() → Level 2 (low)
  → "Ready for Themis"
```

---

### 8. IRIS — Auditor & Decision Logger

**Purpose:** Create immutable audit trail and GitHub bridge.

**Responsibilities:**
- Log every decision (Aegis, Athena, Argus, Themis)
- Create GitHub PR comment (formatted, readable)
- Link to issue, plan, audit
- Post Themis decision to PR
- Archive evidence (code, tests, logs)
- Provide traceback on request

**Authority:** Can post to GitHub PR; cannot modify past comments

**Output:**
```
[Iris Audit Trail]
Issue: #42 (Add user login form)
Branch: feature/42-user-login
Status: Waiting for Themis Approval

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AEGIS: Safety check PASSED
   • No sacred objects touched
   • No dangerous patterns

✅ ATHENA: Plan created
   • Scope: 3 files, ~150 LOC
   • Deps: react, axios
   • Risk: Level 2

✅ CHRONOS: Environment ready
   • Dependencies resolved
   • Tools loaded

✅ CODE GENERATION: Complete
   • 2 components generated
   • Full docstrings

✅ ARGUS: Audit passed
   • Tests: 12 PASS
   • Coverage: 89%
   • Risk: Level 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Awaiting Themis Decision
```

**Interface:**
```python
class Iris:
    def log_decision(role: str, decision: str, detail: str) -> None
    def post_github_pr_comment(pr: PullRequest, content: str) -> None
    def archive_evidence(issue: Issue, artifacts: List[Artifact]) -> None
    def generate_audit_trail(issue: Issue) -> AuditTrail
```

---

### 9. MORPHEUS — Memory & Trajectory Storage

**Purpose:** Learn from past workflows; support future issue handling.

**Responsibilities:**
- Store completed trajectories (issue → PR → decision)
- Record patterns (common issue types, typical code paths)
- Archive successful workflows for reference
- Support recall on demand (Mnemosyne can ask)
- Maintain index for pattern matching

**Authority:** Can query and store; cannot execute or decide

**Data Model:**
```
Trajectory {
  issue_number: int
  branch: str
  status: COMPLETED | FAILED
  roles_executed: [str]  # [Aegis, Athena, Chronos, ...]
  decisions: [Decision]
  code_generated: str
  tests_passed: int
  themis_decision: Decision
  time_elapsed: float
  lessons_learned: str
  errors: [str]
}
```

**Interface:**
```python
class Morpheus:
    def store_trajectory(trajectory: Trajectory) -> None
    def recall_similar_issues(current_issue: Issue) -> List[Trajectory]
    def extract_patterns(trajectories: List[Trajectory]) -> Patterns
    def suggest_approach(issue: Issue) -> SuggestedApproach
```

**Example:**
```
Mnemosyne asks Morpheus:
  "Have we done login forms before?"
  
Morpheus recalls:
  • Issue #10: Login form (2026-05-15) ✓ PASSED
  • Issue #22: OAuth login (2026-05-28) ✓ PASSED
  
Suggests:
  "Use React form pattern from #10; add OAuth step from #22"
```

---

## ROLE INTERACTION MATRIX

| From → To | Aegis | Athena | Chronos | Argus | Iris | Themis | Morpheus |
|-----------|-------|--------|---------|-------|------|--------|----------|
| **Mnemosyne** | ✓ dispatch | ✓ dispatch | ✓ dispatch | ✓ dispatch | ✓ dispatch | ✓ dispatch | ✓ store |
| **Aegis** | — | — | — | — | ✓ escalate | ✓ escalate | — |
| **Athena** | — | — | ✓ request | — | ✓ log | — | ✓ query |
| **Chronos** | — | — | — | — | ✓ log | — | — |
| **Argus** | — | — | — | — | ✓ log audit | — | — |
| **Iris** | — | — | — | — | — | ✓ posts decision | ✓ archives |
| **Themis** | — | — | — | — | ✓ log | — | — |

**Key Rules:**
- Roles cannot modify each other's outputs
- Only escalation up the chain (Aegis → Themis, Athena → Iris)
- Morpheus is read-only for other roles
- Mnemosyne orchestrates; never executes alone
- Themis decision is final

---

## DEPLOYMENT ROLES (Future)

Once Daedalus V1.0 ships with autonomous merge capability:

- **Hermes** — Merge coordinator (not yet deployed)
- **Apollo** — Deployment validator (not yet deployed)
- **Hades** — Rollback manager (not yet deployed)

V0.1 explicitly excludes these roles.

---

## ROLE EVOLUTION TIMELINE

| Milestone | Roles | Focus |
|-----------|-------|-------|
| **V0.1 (NOW)** | 8 roles | Issue → PR (no merge) |
| **V0.2** | +Chronos enhancements | Tool chains, secrets mgmt |
| **V0.3** | +Morpheus learning | Pattern detection, recall |
| **V1.0** | +Hermes, Apollo, Hades | Merge, deploy, rollback |
| **V2.0** | +distributed roles | Multi-agent orchestration |

---

**Role Architecture Complete & Frozen**  
*No changes without constitutional amendment*

*Version 1.0 — Ready for Themis Review*
