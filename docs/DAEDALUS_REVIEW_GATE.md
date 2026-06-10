# Daedalus Review Gate (Themis)

**Version:** 0.1  
**Status:** PR Review & Approval Flow  
**Guardians:** Reviewer Agent → Agent Matt → Human (escalation only)

---

## Overview

**Themis** is the approval gate. No code merges to `feature/daedalus-operational-core` (or beyond) without passing Themis.

Themis is **layered**:

```
1. Automated Checks (CI/CD)
   ↓
2. Aegis Security Scan
   ↓
3. Iris Architecture Audit
   ↓
4. Reviewer Agent (code review)
   ↓
5. Agent Matt (risky ops check)
   ↓
6. Human (if CRITICAL or escalated)
```

**No skip. No bypass.**

---

## Gate 1: Automated Checks

### Run On
- Every push to feature branch
- PR creation

### Checks
- ✅ Syntax validation (Python, JSON, YAML)
- ✅ Linting (black, flake8, eslint)
- ✅ Formatting (isort, prettier)
- ✅ Unit tests (pytest)
- ✅ Test coverage report (≥80%)
- ✅ Type checking (mypy, if applicable)

### Pass Criteria
- All checks pass (green status)
- No syntax errors
- No critical linting violations
- Coverage ≥80%

### Failure Action
- ❌ PR blocked
- 📝 Report specific failures
- 🔴 Cannot proceed to Aegis

### Owner
CI/CD system (GitHub Actions)

---

## Gate 2: Aegis (Security Scan)

### Run On
- Post-automated checks
- Before code review

### Scans For
- Secret patterns (API keys, tokens, passwords)
- Dangerous functions (eval, exec, dangerously_set_inner_html)
- No-go area violations (auth changes, production paths, etc.)
- Hardcoded credentials
- SQL injection vectors

### Pass Criteria
- No CRITICAL security issues
- No secret patterns detected
- No no-go area operations
- All code authenticated/authorized properly

### Failure Action
- 🔴 **CRITICAL:** PR blocked immediately
  - Cannot be overridden
  - Requires human to file new issue with explicit approval
- 🟠 **HIGH:** Flagged for review
  - Reviewer must approve
  - Cannot merge without explicit acknowledgment

### Owner
Aegis module + Daedalus reporter

---

## Gate 3: Iris (Architecture Audit)

### Run On
- Post-Aegis
- Before code review

### Checks
- Design system compliance (component usage, styling)
- Module boundary violations (separation of concerns)
- Dependency rules (no circular imports)
- API consistency (naming, patterns)
- Testability (mocking boundaries, isolation)

### Pass Criteria
- No architecture violations
- Design system respected
- Tests follow module structure
- Documentation updated (if applicable)

### Failure Action
- 🟠 **Architecture Issue:** Flagged for review
  - Reviewer discusses with builder
  - Can request changes or approve with notes
  - Cannot merge without agreement on design

### Owner
Iris module + code review

---

## Gate 4: Reviewer Agent (Code Review)

### Run On
- Post-Iris
- Before human approval

### Reviews
- Code quality (readability, naming, comments)
- Test coverage (are tests thorough?)
- Logic correctness (does it do what it claims?)
- Edge cases (error handling, boundary conditions)
- Performance (any obvious inefficiencies?)

### Decision Tree

```
Does code pass Aegis + Iris?
├─ NO → Reject, request changes
├─ YES
   ├─ Risk Level GREEN?
   │  └─ AUTO-APPROVE (no human review needed)
   ├─ Risk Level YELLOW?
   │  └─ Request Agent Matt review
   ├─ Risk Level ORANGE?
   │  └─ Escalate (human review required)
   └─ Risk Level CRITICAL?
      └─ BLOCK (human approval only)
```

### Pass Criteria
- Code meets quality standards
- Tests are thorough
- Logic is correct
- Matches acceptance criteria from issue

### Failure Action
- 🔴 Request changes (PR marked as "Review changes requested")
- 📝 Specific feedback to builder
- Builder can update code; re-runs all gates

### Owner
Reviewer Agent (Daedalus reviewer module)

---

## Gate 5: Agent Matt (Risk Review)

### Triggered By
- YELLOW risk level tasks
- ORANGE tasks (must review)
- Any escalation from Aegis/Iris/Reviewer

### Reviews
- Does this actually solve the issue?
- Are there simpler approaches?
- Any architectural concerns?
- Any edge cases the tests missed?
- Risk mitigation: Is it adequate?

### Decision
- ✅ Approve (sign off on risk)
- 🤔 Request changes
- ❌ Escalate to human

### Pass Criteria
- Agent Matt approves
- Risk is acceptable for the scope
- Mitigation plan documented

### Failure Action
- Request changes or escalate to human
- No merge without sign-off for risky changes

### Owner
Agent Matt (autonomous approval agent)

---

## Gate 6: Human Approval (Final Gate)

### Triggered By
- ORANGE risk level
- CRITICAL risk detected
- Escalation from Agent Matt
- Explicit issue request

### Reviews
- Final sign-off on risk
- Does this align with product strategy?
- Any concerns about execution?

### Decision
- ✅ Approve & merge
- 🤔 Request changes
- ❌ Reject (do not merge)

### Pass Criteria
- Human explicitly approves
- All gates passed
- Decision log written
- No concerns raised

### Failure Action
- PR stays open; no merge
- Human provides feedback
- Builder can update; resubmit for review

### Owner
Human (user/Agent Matt override)

---

## Risk Level → Approval Path

| Risk Level | Automated | Aegis | Iris | Reviewer | Agent Matt | Human | Result |
|------------|-----------|-------|------|----------|-----------|-------|--------|
| 🟢 GREEN | ✅ | ✅ | ✅ | ✅ Auto-approve | — | — | Auto-merge (if human enabled auto-merge) |
| 🟡 YELLOW | ✅ | ✅ | ✅ | ✅ Approve | ✅ Approve | — | Can merge |
| 🟠 ORANGE | ✅ | ✅ | ✅ | ✅ Approve | ✅ Approve | ✅ Approve | Can merge |
| 🔴 CRITICAL | ✅ | 🔴 BLOCK | — | — | — | 🔴 HUMAN ONLY | Cannot merge (requires human override + new issue) |

---

## Review Checklist Template

Reviewer uses this checklist:

```markdown
## Themis Review Checklist

### Automated Gates
- [ ] Syntax validation: PASS
- [ ] Linting: PASS
- [ ] Tests: PASS (coverage ≥80%)

### Aegis (Security)
- [ ] No secret patterns detected
- [ ] No dangerous functions
- [ ] No no-go areas touched
- [ ] Status: ✅ PASS

### Iris (Architecture)
- [ ] Design system respected
- [ ] Module boundaries intact
- [ ] No circular dependencies
- [ ] Status: ✅ PASS

### Code Quality
- [ ] Code is readable
- [ ] Comments explain intent
- [ ] Tests are thorough
- [ ] Edge cases handled

### Risk & Mitigation
- [ ] Risk classified: [GREEN/YELLOW/ORANGE/CRITICAL]
- [ ] Mitigation plan adequate
- [ ] Issue requirements met
- [ ] No blockers identified

### Decision
- [ ] Approve (merge OK after gates pass)
- [ ] Request changes (specify)
- [ ] Escalate to human (reason)

Reviewer: [Agent/Human]
Date: [timestamp]
```

---

## Escalation Path

If Reviewer or Agent Matt escalates:

```
Escalation Detected
├─ Reason: [ambiguity/blocker/CRITICAL/override needed]
├─ PR: [GitHub URL]
├─ Issue: [Issue #]
└─ Action: Send message to human
   ├─ Problem summary
   ├─ Options (if applicable)
   ├─ Recommendation
   └─ Urgent? (yes → follow up in 2h)
```

Human responds:
- Approves with notes → Merge OK
- Requests changes → Builder updates, re-review
- Rejects → PR closed, issue amended

---

## Merge Rules (V0.1)

### When Can Code Merge?

1. **All gates passed** (Automated, Aegis, Iris, Reviewer)
2. **Risk level determined:**
   - GREEN: Auto (if enabled) or Reviewer auto-approves
   - YELLOW: Agent Matt approves
   - ORANGE: Human approves
   - CRITICAL: Cannot merge (issue must be rewritten)
3. **Decision log written** (DECISION_LOG_TASK-DXXX.md)
4. **PR ready** (all conversations resolved)

### Who Can Merge?

- ✅ Human (always allowed if gates pass)
- ✅ Reviewer Agent (GREEN risk only, auto-enabled)
- ✅ Agent Matt (YELLOW risk approved)
- ❌ Daedalus (never)
- ❌ Automated (never)

### Cannot Merge If:

- ❌ Any gate is failing
- ❌ Risk is CRITICAL
- ❌ Human explicitly rejected
- ❌ Decision log missing
- ❌ Tests <80% coverage

---

## Decision Log Format

Every PR must include a decision log:

**File:** `DECISION_LOG_TASK-D001.md`

```markdown
# Decision Log — TASK-D001

## Issue
GitHub Issue #X: [Issue title]

## Decision Made
[What was built / changed]

## Why
[Reasoning / trade-offs considered]

## Risk Classification
- Level: [GREEN/YELLOW/ORANGE/CRITICAL]
- Mitigations: [How risks addressed]

## Files Changed
- daedalus/planner/issue_reader.py (new, 120 lines)
- tests/test_issue_reader.py (new, 80 lines)
- daedalus/planner/__init__.py (modified, +2 lines)

## Tests
- Unit: 12 tests, all pass ✅
- Coverage: 92%
- Integration: N/A

## Approval Status
- Aegis: ✅ PASS
- Iris: ✅ PASS
- Reviewer: ✅ APPROVE
- Agent Matt: ✅ APPROVE
- Human: ⏳ PENDING

## Next Steps
[What comes after this task]

## Sign-Off
- Builder: Daedalus (auto)
- Reviewer: [Agent/Human]
- Approved: [Human] (date/time)
```

---

## Metrics & Monitoring

### Track per PR:
- Time from issue to PR: ___ minutes
- Gates passed/failed: ___ / ___
- Risk escalations: ___ (how many)
- Changes requested: ___ (iterations)
- Merge time: ___ hours
- Decision log quality: [Good/Fair/Poor]

### Success Targets (V0.1):
- 100% of PRs pass all automated gates
- 0 CRITICAL security issues missed
- ≥80% test coverage maintained
- ≤3 iterations per PR (changes requested)
- Decision log complete on all PRs

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-06-10 | Initial Themis review gate for V0.1 |

