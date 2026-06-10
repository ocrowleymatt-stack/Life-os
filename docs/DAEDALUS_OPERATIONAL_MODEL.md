# Daedalus Operational Model

**Version:** 0.1  
**Status:** V0.1 Flow (Issue → Plan → Code → Test → Report → PR)  
**Deployment Target:** Life-os (not production)

---

## Overview

Daedalus operates in **discrete, issue-driven tasks**. Each task flows through 6 stages:

```
1. INGEST       GitHub Issue → Parse directives
2. PLAN         Create implementation plan
3. CODE         Generate code proposal
4. TEST         Run automated tests
5. REPORT       Generate agent report + decision log
6. REVIEW       Open PR, await human approval
```

**No autonomous merge. No production deploy. No real secrets.**

---

## Stage 1: Ingest

### Input
GitHub issue with:
- Title (task directive)
- Description (requirements, constraints)
- Labels (optional: risk level, component)
- Assignee (human reviewer)

### Process
- Parse issue title + description
- Extract:
  - Acceptance criteria
  - Files/modules affected
  - Risk keywords (auth, deploy, secrets, etc.)
  - Constraints (no production, testing only, etc.)
- Output: Parsed issue object (JSON)

### Output
```json
{
  "issue_id": "D001",
  "title": "Add GitHub issue reader",
  "risk_level": "YELLOW",
  "modules_affected": ["planner", "aegis"],
  "requirements": [...],
  "constraints": [...],
  "escalate_if": "..."
}
```

---

## Stage 2: Plan

### Input
Parsed issue object

### Process
- Daedalus planner creates implementation plan:
  - High-level approach
  - Files to create/modify
  - Test strategy
  - Estimated risk
  - Known blockers

### Output
```markdown
# Implementation Plan — TASK-D001

## Approach
1. Create `/daedalus/planner/issue_reader.py`
2. Parse GitHub issue JSON
3. Extract directives + risk keywords
4. Output parsed issue object

## Files Affected
- daedalus/planner/issue_reader.py (new)
- daedalus/planner/__init__.py (modify)
- tests/test_issue_reader.py (new)

## Tests Required
- Unit: Parse valid GitHub issue
- Unit: Detect risk keywords
- Unit: Handle malformed input

## Risk Assessment
- Risk Level: YELLOW
- No no-go areas detected
- Requires: Code review (no human escalation)

## Blockers
- None identified
```

---

## Stage 3: Code

### Input
Implementation plan

### Process
- Daedalus builder generates code:
  - Create/modify files per plan
  - Add docstrings + comments
  - Follow repo style guide
  - No dead code

### Output
- Modified/created files staged in branch
- Code is ready for testing
- No syntax errors (validated locally)

---

## Stage 4: Test

### Input
- Code changes
- Test files

### Process
- Run all tests for affected modules
- Generate coverage report
- Validate:
  - ✅ Unit tests pass
  - ✅ Integration tests pass
  - ✅ Coverage ≥80%
  - ✅ No security issues detected

### Output
```
Test Results: PASS
├── Unit Tests: 12/12 ✅
├── Coverage: 92%
├── Security Scan: No issues
└── Ready for review
```

If any test fails:
- ❌ Stop here
- 🔴 Report failure
- 📝 Escalate to human for guidance

---

## Stage 5: Report

### Input
- Test results
- Code changes
- Decision log

### Process
- Generate agent report:
  - Summary of changes
  - Risk classification
  - Test results
  - Approval gate status
  - Decision log entry

### Output
`AGENT_REPORT_TASK-DXXX.md`:

```markdown
# Agent Report — TASK-D001

## Summary
Added GitHub issue reader to ingest task directives.

## Changes
- Created `daedalus/planner/issue_reader.py`
- Created `tests/test_issue_reader.py`
- Modified `daedalus/planner/__init__.py`

## Risk Classification
**Level:** YELLOW (medium risk)
- Code review required
- No no-go areas detected
- Aegis: ✅ PASS
- Iris: ✅ PASS
- Themis: Awaiting reviewer

## Test Results
- Unit: 12/12 ✅
- Integration: N/A
- Coverage: 92% ✅
- Security: ✅ PASS

## Decision Log
[See DECISION_LOG_TASK-D001.md]

## Gates
1. ✅ Automated tests: PASS
2. ✅ Aegis security: PASS
3. ✅ Iris architecture: PASS
4. ⏳ Themis approval: PENDING

## Recommendation
Ready for review and merge (post-approval).
```

---

## Stage 6: Review

### Input
- PR with code + report + decision log
- GitHub PR checks

### Process
- Open PR on `feature/daedalus-operational-core`
- Reviewer gate:
  1. **Automated tests** (CI/CD): Must pass
  2. **Aegis check**: Must pass (no CRITICAL flagged)
  3. **Iris audit**: Must pass (architecture OK)
  4. **Themis approval**: Reviewer agent or Agent Matt reviews

- If CRITICAL or HIGH risk: Agent Matt + human approval required
- If YELLOW or GREEN: Reviewer agent can approve

### Output
- ✅ PR approved (human reviews description + decision log)
- ❌ PR rejected (human requests changes or escalates)

**No merge without human sign-off on risky changes.**

---

## V0.1 Full Flow Example

### Issue Input
```
Title: Add GitHub issue reader
Description:
  Create a module to ingest GitHub issues and extract task directives.
  
  Requirements:
  - Parse issue title + description
  - Extract acceptance criteria
  - Detect risk keywords (auth, deploy, secrets)
  - Output structured task object
  
  Constraints:
  - No production code
  - Test-only
```

### Flow Execution

**Stage 1: Ingest**
```
✅ Parsed issue D001
Risk: YELLOW (code review needed)
Modules: planner, aegis
```

**Stage 2: Plan**
```
✅ Generated implementation plan
Files: 3 (1 new, 1 modified, 1 test)
Tests: 3 unit tests required
```

**Stage 3: Code**
```
✅ Generated code
Lines: 120 new
Style: ✅ OK
Syntax: ✅ OK
```

**Stage 4: Test**
```
✅ All tests passed
Coverage: 92%
Security: ✅ OK
```

**Stage 5: Report**
```
✅ Generated AGENT_REPORT_TASK-D001.md
Decision log: DECISION_LOG_TASK-D001.md
Recommendation: Ready for review
```

**Stage 6: Review**
```
✅ Opened PR #1 on feature/daedalus-operational-core
Awaiting Themis approval
```

---

## Mocked Components (V0.1)

For testing without live GitHub:

- **Mock GitHub Issue:** JSON fixture in `/daedalus/fixtures/`
- **Mock Planner:** Predefined implementation plan template
- **Mock Builder:** Code generation from template + substitutions
- **Mock Tester:** Fixed pytest output (success/failure scenarios)
- **Mock Reporter:** Template-based report generation
- **Mock Decision Log:** Structured memory entry template

---

## Error Handling

### If Plan Fails
→ Stop, escalate to human with reason

### If Code Generation Fails
→ Stop, report syntax/logic error

### If Tests Fail
→ Stop, report which tests failed + coverage gap
→ Escalate to human for guidance on fix

### If Aegis Detects CRITICAL
→ Refuse operation, log violation, escalate immediately

### If Iris Detects Architecture Violation
→ Stop, request human clarification on requirements

### If Themis Approval Denied
→ Accept feedback, wait for human instruction

---

## V0.1 vs V1 Roadmap

**V0.1 (This Release)**
- ✅ Issue ingest
- ✅ Plan generation
- ✅ Code proposal (mocked)
- ✅ Test runner (mocked)
- ✅ Report + decision log
- ✅ PR creation (mocked)
- ❌ No merge
- ❌ No production

**V1 (Future)**
- ✅ Real GitHub API integration
- ✅ Real code generation (not templates)
- ✅ Real test execution
- ✅ Architecture checker (real validation)
- ✅ Design system checker
- ✅ Security/privacy checker
- ✅ Review gate orchestration
- ✅ Decision memory database
- ✅ Risk escalation automation

---

## Success Metrics (V0.1)

For EPIC D-01 to be "done":

- [ ] Parse a mock GitHub issue correctly
- [ ] Generate an implementation plan
- [ ] Propose code changes (mocked)
- [ ] Run tests and report results (mocked)
- [ ] Classify task risk correctly
- [ ] Refuse CRITICAL operations
- [ ] Generate agent report
- [ ] Write decision log
- [ ] Open PR without merging
- [ ] All 8 tasks (D001–D008) tested

